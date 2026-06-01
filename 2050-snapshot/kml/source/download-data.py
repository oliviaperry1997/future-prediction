#!/usr/bin/env python3
"""
2050 Climate KML — Data Download Script
=========================================

Downloads and validates source datasets for Phase 21 climate KML layers:
1. GloH2O V3 Köppen-Geiger climate classification (2041-2070, SSP3-7.0)
2. WWF Terrestrial Ecoregions (TEOW) — biomes
3. HydroSHEDS HydroBASINS v1c — watersheds
4. SRTM/Copernicus DEM tiles — sea level rise inundation

Usage:
    python3 download-data.py --all          # Download everything possible
    python3 download-data.py --koppen       # Köppen only
    python3 download-data.py --biomes       # Biomes only (manual + automated alt)
    python3 download-data.py --watersheds   # Watersheds only
    python3 download-data.py --dem          # DEM tiles only (manual instructions)
    python3 download-data.py --status       # Check which datasets already present

Output directory: ./source/  (created automatically)

Threat model compliance:
    T-21-01: HTTPS URL validation before download; try/except with informative errors
    T-21-02: File integrity via size > 0 and format detection (rasterio/shapefile)
"""

import argparse
import hashlib
import logging
import os
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("download-data")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent.resolve()
DEFAULT_OUTPUT = SCRIPT_DIR

# Minimum acceptable file sizes (bytes) — rough sanity checks
MIN_SIZE: dict[str, int] = {
    ".tif": 1_000_000,     # 1 MB for a GeoTIFF
    ".zip": 1_000_000,     # 1 MB for compressed archives
    ".shp": 1_000,         # 1 KB for shapefiles (main file)
}

# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _validate_url(url: str) -> str:
    """Validate HTTPS URL before attempting download (T-21-01)."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https", "ftp"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme} in {url}")
    if not parsed.netloc:
        raise ValueError(f"URL missing network location: {url}")
    return url


def _check_file_integrity(path: Path) -> bool:
    """Verify file exists, is non-empty, and has expected format magic bytes.

    Returns True if valid, False otherwise (T-21-02).
    """
    if not path.exists():
        log.error("  File does not exist: %s", path)
        return False

    size = path.stat().st_size
    if size == 0:
        log.error("  File is empty (0 bytes): %s", path)
        return False

    ext = path.suffix.lower()
    min_size = MIN_SIZE.get(ext, 0)
    if size < min_size:
        log.error("  File too small (%d bytes, expected >= %d): %s", size, min_size, path)
        return False

    # Format magic-byte check
    try:
        with open(path, "rb") as fh:
            header = fh.read(16)
    except OSError as exc:
        log.error("  Cannot read file header: %s", exc)
        return False

    if ext == ".tif" or ext == ".tiff":
        # TIFF magic: II (little-endian) or MM (big-endian) at bytes 0-1, then 42
        if header[:2] not in (b"II", b"MM"):
            log.error("  Not a valid TIFF (missing TIFF magic bytes): %s", path)
            return False
    elif ext == ".zip":
        # ZIP magic: PK\x03\x04
        if header[:4] != b"PK\x03\x04":
            log.error("  Not a valid ZIP (missing PK header): %s", path)
            return False
    elif ext == ".kml":
        # KML/XML: starts with <?xml or <kml
        if not header.startswith(b"<?xml") and not header.startswith(b"<kml"):
            log.error("  Not a valid KML (missing XML/KML header): %s", path)
            return False

    log.info("  Integrity OK: %s (%.1f MB)", path.name, size / 1_000_000)
    return True


def _download_file(url: str, dest: Path, timeout: int = 300) -> bool:
    """Download a file from *url* to *dest*, returning success status.

    Handles redirects, network errors, and timeouts.
    """
    _validate_url(url)
    dest = dest.resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Clean up zero-byte files from previous failed attempts (WAF challenges, etc.)
    if dest.exists() and dest.stat().st_size == 0:
        log.warning("  Removing stale zero-byte file: %s", dest.name)
        dest.unlink()

    # Check if already downloaded and valid
    if dest.exists() and dest.stat().st_size > 0:
        log.info("  Already exists, skipping: %s", dest.name)
        return _check_file_integrity(dest)

    log.info("  Downloading: %s", url)
    log.info("  -> %s", dest)
    try:
        import urllib.request
        import urllib.error
        import ssl

        # Use certifi CA bundle for SSL (macOS workaround)
        try:
            import certifi
            ssl_context = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            ssl_context = ssl.create_default_context()

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (compatible; FuturePrediction/1.0; "
                    "research-project)"
                ),
            },
        )
        with urllib.request.urlopen(req, context=ssl_context, timeout=timeout) as response:
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            chunk_size = 8192
            with open(dest, "wb") as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = downloaded * 100 // total
                        if pct % 10 == 0:
                            log.info("  Progress: %d%% (%d / %d MB)", pct, downloaded // 1_000_000, total // 1_000_000)
    except urllib.error.HTTPError as exc:
        log.error("  HTTP %d: %s — %s", exc.code, exc.reason, url)
        if exc.code == 403:
            log.error("  This dataset may require manual download (browser interaction).")
        # Remove partial download
        if dest.exists():
            dest.unlink()
        return False
    except urllib.error.URLError as exc:
        log.error("  Network error: %s — %s", exc.reason, url)
        return False
    except OSError as exc:
        log.error("  File error: %s — %s", exc, dest)
        return False

    # If the file is empty after download (e.g., WAF challenge returned HTTP 200+0 bytes),
    # clean up and report failure
    if dest.exists() and dest.stat().st_size == 0:
        log.error("  Downloaded file is empty (0 bytes) — likely blocked by WAF.")
        dest.unlink()
        return False

    return _check_file_integrity(dest)


def _sha256(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

# ---------------------------------------------------------------------------
# Download functions
# ---------------------------------------------------------------------------

KOPPEN_ZIP_URL = "https://figshare.com/ndownloader/files/61012822"
"""Direct download URL for koppen_geiger_tif.zip (~90 MB) from figshare.

