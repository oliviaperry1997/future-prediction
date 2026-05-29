# Phase 14: Western Europe Review - Context

**Gathered:** 2026-05-29
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of Western European entities in the 2050 snapshot: Austria, Belgium, France, Germany, Luxembourg, Netherlands, Switzerland, plus European Union-level entities. Verify each against the revolutionary feedback loop and established dynamics, fix KML issues, fill documentation gaps.

**Key structural findings from codebase scouting:**
- All 6 EU Western members (Austria, Belgium, France, Germany, Luxembourg, Netherlands) are already merged into the European Federation KML polygon. No (wip) tags. The gap is documentation — they have ZERO individual sub-entries across all 5 domain docs, unlike Southern EU members which received them in Phase 12.
- Switzerland has a contradictory status: CHE appears in BOTH the EU Federation country_codes (line 688) AND as a standalone entity entry (lines 1276-1284) with its own KML polygon.
- Liechtenstein is absent from all documentation — no entity-config, no KML, no domain doc mention.
- Western Europe has no "restructured" bullet in borders-geopolitics.md Key Changes section (lines 28-31).

</domain>

<decisions>
## Implementation Decisions

### Switzerland — Full EU Member (LOCKED)

- **D-01:** Switzerland is a **full European Federation member** by 2050. The structural pressure of EU encirclement, economic dependency (~60% exports to EU), and the security vacuum created by US collapse (~2032) overcome Swiss neutrality and Sonderfall identity. Swiss direct democracy may require a mechanism (a second or third referendum on EU accession, or a gradual process where association deepens into de facto membership before formal accession).
- **D-02:** Switzerland's CHE is removed from the standalone entity entry in entity-config.json (lines 1276-1284). Its territory is part of the European Federation polygon. No standalone Switzerland profile — covered by EU collective.
- **D-03:** Switzerland's KML polygon is merged into the European Federation multi-polygon in borders.kml.
- **D-04:** Switzerland's `section_anchor` (currently empty string) is no longer needed.
- **Liechtenstein (D-05):** Follows Switzerland's outcome — absorbed into the EU Federation. Not a separate entity.

### Western EU Members — Sub-Entry Depth

- **D-06:** All 6 Western EU members (France, Germany, Netherlands, Belgium, Austria, Luxembourg) get **individual sub-entries** across all 5 domain docs, following the Phase 12 Southern Europe precedent (D-03 in 12-CONTEXT.md). Phase 9 Northern Europe's no-sub-entry rule does NOT apply to Western Europe.
- **D-07 Depth stratification:**
  - **France** — Substantial depth (like Italy in Phase 12). Extensive transition doc analysis (europe.md lines 157-163, 104, 67).
  - **Germany** — Substantial depth (like Spain in Phase 12). Extensive transition doc analysis (europe.md lines 145-155, 84, 91-95).
  - **Netherlands** — Research-driven depth. Specific revolutionary trajectory (PVV collapse, Jetten cabinet 2026) to be fully characterized by researcher.
  - **Belgium** — Standard depth. "Ambiguous — N-VA is Flemish nationalist right but not far-right. Core-adjacent" (europe.md line 141).
  - **Austria** — Standard depth. "Reactionary but small — degrades without fragmenting" (europe.md line 119).
  - **Luxembourg** — Standard depth. Barely mentioned in transition doc; researcher determines the arc.

### France — Nuclear Deterrent & Territorial Integrity

- **D-08:** France's independent nuclear deterrent (force de frappe) remains **national through the 2030s-2040s**. As the European Defense Federation matures (~2038-2039, catalyzed by the Greco-Turkish Aegean crisis per Phase 12 D-11), France's nuclear arsenal is **federalized into a European Nuclear Command framework**. By 2050, France's deterrent is the EU Federation's nuclear deterrent under shared command.
- **D-09:** **France is NOT territorially intact at 2050.** During the Bardella degradation window (2027-2043), Corsican and Breton separatism succeed. Both become **direct EU Federation subdivisions** — not independent sovereign states, not EU associates. Their territory is EU territory with administrative autonomy.
- **D-10:** The rump French state (mainland France minus Brittany and Corsica) undergoes the left reboot (~2043-2045) and re-engages with the EU core from a weakened, territorially reduced position.

### Germany — US Bases & Economic Trajectory

