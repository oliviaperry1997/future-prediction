# Feature Landscape: Geopolitical Future Forecasting

**Domain:** Multi-century geopolitical forecasting / world-building
**Researched:** 2026-05-19
**Mode:** Ecosystem (Features dimension)
**Overall confidence:** HIGH

**Sources consulted:** ODNI Global Trends (7 editions, 1997–2021), UK MOD Global Strategic Trends (GST 6 & 7), NATO Strategic Foresight Analysis 2023, BCG "Beyond Tomorrow: Four Scenarios for 2050", AlphaGeo Periodic Table of States, Scenario Atlas AI, FUTARCHY methodology, ISW tradecraft standards, RAND forecasting research, Geopolitical Futures model, OECD Foresight Toolkit, Perry World House forecasting report, FOI China 2050 study.

---

## Table Stakes

Features users/readers expect. Missing these = the project feels amateurish, unserious, or incomplete for a geopolitical forecasting project.

### 1. Structured Domain Coverage (Multiple Analytical Dimensions)

**What:** The forecast must analyze the world through multiple independent lenses, not just "politics" or "conflict." Every serious institutional forecast uses a structured domain framework.

**Why Expected:** Mono-dimensional analysis is the hallmark of superficial forecasting. The ODNI Global Trends (HIGH confidence), UK GST (HIGH), and NATO SFA (HIGH) all converge on a core set of analytical domains. BCG uses 100 megatrends across multiple categories.

**Complexity:** MEDIUM — requires parallel knowledge across fields but is fundamentally structured writing.

**Institutional standard domains (for reference):**
| Source | Domains |
|--------|---------|
| ODNI Global Trends 2040 | Demographics/Human Development, Environment, Economics, Technology |
| UK GST 7 | Society, Economy, Environment (subsystems); Information/Technology, Conflict/Security (ring roads) |
| NATO SFA 2023 | Climate change, Resource scarcity, Disruptive tech, Securitization of economics, Human networks, Global commons, Intl. order transition |
| BCG 2050 | 100 megatrends across regulation, geopolitics, resources, technology |

**Recommended domains for this project** (partially defined in PROJECT.md):
- **Borders & Geopolitics** — territorial control, state viability, alliance/block structure
- **Demographics & Health** — population size, age structure, migration, disease burden
- **Climate & Environment** — temperature, sea level, resource scarcity, ecosystem states
- **Economics & Resources** — economic system type, production, trade, energy, food
- **Technology** — general-purpose technologies, energy tech, biotech, AI, space
- **Culture & Ideology** — dominant belief systems, national narratives, social cohesion
- **Governance & Law** — institutional forms, international law, regime types
- **Conflict & Security** — war forms, WMD proliferation, internal conflict, policing

> **IMPORTANT:** Culture/ideology is the domain most frequently neglected by institutional forecasts (overly economistic), yet for century-scale horizons it may be the most important driver. The QDNI GT mentions it only indirectly; BCG ignores it. This is an opportunity.

### 2. Current-State Baseline

**What:** An explicit description of the world at the starting point (present day) that all projections build from. Not assumed — documented.

**Why Expected:** Without a shared starting point, projections float disconnected from reality. Every serious forecasting project establishes a baseline. The ODNI GT uses "structural forces" analysis grounded in current data. The RAND Australia report explicitly states: "To project forward, it is important to first develop an understanding of the current state of the globe."

**Complexity:** LOW-MEDIUM — mostly data gathering and synthesis. Particularly important because KML boundaries at the starting point must be accurate.

### 3. Temporal Framework with Explicit Milestones

**What:** Clear time-horizon structure. Not a continuous narrative, but defined checkpoints with consistent intervals.

**Why Expected:** Readers need to know what period each analysis covers. The ODNI GT uses a 20-year horizon (2040). UK GST uses 2055. BCG uses 2050. FOI uses 2050 for its China study.

**Complexity:** LOW — the 2050/2075/2100 structure + transition docs is already defined. The differentiator is the uniqueness of the timeline structure itself.

### 4. Structural Forces vs. Emerging Dynamics vs. Scenario Distinction