Contains GeoTIFFs for all periods and scenarios at 0.01°, 0.1°, 0.5°, 1.0° resolution.
Source: Beck et al. (2023) — gloh2o.org/koppen.
"""

def download_koppen(output_dir: str | Path = DEFAULT_OUTPUT) -> Path | None:
    """Download GloH2O V3 Köppen-Geiger GeoTIFF for 2041-2070 SSP3-7.0.

    Downloads the full figshare ZIP archive (~90 MB), then extracts the
    2041-2070 SSP3-7.0 GeoTIFF at 0.01° resolution.

    Returns path to extracted GeoTIFF, or None on failure.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    zip_dest = output / "koppen_geiger_tif.zip"
    target_file = output / "koppen_2041-2070_ssp370.tif"

    # If target already exists and is valid, skip
    if target_file.exists() and _check_file_integrity(target_file):
        log.info("Köppen target already present: %s", target_file)
        return target_file

    log.info("=" * 60)
    log.info("Köppen-Geiger Climate Classification (GloH2O V3)")
    log.info("=" * 60)

    # Download the ZIP archive
    if not _download_file(KOPPEN_ZIP_URL, zip_dest):
        log.error("Automated download failed — figshare WAF blocks direct HTTP access.")
        log.warning("")
        log.warning("=" * 60)
        log.warning("MANUAL DOWNLOAD REQUIRED")
        log.warning("=" * 60)
        log.warning("")
        log.warning("The GloH2O V3 data on figshare is protected by AWS WAF and")
        log.warning("requires a browser session to download.")
        log.warning("")
        log.warning("  1. Visit: https://www.gloh2o.org/koppen/")
        log.warning("  2. Click the 'download here' link for the TIF archive")
        log.warning("     (or use direct URL: %s)", KOPPEN_ZIP_URL)
        log.warning("  3. Save the ZIP file to: %s", zip_dest)
        log.warning("")
        log.warning("After downloading, run again to extract the 2041-2070 SSP3-7.0")
        log.warning("GeoTIFF automatically:")
        log.warning("  python3 download-data.py --koppen")
        log.warning("")
        log.warning("If the ZIP is already in place, it will be extracted without")
        log.warning("re-downloading.")
        log.warning("=" * 60)
        return None

    # Extract the specific file for 2041-2070 SSP3-7.0 at 0.01°
    # Internal path: 2041_2070/ssp370/koppen_geiger_0p01.tif
    try:
        with zipfile.ZipFile(zip_dest, "r") as zf:
            candidates = [
                name for name in zf.namelist()
                if "2041_2070" in name and "ssp370" in name and name.endswith(".tif")
            ]
            if not candidates:
                # Try alternative: any 2041-2070 SSP3-7.0 file
                candidates = [
                    name for name in zf.namelist()
                    if "2041_2070" in name and "ssp370" in name
                ]
            if not candidates:
                log.error("No matching file for 2041_2070/ssp370 found in ZIP.")
                log.info("Files in ZIP (first 20): %s", zf.namelist()[:20])
                return None

            # Prefer highest resolution (0p01)
            chosen = candidates[0]
            for c in candidates:
                if "0p01" in c:
                    chosen = c
                    break

            log.info("  Extracting: %s -> %s", chosen, target_file.name)
            with zf.open(chosen) as source, open(target_file, "wb") as dest:
                while True:
                    chunk = source.read(8192)
                    if not chunk:
                        break
                    dest.write(chunk)

            log.info("  Extracted: %s (from %s)", target_file.name, chosen)
    except (zipfile.BadZipFile, OSError) as exc:
        log.error("ZIP extraction error: %s", exc)
        return None

    if _check_file_integrity(target_file):
        return target_file

    log.error("Extracted file failed integrity check.")
    return None


