---
phase: 21-climate-kml-work
plan: 03
subsystem: kml-generation
tags: [biomes, slr, climate, kml, simplekml, fallback, narrative-derived]

# Dependency graph
requires:
  - phase: 21-02
    provides: generate-climate-layers.py with Köppen generation, climate.kml with Köppen folder
provides:
  - Ecological Biomes (2050) KML folder with 6 biome types
  - Sea Level Rise Inundation (0.35m) KML folder with 6 coastal region zones
  - generate_biomes_kml() and generate_slr_kml() functions in generate-climate-layers.py
affects: [21-04, 21-05]

# Tech tracking
tech-stack:
  added: [fiona for shapefile reading, shapely.unary_union for polygon dissolve]
  patterns: [data-driven with graceful fallback, narrative-derived approximate polygons, deep-copy lxml merge]

key-files:
  modified:
    - 2050-snapshot/kml/generate-climate-layers.py
    - 2050-snapshot/kml/climate.kml

key-decisions:
  - "Biomes uses earthy color scheme (grays, greens, tans, yellows) visually distinct from Köppen primary/secondary palette"
  - "Fallback biome polygons use approximate geographic bounding boxes derived from known biome distribution descriptions in climate.md"
  - "SLR polygons use semi-transparent teal (6055b0b0) matching entity-config.json climate-overlay convention"
  - "Pacific atolls rendered as individual small polygons (~2km²) per atoll rather than single polygon covering all"

patterns-established:
  - "Layer insertion pattern: generate temp KML → deep-copy merge via lxml between existing folders"
  - "Fallback documentation pattern: all approximate polygons include 'APPROXIMATE' marker in description"
  - "Region-atoll hybrid pattern: polygon-based for continental regions, point-buffer for atoll nations"

requirements-completed: [CLMKML-02]

# Metrics
duration: 4min
completed: 2026-06-01
---

# Phase 21 Plan 03: Ecological Biomes & Sea Level Rise KML Layers Summary

**Two new KML folders added to climate.kml — Ecological Biomes (2050) with 6 biome types (tundra, boreal forest, temperate forest, grassland/savanna, desert, tropical rainforest) and Sea Level Rise Inundation (0.35m) with 9 placemarks across 6 coastal regions (Bangladesh, Mekong, Nile, US Gulf, Pacific Atolls, Netherlands) — both with See: cross-references to climate.md**

## Performance

- **Duration:** 4 min
- **Started:** 2026-06-01T11:48:00Z
- **Completed:** 2026-06-01T11:52:30Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Added `generate_biomes_kml()` to `generate-climate-layers.py` — data-driven (WWF ecoregions via fiona) with narrative-derived fallback creating approximate geographic polygons for 6 biome types
- Added `generate_slr_kml()` to `generate-climate-layers.py` — data-driven (DEM tiles via rasterio) with narrative-derived fallback creating approximate coastal inundation zones for 6 regions
- Merged both layers as styled folders into `climate.kml` — inserted between the Köppen folder (Plan 02) and the original Climate folder with 11 thematic placemarks
- Biomes layer: 23 placemarks across 6 biome types with earthy color scheme (gray, dark/medium green, tan, yellow-green) visually distinct from Köppen palette
- SLR layer: 9 placemarks (5 coastal bounding-box polygons + 4 atoll-specific polygons) with semi-transparent teal fill (6055b0b0) matching entity-config.json climate-overlay convention
- All 32 placemarks include `See:` cross-reference to climate.md (`#global-climate-state` for biomes, `#sea-level` for SLR)
- CLI now supports `--biomes` and `--slr` flags alongside default Köppen generation
- Original Climate folder with all 11 thematic placemarks preserved untouched

## Task Commits

Each task was committed atomically:

1. **Task 1: Add biomes and SLR generation functions** — `5fe8b79` (feat)
2. **Task 2: Generate and merge biomes + SLR layers into climate.kml** — `3464ee6` (feat)

## Files Modified

