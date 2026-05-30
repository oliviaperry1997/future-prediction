# Phase 17: Micronesia Review - Context

**Gathered:** 2026-05-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of 6 Micronesian entities (Guam, Kiribati, Marshall Is., Micronesia/FSM, Nauru, Palau) plus CNMI in the 2050 snapshot — verify each entity against the revolutionary feedback loop and established Oceania dynamics, fix KML `(wip)` tag (all entity polygons already exist), and fill documentation gaps across all domain docs.

**Scope:** The 6 named Micronesian entities + CNMI (7 entities total). US Minor Outlying Islands (Wake, Midway, Johnston, Palmyra) get a brief note only — they are uninhabited and handled in the same section as US territories. No new entities added beyond these.

</domain>

<decisions>
## Implementation Decisions

### Guam — Treatment

- **D-01:** Guam gets a **full individual sub-entry** under a "Micronesia" subsection in borders-geopolitics.md, following the Phase 15/16 Melanesia/Australasia pattern. The existing "US Pacific Territories" stub at line 812 is **replaced** by this expanded individual entry. The sub-entry covers: territorial integrity (Chamorro compact with Pacifica/HFS), strategic posture (Andersen AFB and Naval Base Guam as jointly managed assets), key dynamics (economy transition off federal spending, Chamorro self-determination recognition), and `→ See KML: Guam`.

### CNMI — Scope Expansion

- **D-02:** CNMI (Northern Mariana Islands) is **in scope** for Phase 17 as a full individual sub-entry, even though it was not listed in the original 6-entity phase goal. CNMI's Japanese alignment trajectory (post-US, tourism collapse, historical ties) and geographic proximity to the other Micronesian entities make it a natural inclusion. Researcher writes CNMI with the same structured format as all other entities.

### Atoll Sovereignty — Entry Depth

- **D-03:** **Standard depth, consistent** across all 6 entities. No special featured treatment for the atoll states (Kiribati, Marshall Islands) — the EEZ-without-territory legal innovation is noted as part of each entity's profile, but the framework is already covered at the regional level in the Pacific Islands paragraph (borders-geopolitics.md line 810). Researcher does not over-develop the legal innovation theme at the expense of entity-level characterization.

### Post-COFA States — Outcome Focus

- **D-04:** FSM, Palau, and Marshall Islands profiles are **outcome-focused** — researcher characterizes the 2050 state (which patron replaced the US, new arrangement structure, revolutionary loop stage). The post-COFA transition history (aid gap, destabilizing crisis, patron selection) is a brief note providing context, not the featured narrative.

### US Minor Outlying Islands

