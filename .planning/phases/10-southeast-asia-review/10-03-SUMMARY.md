---
phase: 10-southeast-asia-review
plan: "03"
subsystem: economy-demographics
tags: [southeast-asia, SEAF, economy, demographics, federation]
dependency_graph:
  requires: [borders-geopolitics-seaf-entry]
  provides: [economy-seaf-entry, demographics-seaf-entry]
  affects: [economy.md, demographics.md]
tech_stack:
  added: []
  patterns: [CAC-style collective entry, federation-first framing]
key_files:
  created: []
  modified:
    - 2050-snapshot/domains/economy.md
    - 2050-snapshot/domains/demographics.md
decisions:
  - "SEAF replaces ASEAN collective entry in economy.md: GDP ~$8T, currency union in formation, collective trade framework"
  - "SEAF replaces ASEAN collective entry in demographics.md: population ~720M, TFR 1.8 federation-wide, SEAF labor mobility"
  - "RCEP/Asian Supply Chains global section updated to reflect SEAF membership (11 states listed)"
  - "Mandarin added as SEAF educational policy second language in demographics.md"
metrics:
  duration: "2m"
  completed: "2026-05-28"
  tasks: 2
  files: 2
---

# Phase 10 Plan 03: SEAF Entries in economy.md and demographics.md Summary

**One-liner:** ASEAN collective entries replaced with SEAF entries in economy.md (~$8T GDP, currency union forming) and demographics.md (~720M population, TFR 1.8, SEAF labor mobility).

## What Was Built

Replaced the outdated `**ASEAN (collective):**` entries in both economy.md and demographics.md with full `**Southeast Asian Federation (SEAF, collective):**` blocks:

### economy.md changes

- **SEAF collective entry:** GDP updated from ~$6T to ~$8T, reflecting Myanmar integration and post-US-collapse trade reorientation. Currency union described as forming with SGD as de facto anchor. SEAF collective trade framework (tariff-free internal trade, one-voice external bargaining) described. SEAF-wide labor mobility section added.
- **Asian Supply Chains global section (lines ~87-89):** ASEAN states updated to Southeast Asian Federation (SEAF) with full 11-member list. "ASEAN local currencies" updated to "SEAF currencies (SGD as anchor, local currencies)". ASEAN reference in key trade flows updated to SEAF.
- **See KML pointer:** Updated from `→ See KML: ASEAN` to `→ See KML: Southeast Asian Federation`

### demographics.md changes

- **SEAF collective entry:** Population updated 680M → ~720M (Myanmar NUG integration + East Timor young population). TFR broken down by member state (Singapore at 1.1 → East Timor at 2.8). Net migration updated 0% → +0.1%/yr (SEAF labor mobility as federation integrates). Urbanization updated 55% → 58% with Yangon recovery noted. Mandarin added as SEAF educational policy required second language.
- **See KML pointer:** Updated from `→ See KML: ASEAN` to `→ See KML: Southeast Asian Federation`

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1 | 015ca4d | feat(10-03): replace ASEAN (collective) entry with SEAF in economy.md |
| 2 | a142269 | feat(10-03): replace ASEAN (collective) entry with SEAF in demographics.md |

## Deviations from Plan

None — plan executed exactly as written.

## Verification Results

All automated checks passed for both files:
- SEAF collective entry present in both economy.md and demographics.md
- ASEAN collective entry removed from both files
- See KML pointers updated to "Southeast Asian Federation" in both files
- No remaining `→ See KML: ASEAN` references in either file
- population ~720M present in demographics.md
- SEAF referenced throughout both entries

## Known Stubs

None — all entries are fully written with economic data, demographic breakdowns, and correct cross-references.

## Threat Flags

None — local markdown file modification only, no new network endpoints or trust boundaries.

## Self-Check: PASSED

- File exists: `2050-snapshot/domains/economy.md` ✓
- File exists: `2050-snapshot/domains/demographics.md` ✓
- Commit 015ca4d exists ✓
- Commit a142269 exists ✓
