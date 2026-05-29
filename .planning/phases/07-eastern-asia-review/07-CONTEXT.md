# Phase 7: Eastern Asia Review - Context

**Gathered:** 2026-05-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of Eastern Asian entities in the 2050 snapshot. Verify against the revolutionary feedback loop and established dynamics, fix KML issues, fill documentation gaps. Covers 5 entities: China, Japan, Mongolia, North Korea (DPRK), South Korea (ROK).

**Critical correction from ROADMAP.md:** The 2050 snapshot previously described Korea as "Unified" (40% revolutionary reunification scenario). All domain docs and KML must be corrected to reflect the 60% scenario: two Koreas on diverging trajectories — ROK in slow-motion reactionary degradation, DPRK in revolutionary ascendancy.

</domain>

<decisions>
## Implementation Decisions

### Entity Fate — Korea Recalibration
- **D-01:** Two Koreas, not Unified Korea. The 60% scenario (non-revolutionary ROK degradation) materialized. ROK continues slow decline — demographic crisis (TFR 0.72), fiscal vulnerability, no strategic purpose post-US. DPRK enters its strongest position since the 1960s — nuclear deterrent codified, Russia alliance functional, Juche ideology validated by US collapse.
- **D-02:** Entity naming convention — **ROK** (Republic of Korea, formerly South Korea) and **DPRK** (Democratic People's Republic of Korea, formerly North Korea). Matches transition doc usage. All existing "Unified Korea" references in domain docs updated to separate ROK/DPRK entries.
- **D-03:** US collapse removes UN sanctions regime — DPRK reconnects with global economy, supercharging domestic growth. This strengthens the two-Koreas divergence: DPRK ascends faster, ROK degrades without US scaffolding.
- **D-04:** ROK entry in borders-geopolitics.md describes reactionary degradation: debt accumulation, dependency on China, loss of technological edge, Lee Jae-myung engagement path as least-bad option.
- **D-05:** DPRK entry in borders-geopolitics.md describes revolutionary ascendancy: nuclear state (codified 9th WPK Congress), Russia alliance (CSPT June 2024), Juche philosophy validated, economic transformation (20×10 plan, weapons exports to Russia, post-sanctions global reconnection).

### Entity Fate — Mongolia
- **D-06:** Mongolia remains a sovereign independent buffer state between China and Russia. Neither absorbed nor satellite — the buffer serves both great powers' interests. Needs complete profile set across all 5 domain docs (borders, economy, demographics, culture, climate).

### Japan — Profile Depth
- **D-07:** Standard depth profiles for Japan across economy, demographics, culture, and climate domains — matching the format used for Russia/India/China (GDP, sectors, trade, model, currency, labor for economy; population, age, TFR, migration, urbanization, life expectancy for demographics; etc.). Japan's slow strategic erosion IS the content of the profiles.
- **D-08:** Japan's borders-geopolitics.md entry already exists (3-line description) — kept as-is with minor updates for KML anchor fix.

### China — Expanded Profiles
- **D-09:** Full demographics, culture, and climate profiles for China added — in addition to existing borders + economy profiles. Standard format matching other major powers.
- **D-10:** China's existing economy profile (GDP ~$30T, advanced manufacturing, AI, renewables, yuan internationalization) and borders entry (largest economy, Taiwan reunification ~2035-2038, demographic crisis managed through automation) retained with minor updates.

### KML Strategy
- **D-11:** Remove `(wip)` tag from Eastern Asia KML folder.
- **D-12:** Remove "Unified Korea" group entity from entity-config.json. Add separate entity config entries for ROK (KOR) and DPRK (PRK) — these already exist in folder_hierarchy but need proper config entries with domain doc references.
- **D-13:** Add Hong Kong (HKG) and Taiwan/TWN (ROC) as additional country codes to China's entity config entry. Change China from single `country_code: "CHN"` to group with codes `["CHN", "HKG", "TWN"]`.
- **D-14:** Add Mongolia placemark description in borders.kml referencing borders-geopolitics.md (once Mongolia entry is written).
- **D-15:** Fix KML description anchors — Japan currently references `#japan` which relies on bold text heading in borders-geopolitics.md. Ensure consistent anchor naming.

### Entity Profile Priority
- **D-16:** Profile writing priority order within this phase:
  1. Borders-geopolitics.md — add Mongolia entry, replace Unified Korea with ROK + DPRK entries
  2. Economy.md — add Japan, Mongolia, ROK, DPRK profiles; expand China profile; remove Unified Korea
  3. Demographics.md — add Japan, Mongolia, ROK, DPRK profiles; expand China profile; remove Unified Korea
  4. Culture.md — add Japan, Mongolia, ROK, DPRK profiles; expand China profile; remove Unified Korea
  5. Climate.md — add Japan, Mongolia, ROK, DPRK sections; expand China section; remove Unified Korea references

### the agent's Discretion
- Exact order of entity review within the phase (subject to D-16 priority)
- KML placemark style choices for Eastern Asia entities
- Exact coordinate precision for border fixes (if any)
- Whether to add climate-overlay KML features for Eastern Asia
- ROK/DPRK profile content depth within the standard format (some fields may not apply to DPRK — e.g., market-based labor market data)

</decisions>

<specifics>
## Specific Ideas

- "The ROK was propped up by the US alliance system and the liberal international order. Without the US, the ROK has no strategic purpose." — This is the foundational insight for ROK's reactionary degradation.
- DPRK's sanctions shackles are removed by US collapse — this supercharges their growth trajectory post-2030s. GDP is a deeply flawed metric for sanctioned economies; DPRK's real economic strength is much higher than nominal figures suggest.
- Mongolia as a sovereign buffer — similar to the project's approach to Central Asia but without confederal transformation. Mongolia survives as-is.
- "Integration-as-transformation" (Phase 6 CAC concept) is specific to Central Asia — not applicable to any Eastern Asian entity.
- Revolutionary feedback loop assessment by entity: China (revolutionary, state-directed), Japan (reactionary trap — demographic/economic), Mongolia (non-applicable — buffer state), DPRK (revolutionary ascendancy), ROK (reactionary degradation).

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Stage 5 Path B (Integration-as-Revolution) added in Phase 6. Eastern Asia entities assessed against existing stages (not Path B).

### Transition Analysis
- `2026-2050-transition/regions/asia.md` (lines 20-36: China, lines 53-62: Japan, lines 64-84: Korea binary fork, lines 139, 151: Korea assessment table) — Probabilistic analysis that drives the 2050 snapshot correction.

### 2050 Snapshot Domain Docs (all need Eastern Asia updates)
- `2050-snapshot/domains/borders-geopolitics.md` (lines 375-383: China/Japan/Korea entries) — Needs Mongolia added, Unified Korea → ROK + DPRK.
- `2050-snapshot/domains/economy.md` (lines 406-433: China entry, 541-560: Unified Korea entry) — Needs Japan/Mongolia/ROK/DPRK profiles, Unified Korea removed.
- `2050-snapshot/domains/demographics.md` (line 41: East Asia TFR, 549-560: Unified Korea entry) — Needs Japan/Mongolia/ROK/DPRK profiles, Unified Korea removed.
- `2050-snapshot/domains/culture.md` (line 82: Unified Korea religion, 258-268: Unified Korea profile) — Needs Japan/Mongolia/ROK/DPRK profiles, Unified Korea removed.
- `2050-snapshot/domains/climate.md` (line 62: Japan typhoons, line 78: Asia section) — Needs expanded Eastern Asia sections.

### KML Files
- `2050-snapshot/kml/borders.kml` (lines ~46072+: Eastern Asia (wip) folder) — Needs (wip) removal, Mongolia description, NK/SK descriptions, China HK/TW codes.
- `2050-snapshot/kml/entity-config.json` — Needs Unified Korea → ROK+DPRK, China HKG+TWN addition.

### Prior Phase Context
- `.planning/phases/06-central-asia-review/06-CONTEXT.md` — Phase 6 template for per-entity profile format, KML conventions, (wip) removal pattern, See KML marker format.

### No external specs beyond project documents listed above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Per-entity profile format established in economy.md (GDP, sectors, trade, model, currency, labor market) — directly reusable for Japan, Mongolia, ROK, DPRK profiles
- Demographics profile format (population, age structure, TFR, migration, urbanization, life expectancy, labor force, languages) — established in Phase 6 for CAC entities
- Culture profile format (language, religion, cultural values, global influence) — established in Phase 6 for CAC entities
- KML entity-config.json pattern — group entity (Unified Korea) can be replaced with individual entries (ROK, DPRK)
- KML description format — `See: 2050-snapshot/domains/borders-geopolitics.md#entity-name` established in Phase 5 pipeline

### Established Patterns
- (wip) tagging pattern across all v1.1 regions — removal is the standard completion flag (Phase 6 pattern)
- Entity naming in domain docs uses common names (China, Japan, India), not formal names (PRC, Japan, Republic of India) — ROK/DPRK is consistent with transition doc but slightly more formal than other entities
- "See KML:" cross-reference markers in domain docs follow format from Phase 4/5
- Domain doc insertion order: entries grouped by region/sub-region in each domain doc

### Integration Points
- ROK and DPRK profiles insert in Asia section of each domain doc (after Japan, before ASEAN)
- Mongolia profile inserts in Asia section (after Japan, before ROK — or after China, before Japan)
- China profiles expand existing entries rather than adding new ones
- KML edits target borders.kml Eastern Asia folder and entity-config.json
- "Unified Korea" references across ALL domain docs require bulk update to ROK + DPRK

</code_context>

<deferred>
## Deferred Ideas

- **DPRK-Russia-China triangle analysis** — The detailed dynamics of the DPRK-Russia alliance post-US-collapse and China's role as guarantor/broker could support a dedicated analytical note. Out of scope for this phase's profile set.
- **Japan nuclear cascade analysis** — With DPRK nuclear and ROK potentially following, Japan's non-nuclear norm erosion timeline could be its own analytical piece. Not part of this phase.
- **Mongolia third-neighbor diplomacy** — Mongolia's "third neighbor" strategy (US, Japan, EU, India) in a post-US world. Intriguing but not required for the 2050 profile.
- **KML climate overlays for Eastern Asia** — Typhoon tracks, sea-level rise zones, demographic heat maps — deferred to KML tooling phase (Phase 5 remainder or future KML enhancement).

</deferred>

---

*Phase: 07-eastern-asia-review*
*Context gathered: 2026-05-27*
