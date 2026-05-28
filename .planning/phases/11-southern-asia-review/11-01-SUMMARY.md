---
phase: 11-southern-asia-review
plan: "01"
subsystem: kml-entity-config
tags: [kml, entity-config, southern-asia, afghanistan, region-review]
dependency_graph:
  requires: []
  provides: [southern-asia-kml-clean, afghanistan-kml-home, southern-asia-entity-anchors]
  affects: [borders.kml, entity-config.json]
tech_stack:
  added: []
  patterns: [json-edit, kml-edit, python3-verification]
key_files:
  created: []
  modified:
    - 2050-snapshot/kml/entity-config.json
    - 2050-snapshot/kml/borders.kml
decisions:
  - "(wip) removed from Southern Asia — region audit Phase 11 is now in progress"
  - "Afghanistan moved from Central Asia to Southern Asia in both entity-config and KML"
  - "All 7 non-India Southern Asia entities now have explicit section_anchor fields"
  - "Siachen Glacier polygon (formerly unclaimed, lon 76.8-77.8 lat 35.1-35.6) assigned to Pakistan and merged into Pakistan main body via shapely unary_union — Pakistan now has 2 polygons (merged northern body 462 pts + small coastal exclave). Do NOT re-add Siachen as a separate entity or revert Pakistan to 3 polygons."
metrics:
  duration: ~5m
  completed: 2026-05-28
  tasks_completed: 2
  files_modified: 2
---

# Phase 11 Plan 01: Southern Asia (wip) Removal and Afghanistan Placement Summary

**One-liner:** Removed `(wip)` from Southern Asia region, moved Afghanistan from Central Asia to Southern Asia, and populated 7 missing `section_anchor` fields in entity-config.json and borders.kml.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Update entity-config.json — rename folder, move Afghanistan, fix anchors | ddb7d79 | entity-config.json |
| 2 | Update borders.kml — remove (wip), add Afghanistan folder | ed86796 | borders.kml |

## What Was Built

**Task 1 — entity-config.json:**
- Renamed `folder_hierarchy.Eurasia["Southern Asia (wip)"]` → `"Southern Asia"`
- Removed `Afghanistan` from `Central Asia` array (now 5 entities)
- Added `Afghanistan` to `Southern Asia` array (now 8 entities: Bangladesh, Bhutan, India, Maldives, Nepal, Pakistan, Sri Lanka, Afghanistan)
- Set `section_anchor` + `see_path` for all 7 non-India entities (Afghanistan, Pakistan, Bangladesh, Nepal, Bhutan, Sri Lanka, Maldives)

**Task 2 — borders.kml:**
- Renamed `<name>Southern Asia (wip)</name>` → `<name>Southern Asia</name>`
- Moved Afghanistan `<Folder>` with real polygon coordinates from Central Asia into Southern Asia
- Updated Afghanistan Placemark description from bare doc reference to `#afghanistan` anchor
- Central Asia KML now has 5 countries; Southern Asia has 8

## Verification

All automated assertions passed:
- `entity-config.json` parses as valid JSON
- `"Southern Asia (wip)"` absent from both files
- `"Afghanistan"` present in Southern Asia (KML line ~60333)
- `Afghanistan` absent from Central Asia KML
- `Pakistan.section_anchor == "pakistan"` — confirmed
- `Afghanistan.section_anchor == "afghanistan"` — confirmed

## Deviations from Plan

None — plan executed exactly as written. Afghanistan had a real polygon in Central Asia KML (not a stub), so the full polygon was moved rather than creating a placeholder stub.

## Known Stubs

None — Afghanistan has real polygon coordinates (moved from Central Asia).

## Self-Check: PASSED

- `2050-snapshot/kml/entity-config.json` — exists and valid JSON
- `2050-snapshot/kml/borders.kml` — exists with Southern Asia (no wip), Afghanistan in Southern Asia
- Task 1 commit `ddb7d79` — confirmed
- Task 2 commit `ed86796` — confirmed