- **D-11:** Post-US-collapse (~2032), all US military bases in Germany (Ramstein, Spangdahlem, etc.) are **transferred to the European Defense Federation (EDF)**. Ramstein becomes the EDF's central command hub — the symbolic and operational center of the EU's independent defense capability. This transfer is part of the broader European Defense Federation formation catalyzed by the Aegean crisis (Phase 12 D-11 timeline: EDF operational ~2038-2039).
- **D-12:** Germany's **economic trajectory is recovery** — the pivot narrative. After the AfD era (~2029-2032 through ~2044), deindustrialization, and the left reboot (~2044-2046), Germany re-emerges as the EU's **leading industrial and technological power** by 2050. Diminished from its 2020s position but still the EU core's engine. The Green-left government that reboots Germany pursues a green industrial policy that positions Germany for the 2050 economy.

### the agent's Discretion

- Exact feedback loop stage assignments for all Western European entities (researcher determines)
- Whether Corsica and Brittany get separate sub-entries within the EU section or are noted within France's sub-entry
- Netherlands' exact revolutionary trajectory details (researcher characterizes fully)
- Belgium's ambiguous N-VA trajectory resolution
- Austria's reactionary degradation timeline and mechanism
- Luxembourg's arc (insufficient transition doc data — researcher fills the gap)
- Order of work within phase wave structure
- Whether the EU collective profile needs a Western Europe subsection update

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Required for assessing all Western European entities against loop stages.

### Transition Analysis — Europe Section
- `2026-2050-transition/regions/europe.md` — Primary Europe analysis. Contains all country classifications for France, Germany, Netherlands, Belgium, Austria. Key lines:
  - Lines 95-107: Phase 3 Core Federation — Benelux + Nordic Council
  - Lines 104: Reactionary periphery — France, Italy, Spain classification
  - Lines 119: Austria — "reactionary but small"
  - Lines 138: Netherlands — PVV collapsed, Jetten cabinet 2026
  - Lines 141: Belgium — "ambiguous, core-adjacent"
  - Lines 145-155: Germany — AfD trajectory, pivot narrative
  - Lines 157-163: France — Bardella 2027, degradation, left reboot
  - Lines 189-196: China investment patterns — avoids unstable reactionary states

### 2050 Snapshot Domain Docs
- `2050-snapshot/domains/borders-geopolitics.md` (lines 278-330: Europe section) — European Federation entry (line 280). Add Western Europe sub-entries for all 6 EU members + Corsica + Brittany. Add "Western Europe restructured" Key Changes bullet (after line 30).
- `2050-snapshot/domains/borders-geopolitics.md` (lines 28-31: Key Changes section) — Add a "Western Europe restructured" bullet following the Southern Europe pattern.
- `2050-snapshot/domains/economy.md` (line 80: EU collective entry) — Add sub-entries for France, Germany, Netherlands, Belgium, Austria, Luxembourg.
- `2050-snapshot/domains/demographics.md` (line 399: EU population breakdown) — Add sub-entries for Western EU members.
- `2050-snapshot/domains/culture.md` (line 75, 235: EU cultural profile) — Add sub-entries for Western EU members.
- `2050-snapshot/domains/climate.md` (line 74: Europe section) — Add sub-entries for Western EU members.
- `2050-snapshot/domains/technology.md` — Add Western EU member mentions where relevant.

### KML Files & Entity Config
- `2050-snapshot/kml/entity-config.json` (line 688: CHE in EU country_codes; lines 1276-1284: Switzerland standalone entry) — Remove standalone Switzerland entry. CHE remains in EU country_codes (was already there). Add any needed validation that European Federation `country_codes` includes AUT, BEL, DEU, FRA, LUX, NLD (should already).
- `2050-snapshot/kml/borders.kml` (lines 56398-61850: Western Europe folder) — Merge Switzerland polygon into European Federation. No other KML changes needed (all EU members already merged).

### Prior Phase Context
- `.planning/phases/12-southern-europe-review/12-CONTEXT.md` — D-03 sub-entry precedent (Southern EU members get individual sub-entries). D-11 Greco-Turkish crisis + EDF formation timeline (critical for France nuke federalization timing).
- `.planning/phases/09-northern-europe-review/09-CONTEXT.md` — Northern Europe no-sub-entry rule (D-12). Confirms Western Europe treatment is distinct.
- `.planning/phases/08-eastern-europe-review/08-CONTEXT.md` — EU federation model D-01/D-02 (EU is single entity in KML and docs).
- `.planning/phases/13-western-asia-review/13-CONTEXT.md` — Entity-config restructuring pattern reference.