**What:** Clear epistemological layering. Some things are relatively knowable (demographic trends, climate physics) while others are deeply uncertain (human choices, leadership, geopolitical reactions). These must be distinguished, not blended into one flat prediction.

**Why Expected:** This is the core methodology that separates professional forecasting from amateur speculation. The ODNI GT 2040 explicitly structures itself:
- **Layer 1:** Structural forces (relatively certain, data-grounded) — demographics, environment, economics, technology
- **Layer 2:** Emerging dynamics (more uncertain, choice-dependent) — societal, state, international levels
- **Layer 3:** Scenarios (possible futures from different choice combinations)

The UK GST 7 uses an Impact/Uncertainty matrix. Scenario planning methodology universally distinguishes predetermined elements from critical uncertainties.

**Complexity:** MEDIUM — requires intellectual discipline to maintain the distinction throughout writing.

### 5. Scenario / Alternative Pathway Consideration

**What:** Multiple plausible futures explored, not a single deterministic prediction. The forecast should acknowledge branching points.

**Why Expected:** Single-path forecasting is inherently dishonest at century scale. Every serious institutional project uses multiple scenarios: ODNI GT has 5, UK GST has 5 pathways, BCG has 4, NATO uses "4 Worlds." The FOI China study includes 7 disruptive changes that would overturn its baseline scenario.

**This project already commits to this via the transition documents between milestones.**

**Complexity:** MEDIUM — balanced against depth per path. For a solo project, 3-4 pathways per dimension is likely the max tractable number.

### 6. Cross-Domain Consistency Mechanism

**What:** A systematic way to ensure that assumptions in one domain don't contradict assumptions in another. E.g., if the climate analysis assumes 3°C warming by 2075, the agriculture analysis must reflect that.

**Why Expected:** Inconsistencies between domains are the most common failure mode of multi-domain forecasting. If the political analysis says the US collapses but the technology analysis assumes continued US-funded research, the forecast is internally broken.

**Complexity:** HIGH — requires the most discipline. Mechanistically, this means having a "global assumptions" registry (shared constants file) that all domain documents reference. Every time a domain document changes an assumption, it must check for ripple effects.

### 7. Explicit Uncertainty Communication

**What:** Not all predictions are equally certain. Each major claim should signal its confidence level.

**Why Expected:** The intelligence community (IC Directive 203, STANDARD 5) demands explicit uncertainty language. The Perry World House report (MEDIUM confidence) documents that policymakers prefer percentage probabilities over vague labels like "likely." The FUTARCHY methodology requires confidence intervals with every probability.

**Complexity:** LOW — a simple annotation convention (HIGH/MEDIUM/LOW confidence per claim, or a 3-5 point scale). Does not require Brier scores for this project type (see Anti-Features).

### 8. Regional Coverage

**What:** The forecast must disaggregate to regional level. "Global" analysis that treats the world as homogeneous is superficial.

**Why Expected:** Every institutional forecast includes regional breakdowns. ODNI GT has regional forecasts for Russia/Eurasia, MENA, Sub-Saharan Africa, NE Asia, SE Asia. UK GST covers 9 regions. RAND Australia focuses on Indo-Pacific.

**Complexity:** MEDIUM — each region needs its own treatment across all domains. For a solo project, a consistent template per region is essential to keep scope manageable.

### 9. Source & Evidence Hygiene

**What:** Even for a personal project, claims should rest on identifiable sources or reasoning chains.

**Why Expected:** Without source tracking, the forecast drifts from analysis into opinion. The ISW methodology (HIGH confidence standard for professional intelligence analysis) emphasizes source evaluation, characterization, and extensive footnoting. The FUTARCHY methodology mandates a minimum of 8 sources per forecast.

**Complexity:** LOW-MEDIUM — can be lightweight (inline citations, notes-to-self) for a solo project. Full academic citation style is overkill.

---

## Differentiators

Features that set this project apart from institutional forecasts. Not expected, but offer unique value.

### D1. Century-Scale Horizon (to 2100)

