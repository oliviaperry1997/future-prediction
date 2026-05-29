# Phase 10: Southeast Asia Review - Context

**Gathered:** 2026-05-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of Southeast Asian entities in the 2050 snapshot. Covers all 11 entities: Brunei, Cambodia, East Timor, Indonesia, Laos, Malaysia, Myanmar, Philippines, Singapore, Thailand, Vietnam. Verify each against the revolutionary feedback loop, fix KML (wip) tags, fill documentation gaps.

**Key structural finding from this discussion:** All 11 Southeast Asian entities reach Stage 2-4+ on the revolutionary loop by 2050, with no reactionary holdouts. This enables full ASEAN federalization — the **Southeast Asian Federation (SEAF)** forms by 2050, following the EU single-polygon model. Myanmar flips revolutionary ~2040 (NUG wins). Brunei integrates with ceremonial monarchy retained. East Timor is a full member.

</domain>

<decisions>
## Implementation Decisions

### Entity Fate — Southeast Asian Federation (SEAF)
- **D-01:** The **Southeast Asian Federation (SEAF)** forms by 2050. All 10 original ASEAN members + East Timor join as full member states. This mirrors the EU/European Federation model — the federation replaces individual state polygons in borders.kml.
- **D-02:** SEAF formation is enabled by all 11 entities reaching revolutionary loop Stage 2-4 by 2050 — uniquely, no reactionary holdouts exist (unlike Europe where the UK was the exception). This makes SEAF more complete than the European Federation at the same milestone.
- **D-03:** The abbreviation is **SEAF** (Southeast Asian Federation). The entity was previously called "ASEAN" in all domain docs — this is updated to SEAF across all docs, with a note that SEAF evolved from the ASEAN institutional framework.

### KML Strategy — Single Federation Polygon
- **D-04:** borders.kml: Remove the `"Southeast Asia (wip)"` folder and all 11 individual country entries. Replace with a single **Southeast Asian Federation** entity (same model as European Federation). The `(wip)` tag is removed via the replacement.
- **D-05:** entity-config.json: Remove all 11 individual country entries under the Southeast Asia (wip) group. Add a new `"Southeast Asian Federation"` collective entity entry with all 11 country codes (BRN, KHM, TLS, IDN, LAO, MYS, MMR, PHL, SGP, THA, VNM).
- **D-06:** No overlay KML files (economy.kml, culture.kml, climate.kml, demographics.kml) need Southeast Asia-specific individual changes — the SEAF collective entry covers all members in overlays.

### Myanmar — Revolutionary Flip
- **D-07:** Myanmar's 2050 trajectory: **junta collapses ~2040, NUG/resistance coalition wins**. The junta's negative feedback loop (economic collapse, talent outflow, territory loss to ethnic armed organizations and PDFs) reaches terminal crisis ~2035-2040. The NUG establishes a federal revolutionary state — socialist-democratic, ethnically inclusive, ASEAN-aligned. Myanmar is fully integrated into SEAF.
- **D-08:** The "failed state" framing from the transition doc (asia.md §5, line 94) is **superseded** by this decision. Myanmar is not a permanent failed state — the feedback loop resolves it through revolutionary flip by 2040. The transition doc entry for Myanmar should be updated to reflect the NUG victory trajectory.

### Brunei — Ceremonial Monarchy
- **D-09:** Brunei joins the SEAF as a full member state. The oil sultanate's declining revenue (energy transition) and the feedback loop's structural pressure make integration rational. The monarchy is preserved but becomes **entirely ceremonial** — Brunei becomes a constitutional monarchy within the federation, similar to how European monarchies operate within the EU.

### East Timor — Full SEAF Member
- **D-10:** East Timor joins the SEAF as a full member. Its long-standing ASEAN aspirations (observer since 2022) and oil revenue provide economic stake. Full membership by ~2040-2045. No separate KML polygon.

### Entity Profiles — borders-geopolitics.md Structure
- **D-11:** borders-geopolitics.md structure: **SEAF collective entry first** (in the Asia section, replacing the current ASEAN entry), then **11 individual sub-entries** showing each member state's trajectory and path to federation. Same structure as the CAC (collective entry + constituent members).
- **D-12:** Individual sub-entry depth: **transition-doc depth** — feedback loop stage + key dynamic characterization + See KML pointer. Not minimal one-liners, not full CAC-style paragraphs. Comparable to the Japan/Mongolia entry length in the existing Asia section.
- **D-13:** The SEAF collective entry replaces the existing ASEAN entry — updated to describe the federation's formation, member states, collective weight, and revolutionary trajectory.

