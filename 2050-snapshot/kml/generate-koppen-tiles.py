#!/usr/bin/env python3
"""
Generate XYZ Web Mercator tiles for Köppen-Geiger 2050 climate zones (combined).

Output: tiles/climate-2050/{z}/{x}/{y}.png  (zoom levels 0–6)

Water pixels (oceans, seas, lakes) masked using Natural Earth 10m land,
rasterized at the source TIF's native resolution so boundaries match
the data pixel size.
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

TIFF_PATH = "source/koppen_2041-2070_ssp370.tif"
TILES_DIR = "../../docs/tiles/climate-2050"
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

NE_LAND_URL = "https://naciscdn.org/naturalearth/10m/physical/ne_10m_land.zip"
NE_LAND_ZIP = "source/ne_10m_land.zip"


def get_land_mask_4326(h, w):
    """Return boolean array (h, w) EPSG:4326, True where pixel is land."""
    cache_path = f"source/ne_land_mask_{h}x{w}.npy"
    if os.path.exists(cache_path):
        print(f"  Loading cached land mask ({h}×{w})…")
        return np.load(cache_path)

    if not os.path.exists(NE_LAND_ZIP):
        print(f"  Downloading Natural Earth 10m land…", flush=True)
        subprocess.run(["curl", "-L", NE_LAND_URL, "-o", NE_LAND_ZIP], check=True)

    print(f"  Rasterizing land polygon at {h}×{w} EPSG:4326…")
    t = rasterio.transform.from_bounds(-180, -90, 180, 90, w, h)

    geoms = []
    with zipfile.ZipFile(NE_LAND_ZIP) as zf:
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

    print(f"  {len(geoms)} land polygons")
    mask = rasterio.features.rasterize(
        geoms, out_shape=(h, w),
        transform=t, fill=0, default_value=1, dtype="uint8"
    ).astype(bool)

    np.save(cache_path, mask)
    print(f"  Mask saved to {cache_path}")
    return mask


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

    # ── Read source band at native resolution ────────────────────────────────
    with rasterio.open(TIFF_PATH) as src:
        src_h, src_w = src.height, src.width
        print(f"Reading source ({src_h}×{src_w})…")
        src_band = src.read(1).astype(np.uint8)
        src_crs = src.crs
        src_transform = src.transform

    # ── Land mask at source resolution (zero out water) ─────────────────────
    land_mask = get_land_mask_4326(src_h, src_w)
    water_mask = ~land_mask
    n_water = int(((src_band > 0) & water_mask).sum())
    src_band[water_mask] = 0
    print(f"Zeroed {n_water:,} water pixels")

    # ── Reproject to Web Mercator ────────────────────────────────────────────
    print(f"Reprojecting to {TARGET_H}×{TARGET_W} Web Mercator…")
    band = np.zeros((TARGET_H, TARGET_W), dtype=np.uint8)
    rasterio.warp.reproject(
        source=src_band, destination=band,
        src_crs=src_crs, dst_crs=WEB_MERCATOR,
        src_transform=src_transform,
        dst_transform=dst_transform, resampling=Resampling.nearest,
    )

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
    print("Tile overlay URL (GitHub Pages):")
    print("  https://oliviaperry1997.github.io/future-prediction/tiles/climate-2050/{z}/{x}/{y}.png")
    print("Local (serve-tiles.py):")
    print("  http://localhost:8080/tiles/climate-2050/{z}/{x}/{y}.png")


if __name__ == "__main__":
    main()
