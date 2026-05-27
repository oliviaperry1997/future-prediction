# Roadmap: Future Prediction

## Overview

A markdown-based geopolitical forecasting and world-building project. This roadmap covers v1 — establishing the Obsidian vault methodology, writing the 2026-2050 transition document, producing the full 2050 snapshot across six STEEP domains (borders, climate, technology, economy, demographics, culture), and creating KML map files for the 2050 world in Google Earth Pro — followed by v1.1, a region-by-region plausibility audit of the Eurasia, Oceania, and Antarctica regions. Each phase delivers a complete, usable layer of the project: foundation first, then causal arc, then structural snapshot, then socioeconomic snapshot, then geographic instantiation, then regional verification.

## Phases

- [ ] **Phase 1: Foundation & Methodology** - Establish Obsidian vault, YAML templates, Dataview queries, counter-scenario document, prediction register, and cross-domain consistency mechanism
- [x] **Phase 2: 2026-2050 Transition** - Write the big-picture trends document with specific dates, driver analysis, and inflection points covering 2026-2050 (completed 2026-05-19)
- [x] **Phase 3: 2050 Structural Snapshot** - Document the geopolitical, climate, and technology landscape of the 2050 world (completed 2026-05-19)
- [x] **Phase 4: 2050 Socioeconomic Snapshot** - Document the economy, demographics, and culture of the 2050 world with cross-references (completed 2026-05-21)
- [ ] **Phase 5: 2050 KML Maps & Integration** - Produce KML map files for the 2050 world, cross-reference to markdown sections, and finalize 2050 index
- [x] **Phase 6: Central Asia Review** — Plausibility audit: Central Asia (completed 2026-05-27)
- [ ] **Phase 7: Eastern Asia Review** — Plausibility audit: Eastern Asia
- [ ] **Phase 8: Eastern Europe Review** — Plausibility audit: Eastern Europe
- [ ] **Phase 9: Northern Europe Review** — Plausibility audit: Northern Europe
- [ ] **Phase 10: Southeast Asia Review** — Plausibility audit: Southeast Asia
- [ ] **Phase 11: Southern Asia Review** — Plausibility audit: Southern Asia
- [ ] **Phase 12: Southern Europe Review** — Plausibility audit: Southern Europe
- [ ] **Phase 13: Western Asia Review** — Plausibility audit: Western Asia
- [ ] **Phase 14: Western Europe Review** — Plausibility audit: Western Europe
- [ ] **Phase 15: Australasia Review** — Plausibility audit: Australasia
- [ ] **Phase 16: Melanesia Review** — Plausibility audit: Melanesia
- [ ] **Phase 17: Micronesia Review** — Plausibility audit: Micronesia
- [ ] **Phase 18: Polynesia Review** — Plausibility audit: Polynesia
- [ ] **Phase 19: Antarctica Review** — Plausibility audit: Antarctica

## Phase Details

### Phase 1: Foundation & Methodology
**Mode**: mvp
**Goal**: Author has an operational Obsidian vault with methodological guardrails in place for bias-resistant forecasting
**Depends on**: Nothing (first phase)
**Requirements**: FOUND-01, FOUND-02, FOUND-03, FOUND-04
**Success Criteria** (what must be TRUE):
  1. Vault directory structure exists with ready-to-use YAML frontmatter templates for domain documents (STEEP domains, prediction register entries, counter-scenario entries)
  2. Author can create a new domain document from template and populate YAML metadata (frontmatter schema validated)
  3. Dataview query exists that surfaces all predictions sorted by confidence level and target milestone date
  4. Counter-scenario document exists with a structured alternative to the primary US-collapse/socialist-transition thesis, written in comparable depth
  5. Prediction register contains at least 5 initial falsifiable claims with confidence labels (HIGH/MEDIUM/LOW) and target milestone dates
**Plans**: 3 plans

Plans:
- [x] 01-01-PLAN.md — Vault Init & Templates (Wave 1)
- [x] 01-02-PLAN.md — Prediction Register & Counter-Scenario (Wave 2, blocked on 01)
- [x] 01-03-PLAN.md — Dataview Dashboard & Consistency (Wave 2, blocked on 01)

