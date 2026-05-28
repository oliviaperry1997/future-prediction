# Phase 9: Northern Europe Review - Context

**Gathered:** 2026-05-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of Northern European entities in the 2050 snapshot. Verify against the revolutionary feedback loop and established dynamics, fix KML issues, fill documentation gaps. Covers 10 entities per ROADMAP.md: Denmark, Estonia, Finland, Iceland, Ireland, Latvia, Lithuania, Norway, Sweden, United Kingdom — plus Scotland as a post-UK independent entity.

**Key structural context from prior phases:** The EU federalizes as a revolutionary project by 2050 (Phase 8 D-01/D-02). Denmark, Estonia, Finland, Ireland, Latvia, Lithuania, Sweden are already EU subdivisions. This discussion determined the fate of the remaining Northern European entities within or outside the federal EU framework.

</domain>

<decisions>
## Implementation Decisions

### Entity Fate — EU Membership
- **D-01:** **Norway** joins the federal EU by 2050. Revolutionary Nordic social-democratic state. Energy transition erodes the oil/gas reactionary anchor. Merges into the EU polygon — no individual KML entity or domain profiles needed.
- **D-02:** **Iceland** joins the federal EU by 2050. Revolutionary social-democratic state. Renewable energy abundance and strategic Arctic position make it a natural EU member. Merges into the EU polygon.
- **D-03:** **Scotland** exits the UK ~2035-2038 and accedes directly to the federal EU. Revolutionary (progressive SNP/Greens, explicitly pro-EU). Merges into the EU polygon.
- **D-04:** **Åland Islands** get a separate KML polygon/placemark within the EU Nordic zone. Autonomous demilitarized Swedish-speaking region of Finland — visible on the map as a distinct sub-entity.
- **D-05:** **Faroe Islands** join the EU with Denmark. Self-governing Danish territory, fishery concerns addressed within the EU's regional framework.
- **D-06:** **Svalbard** becomes EU Arctic territory. Norway's EU membership and the EU's Arctic governance framework effectively supersede the 1920 Svalbard Treaty's special status.

### Entity Fate — Irish Unification
- **D-07:** **Northern Ireland** reunifies with Ireland ~2030s following a border poll. Post-Brexit, with Scotland in the EU and the UK outside, the case for unification is overwhelming. Northern Ireland becomes part of Ireland, which is an EU subdivision.

### Entity Fate — United Kingdom
- **D-08:** The UK undergoes a **late revolutionary flip (~2045-2048)**. Trajectory: reactionary post-Brexit isolation through ~2035 (Scotland exit, City loses dollar-clearing, US collapse), reactionary trap ~2035-2045, then revolutionary transformation in the late 2040s. By 2050, the UK is in early-stage revolutionary state — nuclear-armed middle power with limited European influence.
- **D-09:** **Isle of Man, Channel Islands** follow the UK, outside the EU. Crown dependencies with UK diplomatic representation.
- **D-10:** **Gibraltar** becomes Spanish territory, part of the federal EU. UK-Spain shared sovereignty deal or Spanish absorption — UK lacks power to contest post-collapse.

### Greenland
- **D-11:** Existing decision stands (from borders-geopolitics.md): Greenland achieves independence from Denmark ~2038-2042 and joins the Inuit Nunangat pan-Inuit Arctic confederation. No change from prior documentation.

### EU Subdivision Profile Strategy
- **D-12:** Northern EU members (Denmark, Estonia, Finland, Iceland, Ireland, Latvia, Lithuania, Norway, Scotland, Sweden) do **not** receive individual domain profiles. The EU collective profile is sufficient to cover all Northern European EU subdivisions.
- **D-13:** The EU collective profile in all 5 domain docs (economy, demographics, culture, climate, borders-geopolitics) already covers these members as administrative subdivisions. No expansion needed beyond what Phase 8 established for the federal EU.

### KML Strategy
- **D-14:** Remove `(wip)` tag from Eurasia → Northern Europe folder in borders.kml.
- **D-15:** Northern Europe KML folder retains only **United Kingdom** as a non-EU entity. All other Northern European entities are EU subdivisions and merged into the "European Federation" polygon.
- **D-16:** Entity-config.json changes:
  - Remove individual entries for Iceland, Norway (merged into EU)
  - Remove individual entry for Ireland (leftover from pre-Phase 8 — covered by EU)
  - Remove any other individual EU member entity entries in Northern Europe (Denmark, Sweden, Estonia, Latvia, Lithuania, Finland)
  - Remove individual entry for Spain, Portugal, Italy, Austria, Greece, Croatia etc. (Phase 8 leftover cleanup — all covered by EU)
  - Add `"NOR"` and `"ISL"` country codes to the European Federation entity's `country_codes`
  - UK entry updated: late-revolutionary classification, Scotland mentioned as having left
  - Åland Islands added as a KML sub-entity/placemark within the EU Nordic zone
- **D-17:** No overlay KML files (economy.kml, culture.kml, climate.kml, demographics.kml) need Northern Europe-specific changes — the EU collective entries cover all members.

### Entity Profile Priority
- **D-18:** Profile work within this phase (following Phase 6-7-8 pattern):
  1. KML edits + entity-config cleanup (Wave 1)
  2. Borders-geopolitics.md — update UK entry with late-revolutionary classification and Scotland-EU accession; remove any Northern Europe-specific sections that reference non-EU entities incorrectly
  3. Domain docs — verify EU collective profile adequately covers Northern European members; add minor references to Norway/Iceland/Scotland if missing (but no individual profiles)
  4. Climate.md — verify Arctic/Nordic coverage within EU profile and existing climate doc (lines 74, 107 already mention Northern Europe)

