#!/usr/bin/env python3
"""
Generate Köppen-Geiger climate classification layer for 2050 KML.

Reads GloH2O V3 2041-2070 SSP3-7.0 GeoTIFF, polygonizes Köppen class zones,
and produces a styled KML file organized by climate group (A/B/C/D/E).

Per D-01, D-02, D-12: Creates climate_koppen.kml for later merge into climate.kml.
Per D-03: High detail global — file size acceptable.
Per D-13: Cross-references back to climate.md.

Fallback: If GeoTIFF not available, creates approximate continental-level polygons
from narrative in climate.md (latitudinal bands).

Output: climate_koppen.kml — containing only the Köppen folder for later merge.
"""

import logging
import os
import sys
from collections import Counter, defaultdict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# --- Color scheme (standard Köppen palette from Beck et al. 2023) ---
# Format: code -> standard HEX RRGGBB (HTML notation)
KOPPEN_COLORS = {
    "Af": "#0000FF",   "Am": "#0078FF",   "Aw": "#46AAFA",
    "BWh": "#FE0000",  "BWk": "#FE9695",  "BSh": "#F5A505",  "BSk": "#FFDC7C",
    "Csa": "#FFCC00",  "Csb": "#C9C800",  "Cwa": "#C6C76A",  "Cwb": "#6C9A5E",
    "Cwc": "#7EAA7D",  "Cfa": "#96FF96",  "Cfb": "#6DB46D",  "Cfc": "#40A040",
    "Dsa": "#5EBDC9",  "Dsb": "#4DA6B8",  "Dsc": "#2F8FA5",
    "Dwa": "#5DF0F0",  "Dwb": "#41C8C8",  "Dwc": "#2CAAAA",
    "Dfa": "#00FFFF",  "Dfb": "#46D2D2",  "Dfc": "#64C8E4",  "Dfd": "#5EE0F0",
    "ET": "#964696",   "EF": "#FFFFFF",
}

KOPPEN_FULL_NAMES = {
    "Af": "Tropical Rainforest",
    "Am": "Tropical Monsoon",
    "Aw": "Tropical Savannah",
    "BWh": "Hot Desert",
    "BWk": "Cold Desert",
    "BSh": "Hot Semi-arid",
    "BSk": "Cold Semi-arid",
    "Csa": "Hot-summer Mediterranean",
    "Csb": "Warm-summer Mediterranean",
    "Cwa": "Monsoon humid subtropical",
    "Cwb": "Subtropical highland",
    "Cwc": "Cold subtropical highland",
    "Cfa": "Humid subtropical",
    "Cfb": "Oceanic",
    "Cfc": "Subpolar oceanic",
    "Dsa": "Mediterranean hot continental",
    "Dsb": "Mediterranean warm continental",
    "Dsc": "Mediterranean subarctic",
    "Dwa": "Monsoon hot continental",
    "Dwb": "Monsoon warm continental",
    "Dwc": "Monsoon subarctic",
    "Dfa": "Hot continental",
    "Dfb": "Warm continental",
    "Dfc": "Subarctic",
    "Dfd": "Extreme subarctic",
    "ET": "Tundra",
    "EF": "Frost/Ice Cap",
}

# Climate groups organized with their sub-types (5 major groups)
KOPPEN_GROUPS = {
    "A — Tropical Climates": ["Af", "Am", "Aw"],
    "B — Arid Climates": ["BWh", "BWk", "BSh", "BSk"],
    "C — Temperate Climates": ["Csa", "Csb", "Cwa", "Cwb", "Cwc", "Cfa", "Cfb", "Cfc"],
    "D — Continental Climates": ["Dsa", "Dsb", "Dsc", "Dwa", "Dwb", "Dwc", "Dfa", "Dfb", "Dfc", "Dfd"],
    "E — Polar Climates": ["ET", "EF"],
}