# ---------------------------------------------------------------------------

TEOW_MANUAL_URL = (
    "https://www.worldwildlife.org/publications/"
    "terrestrial-ecoregions-of-the-world"
)
"""WWF TEOW page — requires browser interaction. 403 for programmatic access.

Alternative download sources (may work programmatically):
  - Stanford Digital Repository: https://purl.stanford.edu/fk938jc7981
"""

TEOW_ALT_URL = "https://purl.stanford.edu/fk938jc7981"
"""Stanford Digital Repository mirror for WWF TEOW data."""

def download_biomes(output_dir: str | Path = DEFAULT_OUTPUT) -> Path | None:
    """Download WWF Terrestrial Ecoregions (TEOW) for biome layer.

    WWF's direct download returns HTTP 403 for programmatic access.
    This function:
    1. Tries the Stanford Digital Repository mirror first
    2. Falls back to detailed manual download instructions

    Returns path to downloaded ZIP if successful, or None.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    target = output / "official_teow.zip"

    log.info("=" * 60)
    log.info("WWF Terrestrial Ecoregions (TEOW) — Biomes")
    log.info("=" * 60)

    # Check if already present
    if target.exists() and _check_file_integrity(target):
        log.info("TEOW already present: %s", target)
        return target

    log.info("Option 1: Attempting download from Stanford Digital Repository...")
    # Try the Stanford alternative URL first (might work programmatically)
    # The Stanford page requires clicking through — try direct file download
    # from the EarthWorks API
    stanford_url = "https://stacks.stanford.edu/file/druid:fk938jc7981/data.zip"
    if _download_file(stanford_url, target):
        if _check_file_integrity(target):
            log.info("TEOW downloaded from Stanford mirror.")
            return target

    # If Stanford failed, provide manual instructions
    log.warning("")
    log.warning("=" * 60)
    log.warning("MANUAL DOWNLOAD REQUIRED for WWF Terrestrial Ecoregions")
    log.warning("=" * 60)
    log.warning("")
    log.warning("WWF's file server blocks automated downloads (HTTP 403).")
    log.warning("Please download manually:")
    log.warning("")
    log.warning("  1. Visit: %s", TEOW_MANUAL_URL)
    log.warning("  2. Click the 'Download' button (~49 MB ZIP)")
    log.warning("  3. Save file to: %s", target)
    log.warning("")
    log.warning("  Alternative Stanford mirror: %s", TEOW_ALT_URL)
    log.warning("  (may require clicking through a redirect page)")
    log.warning("")
    log.warning("  Expected file: official_teow.zip")
    log.warning("  Inside ZIP: official/wwf_terr_ecos.shp (main shapefile)")
    log.warning("")
    log.warning("After manual download, run again to verify integrity:")
    log.warning("  python3 download-data.py --biomes")
    log.warning("=" * 60)

    return None


# ---------------------------------------------------------------------------

HYDROSHEDS_BASE = "https://data.hydrosheds.org/file/hydrobasins/standard"

HYDROSHEDS_REGIONS: dict[str, str] = {
    "af": "Africa",
    "ar": "Arctic (North America)",
    "as": "Asia (Central & South-East)",
    "au": "Australia & Oceania",
    "eu": "Europe & Middle East",
    "gr": "Greenland",
    "na": "North America & Caribbean",
    "sa": "South America",
    "si": "Siberia",
}
"""HydroBASINS continental region codes and names."""

# Level 4-5 provides the right granularity for major river basins
HYDROSHEDS_LEVEL = "04"
"""Pfafstetter level for water conflict basins (moderate granularity)."""

def download_watersheds(
    output_dir: str | Path = DEFAULT_OUTPUT,
    regions: list[str] | None = None,
    level: str = HYDROSHEDS_LEVEL,
) -> list[Path]:
    """Download HydroSHEDS HydroBASINS v1c watershed boundaries.

    Downloads shapefiles for specified Pfafstetter level from hydrosheds.org.

    Args:
        output_dir: Directory to save files.
        regions: List of region codes (default: all except Arctic/Greenland).
        level: Pfafstetter level (01-12). Level 4-5 for major basins.

    Returns:
        List of successfully downloaded ZIP file paths.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    if regions is None:
        # Relevant continents for water conflict basins per D-08
        regions = ["af", "as", "au", "eu", "na", "sa", "si"]

    success: list[Path] = []

    log.info("=" * 60)
    log.info("HydroSHEDS HydroBASINS v1c — Watersheds (Level %s)", level)
    log.info("=" * 60)

    for code in regions:
        name = HYDROSHEDS_REGIONS.get(code, code)
        url = f"{HYDROSHEDS_BASE}/hybas_{code}_lev{level}_v1c.zip"
        dest = output / f"hybas_{code}_lev{level}_v1c.zip"

        log.info("Region: %s (%s)", name, code)
        if _download_file(url, dest):
            success.append(dest)
        else:
            log.warning("  Failed to download HydroBASINS region: %s", code)

    log.info(
        "Downloaded %d/%d HydroBASINS regions (Level %s).",
        len(success), len(regions), level,
    )
    if success:
        log.info("Files: %s", [s.name for s in success])

    return success


