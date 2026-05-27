---
phase: 06-central-asia-review
plan: 01
subsystem: kml-borders
tags: [kml, central-asia, exclaves, ferghana-valley, geopolitics]
dependency_graph:
  requires: [05-2050-kml-maps-integration (borders.kml created)]
  provides: [clean-central-asia-kml]
  affects: [borders.kml]
tech-stack:
  added: []
  patterns: [KML innerBoundaryIs for exclave holes]
key-files:
  created: []
  modified:
    - 2050-snapshot/kml/borders.kml
decisions:
  - "Exclave coordinates use approximate rectangles (plan nominal values — sufficient for visualization in Google Earth)"
  - "Afghanistan KML entity removed but will be restored in Phase 11 (Southern Asia Review)"
metrics:
  duration: "~8 minutes"
  completed: "2026-05-27"
---

# Phase 06 Plan 01: Central Asia KML Review — Summary

**One-liner:** Removed (wip) tags, deleted Afghanistan from Central Asia folder, added Ferghana Valley exclave interior holes (Sokh, Shakhimardan, Vorukh, Barak) as innerBoundaryIs polygons, and updated all 16 Central Asia Placemark descriptions with CAC member context.

## Tasks Executed

| Task | Name | Commit | Key Files |
|------|------|--------|-----------|
| 1 | Remove (wip) tags and relocate Afghanistan from Central Asia | `f7e5403` | borders.kml |
| 2 | Add Ferghana Valley exclave interior holes | `3287ff2` | borders.kml |
| 3 | Update KML descriptions to reference 2050 domain documents | `10f2b64` | borders.kml |

## Results

### Task 1: (wip) tags removed, Afghanistan removed
- `Eurasia (wip)` → `Eurasia` ✓
- `Central Asia (wip)` → `Central Asia` ✓
- Afghanistan folder (16 lines, 1 Placemark with coordinates) deleted from Central Asia ✓
- All 5 Stan Folders (Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Uzbekistan) remain intact ✓

### Task 2: Ferghana Valley exclave interior holes
- Kyrgyzstan main polygon: 3 `<innerBoundaryIs>` sections added for:
  - **Sokh** (Uzbekistan exclave): 71.05,39.95 — 71.20,40.07
  - **Shakhimardan** (Uzbekistan exclave): 71.75,39.88 — 71.85,39.98
  - **Vorukh** (Tajikistan exclave): 70.55,39.75 — 70.68,39.88
- Uzbekistan main polygon: 1 `<innerBoundaryIs>` section added for:
  - **Barak** (Kyrgyzstan exclave): 72.77,40.58 — 72.82,40.63
- Total inner rings: 7 (3 existing + 4 new)
- KML well-formed: ✓ (xmllint --noout passes)

### Task 3: CAC member descriptions
- All 16 Placemark descriptions in Central Asia updated to reference `CAC member — See: 2050-snapshot/domains/borders-geopolitics.md#central-asia`
- No Placemarks outside Central Asia modified ✓
- KML remains well-formed ✓

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None. The exclave coordinates use approximate rectangles as specified in the plan, which is intentional for the current review phase.

## Threat Flags

None. The plan's threat register mitigations (T-06-01: xmllint validation, T-06-02: Stan Folder integrity check) were both verified.

## Self-Check

| Check | Result |
|-------|--------|
| `grep 'Eurasia (wip)'` returns 0 matches | ✅ PASS |
| `grep 'Central Asia (wip)'` returns 0 matches | ✅ PASS |
| No `<name>Afghanistan</name>` inside Central Asia folder | ✅ PASS |
| All 5 Stan Folders exist | ✅ PASS |
| Total innerBoundaryIs = 7 | ✅ PASS |
| CAC descriptions count = 16 | ✅ PASS |
| `xmllint --noout` validates | ✅ PASS |
| Commit hashes exist: f7e5403, 3287ff2, 10f2b64 | ✅ PASS |
