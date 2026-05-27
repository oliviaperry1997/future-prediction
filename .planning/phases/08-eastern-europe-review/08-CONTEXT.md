# Phase 8: Eastern Europe Review - Context

**Gathered:** 2026-05-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of Eastern European entities in the 2050 snapshot. Verify against the revolutionary feedback loop and established dynamics, fix KML issues, fill documentation gaps. Covers 10 entities: Belarus, Bulgaria, Czechia, Hungary, Moldova, Poland, Romania, Russia, Slovakia, Ukraine.

**Critical decision from this discussion:** The European Union federalizes as a revolutionary project by 2050. Federations are depicted as single entities in KML and documentation — all former EU member states become subdivisions of a single federal "European Union" entity. Confederations (like the Union State) are depicted as their constituent members.

</domain>

<decisions>
## Implementation Decisions

### European Union — Revolutionary Federalization
- **D-01:** The EU federalizes as a revolutionary project by 2050. Individual member states flipped revolutionary at different points (Germany post-AfD ~2044-2046, France post-Bardella ~2043-2045, Hungary post-Orbán 2026, Netherlands counterexample 2025-2026) — enough to create critical mass for federalization. Remaining reactionary holdouts were overpowered in the revolutionary federalization process.
- **D-02:** The EU is a single entity in all documentation and KML. Former member states (Poland, Czechia, Slovakia, Bulgaria, Romania, Hungary, plus all Western/Northern/Southern members) are administrative subdivisions, not separate profiled entities.
- **D-03:** The existing "EU Core Federation" profile across all domain docs is expanded to the full federal EU including all members.

### Entity Fates — Union State
- **D-04:** **Russia** — Declining peripheral reactionary Union State anchor. China-dependent junior partner. Degrading through internal contradictions (demographics ~120-125M, brain drain, resource dependency) rather than patron loss. Already fully profiled across all 5 domain docs — needs light update to add Union State context (Belarus + Ukraine as co-republics).
- **D-05:** **Ukraine** — Union State republic. Five eastern oblasts (Crimea, Donetsk, Luhansk, Zaporizhzhia, Kherson) transferred to Russia proper. Remaining ~18 oblasts plus Kyiv form the Ukrainian Union State republic. Assessed as reactionary throughout its trajectory (pre-2014, during US-alignment, and post-US-collapse). Absorbed Transnistria.
- **D-06:** **Belarus** — Union State republic. Reactionary Russian satellite (Lukashenko regime since 1994, never outside Russian sphere). No territorial changes.
- **D-07:** The Union State is a confederation — Russia, Belarus, Ukraine depicted as separate KML entities (matching the CAC confederation model).

### Entity Fates — EU Members
- **D-08:** **Poland** — EU subdivision. Defense-driven alignment with revolutionary EU (facing Union State on Kaliningrad + Belarus/Ukraine borders). PiS reactionary domestic politics ultimately overcome by security imperative.
- **D-09:** **Czechia, Slovakia, Bulgaria** — EU subdivisions. Czechia strongly pro-EU industrial economy. Slovakia post-Fico recovery. Bulgaria EU structural funds-dependent.
- **D-10:** **Romania** — EU subdivision. Absorbed Moldova through reunification. Post-AUR far-right recovery. Deeply contested through the transition period but landed in the federal EU.
- **D-11:** **Moldova** — Reunified with Romania. Not a separate entity. Reunification driven by survival logic (squeezed between Union State and EU, Romanian linguistic/cultural identity, ~44% polling support growing).
- **D-12:** **Transnistria** — Absorbed into Ukraine (Union State republic). Russian troops resolved as part of broader settlement. No separate entity.

### Entity Profile Strategy
- **D-13:** Russia — light profile update across all domains to add Union State context. Core content (declining peripheral power, China-dependent) remains accurate.
- **D-14:** Belarus — new standard-depth profiles across borders-geopolitics, economy, demographics, culture, climate (matching Russia/Turkey/India depth per D-07 from Phase 6).
- **D-15:** Ukraine — new standard-depth profiles across all 5 domain docs (same depth as Belarus/Russia).
- **D-16:** EU collective profile expanded across all domain docs to represent the full federal EU (previously limited to "EU Core" — Nordics, Benelux, post-Orbán Hungary, Baltic states, Slovenia).
- **D-17:** Moldova — no separate profile (absorbed into Romania, covered by EU collective profile).
- **D-18:** Transnistria — no separate profile (absorbed into Ukraine).
- **D-19:** Profile writing priority follows Phase 6-7 pattern: borders-geopolitics → economy + demographics → culture + climate.