### Domain Docs Strategy
- **D-14:** SEAF collective replaces ASEAN across all domain docs:
  - `economy.md`: ASEAN collective entry → SEAF collective entry (rename + update for federation, currency union, collective trade bloc)
  - `demographics.md`: ASEAN collective entry → SEAF collective entry (population, demographic dividend, migration patterns)
  - `culture.md`: ASEAN collective entry → SEAF collective entry (pluralist identity, Mandarin integration, Islamic/Buddhist/Christian coexistence)
  - `climate.md`: Verify SEAF climate coverage; update any references to ASEAN
  - `technology.md`: Verify coverage; update any ASEAN references
- **D-15:** No individual SEAF member state profiles in domain docs. The SEAF collective entry is sufficient — this mirrors Phase 8's EU model where no individual EU member state profiles were created.

### Revolutionary Feedback Loop Assessment
- **D-16:** Per-entity loop stages at 2050:
  - Vietnam: Stage 3-4 Revolutionary (state-directed socialist-market, resisted US coercion, export manufacturing hub)
  - Indonesia: Stage 3-4 Revolutionary (BRICS+ member, nickel strategic trump card, largest SEAF state, most independent posture)
  - Singapore: Stage 4-5 Revolutionary (BRICS+ financial node, maximum adaptation success, financial hub model validated)
  - Philippines: Stage 2-3 Revolutionary (recovering from US coercion spring effect, dramatic China accommodation post-collapse)
  - Thailand: Stage 2-3 Revolutionary (recovering from US coercion, export manufacturing, pragmatic neutrality)
  - Malaysia: Stage 3 Revolutionary (oil/gas transition, hedging model, resource diversification)
  - Myanmar: Stage 3-4 Revolutionary by 2050 (NUG wins ~2040, federal revolutionary state established)
  - Cambodia: Stage 2-3 Revolutionary (post-Hun Sen normalization, China-dependent, gradual integration)
  - Laos: Stage 2-3 Revolutionary (single-party socialist, China-dependent via BRI, hydropower energy transition)
  - Brunei: Stage 2-3 Revolutionary (ceremonial monarchy within SEAF, oil sultanate model dissolved by energy transition)
  - East Timor: Stage 2-3 Revolutionary (young state, oil revenue, SEAF integration provides stability)

### Claude's Discretion
- Exact federation formation date (anywhere in 2040s-early 2050s range)
- Sub-entity geographic details (islands, territorial sea claims, South China Sea resolution specifics)
- Climate coverage specifics for individual island/coastal entities within SEAF
- Order of KML entity cleanup and domain doc updates within the phase wave structure
- Whether the transition doc's asia.md section 5 entry for Myanmar is updated in this phase or noted for a future docs pass

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Stage 2-5 paths, ASEAN application (Stage 3-4 collective), Myanmar Stage 4 degradation entry (superseded by D-07/D-08). Path C (Integration Feedback Loop) applies to SEAF federalization.

### Transition Analysis
- `2026-2050-transition/regions/asia.md` §5 (lines 86-97: Southeast Asia ASEAN section, lines 130-142: loop stage table) — Primary SEA analysis. Myanmar "failed state" framing (line 94, 142) is superseded by D-07. All other ASEAN analysis remains valid.

### 2050 Snapshot Domain Docs (need SEAF updates)
- `2050-snapshot/domains/borders-geopolitics.md` (line 392: ASEAN entry in Asia section) — Replace ASEAN entry with SEAF federation entry + 11 sub-entries. Asia section needs Southeast Asian Federation block.
- `2050-snapshot/domains/economy.md` (lines 495-502: ASEAN collective entry) — Rename to SEAF, update for federation (currency union evolution, collective trade bloc depth, BRICS+ full integration).
- `2050-snapshot/domains/culture.md` (line 249: ASEAN collective entry) — Rename to SEAF, update for federation (pluralist federal identity, institutional multiculturalism).
- `2050-snapshot/domains/demographics.md` — Find ASEAN population/migration entries, update to SEAF.
- `2050-snapshot/domains/climate.md` — Verify SEAF coverage (tropical climate, sea-level rise, monsoon patterns, South China Sea warming).

### KML Files & Entity Config
- `2050-snapshot/kml/entity-config.json` (lines 237-248: Southeast Asia (wip) folder) — Remove all 11 individual entries, add Southeast Asian Federation collective entry.
- `2050-snapshot/kml/borders.kml` — Find Southeast Asia (wip) folder, replace with single SEAF polygon entry. Remove individual country polygons.