### the agent's Discretion
- Exact order of entity review within the phase (subject to D-18 priority)
- Exact coordinate precision for any KML edits
- Low-priority territory cleanup (Shetland, Rockall, Jan Mayen, Bouvet Island, etc.)
- Whether to add Arctic/Nordic overlay KML features
- Whether any EU collective profile entries need minor updates for the new Nordic members

</decisions>

<specifics>
## Specific Ideas

- "depends on their position within the feedback loop — revolutionary states would more likely join [the EU], reactionary states likely wouldn't" — This principle was the foundation for all EU membership decisions in this phase. Applied to Norway, Iceland, Scotland (revolutionary → join), UK (late flip → separate until ~2048).
- The UK's late revolutionary flip means it's more like France (post-Bardella ~2043-2045) in timeline — recently revolutionary, early-stage transformation by 2050.
- "Integration as survival" for Northern Ireland — the structural logic that drove Moldova-Romania reunification (Phase 8) applies again: a squeezed territory escapes the reactionary trap by merging with the revolutionary EU.
- Åland Islands on the map as a visible Nordic sub-entity.
- Svalbard's treaty status as effectively superseded by the EU Arctic framework — governance reality supersedes 1920 treaty by 2050.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Stage 5 (Unification & Integration Mechanisms). All revolutionary entities ultimately unify.

### Transition Analysis
- `2026-2050-transition/regions/europe.md` (lines 165-167: UK section, lines 73-105: revolutionary core, line 219: Nordic-Baltic security) — European transition analysis driving the 2050 snapshot.

### 2050 Snapshot Domain Docs (may need minor updates)
- `2050-snapshot/domains/borders-geopolitics.md` (lines 277-279: European Federation + UK) — UK entry needs late-revolutionary classification and Scotland-EU accession update. EU entry may need mention of new Nordic members.
- `2050-snapshot/domains/economy.md` (line 80: EU participants, line 129: UBI Nordic states) — Verify Norway/Iceland/Scotland are listed as EU participants.
- `2050-snapshot/domains/demographics.md` (line 399: EU subdivision populations) — May need minor updates for new EU members.
- `2050-snapshot/domains/culture.md` (line 75: EU secularization) — No changes needed.
- `2050-snapshot/domains/climate.md` (lines 74, 107: Northern Europe climate) — No changes needed but verify coverage is sufficient.
- `2050-snapshot/domains/technology.md` (line 43: Iceland/Scandinavia datacenter) — No changes needed.

### KML Files & Entity Config
- `2050-snapshot/kml/borders.kml` (line ~51470: Northern Europe (wip) folder) — Needs (wip) removal, UK-only folder.
- `2050-snapshot/kml/entity-config.json` — Needs: individual entries removed for Iceland, Norway, Ireland, Spain, Portugal, Italy, Austria, Greece, Croatia, and other individual EU member entities; NOR and ISL codes added to European Federation; UK entry updated; Åland placemark added.

### Prior Phase Context
- `.planning/phases/08-eastern-europe-review/08-CONTEXT.md` — EU federalization decision (D-01/D-02), EU single-entity KML model, confederation KML model (separate polygons).
- `.planning/phases/06-central-asia-review/06-CONTEXT.md` — (wip) removal pattern, entity profile format conventions.
- `.planning/phases/07-eastern-asia-review/07-CONTEXT.md` — Entity-config cleanup pattern (Phase 7 removed Unified Korea).

### No external specs beyond project documents listed above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- EU single-entity KML model from Phase 8 — the "European Federation" group entity with `country_codes` array already includes most Northern EU members (DNK, EST, FIN, IRL, LVA, LTU, SWE) — just need to add NOR, ISL.
- Entity-config individual-entry removal pattern — Phase 7 removed Unified Korea; same pattern applies to removing residual individual entries for Norway, Iceland, Ireland, Spain, Portugal, Italy, Austria, Greece, Croatia etc.
- Domain doc EU collective profile format — established in Phase 8 for expanded federal EU. Phase 9 merely verifies coverage.

### Established Patterns
- (wip) tagging pattern across all v1.1 regions — removal is the standard completion flag.
- Confederation = separate KML polygons (CAC/Union State model). Federation = single KML polygon (EU model).
- Profile writing wave structure: KML + borders (Wave 1) → verify domain docs (Wave 2).
- Domain doc entries grouped by region/sub-region — Northern Europe doesn't need its own section.

### Integration Points
- Entity-config.json European Federation entry needs NOR and ISL added to country_codes array.
- Borders.kml Northern Europe folder needs (wip) removal and reduction to UK-only.
- Individual EU member entity entries across entity-config.json (Spain, Portugal, Italy, etc.) need cleanup — they're leftovers from before Phase 8 EU merge.
- UK entry in borders-geopolitics.md needs late-revolutionary classification and Scotland accession note.
- EU collective profile in domain docs may need minor updates to add Norway, Iceland, Scotland to participant listings.

</code_context>

<deferred>
## Deferred Ideas

- **UK post-2050 trajectory** — The UK's late revolutionary flip (~2045-2048) means the 2050 snapshot captures it in early-stage transformation. Detailed post-2050 trajectory (EU accession? Union State? Independent revolutionary? Nuclear posture?) belongs in the 2075 snapshot phase.
- **Arctic governance evolution** — The EU's Arctic role post-Norway/Iceland membership and Svalbard integration. Could support a dedicated analytical note in a future phase.
- **Nordic regional identity within the EU** — Whether the Nordic Council retains any significance within the federal EU, or whether all regional identity is subsumed by the EU structure. Deferred — covered by EU collective profile.
- None from this discussion that is outside the phase scope.

</deferred>

---

*Phase: 09-northern-europe-review*
*Context gathered: 2026-05-28*
