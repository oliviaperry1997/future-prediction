---
phase: 10-southeast-asia-review
plan: "01"
subsystem: kml-data
tags: [southeast-asia, seaf, kml, entity-config, federation]
dependency_graph:
  requires: []
  provides: [seaf-entity-config, seaf-kml-folder]
  affects: [borders-kml-pipeline, entity-config]
tech_stack:
  added: []
  patterns: [european-federation-pattern, group-entity-with-country-codes]
key_files:
  created: []
  modified:
    - 2050-snapshot/kml/entity-config.json
    - 2050-snapshot/kml/borders.kml
decisions:
  - "Southeast Asian Federation replaces all 11 individual country entries — mirrors European Federation pattern (source: group, keep_unified: true)"
  - "TLS (ISO 3166-1 alpha-3) used for East Timor/Timor-Leste as per D-05 cross-check"
  - "Placeholder polygon sufficient until generate-kml.py reruns with updated entity-config.json"
metrics:
  duration: "~8 minutes"
  completed: "2026-05-28"
  tasks_completed: 3
  files_modified: 2
---

# Phase 10 Plan 01: Southeast Asian Federation — entity-config.json and borders.kml Summary

## One-Liner

Southeast Asia (wip) folder replaced by Southeast Asian Federation collective entity with all 11 ISO codes in entity-config.json and borders.kml, mirroring the European Federation pattern.

## What Was Built

Replaced the Southeast Asia (wip) region folder across both KML data files with a single unified Southeast Asian Federation (SEAF) entity. This mirrors the Eastern Europe and European Federation approach: no individual country entries, one collective group entity with all member state ISO codes.

**entity-config.json changes:**
- `folder_hierarchy.Eurasia`: "Southeast Asia (wip)" → "Southeast Asian Federation": ["Southeast Asian Federation"]
- Removed East Timor individual entity entry (the only individual SEA country entity)
- Added Southeast Asian Federation entity: source: group, keep_unified: true, 11 country codes (BRN, KHM, TLS, IDN, LAO, MYS, MMR, PHL, SGP, THA, VNM), section_anchor: southeast-asian-federation

**borders.kml changes:**
- Removed ~409 KB Southeast Asia (wip) folder (477 Placemarks, 11 country subfolders: Brunei, Cambodia, East Timor, Indonesia, Laos, Malaysia, Myanmar, Philippines, Singapore, Thailand, Vietnam)
- Replaced with single Southeast Asian Federation folder containing one representative polygon Placemark
- Description anchor: `See: 2050-snapshot/domains/borders-geopolitics.md#southeast-asian-federation`

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| Task 1 | d792275 | feat(10-01): replace Southeast Asia (wip) with Southeast Asian Federation in entity-config.json |
| Task 2 | ec779d7 | feat(10-01): replace Southeast Asia (wip) folder with Southeast Asian Federation in borders.kml |
| Task 3 | — | Validation only (no file changes) |

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

**borders.kml SEAF polygon:** The Placemark contains a rough representative polygon (20 coordinate points approximating the SEA region bounding box). The actual unified SEAF polygon will be properly generated when `generate-kml.py` is re-run with the updated entity-config.json. This is intentional per the plan — the placeholder confirms structure in Google Earth Pro while the pipeline generates the real geometry.

## Self-Check

- [x] `2050-snapshot/kml/entity-config.json` exists and contains SEAF entity
- [x] `2050-snapshot/kml/borders.kml` exists and contains Southeast Asian Federation folder
- [x] Commit d792275 exists (entity-config.json)
- [x] Commit ec779d7 exists (borders.kml)
- [x] All validations passed: `PASS: All Phase 10 Plan 01 validations passed`

## Self-Check: PASSED
