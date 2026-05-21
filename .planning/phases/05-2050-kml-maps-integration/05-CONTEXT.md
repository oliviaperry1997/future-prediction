# Phase 5: 2050 KML Maps & Integration - Context

**Gathered:** 2026-05-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Produce KML map files for the 2050 world map from domain doc content, cross-referenced bidirectionally between markdown sections and KML polygon placemarks, and finalize 2050-snapshot/index.md as navigable entry point linking to all six domain documents and KML map descriptions. KML files open in Google Earth Pro.

**Requirements locked:** BORD-03 (KML polygons for 2050 world map), KMLP-01 (KML files with geopolitical boundaries), KMLP-02 (KML entries cross-referenced to markdown sections). Existing user basemap at `2050-snapshot/kml/Earth Current.kml`.

**Success criteria:**
1. KML map files exist (at minimum borders/geopolitics layer) with 2050 geopolitical boundaries as polygons
2. KML files open correctly in Google Earth Pro
3. Each KML polygon includes See: reference back to the markdown section justifying that boundary
4. All markdown border descriptions consistent with KML polygons
5. 2050-snapshot/index.md links to all six domain docs and KML descriptions

</domain>

<spec_lock>
## Locked Requirements

### BORD-03
Create KML polygons for 2050 world map.

### KMLP-01
Produce KML map files for the 2050 world map with geopolitical boundaries.

### KMLP-02
Ensure KML entries cross-reference the markdown sections that justify each boundary.

### Prior Context Decisions Carried Forward
- **D-15 (Phase 4):** Entity-level KML markers — KMLs primarily for borders. Economic/demographic zone layers deferred.
- **D-27/28/29 (Phase 3):** Every terrestrial region claimed by exactly one entity. No overlaps. Antarctica deliberately resolved.
- **D-36 (Phase 3):** → See KML: markers in domain docs provide forward references for KML integration.
- **V2 KML tooling deferred** (from REQUIREMENTS.md): confidence-encoded opacity, NetworkLink architecture, shared style library — not in scope for Phase 5.

</spec_lock>

<decisions>
## Implementation Decisions

### KML File Structure & Layer Organization

- **D-01 (Domain-mirrored file structure):** One KML file per STEEP domain — `borders.kml`, `climate.kml`, `technology.kml`, `economy.kml`, `demographics.kml`, `culture.kml` — all in `2050-snapshot/kml/`. Matches the domain doc organization established in Phases 3-4.
- **D-02 (Geographic hierarchy within files):** Inside each KML, placemarks organized by geographic hierarchy (Continent > Subregion > Entity), matching the existing "Earth Current" basemap's folder pattern. US successor states nested under North America > Former United States.
- **D-03 (Entity polygons only in borders.kml):** borders.kml contains ALL entity polygons (complete world coverage). Other domain KMLs only contain domain-specific overlay placemarks referenced by their → See KML: markers (AI regulation zones, energy systems, etc.).
- **D-04 (Rough polygon overlays for non-border domains):** Domain-specific placemarks are drawn as rough polygon overlays (not point markers) that approximate the zone referenced in the domain doc.
- **D-05 (KML format, not KMZ):** Raw KML files — editable in text editor, diff-able in git, native Google Earth Pro support. KMZ can be exported by user if needed for distribution.
- **D-06 (Separate 2050 files from basemap):** 2050 KMLs are separate files loaded alongside Earth Current.kml, not modifications of it.

### KML Scope: What Gets Mapped

