---
phase: 10-southeast-asia-review
plan: "02"
subsystem: borders-geopolitics
tags: [southeast-asia, SEAF, borders, geopolitics, federation]
dependency_graph:
  requires: []
  provides: [borders-geopolitics-seaf-entry]
  affects: [borders-geopolitics.md]
tech_stack:
  added: []
  patterns: [CAC-style collective + sub-entry block]
key_files:
  created: []
  modified:
    - 2050-snapshot/domains/borders-geopolitics.md
decisions:
  - "SEAF replaces ASEAN entry in borders-geopolitics.md Asia section (D-11 through D-13, D-16)"
  - "11 SEAF sub-entries at transition-doc depth: Stage + key dynamic + See KML pointer (D-12)"
  - "Myanmar NUG victory ~2040 canonical in 2050 snapshot; transition doc inconsistency deferred (D-08)"
metrics:
  duration: "3m"
  completed: "2026-05-28"
  tasks: 2
  files: 1
---

# Phase 10 Plan 02: SEAF Entry in borders-geopolitics.md Summary

**One-liner:** ASEAN single-line entry replaced with SEAF collective entry + 11 member sub-entries describing federation formation, revolutionary completeness, and Stage assignments.

## What Was Built

Replaced the outdated ASEAN single-line entry (line ~392) in `2050-snapshot/domains/borders-geopolitics.md` with a full Southeast Asian Federation (SEAF) block:

- **SEAF collective entry:** Describes federation formation (~2040-2048), 11 member states, zero reactionary holdouts, ASEAN institutional lineage, combined GDP ~$8T, South China Sea management, Singapore as BRICS+ financial node
- **11 member sub-entries:** Vietnam, Indonesia, Singapore, Philippines, Thailand, Malaysia, Myanmar, Cambodia, Laos, Brunei, East Timor — each with feedback loop Stage, key dynamic, and See KML pointer
- **Territorial Integrity table:** Asia row updated from ASEAN to Southeast Asian Federation (SEAF) with note on 11-state federation
- **Phase 10 review comment** added before SEAF section following Phase 6-9 convention

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1 | b26f560 | feat(10-02): replace ASEAN entry with SEAF collective + 11 sub-entries |
| 2 | d0122e3 | feat(10-02): update Territorial Integrity table Asia row to SEAF |

## Deviations from Plan

None — plan executed exactly as written.

## Verification Results

All automated checks passed:
- SEAF collective entry present
- All 11 sub-entries present (Vietnam, Indonesia, Singapore, Philippines, Thailand, Malaysia, Myanmar, Cambodia, Laos, Brunei, East Timor)
- Old `**ASEAN:**` entry removed
- Myanmar NUG victory mentioned
- Brunei ceremonial monarchy mentioned
- CAC entry intact (not accidentally removed)
- Territorial Integrity table Asia row: SEAF present, ASEAN absent
- No remaining `→ See KML: ASEAN` references

## Known Stubs

None — all sub-entries are fully written with Stage assignments, key dynamics, and See KML pointers.

## Threat Flags

None — local markdown file modification only, no new network endpoints or trust boundaries.

## Self-Check: PASSED

- File exists: `2050-snapshot/domains/borders-geopolitics.md` ✓
- Commit b26f560 exists ✓
- Commit d0122e3 exists ✓
