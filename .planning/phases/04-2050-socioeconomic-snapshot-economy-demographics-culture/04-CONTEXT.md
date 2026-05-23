# Phase 4: 2050 Socioeconomic Snapshot — Economy, Demographics & Culture - Context

**Gathered:** 2026-05-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Document the 2050 steady-state snapshot for three socioeconomic STEEP domains: economy, demographics, and culture. Each domain doc uses `templates/domain-doc.md` as-is, describes what the world *looks like* as of 2050 (not the trajectory — that was Phase 2), and includes `→ See KML:` cross-reference markers per the template. Domain docs are mutually consistent — no contradictions between economic assumptions, demographic constraints, and cultural dynamics. Building on the structural framework established in Phase 3 (borders, climate, technology).

**Writing mode:** 2050 end-state — present-tense snapshot language, not historical narrative. Same as Phase 3.

</domain>

<specs>
## Locked Requirements (from REQUIREMENTS.md)

### ECON-01
Describe the global economic structure, dominant systems, trade patterns, and economic blocs as of 2050.

### ECON-02
Detail the transition from capitalist to socialist economic organization.

### DEMO-01
Describe population distributions, migration patterns, urbanization, and demographic trends as of 2050.

### DEMO-02
Address population decline/boom regions and their geopolitical implications.

### CULT-01
Describe the ideological landscape, dominant belief systems, cultural shifts, and identity structures as of 2050.

### Success Criteria (from ROADMAP.md)
1. Economic document describes the global economic structure, dominant systems, trade patterns, economic blocs, and the transition from capitalist to socialist economic organization as of 2050.
2. Demographic document describes population distributions, migration patterns, urbanization trends, and identifies population decline/boom regions with their geopolitical implications as of 2050.
3. Culture document describes the ideological landscape, dominant belief systems, cultural shifts, and identity structures as of 2050.
4. All five domain documents include `→ See KML:` cross-reference markers linking specific claims to intended map features.
5. Domain documents are mutually consistent (no contradictions between economic assumptions and demographic constraints, etc.).

</specs>

<decisions>
## Implementation Decisions

### Economy: Description Depth & Structure

- **D-01 (Hybrid structure):** Global architecture sections + entity-by-entity economic profiles covering ALL successor states. Not just high-impact entities — every successor state gets a profile.
- **D-02 (Sector-level profiles):** Per entity includes: GDP range, dominant sectors (manufacturing, services, energy, tech, agriculture), trade partners and bloc alignment, economic model (socialist-state-directed, social-democratic mixed, nationalist-capitalist, extractive), currency status, labor market character (automated, mixed, labor-intensive).
- **D-03 (Global financial architecture):** Both — a standalone overview section (1-2 pages) covering the BRICS+ alternative financial system, multicurrency reserve standard, post-dollar trade settlement, and digital basket currencies. Entity profiles and trade bloc sections then reference this architecture with entity-specific details.
- **D-04 (Labor & automation section):** Dedicated standalone section on employment structures, automation penetration, UBI/workfare programs, labor migration between entities, and the post-work question in automated economies.
- **D-05 (Trade blocs):** By bloc — dedicated sections per major trade bloc/system: BRICS+, EU Core/Periphery, Asian supply chains, Americas trade, African blocs. Each section covers participants, currencies, key trade flows, and integration depth.

### Demographics: Population Data & Structure

- **D-06 (Population figures):** Single best-estimate figures (not ranges). Cleaner for mapping and cross-referencing. Uncertainty documented in the Known Uncertainties section of each doc.
- **D-07 (Hybrid structure):** Global thematic sections covering fertility decline, aging & dependency ratios, climate migration settlement patterns, urbanization & coastal retreat, and successor state demographic divergence — PLUS entity-level demographic profiles.
- **D-08 (Climate migration treatment):** Both — a standalone overview section (2-3 pages) with source regions, destination regions, internal vs cross-border breakdown, legal status, and impact on destination demographics — PLUS integration into other thematic sections where migration is a factor.
- **D-09 (Global demographic headline):** Africa still growing, Asia declining. Sub-Saharan Africa continues growing (though slowing) while East Asia, Europe, and Latin America are in decline. This demographic asymmetry drives migration pressure.
- **D-10 (Entity profile variables — expanded):** Population, age structure (median age / dependency ratio), fertility rate (TFR), net migration rate, urbanization rate, life expectancy, ethnic/religious composition summary, labor force participation rate, and primary languages.

### Culture: Scope & Structure

- **D-11 (Comprehensive scope):** Four content areas:
  1. Ideological & belief systems mapping — per entity: dominant ideology, religious landscape, identity structures, education system character, value orientations
  2. Cultural production & everyday life — media ecosystems, art, music, literature, food culture, fashion
  3. Institutions & cultural transmission — education systems, media, religious organizations, civic institutions, family structures
  4. Language shift — decline of English, rise of Chinese, regional lingua franca shifts
