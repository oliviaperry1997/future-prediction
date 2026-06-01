# Phase 21: Climate KML Work — Research & Data Discovery

**Date:** 2026-06-01
**Researcher:** Planner agent
**Confidence:** HIGH

## Research Questions

Phase 21 requires four new/enhanced KML layers in `2050-snapshot/kml/climate.kml`:
1. Köppen-Geiger climate classification layer (global, 2050 projection)
2. Ecological biomes layer (global, 2050)
3. Sea level rise inundation polygons (key coastal regions)
4. Refined existing 11 thematic placemarks (multi-polygon geometries)

Each layer requires identifying appropriate open geospatial datasets.

## 1. Köppen-Geiger Climate Classification (2050 Projection)

### Best Available Dataset: GloH2O / Beck et al. V3 (2023)

**Source:** www.gloh2o.org/koppen
**Paper:** Beck et al. (2023), "High-resolution (1 km) Köppen-Geiger maps for 1901-2099 based on constrained CMIP6 projections", *Scientific Data* 10, 724.

**Key specifications:**
- **Resolution:** 1 km (0.0083°) — the highest available resolution
- **Temporal coverage:** Historical (1901-1930, 1931-1960, 1961-1990, 1991-2020) and Future (2041-2070, 2071-2099)
- **Future scenarios:** 7 SSPs (SSP1-1.9 through SSP5-8.5), based on 42 CMIP6 models screened for realistic TCR/ECS
- **All 30 Köppen sub-types** (Af through EF) included
- **Data format:** GeoTIFF raster + confidence maps + monthly temp/precip netCDF
- **Download:** figshare DOI archive — single ~300MB download for all periods/scenarios
- **License:** CC BY 4.0

