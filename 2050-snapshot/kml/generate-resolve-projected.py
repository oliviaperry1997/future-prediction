#!/usr/bin/env python3
"""
Project RESOLVE biome classes to 2050 using a Köppen-Geiger crosswalk.

Each Köppen zone is mapped to its best-fit RESOLVE biome class (1-14),
using the correspondence documented in Kottek et al. 2006, Beck et al. 2018,
and the original Whittaker/Walter vegetation zone literature.

Input:  source/koppen_2041-2070_ssp370.tif  (GloH2O V3, pixel values 1-30)
Output: source/resolve_projected_2050.tif   (uint8, values 1-14)

RESOLVE biome IDs:
  1   Tropical & Subtropical Moist Broadleaf Forests
  2   Tropical & Subtropical Dry Broadleaf Forests
  3   Tropical & Subtropical Coniferous Forests
  4   Temperate Broadleaf & Mixed Forests
  5   Temperate Conifer Forests
  6   Boreal Forests / Taiga
  7   Tropical & Subtropical Grasslands, Savannas & Shrublands
  8   Temperate Grasslands, Savannas & Shrublands
  9   Flooded Grasslands & Savannas   (no direct K\u00f6ppen equivalent — omitted)
  10  Montane Grasslands & Shrublands (no direct K\u00f6ppen equivalent — omitted)
  11  Tundra
  12  Mediterranean Forests, Woodlands & Scrub
  13  Deserts & Xeric Shrublands
  14  Mangroves                       (no direct K\u00f6ppen equivalent — omitted)

K\u00f6ppen → RESOLVE crosswalk rationale:
  Af  Tropical rainforest      → 1  (Tropical Moist BL)
  Am  Tropical monsoon         → 1  (still moist enough for rainforest)
  Aw  Tropical savanna         → 7  (Trop/Subtr Grasslands/Savannas)

  BWh Hot desert               → 13 (Deserts & Xeric Shrublands)
  BWk Cold desert              → 13
  BSh Hot steppe               → 13 (semi-arid; closer to xeric than savanna)
  BSk Cold steppe              → 8  (Temperate Grasslands — cold steppe)

  Csa Hot-summer Mediterranean → 12 (Mediterranean)
  Csb Warm-summer Mediterranean→ 12
  Csc Cold-summer Mediterranean→ 12
  Cwa Humid subtropical, dry W → 2  (Trop/Subtr Dry BL Forests)
  Cwb Subtropical highland     → 2
  Cwc Subpolar oceanic, dry W  → 4  (Temperate BL — cool variant)
  Cfa Humid subtropical        → 4  (Temperate BL & Mixed)
  Cfb Oceanic                  → 4
  Cfc Subpolar oceanic         → 5  (Temperate Conifer — cool)

  Dsa Hot-summer continental,dry→ 8  (Temperate Grasslands — semi-arid interior)
  Dsb Warm-summer continental,d → 8
  Dsc Subarctic, dry summer    → 6  (Boreal — dry subarctic)
  Dsd Subarctic, dry summer,vC → 6
  Dwa Humid continental, dry W → 4  (Temperate BL & Mixed)
  Dwb Warm humid continental,dW→ 4
  Dwc Subarctic, dry winter    → 6  (Boreal)
  Dwd Subarctic, dry winter,vC → 6
  Dfa Hot humid continental    → 4  (Temperate BL & Mixed)
  Dfb Cool humid continental   → 4
  Dfc Subarctic                → 6  (Boreal / Taiga)
  Dfd Subarctic, very cold     → 6

  ET  Tundra                   → 11 (Tundra)
  EF  Ice cap                  → 11 (Tundra/Ice — closest RESOLVE class)
"""

import os
import numpy as np
import rasterio

KOPPEN_TIF  = "source/koppen_2041-2070_ssp370.tif"
OUT_TIF     = "source/resolve_projected_2050.tif"

