---
phase: 20-africa-and-america-re-review
plan: 02
subsystem: kml
tags: [entity-config, kml-generation, nigeria-split, cameroon-fragmentation, car-reassessment, ambazonia, sahel]

requires:
  - phase: 20-01
    provides: Discovery research — Nigeria state allocation, Cameroon fragmentation determination, CAR reassessment outcome

provides:
  - Updated entity-config.json with canonical Africa border changes (3 KML changes: Sahel-Nigeria, Cameroon fragmentation, CAR reassessment)
  - Ambazonia as new source:group entity with North-West and South-West Cameroon regions
  - Updated user_colors.json with Ambazonia color entry
  - Regenerated borders.kml and all 5 overlay KMLs reflecting updated entity set

affects:
  - 20-03: borders-geopolitics.md revision — entity profiles must reference correct entity set from this plan
  - 20-04 through 20-09: All domain doc entity profiles must match entity-config.json entities

tech-stack:
  added: []
  patterns:
    - "Entity fragmentation: source:group with country_codes + admin1_regions for entities with territory from multiple countries"
    - "Multi-fragment entity: source:country with subtract_admin1 for reduced entities, paired with admin1_regions on the absorbing entity"

key-files:
  created: []
  modified:
    - 2050-snapshot/kml/entity-config.json
    - 2050-snapshot/kml/user_colors.json
    - 2050-snapshot/kml/borders.kml
    - 2050-snapshot/kml/climate.kml
    - 2050-snapshot/kml/technology.kml
    - 2050-snapshot/kml/economy.kml
    - 2050-snapshot/kml/demographics.kml
    - 2050-snapshot/kml/culture.kml

key-decisions:
  - "CAR EAF absorption confirmed PLAUSIBLE: 9 southern CAR prefectures subtracted from CAR (via subtract_admin1) and added to EAF admin1 (via source:group with admin1_regions)"
  - "EAF converted from source:manual to source:group with 6 member country codes (BDI, COD, KEN, RWA, TZA, UGA) + 9 CAR admin1 prefectures, keeping original manual KML via add_manual_paths"
  - "Cameroon regions use Natural Earth French admin1 names: Adamaoua, Nord, Extrême-Nord for AES; Centre, Est, Littoral, Ouest, Sud for rump; Nord-Ouest, Sud-Ouest for Ambazonia"
  - "SSD (South Sudan) removed from EAF country_codes — not found in Natural Earth 10m admin0 dataset; covered by add_manual_paths manual EAF KML"

patterns-established:
  - "Entity with admin1 subtractions: source:country + subtract_admin1 for reduced entities (CAR rump pattern)"
  - "Entity with external admin1 additions: source:group + admin1_regions for absorbing entities (AES gets CMR regions, EAF gets CAR prefectures)"

requirements-completed:
  - AFAM-01

# Metrics
duration: 26min
completed: 2026-05-31
---

# Phase 20 Plan 02: Africa KML Border Changes — Sahel-Nigeria, Cameroon Fragmentation, CAR Reassessment

**KML entity-config.json and KML regeneration implementing three canonical Africa border changes from DISCOVERY.md: Sahel-Nigeria reallocation (15 AES + 3 northern CMR / 22 Nigeria states), Cameroon 3-way fragmentation (AES North + Ambazonia + Rump), and CAR reassessment (9 southern prefectures to EAF)**

## Performance

- **Duration:** 26 min
- **Started:** 2026-05-31T10:00:03Z
- **Completed:** 2026-05-31T10:26:14Z
- **Tasks:** 2
- **Files modified:** 8

## Accomplishments

- **entity-config.json:** Implemented all 3 Africa KML changes from DISCOVERY.md with correct admin1 counts:
  - **Sahel-Nigeria:** AES reduced from 20 to 15 NGA states (+3 CMR regions). Nigeria expanded from 17 to 22 states (+FCT, Plateau, Nassarawa, Benue, Kogi).
  - **Cameroon fragmentation:** Cameroon → source:group with 5 southern regions. Ambazonia created with NW+SW regions. AES gains Adamaoua, Nord, Extrême-Nord.
  - **CAR reassessment:** 9 southern prefectures subtracted from CAR via subtract_admin1. 9 southern prefectures added to EAF via admin1_regions.