**Selection recommendation:** Use the **2041-2070** period under **SSP3-7.0** (most consistent with the project's +2.1°C warming narrative). Also provide SSP2-4.5 as an alt-scenario layer.

**2025-2026 update:** V3 now uses CMIP6 models with TCR/ECS screening (42 of 67 models passed). Previous V1 (Beck et al. 2018, RCP8.5, 2071-2100) is available but outdated.

### Alternative Datasets

| Dataset | Resolution | Future Period | Pros | Cons |
|---------|-----------|---------------|------|------|
| WorldClim CMIP6 | 30s (~1km) | 2041-2060 avg | Well-known, 23 GCMs, 4 SSPs | 2.5-10min resolution default; 30s needs account |
| FAO GAEZ v5 | ~10km | 2041-2060 | CMIP6-based, 3 SSPs, 14 2-char classes | Only 2-character classes (not full sub-types) |
| CHC-CMIP6 | 0.05° (~5km) | 2045-2055 | Closest to exact 2050 target | Daily temp/precip only (need to compute Köppen manually) |
| CHELSA V2.1 | ~1km | 2071-2100 only | High quality downscaling | No 2050 window — only far future and historical |

**Decision:** GloH2O V3 (2041-2070 SSP3-7.0) is the best match. It provides pre-computed Köppen zones at 1km, eliminating the need to compute from raw climate rasters.

### Technical Approach for KML Conversion

1. Download the 2041-2070 SSP3-7.0 GeoTIFF from figshare
2. Use GDAL `gdal_polygonize.py` to convert raster zones to vector polygons
3. Simplify polygons with Douglas-Peucker (0.02° threshold, ~2.2km, matching existing project convention)
4. Use simplekml to write styled KML with all 30 sub-types, organized in a folder hierarchy (major climate groups A/B/C/D/E → sub-type placemarks)
5. Assign standard Köppen color scheme for immediate legibility

**Standard Köppen colors (established convention):**
- Af (Tropical Rainforest): #0000FF (blue)
- Am (Tropical Monsoon): #0078FF
- Aw (Tropical Savannah): #46AAFA
- BWh (Hot Desert): #FE0000 (red)
- BWk (Cold Desert): #FE9695
- BSh (Hot Semi-arid): #F5A505
- BSk (Cold Semi-arid): #FFDC7C
- Csa (Hot-summer Mediterranean): #FFCC00
- Csb (Warm-summer Mediterranean): #C9C800
- Cwa (Monsoon-influenced humid subtropical): #C6C76A
- Cwb (Subtropical highland): #6C9A5E
- Cwc (Cold subtropical highland): #7EAA7D
- Cfa (Humid subtropical): #96FF96
- Cfb (Oceanic): #6DB46D
- Cfc (Subpolar oceanic): #40A040
- Dsa (Mediterranean-influenced hot continental): #5EBDC9
- Dsb (Mediterranean-influenced warm continental): #4DA6B8
- Dsc (Mediterranean-influenced subarctic): #2F8FA5
- Dwa (Monsoon-influenced hot continental): #5DF0F0
- Dwb (Monsoon-influenced warm continental): #41C8C8
- Dwc (Monsoon-influenced subarctic): #2CAAAA
- Dfa (Hot continental): #00FFFF
- Dfb (Warm continental): #46D2D2
- Dfc (Subarctic): #64C8E4
- Dfd (Extreme subarctic): #5EE0F0
- ET (Tundra): #964696 (purple)
- EF (Frost/Ice Cap): #FFFFFF (white)

## 2. Ecological Biomes Layer

### Best Available Dataset: WWF Terrestrial Ecoregions (TEOW)

**Source:** https://www.worldwildlife.org/publications/terrestrial-ecoregions-of-the-world
**Also available:** Google Earth Engine (`WWF/WWF_TerrestrialEcoregions`)

**Key specifications:**
- **14 major biome types** (includes 6 we need: tundra, boreal forest/taiga, temperate forest, grassland/savanna, desert, tropical rainforest)
- **Rester:** Polygons/shapefile, global coverage
- **867 ecoregions** nested within biomes

**Reclassification plan:** Map TEOW biomes to our 6 target classes:
- Tundra → Tundra
- Boreal Forests/Taiga → Boreal Forest/Taiga
- Temperate Coniferous/Mixed/Broadleaf Forests → Temperate Forest
- Tropical/Subtropical Moist/Dry/Coniferous Forests → Tropical Rainforest
- Temperate Grasslands/Savannas/Shrublands + Flooded Grasslands → Grassland/Savanna
- Deserts and Xeric Shrublands → Desert

**Technical approach:**
1. Download WWF Terrestrial Ecoregions shapefile
2. Dissolve polygons by reclassified biome type
3. Simplify geometries (Douglas-Peucker 0.02°)
4. Write to KML with simplekml, using a distinct color scheme from Köppen

**Suggested biome colors** (distinct from Köppen palette):
- Tundra: #A0A0A0 (gray)
- Boreal Forest/Taiga: #3A7D3A (dark green)
- Temperate Forest: #5CA65C (medium green)
- Grassland/Savanna: #E8D44D (yellow-green)
- Desert: #EDC58E (tan)
- Tropical Rainforest: #1A5C1A (very dark green)

## 3. Sea Level Rise Inundation Polygons

**Approach:** Based on the climate.md +0.35m rise baseline (D-11), we need inundation polygons for key deltas and coastal zones.

**Available elevation datasets:**
- **SRTM 30m** (global, 60°N-56°S) — best for most regions
- **COP30 / Copernicus DEM 30m** (global, better coverage, less void issues)
- **NASADEM** (improved SRTM)

**Key regions per D-11:** Bangladesh delta, Mekong Delta, Nile Delta, US Gulf Coast, Pacific atolls (Tuvalu, Kiribati, Marshall Is., Maldives), Netherlands

**Technical approach:**
1. For each region, download SRTM/COP30 DEM tile
2. Select cells at elevation ≤ 0.35m (or ≤ 0.5m with buffer)
3. Mask to coastal zone boundary
4. Polygonize and simplify
5. Write to KML as semi-transparent blue (#4055B0B0 fill, matching climate overlay convention)

**Alternative:** Use pre-computed SLR inundation datasets from NASA/IPCC coastal impact studies if available (lower priority — manual SRTM approach is reliable for 0.35m threshold).

## 4. Thematic Placemark Refinement Data Sources

Per D-07 (multi-polygon) and D-08 (actual river basin watersheds):

| Placemark | Data Source | Geometry Type |
|-----------|-------------|---------------|
| Arctic Permafrost Degradation Zone | NSIDC permafrost extent map (circumpolar) | Permafrost zone polygons |
| Greenland Ice Sheet Retreat Zone | PROMICE ice sheet margin data | Retreat margin polygons |
| Glacier Mass Loss Extent | RGI (Randolph Glacier Inventory) + GLIMS | Glacier polygons, grouped by region |
| Sea Level Impact Zones | SRTM coastal elevation + climate.md narrative | Semi-transparent coastal polygon |
| Extreme Heat Zones | Climate.md narrative (Indus, Persian Gulf, Sahel, US SW) | Approximate geographic bounding polygons |
| Fire Regime Shift | Climate.md + GFED fire regime zones | Multi-polygon: W US, Siberia, Australia, Mediterranean, Amazon |
| Sahel Degradation Zone | Climate.md belt + GADM admin boundaries | Sahelian country polygons (Mali, Niger, Chad, Sudan, Burkina Faso) |
| Extreme Heat — Persian Gulf | Climate.md + geographic bounding | Persian Gulf coastal zone |
| Transboundary Water Conflict Basins | **HydroSHEDS HydroBASINS** — specific PFafstetter codes for each basin | Watershed polygons |
| Arctic Resource Zones | Arctic Council CAFF boundary | Arctic circle + EEZ polygons |
| Desalination and Adaptation Infrastructure | Climate.md narrative → Point locations | Point placemarks with descriptions |

**HydroSHEDS watershed data** (for D-08):
- **Source:** hydrosheds.org → HydroBASINS product
- **Available resolutions:** 15s (~500m) for basin delineation
- **PFafstetter levels:** Level 4-5 for major basins (Indus, Nile, Mekong, etc.)
- **Format:** Shapefile with hierarchical basin ID coding
- **Alternative:** Google Earth Engine `WWF/HydroSHEDS/v1/Basins/hybas_9`

## 5. Tooling & Pipeline

**Required Python packages:**
- `simplekml` (already in stack) — KML generation
- `rasterio` or `osgeo.gdal` — GeoTIFF reading and polygonization
- `fiona` or `shapefile` (pyshp) — Shapefile reading
- `shapely` (already in stack) — Geometry operations, simplification
- `pyproj` — Coordinate reference system handling

**Environment setup:**
```bash
pip install rasterio fiona shapely pyproj simplekml
# GDAL should already be available or installable via:
# brew install gdal  # macOS
```

**Pipeline pattern for each layer (follows D-19 programmatic generation precedent):**
```
Data Source (GeoTIFF/Shapefile)
  → Polygonize/extract features (GDAL/Fiona)
  → Simplify + clean geometries (Shapely)
  → Style + write KML (simplekml)
  → Add cross-references (Python string formatting)
```

## Decision Summary

| Delivery | Data Source | Confidence |
|----------|-------------|------------|
| Köppen layer | GloH2O V3 2041-2070 SSP3-7.0 (beck et al. 2023) | HIGH — pre-computed, 1km, authoritative |
| Biomes layer | WWF Terrestrial Ecoregions (TEOW) | HIGH — well-established global biome dataset |
| SLR inundation | SRTM/COP30 DEM + climate.md 0.35m threshold | MEDIUM — elevation accuracy varies in delta regions |
| Water conflict basins | HydroSHEDS HydroBASINS (v1c) | HIGH — standard watershed dataset |
| Ice/permafrost zones | NSIDC + PROMICE + RGI | HIGH — authoritative cryosphere data |
| Fire/heat/sahel | Narrative-derived from climate.md | MEDIUM — approximate geographic boundaries |
| Adaptation points | Narrative-derived from climate.md | MEDIUM — point locations from text analysis |

**Key risk:** Large GeoTIFF downloads (Köppen ~300MB) and complex GDAL polygonization may require manual refinement in Google Earth Pro. Phase 5 precedent (D-19) anticipates this — programmatic generation with user refinement.

---

*Research completed: 2026-06-01*
*Ready for planning: yes*