# Pixel value (1-30) → RESOLVE biome (1-14)
# RASTER_LEGEND: 1=Af … 30=EF (GloH2O V3 numbering)
KOPPEN_TO_RESOLVE = {
    1:  1,   # Af  → Tropical Moist BL Forests
    2:  1,   # Am  → Tropical Moist BL Forests
    3:  7,   # Aw  → Trop/Subtr Grasslands/Savannas/Shrublands
    4:  13,  # BWh → Deserts & Xeric Shrublands
    5:  13,  # BWk → Deserts & Xeric Shrublands
    6:  13,  # BSh → Deserts & Xeric Shrublands (hot semi-arid)
    7:  8,   # BSk → Temperate Grasslands/Savannas (cold steppe)
    8:  12,  # Csa → Mediterranean
    9:  12,  # Csb → Mediterranean
    10: 12,  # Csc → Mediterranean
    11: 2,   # Cwa → Trop/Subtr Dry BL Forests
    12: 2,   # Cwb → Trop/Subtr Dry BL Forests
    13: 4,   # Cwc → Temperate BL & Mixed Forests
    14: 4,   # Cfa → Temperate BL & Mixed Forests
    15: 4,   # Cfb → Temperate BL & Mixed Forests
    16: 5,   # Cfc → Temperate Conifer Forests
    17: 8,   # Dsa → Temperate Grasslands (semi-arid continental)
    18: 8,   # Dsb → Temperate Grasslands
    19: 6,   # Dsc → Boreal Forests / Taiga
    20: 6,   # Dsd → Boreal Forests / Taiga
    21: 4,   # Dwa → Temperate BL & Mixed Forests
    22: 4,   # Dwb → Temperate BL & Mixed Forests
    23: 6,   # Dwc → Boreal Forests / Taiga
    24: 6,   # Dwd → Boreal Forests / Taiga
    25: 4,   # Dfa → Temperate BL & Mixed Forests
    26: 4,   # Dfb → Temperate BL & Mixed Forests
    27: 6,   # Dfc → Boreal Forests / Taiga
    28: 6,   # Dfd → Boreal Forests / Taiga
    29: 11,  # ET  → Tundra
    30: 11,  # EF  → Tundra (ice cap — no RESOLVE class, closest is 11)
}

RESOLVE_NAMES = {
    1:  "Tropical & Subtropical Moist Broadleaf Forests",
    2:  "Tropical & Subtropical Dry Broadleaf Forests",
    4:  "Temperate Broadleaf & Mixed Forests",
    5:  "Temperate Conifer Forests",
    6:  "Boreal Forests / Taiga",
    7:  "Tropical & Subtropical Grasslands, Savannas & Shrublands",
    8:  "Temperate Grasslands, Savannas & Shrublands",
    11: "Tundra",
    12: "Mediterranean Forests, Woodlands & Scrub",
    13: "Deserts & Xeric Shrublands",
}


def main():
    if not os.path.exists(KOPPEN_TIF):
        raise FileNotFoundError(f"Köppen GeoTIFF not found: {KOPPEN_TIF}")

    print("Loading Köppen 2050 raster…")
    with rasterio.open(KOPPEN_TIF) as src:
        band    = src.read(1)
        profile = src.profile.copy()
        nodata  = src.nodata

    print(f"  Shape: {band.shape}, dtype: {band.dtype}")

    # Build LUT: 256 entries, 0 = nodata/ocean
    lut = np.zeros(256, dtype=np.uint8)
    for koppen_pv, resolve_bv in KOPPEN_TO_RESOLVE.items():
        lut[koppen_pv] = resolve_bv

    print("Applying crosswalk…")
    result = lut[band]
    if nodata is not None:
        result[band == int(nodata)] = 0

    # Print coverage stats
    total = int((result > 0).sum())
    print(f"\nProjected biome coverage ({total:,} land pixels):")
    for bv in sorted(RESOLVE_NAMES):
        count = int((result == bv).sum())
        pct   = 100 * count / total if total else 0
        print(f"  {bv:>2}: {RESOLVE_NAMES[bv]:<55} {count:>10,} px  ({pct:.1f}%)")

    profile.update(dtype="uint8", nodata=0, compress="deflate")
    with rasterio.open(OUT_TIF, "w", **profile) as dst:
        dst.write(result, 1)

    print(f"\nWritten: {OUT_TIF} ({os.path.getsize(OUT_TIF):,} bytes)")
    print("\nNote: RESOLVE biomes 3 (Trop/Subtr Coniferous), 9 (Flooded Grasslands),")
    print("      10 (Montane), and 14 (Mangroves) have no direct Köppen equivalent")
    print("      and are not represented in the projected output.")


if __name__ == "__main__":
    main()
