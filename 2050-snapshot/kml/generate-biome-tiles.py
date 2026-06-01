#!/usr/bin/env python3
"""
Generate XYZ Web Mercator tiles for biome layers (combined, one tileset each).

  RESOLVE 2017 current biomes (14 classes):
    source: source/resolve_biomes_2017.tif
    output: tiles/biomes-current/{z}/{x}/{y}.png

  Projected 2050 biomes via RF ensemble:
    source: source/resolve_rf_projected_2050.tif
    output: tiles/biomes-2050/{z}/{x}/{y}.png

Zoom 0-6, nearest-neighbour, transparent ocean/nodata tiles skipped.

Lake pixels masked using Natural Earth 10m lakes, rasterized at the source
TIF's native resolution so lake boundaries match the data pixel size.
"""

import os
import subprocess
import tempfile
import shutil
import zipfile
import numpy as np
import rasterio
import rasterio.warp
import rasterio.features
from rasterio.crs import CRS
from rasterio.enums import Resampling
import fiona
from PIL import Image

TILES_DIR = "tiles"
MIN_ZOOM  = 0
MAX_ZOOM  = 6
TILE_SIZE = 256
ALPHA     = 200

RESOLVE_BIOMES = {
    1:  ("#38A700", "Tropical & Subtropical Moist Broadleaf Forests"),
    2:  ("#CCCD65", "Tropical & Subtropical Dry Broadleaf Forests"),
    3:  ("#88CE66", "Tropical & Subtropical Coniferous Forests"),
    4:  ("#00734C", "Temperate Broadleaf & Mixed Forests"),
    5:  ("#458970", "Temperate Conifer Forests"),
    6:  ("#7AB6F5", "Boreal Forests / Taiga"),
    7:  ("#FEAA01", "Tropical & Subtropical Grasslands, Savannas & Shrublands"),
    8:  ("#FEFF73", "Temperate Grasslands, Savannas & Shrublands"),
    9:  ("#BEE7FF", "Flooded Grasslands & Savannas"),
    10: ("#D6C39D", "Montane Grasslands & Shrublands"),
    11: ("#9ED7C2", "Tundra"),
    12: ("#FE0000", "Mediterranean Forests, Woodlands & Scrub"),
    13: ("#CC6767", "Deserts & Xeric Shrublands"),
    14: ("#FE01C4", "Mangroves"),
}

WHITTAKER_BIOMES = {
    1: ("#1A7F1A", "Tropical Rainforest"),
    2: ("#8DB84E", "Tropical Seasonal Forest & Savanna"),
    3: ("#E8C46A", "Subtropical Desert"),
    4: ("#2D6E4E", "Temperate Rainforest"),
    5: ("#4E9B5A", "Temperate Seasonal Forest"),
    6: ("#C8A44A", "Woodland & Shrubland"),
    7: ("#C8C87A", "Temperate Grassland & Desert Scrub"),
    8: ("#7AB6F5", "Boreal Forest (Taiga)"),
    9: ("#C8E8D8", "Tundra & Ice"),
}

WEB_MERCATOR = CRS.from_epsg(3857)

NE_LAKES_URL = "https://naciscdn.org/naturalearth/10m/physical/ne_10m_lakes.zip"
NE_LAKES_ZIP = "source/ne_10m_lakes.zip"


def get_lake_mask_4326(h, w):
    """Return boolean array (h, w) in EPSG:4326, True where pixel overlaps a lake."""
    cache_path = f"source/ne_lakes_mask_{h}x{w}.npy"
    if os.path.exists(cache_path):
        print(f"  Loading cached lake mask ({h}×{w})…")
        return np.load(cache_path)

    if not os.path.exists(NE_LAKES_ZIP):
        print(f"  Downloading Natural Earth 10m lakes…", flush=True)
        subprocess.run(["curl", "-L", NE_LAKES_URL, "-o", NE_LAKES_ZIP], check=True)

    print(f"  Rasterizing lake polygons at {h}×{w} EPSG:4326…")
    t = rasterio.transform.from_bounds(-180, -90, 180, 90, w, h)

    geoms = []
    with zipfile.ZipFile(NE_LAKES_ZIP) as zf:
        tmpdir = tempfile.mkdtemp()
        try:
            zf.extractall(tmpdir)
            shp_path = next(
                os.path.join(root, f)
                for root, _, files in os.walk(tmpdir)
                for f in files if f.endswith(".shp")
            )
            with fiona.open(shp_path) as lyr:
                for feat in lyr:
                    g = feat["geometry"]
                    if g is not None:
                        geoms.append(g)
        finally:
            shutil.rmtree(tmpdir)

    print(f"  {len(geoms)} lake polygons")
    mask = rasterio.features.rasterize(
        geoms, out_shape=(h, w),
        transform=t, fill=0, default_value=1, dtype="uint8"
    ).astype(bool)

    np.save(cache_path, mask)
    print(f"  Mask saved to {cache_path}")
    return mask