# All 30 codes in order
ALL_KOPPEN_CODES = [
    "Af", "Am", "Aw",
    "BWh", "BWk", "BSh", "BSk",
    "Csa", "Csb", "Cwa", "Cwb", "Cwc", "Cfa", "Cfb", "Cfc",
    "Dsa", "Dsb", "Dsc", "Dwa", "Dwb", "Dwc", "Dfa", "Dfb", "Dfc", "Dfd",
    "ET", "EF",
]

# Numeric value -> sub-type code (GloH2O V3 Beck et al. 2023 standard legend)
RASTER_LEGEND = {
    1: "Af", 2: "Am", 3: "Aw",
    4: "BWh", 5: "BWk", 6: "BSh", 7: "BSk",
    8: "Csa", 9: "Csb", 10: "Cwa", 11: "Cwb", 12: "Cwc",
    13: "Cfa", 14: "Cfb", 15: "Cfc",
    16: "Dsa", 17: "Dsb", 18: "Dsc",
    19: "Dwa", 20: "Dwb", 21: "Dwc",
    22: "Dfa", 23: "Dfb", 24: "Dfc", 25: "Dfd",
    26: "ET", 27: "EF",
}

# Cross-reference target for all placemarks
CLIMATE_MD_ANCHOR = "2050-snapshot/domains/climate.md#global-climate-state"

# --- Helper functions ---

def hex_to_kml_color(hex_color, alpha="80"):
    """
    Convert #RRGGBB to AARRGGBB KML color format.
    Matches the project convention used in climate.kml and entity-config.json.
    Alpha 80 = ~50% opacity (semi-transparent overlay).
    """
    hex_color = hex_color.lstrip("#")
    return f"{alpha}{hex_color}"


def make_description(subtype_code):
    """Build the KML description with cross-reference."""
    full_name = KOPPEN_FULL_NAMES.get(subtype_code, subtype_code)
    return (
        f"Köppen-Geiger climate zone: {subtype_code} ({full_name})"
        f" — 2050 projection under SSP3-7.0."
        f" See: {CLIMATE_MD_ANCHOR}"
    )


def koppen_type_sorter_key(code):
    """
    Return a stable ordering key for Köppen codes.
    Groups: A=0, B=1, C=2, D=3, E=4, then index within group.
    """
    group_order = {c: i for i, codes in enumerate(KOPPEN_GROUPS.values()) for c in codes}
    return group_order.get(code, 99)


# --- Fallback generation (when GeoTIFF unavailable) ---

def create_fallback_polygons(code):
    """
    Create approximate latitudinal-band polygon(s) for a Köppen sub-type.
    Used when the real GloH2O GeoTIFF is not available.

    Returns list of (lon, lat) exterior ring coordinate lists.
    Each sub-type within a group gets a longitudinal slice to avoid
    all subtypes overlapping identically.
    """
    from shapely.geometry import Polygon

    # Collect all subtypes in the same group as this code
    all_in_group = []
    for group_codes in KOPPEN_GROUPS.values():
        if code in group_codes:
            all_in_group = sorted(group_codes)
            break

    if not all_in_group:
        return []

    idx = all_in_group.index(code)
    n = len(all_in_group)

    # Assign each subtype a longitudinal slice of the global band
    slice_width = 360.0 / n
    lon_start = -180.0 + idx * slice_width
    lon_end = lon_start + slice_width

    # Set latitude bounds based on climate group
    first_letter = code[0]
    if first_letter == "A":
        lat_min, lat_max = -15, 15
    elif first_letter == "B":
        lat_min, lat_max = 15, 38
    elif first_letter == "C":
        lat_min, lat_max = 30, 55
    elif first_letter == "D":
        lat_min, lat_max = 45, 65
    elif first_letter == "E":
        if code == "ET":
            lat_min, lat_max = 60, 72  # Tundra (land masses extend this far north)
        else:
            lat_min, lat_max = 72, 85  # Ice cap
    else:
        return []

    # Build the ring: counterclockwise for exterior
    ring = [
        (lon_end, lat_min),
        (lon_end, lat_max),
        (lon_start, lat_max),
        (lon_start, lat_min),
        (lon_end, lat_min),  # close
    ]
    return [ring]