**Cross-cutting constraints:**
- Plan 01 depends on `must_haves.truths`: "Author can open the project as an Obsidian vault", "YAML frontmatter schemas exist for all document types"
- Plans 02 and 03 share `must_haves.truths`: "Author can create content using templates", "Dataview queries can read YAML frontmatter"

### Phase 2: 2026-2050 Transition
**Mode**: mvp
**Goal**: Author has a complete causal narrative connecting present day to 2050, grounded in the structural forces and the project's central thesis
**Depends on**: Phase 1
**Requirements**: TRAN-01, TRAN-02
**Success Criteria** (what must be TRUE):
   1. Transition document covers the full 2026-2050 timeline with specific dates for at least 10 major inflection points and transitional events
   2. Document includes driver analysis across all six STEEP domains (borders, climate, technology, economy, demographics, culture)
   3. Cross-domain feedback loops are identified and described between at least three domain pairs
   4. Open uncertainties are explicitly flagged with confidence labels (HIGH/MEDIUM/LOW) where appropriate
**Plans**: 4 plans

Plans:
- [x] 02-01-PLAN.md — Timeline Framework (Wave 1) — Create transition index and 14-event timeline table with T-IDs
- [x] 02-02-PLAN.md — Structural Domains (Wave 2) — Write borders, climate, technology domain sections with 4-5 drivers each
- [x] 02-03-PLAN.md — Socioeconomic Domains (Wave 2) — Write economy, demographics, culture domain sections with 4-5 drivers each
- [x] 02-04-PLAN.md — Synthesis & Predictions (Wave 3) — Write cross-domain synthesis (5 domain pairs), create 5 new prediction entries, update index

**Cross-cutting constraints:**
- Plan 01 defines event IDs (T-01 through T-14) that all domain sections must reference
- Plans 02 and 03 are parallel (Wave 2) — different files, no conflict
- Plan 04 depends on Plans 02 and 03 (consumes their domain content for synthesis)
- All plans: trajectory-only language per D-19/D-20, no 2050 steady-state descriptions, no KML markers per D-15

### Phase 3: 2050 Structural Snapshot — Borders, Climate & Technology
**Mode**: mvp
**Goal**: Author has documented the structural landscape (borders, climate, technology) of the 2050 world, providing the constraining framework for socioeconomic domains
**Depends on**: Phase 2
**Requirements**: BORD-01, BORD-02, CLIM-01, CLIM-02, TECH-01, TECH-02
**Success Criteria** (what must be TRUE):
   1. Geopolitical landscape document describes sovereign entities, border changes, and power blocs as of 2050 with specific detail, consistent with the collapse/socialist transition thesis
   2. Specific border shifts are detailed and internally consistent (e.g., which new entities emerge, which dissolve, where blocs form)
   3. Climate document describes the state of the climate system (temperature, sea level, extreme events) and major environmental changes with their geopolitical impacts
   4. Climate-driven migration patterns and resource conflicts are identified and linked to the border/geopolitical analysis
   5. Technology document covers transformative technologies (energy systems, AI, biotechnology) and their societal impacts, with implications for the economic and demographic domains
**Plans**: 3 plans

Plans:
- [x] 03-01-PLAN.md — Borders & Geopolitics + Micro Verfication (Wave 1) — Create 2050 index, borders snapshot with territorial integrity verification
- [x] 03-02-PLAN.md — Climate Snapshot (Wave 2, parallel) — Create climate snapshot with migration and resource conflict analysis
- [x] 03-03-PLAN.md — Technology Snapshot (Wave 2, parallel) — Create technology snapshot across all transformative tech domains

### Phase 4: 2050 Socioeconomic Snapshot — Economy, Demographics & Culture
**Mode**: mvp
**Goal**: Author has documented the socioeconomic landscape (economy, demographics, culture) of the 2050 world, building on the structural constraints from Phase 3
**Depends on**: Phase 3
**Requirements**: ECON-01, ECON-02, DEMO-01, DEMO-02, CULT-01
**Success Criteria** (what must be TRUE):
  1. Economic document describes the global economic structure, dominant systems, trade patterns, economic blocs, and the transition from capitalist to socialist economic organization as of 2050
  2. Demographic document describes population distributions, migration patterns, urbanization trends, and identifies population decline/boom regions with their geopolitical implications
  3. Culture document describes the ideological landscape, dominant belief systems, cultural shifts, and identity structures as of 2050
  4. All five domain documents include `→ See KML:` cross-reference markers linking specific claims to intended map features
  5. Domain documents are mutually consistent (no contradictions between economic assumptions and demographic constraints, etc.)
