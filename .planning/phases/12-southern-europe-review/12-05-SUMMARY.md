---
phase: 12-southern-europe-review
plan: "05"
subsystem: kml-data
tags: [kml, entity-config, gap-closure, turkey, northern-cyprus, bosnia, serbia]
dependency_graph:
  requires: [12-01, 12-02, 12-03, 12-04]
  provides: [entity-config-bosnia-serbia-absorbed, turkey-in-western-asia, northern-cyprus-precise-polygon]
  affects: [borders.kml, entity-config.json]
tech_stack:
  added: []
  patterns: [python-json-load-write, python-string-replace, folder-counting-algorithm]
key_files:
  modified:
    - 2050-snapshot/kml/entity-config.json
    - 2050-snapshot/kml/borders.kml
decisions:
  - "Turkey folder moved to first child of Western Asia (wip) using depth-counting algorithm to find exact </Folder> boundary"
  - "Bosnia/Serbia removed as standalone entities; BIH/SRB appended to EU Federation country_codes (36→38)"
  - "Northern Cyprus approximate 24-point bounding box replaced with precise 28-point Attila Line polygon"
metrics:
  duration: "~10 minutes"
  completed: "2026-05-28"
  tasks_completed: 2
  files_modified: 2
---

# Phase 12 Plan 05: KML/Entity-Config Gap Closure Summary

**One-liner:** Three surgical data-integrity fixes: Bosnia/Serbia EU absorption propagated to entity-config, Turkey repositioned inside Western Asia (wip), Northern Cyprus upgraded to precise Attila Line polygon.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Fix entity-config.json — remove Bosnia/Serbia standalones, add BIH/SRB to EU Federation | 5af5f77 | entity-config.json |
| 2 | Fix borders.kml — move Turkey into Western Asia (wip) and replace Northern Cyprus polygon | aa991c9 | borders.kml |

## What Was Built

### Task 1 — entity-config.json changes
- `folder_hierarchy.Eurasia.Southern Europe` set to `[]` (was `["Bosnia and Herzegovina", "Serbia"]`)
- `entities["Bosnia and Herzegovina"]` entry deleted entirely
- `entities["Serbia"]` entry deleted entirely
- `entities["European Federation"]["country_codes"]` extended with `"BIH"` and `"SRB"` (36 → 38 entries)
- ALB, KOS, MNE, MKD confirmed already present

### Task 2 — borders.kml changes
- Turkey's `<Folder>` block extracted from bare Eurasia level and inserted as first child of `<Folder><name>Western Asia (wip)</name>` (before Bahrain)
- Used depth-counting algorithm to find exact Turkey block end (counting `<Folder>` / `</Folder>` tags)
- Northern Cyprus `<coordinates>` block replaced: 24-point approximate bounding box → 28-point precise Attila Line polygon
- Removed 4 TODO/approximate placeholder comments; replaced with accurate Attila Line description

## Verification Results

All checks passed:
- `python3 -c "import json; json.load(open('2050-snapshot/kml/entity-config.json'))"` → exit 0
- `python3 -c "import xml.etree.ElementTree as ET; ET.parse('2050-snapshot/kml/borders.kml')"` → exit 0
- European Federation country_codes length: **38**, BIH: True, SRB: True
- `grep -c "TODO: Replace with precise" borders.kml` → **0**
- `grep -c "33.355000,35.098000,0" borders.kml` → **1**
- Bosnia and Herzegovina absent from entities: **PASS**
- Serbia absent from entities: **PASS**

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check: PASSED

- [x] `2050-snapshot/kml/entity-config.json` exists and modified
- [x] `2050-snapshot/kml/borders.kml` exists and modified
- [x] Commit 5af5f77 exists
- [x] Commit aa991c9 exists
