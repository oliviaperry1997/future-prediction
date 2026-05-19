# Phase 1: Foundation & Methodology - Context

**Gathered:** 2026-05-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Establish the operational Obsidian vault with YAML frontmatter schemas, directory layout, Dataview query templates, counter-scenario document, prediction register, and cross-domain consistency mechanism. All subsequent forecasting phases build on this foundation.

</domain>

<decisions>
## Implementation Decisions

### Vault Location & Directory Layout

- **D-01:** In-repo vault — `.obsidian/` lives inside the `future-prediction` repo directory (at `/Users/oliviaperry/Documents/Coding/Projects/future-prediction`). Keeps everything in one place with the project.
- **D-02:** Flat per-milestone structure — each milestone gets a top-level folder. Nesting is shallow: `./templates/`, `./meta/`, `./sources/`, `./2026-2050-transition/`, `./2050-snapshot/`, `./2075-snapshot/`, `./2100-snapshot/`.
- **D-03:** Supporting directories at root: `/templates` (YAML frontmatter templates), `/meta` (prediction register, consistency checks, index), `/sources` (reference materials), plus root `index.md`.

### YAML Frontmatter Schemas

- **D-04:** Shared base schema across all document types. Required fields: `title`, `status` (draft/review/final), `created`, `updated`. Optional: `tags`.
- **D-05:** Domain documents extend the base with: `domain` (borders/climate/tech/economy/demographics/culture), `milestone` (2050/2075/2100).
- **D-06:** Prediction entries extend the base with: `confidence` (HIGH/MEDIUM/LOW), `target_milestone`, `falsifiable_statement`, `domain`, `doc_ref` (links to the domain doc this prediction belongs to).
- **D-07:** Counter-scenario extends the base with: `alternative_thesis`, `divergence_points`.

### Prediction Register

- **D-08:** Individual prediction notes — each prediction is its own `.md` file in `/meta/predictions/` with YAML frontmatter. Enables Dataview to query and aggregate across any dimension.
- **D-09:** Three-tier confidence scale with written criteria:
  - **HIGH:** Strong evidence across multiple domains, consistent with established trends
  - **MEDIUM:** Plausible with supporting logic, some uncertainty
  - **LOW:** Speculative but worth tracking; single line of evidence or contrarian signal
- **D-10:** Each prediction includes a `doc_ref` field linking to the domain doc it relates to, enabling cross-domain traceability.

### Counter-Scenario

- **D-11:** Single structured document at `/meta/counter-scenario.md`.
- **D-12:** Thesis — a "clean revolution" path: revolutionary movements gain enough strength to overcome reactionary insurgencies nationwide, consolidating as a single socialist state. This contrasts with the primary scenario's region-by-region fragmentation. The doc covers: thesis statement, key divergence points, domain-by-domain implications, and likelihood assessment.

### Dataview Queries

- **D-13:** Full dashboard — views for: confidence sort (predictions ordered by confidence descending), milestone sort (predictions grouped by target milestone), domain filter (predictions by STEEP domain), status filter (active/retired/confirmed), recently added.

### Cross-Domain Consistency

- **D-14:** Dataview + manual review process. A `/meta/consistency-check.md` uses Dataview queries to surface cross-domain claims grouped by domain and `doc_ref`. The author reviews flagged items during each milestone finalization. No automated enforcement — the author is the consistency engine.

### the agent's Discretion

- Exact milestone folder naming conventions and file naming patterns
- Template styling and YAML layout details
- Dataview query implementation syntax (exact DQL queries)
- Consistentency check review cadence
- Root `index.md` content and level of detail
- `.gitignore` additions for `.obsidian/` if needed

</decisions>

<specifics>
## Specific Ideas

- Counter-scenario is a "clean revolution" thesis — revolutions win nationwide, single socialist state emerges
- Dataview's aggregation capabilities are the preferred querying mechanism
- Flat directory structure preferred — this is a single-author project; deep nesting adds navigation overhead without benefit
- The `doc_ref` field on predictions enables the cross-domain consistency mechanism to function

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` — Phase 1 requirements (FOUND-01 through FOUND-04) and acceptance criteria
- `.planning/ROADMAP.md` — Phase 1 goal, success criteria, domain descriptions, and success criteria for what must be TRUE

### Project Foundation
- `.planning/PROJECT.md` — Project vision, core value, constraints, and key decisions table

No external specs — requirements are fully captured in the documents above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- The author has an existing Obsidian vault at `/Users/oliviaperry/Documents/Human Futures/` — this is a separate project (interplanetary forecasting) but shows established Obsidian familiarity
- Multiple KML files in Downloads demonstrate comfort with Google Earth mapping workflows
- Dataview plugin is not yet installed in this project's vault but is the intended query mechanism

### Established Patterns
- Author works with structured markdown content organized by domain (the Human Futures vault has directories for Geopolitics, Science and Technology, Socioeconomics, etc.)
- `.planning/` uses YAML-frontmatter-free markdown for planning docs; the vault will introduce YAML frontmatter to content docs

### Integration Points
- Phase 1 creates the vault directory structure at the repo root. All subsequent phases write content into milestone directories within this vault.
- Prediction register entries created in Phase 1 serve as the tracking mechanism for predictions made in phases 2–5.
- The counter-scenario document created in Phase 1 is referenced by transition and snapshot phases for alternative-path analysis.

</code_context>

<deferred>
## Deferred Ideas

- **Prediction register review and calibration tracking** — periodic review of prediction accuracy and recalibration of confidence labels. Future methodology phase.
- **Synthesis and retrospective across all milestones** — end-to-end analysis after all milestones are written. Future phase or phase zero retrospective.
- **KML tooling improvements** (confidence-encoded polygon opacity, NetworkLink modular KML, shared style library) — tracked in REQUIREMENTS.md v2.
- None — discussion stayed within Phase 1 scope.

</deferred>

---

*Phase: 01-foundation-methodology*
*Context gathered: 2026-05-19*