**Plans**: TBD

### Phase 5: 2050 KML Maps & Integration
**Mode**: mvp
**Goal**: Author has a complete, navigable 2050 world map in Google Earth Pro with bidirectional cross-references between markdown analysis and KML polygons
**Depends on**: Phase 4
**Requirements**: BORD-03, KMLP-01, KMLP-02
**Success Criteria** (what must be TRUE):
  1. KML map files for the 2050 world exist (at minimum, a borders/geopolitics layer) with geopolitical boundaries displayed as polygons
  2. KML files open correctly in Google Earth Pro and display the 2050 geopolitical landscape
  3. Each KML polygon entry includes a `See:` cross-reference back to the specific markdown section that justifies that boundary change
  4. All border descriptions in domain documents are consistent with KML map polygons (no border described in markdown that contradicts the map)
  5. 2050/index.md exists as a navigable entry point linking to all six domain documents and the KML map descriptions
**Plans**: 3 plans

Plans:
- [x] 05-01-PLAN.md — KML Generation Script & Source Data Pipeline (Wave 1)
- [x] 05-02-PLAN.md — Generate All 6 KML Files (Wave 2)
- [ ] 05-03-PLAN.md — Verification & Index Finalization (Wave 3)

**Cross-cutting constraints:**
- Plan 01 defines the generation script and config that Plans 02 and 03 depend on
- Plan 02 is the core deliverable (all KML files)
- Plan 03 has a human-verify checkpoint — user must open KMLs in Google Earth Pro
- Per D-06: 2050 KMLs are separate files loaded alongside Earth Current.kml, not modifications of it
- Per D-19: Programmatic generation with user refinement — script generates, user adjusts in Google Earth Pro

### Phase 6: Central Asia Review
**Mode**: mvp
**Goal**: Central Asia (Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Uzbekistan) plausibility verified, KML issues fixed, CAC documentation gaps filled
**Depends on**: Phase 5
**Requirements**: EURA-01
**Success Criteria** (what must be TRUE):
  1. All 5 Central Asian CAC constituent entities assessed against revolutionary feedback loop and established dynamics — no contradictions
  2. KML entities for Central Asia open correctly in Google Earth Pro with correct boundaries (exclave holes, no wip, Afghanistan removed)
  3. All documentation gaps for CAC entities identified and filled (See KML markers, economy/demographics/culture/climate profiles, borders doc entry)
**Plans**: 4 plans

Plans:
- [x] 06-01-PLAN.md — KML Edits: exclave holes, (wip) removal, Afghanistan relocation (Wave 1)
- [x] 06-02-PLAN.md — Borders-geopolitics CAC entity entry (Wave 1, parallel with 01)
- [x] 06-03-PLAN.md — Economy & Demographics CAC profiles (Wave 2, blocked on 02)
- [x] 06-04-PLAN.md — Culture & Climate CAC profiles (Wave 2, blocked on 02, parallel with 03)

**Cross-cutting constraints:**
- Afghanistan deferred to Phase 11 (Southern Asia Review) per D-13; KML entity removed from Central Asia folder
- Ferghana Valley exclaves need interior polygon holes per D-11
- All CAC constituent profiles follow standard format (matching Russia/Turkey/India depth) per D-07
- (wip) tag removal from Eurasia/Central Asia KML folders signals region reviewed per D-10
- D-15 framework gap (revolutionary feedback loop doc needs update) is out of scope for this phase

### Phase 7: Eastern Asia Review
**Mode**: mvp
**Goal**: Eastern Asia (China, Japan, Mongolia, ROK, DPRK) plausibility verified — Korea recalibrated from unified 40% scenario to two-Koreas 60% scenario — KML issues fixed, documentation gaps filled across all 6 STEEP domains
**Depends on**: Phase 6
**Requirements**: EURA-02
**Success Criteria** (what must be TRUE):
  1. All 5 Eastern Asian entities assessed against revolutionary feedback loop and established dynamics — no contradictions
  2. ROK (reactionary degradation) and DPRK (revolutionary ascendancy) replace Unified Korea across all domain docs, KML, and entity config
  3. KML entities for Eastern Asia open correctly in Google Earth Pro with correct boundaries
  4. All documentation gaps filled: Japan/Mongolia/ROK/DPRK profiles added to economy, demographics, culture, climate; China profiles expanded