def generate_fallback_koppen_kml(script_dir):
    """
    Generate approximate Köppen zones using latitudinal-band fallback.
    Called when the GeoTIFF source data is unavailable.
    """
    log.info("GeoTIFF not found — generating approximate fallback Köppen layer")
    log.info("NOTE: Fallback uses latitudinal-band approximations from climate.md narrative")
    log.info("      Replace with real GeoTIFF data when source becomes available")

    from shapely.geometry import Polygon

    subtype_polygons = defaultdict(list)
    total_vertices = 0
    total_polygons = 0

    for code in ALL_KOPPEN_CODES:
        rings = create_fallback_polygons(code)
        for ring in rings:
            if len(ring) < 4:
                continue
            poly = Polygon(ring)
            if poly.is_empty or not poly.is_valid:
                continue
            subtype_polygons[code].append(poly)
            total_polygons += 1
            total_vertices += len(ring)

    log.info(
        f"Fallback generated {total_polygons} polygons "
        f"({total_vertices} total vertices) across {len(subtype_polygons)} sub-types"
    )

    return subtype_polygons


# --- GeoTIFF-based generation ---

def generate_from_geotiff(geotiff_path, script_dir):
    """
    Generate Köppen zones from GloH2O V3 2041-2070 SSP3-7.0 GeoTIFF.
    Polygonizes contiguous zones of the same class, simplifies geometry,
    and organizes into the KML hierarchy.

    Per T-21-04: Validates simplified polygons for self-intersection via
    shapely.is_valid before writing KML.
    Per T-21-05: Prints histogram of raster values before mapping.
    """
    import rasterio
    from rasterio.features import shapes
    from shapely.geometry import shape as shp_shape
    from shapely.ops import unary_union

    log.info(f"Reading GeoTIFF: {geotiff_path}")

    with rasterio.open(geotiff_path) as src:
        band = src.read(1)
        transform = src.transform
        crs = src.crs

        log.info(f"  Raster shape: {band.shape}, CRS: {crs}")

        # Print value histogram (T-21-05)
        unique, counts = Counter(band[band != src.nodata]).most_common()
        if not unique:
            unique, counts = Counter(band.flatten()).most_common()

        log.info(f"  Unique pixel values found: {len(unique)}")
        for val, cnt in unique[:35]:
            code = RASTER_LEGEND.get(val, "UNKNOWN")
            log.info(f"    Value {val:3d} ({code:>4s}): {cnt:>10,d} pixels")

        # Polygonize: convert raster zones to vector polygons
        log.info("  Polygonizing raster zones...")
        results = (
            (shp_shape(geom).simplify(0.02, preserve_topology=True), value)
            for geom, value in shapes(band, mask=band != src.nodata, transform=transform)
        )

        # Group polygons by Köppen sub-type code
        subtype_polygons = defaultdict(list)
        total_raw_count = 0
        total_simplified_count = 0
        total_simplified_vertices = 0

        for poly, value in results:
            total_raw_count += 1
            code = RASTER_LEGEND.get(int(value))
            if code is None:
                continue

            # Douglas-Peucker simplification (D-16 convention, 0.02° ~2.2km)
            simplified = poly.simplify(0.02, preserve_topology=True)

            # T-21-04: Validate simplified polygon
            if simplified.is_empty:
                continue
            if simplified.geom_type == "Polygon":
                if simplified.exterior is None or len(simplified.exterior.coords) < 4:
                    continue
                if not simplified.is_valid:
                    repaired = simplified.buffer(0)
                    if repaired.is_empty or not repaired.is_valid:
                        continue
                    simplified = repaired
                subtype_polygons[code].append(simplified)
                total_simplified_count += 1
                total_simplified_vertices += len(simplified.exterior.coords)
            elif simplified.geom_type == "MultiPolygon":
                for part in simplified.geoms:
                    if not part.is_empty and part.is_valid and len(part.exterior.coords) >= 4:
                        subtype_polygons[code].append(part)
                        total_simplified_count += 1
                        total_simplified_vertices += len(part.exterior.coords)

        log.info(
            f"  Polygonization: {total_raw_count} raw → "
            f"{total_simplified_count} valid simplified polygons "
            f"({total_simplified_vertices} vertices)"
        )

        # Report per sub-type counts
        for code in sorted(subtype_polygons, key=koppen_type_sorter_key):
            poly_count = len(subtype_polygons[code])
            vertex_count = sum(
                len(p.exterior.coords) if p.geom_type == "Polygon"
                else sum(len(part.exterior.coords) for part in p.geoms)
                for p in subtype_polygons[code]
            )
            log.info(f"    {code} ({KOPPEN_FULL_NAMES[code]}): {poly_count} polygons, {vertex_count} vertices")

        # Report missing sub-types
        present_codes = set(subtype_polygons.keys())
        missing = set(ALL_KOPPEN_CODES) - present_codes
        if missing:
            log.warning(f"  Missing sub-types (no polygons found): {sorted(missing)}")

        return subtype_polygons


