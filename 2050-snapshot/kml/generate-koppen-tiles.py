#!/usr/bin/env python3
"""
Generate XYZ Web Mercator tiles for Köppen-Geiger 2050 climate zones.

Outputs two tile sets:
  tiles/{z}/{x}/{y}.png          — all zones combined
  tiles/{code}/{z}/{x}/{y}.png   — one directory per Köppen code (e.g. tiles/Af/)

Zoom levels 0–6, nearest-neighbour resampling, transparent ocean/nodata tiles skipped.

Feed a tile URL to Google Earth Web's Tile Overlay:
  https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles/{z}/{x}/{y}.png
  https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles/Af/{z}/{x}/{y}.png
  … etc.
"""

import os
import numpy as np
import rasterio
import rasterio.warp
from rasterio.crs import CRS
from rasterio.enums import Resampling
from PIL import Image

TIFF_PATH = "source/koppen_2041-2070_ssp370.tif"
TILES_DIR = "tiles"
MIN_ZOOM  = 0
MAX_ZOOM  = 6
TILE_SIZE = 256
ALPHA     = 180   # 0-255 overlay opacity

# ── Palette ──────────────────────────────────────────────────────────────────
KOPPEN_COLORS = {
    "Af":  "#0000F5",  "Am":  "#3475F6",  "Aw":  "#61A7F7",
    "BWh": "#E83423",  "BWk": "#F19C98",  "BSh": "#E8A63A",  "BSk": "#F9DD77",
    "Csa": "#FFFF55",  "Csb": "#C5C740",  "Csc": "#96952E",
    "Cwa": "#B0FCA0",  "Cwb": "#7CC471",  "Cwc": "#509541",
    "Cfa": "#D1FD6E",  "Cfb": "#92F95B",  "Cfc": "#64C43A",
    "Dsa": "#E934F6",  "Dsb": "#B526BF",  "Dsc": "#88388E",  "Dsd": "#8E668F",
    "Dwa": "#ACB1F9",  "Dwb": "#6075D3",  "Dwc": "#4F52AF",  "Dwd": "#2C0381",
    "Dfa": "#75FBFC",  "Dfb": "#66C4F8",  "Dfc": "#367C7C",  "Dfd": "#1A445C",
    "ET":  "#B2B2B2",  "EF":  "#686868",
}

RASTER_LEGEND = {
    1:"Af",  2:"Am",  3:"Aw",
    4:"BWh", 5:"BWk", 6:"BSh", 7:"BSk",
    8:"Csa", 9:"Csb", 10:"Csc",
    11:"Cwa",12:"Cwb",13:"Cwc",
    14:"Cfa",15:"Cfb",16:"Cfc",
    17:"Dsa",18:"Dsb",19:"Dsc",20:"Dsd",
    21:"Dwa",22:"Dwb",23:"Dwc",24:"Dwd",
    25:"Dfa",26:"Dfb",27:"Dfc",28:"Dfd",
    29:"ET", 30:"EF",
}

WEB_MERCATOR = CRS.from_epsg(3857)

# ── Helpers ──────────────────────────────────────────────────────────────────
def hex_to_rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def build_full_lut(alpha=ALPHA):
    """256×4 uint8 LUT: pixel value → RGBA for all zones combined."""
    lut = np.zeros((256, 4), dtype=np.uint8)
    for pv, code in RASTER_LEGEND.items():
        h = KOPPEN_COLORS.get(code, "")
        if h:
            r, g, b = hex_to_rgb(h)
            lut[pv] = [r, g, b, alpha]
    return lut


def write_tiles(rgba_full, target_w, target_h, base_dir, label=""):
    """Slice rgba_full into XYZ tiles and write non-transparent ones."""
    written = 0
    total   = 0
    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        n = 2 ** z
        for x in range(n):
            x_dir = os.path.join(base_dir, str(z), str(x))
            for y in range(n):
                total += 1
                px0 = round(x * target_w / n)
                py0 = round(y * target_h / n)
                px1 = round((x + 1) * target_w / n)
                py1 = round((y + 1) * target_h / n)

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
    print(f"  {tag}{written}/{total} tiles written")
    return written


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    if not os.path.exists(TIFF_PATH):
        raise FileNotFoundError(f"GeoTIFF not found: {TIFF_PATH}")

    # Full-globe Web Mercator raster — 16384 px wide ≈ zoom-6 resolution
    TARGET_W = 16384
    TARGET_H = 16384
    ORIGIN   = 20037508.342789244

    dst_transform = rasterio.transform.from_bounds(
        -ORIGIN, -ORIGIN, ORIGIN, ORIGIN, TARGET_W, TARGET_H
    )

    print("Opening source GeoTIFF and reprojecting to Web Mercator…")
    with rasterio.open(TIFF_PATH) as src:
        mercator_band = np.zeros((TARGET_H, TARGET_W), dtype=np.uint8)
        rasterio.warp.reproject(
            source        = rasterio.band(src, 1),
            destination   = mercator_band,
            src_crs       = src.crs,
            dst_crs       = WEB_MERCATOR,
            dst_transform = dst_transform,
            resampling    = Resampling.nearest,
        )
    print(f"  Reprojected: {TARGET_W}×{TARGET_H} px")

    # ── Combined layer ────────────────────────────────────────────────────────
    print(f"\nGenerating combined tile set → {TILES_DIR}/")
    full_lut  = build_full_lut()
    rgba_full = full_lut[mercator_band]
    write_tiles(rgba_full, TARGET_W, TARGET_H, TILES_DIR, label="all")

    # ── Per-zone layers ───────────────────────────────────────────────────────
    print(f"\nGenerating per-zone tile sets → {TILES_DIR}/{{code}}/…")
    total_zones = len(RASTER_LEGEND)
    for i, (pv, code) in enumerate(RASTER_LEGEND.items(), 1):
        hex_color = KOPPEN_COLORS.get(code, "")
        if not hex_color:
            continue

        r, g, b = hex_to_rgb(hex_color)

        # RGBA: only pixels matching this zone are visible
        rgba_zone        = np.zeros((TARGET_H, TARGET_W, 4), dtype=np.uint8)
        mask             = mercator_band == pv
        rgba_zone[mask]  = [r, g, b, ALPHA]

        zone_dir = os.path.join(TILES_DIR, code)
        print(f"  [{i}/{total_zones}] {code} ({mask.sum():,} px) → {zone_dir}/")
        write_tiles(rgba_zone, TARGET_W, TARGET_H, zone_dir, label=code)

    print("\nDone.")
    print()
    print("Tile overlay URLs for Google Earth Web:")
    print(f"  All zones:  https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles/{{z}}/{{x}}/{{y}}.png")
    for code in KOPPEN_COLORS:
        print(f"  {code:<4}: https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles/{code}/{{z}}/{{x}}/{{y}}.png")


if __name__ == "__main__":
    main()