**Plans**: 4 plans

Plans:
- [x] 07-01-PLAN.md — KML Edits: (wip) removal, entity-config ROK/DPRK, China HKG+TWN, Korea rename (Wave 1)
- [ ] 07-02-PLAN.md — Borders-geopolitics: Mongolia entry, ROK+DPRK replacement, China update, Territorial Integrity (Wave 1, parallel with 01)
- [ ] 07-03-PLAN.md — Economy & Demographics profiles: Japan, Mongolia, ROK, DPRK + expanded China (Wave 2, blocked on 02)
- [ ] 07-04-PLAN.md — Culture & Climate: Japan, Mongolia, ROK, DPRK cultural profiles + expanded Eastern Asia climate (Wave 2, blocked on 02, parallel with 03)

**Cross-cutting constraints:**
- Plans 01 and 02 are parallel (Wave 1) — KML edits and borders-geopolitics don't conflict
- Plans 03 and 04 are parallel (Wave 2) — different domain docs, no file conflicts
- Plan 02 must complete first (defines entity names and narratives that 03/04 reference)
- All plans: Unified Korea removed everywhere, replaced with ROK (reactionary degradation) + DPRK (revolutionary ascendancy) per D-01
- Korea recalibration (40% → 60% scenario) affects every domain document cross-reference

### Phase 8: Eastern Europe Review
**Mode**: mvp
**Goal**: Eastern Europe (Belarus, Bulgaria, Czechia, Hungary, Moldova, Poland, Romania, Russia, Slovakia, Ukraine) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 7
**Requirements**: EURA-03
**Success Criteria** (what must be TRUE):
  1. All 10 Eastern European entities assessed — no contradictions
  2. KML entities for Eastern Europe correct in Google Earth Pro
  3. All documentation gaps for Eastern European entities identified and filled

### Phase 9: Northern Europe Review
**Mode**: mvp
**Goal**: Northern Europe (Denmark, Estonia, Finland, Iceland, Ireland, Latvia, Lithuania, Norway, Sweden, United Kingdom) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 8
**Requirements**: EURA-04
**Success Criteria** (what must be TRUE):
  1. All 10 Northern European entities assessed — no contradictions
  2. KML entities for Northern Europe correct in Google Earth Pro
  3. All documentation gaps for Northern European entities identified and filled

### Phase 10: Southeast Asia Review
**Mode**: mvp
**Goal**: Southeast Asia (Brunei, Cambodia, East Timor, Indonesia, Laos, Malaysia, Myanmar, Philippines, Singapore, Thailand, Vietnam) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 9
**Requirements**: EURA-05
**Success Criteria** (what must be TRUE):
  1. All 11 Southeast Asian entities assessed — no contradictions
  2. KML entities for Southeast Asia correct in Google Earth Pro
  3. All documentation gaps for Southeast Asian entities identified and filled

### Phase 11: Southern Asia Review
**Mode**: mvp
**Goal**: Southern Asia (Bangladesh, Bhutan, India, Maldives, Nepal, Pakistan, Sri Lanka) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 10
**Requirements**: EURA-06
**Success Criteria** (what must be TRUE):
  1. All 7 Southern Asian entities assessed — no contradictions
  2. KML entities for Southern Asia correct in Google Earth Pro
  3. All documentation gaps for Southern Asian entities identified and filled

### Phase 12: Southern Europe Review
**Mode**: mvp
**Goal**: Southern Europe (Albania, Bosnia, Croatia, Cyprus, Greece, Italy, Kosovo, Malta, Montenegro, North Macedonia, Portugal, Serbia, Slovenia, Spain, Turkey) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 11
**Requirements**: EURA-07
**Success Criteria** (what must be TRUE):
  1. All 15 Southern European entities assessed — no contradictions
  2. KML entities for Southern Europe correct in Google Earth Pro
  3. All documentation gaps for Southern European entities identified and filled

