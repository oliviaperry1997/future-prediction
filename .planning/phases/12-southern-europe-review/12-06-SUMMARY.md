---
phase: 12-southern-europe-review
plan: "06"
subsystem: domain-files
tags: [serbia, bosnia, eu-accession, borders-geopolitics, economy, culture, climate, gap-closure]
dependency_graph:
  requires: [12-05]
  provides: [consistent-serbia-bosnia-eu-framing-across-four-domain-files]
  affects: [borders-geopolitics.md, economy.md, culture.md, climate.md]
tech_stack:
  added: []
  patterns: [sovereign-to-eu-subdivision-reframing]
key_files:
  modified:
    - 2050-snapshot/domains/borders-geopolitics.md
    - 2050-snapshot/domains/economy.md
    - 2050-snapshot/domains/culture.md
    - 2050-snapshot/domains/climate.md
decisions:
  - "Serbia documented as EU member (~2045 accession) across all domain files, consistent with SRB in entity-config.json country_codes"
  - "Bosnia documented as EU member (~2047 accession) across all domain files, consistent with BIH in entity-config.json country_codes"
  - "Territorial integrity table updated to 33 EU subdivisions / 6 Western Balkans accessions ~2040-2047"
  - "BRI/remittance/Orthodox/Dinaric factual content retained as legacy pre-accession context"
metrics:
  duration: "4m"
  completed: "2026-05-28T22:45:15Z"
  tasks: 2
  files: 4
---

# Phase 12 Plan 06: Serbia/Bosnia EU Reframing — Four Domain Files Summary

**One-liner:** Serbia (~2045) and Bosnia (~2047) reframed as EU Federation subdivision sub-entries with accession narratives across borders-geopolitics, economy, culture, and climate domain files.

## Objective

Close UAT failures in tests 5, 7, 9, and 10 — all caused by Phase 12's executor keeping Serbia/Bosnia as sovereign states contrary to user intent. This plan aligns four domain files with entity-config.json and borders.kml (fixed in 12-05), which encode Serbia/Bosnia as EU Federation members.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Reframe Serbia and Bosnia in borders-geopolitics.md | 27f337c | borders-geopolitics.md |
| 2 | Remove *(Sovereign)* labels in economy, culture, climate | f019309 | economy.md, culture.md, climate.md |

## Changes Made

### borders-geopolitics.md
- **Serbia entry** replaced: standalone sovereign "reactionary holdout through 2050" paragraph → EU subdivision sub-entry documenting ~2045 accession after Vučić-era degradation, Kosovo recognition threshold, BRI base as pre-accession legacy
- **Bosnia entry** replaced: standalone sovereign "frozen in Dayton amber" paragraph → EU subdivision sub-entry documenting ~2047 accession structurally coupled to Serbia's, Republika Srpska blocking mechanism dissolution
- **Territorial integrity table**: Europe row updated — Serbia and Bosnia removed from entity list; EU count updated from 31→33 subdivisions; accession range updated ~2040-2046→~2040-2047; "Serbia and Bosnia-Herzegovina are sovereign non-EU states" sentence removed

### economy.md
- Serbia: `*(Sovereign — see borders-geopolitics.md#serbia)*` removed; BRI paragraph reframed from present-tense dependency to legacy pre-accession footprint; KML pointer updated to European Federation
- Bosnia: `*(Sovereign — see borders-geopolitics.md#bosnia-and-herzegovina)*` removed; structural dysfunction closing sentence updated from "without accession, structural funds unavailable" to EU accession legacy challenge framing; KML pointer updated to European Federation

### culture.md
- Serbia: `*(Sovereign)*` removed; added closing sentence on EU membership without erasing Orthodox-Slavic distinctiveness; KML pointer updated to European Federation
- Bosnia: `*(Sovereign)*` removed; added closing sentence on three-community cultural geography within EU framework; KML pointer updated to European Federation

### climate.md
- Serbia: `*(Sovereign)*` removed; climate facts retained unchanged (geographically invariant); KML pointer updated to European Federation
- Bosnia: `*(Sovereign)*` removed; coal/CBAM sentence updated from "carbon border adjustment mechanism penalizes Bosnian exports" to mandatory phase-out under EU environmental law with Just Transition Mechanism funding; KML pointer updated to European Federation

## Verification Results

All automated checks pass:
- `Sovereign non-EU` in borders-geopolitics.md: 0 occurrences ✓
- `Acceded to the European Federation ~2045` in borders-geopolitics.md: 1 ✓
- `Acceded to the European Federation ~2047` in borders-geopolitics.md: 1 ✓
- `33 member subdivisions` in borders-geopolitics.md: 1 ✓
- `(Sovereign)` in economy.md: 0 ✓
- `(Sovereign)` in culture.md: 0 ✓
- `(Sovereign)` in climate.md: 0 ✓
- `See KML: Serbia` in economy.md: 0 ✓
- `See KML: Bosnia` in economy.md: 0 ✓

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None — all four domain files have complete factual content with full accession narratives.

## Self-Check: PASSED

- `27f337c` confirmed in git log ✓
- `f019309` confirmed in git log ✓
- All four modified files verified to exist and contain correct content ✓
