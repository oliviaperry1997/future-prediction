# Phase 12: Southern Europe Review - Context

**Gathered:** 2026-05-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of 15 Southern European entities in the 2050 snapshot: Albania, Bosnia and Herzegovina, Croatia, Cyprus, Greece, Italy, Kosovo, Malta, Montenegro, North Macedonia, Portugal, Serbia, Slovenia, Spain, Turkey. Verify each against the revolutionary feedback loop and established dynamics, fix KML (wip) issues, fill documentation gaps.

**Key structural findings from codebase scouting:**
- 8 entities are EU Federation members (Croatia, Cyprus, Greece, Italy, Malta, Portugal, Slovenia, Spain) — no individual KML, covered collectively by the European Federation entry. These get individual sub-profile depth (all 8, per D-03). Cyprus's KML covers only the southern Republic of Cyprus territory (TRNC is a sub-polygon of Turkey per D-11).
- 6 non-EU Balkans entities (Albania, Bosnia-Herzegovina, Kosovo, Montenegro, North Macedonia, Serbia) are in the `Southern Europe (wip)` folder — likely all join the EU Federation by 2050 (research to confirm/refute, per D-06).
- Turkey is in the `Southern Europe (wip)` folder but is a Quartet anchor with its own standalone KML and established profile. KML folder restructure removes Turkey; full Turkey profile handled in Phase 13.
- 4 European microstates (Andorra, San Marino, Vatican, Monaco) are currently absent from all documentation — likely absorbed into EU Federation (research to confirm, per D-07).

</domain>

<decisions>
## Implementation Decisions

### KML Restructure — Southern Europe (wip)

- **D-01:** The `Southern Europe (wip)` folder is **replaced with individual entity entries** for the 6 non-EU Balkans states, following the same pattern as Phase 8 Eastern Europe. If research confirms that some or all of them join the EU Federation by 2050, their individual KML entries are removed (absorbed by the European Federation polygon). If they remain sovereign, they keep individual entries.
- **D-02:** **Turkey is removed from the Southern Europe folder entirely** — it's already handled as a standalone KML entity and profiled as a Quartet anchor. This phase confirms that restructure; Turkey's full KML and profile depth belongs to Phase 13 (Western Asia Review).

### Western Balkans — Entity Trajectories

- **D-03:** The user's prior expectation is that **all 6 Western Balkans entities join the EU Federation by 2050**, but this is not a locked decision — the researcher must **confirm or refute plausibility** by applying the revolutionary feedback loop to each entity. Key considerations the researcher must address:
  - Kosovo's recognition problem (Spain — an EU member — doesn't recognize Kosovo; does EU accession require universal recognition?)
  - Bosnia-Herzegovina's Republika Srpska dysfunction — is it still a governance blocker by the late 2030s-2040s?
  - Serbia's Russia/China hedging and EU ambivalence — does it flip revolutionary and accede, or stall?
  - Albania, Montenegro, North Macedonia — assessed as closer to accession; researcher confirms loop stage and accession plausibility.
- **D-04:** **If any entity joins the EU Federation by 2050:** Its individual KML polygon is removed (absorbed by the European Federation), and it is documented as an EU subdivision with a sub-entry in the EU Federation section of borders-geopolitics.md.
- **D-05:** **If any entity remains sovereign by 2050:** It keeps an individual KML polygon and gets a standalone borders-geopolitics entry at standard depth. The researcher determines whether non-EU status reflects a frozen reactionary state, unresolved recognition dispute, or deliberate non-alignment.

### EU Member States — Documentation Depth

- **D-03:** **All 8 EU Southern Europe members get individual sub-entries** in borders-geopolitics.md, despite being EU subdivisions — consistent with the substantial transition doc analysis for Italy and Spain, and ensuring completeness across all Southern European entities. The EU entry covers the collective; sub-entries cover the particulars.
- **Sub-entry depth per entity:**
  - **Italy:** Significant depth — far-right governance trajectory (Meloni/FdI), northern autonomy/separatism risk, periphery euro user, eventual EU reabsorption into the revolutionary core. The transition doc has substantial Italy analysis.
  - **Spain:** Significant depth — swing-state trajectory (PP+Vox vs. PSOE), Chinese green investment (CATL Zaragoza), Mediterranean migration exposure, Gibraltar transfer to Spain confirmed (from Phase 9 Northern Europe context — D-01 in Phase 9).
  - **Greece:** Focus on Aegean/Turkey disputes and EU Federation membership. Research-driven depth.
  - **Portugal:** Standard depth — Atlantic-oriented economy, BRICS+ relationship, post-US collapse posture.
  - **Croatia, Cyprus, Malta, Slovenia:** Standard sub-entry depth — brief but present. Cyprus requires acknowledgment of the Turkish-controlled north (TRNC) situation.