### Established Cross-References
- `2050-snapshot/domains/economy.md` line 417 — Swiss watches mentioned in EU luxury goods context. Verify alignment with Switzerland-as-EU-member status.
- `2050-snapshot/domains/economy.md` lines 470, 489 — Kosovo/Serbia diaspora references to Switzerland as EU member. Update if needed.
- `2050-snapshot/domains/demographics.md` lines 472, 480, 486, 490-491 — Western Balkans diaspora references to Switzerland, Germany, Austria. Verify alignment.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Southern EU sub-entry pattern (economy.md lines 415-463, demographics.md lines 422-491, culture.md lines 243-306, climate.md lines 92-134) — Template for Western EU sub-entries. France/Germany at Italy/Spain depth; Netherlands research depth; Belgium/Austria/Luxembourg at Croatia/Malta depth.
- EU Federation collective profile (borders-geopolitics.md line 280, economy.md line 80, demographics.md line 399) — Western EU members are already covered collectively. Sub-entries add individual depth.
- Phase 12 Key Changes bullet pattern (borders-geopolitics.md line 30) — Pattern for adding "Western Europe restructured" bullet.

### Established Patterns
- EU member = no individual KML polygon. Western Europe KML requires no changes (all members already merged).
- Individual sub-entries in borders-geopolitics.md within the EU Federation section (Phase 12 pattern).
- Domain doc sub-entries at entity level (existing Southern Europe, Western Balkans patterns in economy.md, demographics.md, culture.md, climate.md).
- Wave structure from prior phases: KML/entity-config (Wave 1) → borders-geopolitics sub-entries (Wave 2) → economy + demographics (Wave 3) → culture + climate (Wave 4).

### Integration Points
- `entity-config.json`: Remove Switzerland standalone entry (lines 1276-1284). CHE removal from EU country_codes is NOT needed (Switzerland is an EU member).
- `borders.kml`: Merge Switzerland polygon into European Federation multi-polygon.
- `borders-geopolitics.md` line 28-31: Add "Western Europe restructured" Key Changes bullet.
- `borders-geopolitics.md` line 280: Add sub-entries for France, Germany, Netherlands, Belgium, Austria, Luxembourg within the EU Federation section.
- `economy.md` line 80/415-463: Add Western EU sub-entries following Southern Europe pattern.
- `demographics.md` line 399/422-491: Add Western EU sub-entries.
- `culture.md` line 75/243-306: Add Western EU sub-entries.
- `climate.md` line 74/92-134: Add Western EU sub-entries.

### Creative Options
- Corsica and Brittany as EU subdivisions: decide whether they get separate sub-entries in the EU section or are noted within France's sub-entry (agent discretion).
- Netherlands revolutionary trajectory: the PVV-collapse story is one of the most distinctive arcs in Western Europe — a case study in how a reactionary wave can be reversed. This could be the centerpiece of the Netherlands sub-entry.

</code_context>

<specifics>
## Specific Ideas

- Switzerland's EU accession is the most dramatic single reversal of Phase 14 — a country that rejected EEA membership in 1992, rejected EU membership repeatedly, and built its national identity on neutrality, becomes an EU Federation member by 2050. The mechanism (gradual bilateral deepening → de facto membership → formal accession) is the key storytelling challenge for the researcher.
- France's fracture (Corsica + Brittany separating) during the Bardella degradation window is the most significant territorial change in Western Europe. Corsica's separation is Mediterranean and EU-adjacent; Brittany's is Atlantic and Celtic-identity-driven.
- The EDF inheriting US bases (Ramstein as central command) completes the narrative arc: US-built European defense infrastructure becomes the EU's own.
- The Netherlands as the counterexample: a country that elected a far-right government (Wilders/PVV), reversed it within 2 years (2024-2026), and became a revolutionary core member. This arc needs the researcher's full characterization.
- Belgium's trajectory is the most ambiguous of the group — N-VA is Flemish nationalist right but not far-right. The question is whether Belgium stays united (N-VA's Flemish nationalism could destabilize the Belgian state itself, not just its EU orientation).
- Austria's "reactionary but small — degrades without fragmenting" is a concise but thin characterization. The researcher should fill in the mechanism: what does "degrades" look like for Austria?

</specifics>

<deferred>
## Deferred Ideas

- **Post-2050 EU defense architecture** — Whether the European Nuclear Command evolves beyond French arsenal to a shared UK-French-EU framework (UK is non-EU). Deferred to a future 2050 snapshot update or 2075.
- **Swiss accession mechanism detailed narrative** — The process by which Switzerland overcomes its EU-rejection history is a rich story that could merit its own transition document entry. Deferred if not needed for 2050.
- **Brittany and Corsica post-2075 evolution** — Whether these EU subdivisions eventually become full member-state-equivalent entities. Deferred to 2075.

</deferred>

---

*Phase: 14-western-europe-review*
*Context gathered: 2026-05-29*
