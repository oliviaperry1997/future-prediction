#!/usr/bin/env python3
"""
Train a Random Forest classifier on RESOLVE 2017 biome labels + CHELSA historical
bioclimatic variables, then predict projected biomes for 2041-2070 (SSP3-7.0).

Streams all 19 CHELSA bioclim variables directly over HTTP — no large downloads.
Reads at 0.1° resolution (3600×1800) matching the Köppen raster.

Inputs:
  source/resolve_biomes_2017.tif               — RESOLVE labels (local)
  CHELSA V2.1 bio01-bio19 historical (remote)  — training features
  CHELSA V2.1 bio01-bio19 SSP3-7.0 (remote)   — prediction features

Output:
  source/resolve_rf_projected_2050.tif         — uint8 raster, RESOLVE biome IDs 1-14

Usage:
  python3 generate-rf-biomes.py

Runtime: ~5 min (streaming + RF training + prediction)
"""

import os
import time
import numpy as np
import rasterio
import rasterio.warp
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rasterio.transform import from_bounds
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# ── Config ────────────────────────────────────────────────────────────────────
TARGET_H, TARGET_W = 1800, 3600   # 0.1° resolution
CHELSA_NODATA      = 65535
N_ESTIMATORS       = 200
N_JOBS             = -1           # use all CPU cores
RANDOM_STATE       = 42

RESOLVE_TIF  = "source/resolve_biomes_2017.tif"
OUT_TIF      = "source/resolve_rf_projected_2050.tif"

CHELSA_BASE  = "https://os.unil.cloud.switch.ch/chelsa02/chelsa/global/bioclim"

def historical_url(n):
    b = f"{n:02d}"
    return f"{CHELSA_BASE}/bio{b}/1981-2010/CHELSA_bio{b}_1981-2010_V.2.1.tif"

def future_url(n):
    b = f"{n:02d}"
    return f"{CHELSA_BASE}/bio{b}/2041-2070/GFDL-ESM4/ssp370/CHELSA_gfdl-esm4_ssp370_bio{b}_2041-2070_V.2.1.tif"

BIO_NUMS = list(range(1, 20))   # bio01 – bio19

RESOLVE_NAMES = {
    1:  "Trop Moist BL Forests",
    2:  "Trop Dry BL Forests",
    3:  "Trop Coniferous Forests",
    4:  "Temp BL & Mixed Forests",
    5:  "Temp Conifer Forests",
    6:  "Boreal Forests / Taiga",
    7:  "Trop Grasslands/Savannas",
    8:  "Temp Grasslands/Savannas",
    9:  "Flooded Grasslands",
    10: "Montane Grasslands",
    11: "Tundra",
    12: "Mediterranean",
    13: "Deserts & Xeric Shrublands",
    14: "Mangroves",
}


# ── Helpers ───────────────────────────────────────────────────────────────────
def read_layer(url_or_path, target_h=TARGET_H, target_w=TARGET_W):
    """Read a single-band raster resampled to target resolution. Returns float32."""
    with rasterio.open(url_or_path) as src:
        data = src.read(
            1,
            out_shape=(target_h, target_w),
            resampling=Resampling.average,
        ).astype(np.float32)
        nd = src.nodata
    if nd is not None:
        data[data == nd] = np.nan
    return data


