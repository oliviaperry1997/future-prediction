---
phase: 06-central-asia-review
plan: 03
type: execute
subsystem: 2050-snapshot
dependency_graph:
  requires: [06-02]
  provides: [CAC economic and demographic profiles in economy.md and demographics.md]
  affects: [KML map generation, borders-geopolitics consistency]
tech-stack:
  added: []
  patterns: [Entity profile format for confederal states with collective + constituent structure]
key-files:
  created: []
  modified:
    - 2050-snapshot/domains/economy.md
    - 2050-snapshot/domains/demographics.md
decisions:
  - "Used CAC collective parent profile + 5 constituent republic profiles matching existing entity format (Turkey as template)"
  - "Kazakhstan economic profile given transition doc link to asia.md#6-central-asia--reactionary-low-intensity-trap"
  - "Kazakhstan demographic profile given transition doc link to demographics.md Driver 3"
metrics:
  duration: ~15m
  completed_date: "2026-05-27"
---

# Phase 6 Plan 3: Add CAC Economic and Demographic Profiles to 2050 Snapshot

**One-liner:** Inserted Central Asian Confederation collective + 5 constituent republic (Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Uzbekistan) economic and demographic profiles into the 2050 snapshot domain documents, matching existing entity profile format and depth.

## Completed Tasks

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Add CAC economic profiles to economy.md | `1b0e052` | `2050-snapshot/domains/economy.md` |
| 2 | Add CAC demographic profiles to demographics.md | `8c42f14` | `2050-snapshot/domains/demographics.md` |

## What Was Built

### 1. CAC Economic Profiles (economy.md)

Inserted 7 entity profiles (1 CAC collective + 5 constituent) between Turkey and Unified Korea:

- **CAC collective** (~$750B combined, confederal coordination model, no common currency)
- **Kazakhstan** (~$450B, oil/gas dominant, most externally oriented CAC economy)
- **Uzbekistan** (~$120B, cotton/gold, largest domestic market at ~37M)
- **Turkmenistan** (~$80B, natural gas/autarkic, least integrated)
- **Kyrgyzstan** (~$40B, hydroelectric/remittance-dependent, smallest economy)
- **Tajikistan** (~$60B, hydropower/aluminum, youngest median age ~26)

Each profile follows the standard fields: GDP, Dominant sectors, Trade partners, Economic model, Currency, Labor market character. Each has a `→ See KML:` marker. Kazakhstan includes a transition doc link to asia.md.

### 2. CAC Demographic Profiles (demographics.md)

Inserted 7 entity profiles (1 CAC collective + 5 constituent) between Turkey and Unified Korea:

- **CAC collective** (~80M, young median age ~30, TFR 2.8, net migration -0.2%/yr)
- **Kazakhstan** (20M, TFR 2.5, urbanization 58%)
- **Uzbekistan** (37M, TFR 3.1, median age 29)
- **Turkmenistan** (6.5M, TFR 2.2, lowest life expectancy 70)
- **Kyrgyzstan** (7M, TFR 2.7, lowest urbanization 38%)
- **Tajikistan** (10M, TFR 3.4, median age 26 — youngest in CAC)

Each profile follows the standard fields: Population, Age structure, TFR, Net migration, Urbanization, Life expectancy, Labor force participation, Primary languages. Each has a `→ See KML:` marker. Kazakhstan includes a transition doc link to demographics.md Driver 3.

## Verification Results

All 6 verification criteria from plan passed:

1. ✅ CAC collective + 5 constituent profiles exist in economy.md
2. ✅ CAC collective + 5 constituent profiles exist in demographics.md
3. ✅ All profiles have → See KML: markers
4. ✅ No existing content removed (Turkey and Unified Korea entries intact)
5. ✅ Population totals internally consistent (20+37+6.5+7+10 = 80.5M ≈ 80M); GDP totals consistent (450+120+80+40+60 = $750B)
6. ✅ No duplicate entity entries created

## Deviations from Plan

None — plan executed exactly as written.

## Threat Mitigation

- **T-06-03 (Data integrity):** Verified population sums (80.5M ≈ 80M) and GDP sums ($750B = $750B) are consistent between CAC collective and constituent profiles.
- **T-06-04 (Consistency):** CAC economic model descriptions ("confederal coordination" with "pooled sovereignty") are consistent with the CAC confederal structure documented in D-01 through D-04 of the phase context.

## Self-Check: PASSED

- `2050-snapshot/domains/economy.md` — exists, contains CAC + 5 republics ✅
- `2050-snapshot/domains/demographics.md` — exists, contains CAC + 5 republics ✅
- Commit `1b0e052` — exists ✅
- Commit `8c42f14` — exists ✅
