#!/usr/bin/env python3
"""
Generate XYZ Web Mercator tiles for biome layers:

  1. RESOLVE 2017 current biomes (14 classes)
     source: source/resolve_biomes_2017.tif
     output: tiles/biomes-current/{biome_slug}/{z}/{x}/{y}.png
             tiles/biomes-current/all/{z}/{x}/{y}.png

  2. Whittaker 2050 projected biomes (9 classes, CHELSA SSP3-7.0 2041-2070)
     source: source/whittaker_biomes_2050.tif
     output: tiles/biomes-2050/{biome_slug}/{z}/{x}/{y}.png
             tiles/biomes-2050/all/{z}/{x}/{y}.png

Zoom 0-6, nearest-neighbour resampling, transparent ocean tiles skipped.
"""

import os
import re
import numpy as np
import rasterio
import rasterio.warp
from rasterio.crs import CRS
from rasterio.enums import Resampling
from PIL import Image

TILES_DIR = "tiles"
MIN_ZOOM  = 0
MAX_ZOOM  = 6
TILE_SIZE = 256
ALPHA     = 200

# ── RESOLVE 2017 biome palette (official COLOR_BIO from SHP) ─────────────────
RESOLVE_BIOMES = {
    1:  ("Tropical & Subtropical Moist Broadleaf Forests",    "#38A700"),
    2:  ("Tropical & Subtropical Dry Broadleaf Forests",      "#CCCD65"),
    3:  ("Tropical & Subtropical Coniferous Forests",         "#88CE66"),
    4:  ("Temperate Broadleaf & Mixed Forests",               "#00734C"),
    5:  ("Temperate Conifer Forests",                         "#458970"),
    6:  ("Boreal Forests / Taiga",                            "#7AB6F5"),
    7:  ("Tropical & Subtropical Grasslands, Savannas & Shrublands", "#FEAA01"),
    8:  ("Temperate Grasslands, Savannas & Shrublands",       "#FEFF73"),
    9:  ("Flooded Grasslands & Savannas",                     "#BEE7FF"),
    10: ("Montane Grasslands & Shrublands",                   "#D6C39D"),
    11: ("Tundra",                                            "#9ED7C2"),
    12: ("Mediterranean Forests, Woodlands & Scrub",          "#FE0000"),
    13: ("Deserts & Xeric Shrublands",                        "#CC6767"),
    14: ("Mangroves",                                         "#FE01C4"),
}

# ── Whittaker 2050 biome palette ──────────────────────────────────────────────
WHITTAKER_BIOMES = {
    1: ("Tropical Rainforest",                    "#1A7F1A"),
    2: ("Tropical Seasonal Forest & Savanna",     "#8DB84E"),
    3: ("Subtropical Desert",                     "#E8C46A"),
    4: ("Temperate Rainforest",                   "#2D6E4E"),
    5: ("Temperate Seasonal Forest",              "#4E9B5A"),
    6: ("Woodland & Shrubland",                   "#C8A44A"),
    7: ("Temperate Grassland & Desert Scrub",     "#C8C87A"),
    8: ("Boreal Forest (Taiga)",                  "#7AB6F5"),
    9: ("Tundra & Ice",                           "#C8E8D8"),
}


# ── Helpers ───────────────────────────────────────────────────────────────────
def hex_to_rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build_lut(biome_dict, alpha):
    lut = np.zeros((256, 4), dtype=np.uint8)
    for pv, (name, color) in biome_dict.items():
        r, g, b = hex_to_rgb(color)
        lut[pv] = [r, g, b, alpha]
    return lut


def reproject_to_mercator(src_path, target_w=16384, target_h=16384):
    """Reproject source raster to Web Mercator, return uint8 band."""
    ORIGIN = 20037508.342789244
    dst_transform = rasterio.transform.from_bounds(
        -ORIGIN, -ORIGIN, ORIGIN, ORIGIN, target_w, target_h
    )
    dst_band = np.zeros((target_h, target_w), dtype=np.uint8)
    with rasterio.open(src_path) as src:
        rasterio.warp.reproject(
            source        = rasterio.band(src, 1),
            destination   = dst_band,
            src_crs       = src.crs,
            dst_crs       = CRS.from_epsg(3857),
            dst_transform = dst_transform,
            resampling    = Resampling.nearest,
        )
    return dst_band


