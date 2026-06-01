#!/usr/bin/env python3
"""
Train a Random Forest classifier on RESOLVE 2017 biome labels + CHELSA historical
bioclimatic variables, then predict projected biomes for 2041-2070 using an
ensemble of all 5 CHELSA CMIP6 GCMs (majority vote per pixel), followed by
a spatial majority filter to remove isolated noisy patches.

Streams all 19 CHELSA bioclim variables directly over HTTP — no large downloads.
Reads at 0.1° resolution (3600×1800).

GCMs used (all available in CHELSA V2.1 SSP3-7.0):
  GFDL-ESM4, IPSL-CM6A-LR, MPI-ESM1-2-HR, MRI-ESM2-0, UKESM1-0-LL

Inputs:
  source/resolve_biomes_2017.tif    — RESOLVE labels (local)
  CHELSA V2.1 bio01-bio19           — streamed over HTTP (historical + 5 future GCMs)

Output:
  source/resolve_rf_projected_2050.tif   — uint8, RESOLVE biome IDs 1-14

Runtime: ~25-30 min total
"""

import os
import time
import numpy as np
import rasterio
import rasterio.warp
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rasterio.transform import from_bounds
from scipy.ndimage import generic_filter
from sklearn.ensemble import RandomForestClassifier

# ── Config ────────────────────────────────────────────────────────────────────
TARGET_H, TARGET_W = 1800, 3600   # 0.1° resolution
N_ESTIMATORS       = 200
N_JOBS             = -1
RANDOM_STATE       = 42
FILTER_SIZE        = 5            # majority filter window (pixels); 5 = ~55km at equator

RESOLVE_TIF = "source/resolve_biomes_2017.tif"
OUT_TIF     = "source/resolve_rf_projected_2050.tif"

CHELSA_BASE = "https://os.unil.cloud.switch.ch/chelsa02/chelsa/global/bioclim"

GCMS = [
    "GFDL-ESM4",
    "IPSL-CM6A-LR",
    "MPI-ESM1-2-HR",
    "MRI-ESM2-0",
    "UKESM1-0-LL",
]

BIO_NUMS = list(range(1, 20))

RESOLVE_NAMES = {
    1:  "Trop Moist BL Forests",        2:  "Trop Dry BL Forests",
    3:  "Trop Coniferous Forests",       4:  "Temp BL & Mixed Forests",
    5:  "Temp Conifer Forests",          6:  "Boreal Forests / Taiga",
    7:  "Trop Grasslands/Savannas",      8:  "Temp Grasslands/Savannas",
    9:  "Flooded Grasslands",            10: "Montane Grasslands",
    11: "Tundra",                        12: "Mediterranean",
    13: "Deserts & Xeric Shrublands",    14: "Mangroves",
}


# ── URL helpers ───────────────────────────────────────────────────────────────
def historical_url(n):
    b = f"{n:02d}"
    return f"{CHELSA_BASE}/bio{b}/1981-2010/CHELSA_bio{b}_1981-2010_V.2.1.tif"

def future_url(n, gcm):
    b   = f"{n:02d}"
    gcm_lower = gcm.lower()
    return (f"{CHELSA_BASE}/bio{b}/2041-2070/{gcm}/ssp370/"
            f"CHELSA_{gcm_lower}_ssp370_bio{b}_2041-2070_V.2.1.tif")


# ── Raster helpers ────────────────────────────────────────────────────────────
def read_layer(url_or_path):
    with rasterio.open(url_or_path) as src:
        data = src.read(1, out_shape=(TARGET_H, TARGET_W),
                        resampling=Resampling.average).astype(np.float32)
        nd = src.nodata
    if nd is not None:
        data[data == nd] = np.nan
    return data

def stream_stack(url_fn, label, **kwargs):
    """Stream all 19 bio vars for one period/GCM. Returns (H, W, 19) float32."""
    layers = []
    for n in BIO_NUMS:
        url = url_fn(n, **kwargs) if kwargs else url_fn(n)
        t0  = time.time()
        layers.append(read_layer(url))
        print(f"    bio{n:02d}  {time.time()-t0:.1f}s", flush=True)
    stack = np.stack(layers, axis=-1)
    print(f"  [{label}] stack ready: {stack.shape}")
    return stack


