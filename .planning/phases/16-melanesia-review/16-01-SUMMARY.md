---
phase: 16-melanesia-review
plan: 01
subsystem: kml
tags: [melanesia, kml, bougainville, entity-config]
dependency_graph:
  requires: []
  provides: [melanesia-folder-renamed, bougainville-entity-added]
  affects: [borders.kml, entity-config.json]
tech_stack:
  added: []
  patterns: [json-edit, kml-edit]
key_files:
  created: []
  modified:
    - 2050-snapshot/kml/entity-config.json
    - 2050-snapshot/kml/borders.kml
decisions:
  - "D-04 RESOLVED: Bougainville is a separate 6th Melanesian entity in the 2050 snapshot"
  - "D-04 reasoning: transition doc explicitly states PNG follows reactionary path by default (governance failure). Under reactionary PNG, Bougainville independence ~2038-2042 is likely per oceania.md lines 124, 151. Bougainville entry added to both KML files."
metrics:
  duration: "8 minutes"
  completed: "2026-05-30"
  tasks_completed: 1
  files_modified: 2
---

# Phase 16 Plan 01: KML Rename + Bougainville Determination Summary

**One-liner:** Removed `(wip)` tag from Melanesia KML folder and added Bougainville as 6th Melanesian entity based on reactionary PNG default per transition doc.

## Tasks Completed

| Task | Description | Commit |
|------|-------------|--------|
| 1 | Resolve D-04, rename Melanesia folder in entity-config.json and borders.kml, add Bougainville | ffac8bd |

## D-04 Decision: Bougainville Independence

**Determination: Bougainville IS a separate 6th Melanesian entity**

**Evidence from oceania.md:**
- Line 61: "Bougainville — potential revolutionary (independence). Autonomous region of PNG with a deferred independence referendum. If the US collapse demonstrates that small-state sovereignty is viable — and if PNG governance continues to fail — Bougainville independence by ~2038-2042 becomes likely."
- Line 123: "PNG follows the reactionary path by default — governance failure prevents it from capturing the revolutionary potential of its resource wealth and strategic position."
- Line 124: "Bougainville achieves independence if PNG governance continues to fail and if the post-US environment demonstrates that small-state sovereignty is viable."
- The conditional is satisfied: PNG governance fails (reactionary default confirmed) + post-US environment demonstrates small-state sovereignty is viable (atoll states, Kanaky precedent).
- Confidence: LOW (per uncertainty ledger line 151) — but the conditions are both met, making this the canonical 2050 outcome.

**Changes made:**
- `entity-config.json`: `"Melanesia (wip)"` → `"Melanesia"` with 6 entities (added `"Bougainville"`)
- `entity-config.json`: Added Bougainville entity entry with country_code `"BVL"`
- `borders.kml`: `<name>Melanesia (wip)</name>` → `<name>Melanesia</name>`
- `borders.kml`: Added empty `<Folder><name>Bougainville</name></Folder>` stub within Melanesia folder

## Verification Results

- ✅ `grep "Melanesia (wip)"` → 0 matches (both files clean)
- ✅ `python3 -c "import json; json.load(...)"` → JSON valid
- ✅ `grep -c '"Melanesia":' entity-config.json` → 1
- ✅ `grep -c '<name>Melanesia</name>'` → 1
- ✅ `grep -c '"Bougainville"' entity-config.json` → 2 (folder list + entity entry)

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check: PASSED
- ffac8bd commit confirmed in git log
- entity-config.json and borders.kml both exist and are modified
