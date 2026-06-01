#!/usr/bin/env python3
"""
Derive projected Whittaker biomes for 2041-2070 (SSP3-7.0) from CHELSA V2.1.

Inputs (source/):
  CHELSA_bio01_2041-2070_gfdl-esm4_ssp370.tif  — Mean Annual Temp (raw uint16, K×10)
  CHELSA_bio12_2041-2070_gfdl-esm4_ssp370.tif  — Annual Precipitation (mm/year, uint16)

Output (source/):
  whittaker_biomes_2050.tif  — uint8 raster, values 1-9 (Whittaker biome classes)

Whittaker biome boundaries follow the classic temperature/precipitation diagram
(Whittaker 1975, as digitized by Ricklefs 2008 and widely cited):

  Biome ID  Name                                     RESOLVE equiv
  --------  ------                                   -------------
  1         Tropical Rainforest                      → biome 1 (Tropical Moist BL)
  2         Tropical Seasonal Forest/Savanna          → biome 2, 7
  3         Subtropical Desert                        → biome 13
  4         Temperate Rainforest                      → biome 4, 5
  5         Temperate Seasonal Forest                 → biome 4
  6         Woodland/Shrubland                        → biome 12
  7         Temperate Grassland/Desert Scrub          → biome 8, 10
  8         Boreal Forest (Taiga)                     → biome 6
  9         Tundra                                    → biome 11 + EF/ET

Boundaries (from Ricklefs/Whittaker):
  Temperature (°C) × Precipitation (mm/yr) defines biome membership.
  Rules applied in order (first match wins):
  - T > 20, P > 2000                 → Tropical Rainforest
  - T > 20, P > 1000                 → Tropical Seasonal Forest/Savanna
  - T > 20, P <= 1000                → Subtropical Desert
  - T 10-20, P > 1500                → Temperate Rainforest
  - T 10-20, P 750-1500              → Temperate Seasonal Forest
  - T 10-20, P 250-750               → Woodland/Shrubland
  - T 10-20, P < 250                 → Temperate Grassland/Desert Scrub
  - T 5-10,  any                     → Temperate Grassland/Desert Scrub
  - T 0-5,   P > 500                 → Boreal Forest
  - T 0-5,   P <= 500                → Tundra
  - T < 0                            → Tundra
"""

import os
import numpy as np
import rasterio
from rasterio.crs import CRS
from rasterio.transform import from_bounds

SRC_DIR = "source"
BIO01   = os.path.join(SRC_DIR, "CHELSA_bio01_2041-2070_gfdl-esm4_ssp370.tif")
BIO12   = os.path.join(SRC_DIR, "CHELSA_bio12_2041-2070_gfdl-esm4_ssp370.tif")
OUT_TIF = os.path.join(SRC_DIR, "whittaker_biomes_2050.tif")

NODATA_RAW = 65535

# Whittaker biome IDs and display names
WHITTAKER_BIOMES = {
    1: "Tropical Rainforest",
    2: "Tropical Seasonal Forest & Savanna",
    3: "Subtropical Desert",
    4: "Temperate Rainforest",
    5: "Temperate Seasonal Forest",
    6: "Woodland & Shrubland",
    7: "Temperate Grassland & Desert Scrub",
    8: "Boreal Forest (Taiga)",
    9: "Tundra & Ice",
}

# Colors chosen to roughly match RESOLVE palette intent + Whittaker diagram colors
WHITTAKER_COLORS = {
    1: "#1A7F1A",  # deep green — tropical rainforest
    2: "#8DB84E",  # yellow-green — tropical seasonal/savanna
    3: "#E8C46A",  # tan — subtropical desert
    4: "#2D6E4E",  # dark teal — temperate rainforest
    5: "#4E9B5A",  # medium green — temperate seasonal forest
    6: "#C8A44A",  # golden — woodland/shrubland
    7: "#C8C87A",  # pale yellow — temperate grassland/desert scrub
    8: "#7AB6F5",  # light blue — boreal forest (matches RESOLVE taiga)
    9: "#C8E8D8",  # pale mint — tundra/ice
}


