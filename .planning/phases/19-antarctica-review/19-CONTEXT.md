# Phase 19: Antarctica Review - Context

**Gathered:** 2026-05-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of Antarctica in the 2050 snapshot — verify against the revolutionary feedback loop and established dynamics, fix KML `(wip)` tag, and fill documentation gaps across all domain docs. Antarctica is a single entity (not multi-entity like phases 15-18) with a unique non-sovereign governance regime.

**Scope:** Antarctica only. No other polar or orbital regions. The continent is a partial-opening regime with active territorial claims, permanent residency, emergent culture, and a non-sovereign economy by 2050.

</domain>

<decisions>
## Implementation Decisions

### KML Strategy

- **D-01:** Replace the single Antarctica polygon with **per-country territorial claims** as distinct KML entities. The current one-polygon setup does not reflect the 2050 governance reality.
- **D-02:** Claim determination and KML generation are **separate plans**. The researcher first determines what the claims look like in 2050 (revised against all Phase 6-18 revised claimant trajectories), then a dependent plan generates KML polygons for each claim zone.
- **D-03:** Antarctica KML polygons use **ice shelf boundaries** as the source geometry, not coastline. The researcher identifies the appropriate publicly available ice-shelf boundary dataset for KML generation. This is a new data source — the existing GADM pipeline uses coastline.
- **D-04:** `Antarctica (wip)` folder in borders.kml is renamed to `Antarctica` after all polygon edits are complete, following the standard phase completion pattern.

### Domain Doc Depth

- **D-05:** **Full depth across all domain docs.** With the continent opened (Madrid Protocol partial opening), permanent residency is possible, a genuine culture is emergent, and a non-sovereign economy is active. Economy, demographics, culture, technology, and climate docs all get full structured entries — not truncated for non-sovereign status.
- **D-06:** The existing Antarctica paragraph in borders-geopolitics.md (line 923) is expanded to a full entry matching the standard format.

### Format & Placement

- **D-07:** Antarctica uses the **standard `**Entity:**` format** — same header and bullet structure as all sovereign entities from Phases 15-18. Individual claimant countries' claims are discussed within the entity entry alongside the overall governance regime.
- **D-08:** Antarctica gets a **standalone section** in each domain doc — not bundled under a "Polar Regions" umbrella with the Arctic. Its governance, economic, demographic, cultural, and technological stories are distinct and substantial enough to stand alone.

### Agent's Discretion

- Exact 2050 claim configuration (researcher determines from revised claimant trajectories across Phases 6-18)
- Ice shelf boundary dataset selection
- Exact depth per domain doc entry (researcher adapts to available material, but floor is "full entry")
- Order of work within phase wave structure
- Whether any claimant's trajectory has changed enough to remove them from Antarctic presence entirely

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Required for assigning Antarctica and its claimant dynamics to loop stages.

### Transition Analysis — Antarctica
- `2026-2050-transition/regions/antarctica.md` — Full Antarctica transition analysis (123 lines). Key sections:
  - Lines 20-21: Overview — from scientifically governed reserve to contested geopolitical zone
  - Lines 24-25: Treaty reality — Madrid Protocol revisability in 2048, no expiry misconception
  - Lines 28-33: China as expansionist revolutionary (Stage 4-5, Marie Byrd Land)
  - Lines 35-42: Conservationist coalition (Australia, NZ, Norway, France, UK — Stage 3 defensive)
  - Lines 44-50: Argentina-Chile sovereignty revolutionary (Stage 2-3, joint administration)
  - Lines 52-57: Russia as reactionary extractive (Stage 3, junior partner to China)
  - Lines 59-64: India/Brazil/South Africa bifurcation (India as swing vote)
  - Lines 66-71: US successor states — PPR limited participation, active vacuum
  - Lines 73-95: Revolutionary feedback loop and convergent evolution
  - Lines 98-103: Three revolutionary integration patterns
  - Lines 116-119: Four key uncertainties (ATS erosion speed, ice-free land, BRICS+ cohesion, conservationist holding power)

### 2050 Snapshot Domain Docs
- `2050-snapshot/domains/borders-geopolitics.md` (line 923) — Current Antarctica paragraph: partial opening regime, Chinese Marie Byrd Land presence, Argentina-Chile joint Peninsula administration, US Antarctic Program collapse. **Expand to full entry.** Also line 951 (Territorial Integrity table) — Antarctica row documents it as "deliberately unclaimed."
- `2050-snapshot/domains/economy.md` — **Zero Antarctica mentions.** Create full entry covering resource extraction, krill fisheries, bioprospecting, logistics economy, tourism, non-sovereign economic models.
- `2050-snapshot/domains/demographics.md` — **Zero Antarctica mentions.** Create full entry covering permanent research/industry population, rotating personnel, claimant-nationality demographics, station-community demographics.
- `2050-snapshot/domains/culture.md` — **Zero Antarctica mentions.** Create full entry covering scientific internationalism, Treaty-system institutional culture, claim-nationality cultures, emergent Antarctic identity.
- `2050-snapshot/domains/technology.md` — **Zero Antarctica mentions.** Create full entry covering station infrastructure, logistics technology, satellite coverage, ice-penetrating survey tech, extraction technology, renewable energy for polar operations.
- `2050-snapshot/domains/climate.md` — Antarctica referenced only as ice sheet melt / sea level driver (lines 22, 43, 359, 404). Create standalone entry covering Antarctic climate state, ice sheet dynamics, ecosystem changes, climate research infrastructure, and climate-driven governance pressure.

