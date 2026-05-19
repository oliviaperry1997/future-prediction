# Project Research Summary

**Project:** Future Prediction (Geopolitical Forecasting & World-Building)
**Domain:** Long-range geopolitical futures / structured world-building
**Researched:** 2026-05-19
**Confidence:** HIGH

## Executive Summary

This project produces a structured, multi-century geopolitical forecast from the present day through 2100, organized around three quarter-century milestone snapshots (2050, 2075, 2100) with detailed world maps in KML format for Google Earth. The central thesis — the collapse of the US empire and a transition from capitalism to socialism — distinguishes it sharply from institutional forecasts, which structurally avoid such collapse framings. The research converges on a clear recommendation: **Obsidian as the markdown knowledge base, Python + simplekml for programmatic KML generation, Git for version control, and a structured methodology pairing 2×2 scenario matrices (per domain) with Three Horizons (for transitions) and STEEP domain coverage**. The workflow is purely text-driven: write structured markdown in Obsidian with YAML frontmatter, run Python scripts to produce KML maps, QA in Google Earth Pro.

The critical risk is **the Hedgehog Trap** — the project's compelling central thesis (US collapse → socialism) can easily become a self-validating narrative that filters out contradictory evidence. This is compounded by the **Linear Projection Fallacy** (assuming smooth trends at 50-75 year horizons) and **Motivated Reasoning** (wanting the collapse narrative to be true). The mitigation requires deliberate structural discipline: maintain a prediction register for calibration tracking, write counter-scenarios in equal detail, encode confidence levels on maps, and use cross-impact matrices to prevent domain silos from producing internally contradictory futures. **The single most important practice**: for every forecast the author is confident about, write the version where they are wrong in equal detail.

Research confidence is HIGH across all dimensions. The technology stack (Obsidian + Python + simplekml + Google Earth Pro) is well-documented and stable. The feature landscape (multi-domain coverage, explicit uncertainty communication, cross-domain consistency, KML output) aligns with best practices from ODNI Global Trends, UK GST, NATO SFA, and BCG scenario work. The architecture (directory-per-milestone, domain-organized markdown, modular KML via NetworkLinks) follows established patterns from institutional foresight toolkits. The pitfalls catalog draws from Tetlock's Good Judgment Project, Dorr's forecasting fallacies, and the scenario planning literature — all HIGH-confidence sources.

## Key Findings

### Recommended Stack

The project needs three technology layers plus a methodological framework layer. **Obsidian** is the clear winner for the knowledge base — it is markdown-native, works fully offline, has bidirectional linking and graph visualization, and its file format guarantees no vendor lock-in. The only serious alternative (Logseq) lacks Canvas and plugin maturity. **Google Earth Pro** is already the user's existing KML viewer and is the right tool for QA and manual touch-up — web-based alternatives (CesiumJS, Mapbox) are scope creep. **simplekml** (Python) is the only actively maintained KML generation library; hand-writing XML or using GDAL are both worse options.

**Core technologies:**
- **Obsidian** (latest stable): Interconnected markdown knowledge base — markdown-native, offline, plugin ecosystem (Dataview for YAML querying, Canvas for spatial scenario mapping), zero vendor lock-in
- **Python 3.12+** with **simplekml 1.3.6+**: Programmatic KML generation from YAML frontmatter — validates XML structure, handles shared styles, avoids malformed polygon data
- **Git**: Version control across all milestones — text-based diffing of both markdown and KML XML, ability to branch "what-if" scenarios
- **PyYAML**: Parse YAML frontmatter from Obsidian notes into Python data structures for KML generation
- **Google Earth Pro**: KML visualization and final QA — the already-owned, de facto standard for KML with 3D globe rendering

