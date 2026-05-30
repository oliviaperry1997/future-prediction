---
phase: 15-australasia-review
plan: "03"
subsystem: economy-demographics
tags: [economy, demographics, australia, new-zealand, split-entries]
dependency_graph:
  requires: [australasia-borders-profiles]
  provides: [australasia-economy-demographics]
  affects: [economy.md, demographics.md]
tech_stack:
  added: []
  patterns: [split-combined-entry, entity-specific-narrative]
key_files:
  created: []
  modified:
    - 2050-snapshot/domains/economy.md
    - 2050-snapshot/domains/demographics.md
decisions:
  - "Retained 'Australia/NZ' cross-references in Driving Forces sections — those are narrative references, not sub-entries being replaced"
  - "Added Primary languages field to demographics entries for completeness"
  - "NZ demographics transition doc link corrected to oceania.md (was pointing to demographics.md driver)"
metrics:
  duration: "4 min"
  completed: "2026-05-30T11:16:00Z"
---

# Phase 15 Plan 03: economy.md + demographics.md Split Summary

**One-liner:** Split combined Australia/NZ sub-entries into individual entries in economy.md (AUD $1.6T, NZD $400B, distinct sector/trade profiles) and demographics.md (~28M + ~7M, distinct migration/climate/ethnic narratives).

## Tasks Completed

| Task | Description | Commit | Files |
|------|-------------|--------|-------|
| 1 | Replace combined Australia/NZ entry in economy.md with 2 separate entries | ae12685 | economy.md |
| 2 | Replace combined Australia/NZ entry in demographics.md with 2 separate entries | ae12685 | demographics.md |

## Verification

- `grep -c "Australia / New Zealand\|Australia/NZ" economy.md` → 0 ✓
- `grep -c "Australia / New Zealand\|Australia/NZ" demographics.md` → 2 (both in Driving Forces cross-references, not sub-entries) ✓
- `grep -n "1.6T\|400B" economy.md` → both GDP figures present in separate entries ✓
- `grep -n "~28M\|~7M" demographics.md` → population figures in separate entries ✓

## Deviations from Plan

**[Rule 2 - Enhancement]** Added `"Primary languages"` field to both demographics entries — the original combined entry had this field, so individual entries should have it too for completeness. Not a deviation from intent, just ensuring field parity.

**[Noted]** Demographics.md has 2 remaining "Australia/NZ" occurrences — both are in the Driving Forces section's narrative cross-references (`destination regions (Pacifica, European Federation, East Africa, Australia/NZ)`) which are out of scope for this plan's sub-entry replacement task.

## Self-Check: PASSED