### Turkey — Phase Boundary

- **D-06:** **Turkey's full profile belongs to Phase 13 (Western Asia Review).** This phase's Turkey work is limited to:
  - Removing Turkey from the `Southern Europe (wip)` KML folder
  - Confirming Turkey's existing standalone KML entity is correct
  - Noting the Greco-Turkish / Cyprus dispute in the Greece and Cyprus sub-entries (cross-reference to Turkey's Phase 13 profile)
  - No new Turkey profile depth is added in Phase 12.

### European Microstates

- **D-07:** The 4 Southern European microstates (Andorra, San Marino, Vatican, Monaco) are **currently absent from all documentation**. The user's prior expectation is that they get absorbed into the EU Federation, but the researcher must **confirm or refute plausibility** for each:
  - **Andorra** (between France and Spain, ~77K): EU candidate-adjacent; customs union with the EU already exists. Absorption plausible.
  - **San Marino** (landlocked in Italy, ~34K): Dependent on Italy/EU; absorption plausible.
  - **Monaco** (enclave in France, ~36K): Sovereign principality with French customs integration. Absorption more complex — Monegasque sovereignty and Grimaldi dynasty. Researcher assesses.
  - **Vatican City** (~800): Papal sovereign state with unique ecclesiastical status. May retain sovereign status even if EU surrounds it — researcher determines whether it gets a line noting continued sui generis status or is treated as de facto EU territory.
- **D-08:** If absorbed: each gets a brief mention within the EU Federation section or the relevant surrounding country's sub-entry. If one retains sovereignty (especially Vatican): it gets its own brief entry and KML polygon.

### Greco-Turkish Conflict — LOCKED

- **D-09:** The Greco-Turkish conflict follows a **specific locked scenario**: In the mid-2030s, after US dissolution and before the EU Defense Federation is operational, Turkey launches a limited military operation against Greek islands in the Eastern Aegean (most likely Lesbos and Chios — 10-8km from the Turkish coast) and simultaneously formally annexes TRNC and seizes control of Cypriot EEZ gas fields. The casus belli is Turkey's longstanding, legally substantive demilitarization claims under the 1923 Treaty of Lausanne and 1947 Paris Peace Treaty (real treaty obligations, not invented pretexts). France's bilateral 2021 defense pact with Greece creates ambiguity — France condemns the operation and imposes sanctions but does not intervene militarily in time to prevent facts on the ground (delayed by domestic political crisis and legal ambiguity over whether the pact covers islands Greece has militarized in potential treaty violation). The operation is a **deliberate demonstration** of Turkish post-NATO independence.
- **D-10:** **NATO exit mechanism — LOCKED:** Turkey does not get expelled from NATO (no such mechanism exists in the Washington Treaty — Article 5 was written for external aggressors, not member-on-member attacks). Instead: remaining NATO members pass a non-binding condemnation resolution and suspend Turkey's participation; Turkey then **announces formal withdrawal under Article 13**, framing the exit as principled departure from a US-centric institution rendered obsolete by US collapse. Turkey levers this to formalize the Quartet as its replacement security architecture. The "expulsion" is de facto through operational exclusion, not de jure.
- **D-11:** **Outcome — LOCKED (frozen conflict model):**
  - **Aegean islands:** Turkey establishes de facto control over 2-4 Eastern Aegean islands. Internationally unrecognized — the Crimea model. Frozen through 2050.
  - **Cyprus:** TRNC formally annexed by Turkey. Republic of Cyprus retains the south as an EU Federation member but under an imposed EEZ gas field revenue-sharing arrangement. The island is de facto partitioned with Turkey holding the north and the Republic of Cyprus (EU) holding the south.
  - **KML — Cyprus:** The Republic of Cyprus KML polygon covers only the southern portion (Republic of Cyprus territory). A **new Northern Cyprus polygon is added to the Turkey KML entity** — TRNC is Turkish-controlled territory and is represented as a sub-polygon of Turkey, not as a separate sovereign entity.
  - **Long-term:** The EU Defense Federation (~2038-2039) forms **in direct response to this crisis** — the Aegean operation is the founding trauma that creates Greek maximalism for EU military integration. The EDF deters further Turkish action but does not attempt military reversal of frozen gains. The Aegean island dispute and Cyprus partition are the defining unresolved territorial disputes of the European periphery at 2050.
- **D-12:** **Greece sub-entry** must document the Aegean island losses as a historical fact of the 2050 world — Greece is an EU Federation member that lost territory in the mid-2030s. This loss is the primary driver of Greece's position as the EU's most ardent advocate for the European Defense Federation. The frozen dispute is noted; the islands remain Turkish-occupied and internationally unrecognized.

### Agent's Discretion

- Whether individual Western Balkans entities that join the EU get sub-entries of their own within the EU Federation section, or are simply noted as "acceded circa [year]" in the EU entry
- Exact feedback loop stage assignments for all Western Balkans entities (researcher determines)
- Whether the Vatican's continued papal sovereignty warrants a KML polygon or is treated as a point entity / footnote
- Depth of domain doc coverage (economy, demographics, culture, climate) for Western Balkans entities — at minimum borders-geopolitics; fuller profiles if the researcher finds meaningful loop dynamics
- Order of work within phase wave structure

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Required for assessing all Western Balkans entities, microstates, and the Greco-Turkish conflict resolution path.

### Transition Analysis — European Section
- `2026-2050-transition/regions/europe.md` — Primary Europe analysis. Contains substantial Italy and Spain assessments (reactionary periphery, euro crisis, northern autonomy), Balkans trajectories, and the EU federalization narrative. This is the key reference for Southern Europe.

### 2050 Snapshot Domain Docs
- `2050-snapshot/domains/borders-geopolitics.md` (line 278: European Federation entry) — The EU Federation entity. Sub-entries for all 8 Southern EU members added here. The EU Defense Federation (~2038-2039) note must reference the Aegean crisis as its founding catalyst. Western Balkans entities that remain sovereign get standalone entries in the Europe section.
- `2050-snapshot/domains/borders-geopolitics.md` (line 290: Turkey entry) — Brief existing Turkey entry. Phase 13 expands this. Phase 12 adds cross-references from Greece and Cyprus sub-entries.
- `2050-snapshot/domains/borders-geopolitics.md` (line 503: territorial integrity table) — Verify and update European entries, including Cyprus TRNC situation.
- `2050-snapshot/domains/economy.md` — Add sub-entries for Southern EU members and sovereign Western Balkans entities.
- `2050-snapshot/domains/demographics.md` — Mediterranean migration dynamics (from Africa), aging populations in Southern Europe. Add sub-entries.
- `2050-snapshot/domains/culture.md` — Add entries for Southern EU members and Western Balkans entities.
- `2050-snapshot/domains/climate.md` — Southern Europe climate coverage: Mediterranean heat stress, desertification (Spain, southern Italy, Greece), wildfire risk, sea-level effects on coastal Malta and Cyprus.

### KML Files & Entity Config
- `2050-snapshot/kml/entity-config.json` (line 239: "Southern Europe (wip)" folder) — Remove (wip) folder. If all 6 Balkans entities join EU: remove individual entries (they're EU Federation). If any remain sovereign: individual entries. Remove Turkey from this folder.
- `2050-snapshot/kml/borders.kml` — Update Southern Europe (wip) folder accordingly. Confirm Turkey standalone. **Add Northern Cyprus sub-polygon to Turkey's KML entry.** Cyprus polygon covers Republic of Cyprus (south) only.

### Prior Phase Context
- `.planning/phases/09-northern-europe-review/09-CONTEXT.md` — EU Federation model decisions. The "EU is a single entity in KML and docs" rule. Gibraltar → Spain established. Scotland → EU.
- `.planning/phases/08-eastern-europe-review/08-CONTEXT.md` — Individual entity KML pattern (replacing (wip) folders with individual entries). Direct pattern for Western Balkans.
- `.planning/phases/11-southern-asia-review/11-CONTEXT.md` — Most recent prior context. Wave structure pattern for phase execution.

### Established Cross-References
- `2050-snapshot/domains/borders-geopolitics.md` line 23 — Summary note about Northern Europe EU restructure. Southern Europe parallel note needed.
- `2050-snapshot/domains/borders-geopolitics.md` line 29 — Gibraltar → Spain established fact. Spain sub-entry must reflect this.
- `2026-2050-transition/regions/europe.md` lines 67, 86, 91, 99, 104, 118, 131 — Italy and Spain trajectory analysis. Key source for their sub-entry depth.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Individual entity KML pattern (Phase 8 Eastern Europe) — wip folder → individual entries. Apply to Western Balkans entities that remain sovereign.
- EU Federation entry structure (borders-geopolitics.md line 278) — Sub-entries are added within this entry's narrative or as named bold entries below it (same pattern as UK at line 280).
- Turkey entry (line 290) — Brief Quartet-anchor paragraph. Cross-reference pattern for Greece/Cyprus sub-entries.
- Wave structure from prior phases: KML + entity-config (Wave 1) → borders-geopolitics sub-entries (Wave 2) → domain docs economy + demographics (Wave 3) → culture + climate (Wave 4).

### Established Patterns
- Standard depth = borders-geopolitics paragraph + economy + demographics + culture + climate entries. EU sub-entries may be lighter — researcher determines appropriate depth per entity.
- (wip) removal via folder restructure — same as Phase 8 and Phase 11.
- EU territorial integrity note in the borders-geopolitics summary (line 23-29) — add a Southern Europe line.

### Integration Points
- `entity-config.json` line 239: `"Southern Europe (wip)"` folder — replace per D-01/D-02.
- `borders-geopolitics.md` line 278 (EU Federation): add 8 Southern EU member sub-entries.
- `borders-geopolitics.md` line 503 (territorial integrity table): verify/update European entries including Cyprus.
- If Western Balkans entities join EU: they are also EU sub-entries; if sovereign: standalone entries in the Europe section.

</code_context>

<specifics>
## Specific Ideas

- Italy's northern autonomy risk (Lombardy, Veneto, Emilia-Romagna) is a HIGH uncertainty flagged in the transition doc. If the far-right government collapses economically, whether Italy stays territorially unified matters for the EU's shape in Southern Europe. The researcher should take a position on whether Italy is territorially intact by 2050.
- Spain's Gibraltar transfer is already an established fact (Phase 9). Spain's sub-entry should reference this as a resolved territorial gain.
- The Cyprus TRNC situation is now locked (D-11): TRNC is formally annexed by Turkey. Northern Cyprus is a sub-polygon of Turkey's KML entity. The Republic of Cyprus KML covers the south only. The Cyprus sub-entry documents this partition as an established fact.
- The Western Balkans EU accession dynamic is strongly influenced by the reactionary periphery thesis: if France, Italy, Austria were reactionary holdouts through the 2030s-2040s, the EU's political will to absorb the Balkans may have been suppressed during that period, potentially delaying accession past 2050 for some entities. The researcher should assess this timing.
- Andorra's customs union with both Spain and France makes it nearly already a de facto EU territory. Its formal accession (or EU absorption) is among the most plausible of the microstates.
- Monaco's Grimaldi dynasty and its role as a wealth-management microstate gives it stronger sovereignty-preservation incentives than Andorra or San Marino. The researcher should consider whether Monaco's tax status survives EU federalization or becomes an internal EU tax haven dispute.

</specifics>

<deferred>
## Deferred Ideas

- **Post-2050 Italy territorial question** — Whether northern Italy's autonomism resolves (reunified revolutionary Italy or fragmented) is a 2075 snapshot question.
- **Balkans post-2050 dynamics** — Any Balkans entities that join EU and their internal post-accession evolution deferred to 2075.
- **Post-2050 Aegean resolution** — Whether the frozen Aegean island dispute eventually resolves (Turkish withdrawal, EU military pressure, negotiated settlement) is a 2075 snapshot question. The 2050 state is frozen conflict.

</deferred>

---

*Phase: 12-southern-europe-review*
*Context gathered: 2026-05-28*
