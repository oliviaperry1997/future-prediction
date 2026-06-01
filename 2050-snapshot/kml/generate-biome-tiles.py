#!/usr/bin/env python3
"""
Generate XYZ Web Mercator tiles for biome layers (combined, one tileset each).

  RESOLVE 2017 current biomes (14 classes):
    source: source/resolve_biomes_2017.tif
    output: tiles/biomes-current/{z}/{x}/{y}.png

  Projected 2050 biomes via Köppen→RESOLVE crosswalk (10 of 14 RESOLVE classes):
    source: source/resolve_projected_2050.tif
    output: tiles/biomes-2050/{z}/{x}/{y}.png

Zoom 0-6, nearest-neighbour, transparent ocean/nodata tiles skipped.

Tile overlay URLs for Google Earth Web:
  https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles/biomes-current/{z}/{x}/{y}.png
  https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles/biomes-2050/{z}/{x}/{y}.png
"""

import os
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
    print(f"  Reprojecting {tiff_path} to Web Mercator…")
    with rasterio.open(tiff_path) as src:
        band = np.zeros((TARGET_H, TARGET_W), dtype=np.uint8)
        rasterio.warp.reproject(
            source=rasterio.band(src, 1), destination=band,
            src_crs=src.crs, dst_crs=WEB_MERCATOR,
            dst_transform=dst_transform, resampling=Resampling.nearest,
        )

    # lut determined by passed biome_dict
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
        "source/resolve_projected_2050.tif",
        os.path.join(TILES_DIR, "biomes-2050"),
        "Projected 2050 Biomes (Köppen→RESOLVE crosswalk)",
    )

    BASE = "https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles"
    print(f"\nTile overlay URLs:")
    print(f"  Köppen 2050:       {BASE}/{{z}}/{{x}}/{{y}}.png")
    print(f"  Biomes (current):  {BASE}/biomes-current/{{z}}/{{x}}/{{y}}.png")
    print(f"  Biomes (2050):     {BASE}/biomes-2050/{{z}}/{{x}}/{{y}}.png")


if __name__ == "__main__":
    main()