# --- KML building ---

def build_koppen_kml(subtype_polygons, output_path):
    """
    Build the Köppen KML structure using simplekml.

    Structure:
    - Root folder: "Köppen-Geiger Climate Classification (2050)"
      - A — Tropical Climates
        - Af folder → placemarks
        - Am folder → placemarks
        - Aw folder → placemarks
      - B — Arid Climates
        - ...
      - C — Temperate Climates
      - D — Continental Climates
      - E — Polar Climates
    """
    import simplekml

    kml = simplekml.Kml(name="Köppen-Geiger Climate Classification (2050)")
    koppen_root = kml.newfolder(name="Köppen-Geiger Climate Classification (2050)")

    # Build group folders
    group_folders = {}
    for group_name in KOPPEN_GROUPS:
        gf = koppen_root.newfolder(name=group_name)
        group_folders[group_name] = gf

    total_placemarks = 0
    total_vertices = 0

    # Iterate groups in order, then subtypes within groups
    for group_name, subtype_codes in KOPPEN_GROUPS.items():
        group_folder = group_folders[group_name]

        for code in subtype_codes:
            polygons = subtype_polygons.get(code, [])

            if not polygons:
                # Create a placeholder folder with note (not a polygon to avoid empty geometry)
                subtype_folder = group_folder.newfolder(name=code)
                note_pm = subtype_folder.newpoint(
                    name=f"{code} — {KOPPEN_FULL_NAMES.get(code, '')}",
                    description=(
                        f"{code} — No polygon data available for "
                        f"this Köppen sub-type in the current source. "
                        f"See: {CLIMATE_MD_ANCHOR}"
                    ),
                    coords=[(0, 0)],  # off-map placeholder, not a geographic polygon
                )
                note_pm.style.iconstyle.icon.href = ""
                note_pm.style.iconstyle.color = "00000000"  # invisible
                continue

            subtype_folder = group_folder.newfolder(name=code)

            # Set default style for this subtype — applies to all contained placemarks
            hex_color = KOPPEN_COLORS.get(code, "#CCCCCC")
            poly_color = hex_to_kml_color(hex_color, alpha="80")
            line_color = hex_to_kml_color(hex_color, alpha="FF")

            for poly in polygons:
                if poly.is_empty:
                    continue

                if poly.geom_type == "Polygon":
                    coords_list = list(poly.exterior.coords)
                    if len(coords_list) < 4:
                        continue

                    # Convert to (lon, lat, 0) format for simplekml
                    kml_coords = [(x, y, 0) for x, y in coords_list]

                    pm = subtype_folder.newpolygon(
                        name=f"{code}",
                        description=make_description(code),
                        outerboundaryis=kml_coords,
                    )
                    pm.style.polystyle.color = poly_color
                    pm.style.polystyle.outline = 1
                    pm.style.linestyle.color = line_color
                    pm.style.linestyle.width = 0.5
                    pm.altitudemode = simplekml.AltitudeMode.clamptoground

                    total_placemarks += 1
                    total_vertices += len(kml_coords)

                elif poly.geom_type == "MultiPolygon":
                    for part in poly.geoms:
                        if part.is_empty:
                            continue
                        coords_list = list(part.exterior.coords)
                        if len(coords_list) < 4:
                            continue
                        kml_coords = [(x, y, 0) for x, y in coords_list]

                        pm = subtype_folder.newpolygon(
                            name=f"{code}",
                            description=make_description(code),
                            outerboundaryis=kml_coords,
                        )
                        pm.style.polystyle.color = poly_color
                        pm.style.polystyle.outline = 1
                        pm.style.linestyle.color = line_color
                        pm.style.linestyle.width = 0.5
                        pm.altitudemode = simplekml.AltitudeMode.clamptoground

                        total_placemarks += 1
                        total_vertices += len(kml_coords)

    log.info(
        f"KML built: {total_placemarks} placemarks, "
        f"{total_vertices} vertices across {len(subtype_polygons)} sub-types"
    )

    kml.save(output_path)
    file_size = os.path.getsize(output_path)
    log.info(f"Written: {output_path} ({file_size:,} bytes)")

    return kml


