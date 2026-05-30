# Requirements: Future Prediction

**Defined:** 2026-05-19
**Core Value:** A coherent, grounded, internally consistent vision of how the world transforms between now and 2100, detailed enough to draw accurate maps at each quarter-century checkpoint.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Foundation & Methodology

- [ ] **FOUND-01**: Establish Obsidian vault with YAML frontmatter schemas, directory layout, and Dataview query templates
- [ ] **FOUND-02**: Create counter-scenario document describing alternative paths (e.g. US adapts, no socialist transition)
- [ ] **FOUND-03**: Implement prediction register tracking falsifiable claims with confidence levels per milestone
- [ ] **FOUND-04**: Build cross-domain consistency tool/mechanism that checks for contradictory assumptions across domain docs

### 2026-2050 Transition

- [ ] **TRAN-01**: Write big-picture trends document covering the causal arc from present day to 2050
- [ ] **TRAN-02**: Include specific dates for major inflection points and transitional events

### 2050 Snapshot — Borders & Geopolitics

- [ ] **BORD-01**: Describe the geopolitical landscape including sovereign entities, border changes, and power blocs as of 2050
- [ ] **BORD-02**: Detail specific border shifts consistent with the collapse/socialist transition thesis
- [x] **BORD-03**: Create KML polygons for 2050 world map

### 2050 Snapshot — Climate

- [ ] **CLIM-01**: Describe the state of the climate system, major environmental changes, and their geopolitical impacts as of 2050
- [ ] **CLIM-02**: Identify climate-driven migration patterns and resource conflicts

### 2050 Snapshot — Technology

- [ ] **TECH-01**: Describe the technological landscape, transformative technologies, and their societal impacts as of 2050
- [ ] **TECH-02**: Address energy systems, AI, biotechnology, and other relevant domains

### 2050 Snapshot — Economy

- [ ] **ECON-01**: Describe the global economic structure, dominant systems, trade patterns, and economic blocs as of 2050
- [ ] **ECON-02**: Detail the transition from capitalist to socialist economic organization

### 2050 Snapshot — Demographics

- [ ] **DEMO-01**: Describe population distributions, migration patterns, urbanization, and demographic trends as of 2050
- [ ] **DEMO-02**: Address population decline/boom regions and their geopolitical implications

### 2050 Snapshot — Culture & Ideology

- [ ] **CULT-01**: Describe the ideological landscape, dominant belief systems, cultural shifts, and identity structures as of 2050

### 2050 KML Maps

- [x] **KMLP-01**: Produce KML map files for the 2050 world map with geopolitical boundaries
- [x] **KMLP-02**: Ensure KML entries cross-reference the markdown sections that justify each boundary

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Later Milestones

- **SNAP-02**: 2075 snapshot with all 6 domains + KML maps
- **SNAP-03**: 2100 snapshot with all 6 domains + KML maps
- **TRAN-03**: 2051-2075 transition document
- **TRAN-04**: 2076-2100 transition document

### KML Tooling

- **KMLT-01**: Confidence-encoded polygon opacity on maps
- **KMLT-02**: NetworkLink modular KML architecture (domain-separated linked files)
- **KMLT-03**: Shared KML style library across milestones

### Methodology Additions

- **METH-01**: Prediction register review and calibration tracking
- **METH-02**: Synthesis and retrospective across all milestones

## v1.1 Requirements

Region-by-region plausibility audit for the 2050 snapshot. Each requirement covers three axes: (1) assess plausibility against established dynamics and the revolutionary feedback loop, (2) fix KML creation issues, (3) fill documentation gaps.

### Eurasia Review

- [ ] **EURA-01**: Central Asia — review complete (plausibility, KML, docs)
- [x] **EURA-02**: Eastern Asia — review complete
- [ ] **EURA-03**: Eastern Europe — review complete
- [ ] **EURA-04**: Northern Europe — review complete
- [x] **EURA-05**: Southeast Asia — review complete
- [ ] **EURA-06**: Southern Asia — review complete
- [x] **EURA-07**: Southern Europe — review complete
- [ ] **EURA-08**: Western Asia — review complete
- [x] **EURA-09**: Western Europe — review complete

### Oceania Review

- [x] **OCEA-01**: Australasia — review complete
- [x] **OCEA-02**: Melanesia — review complete
- [ ] **OCEA-03**: Micronesia — review complete
- [ ] **OCEA-04**: Polynesia — review complete

### Antarctica Review

- [ ] **ANTA-01**: Antarctica — review complete

## Out of Scope

| Feature | Reason |
|---------|--------|
| Year-by-year granular predictions | Pseudoprecision at century scale; big-picture trends only |
| Narrative prose / fiction-style writing | Structured analysis format preferred |
| Quantitative simulation models | Beyond scope; qualitative forecasting with structured reasoning |
| Public publishing or sharing | Solo project, no distribution infrastructure |
| Real-time collaboration | Solo project |
| Web map framework (CesiumJS, Mapbox) | Unnecessary server/API dependency; KML files for Google Earth Pro only |

## Traceability

### v1 (Phase 1-5)

| Requirement | Phase | Status |
|-------------|-------|--------|
| FOUND-01 | Phase 1 | Pending |
| FOUND-02 | Phase 1 | Pending |
| FOUND-03 | Phase 1 | Pending |
| FOUND-04 | Phase 1 | Pending |
| TRAN-01 | Phase 2 | Pending |
| TRAN-02 | Phase 2 | Pending |
| BORD-01 | Phase 3 | Pending |
| BORD-02 | Phase 3 | Pending |
| BORD-03 | Phase 5 | Complete |
| CLIM-01 | Phase 3 | Pending |
| CLIM-02 | Phase 3 | Pending |
| TECH-01 | Phase 3 | Pending |
| TECH-02 | Phase 3 | Pending |
| ECON-01 | Phase 4 | Pending |
| ECON-02 | Phase 4 | Pending |
| DEMO-01 | Phase 4 | Pending |
| DEMO-02 | Phase 4 | Pending |
| CULT-01 | Phase 4 | Pending |
| KMLP-01 | Phase 5 | Complete |
| KMLP-02 | Phase 5 | Complete |

**Coverage:**
- v1 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0 ✓

### v1.1 (Phase 6-19)

| Requirement | Phase | Status |
|-------------|-------|--------|
| EURA-01 | Phase 6 | Pending |
| EURA-02 | Phase 7 | Complete |
| EURA-03 | Phase 8 | Pending |
| EURA-04 | Phase 9 | Pending |
| EURA-05 | Phase 10 | Complete |
| EURA-06 | Phase 11 | Pending |
| EURA-07 | Phase 12 | Complete |
| EURA-08 | Phase 13 | Pending |
| EURA-09 | Phase 14 | Complete |
| OCEA-01 | Phase 15 | Complete |
| OCEA-02 | Phase 16 | Complete |
| OCEA-03 | Phase 17 | Pending |
| OCEA-04 | Phase 18 | Pending |
| ANTA-01 | Phase 19 | Pending |

**Coverage:**
- v1.1 requirements: 14 total
- Mapped to phases: 14
- Unmapped: 0 ✓

---

*Requirements defined: 2026-05-19*
*Last updated: 2026-05-27 — v1.1 milestone added*
