---
phase: 14-western-europe-review
plan: 01
subsystem: kml-entity-config
tags:
  - entity-config
  - borders.kml
  - Switzerland
  - Liechtenstein
  - European Federation
  - EU
dependency_graph:
  requires: []
  provides:
    - "CHE+LIE added to EU Federation country_codes in entity-config.json"
    - "Switzerland standalone KML/entity entry removed"
    - "Switzerland polygon merged into EU Federation multi-polygon KML"
  affects:
    - borders-geopolitics.md (plan 14-02 will add Western Europe sub-entries)
tech-stack:
  added: []
  patterns: []
key-files:
  created: []
  modified:
    - 2050-snapshot/kml/entity-config.json
    - 2050-snapshot/kml/borders.kml
decisions: []
metrics:
  duration: "~15 minutes"
  completed_date: "2026-05-29"
---

# Phase 14 Plan 01: Merge Switzerland and Liechtenstein into European Federation KML — Summary

**One-liner:** Removed Switzerland standalone entity entry (entity-config.json lines ~1276-1284) and folder/KML polygon (borders.kml lines ~61834-61849); added CHE and LIE to European Federation country_codes; merged Switzerland's polygon geometry as a new Placemark in the European Federation folder.

## Tasks Executed

### Task 1: Entity Config — Remove Switzerland standalone, add CHE+LIE to EU Federation

**Action:**
1. Removed the Switzerland standalone entity entry from `entities` object in `entity-config.json` (8 lines: key, type, category, source, country_code, domain_doc, section_anchor, see_path).
2. Removed `"Switzerland"` from the `folder_hierarchy.Eurasia["Western Europe"]` array — only `"European Federation"` remains.
3. Added `"CHE"` (Switzerland) and `"LIE"` (Liechtenstein) to the European Federation `country_codes` array, inserted after `"BIH"` and before `"SRB"`.
4. Confirmed all 6 Western EU member codes present: AUT, BEL, FRA, DEU, LUX, NLD.

**Verification:**
- `c.entities.Switzerland` → `undefined` (standalone removed)
- `c.entities['European Federation'].country_codes.includes('CHE')` → `true`
- `c.entities['European Federation'].country_codes.includes('LIE')` → `true`
- JSON parse: valid (no syntax errors)

**Commit:** `5376161`

### Task 2: KML — Merge Switzerland polygon into European Federation

**Action:**
1. Extracted Switzerland's Polygon geometry (2939-char coordinate string) from the standalone Switzerland `<Placemark>`.
2. Created a new `<Placemark>` at the end of the European Federation folder with the same polygon geometry, using the European Federation name (`<name>European Federation</name>`) and style (`#__managed_style_000000000000005A`).
3. Removed the Switzerland `<Folder>` block entirely.
4. Fixed orphaned `</Folder>` closing tag left after removal.

**Verification:**
- `/<name>Switzerland<\/name>/.test(xml)` → `false` (Switzerland Placemark removed)
- `/<name>European Federation<\/name>/.test(xml)` → `true` (EU Federation present)
- XML structure: 1 Document, 205 Folder, 4775 Placemark — all open/close counts balanced
- EU Federation Placemarks: 419 (418 original + 1 Switzerland polygon)

**Commit:** `8f1973b`

## Deviations from Plan

### Auto-fixed Issues (Rule 2 — Missing Critical Functionality)

**1. [Rule 2] Removed Switzerland from folder_hierarchy in entity-config.json**
- **Found during:** Task 1
- **Issue:** The plan specified removing Switzerland from the `entities` object but did not explicitly mention removing it from the `folder_hierarchy.Eurasia["Western Europe"]` array. Without this removal, the KML generator would still create a Switzerland folder entry.
- **Fix:** Removed `"Switzerland"` from the Western Europe folder list, leaving only `"European Federation"`.
- **Files modified:** `2050-snapshot/kml/entity-config.json`
- **Commit:** `5376161`

**2. [Rule 1] Orphaned `</Folder>` closing tag after KML removal**
- **Found during:** Task 2
- **Issue:** After removing the Switzerland `<Folder>` block, an orphaned `</Folder>` closing tag (originally the Switzerland folder's close) remained, producing an unbalanced XML structure.
- **Fix:** Removed the orphaned closing tag.
- **Files modified:** `2050-snapshot/kml/borders.kml`
- **Commit:** `8f1973b`

## Known Stubs

None.

## Threat Flags

| Flag | File | Description |
|------|------|-------------|
| N/A | | No new security-relevant surface introduced. |

## Self-Check: PASSED

- [x] `2050-snapshot/kml/entity-config.json` exists and is valid JSON
- [x] `2050-snapshot/kml/borders.kml` exists and has balanced XML tags
- [x] Commit `5376161` exists in git log
- [x] Commit `8f1973b` exists in git log
- [x] All acceptance criteria met
