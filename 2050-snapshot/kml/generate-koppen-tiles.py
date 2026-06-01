#!/usr/bin/env python3
"""
Generate XYZ Web Mercator tiles for Köppen-Geiger 2050 climate zones (combined).

Output: tiles/{z}/{x}/{y}.png  (zoom levels 0–6)

Feed the tile URL to Google Earth Web's Tile Overlay:
  https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles/{z}/{x}/{y}.png
"""

import os
import numpy as np
import rasterio
import rasterio.warp
from rasterio.crs import CRS
from rasterio.enums import Resampling
from PIL import Image

# ── Lake mask (reuse cached from biome pipeline) ──────────────────────────────
NE_LAKES_MASK = "source/ne_lakes_mask.npy"


def load_lake_mask(h, w):
    if not os.path.exists(NE_LAKES_MASK):
        print(f"Lake mask not found at {NE_LAKES_MASK}, skipping.")
        return None
    mask = np.load(NE_LAKES_MASK)
    if mask.shape != (h, w):
        print(f"Lake mask shape mismatch ({mask.shape} vs ({h},{w})), skipping.")
        return None
    return mask

TIFF_PATH = "source/koppen_2041-2070_ssp370.tif"
TILES_DIR = "tiles"
MIN_ZOOM  = 0
MAX_ZOOM  = 6
TILE_SIZE = 256
ALPHA     = 180

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


def hex_to_rgba(h, alpha=ALPHA):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha


def build_lut():
    lut = np.zeros((256, 4), dtype=np.uint8)
    for pv, code in RASTER_LEGEND.items():
        h = KOPPEN_COLORS.get(code, "")
        if h:
            lut[pv] = hex_to_rgba(h)
    return lut


def main():
    if not os.path.exists(TIFF_PATH):
        raise FileNotFoundError(f"GeoTIFF not found: {TIFF_PATH}")

    TARGET_W = TARGET_H = 16384
    ORIGIN = 20037508.342789244
    dst_transform = rasterio.transform.from_bounds(
        -ORIGIN, -ORIGIN, ORIGIN, ORIGIN, TARGET_W, TARGET_H
    )

    print("Reprojecting Köppen GeoTIFF to Web Mercator…")
    with rasterio.open(TIFF_PATH) as src:
        band = np.zeros((TARGET_H, TARGET_W), dtype=np.uint8)
        rasterio.warp.reproject(
            source=rasterio.band(src, 1), destination=band,
            src_crs=src.crs, dst_crs=WEB_MERCATOR,
            dst_transform=dst_transform, resampling=Resampling.nearest,
        )

    # ── Mask out lake pixels ────────────────────────────────────────────────────
    lake_mask = load_lake_mask(TARGET_H, TARGET_W)
    if lake_mask is not None:
        n_lake = int(((band > 0) & lake_mask).sum())
        band[lake_mask] = 0
        print(f"Zeroed {n_lake:,} lake pixels")

    print("Applying colour LUT…")
    rgba = build_lut()[band]

    written = total = 0
    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        n = 2 ** z
        print(f"Zoom {z} ({n}×{n})…")
        for x in range(n):
            x_dir = os.path.join(TILES_DIR, str(z), str(x))
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

    print(f"\nDone. {written}/{total} tiles → {TILES_DIR}/")
    print("Tile overlay URL:")
    print("  https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles/{z}/{x}/{y}.png")


if __name__ == "__main__":
    main()
