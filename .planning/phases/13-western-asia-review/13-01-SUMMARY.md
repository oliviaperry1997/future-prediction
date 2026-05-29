# Phase 13 Plan 01: Restructure Western Asia KML folder and entity configuration

**One-liner:** Renamed Western Asia (wip) folder, added South Caucasus + Levant Republic + Arab United Front entities to entity-config.json and borders.kml stubs.

## What Was Done

### Task 1: entity-config.json

1. **Renamed folder key** `"Western Asia (wip)"` → `"Western Asia"` in `folder_hierarchy.Eurasia`
2. **Updated folder list:**
   - Removed: Jordan, Lebanon (deprecated into Levant Republic)
   - Kept: Bahrain, Iran, Iraq, Israel, Kuwait, Oman, Palestine, Qatar, Saudi Arabia, Syria, Turkey, United Arab Emirates, Yemen
   - Added: Armenia, Azerbaijan, Georgia, Nagorno-Karabakh, Levant Republic, Arab United Front
3. **Confirmed** Turkey not present in Southern Europe (empty list — no deduplication needed)
4. **Added 6 new entity entries:**
   - Armenia (country, ARM)
   - Azerbaijan (country, AZE)
   - Georgia (country, GEO)
   - Nagorno-Karabakh (manual, regional category)
   - Levant Republic (manual, merged Jordan+Lebanon+Palestine polygon)
   - Arab United Front (group: PSX, YEM, LBN)
5. **Updated section_anchors** for 10 existing entities with empty anchors: Iraq, Jordan, Lebanon, Kuwait, Oman, Qatar, Syria, United Arab Emirates, Yemen, Bahrain. Jordan and Lebanon redirect to `levant-republic`.

### Task 2: borders.kml

1. **Renamed** `<name>Western Asia (wip)</name>` → `<name>Western Asia</name>`
2. **Added 5 new stub Placemarks** inside the Western Asia folder (before closing `</Folder>`): Armenia, Azerbaijan, Georgia, Nagorno-Karabakh, Levant Republic — each with TODO comments and description links
3. **Added deprecation comments** before Jordan and Lebanon `<Folder>` tags noting they are retained for polygon reference only

## Verification

All automated checks passed:
- JSON valid
- KML XML valid
- All assertion checks on folder hierarchy, folder contents, entity entries, section_anchors, sources

## Files Modified

- `2050-snapshot/kml/entity-config.json`
- `2050-snapshot/kml/borders.kml`

## Deviations from Plan

None — plan executed exactly as written.
