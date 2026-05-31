# Phase 21: Climate KML Work - Context

**Gathered:** 2026-05-31
**Status:** Ready for planning

## Phase Boundary

Produce an enhanced 2050 climate KML containing: (1) a high-detail global 2050 Köppen climate classification layer, (2) a global ecological biomes layer, (3) sea level rise inundation polygons for key coastal regions, and (4) refined versions of the existing 11 thematic placemarks with geographically accurate multi-polygon geometries replacing the current rough bounding boxes. All content lives in `2050-snapshot/kml/climate.kml` as separate internal folders.

## Implementation Decisions

### Phase Scope & Deliverables
- **D-01:** Primary new feature: 2050 Köppen climate classification map as a new KML layer — climate zones derived from projected temperature/precipitation rasters (all sub-types: Af, Am, Aw, BWh, BWk, BSh, BSk, Csa, Csb, Cwa, Cwb, Cwc, Cfa, Cfb, Cfc, Dsa, Dsb, Dsc, Dwa, Dwb, Dwc, Dfa, Dfb, Dfc, Dfd, ET, EF).
- **D-02:** Köppen data source: Researcher finds existing 2050 climate projection datasets (CMIP6-based, WorldClim, CHELSA) and derives Köppen zones from projected temperature/precipitation rasters. Research-driven, not manually drawn.
- **D-03:** Köppen detail level: High detail global, all sub-types included. Full-resolution zones preferred — file size is acceptable.
- **D-04:** Existing 11 thematic placemarks refined alongside the new layers (not deferred to future phase).
- **D-05:** Placemark refinement source priority: Data-driven where possible (elevation, satellite, climate model outputs), narrative-driven from climate.md where spatial data is unavailable. Researcher decides per-zone.

### Polygon Refinement Strategy
- **D-06:** Geometry sources: Both GADM admin boundaries and elevation/coastline data — researcher picks the best source per zone type.
- **D-07:** Multi-polygon per placemark: Each thematic placemark becomes a collection of actual geographic zones (e.g., Fire Regime Shift has separate polygons for Western US, Siberia, Australia, Mediterranean basin). No more single global bounding boxes.
- **D-08:** Water conflict basins: Actual river basin watershed geometries for each named basin (Indus, Nile, Mekong, Colorado, Amu Darya/Syr Darya, Tigris-Euphrates, Dnieper, Yellow River, Amur/Heilongjiang). Replace the current global bounding box.
- **D-09:** Ice placemarks (Arctic Permafrost Degradation Zone, Greenland Ice Sheet Retreat Zone, Glacier Mass Loss Extent): Replace with accurate satellite/climate-model-derived geometries. Upgrade-in-place, not new layers.

### New Climate KML Features
- **D-10:** Ecological biomes layer: Vegetation/ecoregion map showing tundra, boreal forest/taiga, temperate forest, grassland/savanna, desert, tropical rainforest. Distinct from Köppen climate classification — Köppen is climate zones (temp/precip thresholds), biomes are actual vegetation/ecological communities.
- **D-11:** Sea level rise inundation polygons: Geographic inundation extents for key coastal zones — Bangladesh delta, Mekong Delta, Nile Delta, US Gulf Coast, Pacific atoll states (Tuvalu, Kiribati, Marshall Islands, Maldives), Netherlands. Based on 0.35m+ rise by 2050 as described in climate.md.
- **D-12:** All new content (Köppen, biomes, SLR inundation, refined placemarks) lives in `2050-snapshot/kml/climate.kml` — organized as separate internal folders. No new KML files.

### Cross-reference & Integration
- **D-13:** Bidirectional cross-references: Each new/refined KML placemark gets `See: 2050-snapshot/domains/climate.md#section` in its description. Climate.md gets new `→ See KML:` markers for new layers where the narrative connects.
- **D-14:** Cross-reference verification scope: Climate.kml only. Entity-level `→ See KML:` markers in climate.md that point to borders.kml entities (~150 refs) are OUT OF SCOPE for this phase.
- **D-15:** All content stays inside `2050-snapshot/kml/climate.kml` — no new KML files created. Internal folder structure separates Köppen, Biomes, SLR Inundation, and refined thematic placemarks.

