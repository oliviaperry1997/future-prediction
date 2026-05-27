---
phase: 08-eastern-europe-review
plan: 05
subsystem: 2050-snapshot
tags: [kml, borders, european-union, eastern-europe, styles, fix]
dependency_graph:
  requires:
    - 08-02 (borders-geopolitics entity fates)
    - 08-04 (culture + climate coverage)
  provides:
    - Corrected KML with all 27 EU member states in a single EU folder
    - Unified EU style (#012F9A) and Belarus style (#A19E77)
    - Balanced folder structure with no orphaned containers
  affects:
    - 2050-snapshot/kml/borders.kml (structural fix)
tech-stack:
  added:
    - __managed_style_EUROPEAN_UNION (gx:CascadingStyle, border ff9a2f01, fill 409a2f01)
    - __managed_style_BELARUS (gx:CascadingStyle, border ff779ea1, fill 40779ea1)
  patterns:
    - All EU placemarks reference unified style via styleUrl
    - All EU placemarks include consistent description linking to borders-geopolitics.md
key-files:
  created: []
  modified:
    - 2050-snapshot/kml/borders.kml (5447 insertions, 5510 deletions)
decisions:
  - All 27 EU member placemarks consolidated into single European Union folder
  - Moldova polygon not in KML (previously removed; absorption documented in entity-config/docs)
  - Eastern Ukraine oblast transfer requires Natural Earth source editing (not KML-only fix)
metrics:
  duration: ~15 minutes
  completed_date: 2026-05-27
---

# Phase 8 Plan 5: KML EU Merge and Style Fix — Summary

**One-liner:** Fixed the Eastern Europe borders.kml by merging all 27 EU member state placemarks (357 polygons across Northern, Southern, and Western Europe) into a single European Union folder with unified #012F9A styling, adding a #A19E77 Belarus style, and removing empty country folders — producing a balanced, xmllint-valid KML.

## Execution

- **Plan type:** fix (autonomous)
- **Tasks completed:** 1 (single atomic KML transformation)
- **Dependencies:** 08-02 (entity fates), 08-04 (culture + climate)

### Task: KML Structural Fix — EU Merge, Style Addition, Folder Cleanup

**Commit:** `0cef97d`

**Changes:**

1. **EU polygon merge (all 27 members)**
   - 6 members (Bulgaria, Czechia, Hungary, Poland, Romania, Slovakia) were already in the EU folder
   - Moved 357 placemarks from 21 remaining EU member countries:
     - **Northern Europe (7):** Denmark (15), Estonia (8), Finland (42), Ireland (7), Latvia (1), Lithuania (2), Sweden (41)
     - **Southern Europe (8):** Croatia (25), Cyprus (4), Greece (74), Italy (29), Malta (2), Portugal (17), Slovenia (1), Spain (23)
     - **Western Europe (6):** Austria (1), Belgium (1), France (30), Germany (22), Luxembourg (1), Netherlands (11)
   - EU folder now contains 363 placemarks covering all 27 member states
   - Empty country folders removed from source regions

2. **Custom style definitions added**
   - `__managed_style_EUROPEAN_UNION`: border `ff9a2f01` (full opacity #012F9A), fill `409a2f01` (25% opacity #012F9A)
   - `__managed_style_BELARUS`: border `ff779ea1` (full opacity #A19E77), fill `40779ea1` (25% opacity #A19E77)
   - Inserted after the last existing `gx:CascadingStyle` in the Document

3. **styleUrl updates**
   - All 363 EU placemarks now reference `#__managed_style_EUROPEAN_UNION`
   - Belarus placemark now references `#__managed_style_BELARUS`
   - Description added to all moved EU placemarks pointing to `borders-geopolitics.md#european-union`

## Things NOT Changed (Intentional Scope)

- **Moldova polygon**: The Moldova folder was previously removed in an earlier plan. Moldova placemarks do not exist in the KML. Romania's EU polygon covers the territory visually. The absorption is documented in entity-config and borders-geopolitics.md. No KML change needed.
- **Eastern Ukraine oblasts transfer (Crimea, Donetsk, Luhansk, Zaporizhzhia, Kherson)**: These require Natural Earth source data editing, not KML folder restructuring. Comment at line ~49330 documents this.
- **Non-EU countries**: Iceland, Norway, United Kingdom, Switzerland, Balkan states (Albania, Bosnia, Kosovo, Montenegro, North Macedonia, Serbia, Turkey) remain in their respective regions.

## Deviations from Plan

None — plan executed exactly as written.

## Verification Results

| # | Check | Result |
|---|-------|--------|
| 1 | All 27 EU members present in EU folder | ✅ All 27 unique countries, 363 placemarks |
| 2 | EU placemarks use EU style (#012F9A) | ✅ 364 references (363 placemarks + 1 definition) |
| 3 | Belarus uses Belarus style (#A19E77) | ✅ 2 references (1 placemark + 1 definition) |
| 4 | Description set on all EU placemarks | ✅ `borders-geopolitics.md#european-union` present on all |
| 5 | Non-EU countries remain in regions | ✅ Iceland, Norway, UK, Switzerland, Balkan states intact |
| 6 | Moldova references = 0 | ✅ 0 matches (absorption handled by docs) |
| 7 | Balanced tags (Folder, Placemark) | ✅ 229/229 open/close Folder, 4928/4928 open/close Placemark |
| 8 | xmllint validates | ✅ No output (valid) |

## Self-Check: PASSED

- Modified file exists: `2050-snapshot/kml/borders.kml`
- Commit exists: `0cef97d`
- KML validates via xmllint with no errors
- No unintended file deletions