### Prior Phase Context (EU model reference)
- `.planning/phases/08-eastern-europe-review/08-CONTEXT.md` — EU federalization decision, EU single-entity KML model, European Federation pattern. SEAF follows this same model.
- `.planning/phases/06-central-asia-review/06-CONTEXT.md` — CAC confederation model (collective + constituent sub-entries). SEAF borders-geopolitics.md structure mirrors CAC's "collective + 11 sub-entries" pattern.

### No external specs beyond project documents listed above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- European Federation single-polygon KML model (Phase 8) — SEAF follows identical implementation: one parent entity, country_codes array with all 11 ISO codes, domain_doc pointer to borders-geopolitics.md SEAF section.
- Entity-config individual entry removal pattern — Phase 7 removed Unified Korea, Phase 8-9 removed individual EU member entries. Same JSON manipulation applies to removing 11 SEA individual entries.
- ASEAN collective profile format in economy.md (lines 495-502) — Existing format, rename and expand for federation depth.

### Established Patterns
- (wip) removal via folder replacement — the "Southeast Asia (wip)" folder in entity-config.json is replaced by SEAF entry; borders.kml folder similarly replaced.
- Wave structure: KML + entity-config (Wave 1) → borders-geopolitics.md (Wave 2) → domain docs verify/update (Wave 3).
- SEAF sub-entries in borders-geopolitics.md: same format as CAC constituent republic entries. Each sub-entry: entity name, feedback loop stage, key dynamic, See KML pointer (for the SEAF collective polygon).

### Integration Points
- entity-config.json: Add `"Southeast Asian Federation"` entry with `country_codes: ["BRN", "KHM", "TLS", "IDN", "LAO", "MYS", "MMR", "PHL", "SGP", "THA", "VNM"]` — modeled on European Federation entry structure.
- borders-geopolitics.md Asia section: ASEAN entry replaced by SEAF entry + 11 sub-entries.
- economy.md BRICS+ section (line 72): Verify Indonesia is listed as BRICS+ member (it is, line 72), and SEAF is represented.
- All domain docs: ASEAN → SEAF rename throughout.

</code_context>

<specifics>
## Specific Ideas

- "SEAF lacks reactionary holdouts" — unlike Europe (UK exception) or CAC (Turkmenistan partial), SEAF achieves full revolutionary coverage across all 11 members by 2050. This makes the SEAF the most ideologically unified major federation at the 2050 milestone. Worth noting in the borders-geopolitics.md SEAF entry.
- Myanmar's revolutionary flip (~2040) driven by NUG/PDF resistance coalition victory — not a "clean revolution" but a civil war resolution. The federal structure of post-junta Myanmar reflects the multi-ethnic reality (Karen, Kachin, Shan, Chin, Arakan autonomy within the federation).
- Brunei's ceremonial monarchy: the Sultan retains a symbolic role analogous to European constitutional monarchs within the EU — this is the precedent to cite in the Brunei sub-entry.
- Singapore as BRICS+ financial node: already documented in economy.md and culture.md. The SEAF benefits from Singapore's financial infrastructure at the federation level.
- East Timor: small island state, oil revenue transitioning, joining SEAF provides security and economic integration it could not achieve independently. Timor Sea resources negotiated collectively within SEAF.

</specifics>

<deferred>
## Deferred Ideas

- **SEAF post-2050 trajectory** — Deepening of the federation, potential SEAF-China relationship evolution, South China Sea governance within SEAF framework. Deferred to 2075 snapshot phase.
- **Myanmar's ethnic federal structure detail** — The specific autonomous territories (Karen State, Kachin State, Shan State, etc.) within post-NUG Myanmar. Sufficient for 2050 to note "federal revolutionary state with ethnic autonomous regions" — detailed borders belong in a future phase.
- **South China Sea maritime delimitation** — How SEAF and China resolve the South China Sea EEZ claims within the federation framework. Deferred — requires more detailed analysis, likely for 2075 phase.
- **ASEAN → SEAF transition doc update** — The asia.md section 5 entry describes ASEAN's institutional model (not SEAF federalization). A broader transition doc update to reflect the SEAF formation pathway may be needed, but is out of scope for this review phase.

</deferred>

---

*Phase: 10-southeast-asia-review*
*Context gathered: 2026-05-28*