**Value Proposition:** Nearly all institutional forecasting maxes out at 2040-2055. The ODNI GT covers 20 years. UK GST covers to 2055. BCG covers to 2050. This project's 2100 horizon is genuinely rare and enables analysis of long-cycle phenomena (Kondratiev waves, climate full-impact, demographic transitions completing, civilizational cycles).

**Complexity:** HIGH — the further out, the less data-grounding is available. Structural forces give way to pure scenario thinking. Requires different analytical tools for different time depths.

**Mitigation:** The quarter-century checkpoint structure (2050, 2075, 2100) naturally creates telescoping detail: more specific near-term, more structural long-term.

### D2. Map Output (KML Territorial Boundaries at Each Checkpoint)

**Value Proposition:** Forces concrete, falsifiable claims. Anybody can write "China fragments" in prose. Drawing the resulting borders on a map forces specificity about which regions, when, and at what boundaries. This is the project's most powerful differentiator and its primary quality-enforcement mechanism.

**No institutional forecasting project produces mapped territorial outcomes at this timescale.** (HIGH confidence — surveys of ODNI GT, UK GST, NATO SFA, BCG, RAND all show text+charts only.)

**Complexity:** HIGH — requires geographic precision. But the constraint is a feature: if a border change doesn't make sense spatially (enclaves, indefensible shapes, resource denial), it reveals a flaw in the underlying political analysis.

### D3. Explicit Collapse Thesis as a Central Framing

**Value Proposition:** Institutional forecasts are structurally conservative — they assume institutional continuity by mandate (ODNI GT: "to inform US national security strategy"), organizational inertia, and bureaucratic politics. This project's thesis (US empire collapse, capitalist-to-socialist transition) would be politically impossible for ODNI, UK MOD, NATO, or BCG to state as a central framing.

This creates genuinely distinct analytical space. The collapse thesis forces the analyst to consider scenarios that institutional forecasting implicitly rules out.

**Complexity:** MEDIUM — the analytical challenge is avoiding the "collapse as deus ex machina" trap. Every collapse event must be causally grounded in preceding domain analyses.

### D4. Transition Documents Between Milestones

**Value Proposition:** The "big-picture trend" documents connecting 2050→2075→2100 fill a gap that snapshot-only forecasts leave open: how does the world get from one state to the next? Institutional forecasts typically offer scenarios but not causal transition chains.

**Complexity:** MEDIUM-HIGH — requires narrative causal logic. The risk is "just so" storytelling. Mitigation: treat transitions as structured analysis of key dynamics, not prose narrative.

### D5. Cross-Domain Consistency Enforced by Territorial Mapping

**Value Proposition:** Most multi-domain forecasts keep domains in separate silos with minimal cross-referencing. This project's KML output forces integration: the territory claimed by each political entity at each checkpoint must be consistent with its demographic capacity, economic base, climate context, and technological capability.

**No institutional forecast has this integration constraint. It is a genuine architectural innovation.**

**Complexity:** HIGH — requires a systematic cross-reference mechanism. But the KML provides a forcing function that makes the work better.

### D6. Culture & Ideology as a First-Class Domain

**Value Proposition:** Institutional forecasts are dominated by economics (BCG), security (NATO), or demographic-technological determinism (ODNI). Culture and ideology are treated as residual. For century-scale forecasting, belief systems, civilizational identities, and ideological evolution may be the most powerful drivers.

This is a gap in the ecosystem that this project can fill.

**Complexity:** HIGH — the least quantifiable domain. Requires synthesis of history of ideas, sociology, anthropology, and religious studies. Hard to ground in hard data. But the attempt itself is valuable.

### D7. Personal (Non-Institutional) Perspective

**Value Proposition:** Unconstrained by:
- Bureaucratic consensus (no "committee-think")
- Political sensitivities (no "we can't say that")
- Methodological orthodoxy (no "only econometric models count")
- Classification boundaries (no "we can't publish our assumptions")

