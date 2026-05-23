# Phase 2: 2026-2050 Transition - Context

**Gathered:** 2026-05-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Write a big-picture trends document covering the causal arc from present day to 2050, with specific dates for at least 10 major inflection points, driver analysis across all six STEEP domains (borders, climate, technology, economy, demographics, culture), and cross-domain feedback loops between at least three domain pairs. Open uncertainties flagged with confidence labels. The document covers the causal path (2026 through end of 2049); the 2050 steady-state description belongs to Phase 3.

</domain>

<decisions>
## Implementation Decisions

### Document Structure & Organization

- **D-01:** Hybrid document structure — timeline introduction with ALL key inflection events in sequence, followed by domain-by-domain sections that elaborate on each.
- **D-02:** Timeline section covers all 10+ inflection events in chronological order. Domain sections then expand on each domain's arc with deeper analysis.
- **D-03:** Domain sections reference timeline events via event IDs (T-01, T-02, etc.) in parentheses — machine-readable for Phase 3-5 cross-referencing.
- **D-04:** Each domain section follows a consistent template: key events (with ID refs), driver analysis, cross-domain effects, known uncertainties with confidence.

### Inflection Point Format

- **D-05:** Inflection points presented in a structured table with columns: ID, Date, Event, Description, Impact (STEEP domains affected), Confidence, See Prediction.
- **D-06:** Both cross-domain and domain-specific inflection points qualify as "major" — threshold is significance within the project's thesis, not exclusively multi-domain scope.
- **D-07:** Per-event confidence column in the timeline table (HIGH/MEDIUM/LOW).
- **D-08:** Timeline table includes a "See prediction" column linking each event to relevant prediction register entries in `meta/predictions/`.

### Depth of Driver Analysis

- **D-09:** Full section per domain (approximately 2-3 pages each).
- **D-10:** 4-6 key drivers identified per domain.
- **D-11:** Templated driver entries — each driver includes: description, timeline (how it unfolds 2026-2049), linked inflection events, cross-domain effects, confidence label.
- **D-12:** Dedicated cross-domain analysis section synthesizing feedback loops across domain pairs (at least 3 domain pairs with explicit mapping), placed after all 6 domain sections.

### Handoff to Phase 3

- **D-13:** No explicit "2050 state-of-play" summary section. Phase 3 derives the 2050 end-state by reading the full transition doc.
- **D-14:** Writing the transition doc includes creating new prediction register entries with `doc_ref` linking back to the transition doc sections (predictions go in `meta/predictions/`).
- **D-15:** No KML cross-reference markers in the transition doc — those belong in Phase 3-4 when 2050 boundaries are defined.

### Confidence Labeling

- **D-16:** Inline confidence badges throughout — e.g., "US dissolution (HIGH)", "carbon taxes (MEDIUM)".
- **D-17:** Existing 3-tier scale from Phase 1, unchanged: HIGH (strong multi-domain evidence), MEDIUM (plausible with supporting logic), LOW (speculative, single line of evidence).
- **D-18:** Confidence labels applied to both inflection events (in timeline table) and driver trajectories (in domain sections).

### Scope Boundary vs Phase 3

- **D-19:** Phase 2 covers the causal arc (how we got from 2026 to 2050). Phase 3 describes what the 2050 world looks like. No steady-state description in Phase 2.
- **D-20:** Driver sections describe trajectory only — they trace how each driver unfolds through 2049 but do not project the 2050 end-state outcome. Phase 3 determines 2050 outcomes independently from the same trajectory.
- **D-21:** Timeline cutoff is end of 2049. Last inflection points can land in late 2049. The 2050 state is Phase 3 territory.
- **D-22:** Cross-domain synthesis section maps pure feedback loops (which domains affect which, with what intensity and timing). No 2050 projection included.

### the agent's Discretion

- File naming conventions for the transition document and its sub-files
- Exact Obsidian callout formatting for confidence annotations
- Specific database field names in structured table columns (beyond the agreed columns)
- Driver breakdown granularity within each domain (within the 4-6 count)
- Implementation of event ID numbering scheme

</decisions>

<specifics>
## Specific Ideas

- Each timeline event should feel like a significant historical inflection — events that would be taught in future history classes
- Confidence labels should be scannable at a glance; inline text like "(HIGH)" is the baseline pattern
- The timeline table being machine-readable with event IDs enables Phase 3-5 to cross-reference without re-reading the full document
- Domain sections should be self-standing enough that each could be read independently, while still referencing the shared timeline

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` — Phase 2 requirements (TRAN-01, TRAN-02) and acceptance criteria
- `.planning/ROADMAP.md` — Phase 2 goal, success criteria, and boundary
- `.planning/PROJECT.md` — Project vision, core value, constraints, central thesis

### Prior Phase Context
- `.planning/phases/01-foundation-methodology/01-CONTEXT.md` — All 14 prior decisions (YAML schemas, prediction register format, confidence scale definitions) — especially D-04 through D-10 for frontmatter schemas and prediction format, D-09 for confidence scale criteria

### Existing Vault Assets
- `index.md` — Project index linking to all milestone directories
- `templates/domain-doc.md` — Domain document YAML frontmatter template
- `templates/prediction.md` — Prediction entry YAML frontmatter template
- `meta/predictions/` — Existing 6 prediction entries with confidence labels and doc_refs
- `meta/dashboard.md` — Dataview dashboard (5 views) for prediction queries
- `meta/counter-scenario.md` — "Clean revolution" alternative thesis

No external specs — requirements are fully captured in the project documents above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **YAML frontmatter schemas** (`templates/domain-doc.md`, `templates/prediction.md`) — ready to use for transition doc metadata and new predictions
- **Prediction register** (`meta/predictions/`) — 6 existing predictions; the transition doc should create new entries with confidence labels and `doc_ref` linking to transition doc sections
- **Dataview dashboard** (`meta/dashboard.md`) — existing 5 views; new predictions appear automatically
- **Counter-scenario doc** (`meta/counter-scenario.md`) — "clean revolution" thesis should be referenced where the transition line diverges
- **Existing predictions relevant to Phase 2 domain:** prediction-001 (US dissolution), prediction-002 (socialist transition), prediction-003 (climate displacement), prediction-004 (AI governance), prediction-005 (UN reconfiguration), prediction-006 (Great Lakes desiccation)
- **Milestone directory** `2026-2050-transition/` already exists at repo root (empty)

### Established Patterns
- Flat directory structure — documents sit at milestone level (e.g., `2026-2050-transition/`), avoid deep nesting
- Domain-organized content — Phase 1 pattern carries forward; domain sections in the transition doc align with existing domain docs in `2050-snapshot/`
- YAML frontmatter on all content docs — the transition doc itself and any sub-docs should include frontmatter using the base template
- Confidence scale from Phase 1 (HIGH/MEDIUM/LOW) — consistent use across all project documents

### Integration Points
- **Phase 1** → The transition doc should reference existing predictions by ID. New predictions created here feed the prediction register and dashboard.
- **Phase 3** → Domain sections in the transition doc provide the trajectory context for Phase 3's 2050 snapshot. Event IDs enable cross-referencing.
- **Phase 5** → While KML markers don't go in this doc, events with geographic/border implications should be identifiable for Phase 5 extraction.

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within Phase 2 scope.

</deferred>

---

*Phase: 02-2026-2050-transition*
*Context gathered: 2026-05-20*