### Agent's Discretion
- Researcher decides which specific datasets (CMIP6 model, WorldClim version, CHELSA release) to use for Köppen derivation
- Researcher decides exact geometry source per-zone (GADM level, elevation dataset, coastline resolution)
- Planner determines wave structure and task ordering within the phase
- Styling (KML colors, opacities, line widths) at agent's discretion unless author objects

## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Climate Domain Content
- `2050-snapshot/domains/climate.md` — Primary source of truth. All climate narrative, entity profiles, thematic analysis, and 170 `→ See KML:` cross-references. 1,225 lines covering global climate state, cryosphere, sea level rise, extreme events, and regional impacts for all 200+ entities.
- `2026-2050-transition/climate.md` — Transition-period climate trajectory that informs the 2050 steady state.

### KML Infrastructure
- `2050-snapshot/kml/climate.kml` — Existing climate KML file (194 lines, 11 thematic placemarks with rough bounding boxes). Target file for all new content.
- `2050-snapshot/kml/entity-config.json` — Entity definitions, style references, climate-overlay style (`4055b0b0` fill). 3,061 lines. Defines how entities map to KML.
- `2050-snapshot/kml/user_colors.json` — Color assignments for entities and overlays. Needed for style consistency.
- `2050-snapshot/kml/borders.kml` — Entity polygon geometries (4,213 placemarks). Referenced by entity-level `→ See KML:` markers in climate.md (out of scope for verification but needed for context).

### Source Data (Phase 5 pipeline)
- `2050-snapshot/kml/source/global-countries-10m.kml` — GADM country boundary source data used by KML generation pipeline.
- `2050-snapshot/kml/source/global-countries.kml` — Higher-resolution GADM source for entity geometries.

### Cross-References
No related ADRs or external specs. Requirements are fully captured in project ROADMAP.md (Phase 21 entry: "Goal: [To be planned]" — now defined by this CONTEXT.md).

## Existing Code Insights

### Reusable Assets
- **Existing 11 thematic placemarks** in `climate.kml`: Source geometries to be replaced, but their structure (name, description format, cross-reference anchor format) provides the template for new layers.
- **entity-config.json climate-overlay style**: `lineColor: ff55b0b0, polyColor: 4055b0b0` — the established visual language for climate KML content.
- **KML generation pipeline** (Phase 5): Script-based programmatic generation precedent. New layers may reuse or extend pattern, or be manually constructed.

### Established Patterns
- **Multi-folder KML structure**: borders.kml and other overlay KMLs use nested folders organized by region. Climate.kml should follow similar internal organization.
- **Cross-reference format**: `See: path/to/file.md#anchor` in KML descriptions, `→ See KML: Feature Name` in markdown. Bidirectional and anchor-based.
- **Styling convention**: Overlay KMLs use distinct color palettes per domain. Climate uses teal (#55b0b0). New layers should maintain color harmony within the climate domain.

### Integration Points
- **climate.md §Global Climate State**: Where Köppen layer naturally connects — temperature/precipitation thresholds match climate zone descriptions
- **climate.md §Cryosphere**: Where refined ice placemarks reference back
- **climate.md §Sea Level Rise**: Where SLR inundation polygons anchor
- **climate.md §Regional Climate Impacts**: Entity-level sections where new `→ See KML:` markers for biomes may be inserted
- **2050 index.md**: May need updated reference to enhanced climate.kml

## Specific Ideas

- Köppen climate classification is a standard, well-defined system — use established color conventions (e.g., Af=tropical rainforest blue, BWh=hot desert red, Dfc=subarctic teal) for immediate legibility
- Biome layer should use visually distinct colors from Köppen to avoid confusion when both are visible
- SLR inundation polygons should use a semi-transparent blue fill to overlay on existing entity polygons — visually communicates "land being lost to sea"
- River basin watershed geometries for water conflict basins can likely be sourced from HydroSHEDS or similar global watershed datasets

## Deferred Ideas

None — discussion stayed within phase scope.

---

*Phase: 21-climate-kml-work*
*Context gathered: 2026-05-31*
