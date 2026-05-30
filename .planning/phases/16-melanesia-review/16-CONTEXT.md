# Phase 16: Melanesia Review - Context

**Gathered:** 2026-05-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of Fiji, Kanaky (New Caledonia), Papua New Guinea, Solomon Islands, and Vanuatu in the 2050 snapshot — verify each entity against the revolutionary feedback loop and established Oceania dynamics, fix KML `(wip)` tag (all 5 entity polygons already exist), and fill documentation gaps across all domain docs.

**Scope:** The 5 Melanesian entities only. Bougainville (potential independent state within/from PNG) is a scoping decision deferred to the researcher — see D-04. French Polynesia (Tahiti) is Phase 18 (Polynesia) scope. The Melanesia sub-folder in borders.kml already contains individual folders for all 5 entities.

</domain>

<decisions>
## Implementation Decisions

### PNG Bifurcation — Canonical 2050 Outcome

- **D-01:** PNG's 2050 revolutionary stage is **open to the researcher**. The transition doc classifies PNG as a "bifurcation point" with LOW confidence, noting governance failure biases toward a reactionary outcome but that BRICS+ commodity strategy remains a viable path. The researcher synthesizes the available analysis and assigns a canonical stage and characterization for the 2050 snapshot. The governance tension is a central feature of PNG's profile — do not flatten it.

### Kanaky (New Caledonia) — Status

- **D-02:** Kanaky is **fully independent by 2050**. The KML entity is already named "Kanaky" (the Kanak independence name, not "New Caledonia") — this is an intentional editorial lock on the revolutionary framing. The transition doc says independence by the late 2030s-2040s; by 2050 the transition is complete. Researcher writes Kanaky's profile as an independent sovereign state.
- **D-03:** The nickel reserves (critical for EV batteries) provide the economic foundation for viability. Researcher characterizes how Kanaky's nickel economy connects to the global green transition and BRICS+ commodity relationships.

### Bougainville — Scoping

- **D-04:** Whether Bougainville is an independent 6th Melanesian entity by 2050 (with its own KML polygon extracted from PNG's polygons) or remains documented as part of PNG is **open to the researcher**. The transition doc gives this LOW confidence (~2038-2042 if PNG governance fails). Researcher determines from the overall PNG characterization — if PNG is reactionary/failed, Bougainville independence is more plausible; if PNG achieved a functioning state, Bougainville independence is less likely. The Panguna copper mine is the economic viability anchor.

### Entity Depth — All Domain Docs

- **D-05:** All 5 (or 6, if Bougainville is separate) entities get **full structured sub-entries** across all domain docs, matching the Australasia Phase 15 pattern. Fiji and PNG have rich transition doc material; Solomon Islands, Vanuatu, and Kanaky have thinner coverage (~1-2 sentences each). Researcher synthesizes what exists and extrapolates from regional dynamics (Blue Pacific regionalism, post-US power vacuum, climate threat) where direct transition doc material is thin. Thin sourcing is noted in the profile, not omitted.

### Sub-Entry Format — All Domain Docs

- **D-06:** The existing borders-geopolitics.md has a brief "Pacific Islands" paragraph covering the whole region (line ~768). This is expanded into individual sub-entries per entity under a "Melanesia" subsection, following the Phase 15 Australasia pattern (individual structured entries per entity).
- **D-07:** Economy, demographics, culture, and climate docs currently have **no Melanesia-specific entries**. Researcher creates individual sub-entries for all Melanesian entities in each domain doc.

### KML — (wip) Tag Removal

- **D-08:** All 5 Melanesian entity KML folders already exist in the `Melanesia (wip)` folder in borders.kml. The `(wip)` tag reflects that the plausibility review hasn't been done — it is removed after the review is complete. No new polygon additions are needed (unlike Phase 15's 4 overseas territory additions).
- **D-09:** If Bougainville is determined to be an independent entity (D-04), researcher adds a Bougainville polygon extracted from PNG's existing polygons and creates a separate folder for it.

### The Agent's Discretion

- PNG's exact revolutionary stage (the researcher resolves the bifurcation from transition doc synthesis)
- Whether Bougainville is a 6th separate entity (researcher determines based on PNG stage and LOW-confidence independence trajectory)
- The exact structure of each entity's sub-entries (researcher adapts to available material per entity)
- How deep the nickel/Panguna economic analysis goes for Kanaky and Bougainville profiles
- Whether Vanuatu and Solomon Islands get regional dynamics framing (Blue Pacific) as the primary narrative spine given thin individual coverage in the transition doc
- Order of work within phase wave structure

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Required for assigning each Melanesian entity to a loop stage.