**Methodological frameworks:**
- **2×2 Scenario Matrix** (Shell/GBN): Per-domain scenario generation — identify two critical uncertainties, generate four futures. Simple enough for solo use, rigorous enough for professional foresight.
- **Three Horizons** (Bill Sharpe): Transition document structure — H1 (declining present), H2 (transitional turbulence), H3 (emerging future). Maps directly to the 2050→2075→2100 transition needs.
- **STEEP/Six Domains** (SRI): Domain taxonomy — the project's existing domains (borders, climate, technology, economy, demographics, culture) fit a proven framework.
- **Backcasting** (Robinson): Start from milestone endpoint, work backward to identify necessary conditions. Complements forward projection.

**Verification tools (optional, in reserve):**
- **shapely**: Validate polygon geometry (no self-intersections, correct winding order) before KML export
- **pandas**: Tabular scenario data manipulation (demographic projections, GDP trajectories)
- **QGIS 3.40+**: Only if complex GIS operations are needed (likely unnecessary)

### Expected Features

The feature research, drawing on ODNI Global Trends (7 editions), UK GST 6 & 7, NATO SFA 2023, BCG scenarios, and other institutional sources, defines a clear expectation set.

**Must have (table stakes):** These define a credible forecast. Missing any of these signals amateur work.
- **Structured domain coverage** (7 domains: borders/geopolitics, demographics, climate, economics, technology, culture, conflict/governance) — every institutional forecast uses a domain framework; mono-dimensional analysis is the hallmark of superficial forecasting
- **Current-state baseline** — explicit starting point documented, not assumed; all projections build from it; KML boundaries must be accurate at t=0
- **Temporal framework with milestones** — the 2050/2075/2100 + transitions structure is already defined; the differentiator is its unique 2100 horizon
- **Structural forces vs. emerging dynamics vs. scenarios distinction** — separates relatively knowable (demographics, climate physics) from deeply uncertain (political choices); this is the core of professional methodology
- **Explicit uncertainty communication** — every major claim gets a confidence label; the IC community (ICD 203) mandates this; ordinal labels (HIGH/MEDIUM/LOW) suffice
- **Cross-domain consistency mechanism** — the most commonly failed dimension; an assumption registry ("global shared constants") prevents contradictions between domain analyses
- **Regional coverage** — disaggregated analysis, not homogenous "global" treatment; consistent template per region
- **Source/evidence hygiene** — even for solo project, claims need identifiable sources or reasoning chains

**Should have (competitive differentiators):** These set the project apart from institutional forecasts.
- **KML map output at each checkpoint** — forces concrete, falsifiable claims about borders and territory; **no institutional forecast produces mapped territorial outcomes at this timescale**; this is the project's strongest differentiator and primary quality-enforcement mechanism
- **Century-scale horizon (to 2100)** — nearly all institutional forecasts max out at 2040-2055; 2100 enables analysis of long-cycle phenomena (Kondratiev waves, climate full-impact, civilizational cycles)
- **Explicit collapse thesis as central framing** — would be politically impossible for ODNI, UK MOD, NATO, or BCG to state; creates genuinely distinct analytical space
- **Transition documents between milestones** — causal chains connecting snapshots, not just snapshot descriptions
- **Culture & ideology as first-class domain** — the most neglected domain in institutional forecasting (overly economistic); may be the most important driver at century scale
- **Kondratiev/extended economic cycle awareness** — 50-year economic cycles mean ignoring them misses 2-3 full cycles over the forecast period

**Defer (v2+):**
- **Multiple full alternative scenarios** — maintaining parallel universes of full milestones is unsustainable for a solo author; note branching points and alternatives within the primary timeline instead
- **Quantitative econometric modeling** — bad model is worse than no model; use existing projections (IPCC, UN, IMF) as inputs

