# Phase 20: Africa and America Re-review - Context

**Gathered:** 2026-05-31
**Status:** Ready for planning

<domain>
## Phase Boundary

Complete the v1.1 regional plausibility review for the two remaining continent groups: Africa (5 subregions, 35 entities) and Americas (4 subregions, 85 entities). The user has already reviewed these regions outside of GSD workflows — the content exists in borders-geopolitics.md and transition docs, but economy, demographics, culture, climate, and technology domain docs lack entity-level profiles matching v1.1 depth. KML structure exists for all entities but needs fragmentation fixes (Cameroon, CAR reassessment) and border adjustments (Sahel-Nigeria).

**Scope:** Africa (Eastern, Middle, Northern, Southern, Western) + Americas (Caribbean, Central America, Northern America, South America). Northern America includes US successor states and Canada/Caribbean-adjacent territories — all need v1.1 format updates. KML changes limited to West Africa border rework, Cameroon fragmentation, and CAR reassessment.

</domain>

<decisions>
## Implementation Decisions

### Phase Scope

- **D-01:** Africa and Americas are treated as a **single phase** (20). The continents are merged because the user already reviewed them outside GSD — the foundational analysis is done. Phase 20 brings documentation up to v1.1 depth and implements remaining KML fragmentation.
- **D-02:** The primary deliverable is **documentation gap-filling** (entity-by-entity sub-entries in economy.md, demographics.md, culture.md, climate.md, technology.md), not foundational KML creation. KML work is limited to the specific border changes described below.
- **D-03:** Work is organized as **multiple plans per subregion** (not 1-2 mega-plans). Each of the 9 subregions (Eastern Africa, Middle Africa, Northern Africa, Southern Africa, Western Africa, Caribbean, Central America, Northern America, South America) may get its own plan wave.

### KML Border Changes — Sahel-Nigeria

