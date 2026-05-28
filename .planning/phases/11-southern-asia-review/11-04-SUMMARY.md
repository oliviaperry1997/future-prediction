---
phase: 11-southern-asia-review
plan: 04
subsystem: content/culture-climate
tags: [southern-asia, culture, climate, india, pakistan, bangladesh, nepal, bhutan, sri-lanka, maldives, afghanistan]
dependency_graph:
  requires: [11-02, 11-03]
  provides: [culture.md Southern Asia full profiles, climate.md Southern Asia entity profiles]
  affects: []
tech_stack:
  added: []
  patterns: [standard-depth cultural profile, entity climate subsection]
key_files:
  created: []
  modified:
    - 2050-snapshot/domains/culture.md
    - 2050-snapshot/domains/climate.md
decisions:
  - "India culture expanded: RSS/BJP cultural project, Hindi language wars, Bollywood $4B soft power, 35M+ diaspora as cultural bridge — consistent with Stage 3 Reactionary Degradation"
  - "Pakistan culture: Urdu-over-regional-languages tension, diaspora more vibrant than domestic, Pashtunwali/Deobandi coexistence"
  - "Bangladesh culture: Language Movement 1952 founding logic, climate-adaptation culture (baira), Dhallywood/Baul tradition"
  - "Nepal culture: 120+ ethnic groups, Himalayan brand, glacier anxiety, remittance gender dynamics"
  - "Bhutan culture: GNH as export philosophy, Lhotshampa trauma, climate grief"
  - "Sri Lanka culture: Aragalaya generation as new cultural identity, Sinhala-Tamil functional coexistence"
  - "Maldives culture: climate grief + Digital Maldives archiving as defining cultural project"
  - "Afghanistan culture: Taliban erasure documented, diaspora as pluralist-culture carrier"
  - "Southern Asia climate: entity-level subsection added after line 82 aggregate; ~15M Bangladesh figure consistent with existing migration section"
  - "GLOF risk: Nepal (20+ critical lakes) and Bhutan (Thorthormi, Raphstreng Tsho) explicitly documented"
  - "Maldives climate: existential framing — 35cm+ rise vs 1.5m mean elevation, EEZ sovereignty without territory"
  - "Indus water conflict: existing line 105 transboundary section confirmed consistent — no rewrite needed"
metrics:
  duration: "15 minutes"
  completed: "2026-05-28"
  tasks: 2
  files: 2
---

# Phase 11 Plan 04: Southern Asia Culture and Climate Summary

**One-liner:** India culture entry expanded with RSS cultural project and diaspora soft-power detail; 7 new Southern Asia cultural profiles added; Southern Asia entity-level climate subsection with GLOF/delta/atoll coverage added after existing Asia aggregate paragraph.

## What Was Built

### Task 1: Expand India culture entry and add 7 Southern Asia cultural profiles

**File:** `2050-snapshot/domains/culture.md`

- **India** expanded from 5-sentence entry to 8-sentence standard-depth profile: RSS/BJP cultural project (cow protection law, Hindi imposition, Uniform Civil Code as cultural-political instruments), constitutional pluralism vs. RSS hegemony tension, regional language resistance (southern states), Bollywood/streaming ~$4B export industry, 35M+ diaspora as cultural bridge (second-generation in UK/Pacifica/Atlantica), Hindi-south resistance dynamics
- **Pakistan:** Urdu-over-majority-language tension, diaspora more vibrant than domestic, Pashtunwali/Deobandi cultural coexistence
- **Bangladesh:** Language Movement 1952 as founding cultural logic, climate-adaptation culture (baira floating gardens), Dhallywood/Baul, Dhaka megacity hub
- **Nepal:** Hindu-Buddhist syncretic synthesis, 120+ ethnic groups federal recognition, Himalayan global brand, remittance gender dynamics
- **Bhutan:** GNH as international reference point export, constitutional cultural preservation (tourism quotas, screen time limits), Lhotshampa trauma, glacier anxiety
- **Sri Lanka:** Sinhala-Tamil functional coexistence, Aragalaya generation as new cultural identity, post-war reconciliation framing
- **Maldives:** climate grief + Digital Maldives archiving as defining cultural project, Dhivehi/Islamic anchors during displacement
- **Afghanistan:** Taliban systematic cultural erasure documented, underground cultural production, diaspora as Dari/Pashto pluralist carrier
- Phase 11 review comment added before India entry

**Commit:** `8e9d8ff`

### Task 2: Add Southern Asia entity-level climate profiles to climate.md

**File:** `2050-snapshot/domains/climate.md`

- Southern Asia subsection header added after Asia aggregate paragraph (does not rewrite existing line 82)
- **India:** heat mortality (50°C+/wet-bulb threshold), glacier retreat (500M+ northern water), flood-drought oscillation, India-Bangladesh climate-migration frontline
- **Pakistan:** Indus basin compounding stresses, 50°C plain temps, 2022-pattern flooding recurrence, Indus Waters Treaty under glacier stress
- **Bangladesh:** 35cm+ sea level vs 1-3m elevation, ~15M displaced (consistent with existing line 95), cyclone intensification, salinization, world's largest managed relocation program
- **Nepal:** GLOF threat (20+ critical glacial lakes), peak water threshold reached, hydropower export risk, Terai monsoon flooding
- **Bhutan:** GLOF (Thorthormi Glacier Lake, Raphstreng Tsho), carbon-negative injustice framing, glacier-hydropower threat
- **Sri Lanka:** Monsoon disruption (both monsoon seasons), coastal erosion, coral bleaching, agriculture resilience transition
- **Maldives:** Climate-existential — 35cm+ vs 1.5m mean, EEZ sovereignty without habitable territory, Hulhumale capacity limit, coral bleaching
- **Afghanistan:** Climate as governance force multiplier, Kabul aquifer 70%+ depleted, climate+conflict migration indistinguishable
- Indus water conflict at existing resource conflicts section verified consistent — no rewrite needed
- Phase 11 review comment added before Southern Asia subsection

**Commit:** `86beb31`

## Deviations from Plan

None — plan executed exactly as written. Threat model mitigations applied:
- T-11-07 (Bangladesh ~15M figure): Read existing migration section before writing; Bangladesh climate entry references ~15M displaced "consistent with the climate migration section above" — no contradiction
- T-11-08 (India entry duplication): Read line 237 before writing; replaced existing entry directly — no duplicate created at the profile section level (line 77 is a bullet in a religion-demographics table, not a cultural profile)

## Verification

- `grep "**Pakistan:**" culture.md` → 1 match ✓
- `grep "**Afghanistan:**" culture.md` → 1 match ✓
- `grep "Maldives" culture.md` → 1 match ✓
- `grep "**Southern Asia**" climate.md` → 1 match ✓
- `grep -c "GLOF\|glacial lake" climate.md` → 2 matches ✓
- India entry: expanded from 5 to 8 sentences with RSS/BJP, Hindi, diaspora, Bollywood detail ✓
- No duplicate India cultural profile entry at the `#### Key Global Powers` section ✓
- Indus water conflict at existing line 105+ confirmed present and consistent ✓

## Known Stubs

None. All profiles are substantive with specific figures, dynamics, and KML cross-references.

## Threat Flags

None. Both files modified only cultural content — no new network endpoints, auth paths, or schema changes introduced.

## Self-Check: PASSED

- `8e9d8ff` exists in git log ✓
- `86beb31` exists in git log ✓
- culture.md: India expanded + 7 new Southern Asia cultural profiles + Phase 11 comment ✓
- climate.md: Southern Asia entity-level subsection with 8 entries + Phase 11 comment ✓
