---
phase: 08-eastern-europe-review
plan: 01
subsystem: kml
tags:
  - eastern-europe
  - kml
  - entity-config
  - borders
  - european-union
  - union-state
  - dev
dependency_graph:
  requires:
    - task_1: "entity-config.json (task 1 must complete first for concept alignment)"
    - task_2: "borders.kml (independent edit from entity-config.json)"
    - task_both: "Both files must be consistent (verified in task 3)"
  provides:
    - Updated Eastern Europe KML and entity config for v1.1
  affects:
    - 2050-snapshot/kml/borders.kml
    - 2050-snapshot/kml/entity-config.json
    - Future pipeline runs using entity-config.json for KML generation
tech-stack:
  added: []
  patterns:
    - "Group entity pattern (source: group, country_codes array) for merged EU representation"
    - "XML comment annotation for programmatic-generation-with-user-refinement boundary precision"
key-files:
  created: []
  modified:
    - 2050-snapshot/kml/entity-config.json
    - 2050-snapshot/kml/borders.kml
decisions: []
metrics:
  duration: 4m0s
  completed_date: "2026-05-27"
---

# Phase 08 Plan 01: Eastern Europe KML & Config Restructuring Summary

**One-liner:** Restructured entity-config.json and borders.kml for Eastern Europe region — merged 6 EU member states into a single European Union entity, removed Moldova, updated Russia/Belarus/Ukraine description anchors, removed all (wip) tags for Eastern Europe.

## Tasks Completed

| # | Task | Type | Commit | Key Files |
|---|------|------|--------|-----------|
| 1 | Update entity-config.json: add European Union, remove EU members, update RU/BY/UA, fix folder_hierarchy | auto | `c668213` | `2050-snapshot/kml/entity-config.json` |
| 2 | Edit borders.kml: remove (wip), restructure EU members into EU folder, remove Moldova, update description anchors | auto | `0b8b9e4` | `2050-snapshot/kml/borders.kml` |
| 3 | Final verification: JSON validation, KML structural check, folder-entity consistency | auto | (same as task 2) | Both files verified |

## What Was Built

### Entity Config (`entity-config.json`)

- **European Union entity**: Added as `source: "group"` with all 27 EU member ISO 3166-1 alpha-3 country codes. References `borders-geopolitics.md#european-union`.
- **Removed individual entities**: Poland, Czechia, Slovakia, Romania, Bulgaria, Moldova — all deleted from entities dict.
- **Updated entities**:
  - **Russia**: Already had correct `section_anchor: "russia"` and `see_path` with `#russia` — no change needed.
  - **Belarus**: Added `section_anchor: "belarus"` and `see_path` with `#belarus`.
  - **Ukraine**: Added `section_anchor: "ukraine"` and `see_path` with `#ukraine`.
- **Folder hierarchy**: Changed `"Eastern Europe (wip)"` → `"Eastern Europe"`. Restructured array to `["European Union", "Russia", "Belarus", "Ukraine"]`.

### Borders KML (`borders.kml`)

- **Removed (wip)**: `"Eastern Europe (wip)"` → `"Eastern Europe"`.
- **European Union folder**: Created with 6 merged Placemarks (Bulgaria, Czechia, Hungary, Poland, Romania, Slovakia), each with `#european-union` description anchor.
- **Moldova folder**: Removed entirely (territory absorbed into Romania → EU).
- **Description updates**:
  - Russia: 214 Placemarks updated to `#russia` anchor
  - Belarus: 1 Placemark updated to `#belarus` anchor
  - Ukraine: 4 Placemarks updated to `#ukraine` anchor
- **XML comment**: Added documenting that precise boundary editing (Crimea + 4 oblasts, Transnistria) requires user adjustment in Google Earth Pro (per D-19 pattern).

## Verification Results

All plan verification checks passed:

- **JSON valid**: `python3 -m json.tool` passes
- **EU entity**: Exists with 27 country_codes, `source: "group"`
- **Removed entities**: Poland, Czechia, Slovakia, Hungary, Romania, Bulgaria, Moldova all absent from entities dict
- **Updated entities**: Russia, Belarus, Ukraine all have non-empty `section_anchor`
- **Folder hierarchy**: `"Eastern Europe": ["European Union", "Russia", "Belarus", "Ukraine"]`, no `(wip)` tag
- **KML structure**: EU folder exists, Moldova removed, all description anchors correct
- **Folder balance**: Positive — Eastern Europe opens/close tags balanced
- **Pipeline compatibility**: Config parses correctly for future generate-kml.py runs

## Deviations from Plan

### Minor Observations (not bugs)

1. **Hungary already in European Core Federation**: The plan assumed Hungary had a standalone entity entry to remove, but Hungary was already part of the existing "European Core Federation" group entry and had no separate `entities` dict entry. The folder_hierarchy reference to Hungary was correctly removed in the Eastern Europe array update.

2. **Old country `<name>` tags remain in EU Placemarks**: The verification grep for `<name>Poland</name>` etc. returns 1 match each — these are the polygon names inside the European Union Placemarks, not top-level country folders. This is correct per the plan's instruction: "Keep the `<name>` as-is (the polygon name like 'Poland' or the coordinate-derived name)".

## Threat Surface Scan

No new threat surface introduced — both files are local KML/JSON data files with no external input channels. All changes are structural re-organization of existing entities.

## Key Decisions

- All changes scoped to Eastern Europe region only — no other regions affected.
- Russia entity entry was already correctly configured (section_anchor + anchored see_path) — no changes needed beyond what was already there.

## Self-Check: PASSED

- `2050-snapshot/kml/entity-config.json` — valid JSON, all assertions pass
- `2050-snapshot/kml/borders.kml` — structurally intact, all folder tags balanced
- `c668213` — commit exists for Task 1
- `0b8b9e4` — commit exists for Task 2
- All verification scripts produce PASS