- **D-04:** Re-partition the Nigeria AES/rump border. **Muslim-majority northern states go to AES, remaining states go to Nigeria rump.** FCT (Abuja) stays with Nigeria. All AES states must be contiguous. The researcher determines exact state allocation using Nigeria admin1 religious demographic data. The current entity-config.json assigns FCT to AES — this **must** move to Nigeria. Expected outcome: roughly 12-18+ AES states (27-35% of Nigeria's territory) after applying the Muslim-majority + contiguity criteria. The current 19-AES-state config is a starting reference, not a locked partition.

### KML Border Changes — Cameroon Fragmentation

- **D-05:** Cameroon fragments into **3 entities** in both KML and entity-config:
  1. **AES North** — Northern regions of Cameroon (Adamawa, North, Extreme North) — added to Federation of Sahel States via admin1 regions
  2. **Ambazonia** — New KML entity: Northwest and Southwest regions of Cameroon (Anglophone regions from the historical Anglophone Crisis). Entity type: `fragmented`, keep_unified: true
  3. **Rump Cameroon** — Existing Cameroon entity reduced to Francophone south (remaining 6 regions: Littoral, Centre, South, East, West, plus the two francophone Adamawa sub-regions)
  - Entity-config.json updated: Cameroon's `admin1_regions` reduced to rump; AES gets northern Cameroon admin1 regions added; Ambazonia created as new entity with CMR admin1 NW+SW regions.

### KML Border Changes — CAR Reassessment

- **D-06:** Central African Republic needs **reassessment**, not automatic splitting. The researcher determines whether the EAF absorption scenario (southern CAR → EAF, northern CAR → contested) is **plausible** against the revolutionary feedback loop. If plausible:
  - Do NOT create a new entity. Instead, add CAR's southern admin1 regions (those plausibly controlled by EAF) to EAF's admin1_regions list, and remove those same admin1 regions from CAR's source admin1 list.
  - If not plausible: keep CAR as a single KML entity and rewrite the borders-geopolitics.md narrative to reflect the reassessment.

### Domain Doc Section Organization

- **D-07:** Domain docs (economy.md, demographics.md, culture.md, climate.md, technology.md) are reorganized to use **UN geoscheme subregion headers**. The existing "US Successor States" section distinction is **removed** — US successor states are integrated into "Northern America" alongside Canada, Bermuda, St. Pierre and Miquelon. Other sections: "Caribbean", "Central America", "South America", "Eastern Africa", "Middle Africa", "Northern Africa", "Southern Africa", "Western Africa".
- **D-08:** All 120 entities receive **entity-by-entity sub-entries** in each domain doc, matching the v1.1 format established in Phases 6-19. Each sub-entry covers: strategic posture, key dynamics, → See KML reference, and domain-specific content (GDP/sectors for economy, population/TFR for demographics, cultural identity for culture, climate risk for climate, technology profile for technology).
- **D-09:** All 40 Northern America entities (currently in Phase 3-4 format) are **converted to v1.1 sub-entry format** — adding → See KML markers, review-completion tags, and structured bullet format matching entity profiles from Phases 15-19. The content already exists; this is a format conversion.

### Wave Structure

- **D-10:** Standard 2-wave structure per subregion when possible. Wave 1: borders-geopolitics review + KML edits + entity-config updates. Wave 2: economy + demographics + culture + climate + technology entity profiles. Subregions without KML changes can skip Wave 1 and proceed directly to documentation.
- **D-11:** Priority order: Western Africa (Sahel-Nigeria border + Cameroon fragmentation is the most complex KML change) → then other subregions. Americas documentation can run in parallel with Africa documentation since the files are independent.

### Agent's Discretion

- Exact Nigeria state allocation (researcher determines from Nigeria admin1 religious demographic data, applying Muslim-majority + contiguity + FCT-with-Nigeria constraints)
- CAR reassessment outcome (plausible → EAF admin1 absorption, or not plausible → single entity + narrative rewrite)
- Exact plan boundaries per subregion — executor determines break points based on entity count and KML complexity
- Whether any subregions can be combined into a single plan (e.g., small subregions like Northern Africa with 1 entity)
- Entity depth variation within standard v1.1 format (major entities like Brazil, South Africa get more depth than microstates)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Required for assigning each entity to a loop stage.

### Transition Docs — Africa
- `2026-2050-transition/regions/africa.md` — Full Africa transition analysis (200 lines). Covers all 5 subregions, key actors, and revolutionary/reactionary dynamics.
- `2026-2050-transition/regions/north-america.md` — North America transition analysis (68 lines). Post-US-collapse dynamics and successor state trajectories.
- `2026-2050-transition/regions/south-america.md` — South America transition analysis (121 lines). Brazil, Argentina, Amazon dieback, Gran Colombia.
- `2026-2050-transition/regions/central-america.md` — Central America transition analysis (173 lines). CAF, Mexico-Aztlán unification, Dry Corridor.

### 2050 Snapshot Domain Docs
- `2050-snapshot/domains/borders-geopolitics.md` — **Africa section** (lines 365-450), **North America Beyond Former US** (lines 118-157), **Caribbean** (lines 159-233), **South America** (lines 235-257), **Central America** (lines 259-277). All four regions have substantive narrative content — researcher works FROM these entries to create domain doc profiles.
- `2050-snapshot/domains/economy.md` — No Africa/Americas entity sections. Africa referenced only in "African Blocs" trade section (lines 100-104) and "Americas Trade" (lines 93-98). US successor states have full profiles (lines 151-403). US Successor States section **will be replaced** with Northern America section per D-07.
- `2050-snapshot/domains/demographics.md` — No Africa/Americas entity sections. US successor states have full profiles (lines 97-398). Same reorganization needed per D-07.
- `2050-snapshot/domains/culture.md` — US successor states and Indigenous nations have profiles (lines 175-210). No Africa or other Americas entity profiles. Same reorganization needed per D-07.
- `2050-snapshot/domains/climate.md` — No Africa or Americas sections. New entity profiles needed per D-08.
- `2050-snapshot/domains/technology.md` — No Africa or Americas sections. New entity profiles needed per D-08.

### KML Files (for border changes)
- `2050-snapshot/kml/borders.kml` — Africa and America folders with existing entity polygons.
- `2050-snapshot/kml/entity-config.json` — Current entity definitions. Key entries needing modification:
  - `Federation of Sahel States` — admin1_regions includes 19 Nigerian states + FCT. FCT must move to Nigeria. Some Muslim-majority states may shift.
  - `Nigeria` — admin1_regions includes 17 southern states. FCT to be added. Potential swaps at the border.
  - `Cameroon` — Single country_code CMR. Will be split into AES north admin1 additions + Ambazonia new entity + rump Cameroon.
  - `East African Federation` — May receive CAR admin1 regions if reassessment confirms plausibility.
  - `Central African Republic` — Single country_code CAF. May lose admin1 regions to EAF if reassessment confirms.
- `2050-snapshot/kml/user_colors.json` — May need new color entries for Ambazonia, updated for any entity changes.

### Prior Phase Patterns
- `.planning/phases/19-antarctica-review/19-CONTEXT.md` — Most recent v1.1 context. Entity format, domain doc expansion pattern.
- `.planning/phases/14-western-europe-review/14-CONTEXT.md` — Phase with similar entity-count complexity (multiple sub-entities within a federation structure).
- `.planning/phases/13-western-asia-review/13-CONTEXT.md` — Phase with fragmentation complexity (Israel dissolution, Saudi fragmentation) — relevant pattern for Cameroon/CAR work.
- `.planning/phases/12-southern-europe-review/12-CONTEXT.md` — 15 entities, established the large-phase pattern.

### Nigeria Admin1 Data
- Researcher must determine religious demographics of Nigeria's 36 states + FCT to apply D-04's Muslim-majority criterion. Sources: current Nigerian census/religious demographic data (Pew Research, Nigeria National Population Commission, Afrobarometer).

</canonical_refs>

<code_context>
## Existing Code Insights

### Established Patterns (from v1.1 Phases 6-19)
- **Entity sub-entry format (v1.1):** `**Entity:**` header, bullet points covering territorial integrity/strategic posture, key dynamics, revolutionary loop stage, `→ See KML:` reference. Used in borders-geopolitics.md, economy.md, demographics.md, culture.md, climate.md, technology.md.
- **Domain doc expansion order:** borders-geopolitics.md → economy + demographics (parallel) → culture + climate + technology (parallel).
- **KLM fidelity:** Most Africa/America entity polygons already exist. KML work in Phase 20 is limited: (1) Sahel-Nigeria border adjustment (entity-config.json region reassignment + KML polygon verification), (2) Cameroon fragmentation (3 entities), (3) CAR reassessment (admin1 reassignment or narrative-only).
- **Review completion markers:** Prior phases removed `(wip)` KML folder suffixes and added review-completion tags. No `(wip)` folders exist for Africa/America — these regions had their initial KML created in Phase 5 before the v1.1 review cycle.

### Integration Points
- The existing "US Successor States" sections in economy.md, demographics.md, culture.md must be **reorganized** into "Northern America" per D-07, not just appended to. This means restructuring existing entity entries (adding → See KML, updating formatting) while keeping the existing content.
- Cameroon fragmentation affects the EAF entity (northern Cameroon regions added to AES admin1 list), the existing Cameroon entry (reduced to rump), and creates a new Ambazonia entry — all 3 must be consistent across KML, entity-config, and all 5 domain docs.
- Current borders-geopolitics.md Africa section (lines 365-450) has rich narrative but may need structure updates to match v1.1 sub-entry format and to reflect KML changes (Cameroon split, CAR reassessment, Sahel border).

### Reusable Assets
- Python KML generation script at `2050-snapshot/kml/generate-kml.py` — existing pipeline for entity polygon generation. May need modification if new entities are added (Ambazonia) or admin1 lists change (Sahel, CAR).
- `2050-snapshot/kml/entity-config-debug.json` — Debug utility for entity-config validation.
- The Phase 13 fragmentation pattern (Israel dissolution, Saudi fragment KMLs) is the closest precedent for Cameroon's 3-way split — see entity-config.json entries for Saudi fragments and Israel dissolution.

</code_context>

<specifics>
## Specific Ideas

- **Sahel-Nigeria border:** The current 19-state + FCT assignment to AES is a starting reference. The researcher applies Muslim-majority + contiguity criteria. FCT must move to Nigeria. The expected outcome is roughly 12-18+ AES northern states. The border must produce two contiguous zones.
- **Ambazonia boundaries:** Northwest and Southwest regions of Cameroon, matching the historical Anglophone Crisis admin1 boundaries. No further subdivision.
- **Cameroon rump:** The Francophone south — Littoral (Douala), Centre (Yaoundé), South, East, West regions. The two francophone Adamawa sub-regions remain with the north (AES).
- **Northern America format conversion:** Existing economy/demographics/culture profiles for US successor states already contain rich data. The conversion is structural: add `→ See KML: [Entity]` line to each, add v1.1 format headers (`**Entity:**`), add review-completion markers. Do NOT rewrite content unless contradictions are found.
- **UN geoscheme subregion boundaries:** Use standard UN geoscheme for Africa and Americas subregion definitions — this is what entity-config.json already uses. Northern America = US successor states + Canada + Bermuda + St. Pierre and Miquelon + Greenland (if present). Central America = Belize to Panama. Caribbean = all island states. South America = continent south of Panama.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 20-africa-and-america-re-review*
*Context gathered: 2026-05-31*