### KML Strategy
- **D-20:** Remove `(wip)` tag from Eurasia → Eastern Europe folder in borders.kml.
- **D-21:** Merge all EU member state polygons into a single EU polygon. Individual country polygons (Poland, Czechia, Slovakia, Bulgaria, Romania, Hungary, plus all other EU members) become one merged EU entity.
- **D-22:** Russia, Belarus, Ukraine remain individual polygons within Union State folder (confederation model).
- **D-23:** Remove Moldova polygon — territory absorbed into Romania (part of EU merged polygon).
- **D-24:** Russia polygon expanded to include Crimea, Donetsk, Luhansk, Zaporizhzhia, Kherson oblasts.
- **D-25:** Ukraine polygon reduced to remaining ~18 oblasts plus absorbed Transnistria.
- **D-26:** Generate boundary changes from Natural Earth source using Phase 5 pipeline (generate-kml.py + entity-config.json).
- **D-27:** Update entity-config.json: remove individual entries for Poland, Czechia, Slovakia, Bulgaria, Romania, Hungary, Moldova (merged into EU or removed). Keep Russia, Belarus, Ukraine individual. Add Belarus and Ukraine domain doc references.
- **D-28:** Add KML placemark descriptions for Belarus and Ukraine linking to borders-geopolitics.md. Update EU placemark description for federal EU.

### Framework Application
- **D-29:** Russia assessed as reactionary state. Degrades through internal contradictions rather than patron loss — oligarchic extraction, demographic collapse, resource curse, brain drain. The loop's degradation stages apply to self-contained reactionary states, not just US clients.
- **D-30:** Belarus and Ukraine assessed as reactionary Russian client states. Degradation through dependency on a reactionary patron power.
- **D-31:** Ukraine assessed as reactionary throughout — pre-2014, during US-alignment period, and post-US-collapse Union State period. Not a state that flipped between revolutionary and reactionary.
- **D-32:** EU revolutionary federalization = Stage 5 Unification at European scale. Individual member states reached Stages 2-3 at different times; federalization is the unification phase.

### the agent's Discretion
- Exact order of entity review within the phase (subject to D-19 priority)
- Exact GDP, population, and other numerical figures for Belarus and Ukraine profiles
- KML placemark style choices for Eastern Europe entities
- Exact coordinate precision for boundary changes
- Whether to add climate-overlay KML features for Eastern Europe
- Profile content depth within standard format (some fields may not apply to Belarus/Ukraine)

</decisions>

<specifics>
## Specific Ideas

- Ukraine's Union State membership as a republic (not full absorption) mirrors the CAC pattern — nominal sovereignty retained within a larger confederal framework. Eastern oblast transfer resolves the territorial question while preserving a Ukrainian state.
- The Union State framework provides the institutional vehicle for Eastern Europe's reactionary states — analogous to how the EU provides the framework for Europe's revolutionary states. Two competing European integration projects: one revolutionary (EU), one reactionary (Union State).
- Moldova's reunification with Romania is "integration as survival," not "integration as revolution" — simpler than CAC's integration-as-transformation but driven by the same structural logic (escape from the reactionary trap through merging with a larger entity).
- "The EU's federalization is the European manifestation of Stage 5 — not post-flip unification (Path A like the EAF) but revolutionary institutional capture of an existing confederal framework (distinct from Paths A, B, and C — a new pathway: institutional revolutionary transformation)."
</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Stage 5 (Unification & Integration Mechanisms: Paths A, B, C). EU federalization may represent a new pathway: institutional revolutionary transformation of an existing confederal framework.

### Transition Analysis
- `2026-2050-transition/regions/europe.md` — Full Europe transition analysis. Country classifications (lines 109-142), EU hollowing-out mechanism, Germany/France/Russia trajectories, Phase 1-3 timelines.