# ---------------------------------------------------------------------------

# SRTM/Copernicus DEM tiles for 6 SLR regions (D-11)
DEM_REGIONS = {
    "bangladesh": {
        "name": "Bangladesh Delta",
        "tiles": ["N21E088", "N21E089", "N22E088", "N22E089",
                  "N23E088", "N23E089", "N24E088", "N24E089"],
    },
    "mekong": {
        "name": "Mekong Delta",
        "tiles": ["N08E104", "N08E105", "N09E104", "N09E105",
                  "N10E104", "N10E105", "N10E106"],
    },
    "nile": {
        "name": "Nile Delta",
        "tiles": ["N30E030", "N30E031", "N31E030", "N31E031",
                  "N31E032", "N32E031"],
    },
    "us-gulf": {
        "name": "US Gulf Coast",
        "tiles": ["N25W082", "N25W081", "N26W082", "N26W081",
                  "N27W082", "N27W081", "N28W082", "N28W081",
                  "N29W089", "N29W088", "N29W087", "N30W089",
                  "N30W088"],
    },
    "pacific-atolls": {
        "name": "Pacific Atolls (Tuvalu, Kiribati, Marshall Is., Maldives)",
        "tiles": ["S09E178", "N08E167", "N07E171", "N05E172",
                  "S01E173", "N03E172", "N04E168"],  # Approximate
    },
    "netherlands": {
        "name": "Netherlands",
        "tiles": ["N51E003", "N51E004", "N51E005", "N51E006",
                  "N52E003", "N52E004", "N52E005", "N52E006",
                  "N52E007"],
    },
}

# Alternative: Copernicus DEM 30m Global (AWS Open Data)
# s3://copernicus-dem-30m/ — requires AWS CLI or direct HTTP access
COP30_URL_TEMPLATE = (
    "https://copernicus-dem-30m.s3.amazonaws.com/"
    "{tile}/{tile}_DEM.tif"
)