- **D-05:** Wake Island (claimed by Marshall Islands), Midway, Johnston, and Palmyra get a **brief note** within the Guam / US territories section — no full sub-entries. Uninhabited, strategically noted (Wake's Marshall Islands claim; Midway's wildlife/naval status; Johnston's chemical/nuclear test history). Administrative fate (PPR/HFS) noted in one sentence.

### Entity Sub-Entry Format — All Domain Docs

- **D-06:** All 7 entities (6 named + CNMI) get **full structured sub-entries** across all domain docs, following the Phase 15/16 pattern. Economy, demographics, culture, and climate docs currently have no Micronesia-specific entries — researcher creates individual sub-entries for all entities in each domain doc.
- **D-07:** Climate profiles adapt to entity-specific risk: atoll states (Kiribati, Marshall Is., Nauru) face sea-level/freshwater intrusion as primary threat; Guam and CNMI face typhoon intensification and military/economic transition; FSM and Palau face coral reef degradation and fisheries loss.

### KML — (wip) Tag Removal

- **D-08:** All 6 Micronesian entity KML folders already exist in the `Micronesia (wip)` folder in borders.kml. After review, rename folder to `Micronesia`. No new polygon additions needed (entities are: Guam, Kiribati, Marshall Is., Micronesia/FSM, Nauru, Palau).
- **D-09:** CNMI has its own KML folder (confirmed as part of US territories structure). Researcher verifies CNMI KML placement and cross-reference consistency.

### Agent's Discretion

- Which patron (China, Australia, or regional framework) each COFA state (FSM, Palau, Marshall Is.) aligned with in the 2050 outcome
- Nauru's characterization — tiny phosphate-depleted island with no obvious resource anchor; researcher synthesizes from regional dynamics
- Exact depth of CNMI's Japan-alignment profile given thin transition doc coverage
- Order of work within phase wave structure

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Required for assigning each Micronesian entity to a loop stage.

### Transition Analysis — Oceania
- `2026-2050-transition/regions/oceania.md` — Primary Oceania analysis. Key sections for Micronesia:
  - Lines 20–22: COFA context (US exclusive military access to Micronesia, Marshall Islands, Palau; aid dependency; COFA voided by US collapse)
  - Lines 57–66: Oceania overview — atoll states characterization, post-COFA reorientation framing
  - Lines 75–83: US Pacific Territories section — Guam (detailed), CNMI, American Samoa, Minor Outlying Islands
  - Lines 101, 112–113: Revolutionary/reactionary table — atoll states (Stage 2-3 Climate Justice), post-COFA states (Stage 1-2 Reorientation crisis), Guam (Stage 1-2 Constitutional crisis)
  - Lines 125, 135: Scenario outcomes for Guam and the military bases
  - Lines 150, 154: MEDIUM-confidence uncertainty flags for COFA transition and US territories resolution

### 2050 Snapshot Domain Docs
- `2050-snapshot/domains/borders-geopolitics.md` (lines ~808–814: "Pacific Islands" and "US Pacific Territories" stubs) — Expand into individual Micronesia sub-entries under a new "Micronesia" subsection. The existing US Pacific Territories stub is replaced by individual sub-entries for Guam and CNMI.
- `2050-snapshot/domains/economy.md` — No Micronesia entries currently. Create individual sub-entries for all entities.
- `2050-snapshot/domains/demographics.md` — No Micronesia entries currently. Create individual sub-entries for all entities.
- `2050-snapshot/domains/culture.md` — No Micronesia entries currently. Create individual sub-entries for all entities.
- `2050-snapshot/domains/climate.md` — Expand/create Micronesia-specific entries adapted to entity climate risk profile (atoll sea-level risk for Kiribati/Marshalls/Nauru; typhoon for Guam/CNMI; coral/fisheries for FSM/Palau).

### KML
- `2050-snapshot/kml/borders.kml` — `Micronesia (wip)` folder containing: Guam, Kiribati, Marshall Is., Micronesia (FSM), Nauru, Palau. All polygons exist. After review, rename folder to `Micronesia`.
- `2050-snapshot/kml/entity-config.json` — Confirm/add entries for all Micronesian entities including CNMI.

### Prior Phase Patterns
- `.planning/phases/16-melanesia-review/16-CONTEXT.md` — Phase 16 context. Same format, same domain doc expansion pattern. Follow Melanesia's sub-entry format as the direct precedent.
- `.planning/phases/15-australasia-review/15-CONTEXT.md` — Phase 15 context. Original pattern source.
- `2050-snapshot/domains/borders-geopolitics.md` (lines ~757–810: Australasia and Melanesia sub-entries) — Use these as the structural template for Micronesian sub-entries.

</canonical_refs>

<code_context>
## Existing Code Insights

### Established Patterns
- **Individual entity sub-entry format** (from Phase 15/16): named `**Entity:**` header, then bullet points covering territorial integrity, strategic posture, key dynamics, and a `→ See KML: [Entity]` reference. Climate.md uses a region-level header with entity bullets. Follow these patterns for Micronesia.
- **KML folder rename on review completion**: After Phase 15/16, the `(wip)` folder was renamed (e.g., `Australasia (wip)` → `Australasia`). Same rename from `Micronesia (wip)` → `Micronesia` closes this phase's KML work.
- **Domain doc order of expansion**: borders-geopolitics.md gets the richest expansion; economy, demographics, culture get medium entries; climate adapts to entity's specific risk profile.

### Integration Points
- The `Oceania` section in borders-geopolitics.md now has `Australasia` and `Melanesia` as developed sub-regions. After Phase 17, `Micronesia` joins them. The existing "Pacific Islands" paragraph (line 810) and "US Pacific Territories" stub (line 812) are **replaced** by the new individual Micronesia sub-entries — do not leave orphaned text.
- Kiribati appears in Fiji's climate.md entry (line ~773) as having purchased land for climate community relocation — Kiribati's climate profile must be consistent with this cross-reference.
- The Pacific Islands paragraph (line 810) covers the regional-level EEZ-without-territory framework — individual Micronesian atoll entity profiles reference this rather than re-stating it.

</code_context>

<specifics>
## Specific Ideas

- Guam is the strategically richest Micronesian entity (Andersen AFB, Chamorro sovereignty, economy transition) — its profile sets the depth standard for the phase.
- The COFA-state profiles (FSM, Palau, Marshall Is.) focus on 2050 outcome state, not transition history — researcher assigns a patron and loop stage for each.
- Nauru has the least source material (phosphate depleted, tiny population, no obvious resource anchor) — researcher synthesizes from regional dynamics and notes thin sourcing explicitly.
- CNMI's Japan-alignment trajectory is the defining 2050 characteristic — researcher builds from this anchor even if transition doc coverage is thin.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 17-micronesia-review*
*Context gathered: 2026-05-30*
