---
phase: 12-southern-europe-review
plan: "04"
subsystem: world-state
tags: [southern-europe, culture, climate, mediterranean, balkans, desertification, wildfire]
dependency_graph:
  requires: [12-02]
  provides: [culture-southern-europe, climate-southern-europe]
  affects: [culture.md, climate.md]
tech_stack:
  added: []
  patterns: [sub-entry-under-federation, sovereign-standalone-entry, regional-framing-entry]
key_files:
  created: []
  modified:
    - 2050-snapshot/domains/culture.md
    - 2050-snapshot/domains/climate.md
decisions:
  - "Italy culture: FdI far-right cultural project ultimately absorbed into EU federal norms; Catholic Church authority declining; northern/southern cultural asymmetry resolved by EU subdivision structure"
  - "Spain culture: Catalan independence defused by EU federalization offering alternative recognition channels; Spanish Islam integration mixed but EU antidiscrimination standards enforced"
  - "Greece culture: post-Aegean trauma as defining cultural event; Orthodox-national bond intensified; Turkey as civilizational adversary"
  - "Mediterranean climate: 1.5-2x global average warming; medicanes; desertification front advancing; Spain/Italy/Greece most affected"
  - "Malta: highest EU sea-level exposure per land area; Grand Harbour/Sliema/airport coastal threat"
  - "Cyprus: 40-42°C summer heat; water scarcity existential; 0.3-0.5m sea-level on eastern Mediterranean coast"
  - "Bosnia-Herzegovina climate: flash flood risk from Dinaric atmospheric rivers; coal dependency penalized by EU carbon border adjustment"
metrics:
  duration: "~20 minutes"
  completed: "2026-05-28"
  tasks_completed: 2
  files_modified: 2
---

# Phase 12 Plan 04: Southern Europe Culture + Climate Summary

**One-liner:** Cultural profiles (far-right Italy, Catalan Spain, post-Aegean Greece, Balkans Orthodox/Muslim divide) and climate profiles (Mediterranean desertification, wildfire, medicanes, Malta/Cyprus sea-level) for all Southern European entities.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Write culture.md entries | `3cfdf29` | `2050-snapshot/domains/culture.md` |
| 2 | Write climate.md entries | `3cfdf29` | `2050-snapshot/domains/climate.md` |

## What Was Built

