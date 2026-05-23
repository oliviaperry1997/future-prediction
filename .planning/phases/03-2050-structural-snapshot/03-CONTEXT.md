# Phase 3: 2050 Structural Snapshot — Context

**Gathered:** 2026-05-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Document the 2050 steady-state snapshot for three structural STEEP domains: borders/geopolitics, climate, and technology. Each domain document describes what the world *looks like* as of 2050, not the trajectory that got it there (that was Phase 2). Domain docs use `templates/domain-doc.md` as-is. Additionally, create `2050-snapshot/index.md` as the milestone entry point with navigation to all domain docs.

**Writing mode shift from Phase 2:** Phase 2 covered the causal arc (2026-2049 trajectory with driver analysis, T-IDs, inflection events). Phase 3 describes the 2050 *end-state* — present-tense snapshot language, not historical narrative. E.g., "The Pacific People's Republic governs ~55M citizens across the former West Coast" not "The Pacific states achieved de facto autonomy in 2034."

</domain>

<decisions>
## Implementation Decisions

### Writing Mode (from Phase 2 D-19, D-20, D-21, D-22)

- **D-19:** Phase 2 covers the causal arc. Phase 3 describes what the 2050 world looks like. No trajectory narrative in Phase 3 documents.
- **D-20:** Phase 3 determines 2050 outcomes independently from the Phase 2 trajectories. Internal consistency with Phase 2 is required, but Phase 3 does not re-narrate the transition.
- **D-22:** Cross-domain synthesis from Phase 2 provides the coupling analysis. Phase 3 domain docs reference each other for consistency but do not re-synthesize.

### Document Structure

- **D-23:** Domain docs use `templates/domain-doc.md` as-is, with 2050 steady-state content filling the sections.
- **D-24:** "Key Changes From Previous Milestone" section describes what changed during 2026-2049 (briefly, 3-5 bullets), establishing continuity with Phase 2 without re-narrating it.
- **D-25:** Predictions only created to fill gaps — no conflicts with existing 11 predictions allowed. Prediction-001 through prediction-011 already cover Phase 3 domains (borders: 3 predictions, climate: 2, technology: 2).
- **D-26:** `2050-snapshot/index.md` created in Plan 03-01 as the milestone entry point. Plans 03-02 and 03-03 update it when their domain docs are created.

### Territorial Integrity (Borders Domain)

- **D-27:** Every terrestrial region on Earth must be claimed by exactly one sovereign entity. No empty areas (except those explicitly documented as unclaimed/uninhabitable with rationale).
- **D-28:** No two entities claim the same territory. Overlaps explicitly prohibited.
- **D-29:** Antarctica is not assumed unclaimed — if partitioned or claimed, those claims must be documented. If left unclaimed, that must be a deliberate narrative choice with rationale.
- **D-30:** A `## Territorial Integrity` section and `## Coverage Cross-Check` table in the borders domain doc serve as the verification mechanism for D-27, D-28, D-29.

### Plan Split

- **D-31:** Phase 3 split into 3 plans (one per domain).
- **D-32:** Plan 03-01 (Wave 1): Borders & Geopolitics + index + territorial verification.
- **D-33:** Plans 03-02 and 03-03 (Wave 2, parallel): Climate and Technology respectively.
- **D-34:** Domain docs are written as 2050 steady-state snapshots — present-tense, describing the world as it exists in 2050.

### Handoff to Phase 4

- **D-35:** Phase 3 domain docs include `→ See also:` cross-references to socioeconomic domains (economy, demographics, culture) where structural constraints shape socioeconomic outcomes.
- **D-36:** Phase 3 includes `→ See KML:` markers (as in template) for future Phase 5 KML integration.

</decisions>

<specifics>
## Specific Ideas

- The borders doc should feel like a geopolitical atlas entry for 2050 — entity descriptions, territorial claims, capital cities, population ranges, government type
- The climate doc should read like a climate assessment report for 2050 — temperature anomalies, sea level, extreme event frequency, biome states
- The technology doc should describe what technologies are mature/depolyed by 2050, not what's emerging
- Territorial integrity table in borders doc: list every major world region + claiming entity, with a verification check that the list is exhaustive
- Existing predictions with doc_ref pointing to `2050-snapshot/domains/` should be updated to point to the actual files created here

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` — Phase 3 requirements (BORD-01, BORD-02, CLIM-01, CLIM-02, TECH-01, TECH-02)
- `.planning/ROADMAP.md` — Phase 3 goal, success criteria, and boundary
- `.planning/PROJECT.md` — Project vision, core value, constraints, central thesis

### Prior Phase Context
- `.planning/phases/02-2026-2050-transition/02-CONTEXT.md` — All Phase 2 decisions, especially D-13 through D-22 for the handoff boundary
- `.planning/phases/02-2026-2050-transition/02-02-PLAN.md` — Structural domain sections with driver analysis (trajectories consumed by Phase 3)
- `.planning/phases/02-2026-2050-transition/02-04-SUMMARY.md` — Phase 2 completion and handoff state

### Existing Vault Assets
- `2026-2050-transition/borders.md` — Borders trajectory with 5 drivers
- `2026-2050-transition/climate.md` — Climate trajectory with 5 drivers
- `2026-2050-transition/technology.md` — Technology trajectory with 5 drivers
- `2026-2050-transition/successor-states.md` — 19-entity successor state reference map
- `2026-2050-transition/timeline.md` — 14 inflection events (T-01 through T-14)
- `2050-snapshot/` — Target directory (to be created)
- `templates/domain-doc.md` — Domain document template (used as-is)
- `templates/prediction.md` — Prediction entry template
- `meta/predictions/` — 11 existing prediction entries
- `meta/dashboard.md` — Dataview dashboard
- `meta/counter-scenario.md` — Counter-scenario thesis

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Region files** in `2026-2050-transition/regions/` — 9 region files (North America, South America, Europe, Africa, Asia, West Asia, Oceania, Antarctica, Orbital Space, Moon) provide post-fragmentation regional descriptions that Phase 3 borders can reference for non-US territories
- **Successor states map** (`2026-2050-transition/successor-states.md`) — Complete listing of ~19 entities across former US territory with population estimates, government types, and economic baselines

### Established Patterns
- Flat milestone directory structure — docs sit at `2050-snapshot/` level
- Domain-organized by STEEP — `2050-snapshot/domains/` mirrors `2026-2050-transition/` structure
- YAML frontmatter on all documents with Dataview-compatible field syntax
- Confidence labels (HIGH/MEDIUM/LOW) used throughout

### Integration Points
- **Phase 3 → Phase 4:** Structural domains (borders, climate, technology) provide the constraining framework for socioeconomic domain docs (economy, demographics, culture) in Phase 4
- **Phase 3 → Phase 5:** `→ See KML:` markers in domain docs provide the specification for KML map polygons in Phase 5
- **Phase 2 → Phase 3:** Phase 2 trajectories provide the "how we got here" context; Phase 3 determines the 2050 end-state independently

</code_context>

<deferred>
## Deferred Ideas

- Phase 3 domain docs include `→ See KML:` markers per the template, but KML file creation is deferred to Phase 5. Markers act as forward references.
- Empty-area and overlap verification: automated script would be ideal but manual checklist is the mechanism for now (Phase 3 scope).

</deferred>

---

*Phase: 03-2050-structural-snapshot*
*Context gathered: 2026-05-21*
