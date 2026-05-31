# Phase 21: Climate KML Work - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-31
**Phase:** 21-climate-kml-work
**Areas discussed:** Phase scope & deliverables, Polygon refinement strategy, New climate KML features, Cross-reference & integration

---

## Phase Scope & Deliverables

| Option | Description | Selected |
|--------|-------------|----------|
| Full climate KML enhancement pass | Refine existing 11 thematic polygons + add missing layers + verify all 170 cross-references | |
| Targeted fixes only | Fix only broken cross-references and display issues | |
| New climate layers first | Focus on adding new climate KML layers that don't exist yet | ✓ |

**User's choice:** New climate layers first
**Notes:** Priorities new content creation over fixing existing content.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Entity polygon climate overlays | Use borders.kml entity geometries with climate styling | |
| Geographic climate zone polygons | New polygons for specific climate zones | |
| Climate migration & impact corridors | Lines/arrows for migration routes and water basins | |
| All of the above | Full treatment | |

**User's choice:** 2050 Köppen climate map (free-text)
**Notes:** User specified a standard Köppen climate classification map for 2050 as the primary new layer.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Research available projections | Planner/researcher finds CMIP6/WorldClim/CHELSA datasets | ✓ |
| Manual/author-driven | User defines zone boundaries themselves | |
| Approximate from narrative | Derive boundaries from climate.md descriptions | |

**User's choice:** Research available projections
**Notes:** Data-driven approach — researcher sources actual climate model outputs.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Medium detail per region | Smoothed polygons at continent scale | |
| High detail global | Full-resolution zones with all Köppen sub-types | ✓ |
| Pragmatic/let agent decide | Researcher figures out best detail level | |

**User's choice:** High detail global
**Notes:** All Köppen sub-types (Af through EF). File size acceptable despite full resolution.

---

| Option | Description | Selected |
|--------|-------------|----------|
| New separate layer in climate.kml | Köppen as new folder alongside existing placemarks | ✓ |
| Replace the thematic placemarks | Köppen replaces rough bounding boxes | |
| Both — thematic as sub-features | Nest placemarks under Köppen | |

**User's choice:** New separate layer in climate.kml
**Notes:** Existing 11 placemarks stay as-is for now (refined separately). Köppen is additional content.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, refine them alongside | Improve existing placemarks while adding Köppen | ✓ |
| No, Köppen-only this phase | Scope limited to Köppen layer only | |
| Refine only some | Pick most important existing placemarks to refine | |

**User's choice:** Yes, refine them alongside
**Notes:** Existing placemarks get refined in the same phase, not deferred.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Data-driven where possible, narrative where not | Elevation/satellite data for physical zones, markdown for political | ✓ |
| Narrative-driven for all | Author defines all boundaries | |
| Mixed — researcher decides | Researcher picks best approach per zone | |

**User's choice:** Data-driven where possible, narrative where not
**Notes:** Sea level, ice, and elevation-based zones use data. Sahel, fire regime, etc. use narrative + approximate boundaries.

---

## Polygon Refinement Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| GADM admin boundaries | Use country/state borders as base geometry | |
| Elevation/coastline data | SRTM/CGIAR for physical geography features | |
| Both — researcher picks per zone | GADM for political, elevation for physical | ✓ |

**User's choice:** Both — researcher picks per zone
**Notes:** Flexibility to use the right data source for each zone type.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Multi-polygon per placemark | Each thematic zone has separate geographic polygons | ✓ |
| Single polygon per placemark | One refined polygon per theme | |
| Mixed — researcher decides | Multi where it makes geographic sense | |

**User's choice:** Multi-polygon per placemark
**Notes:** Fire regimes get separate polygons for Western US, Siberia, Australia, etc. — not one global box.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — actual river basin geometries | Each basin gets own watershed polygon | ✓ |
| Yes — simplified basin outlines | Approximate boundaries | |
| No — keep as abstract zone | Geopolitical concept, not geographic | |