def classify_whittaker(temp_c, precip_mm, nodata_mask):
    """
    Classify each pixel into Whittaker biome (1-9).
    Returns uint8 array, 0 = nodata.
    """
    out = np.zeros(temp_c.shape, dtype=np.uint8)

    # Work only on valid pixels
    valid = ~nodata_mask

    T = temp_c
    P = precip_mm

    # Apply rules in order — later rules overwrite earlier (we go coarse→fine)
    # Tundra / polar (lowest priority base)
    out[valid & (T < 5)]  = 9

    # Boreal forest
    out[valid & (T >= 0) & (T < 5)  & (P > 500)] = 8
    out[valid & (T >= 5) & (T < 10)]              = 8   # cool temperate → taiga-ish

    # Temperate zone (10-20°C)
    out[valid & (T >= 10) & (T < 20) & (P < 250)]          = 7  # grassland/desert scrub
    out[valid & (T >= 10) & (T < 20) & (P >= 250) & (P < 750)]  = 6  # woodland/shrubland
    out[valid & (T >= 10) & (T < 20) & (P >= 750) & (P < 1500)] = 5  # temperate seasonal forest
    out[valid & (T >= 10) & (T < 20) & (P >= 1500)]              = 4  # temperate rainforest

    # Warm/tropical zone (>20°C)
    out[valid & (T >= 20) & (P <= 1000)]              = 3  # subtropical desert
    out[valid & (T >= 20) & (P > 1000) & (P <= 2000)] = 2  # tropical seasonal/savanna
    out[valid & (T >= 20) & (P > 2000)]               = 1  # tropical rainforest

    return out


def main():
    print("Loading CHELSA bio01 (temperature)…")
    with rasterio.open(BIO01) as src:
        raw_temp = src.read(1).astype(np.float32)
        profile  = src.profile.copy()

    print("Loading CHELSA bio12 (precipitation)…")
    with rasterio.open(BIO12) as src:
        raw_prec = src.read(1).astype(np.float32)

    # Convert: bio01 stored as K×10 → °C
    nodata_mask = (raw_temp == NODATA_RAW) | (raw_prec == NODATA_RAW)
    temp_c  = np.where(nodata_mask, 0.0, raw_temp / 10.0 - 273.15)
    precip  = np.where(nodata_mask, 0.0, raw_prec.astype(np.float32))

    print(f"  Temp  range (valid): {temp_c[~nodata_mask].min():.1f}°C – {temp_c[~nodata_mask].max():.1f}°C")
    print(f"  Precip range (valid): {precip[~nodata_mask].min():.0f} – {precip[~nodata_mask].max():.0f} mm/yr")

    print("Classifying Whittaker biomes…")
    biome = classify_whittaker(temp_c, precip, nodata_mask)

    counts = {i: int((biome == i).sum()) for i in range(1, 10)}
    total  = sum(counts.values())
    print("  Biome pixel counts:")
    for k, v in counts.items():
        print(f"    {k}: {WHITTAKER_BIOMES[k]:<45} {v:>10,} px  ({100*v/total:.1f}%)")

    # Apply land mask from RESOLVE raster (ocean = 0) to remove ocean pixels.
    # RESOLVE is 43200×21600 vs CHELSA 43200×20880 — resample to match.
    print("Applying RESOLVE land mask…")
    RESOLVE_TIF = os.path.join(SRC_DIR, "resolve_biomes_2017.tif")
    if os.path.exists(RESOLVE_TIF):
        import rasterio.warp as _warp
        from rasterio.enums import Resampling as Res
        with rasterio.open(RESOLVE_TIF) as rsrc:
            land_mask = np.zeros(biome.shape, dtype=np.uint8)
            _warp.reproject(
                source        = rasterio.band(rsrc, 1),
                destination   = land_mask,
                src_crs       = rsrc.crs,
                dst_crs       = CRS.from_epsg(4326),
                dst_transform = profile["transform"],
                dst_nodata    = 0,
                resampling    = Res.nearest,
            )
        ocean = land_mask == 0
        biome[ocean] = 0
        land_px = int((biome > 0).sum())
        print(f"  Land pixels after masking: {land_px:,}")

    profile.update(count=1, dtype="uint8", nodata=0, compress="deflate")
    with rasterio.open(OUT_TIF, "w", **profile) as dst:
        dst.write(biome, 1)

    print(f"\nWritten: {OUT_TIF} ({os.path.getsize(OUT_TIF):,} bytes)")


if __name__ == "__main__":
    main()
