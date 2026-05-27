---
phase: 07-eastern-asia-review
plan: 02
subsystem: borders-geopolitics
tags: [borders, geopolitics, eastern-asia, korea, mongolia, china, japan]
requires: [07-01-KML-updates]
provides: [07-03-economy, 07-04-demographics]
affects: [borders-geopolitics.md]
tech-stack:
  added: []
  patterns: [markdown-document-editing, entity-profile-format, KML-anchor-naming]
key-files:
  created: []
  modified:
    - 2050-snapshot/domains/borders-geopolitics.md (Asia section, TI table, Key Changes)
decisions:
  - D-01: Two Koreas materialized (60% scenario) — ROK reactionary degradation, DPRK revolutionary ascendancy
  - D-02: Entity naming convention: ROK (Republic of Korea) and DPRK (Democratic People's Republic of Korea)
  - D-04: ROK entry describes reactionary degradation — debt, dependency, Lee Jae-myung as least-bad option
  - D-05: DPRK entry describes revolutionary ascendancy — nuclear deterrent codified, sanctions removal, Russia alliance
  - D-06: Mongolia remains sovereign buffer state between China and Russia
  - D-08: Japan entry retained as-is with slow-motion strategic erosion
  - D-10: China territorial reference added — Hong Kong (SAR) and Taiwan (SAR since ~2035-2038)
metrics:
  duration: 12m
  completed_date: "2026-05-27"
---

# Phase 07 Plan 02: Eastern Asia borders-geopolitics recalibration — Summary

**One-liner:** Replaced Unified Korea with separate ROK reactionary degradation and DPRK revolutionary ascendancy entries, added Mongolia as sovereign buffer, updated China with Hong Kong+Taiwan territorial references, and documented the Korea recalibration in the Key Changes section.

## Tasks Completed

| # | Task | Status | Commit(s) | Files |
|---|------|--------|-----------|-------|
| 1 | Replace Korea (Unified) with ROK + DPRK entries, add Mongolia, update China, verify Japan | Complete | fcad63c | borders-geopolitics.md |
| 2 | Update Territorial Integrity table and add Key Changes bullet | Complete | 469af0f | borders-geopolitics.md |
| 3 | Scan for and update residual "Unified Korea" references | Complete (clean — 0 found) | — | — |

## Verification Results

All 12 success criteria verified:

| # | Check | Result |
|---|-------|--------|
| 1 | Mongolia entry as sovereign buffer with KML reference | ✓ PASS |
| 2 | ROK reactionary degradation with US scaffolding loss context | ✓ PASS |
| 3 | DPRK revolutionary ascendancy with sanctions removal context | ✓ PASS |
| 4 | China entry includes "Hong Kong (SAR), and Taiwan (SAR since ~2035-2038)" | ✓ PASS |
| 5 | Japan entry unchanged (slow-motion strategic erosion) | ✓ PASS |
| 6 | India entry preserved intact | ✓ PASS |
| 7 | ASEAN entry preserved intact | ✓ PASS |
| 8 | CAC and all 5 constituent entries preserved intact | ✓ PASS |
| 9 | Territorial Integrity table updated to Mongolia, ROK, DPRK | ✓ PASS |
| 10 | Key Changes has Eastern Asia recalibration bullet | ✓ PASS |
| 11 | Zero residual "Unified Korea" or "Korea (Unified)" references | ✓ PASS |
| 12 | All → See KML: markers use entity names matching Plan 01's KML updates | ✓ PASS |

**Entity insertion order (verified):** China → India → Japan → Mongolia → ROK → DPRK → ASEAN → CAC

## Deviations from Plan

None — plan executed exactly as written. The Task 3 scan found zero residual "Unified Korea" references anywhere in the document, confirming that Tasks 1-2 fully cleaned the document during their edits. No additional file changes were required for Task 3.

## Threat Mitigation Verification

| Threat | Mitigation | Status |
|--------|-----------|--------|
| T-07-05: Accidental deletion of existing entities (India, ASEAN, CAC) | Verified India, ASEAN, and all CAC constituent entries retained after edits | ✓ PASS |
| T-07-06: Inconsistent Korea narrative (ROK/DPRK entries contradicting transition doc) | ROK and DPRK entries cross-referenced with asia.md lines 64-84; consistent with 60% two-Koreas scenario | ✓ PASS |
| T-07-07: TI table entity list incomplete after changes | Verified TI table includes China, India, Japan, Mongolia, ROK, DPRK, ASEAN, CAC | ✓ PASS |

## Decisions Applied

- **D-01**: Two Koreas on diverging trajectories (ROK degradation, DPRK ascendancy)
- **D-02**: Entity names "ROK" and "DPRK" used consistently
- **D-03**: US collapse removed UN sanctions — reflected in DPRK entry
- **D-04**: ROK entry captures reactionary degradation narrative
- **D-05**: DPRK entry captures revolutionary ascendancy narrative
- **D-06**: Mongolia as sovereign buffer state
- **D-08**: Japan entry kept as-is
- **D-10**: China territorial reference added

## Self-Check: PASSED

- [x] `2050-snapshot/domains/borders-geopolitics.md` exists and contains all 3 new entity entries
- [x] Commit fcad63c exists in git log
- [x] Commit 469af0f exists in git log
- [x] Zero residual "Unified Korea" references
- [x] All 12 verification criteria met