- **D-07 (Entity border polygons):** Required minimum — all 19 US successor states + indigenous nations + global powers (China, EU Core, India, Brazil, EAF, ASEAN, Russia, Turkey, Unified Korea, Australia/NZ, Canada, etc.) represented as polygon placemarks in borders.kml.
- **D-08 (Domain overlay polygons):** Each domain's KML includes rough polygon overlays corresponding to its → See KML: markers beyond entity references (e.g., BRICS+ Financial Infrastructure in economy.kml, AI Regulation Zones in technology.kml).
- **D-09 (Fragmented entities as sub-polygons):** Fragmented entities (Atlantic South's city-state islands, Appalachian Zone's patchwork, Mountain Tapestry's fragments) drawn as multiple sub-entity polygons rather than one collective polygon. The entity's → See KML: marker in domain docs points to the collective folder.
- **D-10 (2050-specific global modifications):** Global entities get 2050-specific polygon modifications — Palestine as new entity, Israel contracted to coastal rump, Quartet security framework reflected, EU Core boundaries redrawn, Canada-Quebec asymmetric federalism shown, etc. Not copied from modern-day basemap.

### Cross-Reference Format & Bidirectional Linking

- **D-11 (Full relative paths in See: fields):** KML→markdown cross-references use full relative file paths with section anchors in the placemark Description field (e.g., `See: 2050-snapshot/domains/borders-geopolitics.md#pacific-peoples-republic`).
- **D-12 (Inline description only in overlays):** Domain overlay placemarks (non-entity) use inline Description with See: path — no balloon excerpt or summary text from the markdown doc.
- **D-13 (Markdown→KML already done):** The 171 → See KML: markers across all 6 domain docs are the forward references. No changes needed to existing markdown files.

### Territorial Verification & Polygon Detail

- **D-14 (Narrative-derived boundaries):** US successor state polygons are based on narrative descriptions in borders-geopolitics.md, using county-level source data merged per entity. Not simple state-line tracing.
- **D-15 (In-KML folder structure as verification):** The KML Places panel hierarchy serves as the verification checklist. Missing regions/entities manifest as absent folders. No separate verification document.
- **D-16 (5-20km vertex spacing):** Polygon coordinates simplified to roughly 5-20km vertex spacing via line simplification (Douglas-Peucker or equivalent). Consistent with the basemap's hand-drawn resolution.
- **D-17 (County-level source for US, country-level for global):** US successor states generated by merging county-level KML polygons. Global entities from a fresh country-level KML dataset (geoBoundaries or Census).
- **D-18 (Antarctica in borders.kml):** Antarctica included as a folder in borders.kml. Resolution (partitioned or unclaimed) follows the territorial integrity section of borders-geopolitics.md per D-29 from Phase 3.

### Polygon Generation Approach

- **D-19 (Programmatic generation with user refinement):** KML files generated via script from source data (US counties KML + global countries KML). User will open generated KMLs in Google Earth Pro to adjust/adjust polygons.
- **D-20 (County-level source data needed):** US county boundaries as KML from Census.gov or geoBoundaries. Global country boundaries from same source. Both datasets are publicly available.

### Index & Finalization

- **D-21 (2050-snapshot/index.md update):** index.md updated to include a KML Maps row in the navigation table with links to each KML file and a brief description.

### the agent's Discretion
- Default colors, line widths, and label visibility for generated placemarks (user will restyle in Google Earth Pro)
- Specific Douglas-Peucker tolerance value to achieve ~5-20km vertex spacing
- Script implementation language and library (Python/KML library recommended)
- Antarctica resolution (partitioned vs unclaimed rationale) — to be read from borders-geopolitics.md territorial integrity section
- Placemark icon choice for overlay placemarks in domain KMLs
- Exact folder hierarchy naming conventions within KML files

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` — Phase 5 requirements (BORD-03, KMLP-01, KMLP-02)
- `.planning/ROADMAP.md` — Phase 5 goal, success criteria, and boundary
- `.planning/PROJECT.md` — Project vision, core value, constraints, user basemap reference

### Prior Phase Context
- `.planning/phases/04-2050-socioeconomic-snapshot-economy-demographics-culture/04-CONTEXT.md` — All Phase 4 decisions, especially D-15 (KML markers), D-16-D-18 (plan structure), D-19 (template)
- `.planning/phases/03-2050-structural-snapshot/03-CONTEXT.md` — Phase 3 decisions: D-27/28/29 (territorial integrity), D-36 (KML markers)
- `.planning/phases/02-2026-2050-transition/02-CONTEXT.md` — Phase 2 boundary decisions
- `.planning/phases/01-foundation-methodology/01-CONTEXT.md` — YAML schemas, prediction format, confidence scale

### Existing Domain Docs (entity specifications for polygons)
- `2050-snapshot/domains/borders-geopolitics.md` — PRIMARY: 19-entity successor state map, territorial claims, trade bloc affiliations, territorial integrity section, Antarctica resolution
- `2050-snapshot/domains/climate.md` — Climate overlay references, migration corridors, resource conflict zones
- `2050-snapshot/domains/technology.md` — AI governance zones, energy systems, healthcare system types, information sovereignty zones
- `2050-snapshot/domains/economy.md` — BRICS+ financial infrastructure, trade bloc zones, labor market zones
- `2050-snapshot/domains/demographics.md` — Entity demographic profiles with KML markers
- `2050-snapshot/domains/culture.md` — Entity cultural profiles with KML markers

### Existing KML Assets
- `2050-snapshot/kml/Earth Current.kml` — User's modern-day basemap, reference for folder hierarchy style and drawing conventions
- `2050-snapshot/kml/` — Target directory for all 2050 KML files

### Existing Vault Assets
- `2050-snapshot/index.md` — Milestone index to be updated with KML navigation
- `2026-2050-transition/successor-states.md` — 19-entity successor state reference map
- `templates/domain-doc.md` — Domain document template
- `meta/consistency-check.md` — Cross-domain consistency mechanism

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Earth Current.kml** (`2050-snapshot/kml/`) — User's hand-drawn modern-day KML basemap organized by continent/subregion hierarchy. Serves as structural model for 2050 KML folder hierarchy and style patterns (CascadingStyle + StyleMap).
- **Domain docs** — All six STEEP domain docs contain → See KML: markers (171 total) specifying placemark names for KML generation. borders-geopolitics.md is the authoritative source for entity boundaries, territorial coverage, and Antarctica status.
- **2050-snapshot/index.md** — Navigation table ready to accept a KML Maps row.
- **Existing prediction register** — Prediction-001 through prediction-013 with doc_ref fields; no new Phase 5 predictions needed (KML is a mapping task, not a forecasting task).

### Established Patterns
- Domain-organized directory structure — KML files follow same STEEP naming as domain docs
- Geographic folder hierarchy in KML — inherited from user's basemap conventions
- → See KML: markers from Phases 3-4 use consistent placemark name format
- Cross-references use full relative paths in existing markdown docs

### Integration Points
- **Phase 5 → Domain docs:** KML polygon descriptions must include See: paths back to specific markdown sections (171 forward references already exist)
- **Phase 5 → 2050-snapshot/index.md:** Navigation table gains a KML Maps row
- **Phase 5 → User workflow:** Generated KMLs opened in Google Earth Pro alongside Earth Current.kml for comparison/verification

</code_context>

<specifics>
## Specific Ideas

- "Entity polygons only in borders.kml" — borders.kml is the authoritative geographic layer; other domain KMLs are overlay-only
- US successor state polygons traced from county-level data, simplified to ~5-20km vertex spacing
- Global entity polygons from fresh country-level dataset (not copied from basemap)
- 2050-specific border modifications drawn for all described changes (Palestine, Israel, EU, Canada-Quebec, etc.)
- Fragmented entities (Atlantic South, Appalachian Zone, Mountain Tapestry) as multiple sub-polygons
- In-KML folder hierarchy doubles as verification checklist
- Programmatic generation via script; user refines in Google Earth Pro
- KML format (not KMZ) for git-friendliness and text editability

</specifics>

<deferred>
## Deferred Ideas

- **V2 KML tooling** (confidence-encoded opacity, NetworkLink modular KML, shared style library) — tracked in REQUIREMENTS.md, deferred to future milestone
- **Economic/demographic zone KML layers** — trade bloc territories, resource extraction areas, population density gradients — deferred per Phase 4 D-15
- **Automated boundary verification script** — current approach is manual/in-KML verification
- **Entity-level language profiles in KML** — language shift covered at global/regional level; entity-level KML annotations deferred

</deferred>

---

*Phase: 05-2050-kml-maps-integration*
*Context gathered: 2026-05-21*