def build_lut(biome_dict, alpha):
    lut = np.zeros((256, 4), dtype=np.uint8)
    for pv, (color, _) in biome_dict.items():
        h = color.lstrip("#")
        lut[pv] = [int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), alpha]
    return lut


def generate_tiles(tiff_path, out_dir, label, biome_dict=None):
    if biome_dict is None:
        biome_dict = RESOLVE_BIOMES

    TARGET_W = TARGET_H = 16384
    ORIGIN = 20037508.342789244
    dst_transform = rasterio.transform.from_bounds(
        -ORIGIN, -ORIGIN, ORIGIN, ORIGIN, TARGET_W, TARGET_H
    )

    print(f"\n{label}")

    # ── Read source band at native resolution ────────────────────────────────
    with rasterio.open(tiff_path) as src:
        src_h, src_w = src.height, src.width
        print(f"  Reading source ({src_h}×{src_w})…")
        src_band = src.read(1).astype(np.uint8)
        src_crs = src.crs
        src_transform = src.transform

    # ── Lake mask at source resolution ───────────────────────────────────────
    lake_mask = get_lake_mask_4326(src_h, src_w)
    n_lake = int(((src_band > 0) & lake_mask).sum())
    src_band[lake_mask] = 0
    print(f"  Zeroed {n_lake:,} lake pixels")

    # ── Reproject to Web Mercator ────────────────────────────────────────────
    print(f"  Reprojecting to {TARGET_H}×{TARGET_W} Web Mercator…")
    band = np.zeros((TARGET_H, TARGET_W), dtype=np.uint8)
    rasterio.warp.reproject(
        source=src_band, destination=band,
        src_crs=src_crs, dst_crs=WEB_MERCATOR,
        src_transform=src_transform,
        dst_transform=dst_transform, resampling=Resampling.nearest,
    )

    lut = build_lut(biome_dict, ALPHA)
    rgba = lut[band]
    written = total = 0

    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        n = 2 ** z
        print(f"  Zoom {z} ({n}×{n})…", end=" ", flush=True)
        z_written = 0
        for x in range(n):
            x_dir = os.path.join(out_dir, str(z), str(x))
            for y in range(n):
                total += 1
                px0 = round(x * TARGET_W / n);  py0 = round(y * TARGET_H / n)
                px1 = round((x+1) * TARGET_W / n); py1 = round((y+1) * TARGET_H / n)
                patch = rgba[py0:py1, px0:px1]
                if patch[:, :, 3].max() == 0:
                    continue
                img = Image.fromarray(patch, mode="RGBA")
                if img.size != (TILE_SIZE, TILE_SIZE):
                    img = img.resize((TILE_SIZE, TILE_SIZE), Image.NEAREST)
                os.makedirs(x_dir, exist_ok=True)
                img.save(os.path.join(x_dir, f"{y}.png"), format="PNG", optimize=False)
                written += 1
                z_written += 1
        print(f"{z_written} tiles")

    print(f"  Done: {written}/{total} tiles → {out_dir}/")


def main():
    generate_tiles(
        "source/resolve_biomes_2017.tif",
        os.path.join(TILES_DIR, "biomes-current"),
        "RESOLVE 2017 Current Biomes",
    )
    generate_tiles(
        "source/resolve_rf_projected_2050.tif",
        os.path.join(TILES_DIR, "biomes-2050"),
        "Projected 2050 Biomes (RF ensemble)",
    )

    BASE = "https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles"
    print(f"\nTile overlay URLs:")
    print(f"  Köppen 2050:       {BASE}/{{z}}/{{x}}/{{y}}.png")
    print(f"  Biomes (current):  {BASE}/biomes-current/{{z}}/{{x}}/{{y}}.png")
    print(f"  Biomes (2050):     {BASE}/biomes-2050/{{z}}/{{x}}/{{y}}.png")


if __name__ == "__main__":
    main()