**Complexity:** LOW — this is naturally the case. The risk is the opposite: unchecked personal bias. Mitigation: structured analytical techniques even for solo use (ACH, pre-mortem, devil's advocate).

### D8. Structured Markdown Format (Not Narrative Prose)

**Value Proposition:** Institutional forecasts are PDF reports with a fixed structure. This project's markdown → directory-per-milestone format enables:
- Cross-linking between domains
- Easy updating/revision of individual sections
- Git-based version tracking
- Machine-readability and future tooling

**Complexity:** LOW — already committed. The key is maintaining the editorial discipline to keep it structured rather than drifting into prose.

### D9. Kondratiev/Extended Economic Cycle Awareness

**Value Proposition:** Most institutional forecasts ignore long-wave economic cycles (Kondratiev waves: ~50-year cycles tied to technological revolutions) and century-scale trends. The academic research on three-layered foresight frameworks (MEDIUM confidence from TU Delft research) shows that incorporating these long cycles improves foresight quality.

For a century-scale forecast, ignoring ~50-year economic cycles would mean missing 2-3 full cycles — a critical structural force.

**Complexity:** MEDIUM — requires familiarity with Kondratiev, long-cycle theory, and world-systems analysis. But the existence of cycles is well-documented.

---

## Anti-Features

Features to explicitly NOT build. Doing them would damage the project's credibility or consume time better spent on core analysis.

### A1. Narrative Fiction / Prose Storytelling

**What:** Writing fictionalized accounts set in the future world (e.g., "As Maria walked through the ruins of Washington...").

**Why Avoid:** Already listed as out of scope in PROJECT.md. Narrative prose creates the illusion of concreteness without analytical discipline. Fictional detail (what Maria wore, what the ruin smelled like) adds no forecasting value. It also takes enormous time for zero analytical return.

**What to Do Instead:** Structured analysis. If you need to make a future concrete, do it through maps, timelines, and specific claims with confidence levels.

### A2. Granular Year-by-Year Predictions

**What:** Specifying what happens in each year from 2026 to 2100.

**Why Avoid:** The further out, the less granularity is epistemically honest. Year-level resolution for a 75-year horizon is pure fiction. Institutional forecasts avoid this for exactly this reason. The ODNI GT gives only 3 time layers (structural forces → emerging dynamics → 2040 scenarios). UK GST gives 1 target year (2055).

**What to Do Instead:** The quarter-century checkpoint structure. Deep detail at 2050, 2075, 2100. Trend documents for transitions. Do not attempt yearly resolution.

### A3. Precise Probability Quantification (Brier Scores, Percentage Probabilities)

**What:** Assigning numerical probabilities to century-scale predictions like "70% chance of US collapse by 2050."

**Why Avoid:** Single-run, non-repeating forecasts cannot be calibrated. Brier scores only work for repeated, resolvable predictions with the same forecaster. A 70% probability that resolves once in 2050 is epistemically meaningless — you can't learn your calibration from one data point. Professional forecasting research (FUTARCHY, RAND, Perry World House) all assumes repeatable resolution for calibration.

> **Note:** This is different from ordinal confidence labels (LOW/MEDIUM/HIGH or 1-5 scale) on individual claims, which are useful even for single-run forecasts.

**What to Do Instead:** Use ordinal confidence labels (LOW/MEDIUM/HIGH per claim). Do not assign percentage probabilities to century-scale predictions.

### A4. Prediction Market Integration

**What:** Tying the project to Polymarket, Metaculus, etc.

**Why Avoid:** Prediction markets operate on sub-year to 1-year timescales. They cannot resolve century-scale questions. Integration would be a gimmick with no analytical value.

**What to Do Instead:** If desired, use prediction markets only for near-term signal (geopolitical trends in 2026-2030 period that inform the forecast's base assumptions). But keep it separate from the core forecasting.

### A5. Formal Delphi Expert Panels

**What:** Conducting structured expert surveys to feed the forecast.

**Why Avoid:** Appropriate for institutional forecasts with budgets and access to subject matter experts. For a solo project, it's overhead without the methodology to do it properly (requires multiple rounds, controlled feedback, statistical aggregation).

**What to Do Instead:** If expert input is desired, rely on published research and think-tank reports as sources. The ISW model shows that rigorous open-source analysis can match government intelligence quality.

### A6. Collaboration / Multi-Author Infrastructure

**What:** Building review systems, permission models, versioning for multiple contributors.

**Why Avoid:** Already out of scope. The project's value proposition is a single coherent vision, not consensus aggregation. Multi-author geopolitical forecasts produce "committee" results that are blander and less interesting.

**What to Do Instead:** Solo author with open-source research inputs. Git for single-user version tracking is fine.

### A7. Fictional Micro-Vignettes or Scenes

**What:** Short narrative inserts ("A day in the life, 2075") to "bring the future to life."

**Why Avoid:** A common trope in futures consulting that adds production time without forecasting rigor. Often used to mask analytical weakness with emotional engagement. Does not belong in a structured forecasting project.

**What to Do Instead:** If concreteness is needed: maps, diagrams, tables, specific data claims. These are harder to write but analytically honest.

### A8. Quantitative Econometric Modeling

**What:** Building formal economic models, system dynamics simulations, agent-based models.

**Why Avoid:** For a solo project, the effort-to-value ratio is terrible. Proper quantitative modeling requires calibration, validation, sensitivity analysis, and domain expertise that exceeds what one person can bring across all domains. A bad model is worse than no model (gives false precision).

**What to Do Instead:** Qualitative structural analysis with reference to existing quantitative projections from IPCC, UN Population Division, IMF/World Bank, etc. Use existing models as inputs, don't build your own.

### A9. Maintaining Multiple Alternative Scenarios as Full Documents

**What:** Writing full alternative versions of each milestone (e.g., "2050 Scenario A: US Remains Strong" and "2050 Scenario B: US Collapses").

**Why Avoid:** For a solo project, branching the entire forecast into parallel universes doubles or triples the work. Institutional forecasts can do this because they have teams of 50+. A solo author maintaining 3 full parallel timelines will never finish any of them.

**What to Do Instead:** In each domain analysis, note key uncertainties and branching points. Acknowledge what alternative paths were considered and why the primary path was chosen. The transition documents are where alternative pathway logic belongs. Only maintain one primary timeline (your best judgment) with uncertainty annotations.

---

## Feature Dependencies

Key relationships between content areas. These dictate ordering and must be respected.

```
Domain Analyses (7 domains)
    |
    v
Domain-specific boundary changes (territorial implications of each domain)
    |
    v
Cross-domain consistency check (do domain boundary changes conflict?)
    |
    v
Unified KML map (resolved territorial boundaries)
    |
    v
    |----> Transition narrative (how did we get here from previous milestone?)
    |
    v
Regional analyses (how do changes affect each world region?)

==============================================================
Inside each domain directory:

Structural Forces (demographics, climate, technology base rates)
    |
    v
Emerging Dynamics (how forces interact with human choices)
    |
    v
Milestone Snapshot (state at target year)
    |
    v
Key Uncertainties (what could change this picture)
    |
    v
Boundary Implications (territorial effects for KML)
```

### Critical Dependency Paths

| If this changes... | ...it affects | Mitigation |
|-------------------|---------------|------------|
| Climate trajectory (e.g., 2°C vs 4°C by 2100) | Agriculture, migration, coastal borders, economics, conflict | Climate baseline must be locked first; all other domains branch from it |
| US collapse timeline | Every other domain: the global order assumption changes | This is the project's central thesis; must be argued in detail before filling in other domains |
| Technology breakthrough (e.g., fusion power by 2040) | Economics, climate (reverse), geopolitics of energy | Tag as a "high-impact uncertainty" with explicit signs to watch for |
| Demographic projection (UN mid vs low variant) | Labor force, economy, migration pressure, conflict risk | Use UN variant range; note which variant is assumed and what changes if it differs |

### Phase Ordering Recommendations

1. **Phase 1: Modern-day baseline + Methodology** — establish the starting point KML, domain templates, cross-domain consistency mechanism, assumption registry
2. **Phase 2: Structural Forces** — demographic, climate, technology base rates (the relatively certain foundations)
3. **Phase 3: US Collapse Thesis** — the central argument that everything else depends on
4. **Phase 4: 2050 Snapshot** — first checkpoint; builds from structural forces + collapse thesis
5. **Phase 5: 2050→2075 Transition** — trends between first two checkpoints
6. **Phase 6: 2075 Snapshot** — second checkpoint
7. **Phase 7: 2075→2100 Transition** — trends between second and third checkpoints
8. **Phase 8: 2100 Snapshot + Final World** — final checkpoint
9. **Phase 9: Map Production** — generate all KML files from the resolved boundary data
10. **Phase 10: Synthesis & Retrospective** — what was learned, what would change, gaps for next edition

### Complexity by Feature

| Feature | Complexity | Priority | Dependencies |
|---------|-----------|----------|--------------|
| Domain coverage (7 domains) | MEDIUM | MUST | None |
| Current-state baseline | LOW-MEDIUM | MUST | Domain structure |
| Temporal framework | LOW | MUST | None |
| Structural vs dynamic distinction | MEDIUM | MUST | Domain coverage |
| Scenario / alternative paths | MEDIUM | SHOULD | Core thesis |
| Cross-domain consistency | HIGH | MUST | All domain docs |
| Uncertainty communication | LOW | MUST | Domain coverage |
| Regional coverage | MEDIUM | SHOULD | Domain coverage |
| Source hygiene | LOW-MEDIUM | MUST | None |
| KML maps | HIGH | MUST | All domain docs, cross-domain consistency |
| Collapse thesis | MEDIUM | MUST | Structural forces |
| Transition documents | MEDIUM-HIGH | MUST | Adjacent milestones |
| Culture/ideology domain | HIGH | SHOULD | Domain coverage |
| Kondratiev cycles | MEDIUM | NICE | Economics domain |

---

## Credibility Markers (What Makes a Forecast Credible vs Superficial)

From synthesis of institutional forecasting best practices:

**Credible forecasts:**
- Distinguish what is relatively knowable from what is highly uncertain
- Acknowledge what would change their conclusions
- Lay out evidence before conclusions
- Show internal consistency across domains
- Use structured analytical techniques (not "I feel like")
- Make specific, falsifiable claims (not vague generalities)
- Document methodology transparently
- Separate data from interpretation from speculation

**Superficial forecasts:**
- Blend all time horizons into one flat narrative
- Make single-path predictions without alternatives
- Make claims without evidence
- Use narrative prose to create the illusion of concreteness
- Are internally inconsistent across domains
- Give specific probabilities for non-repeatable events
- Avoid stating what would prove them wrong
- Depend on unspecified "expertise"

---

## Sources

- ODNI National Intelligence Council, *Global Trends 2040: A More Contested World* (2021) — HIGH confidence, official government forecasting methodology
- UK MOD Development, Concepts and Doctrine Centre, *Global Strategic Trends: Out to 2055, 7th Edition* (2024) — HIGH confidence
- NATO Allied Command Transformation, *Strategic Foresight Analysis 2023* — HIGH confidence
- BCG, "Beyond Tomorrow: Four Scenarios for the World of 2050" (2026) — HIGH confidence
- AlphaGeo, *The Periodic Table of States* (2024) — MEDIUM confidence, well-documented methodology
- FUTARCHY.media, *Our Methodology* (2024) — HIGH confidence for structured analysis principles
- Institute for the Study of War, *Statement on Methodology* (2023) — HIGH confidence for intelligence tradecraft standards
- Perry World House/University of Pennsylvania, *Keeping Score: A New Approach to Geopolitical Forecasting* (2021) — MEDIUM confidence
- OECD, *Foresight Toolkit for Resilient Public Policy* (2025) — HIGH confidence
- FOI Sweden, *When the People's Republic Turns 100* (2024) — HIGH confidence, exemplar of structured long-range analysis
- RAND Australia, *Beyond the Horizon* (2024) — HIGH confidence
- TU Delft, "Integrated Three-Layered Foresight Framework" — MEDIUM confidence, academic source on long-cycle analysis
