#!/usr/bin/env python3
"""
Generate XYZ Web Mercator tiles for Köppen-Geiger 2050 climate zones.

Output: tiles/{z}/{x}/{y}.png  (zoom levels 0–6)
Uses nearest-neighbor resampling to preserve sharp zone boundaries.

Feed the tile URL to Google Earth Web's Tile Overlay:
  http://localhost:8080/tiles/{z}/{x}/{y}.png
"""

import os
import math
import numpy as np
import rasterio
import rasterio.warp
from rasterio.crs import CRS
from PIL import Image

TIFF_PATH  = "source/koppen_2041-2070_ssp370.tif"
TILES_DIR  = "tiles"
MIN_ZOOM   = 0
MAX_ZOOM   = 6
TILE_SIZE  = 256
ALPHA      = 180   # 0-255 overlay opacity

# ── Palette (same as KMZ generator) ────────────────────────────────────────
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
    1:"Af", 2:"Am", 3:"Aw",
    4:"BWh", 5:"BWk", 6:"BSh", 7:"BSk",
    8:"Csa", 9:"Csb", 10:"Csc",
    11:"Cwa", 12:"Cwb", 13:"Cwc",
    14:"Cfa", 15:"Cfb", 16:"Cfc",
    17:"Dsa", 18:"Dsb", 19:"Dsc", 20:"Dsd",
    21:"Dwa", 22:"Dwb", 23:"Dwc", 24:"Dwd",
    25:"Dfa", 26:"Dfb", 27:"Dfc", 28:"Dfd",
    29:"ET", 30:"EF",
}

WEB_MERCATOR = CRS.from_epsg(3857)
WGS84        = CRS.from_epsg(4326)

# ── Colour LUT ──────────────────────────────────────────────────────────────
def build_color_lut(alpha=ALPHA):
    lut = np.zeros((256, 4), dtype=np.uint8)
    for pv, code in RASTER_LEGEND.items():
        h = KOPPEN_COLORS.get(code, "").lstrip("#")
        if len(h) == 6:
            lut[pv] = [int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), alpha]
    return lut


# ── Tile math ────────────────────────────────────────────────────────────────
def tile_bounds_mercator(z, x, y):
    """Return (west, south, east, north) in Web Mercator metres for tile z/x/y."""
    n = 2 ** z
    origin = 20037508.342789244
    tile_m  = 2 * origin / n
    west  = -origin + x * tile_m
    east  = west + tile_m
    north =  origin - y * tile_m
    south =  north - tile_m
    return west, south, east, north


def tile_bounds_wgs84(z, x, y):
    """Return (west, south, east, north) in WGS-84 degrees."""
    n = 2 ** z
    lon_w = x / n * 360.0 - 180.0
    lon_e = (x + 1) / n * 360.0 - 180.0
    lat_n = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    lat_s = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (y + 1) / n))))
    return lon_w, lat_s, lon_e, lat_n


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    if not os.path.exists(TIFF_PATH):
        raise FileNotFoundError(f"GeoTIFF not found: {TIFF_PATH}")

    lut = build_color_lut()

    # Reproject entire raster to Web Mercator once, into a big RGBA array.
    # For categorical data we use nearest-neighbour (Resampling.nearest).
    from rasterio.enums import Resampling

    print("Opening source GeoTIFF…")
    with rasterio.open(TIFF_PATH) as src:
        # Compute target transform / dimensions for a full-globe Web Mercator raster
        # at a resolution ~equivalent to zoom-6 tiles (256 * 2^6 = 16384 px wide).
        target_width  = 16384
        target_height = 16384

        origin = 20037508.342789244
        res = 2 * origin / target_width

        dst_transform = rasterio.transform.from_bounds(
            -origin, -origin, origin, origin,
            target_width, target_height
        )

        mercator_band = np.zeros((target_height, target_width), dtype=np.uint8)

        print(f"Reprojecting to Web Mercator {target_width}×{target_height}…")
        rasterio.warp.reproject(
            source      = rasterio.band(src, 1),
            destination = mercator_band,
            src_crs     = src.crs,
            dst_crs     = WEB_MERCATOR,
            dst_transform = dst_transform,
            resampling  = Resampling.nearest,
        )

    print("Applying colour LUT…")
    rgba_full = lut[mercator_band]   # (H, W, 4)

    total_tiles   = 0
    written_tiles = 0

    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        n = 2 ** z
        zoom_dir = os.path.join(TILES_DIR, str(z))
        print(f"Zoom {z}: {n}×{n} tiles…")

        for x in range(n):
            x_dir = os.path.join(zoom_dir, str(x))
            for y in range(n):
                total_tiles += 1

                # Pixel window within the full mercator image
                px0 = round(x * target_width  / n)
                py0 = round(y * target_height / n)
                px1 = round((x + 1) * target_width  / n)
                py1 = round((y + 1) * target_height / n)

                patch = rgba_full[py0:py1, px0:px1]   # may not be exactly 256×256

                # Skip fully transparent tiles
                if patch[:, :, 3].max() == 0:
                    continue

                # Resize to TILE_SIZE×TILE_SIZE (nearest-neighbour)
                img = Image.fromarray(patch, mode="RGBA")
                if img.size != (TILE_SIZE, TILE_SIZE):
                    img = img.resize((TILE_SIZE, TILE_SIZE), Image.NEAREST)

                os.makedirs(x_dir, exist_ok=True)
                tile_path = os.path.join(x_dir, f"{y}.png")
                img.save(tile_path, format="PNG", optimize=False)
                written_tiles += 1

        print(f"  zoom {z}: {written_tiles} tiles written so far")

    print(f"\nDone. {written_tiles}/{total_tiles} tiles written to {TILES_DIR}/")
    print("Transparent (ocean/nodata) tiles skipped.")


if __name__ == "__main__":
    main()