- **D-12 (Language shift approach):** Global overview + regional trends. Covers English decline mechanisms (US collapse, dollar's end, soft power evaporation), Chinese rise (Belt & Road, tech standards, academic publishing), and regional lingua franca shifts (Swahili in East Africa, Spanish as Americas bridge, Mandarin across Asia).
- **D-13 (Hybrid structure):** Thematic global sections for broad patterns (post-capitalist ideology, information ecosystem, climate culture, language shift) + entity profiles summarizing each entity's cultural character.
- **D-14 (Entity coverage — comprehensive):** All US successor states (revolutionary, indigenous, reactionary, degrading) + key global powers: China, EU Core, India, Brazil, East African Federation, ASEAN, Russia, Turkey, Unified Korea, Australia/NZ. ~30 profiles total.

### KML Markers

- **D-15 (Entity-level markers):** One `→ See KML:` marker per entity profile per domain. KMLs are primarily for borders (Phase 3 established the entity placemarks). Phase 4's markers reference those same entity placemarks to anchor socioeconomic claims to specific geographic entities. Not attempting to map economic zones or demographic gradients as separate KML layers.

### Plan Split

- **D-16 (3 parallel plans, Wave 1):**
  - 04-01-PLAN.md — Economy Snapshot
  - 04-02-PLAN.md — Demographics Snapshot
  - 04-03-PLAN.md — Culture Snapshot
  All three written in parallel (same Wave 1), following Phase 3's Wave 2 pattern.
- **D-17 (Dedicated consistency plan):** Plan 04-04 — Cross-Consistency Review & Index Finalization. Runs after the three domain plans complete. Checks for contradictions between docs, alignment of `→ See KML:` markers, and updates `2050-snapshot/index.md`.
- **D-18 (Index update):** Each plan adds its own domain row to the navigation table in `2050-snapshot/index.md` upon completion. 04-04 does the final verification.
- **D-19 (Template):** Use `templates/domain-doc.md` as-is (same D-23 from Phase 3). No modifications needed for socioeconomic content.

### Predictions

- **D-20 (New predictions):** 2 new culture-domain predictions only. Culture has zero existing predictions (prediction-001 through prediction-011 cover borders, economy, demographics, technology, climate). Must not contradict any existing predictions. Economy and demographics are sufficiently covered by existing preds. New predictions numbered following the existing sequence (starting at prediction-012).

### the agent's Discretion
- Exact GDP and population figures (within narrative consistency constraints across domains)
- Specific culture prediction statements (validated during planning — must be falsifiable)
- Cross-reference marker placement and density within sections (one per entity minimum)
- KML placemark naming conventions (follow Phase 3 pattern)
- Exact Obsidian callout formatting for `→ See KML:` markers
- Prediction-012 and prediction-013 specific statements and confidence levels

</decisions>

<specifics>
## Specific Ideas

- Economy doc should cover: global financial architecture overview (BRICS+, multicurrency, post-dollar), entity profiles with sector-level breakdowns, trade bloc analysis, labor/automation section
- Demographics doc should cover: fertility decline, aging, climate migration (standalone + integrated), urbanization, successor state divergence, entity profiles with expanded variables
- Culture doc should cover: ideology, everyday life, institutions, language shift — thematic sections + entity profiles for ~30 entities
- KML markers point to entity placemarks (not economic zones or population gradients)
- All ~19 successor state entities get economic, demographic, and cultural profiles
- Key global powers (China, EU Core, India, Brazil, EAF, ASEAN, Russia, Turkey, Unified Korea, Australia/NZ) get global coverage in all three domains
- Africa growing, Asia declining is the demographic headline
- Language shift: global overview + regional trends (not entity-level)

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Scope
- `.planning/REQUIREMENTS.md` — Phase 4 requirements (ECON-01, ECON-02, DEMO-01, DEMO-02, CULT-01)
- `.planning/ROADMAP.md` — Phase 4 goal, success criteria, and boundary
- `.planning/PROJECT.md` — Project vision, core value, constraints, central thesis

### Prior Phase Context
- `.planning/phases/03-2050-structural-snapshot/03-CONTEXT.md` — All Phase 3 decisions, especially D-19/D-20 (writing mode), D-23 (template), D-24 (Key Changes section), D-35/D-36 (cross-references and KML markers)
- `.planning/phases/02-2026-2050-transition/02-CONTEXT.md` — Phase 2 decisions including D-19 through D-22 (handoff boundary), event ID system
- `.planning/phases/01-foundation-methodology/01-CONTEXT.md` — YAML schemas, prediction format, confidence scale

### Existing Transition Docs (trajectory context for Phase 4)
- `2026-2050-transition/economy.md` — Economy trajectory with 5 drivers, dollar decline timeline, socialist transition arc
- `2026-2050-transition/demographics.md` — Demographics trajectory with 4 drivers, fertility decline, climate migration acceleration
- `2026-2050-transition/culture.md` — Culture trajectory with 5 drivers, identity erosion, post-capitalist ideology formation, Landback

### Existing Phase 3 Domain Docs (structural constraints)
- `2050-snapshot/domains/borders-geopolitics.md` — 19-entity successor state map, territorial claims, trade bloc affiliations, population ranges, economic summaries
- `2050-snapshot/domains/climate.md` — Climate migration analysis (50-80M migrants), water conflict zones, agricultural zone shifts
- `2050-snapshot/domains/technology.md` — AI governance, automation impact, energy systems, healthcare tech divergence, information ecosystem fragmentation

### Existing Vault Assets
- `2050-snapshot/index.md` — Milestone index to be updated by each plan
- `templates/domain-doc.md` — Domain document template (used as-is per D-19/D-23)
- `templates/prediction.md` — Prediction entry template
- `meta/predictions/` — 11 existing prediction entries (prediction-001 through prediction-011)
- `meta/dashboard.md` — Dataview dashboard
- `meta/counter-scenario.md` — Counter-scenario thesis
- `2026-2050-transition/successor-states.md` — 19-entity successor state reference map with population estimates, government types, and economic baselines
- `2026-2050-transition/timeline.md` — 14 inflection events (T-01 through T-14) referenced by domain docs

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Domain doc template** (`templates/domain-doc.md`) — used as-is, same sections as Phase 3 (Key Changes, Analysis, Driving Forces, Cross-Domain Interactions, Key Uncertainties)
- **Entity profiles** in `2050-snapshot/domains/borders-geopolitics.md` — each entity has population ranges, government type, and economic summaries that Phase 4 expands with sector-level detail
- **Successor states map** (`2026-2050-transition/successor-states.md`) — complete listing of ~19 entities with baseline data
- **Prediction template** (`templates/prediction.md`) — ready for 2 new culture-domain prediction entries
- **Existing dashboard** (`meta/dashboard.md`) — new predictions appear automatically via Dataview

### Established Patterns
- Flat milestone directory structure — docs at `2050-snapshot/domains/` level
- Domain-organized by STEEP — economy, demographics, culture docs in `2050-snapshot/domains/`
- YAML frontmatter with Dataview-compatible field syntax
- Confidence labels (HIGH/MEDIUM/LOW) used throughout
- `→ See KML:` markers in domain docs for Phase 5 KML integration
- `→ See also:` cross-references between domain docs
- Event IDs (T-01 through T-14+) for cross-referencing transition doc

### Integration Points
- **Phase 3 → Phase 4:** Structural domains (borders, climate, technology) provide the constraining framework. Borders doc lists entities and trade blocs. Climate doc provides migration drivers and water/resource constraints. Technology doc provides automation and economic infrastructure context.
- **Phase 4 → Phase 5:** `→ See KML:` markers in Phase 4 docs provide the cross-references for Phase 5's KML map files. Each entity profile gets one marker pointing to its KML placemark.
- **Phase 2 → Phase 4:** Transition doc domain sections (economy.md, demographics.md, culture.md) provide the trajectory context. Phase 4 determines the 2050 end-state independently from the same trajectory.
- **Within Phase 4:** Economy, demographics, and culture are closely coupled — economic model constrains demographic possibilities, demographic structure shapes cultural dynamics, cultural ideology drives economic model choice. Plan 04-04 enforces cross-consistency.

</code_context>

<deferred>
## Deferred Ideas

- **→ See KML: economic zone polygons** (trade bloc territories, resource extraction areas) — user views KMLs as primarily for borders. Economic zone KML layers are a possible future enhancement but not part of Phase 4 or Phase 5 scope.
- **→ See KML: demographic feature polygons** (population density gradients, migration corridors) — same reasoning: beyond the scope of the border-focused KML approach.
- **New economy predictions** — existing prediction-007 (dollar) and prediction-009 (PPR constitution) plus the transition doc coverage are sufficient for Phase 4's economic content. Additional economy preds deferred to future phases if needed.
- **New demographics predictions** — existing prediction-003 (climate migration) and prediction-008 (population peak) cover the main demographic claims. Additional demographics preds deferred.
- **Entity-level language profiles** — language shift covered at global overview + regional trends level. Entity-level detail is future scope.

</deferred>

---

*Phase: 04-2050-socioeconomic-snapshot*
*Context gathered: 2026-05-21*