### 2050 Snapshot Domain Docs (all need Eastern Europe updates)
- `2050-snapshot/domains/borders-geopolitics.md` — Current borders doc (lines 274-286: EU Core + Russia entries). Needs: Russia light update for Union State context, EU profile expanded to federal EU, Belarus and Ukraine new entries, territorial changes documented.
- `2050-snapshot/domains/economy.md` — Current economy doc (lines 416-424: EU Core, 506-514: Russia). Needs: Russia Union State update, EU expanded, Belarus and Ukraine new standard-depth profiles.
- `2050-snapshot/domains/demographics.md` — Current demographics doc (lines 398-408: EU Core, 506-516: Russia). Needs: Russia Union State update, EU expanded, Belarus and Ukraine new standard-depth profiles.
- `2050-snapshot/domains/culture.md` — Current culture doc (lines 235: EU Core, 251: Russia). Needs: Russia Union State update, EU expanded, Belarus and Ukraine new cultural profiles.
- `2050-snapshot/domains/climate.md` — Current climate doc (Europe section lines 74-75). Needs: Russia/Belarus/Ukraine climate sections, EU climate profile expanded.

### KML Files
- `2050-snapshot/kml/borders.kml` — Eurasia/Eastern Europe (wip) folder with 10 entity sub-folders. Needs: (wip) removal, EU polygon merge, Russia boundary expansion, Ukraine boundary reduction, Moldova removal.
- `2050-snapshot/kml/entity-config.json` — Entity configuration. Needs: EU members merged, Moldova removed, Belarus/Ukraine domain doc references added.
- `2050-snapshot/kml/source/global-countries.kml` — Natural Earth source data for boundary regeneration.

### Prior Phase Context
- `.planning/phases/06-central-asia-review/06-CONTEXT.md` — Phase 6 template: per-entity profile format (D-07 standard depth), KML conventions, (wip) removal pattern, confederation KML model (CAC = separate polygons).
- `.planning/phases/07-eastern-asia-review/07-CONTEXT.md` — Phase 7 entity fate patterns: Korea recalibration, profile writing priority order, KML description anchor format.

### No external specs beyond project documents listed above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Per-entity standard profile format established in economy.md (GDP, sectors, trade, model, currency, labor market) — directly reusable for Belarus and Ukraine profiles
- Demographics profile format (population, age structure, TFR, migration, urbanization, life expectancy, labor force, languages) — established in Phase 6 for CAC entities
- Culture profile format (language, religion, cultural values, global influence) — established in Phase 6, reused in Phase 7
- KML generation pipeline from Phase 5 (generate-kml.py + entity-config.json) — usable for boundary regeneration
- Phase 5 Natural Earth source data pipeline — supports EU polygon merge and Russia/Ukraine boundary changes

### Established Patterns
- (wip) tagging pattern across all v1.1 regions — removal is the standard completion flag (Phase 6 pattern)
- "See KML:" cross-reference markers in domain docs follow format from Phase 4/5
- Per-entity domain doc entries grouped by region/sub-region within each domain doc
- Confederation KML model: separate polygons for constituent members, grouped under region folder (CAC pattern from Phase 6)
- Profile writing wave structure: KML + borders (Wave 1) → economy + demographics (Wave 2) → culture + climate (Wave 2) — Phase 6-7 pattern

### Integration Points
- Russia profiles in all 5 domain docs need light updates (Union State context, Belarus/Ukraine co-republic references)
- EU collective profile in all 5 domain docs needs expansion from "EU Core" to full federal EU
- Belarus and Ukraine profiles insert in Europe section of each domain doc, after Russia
- KML edits target borders.kml Eastern Europe folder and entity-config.json
- EU polygon merge affects all global entities — the merged EU polygon replaces individual country polygons globally
- Moldova's former territory is now part of the EU polygon (via Romania)
- Transnistria's former territory is now part of Ukraine's polygon
</code_context>

<deferred>
## Deferred Ideas

- **Russia-China dependency dynamics** — Detailed analysis of Russia's junior-partner relationship with China post-US-collapse. Out of scope for this phase's profile updates.
- **Union State internal dynamics** — The tension between confederal sovereignty (separate republics) and integration pressure (Russia as anchor). Could support a dedicated analytical note.
- **KML climate overlays for Eastern Europe** — Permafrost thaw zones (Russian Arctic), Black Sea grain belt shifts, Danube basin water stress. Deferred to KML tooling phase.
- **EU federal constitution details** — The specific institutional design of the federal EU (presidential vs. parliamentary, upper house composition, fiscal federalism). Out of scope for this phase.

</deferred>

---

*Phase: 08-eastern-europe-review*
*Context gathered: 2026-05-27*
