# Phase 7: Eastern Asia Review - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-27
**Phase:** 07-eastern-asia-review
**Areas discussed:** Korea KML strategy, Korea probability recalibration, Mongolia entity fate, Japan profile depth, China profile expansion, KML entity config cleanup, Korea naming convention

---

## Korea KML — Merged vs Parent Folder

| Option | Description | Selected |
|--------|-------------|----------|
| Polygon merge — single Unified Korea | Merge NK+SK polygons into one entity | |
| Parent folder — keep NK/SK separate | Place NK/SK under Unified Korea parent folder (Phase 6 CAC pattern) | |

**User's choice:** Neither — the fundamental issue is that the 60% scenario (non-revolutionary ROK degradation) is more likely, so Korea should not be unified at all. The docs are inconsistent (transition doc says 60/40 fork, 2050 snapshot says Unified Korea happened). User wants research to recalibrate.

**Notes:** User identified a structural inconsistency: transition doc says 60% reactionary degradation, but 2050 snapshot claims 40% unification scenario materialized. User wants consistency: "if the reactionary degradation scenario is more likely, then that's what happens."

---

## Korea Probability Recalibration (Research)

| Factor | Finding |
|--------|---------|
| DPRK economy 2024 | 3.7% GDP growth (largest in 8 years). Driven by weapons exports to Russia, construction, mining/manufacturing |
| DPRK per capita | ~$1,239 (3.4% of ROK's $37,412). But GDP is flawed metric for sanctioned economies |
| ROK economy 2026 | $1.93T, 1.9% growth. TFR 0.72 (world's lowest). Household debt 200%+ disposable income |
| ROK political polarization | Yoon impeachment upheld April 2025 (martial law Dec 2024). Lee Jae-myung won snap election. Socialist movements remain marginal |
| Russia-DPRK alliance | Comprehensive Strategic Partnership Treaty June 2024 — military alliance restoration, technology transfers, space cooperation |
| DPRK post-sanctions boost | US collapse removes UN sanctions — DPRK reconnects with global economy, supercharging growth |

**User's choice:** Two Koreas (non-revolutionary ROK). The 60% scenario materialized.

**Notes:** User corrected the GDP framing — "GDP is a deeply flawed metric when it comes to countries sanctioned by the US. The real gap is nowhere near as large as those figures would imply." User also noted: US collapse allows DPRK to reconnect with global economy, potentially supercharging domestic growth.

---

## Mongolia — Entity Fate

| Option | Description | Selected |
|--------|-------------|----------|
| Status quo sovereign — buffer state | Mongolia remains independent, third-neighbor diplomacy between China and Russia | ✓ |
| China satellite — de facto protectorate | Deep economic dependence leads to satellite status | |
| Russia-China condominium | Joint management/guarantee framework, Austria model | |

**User's choice:** Status quo sovereign for Mongolia.

**Notes:** Mongolia is completely absent from all project docs — zero mentions in any domain doc. Needs full profile set across all 5 domains. The buffer state model works for both China and Russia.

---

## Japan — Profile Depth

| Option | Description | Selected |
|--------|-------------|----------|
| Standard depth — full profiles | Economy/demographics/culture/climate matching China/Korea format | ✓ |
| Lightweight — existing sufficient | Minimal additions, trajectory IS the profile | |

**User's choice:** Standard depth — full profiles.

**Notes:** Japan currently has NO economy, demographics, or culture profile despite being a major power. The standard format (GDP, sectors, trade, model, currency, labor; population, TFR, etc.) should be applied.

---

## China — Expand Profiles

| Option | Description | Selected |
|--------|-------------|----------|
| Add full demographics/culture/climate profiles | Dedicated entries matching other major powers | ✓ |
| Existing coverage sufficient | Broader Asia analysis already covers China | |

**User's choice:** Add full profiles. Also noted: DPRK post-US-collapse global reconnection would supercharge growth.

**Notes:** China already has borders + economy entries. Needs demographics, culture, and climate profiles added.

---

## China Territory — HK/TW Codes

| Option | Description | Selected |
|--------|-------------|----------|
| China polygon already includes both — verify only | No geometry changes needed | |
| Add explicit HK/TW as country codes | Add HKG and TWN to China's entity-config.json entry | ✓ |

**User's choice:** Add country codes to China in entity-config.json for Hong Kong and Taiwan.

**Notes:** China's modern-day KML polygon includes both. The entity-config.json needs China changed from single country_code to group with CHN+HKG+TWN. Taiwan is a SAR of China since ~2035-2038 per project timeline.

---

## KML Entity Config Cleanup

| Option | Description | Selected |
|--------|-------------|----------|
| Full cleanup | Remove Unified Korea, add NK/SK configs, add HK/TW to China, add Mongolia description, remove (wip) | ✓ |
| Minimal — just HK/TW and (wip) removal | Defer NK/SK configs and Mongolia description | |

**User's choice:** Full cleanup.

**Notes:** Unified Korea group entity removed from entity-config.json. Separate ROK (KOR) and DPRK (PRK) entity config entries added. China gets HKG+TWN codes. Mongolia gets KML description. (wip) tag removed.

---

## Korea Naming Convention

| Option | Description | Selected |
|--------|-------------|----------|
| South Korea / North Korea | Standard modern naming | |
| ROK / DPRK | Official short names — matches transition doc usage | ✓ |
| Republic of Korea / Democratic People's Republic of Korea | Full formal names | |

**User's choice:** ROK / DPRK.

**Notes:** Matches existing transition doc usage (asia.md line 66+). All "Unified Korea" references across domain docs updated to separate ROK and DPRK entries.

---

## Agent's Discretion

- Exact order of entity review within the phase
- KML placemark style choices for Eastern Asia entities
- Exact coordinate precision for border fixes (if any)
- Whether to add climate-overlay KML features for Eastern Asia
- ROK/DPRK profile content depth within the standard format

## Deferred Ideas

- DPRK-Russia-China triangle analysis — dedicated analytical note, out of scope
- Japan nuclear cascade analysis — non-nuclear norm erosion timeline
- Mongolia third-neighbor diplomacy analysis in post-US world
- KML climate overlays for Eastern Asia — deferred to KML tooling phase