**Anti-features (explicitly NOT to build):**
- Narrative fiction / prose storytelling (zero analytical value, high time cost)
- Granular year-by-year predictions (epistemically dishonest at 75-year horizon)
- Precise probability quantification / Brier scores for century-scale predictions (a 70% probability that resolves once is meaningless)
- Prediction market integration (they operate on sub-year timescales)
- Formal Delphi expert panels (requires methodology the solo project can't sustain)
- Collaboration / multi-author infrastructure (out of scope)
- Fictional micro-vignettes or scenes (masks analytical weakness with emotional engagement)

### Architecture Approach

The project produces two parallel representations for each milestone: **structured markdown** (rationale, logic, descriptions) and **KML polygons** (geographic instantiation). These form a bidirectional pair linked by cross-references (`→ See KML:` in markdown, `See:` back-references in KML descriptions). The architecture is deliberately flat: 3 milestone directories (2050/, 2075/, 2100/), each with domains/ and kml/ subdirectories, plus 3 transition documents at the root. Total file count ~48, each milestone = 14 files.

**Major components:**
1. **Milestone Snapshot Markdown** (7 files per milestone: index + 6 domains) — structured per a uniform template with "Key Changes From Previous Milestone," driving forces, cross-domain interactions, and `→ See KML:` markers linking to geographic features
2. **Milestone KML Layers** (7 files per milestone: doc.kml root + 6 domain KMLs) — modular KML with NetworkLinks for lazy loading, per-domain color schemes, Git-diffable XML, consistent styles across milestones
3. **Transition Documents** (3 files: 2026-2050, 2051-2075, 2076-2100) — narrative-only causal pathway analysis with timeline of key events, driver analysis per domain, causal chain summaries, and cross-domain feedback loops
4. **Master Index** (index.md at project root) — single entry point linking to all milestones, transitions, and basemap documentation
5. **Modern-Day Basemap** (pre-existing KML + BASEMAP_README) — the t=0 starting point for all projections

**Key patterns:**
- **Sequential build order** (recommended): Transition → milestone markdown → milestone KML, repeated per milestone. This lets each milestone's analysis inform the next.
- **Per-milestone domain writing order** (with dependencies): borders → climate → technology → economy → demographics → culture. Each domain depends on the ones before it.
- **Information flow is unidirectional**: Transition (drivers, causal logic) → Snapshot Markdown (state descriptions) → KML (geographic polygons). Each layer adds specificity.
- **Cross-referencing is bidirectional but manual**: markdown-to-KML, KML-to-markdown, transition-to-snapshot, all using consistent text marker conventions
- **KML is kept flat (not KMZ)**: enables individual file editing, Git diffing, and modular loading

### Critical Pitfalls

The pitfalls research, grounded in Tetlock's *Superforecasting*, Dorr's forecasting fallacies analysis, and the scenario planning literature, identifies 10 critical pitfalls plus 4 moderate ones. The most dangerous for this specific project cluster around the central thesis itself.

1. **The Hedgehog Trap** — The single biggest risk. The project's compelling thesis (US collapse → socialist transition) becomes a master narrative that filters evidence and dismisses contradictions. **Prevention:** Write a counter-scenario in equal detail where the thesis does NOT happen. For each major forecast, ask what a Marxist, a realist, a techno-optimist, and a Malthusian would say. Include explicit "What would falsify this forecast?" sections.

2. **Linear Projection Fallacy** — Assuming current trends continue smoothly. At 50-75 year horizons, this is the single most dangerous analytical error. **Prevention:** For every trend, identify the shape (linear, exponential, S-curve, step-function, cyclical) and trigger thresholds. Ask "what would make this go nonlinear?"

3. **End-of-History Illusion (Presentism)** — Projecting today's ideological categories (socialism vs. capitalism, US-China rivalry, nation-states) onto 2100 as if permanent. Look back 75 years from 2026 — how many 1951 categories still apply? **Prevention:** Explicit assumption inventory; radical discontinuity scenario; read historical forecasts from 50-75 years ago.

4. **Motivated Reasoning / Wishful Thinking** — Conclusions aligning with what the author wants to happen. The collapse narrative is emotionally satisfying; this is a direct threat to credibility. **Prevention:** Write the "nightmare scenario" in equal detail. State "I want this to happen, so I should be *more* skeptical of this forecast." Red-team every milestone.

5. **Arrival Fallacy** — Treating milestone snapshots as stable endpoints rather than dynamic moments. The KML format invites endpoint thinking. **Prevention:** Always pair snapshots with a "dynamics" appendix. Use dashed borders for uncertain boundaries. Include "what's emerging" and "what's dissolving" sections.

6. **False Precision** — Maps and forecasts with unjustified specificity at long horizons. A KML polygon showing "Republic of California" in 2050 suggests unwarranted certainty. **Prevention:** Encode confidence via polygon transparency/opacity. Use buffers/zones of ambiguity instead of sharp lines. Include a confidence legend on every map.

7. **Ceteris Paribus Fallacy** — Analyzing one domain while holding all others constant. The project's domain-by-domain structure invites this. **Prevention:** Cross-impact matrices. Build milestones iteratively: draft all domains, cross-check for contradictions, reconcile. Identify 2-3 master variables.

8. **Declinism** — Conflating relative decline with total collapse. Paul Kennedy's timing on US overstretch was famously wrong. **Prevention:** Distinguish absolute decline, relative decline, collapse, and transformation. Write at least one "US adapts" scenario. Use multiple power metrics, not aggregated "US power."

9. **No Calibration Tracking** — The amateur-vs-professional divide. Without tracking, you can't distinguish a skilled forecaster from a confident one. **Prevention:** Maintain a prediction register from day one — specific falsifiable claims with confidence levels and date targets. Review at each milestone. Reference Brier scores and calibration concepts.

10. **Clocklike vs. Cloudlike Confusion** — Treating inherently unpredictable domains (political borders in 2075) as if they were predictable (demographics, climate physics). **Prevention:** Map each domain on a clocklike→cloudlike spectrum. Spend more effort on cloudlike domains via scenarios, not point predictions. Accept that at 50-75 years, almost all political questions are cloudlike.

**Phase-specific warning clusters:**
- **Initial thesis framing:** Hedgehog trap + Declinism + Motivated reasoning (triple threat — address together upfront)
- **Domain analyses:** Ceteris paribus + linear projection + ignoring 2nd-order effects
- **KML map creation:** False precision + arrival fallacy
- **2075/2100 snapshots:** Presentism + far-term fade-out + cloudlike confusion

## Implications for Roadmap

### Phase Structure (Recommended)

Based on combined research across all four dimensions, the following phase structure emerges. The overall arc is: **foundation → structural forces → first milestone → cascade through remaining milestones → synthesis**. The sequential approach (milestone-by-milestone, each fully complete before starting the next) is strongly preferred for a solo project with a strong causal thesis.

#### Phase 1: Foundation & Methodology
**Rationale:** Every subsequent phase depends on the frameworks established here. The baseline must be documented before any projections begin. The anti-hedgehog methodology must exist as a guardrail before the first domain analysis.
**Delivers:** Modern-day basemap documented, domain templates created, cross-domain consistency mechanism defined, prediction register initialized, assumption registry started, STEEP framework adopted, 2×2 matrix methodology defined, uncertainty communication convention locked
**Addresses:** FEATURES #2 (current-state baseline), #4 (structural vs. dynamic distinction), #7 (uncertainty communication), #9 (source hygiene)
**Avoids:** PITFALLS #1 (hedgehog trap — methodology forces counter-scenario writing), #8 (declinism — collapse/decline/distinction established upfront), #4 (motivated reasoning — pre-mortem and devil's advocate steps locked in), #9 (no calibration — prediction register created day one)
**Stack elements used:** Obsidian (vault structure), Git (repo initialized), Python + simplekml (scaffolded), methodological frameworks documented
**Architecture components instantiated:** index.md (master), BASEMAP_README, directory structure (2050/, 2075/, 2100/, transitions/), domain templates

#### Phase 2: Structural Forces Analysis
**Rationale:** Climate physics, demographic trends, and technology base rates are the relatively knowable foundations. These constrain and shape all other domains. Climate trajectory in particular must be locked before borders or economics can be projected.
**Delivers:** Locked climate baseline (2°C vs 3°C vs 4°C scenario), assumed UN demographic variant, technology S-curve projections for key domains (energy, AI, biotech), master assumption registry populated with structural force parameters
**Addresses:** FEATURES #4 (structural forces as Layer 1), builds from feature complexity matrix's critical dependency path (climate must be first)
**Avoids:** PITFALLS #2 (linear projection — structural forces analysis explicitly models non-linearity), #7 (ceteris paribus — cross-impact with master assumption registry)
**Stack elements used:** Python (pandas optional for tabular data), Obsidian (notes), reference to institutional projections (IPCC, UN, IEA)
**Research flag:** Needs deeper research into climate model consensus and demographic variant selection. Medium complexity — well-documented but requires synthesis.

#### Phase 3: Transition 2026-2050
**Rationale:** Before writing the 2050 snapshot, establish the causal arc from present to 2050. This prevents the 2050 snapshot from being written as a static endpoint (arrival fallacy). The transition document becomes the foundation for domain analyses.
**Delivers:** Complete transition document covering timeline of key events (2026-2050), driver analysis per domain, causal chain summary, cross-domain feedback loops, open uncertainties
**Addresses:** FEATURES #5 (scenario/alternative pathways), D4 (transition documents), D7 (personal perspective — the arc is the core contribution)
**Avoids:** PITFALLS #5 (arrival fallacy — transition before snapshot prevents endpoint thinking), #2 (linear projection — timeline of key events forces identification of discontinuities)
**Architecture component:** Transitions/2026-2050.md fully drafted

#### Phase 4: 2050 Snapshot — Domain Analyses
**Rationale:** The first checkpoint. All six domain analyses are written using the templates from Phase 1, grounded in the structural forces from Phase 2 and the causal arc from Phase 3. Must be written in domain dependency order.
**Delivers:** 6 domain markdown files (borders → climate → technology → economy → demographics → culture) + 2050/index.md. Each domain file includes: key changes from present day, per-region analysis with `→ See KML:` markers, driving forces, interactions with other domains
**Addresses:** FEATURES #1 (structured domain coverage), #3 (temporal framework), #5 (scenario/alternative paths noted as branching points), #6 (cross-domain consistency), #8 (regional coverage), D3 (collapse thesis), D6 (culture/ideology as first-class), D8 (structured markdown)
**Avoids:** PITFALLS #3 (presentism — categories explicitly examined), #7 (ceteris paribus — "Interactions With Other Domains" section + cross-impact check), #4 (motivated reasoning — counter-scenarios required per domain), #13 (second-order effects — trace chains required)
**Stack elements used:** Obsidian (writing environment), Git (version tracking), all methodological frameworks
**Architecture components delivered:** 2050/domains/ (6 files), 2050/index.md

#### Phase 5: 2050 KML Map Production
**Rationale:** The geographic instantiation of the 2050 snapshot. Converting domain analyses into KML polygons forces concrete, specific claims and reveals inconsistencies in the written analysis.
**Delivers:** 7 KML files (doc.kml root + 6 domain layers) with confidence-encoded polygons, consistent styling per domain color palette, cross-references back to markdown, reference NetworkLink to modern-day basemap
**Addresses:** FEATURES D2 (KML map output — the project's strongest differentiator), D5 (cross-domain consistency enforced by territorial mapping)
**Avoids:** PITFALLS #6 (false precision — confidence encoding on polygons, ambiguity buffers for uncertain borders), #5 (arrival fallacy — "what's emerging" and "what's dissolving" appended)
**Research flag:** Needs testing of Google Earth NetworkLink behavior with local relative paths on macOS. Well-documented pattern with platform-specific behavior.
**Stack elements used:** Python + simplekml (KML generation from YAML frontmatter), Google Earth Pro (QA), shapely (polygon validation)
**Architecture components delivered:** 2050/kml/ (7 files)

#### Phase 6: Transition 2051-2075
**Rationale:** With 2050 fully defined, the causal arc to 2075 can be built. The 2050 snapshot provides the starting point for this transition.
**Delivers:** Transition document covering 2051-2075 timeline, driver analysis, causal chains, cross-domain feedback loops
**Addresses:** FEATURES D4 (transition documents)
**Architecture component:** Transitions/2051-2075.md fully drafted

#### Phase 7: 2075 Snapshot — Domain Analyses & KML
**Rationale:** The middle checkpoint. The 2075 world builds on the 2050 state via the 2051-2075 transition. Same domain writing order as Phase 4.
**Delivers:** 6 domain markdown files + index + 7 KML files for the 2075 milestone
**Addresses:** All the same feature areas as Phase 4, now at the 2075 horizon
**Avoids:** PITFALLS #12 (far-term fade-out — equal structural treatment to 2050), #3 (presentism — 2075 is far enough out that categories may need radical revision)
**Research flag:** This is where the project's unique value peaks — the midpoint of a century-scale forecast. The evolution from 2050→2075 should reveal convergence or divergence patterns. Medium-high research depth needed for novel geopolitical configurations.
**Architecture components delivered:** 2075/ directory complete

#### Phase 8: Transition 2076-2100
**Rationale:** The final arc. Connects 2075 to 2100. At this horizon, structural forces give way almost entirely to scenario thinking.
**Delivers:** Transition document covering 2076-2100 timeline, driver analysis, causal chains
**Avoids:** PITFALLS #10 (clocklike/cloudlike confusion — at this horizon, almost everything is cloudlike; scenarios replace point predictions)
**Architecture component:** Transitions/2076-2100.md drafted

#### Phase 9: 2100 Snapshot — Domain Analyses & KML
**Rationale:** The final checkpoint. The resolution of the project's central thesis.
**Delivers:** 6 domain markdown files + index + 7 KML files for 2100 milestone
**Avoids:** PITFALLS #10 (cloudlike treatment — use ranges, scenario families, signposts), #3 (presentism — 2100 categories may be unrecognizable)
**Research flag:** HIGH research depth needed. At 2100, there are no institutional forecasts to reference. Pure scenario construction. Counter-scenario work is essential.
**Architecture components delivered:** 2100/ directory complete

#### Phase 10: Synthesis, Map Refinement & Retrospective
**Rationale:** With all three milestones complete, cross-milestone consistency audit, map refinement across all checkpoints, and retrospective analysis.
**Delivers:** Cross-milestone style consistency check, counter-scenario integration, prediction register update, lessons learned, gaps for next edition
**Addresses:** FEATURES D5 (cross-domain consistency at project level), D9 (Kondratiev cycles — long-wave patterns visible only across all three milestones)
**Avoids:** PITFALLS #9 (no calibration tracking — post-hoc review against any resolved predictions)
**Architecture components:** Master index (index.md) finalized with cross-milestone consistency map

### Phase Ordering Rationale

- **Foundation first (Phase 1):** The methodology must exist before any domain analysis begins, because the methodology itself is the primary defense against the top-4 critical pitfalls (hedgehog trap, linear projection, presentism, motivated reasoning). If Phase 1 is skipped, these biases compound across all subsequent phases.
- **Structural forces before projection (Phase 2 before Phases 3-9):** Climate and demographics are the most constraint-heavy domains. Locking their parameters first prevents rework when inconsistencies surface later. The feature dependency analysis and architecture both confirm this ordering.
- **Sequential milestones (Phases 3-5, 6-7, 8-9):** The sequential pattern (transition → domains → KML, repeated per milestone) is strongly recommended over parallel sketching because the project's causal chain is linear — 2050 builds from present, 2075 builds from 2050, 2100 builds from 2075. Writing them sequentially lets each milestone's insights inform the next.
- **Domain writing order within milestones:** Borders first, culture last. This is enforced by the domain dependency chain: territorial framework enables climate analysis, which constrains technology and economy, which shape demographics, which culture sits atop. The architecture research confirms this ordering is optimal.
- **KML after markdown every time:** The KML is the geographic consequences of the domain analysis. Writing KML before the markdown would prioritize map aesthetics over analytical grounding. The bidirectional cross-reference system (markdown → KML and KML → markdown) only works if markdown drives.

### Research Flags

**Phases likely needing deeper research during planning:**
- **Phase 2 (Structural Forces):** Climate model consensus and demographic variant selection require synthesis of IPCC AR7 (or equivalent), UN Population Division projections, and IEA energy scenarios. Well-documented but voluminous. RECOMMEND: dedicated research sub-phase.
- **Phase 5/7/9 (KML Production):** Google Earth NetworkLink behavior with local relative paths on macOS needs platform-specific testing. Standard pattern for KML, but the specific workflow (save from GE → overwrite KML → git commit) needs validation. RECOMMEND: spike test in Phase 1.
- **Phase 9 (2100 Snapshot):** At 2100 horizon, institutional references vanish. Pure scenario construction. Needs the most methodological rigor and counter-scenario discipline. RECOMMEND: dedicated research into century-scale foresight methods.
- **Phase 5 (2050 KML):** KML style library vs. inline-style decision needs to be made. By Phase 5, the team will have enough domains to see the pattern. RECOMMEND: defer decision, decide after 2-3 domain KML files exist.

**Phases with standard patterns (skip research-phase):**
- **Phase 1 (Foundation):** Well-documented patterns for Obsidian vault setup, Git initialization, directory structure. Skip dedicated research — the templates from ARCHITECTURE.md are sufficient.
- **Phase 3/6/8 (Transitions):** The Three Horizons framework and timeline-of-events structure are well-established. Skip dedicated research.
- **Phase 10 (Synthesis):** Retrospective and consistency checking follow naturally from project conventions. No research needed.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All technologies well-documented and stable. Obsidian's plugin ecosystem and offline capability are verified. simplekml is production-grade (stable since Sep 2021). Google Earth Pro is the de facto KML standard. Methodological frameworks (2×2 matrix, Three Horizons, STEEP) are established foresight practice from Shell, UK Government, and UNDP sources. |
| Features | HIGH | Synthesized from 7 editions of ODNI Global Trends (HIGH confidence), UK MOD GST 6 & 7 (HIGH), NATO SFA 2023 (HIGH), BCG 2050 scenarios (HIGH), plus RAND, Perry World House, FOI, and TU Delft research (all MEDIUM-HIGH). The feature landscape is well-understood and the "table stakes vs differentiators vs anti-features" distinction maps cleanly to the project's scope. |
| Architecture | HIGH | KML structure and NetworkLink patterns come from official Google documentation (HIGH). Domain organization mirrors institutional foresight frameworks from UK Government Futures Toolkit (HIGH) and FEMA Strategic Foresight (HIGH). The directory-per-milestone pattern is simple and well-proven. Cross-referencing conventions are manually specified but straightforward. |
| Pitfalls | HIGH | Grounded in Tetlock's *Superforecasting* and *Expert Political Judgment* (HIGH — the foundational research on forecasting accuracy). Dorr's forecasting fallacies (HIGH, peer-reviewed). Gilbert & Quoidbach's "End of History Illusion" (HIGH, published in *Science*). Voros's futures cone (HIGH, widely cited). Burgh & Melo's wishful thinking model (MEDIUM, SSRN preprint). The pitfalls are not speculative — they are empirically documented failure modes. |

**Overall confidence:** HIGH

### Gaps to Address

- **KML NetworkLink behavior on macOS:** The architecture assumes Google Earth Pro handles local relative-path NetworkLinks reliably on macOS. This needs platform-specific testing. Mitigation: test in Phase 1; fallback is opening individual KML files manually.
- **KML style management:** Whether styles should be defined per-file vs. in a shared library depends on observed reuse patterns. Mitigation: defer decision to Phase 5 (2050 KML), after 2-3 domain KMLs exist.
- **Basemap reference strategy:** Whether to copy basemap polygons into each milestone (self-contained) or NetworkLink from a single source (consistent). Mitigation: defer to Phase 5 testing; tradeoff between independence and consistency.
- **Cross-domain coupling depth:** The "Interactions With Other Domains" sections may be sufficient, or a formal dependency matrix may be needed. Mitigation: assess after Phase 4 (2050 domains). If coupling is complex, add matrix in Phase 7 (2075 domains).
- **Counter-scenario vs. primary timeline balance:** The project needs one primary timeline (by scope) plus counter-scenario fragments. The exact balance between "depth in primary" and "breadth in alternatives" is an editorial judgment. Mitigation: Phase 1 methodology should define a ratio (e.g., primary timeline = 80% of effort, counter-scenarios = 20%).

## Sources

### Primary (HIGH confidence)
- **ODNI National Intelligence Council**, *Global Trends 2040: A More Contested World* (2021) — forecasting methodology, domain framework, structural vs. dynamic distinction
- **UK MOD DCDC**, *Global Strategic Trends: Out to 2055, 7th Edition* (2024) — domain taxonomy, scenario methodology, regional coverage
- **NATO Allied Command Transformation**, *Strategic Foresight Analysis 2023* — domain taxonomy, scenario families
- **BCG**, "Beyond Tomorrow: Four Scenarios for the World of 2050" (2026) — century-scale scenario construction
- **Tetlock & Gardner**, *Superforecasting* (2015) — hedgehog/fox distinction, calibration tracking, prediction register methodology
- **Tetlock**, *Expert Political Judgment* (2005) — forecasting accuracy research, ideology and accuracy
- **Dorr**, "Common errors in reasoning about the future: Three informal fallacies" (2017) — linear projection, ceteris paribus, arrival fallacies
- **Gilbert & Quoidbach**, "The End of History Illusion" (2011, *Science*) — presentism bias
- **Voros**, "A Primer on Futures Studies, Foresight and the Use of Scenarios" (2001) — futures cone, scenario methodology
- **Google KML Documentation** — NetworkLinks, KMZ architecture, KML style definitions
- **Obsidian.md** — official product documentation and capabilities
- **simplekml** (PyPI, v1.3.6+) — official library documentation and API reference
- **UNDP Foresight Toolkit** — 2×2 scenario matrix methodology
- **UK Government Futures Toolkit** — PESTLE/STEEP domain categories, driver mapping
- **FEMA Strategic Foresight 2050 Report** — STEEP framework, scenario planning in government
- **RAND** — scenario methodology, stressors-and-shocks framework

### Secondary (MEDIUM confidence)
- **FOI Sweden**, *When the People's Republic Turns 100* (2024) — exemplar of structured long-range analysis
- **Perry World House**, *Keeping Score: A New Approach to Geopolitical Forecasting* (2021) — confidence communication standards
- **FUTARCHY.media**, *Our Methodology* (2024) — structured analysis principles
- **AlphaGeo**, *The Periodic Table of States* (2024) — state classification framework
- **OECD**, *Foresight Toolkit for Resilient Public Policy* (2025) — foresight methodology
- **RAND Australia**, *Beyond the Horizon* (2024) — current-state baseline methodology
- **Burgh & Melo**, "Wishful Thinking is Risky Thinking" (2023, SSRN) — motivated reasoning formal model
- **Kennedy**, *The Rise and Fall of the Great Powers* (1987) — imperial overstretch thesis
- **Milojević**, "Futures Fallacies" (2021, *Journal of Futures Studies*) — ten futures fallacies catalogued
- **TU Delft**, "Integrated Three-Layered Foresight Framework" — long-cycle analysis
- **Bill Sharpe**, Three Horizons framework (International Futures Forum) — transition document methodology

### Tertiary (LOW confidence — needs validation)
- **StackOverflow: Building Large KML Files** — NetworkLink + Folder patterns (practitioner knowledge, confirmed by official docs)
- **Geopol-Forecaster project (danielrosehill)** — SITREP-first document architecture (single open-source project, patterns partially validated)
- **Aerotas KML Workflow Guide** — Google Earth Pro polygon creation workflow (operational guide, not authoritative)
- **John Robinson**, "Future subjunctive: backcasting as social learning" (2003) — backcasting methodology (academic, lower citation count)
- **Rasmus**, "The Top Ten Ways Scenario Planning Can Go Wrong" (2025) — practitioner perspective, secondary to Tetlock/Dorr

---

*Research completed: 2026-05-19*
*Ready for roadmap: yes*