### KML
- `2050-snapshot/kml/borders.kml` — `Antarctica (wip)` folder containing a single Antarctica placemark with multiple polygon patches (coastline-based). **Replace with claim-zone polygons using ice-shelf boundaries.** After all edits, rename folder to `Antarctica`.
- `2050-snapshot/kml/entity-config.json` (line 203-204) — Antarctica (wip) folder entry. Antarctica entity entry (lines 1715-1722) with country_code ATA. **Add entries for each claim zone entity.**

### Prior Phase Patterns
- `.planning/phases/18-polynesia-review/18-CONTEXT.md` — Phase 18 context. Most recent precedent for entity format, domain doc expansion, KML strategy. Note: Polynesia was 10 entities; Antarctica is 1 entity plus claim zones.
- `.planning/phases/17-micronesia-review/17-CONTEXT.md` — Phase 17 context. Pattern for entity sub-entry format and COFA/post-patronage framework.
- `.planning/phases/16-melanesia-review/16-CONTEXT.md` — Phase 16 context. Pattern for independence determination (Kanaky D-02) and researcher-determined sovereignty outcomes.

### Revised Claimant Trajectories (Phases 6-18)
The researcher must read the domain docs for each of the 7 original claimants to determine whether their 2050 Antarctic posture has changed:
- Australia (Phase 15) — Revolutionary Stage 3, largest territorial claim (42%)
- New Zealand (Phase 15) — Revolutionary Stage 4, gateway (Christchurch), Scott Base
- United Kingdom (Phase 9) — Late-revolutionary, post-Brexit capacity constrained, British Antarctic Survey
- Argentina (Phase 13) — Revolutionary sovereignty, 6 permanent + 7 seasonal bases
- Chile (Phase 13) — Revolutionary sovereignty, 4 permanent + 8 seasonal bases
- France (Phase 14) — EU member, Adélie Land claim, Kerguelen logistics base
- Norway (Phase 9) — EU Federation member, Dronning Maud Land claim

Plus non-claimant actors:
- China (Phase 7) — Revolutionary Stage 4-5, Marie Byrd Land de facto zone
- Russia (Phase 8) — Union State, reactionary extractive, junior partner to China
- India (Phase 11) — BRICS+ swing vote, 2 stations
- South Africa (Phase 11) — BRICS+ member, SANAE IV station
- Brazil — Not reviewed in v1.1 (South America not in scope)
- PPR (Phase 15-18) — NZ successor, limited Antarctic participation, conservationist

</canonical_refs>

<code_context>
## Existing Code Insights

### Established Patterns
- **Entity sub-entry format** (from Phases 15-18): `**Entity:**` header, then bullet points covering territorial integrity, strategic posture, key dynamics, and a `→ See KML: [Entity]` reference. Climate.md uses region-level header with entity bullets. Antarctica follows this format but adapted for non-sovereign governance regime — territorial integrity becomes governance structure and claim dynamics.
- **KML folder rename on review completion**: `Antarctica (wip)` → `Antarctica` after all polygon edits and claim zone additions.
- **Domain doc expansion order**: borders-geopolitics.md gets richest expansion; economy, demographics, culture, technology get full entries; climate adapts to Antarctica's specific risk profile (ice sheet dynamics, ecosystem change).
- **Claim-based KML**: No direct precedent in prior phases (all prior entities were sovereign states with contiguous territory). The claim-zone polygon strategy for Antarctica is a new pattern — researcher documents the approach for downstream planners.

### Integration Points
- The "Polar Regions" section in borders-geopolitics.md currently has Antarctica (line 923) and Arctic (line 921) as adjacent paragraphs. After Phase 19, Antarctica becomes a standalone section — the Polar Regions framing in borders-geopolitics may need adjusting.
- Climate.md Antarctica references (ice sheet melt, sea level rise) must remain consistent with the new standalone Antarctica climate entry.
- The Territorial Integrity table (borders-geopolitics.md line 951) explicitly documents Antarctica as "deliberately unclaimed" — this row may need updating after the researcher determines the 2050 claim configuration.
- No domain doc currently has an Antarctica section — all five docs (economy, demographics, culture, technology, climate) are blank canvases for new entries.

### Reusable Assets
- The claim determination → KML generation two-plan dependency pattern is similar to Phase 16's Bougainville determination (D-04: researcher determines independence, then KML follows).
- The transition doc antarctica.md is the richest single-entity transition analysis in the project (123 lines, 5 actor categories, 3 integration patterns) — researcher works from abundant source material, not thin coverage.

</code_context>

<specifics>
## Specific Ideas

- The KML redesign from single continent polygon to claim zones is the defining structural change of this phase — it fundamentally changes what Antarctica looks like in Google Earth and how downstream viewers understand the continent's 2050 governance.
- Ice shelf boundary polygons are a new KML pipeline requirement. The researcher should document the source dataset clearly so the planner can build or adapt the generation pipeline. GADM coastline will not suffice.
- Claims must be reworked against revised claimant trajectories. The transition doc (antarctica.md) was written before Phases 6-18 — every claimant has been revised since. The researcher treats the transition doc as a starting point, not a locked description. The UK (post-Brexit, capacity constrained), France/Norway (now EU Federation members), and PPR (now exists as NZ successor) are the most likely candidates for trajectory revision.
- Antarctica is the only phase in v1.1 covering a non-sovereign entity. The entity format adaptation from sovereign state to governance regime without changing the structural format is the phase's editorial challenge.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 19-antarctica-review*
*Context gathered: 2026-05-30*