# ── Majority filter (spatial smoothing) ──────────────────────────────────────
def majority_filter(arr, size=FILTER_SIZE, nodata=0):
    """
    Replace each pixel with the modal value in a (size×size) neighbourhood.
    Nodata pixels (0) are excluded from the vote and preserved as 0.
    """
    print(f"  Applying {size}×{size} majority filter…")

    def modal(window):
        vals = window[window != nodata].astype(np.int32)
        if len(vals) == 0:
            return nodata
        counts = np.bincount(vals, minlength=15)
        return np.argmax(counts)

    result = generic_filter(arr.astype(np.float64), modal,
                            size=size, mode="nearest").astype(np.uint8)
    result[arr == nodata] = nodata   # preserve original nodata
    return result


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    # ── RESOLVE labels ────────────────────────────────────────────────────────
    print("Loading RESOLVE 2017 biome labels…")
    with rasterio.open(RESOLVE_TIF) as src:
        resolve = src.read(1, out_shape=(TARGET_H, TARGET_W),
                           resampling=Resampling.nearest).astype(np.uint8)
    land_mask = resolve > 0
    print(f"  Land pixels: {land_mask.sum():,}")

    # ── Train RF on historical climate ───────────────────────────────────────
    print("\nStreaming CHELSA historical bioclim (1981-2010)…")
    hist_stack = stream_stack(historical_url, "historical")

    flat_labels = resolve[land_mask]
    flat_hist   = hist_stack[land_mask]
    valid       = ~np.isnan(flat_hist).any(axis=1)
    X_train, y_train = flat_hist[valid], flat_labels[valid]
    print(f"\nTraining RandomForest on {len(X_train):,} samples…")
    t0 = time.time()
    clf = RandomForestClassifier(n_estimators=N_ESTIMATORS, n_jobs=N_JOBS,
                                 random_state=RANDOM_STATE,
                                 class_weight="balanced", min_samples_leaf=5)
    clf.fit(X_train, y_train)
    print(f"  Trained in {time.time()-t0:.1f}s")

    print("\n  Top feature importances:")
    imp = clf.feature_importances_
    for i in np.argsort(imp)[::-1][:8]:
        print(f"    bio{i+1:02d}: {imp[i]:.3f}")

    # ── Predict for each GCM, accumulate votes ────────────────────────────────
    # votes[i, j, k] = number of GCMs that predicted class k at pixel (i,j)
    n_classes  = 15   # biome IDs 0-14
    votes      = np.zeros((TARGET_H, TARGET_W, n_classes), dtype=np.uint8)
    land_flat  = np.where(land_mask.ravel())[0]

    for gcm in GCMS:
        print(f"\nStreaming future bioclim — {gcm}…")
        fut_stack  = stream_stack(future_url, gcm, gcm=gcm)
        flat_fut   = fut_stack[land_mask]
        valid_fut  = ~np.isnan(flat_fut).any(axis=1)

        preds = np.zeros(land_mask.sum(), dtype=np.uint8)
        preds[valid_fut] = clf.predict(flat_fut[valid_fut]).astype(np.uint8)

        # Accumulate into votes grid
        pred_grid = np.zeros((TARGET_H, TARGET_W), dtype=np.uint8)
        pred_grid[land_mask] = preds
        for cls in range(1, n_classes):
            votes[:, :, cls] += (pred_grid == cls).astype(np.uint8)

        print(f"  {gcm} done.")

    # ── Majority vote across GCMs ─────────────────────────────────────────────
    print("\nComputing majority vote across GCMs…")
    result = np.argmax(votes, axis=2).astype(np.uint8)
    result[~land_mask] = 0   # restore ocean/nodata

    # ── Spatial majority filter ───────────────────────────────────────────────
    result = majority_filter(result, size=FILTER_SIZE)

    # ── Coverage stats ────────────────────────────────────────────────────────
    total = int((result > 0).sum())
    print(f"\nFinal projected biome coverage ({total:,} land pixels):")
    for bv in range(1, 15):
        cnt = int((result == bv).sum())
        if cnt > 0:
            print(f"  {bv:>2}: {RESOLVE_NAMES[bv]:<35} {cnt:>8,} px  ({100*cnt/total:.1f}%)")

    # ── Write GeoTIFF ──────────────────────────────────────────────────────────
    transform = from_bounds(-180, -90, 180, 90, TARGET_W, TARGET_H)
    with rasterio.open(OUT_TIF, "w", driver="GTiff",
                       height=TARGET_H, width=TARGET_W, count=1, dtype="uint8",
                       crs=CRS.from_epsg(4326), transform=transform,
                       nodata=0, compress="deflate") as dst:
        dst.write(result, 1)

    print(f"\nWritten: {OUT_TIF} ({os.path.getsize(OUT_TIF):,} bytes)")


if __name__ == "__main__":
    main()
