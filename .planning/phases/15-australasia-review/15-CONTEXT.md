# Phase 15: Australasia Review - Context

**Gathered:** 2026-05-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of Australia and New Zealand in the 2050 snapshot — verify each entity against the revolutionary feedback loop and established Oceania dynamics, fix KML `(wip)` tags (including adding 4 missing overseas territory polygons for Australia), and replace combined `Australia/NZ` entries with individual sub-entries across all 5 domain docs.

**Scope:** Australia and New Zealand only. NZ's associated territories (Cook Islands, Niue, Tokelau) are Phase 18 (Polynesia) scope and are explicitly out of scope here.

</domain>

<decisions>
## Implementation Decisions

### Australia — Revolutionary Stage & Depth

- **D-01:** Australia's revolutionary stage (1-2 vs. 3-4) is **open to researcher** — the transition doc (oceania.md) classifies Australia as "bifurcation point / Stage 1-2" as of 2049 but borders-geopolitics.md says the pivot is "completed" by 2050. The researcher resolves this contradiction and assigns the canonical stage and characterization for the 2050 snapshot.
- **D-02:** Australia gets **substantial (Italy-level) depth** across all domain docs. The transition doc has ~120 lines of analysis on Australia — the researcher synthesizes this into a rich profile covering: AUKUS collapse, strategic pivot trajectory, economic reorientation (China dependency, lithium/rare earths), climate vulnerability, Five Eyes residual status, and BRICS+ observer posture.

### New Zealand — Stage & Depth

- **D-03:** New Zealand is the **"proof of concept" revolutionary small state** — already on the correct path since 1984. The US collapse validates NZ's posture but doesn't require dramatic adjustment. Researcher characterizes NZ as the clearest example of a fully realized revolutionary small state.
- **D-04:** NZ gets **standard depth** — complete but more concise than Australia. The transition doc has ~30 lines on NZ; researcher synthesizes into a focused profile.

### Sub-Entry Format — All Domain Docs

- **D-05:** The existing **combined `Australia / New Zealand`** sub-entries in economy.md (line 770), demographics.md (line 841), culture.md (line 400), and climate.md (line 191) are **replaced** with separate individual sub-entries for Australia and New Zealand in each domain doc.
- **D-06:** borders-geopolitics.md currently has brief paragraph stubs (lines 751-753) for both entities. These are expanded into properly structured individual sub-entries under an "Australasia" section, following the Phase 12 Southern Europe sub-entry pattern.

### AUKUS Collapse

