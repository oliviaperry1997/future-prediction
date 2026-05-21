---
phase: 05-2050-kml-maps-integration
plan: 02
subsystem: kml-generation
tags: [python, kml, lxml, shapely, fiona, geospatial, cross-reference]
requires:
  - plan: 05-01
    provides: generate-kml.py, entity-config.json, source boundary KMLs
provides:
  - All 6 KML files validated with 96.5% cross-reference coverage
  - Fixed fragmented entity placemark handling
  - Domain doc See KML markers reconciled with KML placemark names
affects:
  - 05-03 (Index finalization — verified KML contents ready for linking)
tech-stack:
  existing:
    - fiona 1.10.1
    - shapely 2.1.2
    - lxml 6.1.1
  patterns:
    - Fragmented entity folders now include parent entity placemark for cross-reference resolution
    - Domain overlay entity_copies bridge domain → KML markers for fragmented entities
key-files:
  modified:
    - 2050-snapshot/kml/generate-kml.py — Added parent placemark in fragmented entity folders
    - 2050-snapshot/kml/entity-config.json — Added 16 entity_copy overlays for demographics, culture, economy
    - 2050-snapshot/kml/borders.kml — Regenerated with 67 placemarks (+3 parent placemarks)
    - 2050-snapshot/kml/climate.kml — Regenerated (unchanged)
    - 2050-snapshot/kml/technology.kml — Regenerated (unchanged)
    - 2050-snapshot/kml/economy.kml — Regenerated with 7 placemarks
    - 2050-snapshot/kml/demographics.kml — Regenerated with 5 placemarks
    - 2050-snapshot/kml/culture.kml — Regenerated with 8 placemarks
    - 2050-snapshot/domains/culture.md — Fixed 4 See KML marker names
    - 2050-snapshot/domains/economy.md — Fixed 1 See KML marker name
    - 2050-snapshot/domains/demographics.md — Fixed 1 See KML marker name
key-decisions:
  - "Added parent entity placemark inside fragmented entity folders (Atlantic South, Appalachian Zone, Mountain Tapestry) so → See KML: markers resolve to a clickable placemark, not just a folder"
  - "Added entity_copy overlays for fragmented entities in economy, demographics, culture domains — these domains have See KML markers referencing entity polygons that exist in borders.kml"
  - "Reconciled domain doc See KML marker names with actual KML entity names (Oceti Sakowin→Dakota/Lakota Nation, Cherokee→Sequoyan Nation, etc.)"
requirements-completed: [BORD-03, KMLP-01, KMLP-02]
duration: 8min 30s
completed: 2026-05-21
---

# Phase 05 Plan 02: KML File Execution and Verification Summary

**Regenerated all 6 STEEP-domain KML files, ran comprehensive cross-reference audit (96.5% coverage), fixed fragmented entity placemark handling, and reconciled domain doc See KML markers with KML entity names**

## Performance

- **Duration:** 8 min 30s
- **Started:** 2026-05-21T21:54:40Z
- **Completed:** 2026-05-21T22:03:10Z
- **Tasks:** 2
- **Files created:** 0
- **Files modified:** 11

## Accomplishments

- **Task 1: Ran KML generation pipeline** — Re-generated all 6 KML files from `entity-config.json` via `generate-kml.py`. Installed dependencies (fiona, shapely, lxml — already present). All 6 KMLs validated as well-formed XML with proper namespace handling, 116 total placemarks across all files, 64 See: cross-references in borders.kml pointing to `borders-geopolitics.md#entity-anchor`.

- **Task 2: Audited cross-references and content completeness** — Ran comprehensive bidirectional cross-reference audit:
  - **166/172** `→ See KML:` markers have matching placemark names (96.5% coverage)
  - All placemarks have `See:` descriptions starting with the proper prefix
  - Folder hierarchy verified: Continent > Subregion > Entity (69 folders across 9 top-level regions)
  - No placemarks without descriptions

### Fixes Applied During Task 2 (Deviation Rule 2)

1. **Fragmented entity placemarks** — generate-kml.py now adds a parent entity-named placemark inside fragmented entity folders, so `→ See KML: Atlantic South` resolves to a clickable placemark in the KML rather than just a folder. Modified 3 fragmented entities.

2. **Entity_copy overlays** — Added 16 entity_copy overlay entries in entity-config.json for economy (4), demographics (4), and culture (7) domains, ensuring their `→ See KML:` markers for fragmented entities and name-corrected entities resolve to placemarks in their own domain KMLs.

3. **Name reconciliation** — Fixed 6 `→ See KML:` marker names in domain docs:
   - culture.md: Oceti Sakowin → Dakota/Lakota Nation
   - culture.md: Cherokee Nation → Sequoyan Nation
   - culture.md: Alaska Indigenous CSR → Alaska Indigenous Confederated Socialist Republic
   - culture.md: EU Core → European Core Federation
   - economy.md: EU Core → European Core Federation
   - demographics.md: EU Core → European Core Federation

## Task Commits

Each task was committed atomically:

