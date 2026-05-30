---
phase: 17-micronesia-review
plan: "01"
subsystem: kml-config
tags: [micronesia, entity-config, borders-kml, wip-removal]
dependency_graph:
  requires: []
  provides: [micronesia-folder-renamed, micronesia-entity-entries]
  affects: [entity-config.json, borders.kml]
tech_stack:
  added: []
  patterns: [json-entity-entry-pattern]
key_files:
  created: []
  modified:
    - 2050-snapshot/kml/entity-config.json
    - 2050-snapshot/kml/borders.kml
decisions:
  - "CNMI absent from borders.kml — entity-config.json entry added as placeholder; KML polygon addition is a future task"
metrics:
  duration: "~5 min"
  completed: "2026-05-30"
---

# Phase 17 Plan 01: Micronesia WIP Removal and Entity Config Summary

**One-liner:** Renamed Micronesia (wip) folder to Micronesia in both KML and entity-config.json; added 6 new entity entries (Kiribati, Marshall Is., Micronesia/FSM, Nauru, Palau, CNMI) and CNMI to folder group.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Rename Micronesia folder group + add 6 entity entries | cd2003d | entity-config.json |
| 2 | Rename Micronesia folder in borders.kml | dae6285 | borders.kml |

## What Was Done

### Task 1 — entity-config.json
- Renamed folder group key from `"Micronesia (wip)"` to `"Micronesia"`
- Added `"CNMI"` to the folder group array (per D-02)
- Added 6 individual entity entries following the existing Guam pattern:
  - Kiribati (KIR)
  - Marshall Is. (MHL)
  - Micronesia/FSM (FSM)
  - Nauru (NRU)
  - Palau (PLW)
  - CNMI (MNP)
- JSON validated: `python3 -c "import json; json.load(...)"` exits 0

### Task 2 — borders.kml
- Changed `<name>Micronesia (wip)</name>` → `<name>Micronesia</name>` at line 67725
- No polygon data modified
- CNMI KML presence check: **CNMI is absent from borders.kml** (no "CNMI" or "Northern Mariana" folder found)

## CNMI KML Gap (D-09)

The CONTEXT.md (D-09) states CNMI has its own KML folder confirmed as part of the US territories structure. However, no CNMI or "Northern Mariana" folder was found in borders.kml. This is a gap:
- entity-config.json CNMI entry has been added as a placeholder
- A KML polygon for CNMI needs to be manually added to borders.kml
- This is out of scope for plan 17-01 — flagged for future attention

## Deviations from Plan

None — plan executed exactly as written. CNMI KML gap documented as instructed.

## Verification Results

- `grep -c '"Micronesia (wip)"' entity-config.json` → 0 ✓
- `grep -c '"Micronesia (wip)"' borders.kml` → 0 ✓
- `python3 JSON validation` → exits 0 ✓
- CNMI entry in entity-config.json → PASS ✓
- Kiribati, Nauru, Palau entries → PASS ✓
- `<name>Micronesia</name>` in borders.kml → 22 occurrences ✓

## Self-Check: PASSED

- `2050-snapshot/kml/entity-config.json` — FOUND (modified, committed cd2003d)
- `2050-snapshot/kml/borders.kml` — FOUND (modified, committed dae6285)
- Commits cd2003d and dae6285 — verified in git log
