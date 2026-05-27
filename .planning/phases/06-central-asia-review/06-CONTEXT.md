# Phase 6: Central Asia Review - Context

**Gathered:** 2026-05-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of Central Asian entities in the 2050 snapshot. Verify against the revolutionary feedback loop and established dynamics, fix KML issues, fill documentation gaps. Covers 5 entities: Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Uzbekistan.

**Scope change from ROADMAP.md:** Afghanistan removed from Central Asia and deferred to Phase 11 (Southern Asia Review). Central Asia covers 5 former Soviet republics only.

</domain>

<decisions>
## Implementation Decisions

### Entity Fate: Central Asian Confederation (CAC)
- **D-01:** The 5 Stans unify as a confederal state by 2050, named the **Central Asian Confederation (CAC)**.
- **D-02:** The confederation is formed ~2045-2050 as an integration-as-transformation mechanism — the Stans escape the reactionary deadlock through collective action, not through individual revolutionary flips. Water crisis (Amu Darya/Syr Darya glacier melt) and energy transition (oil/gas revenue decline) are the forcing functions.
- **D-03:** Tajikistan joins as a Persian-speaking autonomous constituent republic within the Turkic-majority confederation.
- **D-04:** The 5 existing sovereign states become constituent republics of the CAC, retaining internal borders and significant autonomy.

### Entity Profiles
- **D-05:** Per-entity profiles for each of the 5 constituent republics across 4 STEEP domains: economy, demographics, culture, climate.
- **D-06:** A collective CAC parent profile in each domain (like ASEAN's collective entry) PLUS individual constituent republic profiles.
- **D-07:** Standard format for profiles (matching Russia/Turkey/India depth in economy.md) — GDP, dominant sectors, trade partners, economic model, currency, labor market for economy; similar depth for demographics, culture, climate.
- **D-08:** Borders domain unchanged — modern-day borders with exclave fixes. Technology domain has no Central Asia-specific content.

### KML Strategy
- **D-09:** Keep 5 separate KML polygons for constituent republics — confederations have no overlay/merged polygon in this project.
- **D-10:** Remove `(wip)` tag from Eurasia → Central Asia folder in borders.kml.
- **D-11:** Add interior polygon holes for Ferghana Valley exclaves (Kyrgyz-Uzbek exclaves: Sokh, Shakhimardan, Barak, Vorukh, etc.).
- **D-12:** Add `See KML:` cross-reference markers from domain profiles to the Central Asia KML entities.

### Afghanistan
- **D-13:** Afghanistan is deferred to Phase 11 (Southern Asia Review). Removed from Central Asia KML folder.
- **D-14:** Afghanistan status confirmed as "beyond the loop" (failed state, insufficient state structure for either feedback dynamic). No 2050-specific changes applied in this phase.

### Framework Gap — Resolved
- **D-15:** The revolutionary feedback loop document (`prediction-002-revolutionary-feedback-loop.md`) did not adequately describe: (a) how states in a reactionary trap escape the deadlock, and (b) how integration-as-revolution (rather than post-flip unification) works. **Resolved 2026-05-27** — Stage 5 (Unification & Integration Mechanisms) added with three pathways: Path A (post-flip unification), Path B (integration-as-revolution), Path C (integration feedback loop). Central Asia's CAC trajectory is now formalized as Stage 5 Path B.

### the agent's Discretion
- Exact order of entity review within the phase
- Water stress placemark design in KML (if any)
- Exclave coordinate accuracy verification method

</decisions>

<specifics>
## Specific Ideas

- "Integration-as-transformation" is the Central Asian mechanism — the Stans don't flip revolutionary individually, they escape the reactionary trap through collective confederal action. This parallels the African integration feedback loop model but driven by different forces (water crisis + energy transition + Russia-China squeeze instead of anti-colonial solidarity).
- The framework should not allow permanent "beyond the loop" or "too constrained to transform" deadlock states — every reactionary trap must resolve (flip, fracture, or integrate).
- Turkic identity (Organization of Turkic States vehicle) provides the cultural/ideological foundation, with Tajikistan accommodated as a Persian-speaking autonomous member.
- Central Asia demonstrates that the revolutionary feedback loop's unification stage can operate on states that haven't flipped revolutionary — integration as the escape mechanism itself.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Note: does not adequately describe integration-as-revolution or reactionary trap escape mechanisms.

### Transition Analysis
- `2026-2050-transition/regions/asia.md` (lines 99-114, 140, 153, 163) — Central Asia section: reactionary low-intensity trap, Russia-China pivot, water stress, collective trajectory analysis.

### 2050 Snapshot Domain Docs (all need CAC updates)
- `2050-snapshot/domains/borders-geopolitics.md` — Current borders doc (needs CAC entity entry)
- `2050-snapshot/domains/economy.md` — Current economy doc (needs CAC collective + constituent profiles)
- `2050-snapshot/domains/demographics.md` — Current demographics doc (needs CAC profiles)
- `2050-snapshot/domains/culture.md` — Current culture doc (needs CAC profiles, currently has Central Asia in language shift section lines 158-165)
- `2050-snapshot/domains/climate.md` — Current climate doc (line 78: Central Asia glacier melt reference)

### KML Files
- `2050-snapshot/kml/borders.kml` (lines ~45839-46080) — Eurasia/Central Asia (wip) folder with 6 entities. Needs CAC name, exclave fixes, (wip) removal, Afghanistan removed.
- `2050-snapshot/kml/source/global-countries.kml` — Modern-day boundary source data for the 5 Stans' base polygons.

### No external specs beyond project documents listed above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Entity profile format established in economy.md (GDP, sectors, trade, model, currency, labor) — directly reusable for CAC constituent profiles
- ASEAN collective + member pattern in economy.md — template for CAC parent + constituent structure
- KML generation pipeline from Phase 5 — can edit borders.kml directly (remove wip, add exclave holes)

### Established Patterns
- All 5 Stans have modern-day KML boundaries from global-countries.kml source — base polygons ready
- (wip) tagging pattern across all v1.1 regions — removal is the standard completion flag
- Domain docs use `→ See KML: EntityName` format for cross-references

### Integration Points
- CAC profiles insert into existing economy.md (after Turkey, before Unified Korea), demographics.md (after Turkey, before Unified Korea), culture.md (after Turkey, before Unified Korea)
- CAC entry in borders-geopolitics.md (new section for Central Asia, after existing global powers)
- KML edits target borders.kml only — CAC has no overlay KML files (economy.kml, culture.kml, etc. would get See KML markers in domain docs, not new polygons)

</code_context>

<deferred>
## Deferred Ideas

- **Afghanistan review** — moved to Phase 11 (Southern Asia Review). KML entity moved to Southern Asia folder.
- **Revolutionary feedback loop doc update** — ~~framework gap noted. Doc needs edits to describe integration-as-revolution and reactionary trap escape mechanisms. Separate task, not part of this phase.~~ **RESOLVED 2026-05-27** — Stage 5 (Unification & Integration Mechanisms: Paths A, B, C) added to prediction-002-revolutionary-feedback-loop.md.
- **Water stress placemark design** — whether to add Amu Darya/Syr Darya glacier-fed river overlay in KML. Deferred to the agent's discretion during planning/execution.

</deferred>

---

*Phase: 06-central-asia-review*
*Context gathered: 2026-05-27*
