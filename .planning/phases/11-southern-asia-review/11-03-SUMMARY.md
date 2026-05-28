---
phase: 11-southern-asia-review
plan: 03
subsystem: content/economy-demographics
tags: [southern-asia, economy, demographics, india, pakistan, bangladesh, afghanistan, maldives, nepal, bhutan, sri-lanka]
dependency_graph:
  requires: [11-02]
  provides: [economy.md Southern Asia full profiles, demographics.md Southern Asia full profiles]
  affects: [11-04]
tech_stack:
  added: []
  patterns: [standard-depth entity profile, bold-header entry format]
key_files:
  created: []
  modified:
    - 2050-snapshot/domains/economy.md
    - 2050-snapshot/domains/demographics.md
decisions:
  - "India economy expanded to full standard depth (7 bullets): GDP ~$12T, IT services $350B, pharma backbone, BRICS+ awkward-member (D-03), fiscal structure, INR BRICS+ clearing, informal-sector labor crisis"
  - "Pakistan economy: GDP ~$450B patronage state, Quartet nuclear-deterrent economy, Gulf remittances $30B/yr primary FX source, perpetual IMF programs"
  - "Bangladesh economy: GDP ~$800B developmental state, garment exports $120B/yr, delta displacement structural drag on coastal zones"
  - "Nepal economy: INR-pegged remittance-dependent semi-subsistence, hydropower export transition (glacial constraint ~2040+)"
  - "Bhutan economy: GNH managed-growth ceiling, hydropower 70%+ government revenue, 1:1 INR peg"
  - "Sri Lanka economy: post-crisis recovery $250B, diversified away from China-only debt model"
  - "Maldives economy: climate-displaced microstate $10B, luxury tourism compressed, climate finance inflows"
  - "Afghanistan economy: $35B Taliban patronage state, Chinese mineral extraction (BRI), normalized drug economy"
  - "India demographics expanded: north-south divide, $100B remittances (world #1 recipient), 15M+ Bangladesh border pressure"
  - "Bangladesh demographics: ~15M delta displacement as defining dynamic (consistent with existing lines 79, 82)"
  - "Maldives demographics: -2.0%/yr net migration (climate relocation), 150-200K relocated to Hulhumale/India by 2050"
  - "Afghanistan demographics: TFR 4.5 (no demographic transition under Taliban), median age 20, life expectancy 63"
metrics:
  duration: "35 minutes"
  completed: "2026-05-28"
  tasks: 2
  files: 2
---

# Phase 11 Plan 03: Southern Asia Economy and Demographics Summary

**One-liner:** India economy/demographics expanded to full standard depth plus 7 new Southern Asia entity profiles (Pakistan–Afghanistan) added to both economy.md and demographics.md — establishing the socioeconomic foundation for Plan 04 culture/climate coverage.

## What Was Built

### Task 1: Expand India economy entry and add 7 Southern Asia economy profiles

**File:** `2050-snapshot/domains/economy.md`

- **India** economy expanded from 6 bullets (~8 lines) to 7 substantive bullets with concrete figures: GDP ~$12T (3rd PPP, high Gini), IT services $350B export despite talent flight, pharma generic backbone for BRICS+, BRICS+ awkward-member detail (D-03 — economic-pragmatic not political-revolutionary), fiscal structure (remittances $100B+/yr, INR BRICS+ clearing house), labor crisis (90% informal, 40%+ graduate unemployment, north-south inequality)
- **Pakistan:** GDP ~$450B — patronage economy, Quartet nuclear-deterrent revenue, CPEC debt, Gulf remittances $30B/yr primary FX; PKR hyperinflation baseline
- **Bangladesh:** GDP ~$800B — developmental state, garment $120B/yr (world #2), delta displacement as structural economic drag, inland industrial center shift
- **Nepal:** GDP ~$150B — INR-pegged remittance-dependent, hydropower export (glacial constraint post-~2040), labor export economy
- **Bhutan:** GDP ~$12B — GNH managed-growth ceiling, hydropower 70%+ government revenue, INR 1:1 peg, BTN legal tender
- **Sri Lanka:** GDP ~$250B — post-2022-crisis recovery, digital services + sustainable tourism diversification, China debt dependency broken
- **Maldives:** GDP ~$10B — climate-displaced microstate, luxury tourism compressed, sovereign wealth fund funding transition, Indian patronage
- **Afghanistan:** GDP ~$35B — Taliban patronage state, Chinese mineral extraction (BRI), opium normalized as state revenue, no SWIFT access
- Phase 11 review comment added before India entry

**Commit:** `172386b`

### Task 2: Expand India demographics entry and add 7 Southern Asia demographics profiles

**File:** `2050-snapshot/domains/demographics.md`

- **India** demographics expanded to 10 bullets: north-south demographic divide (median age 27 north vs. 37 south), $100B remittances/8M+ Gulf workers, internal migration corridors, India-Bangladesh border pressure (15M+ Bangladeshis displaced toward Assam/West Bengal), religious diversity under RSS governance
- **Pakistan:** 280M growing, TFR 3.0, median age 24 extreme youth bulge, 5-8M internally displaced from Balochistan/KP conflict + recurrent flooding
- **Bangladesh:** 190M approaching peak, TFR 1.7, ~15M delta displacement as defining demographic dynamic (consistent with demographics.md lines 79, 82 — no contradiction), managed India climate-migration agreements
- **Nepal:** 35M stable, -1.5%/yr net migration (one of South Asia's highest per capita), 500K+ high-altitude climate displacement
- **Bhutan:** 1M, GNH happiness brain drain, GLOF displacement risk in northern communities
- **Sri Lanka:** 22M stable-declining, TFR 1.6, Tamil/Sinhala/Muslim demographic composition, post-crisis diaspora reversal
- **Maldives:** peak 600K declining to ~400K, -2.0%/yr net migration (climate relocation — highest in Southern Asia), 150-200K relocated to Hulhumale/India, sovereign state maintained
- **Afghanistan:** 50M growing, TFR 4.5 (Taliban reversed demographic transition drivers), median age 20, 1-2M climate displaced, life expectancy 63 (lowest in region)
- Phase 11 review comment added before India entry

**Commit:** `b6942ac`

## Deviations from Plan

None — plan executed exactly as written. Both files expanded with all 8 Southern Asian entity profiles. Cross-references verified:
- economy.md line 72 (BRICS+ member list): India entry confirms awkward-member status ✓
- economy.md line 135 (talent flight from India): India economy entry adds detail on talent flight consistent with labor mobility section ✓
- demographics.md lines 79, 82 (~15M Bangladesh delta migration): Bangladesh demographics entry explicitly references this figure and is consistent ✓

## Verification

- `grep "**Pakistan:**" economy.md` → 1 match ✓
- `grep "**Afghanistan:**" economy.md` → 1 match ✓
- `grep "awkward" economy.md` → 1 match (India BRICS+ awkward member) ✓
- `grep "**Bangladesh:**" demographics.md` → 1 match ✓
- `grep "15M" demographics.md` → 7 matches (existing lines 79, 82 + Bangladesh profile multiple refs) ✓
- All 8 entities present in both files with GDP, sectors/population, model/TFR, currency/migration, labor/urbanization, KML links ✓

## Known Stubs

None. All profiles are substantive with specific figures, dynamics, and cross-references.

## Self-Check: PASSED

- `172386b` exists in git log ✓
- `b6942ac` exists in git log ✓
- economy.md: India expanded + 8 Southern Asia entities ✓
- demographics.md: India expanded + 8 Southern Asia entities ✓
