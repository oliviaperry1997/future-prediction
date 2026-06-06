#!/usr/bin/env python3
"""
Generate XYZ Web Mercator tiles for coastal inundation zones — 2050,
SSP3-7.0, IPCC AR6 median SLR + Tebaldi-style flood levels.

Merges 3 zones into one image set (bottom to top):
  10-year flood (lightest blue)
  Annual flood  (medium blue)
  SLR baseline  (darkest blue)

Output: tiles/inundation-2050/{z}/{x}/{y}.png  (zoom 0-6)
"""

import os
import numpy as np
import rasterio
import rasterio.warp
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rasterio.features import rasterize
from scipy.ndimage import label, binary_dilation
from shapely.geometry import shape
from shapely.ops import unary_union
from PIL import Image
import fiona

ETOPO_TIF    = "source/ETOPO_2022_v1_60s_N90W180_surface.tif"
NE_LAND_ZIP  = "source/ne_10m_land.zip"
TILES_DIR    = "../../docs/tiles/inundation-2050"
MIN_ZOOM     = 0
MAX_ZOOM     = 6
TILE_SIZE    = 256

# Flood level thresholds (meters above current sea level)
# IPCC AR6 SSP3-7.0 median 2050: ~0.25m
# Annual flood: SLR + mean higher high water + typical storm surge (~3m globally)
# 10-year flood: SLR + extreme water level (~5m globally)
SLR_M      = 0.25
ANNUAL_M   = 3.0
TEN_YR_M   = 5.0

# Dilation: 1px (~1.8km) into cells with reasonable elevation
# Prevents "all coastlines lit up" by not expanding into steep terrain
DILATE      = 1
# Max elevation for dilation landward expansion per zone
SLR_MAX_ELEV   = 1.0
ANNUAL_MAX_ELEV = 6.0
TEN_YR_MAX_ELEV = 10.0

# Colors: darkest for SLR, lightest for 10-year
#                (R,  G,  B,  A)
SLR_RGBA    = (0,   50,  180, 200)
ANNUAL_RGBA = (50,  130, 230, 160)
TEN_YR_RGBA = (130, 190, 255, 120)

WEB_MERCATOR = CRS.from_epsg(3857)
TARGET_W = TARGET_H = 16384
ORIGIN = 20037508.342789244


def build_lut():
    lut = np.zeros((256, 4), dtype=np.uint8)
    lut[1] = SLR_RGBA
    lut[2] = ANNUAL_RGBA
    lut[3] = TEN_YR_RGBA
    return lut


