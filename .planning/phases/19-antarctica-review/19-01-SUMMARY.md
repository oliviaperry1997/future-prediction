---
phase: 19-antarctica-review
plan: 01
subsystem: kml
tags: [kml, json, entity-config, borders, colors, antarctica, claim-zones, polygons]
requires:
  - phase: 18-polynesia-review
    provides: KML folder structure patterns, managed style conventions
provides:
  - 7 claim-zone KML subfolders replacing single Antarctica polygon
  - 7 entity entries in entity-config.json with ATA-{claimant} country codes
  - 7 color entries in user_colors.json
  - 12 new CascadingStyles and 6 new StyleMaps in borders.kml
affects: [19-antarctica-review plan 02+]
tech-stack:
  added: []
  patterns: [longitude-sector polygon classification, managed KML style replication]
key-files:
  created: []
  modified:
    - 2050-snapshot/kml/borders.kml
    - 2050-snapshot/kml/entity-config.json
    - 2050-snapshot/kml/user_colors.json
key-decisions:
  - "GADM coastline geometry used as v1; SCAR ADD ice-shelf data deferred"
  - "Polygons classified by majority-vote longitude sector assignment"
  - "Adélie Land wedge (136°E–142°E) has no assigned polygon patches from existing GADM data"
  - "British Antarctic Territory fill opacity reduced to 25% (dormant paper-claim status)"
requirements-completed:
  - ANTA-01
duration: 674
completed: 2026-05-30
---

# Phase 19 Plan 01: Antarctica Claim-Zone KML Restructuring Summary

**7 claim-zone KML subfolders with distinct styles, entity-config entries, and color definitions replace the single Antarctica coastline polygon, with (wip) tags removed across all files**

## Performance

- **Duration:** 11 min 14 sec (674s)
- **Started:** 2026-05-30T17:47:52Z
- **Completed:** 2026-05-30T17:59:06Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- **borders.kml:** Antarctica (wip) folder renamed to Antarctica; 179 Placemarks classified into 7 claim-zone subfolders by longitude sector; 18 new managed style entries added (12 CascadingStyles 0256-0261 + 6 StyleMaps 0262-0267); XML validates clean
- **entity-config.json:** folder_hierarchy key renamed from "Antarctica (wip)" to "Antarctica" with 7 claim-zone IDs; 7 new entity entries (ATA-AUS through ATA-CN) replace single "Antarctica" entity
- **user_colors.json:** "Antarctica" color key renamed to "Australian Antarctic Territory" (kept #1f2d4a); 6 new color entries added with correct AABBGGRR kml_fill/kml_line values

## Task Commits

1. **Task 1: Replace Antarctica KML with 7 claim-zone subfolders** - `9d23a59` (feat)
2. **Task 2: Update entity-config.json and user_colors.json** - `8d3933d` (feat)

## Verification Results

| Check | Result |
|-------|--------|
| (wip) tag removed from borders.kml | PASS (0 occurrences) |
| Top-level Antarctica folder (1 occurrence) | PASS |
| 7 claim-zone folders present | PASS (AAT:20, Ross:26, Adélie:1, DML:16, ACP:82, BAT:10, CMBL:31) |
| altitudeMode clampToGround present | PASS (4748 occurrences) |
| borders-geopolitics.md#antarctica descriptions | PASS (179 occurrences) |
| KML XML validity (xmllint) | PASS |
| entity-config.json valid JSON | PASS |
| user_colors.json valid JSON | PASS |
| 7 entity entries with ATA- codes | PASS |
| 7 color entries with correct kml values | PASS |
| British Antarctic Territory 25% fill opacity | PASS (kml_fill=408a8a8a) |
| AAT preserved original color #1f2d4a | PASS |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] KML parsing off-by-one in file reconstruction**
- **Found during:** Task 1
- **Issue:** The script's file extraction used incorrect line numbers (41907 vs actual 41491) after discovering the file had shifted from a prior read. Additionally, the `after` block splicing had an off-by-one error that omitted the `<Folder>` tag for Eurasia.
- **Fix:** Corrected line numbers to match actual file positions (block: 41491-43823) and fixed end-of-block index to use `lines[antarctica_end_idx:]` instead of `lines[antarctica_end_idx + 1:]`.
- **Files modified:** 2050-snapshot/kml/borders.kml (via script)
- **Commit:** 9d23a59

**2. [Rule 1 - Bug] Managed style ID template double-prefix**
- **Found during:** Task 1
- **Issue:** The CascadingStyle template had `__managed_style_000000000000{style_id}` where `style_id` already contained the full prefix, producing IDs like `__managed_style_0000000000000000000000000256`.
- **Fix:** Changed template to use `{style_id}` directly without the hardcoded prefix.
- **Files modified:** 2050-snapshot/kml/borders.kml (via script)
- **Commit:** 9d23a59

**3. [Rule 1 - Bug] Style insertion index cut into Africa folder**
- **Found during:** Task 1
- **Issue:** The `style_insert_idx` was set to 10353 (0-indexed) pointing to the `<Folder>` tag for Africa instead of the `</StyleMap>` closing tag for style 0255 at index 10352.
- **Fix:** Corrected to `style_insert_idx = 10352`.
- **Files modified:** 2050-snapshot/kml/borders.kml (via script)
- **Commit:** 9d23a59

## Known Stubs

| Stub | File | Line | Description |
|------|------|------|-------------|
| Adélie Land empty folder | 2050-snapshot/kml/borders.kml | claim-zone subfolder | Adélie Land wedge (136°E–142°E) has 0 Placemarks — no existing GADM polygon patches fell within this narrow 6° sector. The folder structure exists for future SCAR ADD ice-shelf boundary polygons. |

## Threat Flags

None — all operations are local file edits. No network endpoints, auth paths, or trust boundaries introduced.

## Self-Check: PASSED

- [x] borders.kml modified and valid (xmllint passes)
- [x] entity-config.json modified and valid JSON
- [x] user_colors.json modified and valid JSON
- [x] Commit 9d23a59 exists (Task 1)
- [x] Commit 8d3933d exists (Task 2)
- [x] All 7 claim zones have style definitions and entity entries
- [x] (wip) tags removed from all three files
