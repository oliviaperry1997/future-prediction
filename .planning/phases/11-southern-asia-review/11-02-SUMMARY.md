---
phase: 11-southern-asia-review
plan: 02
subsystem: content/geopolitics
tags: [southern-asia, borders-geopolitics, feedback-loop, india, pakistan, afghanistan, bangladesh]
dependency_graph:
  requires: [11-01]
  provides: [borders-geopolitics Southern Asia section, asia.md loop stage table updated]
  affects: [11-03, 11-04]
tech_stack:
  added: []
  patterns: [standard-depth entity paragraph, loop stage table row]
key_files:
  created: []
  modified:
    - 2050-snapshot/domains/borders-geopolitics.md
    - 2026-2050-transition/regions/asia.md
decisions:
  - "India expanded to Stage 3 Reactionary Degradation (standard depth, 6 sentences) — RSS/BJP structural dominance, Kashmir LoC frozen, BRICS+ awkward member, orbital role"
  - "Pakistan Stage 4-5 Degradation/Fractures — Quartet nuclear deterrent anchor preserved; 'failed state in all but name' framing superseded"
  - "Afghanistan Stage 1 Reactionary — 'beyond the loop' framing superseded; Taliban as reactionary driver, Chinese mineral penetration"
  - "Bangladesh Stage 2-3 Revolutionary (climate-stressed) — delta crisis, ~15M climate migrants as defining dynamic"
  - "Nepal Stage 2 Revolutionary — China-India buffer leverage, non-alignment"
  - "Bhutan Stage 1-2 GNH model — climate-stressed, neither clearly reactionary nor revolutionary"
  - "Sri Lanka Stage 2 Revolutionary — post-Aragalaya political opening, debt restructuring"
  - "Maldives Stage 1 climate-existential — 0.35m+ sea level, partial relocation by 2050"
metrics:
  duration: "62 minutes"
  completed: "2026-05-28"
  tasks: 2
  files: 2
---

# Phase 11 Plan 02: Southern Asia Borders-Geopolitics Expansion Summary

**One-liner:** India entry expanded to 6-sentence standard depth, 7 new Southern Asia entity paragraphs added (Pakistan–Afghanistan), loop stage table updated with all 8 entities — superseding "failed state" and "beyond the loop" framings.

## What Was Built

### Task 1: Expand India entry and add Southern Asian entity paragraphs to borders-geopolitics.md

**File:** `2050-snapshot/domains/borders-geopolitics.md`

- **India** expanded from 2-line entry to 6-sentence standard-depth paragraph covering: RSS/BJP structural dominance (Stage 3 Reactionary Degradation), jobless growth + 40%+ graduate unemployment + talent flight, Kashmir LoC frozen conflict, Khalistan/Manipur/Tamil pressures contained by BJP centralization, BRICS+ awkward member status, orbital/cislunar role
- **Pakistan** new entry (~3 sentences): Stage 4-5 Degradation/Fractures, Quartet nuclear deterrent anchor (Turkey-Saudi-Egypt-Pakistan framework), Bir Tiwil assignment to Pakistan
- **Bangladesh** new entry (~3 sentences): Stage 2-3 Revolutionary (climate-stressed), delta crisis as defining dynamic, ~15M climate migrants
- **Nepal** new entry (~3 sentences): Stage 2 Revolutionary, China-India buffer leverage, glacier/remittance constraints
- **Bhutan** new entry (~3 sentences): Stage 1-2 GNH model, GLOF risks, no China diplomatic relations, Indian security guarantee
- **Sri Lanka** new entry (~3 sentences): Stage 2 Revolutionary, post-Aragalaya political opening, debt restructuring completed
- **Maldives** new entry (~3 sentences): Stage 1 climate-existential, 0.35m+ sea level rise, ~30-40% population relocated by 2050
- **Afghanistan** new entry (~3 sentences): Stage 1 Reactionary — Taliban reactionary driver, "beyond the loop" framing superseded, Chinese mineral extraction
- Phase 11 review comment added before India entry
- Territorial Integrity table updated: Asia row expanded to include all 8 Southern Asia entities with Pakistan (Quartet, Kashmir, fragmentation notes) and Bangladesh (delta displacement) documented

**Commit:** `88acc52`

### Task 2: Update asia.md loop stage table with Southern Asia assessments

**File:** `2026-2050-transition/regions/asia.md`

- India row updated: Stage 3 Reactionary Degradation (from Stage 3-4)
- Pakistan row updated: Stage 4-5 Degradation/Fractures with Quartet nuclear role preserved ("failed state in all but name" framing replaced)
- 6 new rows added: Bangladesh (Stage 2-3 Revolutionary), Nepal (Stage 2 Revolutionary), Bhutan (Stage 1-2 GNH), Sri Lanka (Stage 2 Revolutionary), Maldives (Stage 1 climate-existential), Afghanistan (Stage 1 Reactionary)
- Afghanistan section heading changed from "Beyond the Loop" to "Stage 1 Reactionary (supersedes 'Beyond the Loop')"
- Pakistan main text (line ~49): "full reactionary collapse" framing replaced with Stage 4-5 Degradation/Fractures + Quartet role
- Convergent evolution section line: "Pakistan and Afghanistan remain failed states" superseded with accurate Stage assessments

**Commit:** `0b0e61e`

## Deviations from Plan

None — plan executed exactly as written. All 8 entity entries written to specified depth and stage assessments. "Beyond the loop" framing superseded as directed by D-08.

## Verification

- `grep "**Pakistan:**" borders-geopolitics.md` → 1 match ✓
- `grep "**Afghanistan:**" borders-geopolitics.md` → 1 match ✓
- `grep "Maldives" borders-geopolitics.md` → 2 matches ✓
- `grep "Bangladesh" asia.md` → 2 matches ✓
- `grep "beyond the loop" asia.md` → 2 matches, both in context of documenting supersession ✓
- India entry: 6 sentences, 100+ words — exceeds 50-word threshold ✓

## Known Stubs

None. All entries are substantive — no placeholder text or TODO markers.

## Self-Check: PASSED

- `88acc52` exists in git log ✓
- `0b0e61e` exists in git log ✓
- `borders-geopolitics.md` modified with 7 new entity entries + expanded India ✓
- `asia.md` modified with updated table and Afghanistan/Pakistan text corrections ✓