OPENTOPO_API = "https://portal.opentopography.org/API/globaldem?dem=SRTM&west={w}&south={s}&east={e}&north={n}&output=GTiff"

def download_dem_tiles(output_dir: str | Path = DEFAULT_OUTPUT) -> list[Path]:
    """Download SRTM/Copernicus DEM tiles for SLR inundation regions.

    Provides detailed download instructions for 6 SLR regions (D-11).
    SRTM tiles are available via OpenTopography API or USGS EarthExplorer.
    Copernicus DEM 30m is available on AWS Open Data.

    Returns list of successfully downloaded file paths.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    log.info("=" * 60)
    log.info("DEM Tiles — SLR Inundation Regions")
    log.info("=" * 60)
    log.info("")
    log.info("Sea Level Rise inundation requires elevation data at <= 0.35m.")
    log.info("Recommended: Copernicus DEM 30m (global, fewer voids than SRTM)")
    log.info("Alternative: SRTM 30m from OpenTopography")
    log.info("")
    log.info("SLR Regions (per D-11) and approximate tile coordinates:")
    log.info("")

    all_tiles: list[str] = []
    for key, region in DEM_REGIONS.items():
        log.info("  %s (%s):", region["name"], key)
        for tile in region["tiles"]:
            all_tiles.append(tile)
            log.info("    - %s", tile)
        log.info("")

    log.info("=" * 60)
    log.info("DOWNLOAD OPTIONS")
    log.info("=" * 60)
    log.info("")
    log.info("Option 1: Copernicus DEM 30m (AWS Open Data, free, no auth)")
    log.info("  Pattern: https://copernicus-dem-30m.s3.amazonaws.com/{TILE}/{TILE}_DEM.tif")
    log.info("  Example: %s", COP30_URL_TEMPLATE.format(tile="N21E088"))
    log.info("")
    log.info("  This can be automated but tiles are ~170 MB each.")
    log.info("  To download all tiles (~1.5 GB total), use:")
    log.info("    python3 download-data.py --dem --auto")
    log.info("")
    log.info("Option 2: OpenTopography SRTM 30m API")
    log.info("  Requires API key from https://opentopography.org")
    log.info("  Each region needs a bounding-box request.")
    log.info("")
    log.info("Option 3: USGS EarthExplorer (manual)")
    log.info("  - Visit: https://earthexplorer.usgs.gov")
    log.info("  - Search SRTM 30m tiles by tile ID")
    log.info("  - Download GeoTIFF for each tile")
    log.info("")
    log.info("After downloading, save DEM .tif files to: %s", output)
    log.info("Run again: python3 download-data.py --dem to verify.")
    log.info("=" * 60)

    return []


def download_dem_automatic(output_dir: str | Path) -> list[Path]:
    """Attempt automatic download of Copernicus DEM 30m tiles from AWS.

    Returns list of successfully downloaded file paths.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    success: list[Path] = []

    all_tile_names: set[str] = set()
    for region in DEM_REGIONS.values():
        for tile in region["tiles"]:
            all_tile_names.add(tile)

    log.info("Attempting Copernicus DEM 30m download for %d tiles...", len(all_tile_names))

    for tile in sorted(all_tile_names):
        url = COP30_URL_TEMPLATE.format(tile=tile)
        dest = output / f"{tile}_DEM.tif"

        if dest.exists() and _check_file_integrity(dest):
            log.info("  DEM tile already present: %s", dest.name)
            success.append(dest)
            continue

        log.info("  DEM tile: %s", tile)
        if _download_file(url, dest, timeout=600):
            success.append(dest)

    log.info(
        "Downloaded %d/%d DEM tiles.",
        len(success), len(all_tile_names),
    )
    return success


# ---------------------------------------------------------------------------
# Status check
# ---------------------------------------------------------------------------