def stream_bioclim_stack(url_fn, label):
    """Stream all 19 bioclim variables, return (H, W, 19) float32 array."""
    layers = []
    for n in BIO_NUMS:
        url = url_fn(n)
        t0 = time.time()
        layer = read_layer(url)
        elapsed = time.time() - t0
        print(f"    bio{n:02d}  {elapsed:.1f}s")
        layers.append(layer)
    stack = np.stack(layers, axis=-1)   # (H, W, 19)
    print(f"  {label} stack: {stack.shape}")
    return stack


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    # ── Load RESOLVE biome labels at target resolution ────────────────────────
    print("Loading RESOLVE 2017 biome labels…")
    with rasterio.open(RESOLVE_TIF) as src:
        resolve = src.read(
            1,
            out_shape=(TARGET_H, TARGET_W),
            resampling=Resampling.nearest,
        ).astype(np.uint8)

    land_mask = resolve > 0
    print(f"  Land pixels: {land_mask.sum():,} / {land_mask.size:,}")

    label_counts = {v: int((resolve == v).sum()) for v in range(1, 15)}
    print("  Biome distribution:")
    for bv, cnt in label_counts.items():
        if cnt > 0:
            print(f"    {bv:>2}: {RESOLVE_NAMES[bv]:<30} {cnt:>8,}")

    # ── Stream historical bioclim stack (training features) ───────────────────
    print("\nStreaming CHELSA historical bioclim (1981-2010)…")
    hist_stack = stream_bioclim_stack(historical_url, "historical")

    # ── Build training set ────────────────────────────────────────────────────
    print("\nBuilding training set…")
    flat_labels = resolve[land_mask]              # (N,)
    flat_hist   = hist_stack[land_mask]           # (N, 19)

    # Remove pixels where any feature is NaN
    valid_rows  = ~np.isnan(flat_hist).any(axis=1)
    X_train     = flat_hist[valid_rows]
    y_train     = flat_labels[valid_rows]
    print(f"  Training samples: {len(X_train):,}  features: {X_train.shape[1]}")

    # ── Train Random Forest ───────────────────────────────────────────────────
    print(f"\nTraining RandomForest ({N_ESTIMATORS} trees, all cores)…")
    t0  = time.time()
    clf = RandomForestClassifier(
        n_estimators  = N_ESTIMATORS,
        n_jobs        = N_JOBS,
        random_state  = RANDOM_STATE,
        class_weight  = "balanced",   # handles rare biomes (mangroves, flooded)
        min_samples_leaf = 5,
    )
    clf.fit(X_train, y_train)
    elapsed = time.time() - t0
    print(f"  Trained in {elapsed:.1f}s")

    # Quick in-sample report (just to check classes learned)
    y_pred_train = clf.predict(X_train[:5000])
    print("\n  Top feature importances (bio number):")
    imp = clf.feature_importances_
    top = np.argsort(imp)[::-1][:8]
    for i in top:
        print(f"    bio{i+1:02d}: {imp[i]:.3f}")

    # ── Stream future bioclim stack (prediction features) ─────────────────────
    print("\nStreaming CHELSA future bioclim (2041-2070, SSP3-7.0)…")
    future_stack = stream_bioclim_stack(future_url, "future")

    # ── Predict on future climate for all land pixels ─────────────────────────
    print("\nPredicting 2050 biomes…")
    flat_future = future_stack[land_mask]          # (N, 19)
    valid_fut   = ~np.isnan(flat_future).any(axis=1)

    predictions = np.zeros(land_mask.sum(), dtype=np.uint8)
    predictions[valid_fut] = clf.predict(flat_future[valid_fut]).astype(np.uint8)

    result = np.zeros((TARGET_H, TARGET_W), dtype=np.uint8)
    result[land_mask] = predictions

    # ── Coverage stats ────────────────────────────────────────────────────────
    total = int((result > 0).sum())
    print(f"\nProjected biome coverage ({total:,} land pixels):")
    for bv in range(1, 15):
        cnt = int((result == bv).sum())
        if cnt > 0:
            pct = 100 * cnt / total
            print(f"  {bv:>2}: {RESOLVE_NAMES[bv]:<35} {cnt:>8,} px  ({pct:.1f}%)")

    # ── Write output GeoTIFF ──────────────────────────────────────────────────
    transform = from_bounds(-180, -90, 180, 90, TARGET_W, TARGET_H)
    with rasterio.open(
        OUT_TIF, "w",
        driver="GTiff", height=TARGET_H, width=TARGET_W,
        count=1, dtype="uint8",
        crs=CRS.from_epsg(4326), transform=transform,
        nodata=0, compress="deflate",
    ) as dst:
        dst.write(result, 1)

    print(f"\nWritten: {OUT_TIF} ({os.path.getsize(OUT_TIF):,} bytes)")


if __name__ == "__main__":
    main()