1. **Task 1: Install dependencies and run KML generation script** — `1ab462e` (feat)
2. **Task 2: Audit KML cross-references and content completeness** — `2b8a343` (feat)

## KML Summary

| File | Size | Lines | Placemarks | Folders | See: Refs |
|------|------|-------|-----------|---------|-----------|
| borders.kml | 312KB | 1,969 | 67 | 69 | 67 |
| climate.kml | 8.3KB | 205 | 11 | 1 | 11 |
| technology.kml | 31.8KB | 356 | 18 | 1 | 18 |
| economy.kml | 30.5KB | 233 | 7 | 1 | 7 |
| demographics.kml | 36.8KB | 231 | 5 | 1 | 5 |
| culture.kml | 53.6KB | 366 | 8 | 1 | 8 |
| **Total** | **483KB** | **3,360** | **116** | **74** | **116** |

## Decisions Made

- **Parent placemark for fragmented entities**: Rather than requiring Google Earth users to navigate to the folder level and click a sub-polygon, each fragmented entity folder now contains a parent placemark with the entity name. This makes `→ See KML:` markers directly clickable and is consistent with how standard entity placemarks work.
- **Domain overlay strategy**: Following the discovered pattern from Plan 01 that demographics and culture have no unique overlay polygons, entity_copy entries provide the bridge between domain doc `→ See KML:` markers and the entity polygons already in borders.kml.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Functionality] Demographics and culture KMLs had 0 placemarks**
- **Found during:** Task 1
- **Issue:** The plan's done criteria required each KML to have at least one Placemark, but demographics and culture had empty domain_overlays arrays in entity-config.json
- **Fix:** Added single entity_copy placemark each (references PPR entity polygon) to ensure at least one clickable placemark per KML
- **Files modified:** entity-config.json
- **Commit:** `1ab462e`

**2. [Rule 2 - Missing Cross-references] Fragmented entities had no parent placemark**
- **Found during:** Task 2
- **Issue:** Atlantic South, Appalachian Zone, and Mountain Tapestry existed as Folders only — their entity names had no Placemark, so `→ See KML:` markers couldn't resolve to them
- **Fix:** Added parent placemark with entity name in fragmented entity folder generation
- **Files modified:** generate-kml.py
- **Commit:** `2b8a343`

**3. [Rule 2 - Missing Functionality] Domain overlays missing for fragmented entities**
- **Found during:** Task 2
- **Issue:** Economy, demographics, and culture domains had `→ See KML:` markers for fragmented entities (Atlantic South, Appalachian Zone, Mountain Tapestry) but no matching placemarks in their domain KMLs
- **Fix:** Added entity_copy overlay entries in entity-config.json for all 3 fragmented entities across 3 domains
- **Files modified:** entity-config.json
- **Commit:** `2b8a343`

**4. [Rule 2 - Name Mismatch] Six See KML marker names didn't match KML entity names**
- **Found during:** Task 2
- **Issue:** Domain docs used shorthand names (Oceti Sakowin, Cherokee Nation, Alaska Indigenous CSR, EU Core) while KML uses full entity names (Dakota/Lakota Nation, Sequoyan Nation, Alaska Indigenous Confederated Socialist Republic, European Core Federation)
- **Fix:** Updated 6 `→ See KML:` markers in culture.md, economy.md, demographics.md
- **Files modified:** culture.md, economy.md, demographics.md
- **Commit:** `2b8a343`

## Known Remaining Gaps

The following 6 `→ See KML:` markers (3.5%) have no matching placemark — all are by-design or known limitations:

1. **Guam / HFS Compact** (borders-geopolitics.md) — Microstate (GUM code) not in Natural Earth 1:110m source data. Requires higher-resolution source or manual polygon.
2. **Orbital Governance Regime** (borders-geopolitics.md) — No-terrestrial-polygon entity by design (D-28).
3. **Haudenosaunee Confederacy** (culture.md, economy.md, demographics.md) — No-polygon entity within NEC territory by design (D-28).
4. **Regex false positive** (culture.md) — A prose sentence fragment captured by the regex, not a real marker.

## Threat Flags

None — this plan introduces no new network endpoints, auth paths, or file access patterns. All operations are local KML generation and domain doc text updates. Cross-reference paths are static relative file paths.

## Self-Check: PASSED

- [x] All 6 KML files exist and are well-formed XML
- [x] borders.kml has 67 entity placemarks with See: descriptions
- [x] Each domain KML has overlay placemarks (≥1 each)
- [x] Cross-reference audit: 166/172 = 96.5% (≥80% threshold)
- [x] Folder hierarchy: 69 folders across 9 continents/regions
- [x] All placemarks have descriptions

## Next Phase Readiness

- Plan 03 can proceed with finalizing the 2050-snapshot/index.md with KML Maps navigation row
- KML files are complete and validated — ready for user refinement in Google Earth Pro per D-19
- Cross-references are verified bidirectionally between domain docs and KML files

---

*Phase: 05-2050-kml-maps-integration*
*Plan: 02*
*Completed: 2026-05-21*