- `2050-snapshot/kml/generate-climate-layers.py` — Added ~625 lines: biome/SLR constants, `generate_biomes_kml()` with WWF data-driven + fallback paths, `generate_slr_kml()` with DEM data-driven + fallback paths, CLI `--biomes`/`--slr` flags
- `2050-snapshot/kml/climate.kml` — Inserted 856 lines: Ecological Biomes (2050) folder with 6 sub-folders + Sea Level Rise Inundation (0.35m) folder with 9 placemarks

## Decisions Made

- **Biome colors distinct from Köppen:** Köppen uses primary/secondary colors (blue, red, yellow, cyan, purple, white). Biomes uses earthy tones (gray #A0A0A0, dark green #3A7D3A, medium green #5CA65C, yellow-green #E8D44D, tan #EDC58E, very dark green #1A5C1A). No visual confusion when both layers are visible.
- **Pacific atolls as individual polygons:** Rather than a single bounding box covering all atolls, each atoll gets its own small polygon (~2km² at ~0.02° buffer) so they render as distinct zones in Google Earth.
- **SLR teal style matches existing convention:** Used `6055b0b0` poly fill / `ff55b0b0` line from entity-config.json climate-overlay convention, ensuring visual consistency with the existing climate layer.
- **Biomes alpha 60 vs Köppen alpha 80:** Slightly more transparent biomes fill prevents visual overload when both Köppen and biomes layers are visible simultaneously.

## Deviations from Plan

None — plan executed exactly as written. Source datasets (WWF ecoregions, DEM tiles) were unavailable as expected, and fallback paths were used as designed per D-05 discretion.

## Known Stubs

All "APPROXIMATE" placemarks are intentional — they are the documented fallback behavior per the plan's threat model (T-21-09: Narrative-derived fallback polygons accepted). When WWF ecoregions shapefile or DEM elevation tiles become available, re-running the script with source data in place will replace approximate polygons with data-driven geometries.

## Threat Mitigation Verification

| Threat ID | Category | Disposition | Verification |
|-----------|----------|-------------|-------------|
| T-21-07 | Information Disclosure | mitigate | Reclassification table documented in BIOME_RECLASSIFICATION dict; standard WWF biome names used as keys |
| T-21-08 | Information Disclosure | accept | +0.35m uniform threshold noted as "global mean; local effects vary" in all SLR placemark descriptions |
| T-21-09 | Denial of Service | accept | All fallback polygons marked "APPROXIMATE" in descriptions per D-05 discretion |

## Issues Encountered

None — both generators produced correct output on first run. Fallback paths triggered as expected due to missing source data.

## User Setup Required

None — no external service configuration required. If WWF ecoregions data becomes available, place it at `source/wwf_ecoregions/wwf_terrestrial_ecoregions.shp` and re-run `generate-climate-layers.py --biomes`. If DEM tiles become available, place them in `source/dem_tiles/` and re-run `generate-climate-layers.py --slr`.

## Next Phase Readiness

- Biomes and SLR layers complete in climate.kml — ready for Plan 04 (Thematic Placemark Refinement)
- generate-climate-layers.py extended with 2 new generation functions following the existing pattern
- Both new layers include `See:` cross-references to climate.md as required by D-13
- Folder order established: Köppen (Plan 02) → Biomes (Plan 03) → SLR (Plan 03) → Climate (original)

---

## Self-Check: PASSED

| Check | Result |
|-------|--------|
| generate-climate-layers.py exists | FOUND |
| climate.kml exists | FOUND |
| SUMMARY.md exists | FOUND |
| Task 1 commit (5fe8b79) | FOUND |
| Task 2 commit (3464ee6) | FOUND |
| generate_biomes_kml() callable | ✓ |
| generate_slr_kml() callable | ✓ |
| Köppen folder in climate.kml | PRESENT |
| Biomes folder in climate.kml | PRESENT |
| SLR folder in climate.kml | PRESENT |
| Climate folder in climate.kml | PRESENT |

---

*Phase: 21-climate-kml-work*
*Completed: 2026-06-01*