- **D-07:** AUKUS is **dead by 2030** — a clean break. US submarine deliveries fail to materialize (the Pentagon's capacity constraints and "America First" lens make delivery unviable). Australia takes the $3B sunk cost loss, cancels remaining payments, and redirects defense investment to independent capability (the Mitsubishi frigates contract is the model). No residual AUKUS legal obligations by 2050.

### US Bases in Australia

- **D-08:** **US presence at Pine Gap and Darwin marine rotations ends with the US collapse (~2032).** What replaces them — whether Pine Gap converts to Australian sovereign intelligence use, a bilateral arrangement with another partner, or something else — is open to researcher. Lock: US presence gone; researcher characterizes the successor arrangement for the 2050 snapshot.

### KML — (wip) Tag Removal and Territory Additions

- **D-09:** The `(wip)` status for Australasia reflects that the plausibility review hadn't been done. The **existing Australia and New Zealand KML polygons are correct** (GADM-sourced modern-day boundaries remain valid — no territorial changes for the main landmasses by 2050).
- **D-10:** Australia has **4 overseas territories that need KML polygons added**: Christmas Island, Cocos (Keeling) Islands, Heard Island and McDonald Islands, and Norfolk Island. All 4 remain Australian sovereign territory in 2050 (remote, non-strategic — no plausible absorption). Researcher adds polygons for these 4 territories and confirms they appear in entity-config.json.
- **D-11:** After polygon additions and plausibility verification, the `Australasia (wip)` folder in borders.kml is **renamed to `Australasia`** (wip tag removed).
- **D-12:** NZ's associated territories (Cook Islands, Niue, Tokelau) are **Phase 18 (Polynesia) scope** — not touched in Phase 15.

### the agent's Discretion

- Australia's exact feedback loop stage (Stage 2-3 vs. 3-4) — researcher determines from transition doc synthesis
- Specific sub-entry structure for Australia's climate vulnerability section (whether Great Barrier Reef, bushfire regime, and heat adaptation get their own sub-sections or are woven into a narrative profile)
- Whether Australia's BRICS+ observer status is formalized by 2050 or remains an informal posture
- Pine Gap and Darwin successor arrangements (what fills the void after US departure)
- Whether individual AUS/NZ entries in economy.md maintain the same structural format as the Southern Europe precedent or adapt to the combined regional data already present
- Order of work within phase wave structure (researcher/planner determines)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Required for assigning Australia and NZ to loop stages.

### Transition Analysis — Oceania
- `2026-2050-transition/regions/oceania.md` — Primary Oceania analysis. Contains full characterization of Australia (~120 lines) and NZ (~30 lines). Key sections:
  - Lines 30-39: Australia bifurcation point, AUKUS trap, strategic pivot
  - Lines 40-56: NZ revolutionary small-state model
  - Lines 88-142: Systemic dynamics, feedback loops, uncertainty ledger
  - Lines 110, 118-119: Summary outcome characterizations for Australia and NZ
  - Line 147-148: AUKUS collapse uncertainty (MEDIUM confidence)

### 2050 Snapshot Domain Docs
- `2050-snapshot/domains/borders-geopolitics.md` (lines 751-753: Oceania section, Australia/NZ stubs) — Expand both stubs into individual structured sub-entries under an "Australasia" subsection.
- `2050-snapshot/domains/economy.md` (line 770: combined Australia/NZ entry) — Replace with individual Australia and NZ sub-entries.
- `2050-snapshot/domains/demographics.md` (line 841: combined Australia/NZ entry) — Replace with individual sub-entries.
- `2050-snapshot/domains/culture.md` (line 400: combined Australia/NZ entry) — Replace with individual sub-entries.
- `2050-snapshot/domains/climate.md` (line 191: Oceania section, combined Australia/NZ content) — Replace with individual sub-entries.

### KML Files & Entity Config
- `2050-snapshot/kml/entity-config.json` (lines 1127-1145: Australia entry; lines 1145-1163: New Zealand entry) — Add 4 overseas territory entries for Christmas Island, Cocos (Keeling) Islands, Heard & McDonald Islands, Norfolk Island.
- `2050-snapshot/kml/borders.kml` (lines 63825-65170 approx: Australasia (wip) folder) — Add 4 overseas territory polygons; rename folder from `Australasia (wip)` to `Australasia`.

### Prior Phase Context (Patterns to Follow)
- `.planning/phases/12-southern-europe-review/12-CONTEXT.md` — Sub-entry pattern precedent (D-03). Italy = substantial depth; Croatia/Malta = standard depth. Use Italy as the template depth for Australia.
- `.planning/phases/14-western-europe-review/14-CONTEXT.md` — Most recent region review; wave structure (KML → borders-geo → economy+demographics → culture+climate).
- `.planning/phases/07-eastern-asia-review/07-CONTEXT.md` — Reference for handling bifurcation-point entities where researcher resolves the stage.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Southern EU sub-entry pattern (economy.md lines 415-463, demographics.md lines 422-491, culture.md lines 243-306, climate.md lines 92-134) — Template for Australia and NZ individual sub-entries. Australia at Italy/Spain depth; NZ at Croatia/Malta depth.
- Phase 12 structured sub-entry format in borders-geopolitics.md — Template for expanding the paragraph stubs into proper sub-entries.
- entity-config.json overseas territory pattern — Researcher can follow existing small-territory entries for the 4 Australian territories.

### Established Patterns
- All prior Oceania region KML is GADM-sourced modern-day polygons — territorial changes only when a deliberate decision requires redrawing (e.g., Switzerland into EU in Phase 14). Australia and NZ main landmasses: no redrawing needed.
- Wave structure from prior phases: KML/entity-config (Wave 1) → borders-geopolitics sub-entries (Wave 2) → economy + demographics (Wave 3) → culture + climate (Wave 4).
- Individual sub-entries replace combined entries: don't add on top, replace (D-05).

### Integration Points
- `borders-geopolitics.md` lines 751-753: Current paragraph stubs become structured sub-entries. Oceania section structure should be consistent with how other sections (Europe, Asia) handle their entities.
- `economy.md` line 770: Combined entry with quantitative data ($2T combined, ~$1.6T/$400B split) — split into individual entries while preserving the quantitative specificity.
- `demographics.md` line 841: Combined entry with 35M population (Australia ~28M, NZ ~7M) — split maintaining these figures.
- `culture.md` line 400: Combined cultural analysis — split by entity since Australian and NZ cultural identities are genuinely distinct (Australia's Asia-Pacific reorientation vs. NZ's Pacific small-state model).
- `climate.md` line 191: Already mentions both countries distinctly within the combined entry — split should be natural.
- Cross-references throughout docs that cite "Australia/NZ" should be updated or left pointing to the Australia sub-entry where Australia is the primary referent.

</code_context>

<specifics>
## Specific Ideas

- Australia's story is fundamentally about the **end of 80 years of US-alliance dependency** — a country that built its entire strategic posture on ANZUS and AUKUS having to find a new identity as an independent Pacific middle power. The AUKUS collapse (~2030) is the concrete inflection point. This is the narrative core of Australia's profile.
- New Zealand as the **vindication story** — a country that chose the correct path in 1984 (nuclear-free, independent foreign policy) and watched the rest of the Anglosphere eventually be forced to arrive at the same place by necessity. NZ is the proof that revolutionary independence for small states works.
- Australia's 4 overseas territories are remote and strategically minor — they need polygons but don't need substantive profiles beyond noting their continued Australian sovereignty.
- The combined `Australia/NZ` entry format was probably a placeholder while the region awaited its plausibility review. Phase 15 is when they get their proper individual treatment.

</specifics>

<deferred>
## Deferred Ideas

- **NZ's associated territories (Cook Islands, Niue, Tokelau)** — Phase 18 (Polynesia) scope. Not touched in Phase 15.
- **Australia's Pacific Island relationships** — Australia's role in Tuvalu's climate relocation agreement and the Pacific Access Category expansion is noted in demographics.md but the full geopolitical relationship between Australia and Pacific Island states is better addressed in the Melanesia/Polynesia/Micronesia phases (16-18).
- **AUKUS/UK dimension** — How the UK (not a US successor state) relates to AUKUS post-collapse is not addressed here. The UK is still sovereign; the AUKUS "clean break" locks Australia's exit but doesn't characterize UK's position. Deferred if not needed for the 2050 Australia profile.

</deferred>

---

*Phase: 15-australasia-review*
*Context gathered: 2026-05-30*
