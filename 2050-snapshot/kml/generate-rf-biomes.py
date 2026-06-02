#!/usr/bin/env python3
"""
Train a Random Forest classifier on RESOLVE 2017 biome labels + CHELSA historical
bioclimatic variables, then predict projected biomes for 2041-2070 using an
ensemble of all 5 CHELSA CMIP6 GCMs (majority vote per pixel).

Post-processing rules applied after majority vote:
  1. Desert (13) + mean future bio12 > 250 mm  → reassign to 2nd-best voted class
  2. Any class + Köppen 2050 = ET (29) or EF (30)  → Tundra (11)
  3. Boreal/Taiga (6) in non-boreal Köppen climates (Dfa/Dwa/Dsa/Bsk/…)
     → reassign to 2nd-best voted class

Caching:
  - Trained RF model saved to source/rf_model.joblib  (skip retrain if present)
  - Vote array saved to source/rf_votes.npy            (skip re-prediction if present)

Streams all 19 CHELSA bioclim variables directly over HTTP — no large downloads.
Reads at 0.1° resolution (3600×1800).

GCMs used (all available in CHELSA V2.1 SSP3-7.0):
  GFDL-ESM4, IPSL-CM6A-LR, MPI-ESM1-2-HR, MRI-ESM2-0, UKESM1-0-LL

Inputs:
  source/resolve_biomes_2017.tif    — RESOLVE labels (local)
  source/koppen_2041-2070_ssp370.tif — GloH2O V3 Köppen (local, for ET/EF override)
  CHELSA V2.1 bio01-bio19           — streamed over HTTP (historical + 5 future GCMs)

Output:
  source/resolve_rf_projected_2050.tif   — uint8, RESOLVE biome IDs 1-14

Runtime: ~25-30 min total (first run); faster on re-run with cached model/votes
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
import joblib

# ── Config ────────────────────────────────────────────────────────────────────
TARGET_H, TARGET_W = 1800, 3600   # 0.1° resolution
N_ESTIMATORS       = 200
N_JOBS             = -1
RANDOM_STATE       = 42

# Köppen class codes for ET and EF in GloH2O V3 numbering
KOPPEN_ET = 29
KOPPEN_EF = 30

RESOLVE_TIF = "source/resolve_biomes_2017.tif"
KOPPEN_TIF  = "source/koppen_2041-2070_ssp370.tif"
OUT_TIF     = "source/resolve_rf_projected_2050.tif"
MODEL_PATH  = "source/rf_model.joblib"
VOTES_PATH  = "source/rf_votes.npy"

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
def read_layer(url_or_path, resampling=Resampling.average):
    with rasterio.open(url_or_path) as src:
        data = src.read(1, out_shape=(TARGET_H, TARGET_W),
                        resampling=resampling).astype(np.float32)
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


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    # ── RESOLVE labels ────────────────────────────────────────────────────────
    print("Loading RESOLVE 2017 biome labels…")
    with rasterio.open(RESOLVE_TIF) as src:
        resolve = src.read(1, out_shape=(TARGET_H, TARGET_W),
                           resampling=Resampling.nearest).astype(np.uint8)
    land_mask = resolve > 0
    print(f"  Land pixels: {land_mask.sum():,}")

    # ── Köppen 2050 (for ET/EF override) ─────────────────────────────────────
    print("Loading Köppen 2050 (for ET/EF post-processing)…")
    with rasterio.open(KOPPEN_TIF) as src:
        koppen = src.read(1, out_shape=(TARGET_H, TARGET_W),
                          resampling=Resampling.nearest).astype(np.uint8)
    polar_mask = (koppen == KOPPEN_ET) | (koppen == KOPPEN_EF)
    print(f"  Polar pixels (ET+EF): {polar_mask.sum():,}")

    # ── Train RF (or load from cache) ─────────────────────────────────────────
    if os.path.exists(MODEL_PATH):
        print(f"\nLoading cached RF model from {MODEL_PATH}…")
        clf = joblib.load(MODEL_PATH)
    else:
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
        joblib.dump(clf, MODEL_PATH)
        print(f"  Model saved to {MODEL_PATH}")

        print("\n  Top feature importances:")
        imp = clf.feature_importances_
        for i in np.argsort(imp)[::-1][:8]:
            print(f"    bio{i+1:02d}: {imp[i]:.3f}")

    # ── Predict for each GCM, accumulate votes ────────────────────────────────
    n_classes  = 15   # biome IDs 0-14

    if os.path.exists(VOTES_PATH):
        print(f"\nLoading cached votes from {VOTES_PATH}…")
        votes = np.load(VOTES_PATH)
        # Also load mean future bio12 for the desert fix — need to restream if not cached
        print("  (bio12 precip ensemble mean will be restreamed for desert post-processing)")
        bio12_sum = None
        bio12_count = 0
        for gcm in GCMS:
            url = future_url(12, gcm)
            print(f"  Streaming bio12 for {gcm}…", end=" ", flush=True)
            t0 = time.time()
            layer = read_layer(url)
            print(f"{time.time()-t0:.1f}s")
            if bio12_sum is None:
                bio12_sum = np.where(np.isnan(layer), 0.0, layer)
            else:
                bio12_sum += np.where(np.isnan(layer), 0.0, layer)
            bio12_count += 1
        bio12_mean = bio12_sum / bio12_count
    else:
        votes      = np.zeros((TARGET_H, TARGET_W, n_classes), dtype=np.uint8)
        bio12_sum  = None
        bio12_count = 0

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

            # Accumulate bio12 (index 11) for desert precipitation check
            bio12 = fut_stack[:, :, 11]  # bio12 = precipitation_annual
            if bio12_sum is None:
                bio12_sum = np.where(np.isnan(bio12), 0.0, bio12)
            else:
                bio12_sum += np.where(np.isnan(bio12), 0.0, bio12)
            bio12_count += 1

            print(f"  {gcm} done.")

        np.save(VOTES_PATH, votes)
        print(f"\nVotes saved to {VOTES_PATH}")
        bio12_mean = bio12_sum / bio12_count

    # ── Majority vote across GCMs ─────────────────────────────────────────────
    print("\nComputing majority vote across GCMs…")
    result = np.argmax(votes, axis=2).astype(np.uint8)
    result[~land_mask] = 0   # restore ocean/nodata

    # ── Post-processing rule 1: Desert + precip > 250 mm → 2nd-best class ─────
    #    CHELSA bio12 is in mm (integer stored as mm directly in V2.1)
    desert_precip_mask = (result == 13) & land_mask & (bio12_mean > 250)
    n_fixed_desert = int(desert_precip_mask.sum())
    if n_fixed_desert > 0:
        print(f"\nPost-processing: fixing {n_fixed_desert:,} desert pixels with bio12 > 250 mm…")
        rows, cols = np.where(desert_precip_mask)
        for r, c in zip(rows, cols):
            v = votes[r, c].copy()
            v[13] = 0   # zero out Desert vote
            second_best = int(np.argmax(v))
            result[r, c] = second_best if second_best > 0 else 8  # fallback: temp grasslands
        print(f"  Done.")

    # ── Post-processing rule 2: Köppen ET/EF → Tundra (11) ───────────────────
    polar_land_mask = polar_mask & land_mask
    n_polar = int(polar_land_mask.sum())
    if n_polar > 0:
        print(f"\nPost-processing: overriding {n_polar:,} Köppen ET/EF pixels → Tundra (11)…")
        result[polar_land_mask] = 11
        print(f"  Done.")

    # ── Post-processing rule 3: Boreal in non-boreal climates → 2nd best ────
    #    Köppen climates that cannot support Boreal/Taiga:
    #    Hot: Dfa(25), Dwa(21), Dsa(17)
    #    Temperate: Cfa(14), Cfb(15), Csc(10), Csa(8), Csb(9), Cwa(11), Cwb(12), Cwc(13)
    #    Arid: BWh(4), BWk(5), BSh(6), BSk(7)
    #    Cfc(16) is subpolar oceanic — marginal, include as flagged.
    NON_BOREAL_KOPPEN = {4,5,6,7,8,9,10,11,12,13,14,15,17,21,25}
    boreal_bad = (result == 6) & land_mask & np.isin(koppen, list(NON_BOREAL_KOPPEN))
    n_boreal = int(boreal_bad.sum())
    if n_boreal > 0:
        print(f"\nPost-processing: fixing {n_boreal:,} Boreal(6) pixels in non-boreal Köppen climates…")
        rows, cols = np.where(boreal_bad)
        for r, c in zip(rows, cols):
            v = votes[r, c].copy()
            v[6] = 0
            second_best = int(np.argmax(v))
            result[r, c] = second_best if second_best > 0 else 8
        print(f"  Done.")

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