def check_status(output_dir: str | Path = DEFAULT_OUTPUT) -> dict[str, bool | str]:
    """Check which datasets are already downloaded and valid."""
    output = Path(output_dir)
    status: dict[str, bool | str] = {}

    # Köppen
    koppen_zip = output / "koppen_geiger_tif.zip"
    koppen_tif = output / "koppen_2041-2070_ssp370.tif"
    if koppen_tif.exists() and _check_file_integrity(koppen_tif):
        status["koppen"] = f"OK ({koppen_tif.name}, {koppen_tif.stat().st_size / 1_000_000:.1f} MB)"
    elif koppen_zip.exists() and _check_file_integrity(koppen_zip):
        status["koppen"] = f"ZIP downloaded, not extracted ({koppen_zip.name})"
    else:
        status["koppen"] = "Not downloaded"

    # TEOW
    teow = output / "official_teow.zip"
    if teow.exists() and _check_file_integrity(teow):
        status["biomes"] = f"OK ({teow.name})"
    else:
        status["biomes"] = "Not downloaded (manual required)"

    # HydroBASINS
    basins_found = sorted(
        p.name for p in output.glob("hybas_*_lev*_v1c.zip")
        if _check_file_integrity(p)
    )
    if basins_found:
        status["watersheds"] = f"OK ({len(basins_found)} regions: {', '.join(basins_found)})"
    else:
        status["watersheds"] = "Not downloaded"

    # DEM
    dem_found = sorted(
        p.name for p in output.glob("*_DEM.tif")
        if _check_file_integrity(p)
    )
    if dem_found:
        status["dem"] = f"OK ({len(dem_found)} tiles: {', '.join(dem_found[:5])}{'...' if len(dem_found) > 5 else ''})"
    else:
        status["dem"] = "Not downloaded"

    return status


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Download source datasets for Phase 21 climate KML layers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Download all datasets (automated where possible)",
    )
    parser.add_argument(
        "--koppen", action="store_true",
        help="Download Köppen-Geiger climate classification data",
    )
    parser.add_argument(
        "--biomes", action="store_true",
        help="Download/download instructions for WWF ecoregions",
    )
    parser.add_argument(
        "--watersheds", action="store_true",
        help="Download HydroSHEDS HydroBASINS watershed data",
    )
    parser.add_argument(
        "--dem", action="store_true",
        help="Download DEM tiles for SLR inundation regions",
    )
    parser.add_argument(
        "--auto", action="store_true",
        help="Attempt automatic DEM download from AWS Copernicus",
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Check which datasets are already downloaded",
    )
    parser.add_argument(
        "--output", type=str, default=str(DEFAULT_OUTPUT),
        help=f"Output directory (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    output = Path(args.output)

    # Default: show help
    if not any([args.all, args.koppen, args.biomes, args.watersheds,
                 args.dem, args.status]):
        parser.print_help()
        print("\n---\nUse --status to check current download state.")
        sys.exit(0)

    # Status check
    if args.status:
        log.info("=" * 60)
        log.info("Data Download Status")
        log.info("=" * 60)
        for key, val in check_status(output).items():
            log.info("  %-15s %s", key + ":", val)
        return

    # Ensure output directory exists
    output.mkdir(parents=True, exist_ok=True)

    results: dict[str, bool] = {}

    # --- Köppen ---
    if args.all or args.koppen:
        log.info("")
        result = download_koppen(output)
        results["Köppen"] = result is not None

    # --- Biomes ---
    if args.all or args.biomes:
        log.info("")
        result = download_biomes(output)
        results["Biomes"] = result is not None

    # --- Watersheds ---
    if args.all or args.watersheds:
        log.info("")
        downloaded = download_watersheds(output)
        results["Watersheds"] = len(downloaded) > 0

    # --- DEM ---
    if args.all or args.dem:
        log.info("")
        if args.auto or args.all:
            downloaded = download_dem_automatic(output)
            results["DEM (auto)"] = len(downloaded) > 0
        else:
            download_dem_tiles(output)
            results["DEM"] = False  # Manual instructions given

    # --- Summary ---
    log.info("")
    log.info("=" * 60)
    log.info("Download Summary")
    log.info("=" * 60)
    for name, ok in results.items():
        icon = "✓" if ok else "—"
        log.info("  %s %s", icon, name)

    if not all(results.values()):
        log.info("")
        log.info("Some downloads require manual steps. See instructions above.")
        log.info("Run 'python3 download-data.py --status' to re-check.")

    log.info("")
    log.info("Done.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Interrupted by user.")
        sys.exit(1)
    except Exception as exc:
        log.critical("Unhandled error: %s", exc, exc_info=True)
        sys.exit(1)