### Transition Analysis — Oceania
- `2026-2050-transition/regions/oceania.md` — Primary Oceania analysis. Key sections for Melanesia:
  - Lines 57–65: Blue Pacific regionalism overview + Melanesian entity classifications (Fiji, PNG, Solomon Islands characterizations)
  - Lines 65: Bougainville independence scenario
  - Lines 71–72: Kanaky (New Caledonia) independence trajectory
  - Lines 100–111: Revolutionary/reactionary table with loop stages for Fiji, Solomon Islands, PNG (bifurcation), French Pacific/Kanaky
  - Line 122–124: Scenario outcomes for Kanaky and Bougainville
  - Lines 151–152: LOW-confidence uncertainty flags for Bougainville independence and New Caledonia outcome

### 2050 Snapshot Domain Docs
- `2050-snapshot/domains/borders-geopolitics.md` (lines ~749–768: Oceania section, "Pacific Islands" paragraph) — Expand into individual Melanesia sub-entries under a "Melanesia" subsection.
- `2050-snapshot/domains/economy.md` — No Melanesia entries currently. Create individual sub-entries for all entities.
- `2050-snapshot/domains/demographics.md` — No Melanesia entries currently. Create individual sub-entries for all entities.
- `2050-snapshot/domains/culture.md` — No Melanesia entries currently. Create individual sub-entries for all entities.
- `2050-snapshot/domains/climate.md` (line ~206: Pacific Island atoll states section) — Expand to include Melanesia-specific entries (note: Melanesian states face cyclone/volcanic risk, not primarily atoll sea-level risk like Micronesia/Polynesia).

### KML
- `2050-snapshot/kml/borders.kml` — `Melanesia (wip)` folder containing: Fiji (44 placemarks), Kanaky (11 placemarks), Papua New Guinea (58 placemarks), Solomon Is. (48 placemarks), Vanuatu (27 placemarks). All polygons exist. After review, rename folder to `Melanesia`. If Bougainville is separate, extract polygon from PNG set.
- `2050-snapshot/kml/entity-config.json` — Confirm/add entries for all Melanesian entities.

### Prior Phase Patterns
- `.planning/phases/15-australasia-review/15-CONTEXT.md` — Phase 15 context. Same format, same domain doc expansion pattern. Follow Australasia's sub-entry format as the precedent for individual entity entries.
- `2050-snapshot/domains/borders-geopolitics.md` (lines ~757–768: Australasia sub-entries for Australia and New Zealand) — Use this as the structural template for Melanesian sub-entries.

</canonical_refs>

<code_context>
## Existing Code Insights

### Established Patterns
- **Individual entity sub-entry format** (from Australasia phase): each entity gets a named `**Entity:**` header, then bullet points covering territorial integrity, strategic posture, key dynamics, and a `→ See KML: [Entity]` reference. Climate.md uses a slightly different structure (region-level header with entity bullets). Follow these patterns for Melanesia.
- **KML folder rename on review completion**: After Phase 15, the `Australasia (wip)` folder was renamed to `Australasia`. Same rename from `Melanesia (wip)` → `Melanesia` closes this phase's KML work.
- **Domain doc order of expansion**: borders-geopolitics.md gets the richest expansion (political/territorial characterization); economy, demographics, culture get medium entries; climate adapts to the entity's primary climate risk profile (cyclone/volcanic for Melanesia, not atoll sea-level).

### Integration Points
- The `Oceania` section in borders-geopolitics.md currently has `Australasia` as the only developed sub-region. After Phase 16, `Melanesia` joins it. After Phases 17-18, `Micronesia` and `Polynesia` complete the Oceania section.
- Fiji appears in climate.md (line 206) as a resettlement destination for atoll climate refugees — any Fiji climate profile must be consistent with this cross-reference.

</code_context>

<specifics>
## Specific Ideas

- The KML entity name "Kanaky" (not "New Caledonia") is a deliberate editorial choice locking the revolutionary framing — researcher should treat this as settled and write Kanaky's profile as an independent sovereign state.
- Fiji is the anchor Melanesian entity (richest transition doc coverage, Stage 3-4) — its profile sets the depth standard for the phase.
- PNG's bifurcation is the most analytically interesting entity — the tension between resource wealth and governance failure should be a featured element of its profile, not just a footnote.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 16-melanesia-review*
*Context gathered: 2026-05-30*
