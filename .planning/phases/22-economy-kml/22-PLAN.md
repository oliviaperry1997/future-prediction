---
phase: 22-economy-kml
type: execute
wave: overall
depends_on:
  - "20-africa-and-america-re-review"
  - "21-climate-kml-work"
requirements:
  - ECONKML-01
  - ECONKML-02
  - ECONKML-03
  - ECONKML-04
---

# Phase 22: Economy KML — Four Data-Driven Layers

<objective>
Replace the existing economy.kml (8 rough-bounding-box placemarks) with 4 data-driven overlay layers: Cities & Megalopolises, Production Metric (BCU-equivalent), Transit & Logistics Systems, and Production Sector classifications. Each layer has accurate geometries, entity-level data from economy.md, and bidirectional cross-references.
</objective>

## Layers

| # | Layer | Type | Data Source |
|---|-------|------|-------------|
| 1 | **Cities & Megalopolises** | Points + Polygons | NE populated places + UMS β=81 clustering on population density + narrative adjustments for 2050 |
| 2 | **Production Metric (BCU)** | Entity fills | Economy.md narrative estimates converted to BCU-equivalent tiers |
| 3 | **Transit & Logistics** | Lines + Points | Narrative-derived corridors (shipping, HSR, pipelines, HVDC, spaceports, port hubs) |
| 4 | **Production Sectors** | Entity fills | Economy.md dominant sector classification per entity |

## Wave Structure

### Wave 1: Research & Data Pipeline
- Research UMS megalopolis calculation method and acquire population data (GPW/GHSL)
- Research BCU conversion approach from narrative GDP estimates
- Research transit data (shipping routes, HSR networks, major ports, spaceports)
- Write DISCOVERY.md with all data sources, processing pipelines, confidence assessments
- Download/acquire all source datasets

### Wave 2: Layer Generation (parallel)
- **Plan 02**: Generate Cities & Megalopolises layer
- **Plan 03**: Generate Production Metric (BCU-equivalent) overlay
- **Plan 04**: Generate Transit & Logistics Systems layer
- **Plan 05**: Generate Production Sectors layer

### Wave 3: Cross-References & Verification
- Add → See KML markers to economy.md entity profiles
- Add → See economy.md back-references to economy.kml placemarks
- Verify all layers open correctly in Google Earth Pro
- Write 22-VERIFICATION.md

## Key Design Decisions

- **Megalopolises**: Computed via UMS β=81 (160 km attractive/repulsive equilibrium distance) on population distribution, following the Urban Metric System from Wikipedia. Use current GPW/GHSL population data as base, with narrative 2050 adjustments for major shifts.
- **Production Metric**: BCU-equivalent — convert narrative GDP estimates using an estimated dollar-to-BCU conversion reflecting the dollar's loss of reserve status. Layer shows economic output in BCU terms.
- **Transit Systems**: Include high-speed rail networks, major shipping routes, energy pipelines, HVDC transmission corridors, major ports, and spaceports. Narrative-derived from economy.md with NE physical infrastructure data as reference.
- **Cities**: Point placemarks scaled by population/economic significance. Sourced from NE populated places filtered to major urban centers (>500K) with 2050 adjustments.

## Constraints

- All 4 layers in a single economy.kml file (no separate KMLs per D-12 precedent from Phase 21)
- No borders.kml cross-references (per D-14 precedent)
- Bidirectional cross-references: KML → economy.md and economy.md → KML
- Automatic generation with user refinement for edge cases
- Entity-level data sourced from existing economy.md entity profiles

## Success Criteria

1. economy.kml has 4 folders with data-driven geometries replacing 8 rough bounding boxes
2. Cities & Megalopolises layer has 20+ city point placemarks and 5+ megalopolis polygons
3. Production Metric layer has entity fills for all ~200 entities with BCU-equivalent tiers
4. Transit & Logistics layer has 10+ corridor lines and 10+ node placemarks (ports, HSR, spaceports)
5. Production Sectors layer shows dominant sector classification per entity
6. Bidirectional cross-references exist between economy.kml and economy.md
7. Total vertex count under Google Earth 250K limit