### Phase 13: Western Asia Review
**Mode**: mvp
**Goal**: Western Asia (Bahrain, Iran, Iraq, Israel, Jordan, Kuwait, Lebanon, Oman, Palestine, Qatar, Saudi Arabia, Syria, UAE, Yemen) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 12
**Requirements**: EURA-08
**Success Criteria** (what must be TRUE):
  1. All 14 Western Asian entities assessed — no contradictions
  2. KML entities for Western Asia correct in Google Earth Pro
  3. All documentation gaps for Western Asian entities identified and filled

### Phase 14: Western Europe Review
**Mode**: mvp
**Goal**: Western Europe (Austria, Belgium, France, Germany, Luxembourg, Netherlands, Switzerland, plus European Union-level entities) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 13
**Requirements**: EURA-09
**Success Criteria** (what must be TRUE):
  1. All Western European entities assessed — no contradictions
  2. KML entities for Western Europe correct in Google Earth Pro
  3. All documentation gaps for Western European entities identified and filled

### Phase 15: Australasia Review
**Mode**: mvp
**Goal**: Australasia (Australia, New Zealand) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 14
**Requirements**: OCEA-01
**Success Criteria** (what must be TRUE):
  1. Both Australasian entities assessed — no contradictions
  2. KML entities for Australasia correct in Google Earth Pro
  3. All documentation gaps for Australasian entities identified and filled

### Phase 16: Melanesia Review
**Mode**: mvp
**Goal**: Melanesia (Fiji, Kanaky, Papua New Guinea, Solomon Is., Vanuatu) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 15
**Requirements**: OCEA-02
**Success Criteria** (what must be TRUE):
  1. All 5 Melanesian entities assessed — no contradictions
  2. KML entities for Melanesia correct in Google Earth Pro
  3. All documentation gaps for Melanesian entities identified and filled

### Phase 17: Micronesia Review
**Mode**: mvp
**Goal**: Micronesia (Guam, Kiribati, Marshall Is., Micronesia, Nauru, Palau) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 16
**Requirements**: OCEA-03
**Success Criteria** (what must be TRUE):
  1. All 6 Micronesian entities assessed — no contradictions
  2. KML entities for Micronesia correct in Google Earth Pro
  3. All documentation gaps for Micronesian entities identified and filled

### Phase 18: Polynesia Review
**Mode**: mvp
**Goal**: Polynesia (Cook Is., Maohi Nui, Niue, Samoa, Tonga, Tuvalu) plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 17
**Requirements**: OCEA-04
**Success Criteria** (what must be TRUE):
  1. All 6 Polynesian entities assessed — no contradictions
  2. KML entities for Polynesia correct in Google Earth Pro
  3. All documentation gaps for Polynesian entities identified and filled

### Phase 19: Antarctica Review
**Mode**: mvp
**Goal**: Antarctica plausibility verified, KML issues fixed, documentation gaps filled
**Depends on**: Phase 18
**Requirements**: ANTA-01
**Success Criteria** (what must be TRUE):
  1. Antarctica entity assessed against established dynamics — no contradictions
  2. KML entity for Antarctica correct in Google Earth Pro
  3. All documentation gaps for Antarctica identified and filled

## Progress

**Execution Order:** Phases execute in numeric order: 1 → 2 → ... → 19

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Methodology | 3/3 | Complete | 2026-05-19 |
| 2. 2026-2050 Transition | 4/4 | Complete | 2026-05-19 |
| 3. 2050 Structural Snapshot | 3/3 | Complete | 2026-05-19 |
| 4. 2050 Socioeconomic Snapshot | 4/4 | Complete | 2026-05-21 |
| 5. 2050 KML Maps & Integration | 2/3 | Paused | — |
| 6. Central Asia Review | 4/4 | Complete   | 2026-05-27 |
| 7. Eastern Asia Review | 0/4 | Planned | — |
| 8. Eastern Europe Review | — | Not started | — |
| 9. Northern Europe Review | — | Not started | — |
| 10. Southeast Asia Review | — | Not started | — |
| 11. Southern Asia Review | — | Not started | — |
| 12. Southern Europe Review | — | Not started | — |
| 13. Western Asia Review | — | Not started | — |
| 14. Western Europe Review | — | Not started | — |
| 15. Australasia Review | — | Not started | — |
| 16. Melanesia Review | — | Not started | — |
| 17. Micronesia Review | — | Not started | — |
| 18. Polynesia Review | — | Not started | — |
| 19. Antarctica Review | — | Not started | — |