**User's choice:** Yes — actual river basin geometries
**Notes:** Indus, Nile, Mekong, Colorado, Amu Darya/Syr Darya, Tigris-Euphrates, etc. as real watershed polygons.

---

## New Climate KML Features

| Option | Description | Selected |
|--------|-------------|----------|
| Amazon dieback boundary | Current vs savannized extent | |
| Sea ice extent — summer vs winter | Arctic seasonal sea ice polygons | |
| Climate migration corridors | Lines/arrows for population movements | |
| Add none beyond Köppen + refined existing | No additional layers | |

**User's choice:** Ice coverages and ice melt, biomes, sea level rise (free-text)
**Notes:** User specified three additional new layer types beyond Köppen.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Replace existing ice placemarks with accurate data | Upgrade the 3 existing land-ice placemarks | ✓ |
| Add seasonal sea ice extent layers | New Arctic summer/winter sea ice polygons | |
| Both | Upgrade existing + add seasonal | |

**User's choice:** Replace existing ice placemarks with accurate data
**Notes:** Arctic Permafrost, Greenland Ice Sheet, Glacier Mass Loss get real geometries — not new layers.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Köppen IS the biome layer | Climate classification covers biome needs | |
| Vegetation/ecoregion biomes | Actual vegetation communities, distinct from climate | ✓ |
| 2050 biome shift map | Current vs projected biome boundaries | |

**User's choice:** Köppen is the climate map, biome is ecological regions
**Notes:** Two distinct layers. Köppen = temp/precip thresholds. Biomes = actual vegetation/ecoregions (tundra, taiga, temperate forest, grassland, desert, tropical rainforest).

---

| Option | Description | Selected |
|--------|-------------|----------|
| Inundation polygons for specific regions | Geographic extents for key coastal zones | ✓ |
| Coastal risk zone styling on entity polygons | Style existing entities by SLR risk | |
| Both | Inundation + entity styling | |

**User's choice:** Inundation polygons for specific regions
**Notes:** Bangladesh delta, Mekong Delta, Nile Delta, US Gulf Coast, Pacific atolls, Netherlands. 0.35m+ rise extents.

---

## Cross-reference & Integration

| Option | Description | Selected |
|--------|-------------|----------|
| Bidirectional: add KML→md and md→KML | Both directions updated for new layers | ✓ |
| KML→md only | Only KML references back to markdown | |
| Verify existing only, no new markers | Just check existing 170 markers | |

**User's choice:** Bidirectional: add KML→md and md→KML
**Notes:** New placemarks get `See:` back to climate.md. Climate.md gets new `→ See KML:` markers for new layers.

---

| Option | Description | Selected |
|--------|-------------|----------|
| Climate.kml only | Only verify climate.kml cross-references | ✓ |
| All climate-related refs | Verify all 170 including entity-level to borders.kml | |
| Spot-check + fix broken ones | Automated matching, fix only mismatches | |

**User's choice:** Climate.kml only
**Notes:** Entity-level `→ See KML:` markers referencing borders.kml (~150 refs) are OUT OF SCOPE.

---

| Option | Description | Selected |
|--------|-------------|----------|
| All in climate.kml | One file, internal folder separation | ✓ |
| Separate KML files per layer | koppen.kml, biomes.kml, etc. | |
| Köppen in own file, rest in climate.kml | Only Köppen gets a separate file | |

**User's choice:** All in climate.kml
**Notes:** No new KML files. Internal folder structure separates Köppen, Biomes, SLR Inundation, and refined placemarks.

---

## Agent's Discretion

- Researcher decides which specific datasets (CMIP6 model, WorldClim version, CHELSA release) to use for Köppen derivation
- Researcher decides exact geometry source per-zone (GADM level, elevation dataset, coastline resolution)
- Planner determines wave structure and task ordering
- Styling (KML colors, opacities, line widths) at agent's discretion

## Deferred Ideas

None — discussion stayed within phase scope.