def write_tiles(rgba_full, target_w, target_h, base_dir, label=""):
    written = total = 0
    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        n = 2 ** z
        for x in range(n):
            x_dir = os.path.join(base_dir, str(z), str(x))
            for y in range(n):
                total += 1
                px0 = round(x * target_w / n);  py0 = round(y * target_h / n)
                px1 = round((x+1) * target_w / n); py1 = round((y+1) * target_h / n)
                patch = rgba_full[py0:py1, px0:px1]
                if patch[:, :, 3].max() == 0:
                    continue
                img = Image.fromarray(patch, mode="RGBA")
                if img.size != (TILE_SIZE, TILE_SIZE):
                    img = img.resize((TILE_SIZE, TILE_SIZE), Image.NEAREST)
                os.makedirs(x_dir, exist_ok=True)
                img.save(os.path.join(x_dir, f"{y}.png"), format="PNG", optimize=False)
                written += 1
    tag = f"[{label}] " if label else ""
    print(f"    {tag}{written}/{total} tiles")
    return written


def process_dataset(tiff_path, biome_dict, out_dir, label):
    TARGET_W = TARGET_H = 16384
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  source: {tiff_path}")
    print(f"  output: {out_dir}/")
    print(f"  Reprojecting to Web Mercator {TARGET_W}×{TARGET_H}…")
    band = reproject_to_mercator(tiff_path, TARGET_W, TARGET_H)

    lut = build_lut(biome_dict, ALPHA)

    # Combined (all biomes)
    all_dir = os.path.join(out_dir, "all")
    print(f"  Generating 'all' tiles → {all_dir}/")
    rgba_all = lut[band]
    write_tiles(rgba_all, TARGET_W, TARGET_H, all_dir, label="all")

    # Per-biome
    print(f"  Generating per-biome tiles…")
    for pv, (name, color) in biome_dict.items():
        slug = slugify(name)
        biome_dir = os.path.join(out_dir, slug)
        r, g, b = hex_to_rgb(color)
        rgba = np.zeros((TARGET_H, TARGET_W, 4), dtype=np.uint8)
        mask = band == pv
        rgba[mask] = [r, g, b, ALPHA]
        px_count = int(mask.sum())
        write_tiles(rgba, TARGET_W, TARGET_H, biome_dir, label=f"{pv}: {name} ({px_count:,}px)")


def main():
    DATASETS = [
        (
            "source/resolve_biomes_2017.tif",
            RESOLVE_BIOMES,
            os.path.join(TILES_DIR, "biomes-current"),
            "RESOLVE 2017 Current Biomes (14 classes)",
        ),
        (
            "source/whittaker_biomes_2050.tif",
            WHITTAKER_BIOMES,
            os.path.join(TILES_DIR, "biomes-2050"),
            "Whittaker 2050 Projected Biomes (9 classes, CHELSA SSP3-7.0)",
        ),
    ]

    for tiff, biome_dict, out_dir, label in DATASETS:
        if not os.path.exists(tiff):
            print(f"SKIP (not found): {tiff}")
            continue
        process_dataset(tiff, biome_dict, out_dir, label)

    BASE = "https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles"
    print(f"\n{'='*60}")
    print("Tile overlay URLs for Google Earth Web:\n")
    print("  RESOLVE 2017 current biomes:")
    print(f"    All:  {BASE}/biomes-current/all/{{z}}/{{x}}/{{y}}.png")
    for pv, (name, _) in RESOLVE_BIOMES.items():
        print(f"    {pv:>2}: {name}")
        print(f"        {BASE}/biomes-current/{slugify(name)}/{{z}}/{{x}}/{{y}}.png")
    print()
    print("  Whittaker 2050 projected biomes:")
    print(f"    All:  {BASE}/biomes-2050/all/{{z}}/{{x}}/{{y}}.png")
    for pv, (name, _) in WHITTAKER_BIOMES.items():
        print(f"    {pv}: {name}")
        print(f"       {BASE}/biomes-2050/{slugify(name)}/{{z}}/{{x}}/{{y}}.png")


if __name__ == "__main__":
    main()