def main():
    # ── Load ETOPO ───────────────────────────────────────────────────────
    print("Loading ETOPO 2022…", flush=True)
    src = rasterio.open(ETOPO_TIF)
    elev = src.read(1).astype(np.float32)
    transform = src.transform
    height, width = elev.shape
    src.close()
    print(f"  Grid {width}\u00d7{height}, {elev.min():.0f}\u2013{elev.max():.0f} m",
          flush=True)

    # ── Land mask from NE 10m vector data ──────────────────────────────
    # ETOPO-derived ocean seed includes below-sea-level land (Netherlands polders,
    # coastal deltas) because the 60s DEM doesn't resolve narrow barriers like
    # dunes or dikes. A vector land mask from NE 10m correctly classifies these
    # as land.
    print("Loading NE 10m land mask…", flush=True)
    ne_path = f"/vsizip/{os.path.abspath(NE_LAND_ZIP)}/ne_10m_land.shp"
    with fiona.open(ne_path) as lyr:
        geoms = [shape(f["geometry"]) for f in lyr]
    land_geom = unary_union(geoms)
    land = rasterize(
        [(land_geom, 1)], out_shape=(height, width),
        transform=transform, fill=0, dtype="uint8", all_touched=False,
    ).astype(bool)
    print(f"  {land.sum():,} land cells", flush=True)

    # ── Ocean seed for flood connectivity (largest ≤ 0m component) ─────
    print("Identifying ocean via connected components (elev ≤ 0m)…", flush=True)
    ocean_mask = elev <= 0
    labels, _ = label(ocean_mask, structure=np.ones((3, 3), dtype=bool))
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    ocean_seed = labels == sizes.argmax()
    print(f"  {ocean_seed.sum():,} ocean seed cells", flush=True)
    del ocean_mask, labels, sizes

    # ── Flood-fill for each level via connected components ───────────────
    struct = np.ones((3, 3), dtype=bool)

    def flood(threshold):
        mask = ocean_seed | (elev <= threshold)
        labels, _ = label(mask, structure=struct)
        ocean_val = labels[ocean_seed][0]
        return labels == ocean_val

    def flooded_land(threshold, max_dilate_elev):
        f = flood(threshold)
        fl = f & land
        dilated = binary_dilation(fl, structure=struct, iterations=DILATE)
        return dilated & (elev <= max_dilate_elev) & land

    print(f"Flood 10-year (≤{TEN_YR_M}m, dilation ≤{TEN_YR_MAX_ELEV}m)…", flush=True)
    flooded_10yr = flooded_land(TEN_YR_M, TEN_YR_MAX_ELEV)
    print(f"Flood annual (≤{ANNUAL_M}m, dilation ≤{ANNUAL_MAX_ELEV}m)…", flush=True)
    flooded_ann = flooded_land(ANNUAL_M, ANNUAL_MAX_ELEV)
    print(f"Flood SLR (≤{SLR_M}m, dilation ≤{SLR_MAX_ELEV}m)…", flush=True)
    flooded_slr = flooded_land(SLR_M, SLR_MAX_ELEV)

    # ── Composite: show only newly flooded land ─
    # Order: 10-year (lightest, widest) first, then annual, then SLR (darkest)
    composite = np.zeros((height, width), dtype=np.uint8)
    composite[flooded_10yr] = 3
    composite[flooded_ann]  = 2
    composite[flooded_slr]  = 1
    del flooded_10yr, flooded_ann, flooded_slr, ocean_seed, land

    n = {1: int((composite == 1).sum()),
         2: int((composite == 2).sum()),
         3: int((composite == 3).sum())}
    for total, label_txt in [(n[1]+n[2]+n[3], "total"),
                              (n[1], "SLR"), (n[2], "annual"), (n[3], "10-year")]:
        pct = total / (height*width) * 100
        if label_txt == "total":
            print(f"  Flooded {total:,} cells ({pct:.3f}%)", flush=True)
        else:
            print(f"    {label_txt}: {total:,} ({pct:.3f}%)", flush=True)
    del elev

    # ── Reproject to Web Mercator ───────────────────────────────────────
    dst_transform = rasterio.transform.from_bounds(
        -ORIGIN, -ORIGIN, ORIGIN, ORIGIN, TARGET_W, TARGET_H
    )
    print(f"Reprojecting to {TARGET_H}\u00d7{TARGET_W} Web Mercator…", flush=True)
    band = np.zeros((TARGET_H, TARGET_W), dtype=np.uint8)
    rasterio.warp.reproject(
        source=composite, destination=band,
        src_crs="EPSG:4326", dst_crs=WEB_MERCATOR,
        src_transform=transform,
        dst_transform=dst_transform, resampling=Resampling.nearest,
    )
    del composite

    # ── Apply colour LUT ────────────────────────────────────────────────
    print("Applying colour LUT…", flush=True)
    rgba = build_lut()[band]
    del band

    # ── Generate tiles ───────────────────────────────────────────────────
    written = total = 0
    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        n = 2 ** z
        print(f"Zoom {z} ({n}\u00d7{n})…", flush=True)
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

    total_mb = sum(os.path.getsize(os.path.join(dp, f))
                   for dp, _, fn in os.walk(TILES_DIR)
                   for f in fn if f.endswith(".png")) / (1024*1024)
    print(f"\nDone. {written}/{total} tiles written, {total_mb:.1f} MB")
    print("Tile overlay URL (GitHub Pages):")
    print("  https://oliviaperry1997.github.io/future-prediction/tiles/inundation-2050/{z}/{x}/{y}.png")
    print("Local (serve-tiles.py):")
    print("  http://localhost:8080/tiles/inundation-2050/{z}/{x}/{y}.png")


if __name__ == "__main__":
    main()
