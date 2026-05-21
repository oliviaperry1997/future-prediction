# Roadmap: Future Prediction

## Overview

A markdown-based geopolitical forecasting and world-building project. This roadmap covers v1 — establishing the Obsidian vault methodology, writing the 2026-2050 transition document, producing the full 2050 snapshot across six STEEP domains (borders, climate, technology, economy, demographics, culture), and creating KML map files for the 2050 world in Google Earth Pro. Each phase delivers a complete, usable layer of the project: foundation first, then causal arc, then structural snapshot, then socioeconomic snapshot, then geographic instantiation.

## Phases

- [ ] **Phase 1: Foundation & Methodology** - Establish Obsidian vault, YAML templates, Dataview queries, counter-scenario document, prediction register, and cross-domain consistency mechanism
- [ ] **Phase 2: 2026-2050 Transition** - Write the big-picture trends document with specific dates, driver analysis, and inflection points covering 2026-2050
- [ ] **Phase 3: 2050 Structural Snapshot** - Document the geopolitical, climate, and technology landscape of the 2050 world
- [x] **Phase 4: 2050 Socioeconomic Snapshot** - Document the economy, demographics, and culture of the 2050 world with cross-references (completed 2026-05-21)
- [ ] **Phase 5: 2050 KML Maps & Integration** - Produce KML map files for the 2050 world, cross-reference to markdown sections, and finalize 2050 index

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

## Progress

**Execution Order:** Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Methodology | 3/3 | Complete | 2026-05-19 |
| 2. 2026-2050 Transition | 0/4 | Ready to execute | - |
| 3. 2050 Structural Snapshot | 0/0 | Not started | - |
| 4. 2050 Socioeconomic Snapshot | 4/4 | Complete   | 2026-05-21 |
| 5. 2050 KML Maps & Integration | 1/3 | In Progress|  |