- **EAF conversion:** Successfully converted from source:manual to source:group with 6 member countries + 9 CAR prefectures + existing manual KML via add_manual_paths.
- **user_colors.json:** Added Ambazonia color (hex: #e6c220, yellow-gold).
- **KML regeneration:** All 6 KML files regenerated with 199 entity polygons, all within 250K vertex limit. No admin1 name mismatches.
- **Validation:** JSON validates, all entities produce valid KML polygons, 242/242 user colors loaded by generator.

## Task Commits

Each task was committed atomically:

1. **Task 1: Update entity-config.json** - `cced8ef` (feat)
2. **Task 2: Add Ambazonia color + regenerate KML** - `b376fab` (feat)

## Files Created/Modified

- `2050-snapshot/kml/entity-config.json` - Updated: AES Nigeria state reallocation, Cameroon fragmentation (3-way), CAR/EAF reassessment, Ambazonia entity
- `2050-snapshot/kml/user_colors.json` - Updated: Ambazonia color entry added
- `2050-snapshot/kml/borders.kml` - Regenerated with all Africa entity changes
- `2050-snapshot/kml/climate.kml` - Regenerated (entity set dependency)
- `2050-snapshot/kml/technology.kml` - Regenerated (entity set dependency)
- `2050-snapshot/kml/economy.kml` - Regenerated (entity set dependency)
- `2050-snapshot/kml/demographics.kml` - Regenerated (entity set dependency)
- `2050-snapshot/kml/culture.kml` - Regenerated (entity set dependency)

## Decisions Made

- **CAR approach:** Used `subtract_admin1` (source:country pattern) for CAR rather than converting to source:group. Cleaner subtraction semantics.
- **EAF approach:** Converted EAF to source:group with country_codes + admin1_regions for CAR prefectures, keeping manual KML via add_manual_paths. SSD excluded from country_codes (not in NE 10m dataset).
- **Admin1 naming:** Natural Earth French admin1 names confirmed correct for CMR (Adamaoua, Nord, Extrême-Nord, Nord-Ouest, Sud-Ouest, Centre, Est, Littoral, Ouest, Sud) and CAF (Bangui, Lobaye, etc.) — generator produced no admin1 lookup errors.

## Deviations from Plan

None — plan executed exactly as written. All admin1 names matched Natural Earth dataset, no manual KML files needed for Ambazonia (source:group with admin1 regions handles it via NE admin1 data).

## Issues Encountered

- **SSD not in Natural Earth 10m:** South Sudan (SSD) is not present in the Natural Earth 10m admin0 KML dataset. Removed from EAF country_codes — the add_manual_paths (existing manual EAF KML) covers this territory.
- **KML regeneration:** The generator must be run after entity-config changes to reflect new entities and admin1 boundaries. All 6 KML files regenerated successfully.

## Known Stubs

None — all entities fully configured with correct admin1 regions and colors.

## Threat Flags

None — no new network endpoints, auth paths, or trust boundary changes introduced.

## Self-Check: PASSED

- entity-config.json contains Ambazonia ✓
- FCT in Nigeria entry ✓
- Ambazonia source:group ✓
- AES 15 NGA states + 3 CMR regions ✓
- Nigeria 22 admin1 regions ✓
- Cameroon 5 admin1 regions (rump) ✓
- CAR 9 subtract_admin1 entries ✓
- EAF source:group with 6 countries + 9 CAR prefectures ✓
- user_colors.json has Ambazonia ✓
- borders.kml references Ambazonia ✓
- All KML files generated under 250K vertex limit ✓

## Next Phase Readiness

- **entity-config.json ready for all downstream documentation work.**
- Borders-geopolitics.md (Plan 03) can reference the final entity set: Nigeria (22 regions), AES (15+3 CMR regions), Ambazonia, Rump Cameroon, Reduced CAR, Expanded EAF.
- Economy/demographics/culture/climate/technology entity profiles (Plans 04-09) must match this entity set.

---

*Phase: 20-africa-and-america-re-review*
*Completed: 2026-05-31*