### culture.md
Added entries for all Southern European entities after the European Federation bloc entry:
- **Italy**: Three-force collision — FdI far-right cultural project vs. EU progressive norms vs. north/south asymmetry. Meloni/FdI cultural trajectory ultimately absorbed into EU federal framework by mid-2040s. Vatican sovereignty maintained but institutional Church authority declining. Lombard EU-oriented identity vs. Roman-Catholic-conservative south.
- **Spain**: Catalan/Basque regionalism defused by EU federal recognition channels (independence question less meaningful when both Spain and Catalonia would be EU subdivisions). Spanish Islam — Moroccan-origin Muslim community ~3-4M, mixed integration outcomes. Atlantic + Mediterranean + colonial history + Moorish legacy = uniquely hybrid cultural identity.
- **Greece**: Post-Aegean territorial loss as the defining cultural event — Orthodox-national bond intensified; EDF advocacy culturally resonant (military dignity, territorial restoration aspiration). Diaspora (Australia, US, UK, Germany) mobilized around Eastern Aegean reconstruction. Turkey as civilizational adversary in Greek cultural self-understanding.
- **Portugal**: Lusophone global culture (Brazilian 215M speakers, Angola, Mozambique); Fado as cultural export; Atlantic-European positioning becomes asset post-US collapse.
- **Cyprus**: Greek Cypriot identity under partition — cultural memory of the north, desire for reunification as cultural constant even if politically frozen.
- **Croatia, Malta, Slovenia**: Post-Yugoslav Catholic/European (Croatia); bilingual Mediterranean microstate Catholic (Malta — Maltese is EU's only Semitic language); Alpine Central European (Slovenia).
- **Albania, Kosovo, Montenegro, North Macedonia**: EU accession as cultural transformation; religious coexistence (Albania Bektashi tradition); Kosovo post-war identity; North Macedonia "name dispute" resolved into EU generational identity shift.
- **Serbia**: Serbian Orthodox nationalism as cultural constant; Kosovo narrative ("Serbian Jerusalem") live cultural wound; Russia as cultural reference (shared Orthodoxy, pan-Slavism, anti-Western alignment).
- **Bosnia-Herzegovina**: Three-entity cultural geography (Bosniak Muslim, Croat Catholic, Serbian Orthodox) sharing a state but not a cultural project. Sarajevo urban cosmopolitan exception.

### climate.md
Added Mediterranean regional framing entry and all Southern European entity entries:
- **Mediterranean regional framing**: 1.5-2× global average warming; summer 45-48°C in southern Spain/Sicily/Greece; Mediterranean SST +2.5°C; medicanes increasing; desertification front advancing; 0.3-0.5m sea-level rise.
- **Spain**: Southeastern desertification (Murcia/Almería crossing threshold); Segura/Jucar permanent water deficit; wildfire regime (Galicia/Cantabrian Atlantic coast counterintuitively severe; central/southern Spain May-October season); renewable energy yield increasing with warming.
- **Italy**: Southern Italy/Sicily semi-arid transition; Po Valley heat stress 40°C+ regularly; agricultural yields down 10-20%; Calabria/Sicily/Sardinia wildfire regime comparable to worst Australian fire years; Alpine glacier retreat.
- **Greece**: Athens 42-45°C — EU's hottest capital; Attica urban heat island; Crete/Aegean desertification (rainfall -15-25%); wildfire regime (Attica, Peloponnese, Rhodes); Eastern Aegean occupied islands face same climate regardless of political control.
- **Portugal**: Alentejo/Algarve desertification; 2017-scale megafires as norm; eucalyptus monoculture replacement; Tagus/Sado/Algarve sea-level exposure.
- **Cyprus**: Limassol/Larnaca/Famagusta 0.3-0.5m sea-level; Nicosia 40-42°C inland heat; water scarcity existential (no rivers, desalination dependent, rainfall declining).
- **Malta**: Highest EU sea-level exposure per land area; Grand Harbour/Sliema/airport threat; 38-40°C summer heat; water entirely desalination-dependent.
- **Croatia/Slovenia**: Dalmatian coast heat disruption; Dubrovnik historic infrastructure sea-level exposure; Alpine Julian Alps glacier retreat; flash flood risk.
- **Serbia**: Continental heatwave frequency; Danube flow reduction; Vojvodina agricultural stress; landlocked — no sea-level exposure.
- **Bosnia-Herzegovina**: Dinaric atmospheric river flash flood risk; coal-energy carbon border adjustment tension.

## Deviations from Plan

None — plan executed exactly as written. All must_haves satisfied.

## Verification Results

- `grep -c "Meloni\|FdI\|far-right" culture.md` → 3 ✓
- `grep -c "Catalan\|Basque" culture.md` → 2 ✓
- `grep -c "Orthodox\|Muslim" culture.md` → 22 ✓
- `grep -c "desertification\|semi-arid" climate.md` → 9 ✓
- `grep -c "wildfire\|fire regime" climate.md` → 9 ✓
- `grep -c "sea-level\|Malta\|Cyprus" climate.md` → 12 ✓
- `grep -c "medicane\|45.*°C\|48.*°C" climate.md` → 3 ✓

## Self-Check: PASSED

- culture.md modified and committed: `3cfdf29` ✓
- climate.md modified and committed: `3cfdf29` ✓
- All required references present (Meloni/FdI, Catalan/Basque, Orthodox/Muslim, desertification, wildfire, sea-level Malta/Cyprus, medicanes) ✓