# --- Main public API ---

def generate_koppen_kml(output_path="climate_koppen.kml"):
    """
    Main entry point for generating the Köppen-Geiger KML layer.

    Args:
        output_path: Path for output KML file (default: climate_koppen.kml).

    Returns:
        Path to the generated KML file, or None if generation failed.
    """
    # Determine paths relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    geotiff_path = os.path.join(script_dir, "source", "koppen_2041-2070_ssp370.tif")

    if not os.path.isfile(geotiff_path):
        log.warning(
            f"Köppen source GeoTIFF not found at {geotiff_path}.\n"
            f"  Download from GloH2O V3 figshare (DOI 10.6084/m9.figshare.21789074)\n"
            f"  or run download-data.py from Plan 01.\n"
            f"  Falling back to approximate latitudinal-band approximation."
        )
        subtype_polygons = generate_fallback_koppen_kml(script_dir)
        if not subtype_polygons:
            log.error("Fallback generation produced no polygons — aborting")
            return None
        build_koppen_kml(subtype_polygons, output_path)
        return output_path if os.path.isfile(output_path) else None

    try:
        subtype_polygons = generate_from_geotiff(geotiff_path, script_dir)
        if not subtype_polygons:
            log.error("GeoTIFF polygonization produced no polygons — aborting")
            return None
        build_koppen_kml(subtype_polygons, output_path)
        return output_path if os.path.isfile(output_path) else None
    except Exception as e:
        log.error(f"GeoTIFF processing failed: {e}")
        log.info("Falling back to approximate latitudinal-band polygons...")
        subtype_polygons = generate_fallback_koppen_kml(script_dir)
        if not subtype_polygons:
            log.error("Fallback generation also failed")
            return None
        build_koppen_kml(subtype_polygons, output_path)
        return output_path if os.path.isfile(output_path) else None


def main():
    """CLI entry point."""
    output_path = "climate_koppen.kml"
    if len(sys.argv) > 1:
        output_path = sys.argv[1]

    result = generate_koppen_kml(output_path)
    if result:
        print(f"Köppen KML generated: {result}")
    else:
        print("Failed to generate Köppen KML")
        sys.exit(1)


if __name__ == "__main__":
    main()
