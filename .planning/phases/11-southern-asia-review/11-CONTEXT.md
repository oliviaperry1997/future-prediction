# Phase 11: Southern Asia Review - Context

**Gathered:** 2026-05-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Plausibility audit of Southern Asian entities in the 2050 snapshot. Covers 8 entities: Afghanistan, Bangladesh, Bhutan, India, Maldives, Nepal, Pakistan, Sri Lanka. Verify each against the revolutionary feedback loop and established dynamics, fix KML (wip) tags, fill documentation gaps.

**Key structural finding from this discussion:** Southern Asia does NOT produce a regional federation or bloc. India's reactionary Hindu nationalism and Pakistan's collapse make regional integration impossible — all 8 entities remain sovereign. No SAARC successor. Each entity gets individual KML polygons (Southern Asia (wip) folder restructured to remove (wip) tag, entities stay individual). India gets full standard-depth profile expansion (its existing entries are too brief). Pakistan and Afghanistan are reassessed within the feedback loop framework — the "failed state" narrative is not a final position. The 5 smaller entities (Bangladesh, Nepal, Bhutan, Sri Lanka, Maldives) all get standard-depth profiles.

</domain>

<decisions>
## Implementation Decisions

### India — Trajectory & Depth

- **D-01:** India's **reactionary trap holds through 2050**. RSS/BJP structural dominance deepens: electoral autocracy entrenched, economic growth is capital-intensive and jobless, graduate unemployment crisis continues (40%+ among 15-25 year olds), talent flight of secular and minority professionals accelerates. The democratic-revolutionary alternative does not materialize by 2050. Researcher should confirm or challenge this based on current trajectory evidence.
- **D-02:** **Territorial integrity holds.** No secessionist movement achieves independence by 2050. Kashmir and the Northeast remain contested — Khalistan, Manipur, Tamil separatist pressures intensify but are contained by RSS centralisation project and strong national identity.
- **D-03:** **BRICS+ awkward member** — India stays in BRICS+ as a hedging vehicle (economic pragmatism) but is an uncomfortable, difficult member. It does not align with the Quartet, nor does it pursue genuine non-alignment. India's BRICS+ participation is economic-pragmatic, not political-revolutionary.
- **D-04:** India gets **full standard-depth profiles** across all domain docs — borders-geopolitics paragraph expanded to Russia/Turkey/India depth, economy.md expanded beyond current ~8 lines, demographics.md verified/expanded, culture.md profile added, climate.md profile added.

### Pakistan — Trajectory & Depth

- **D-05:** Pakistan's **"failed state in all but name" framing is not a valid final position within the feedback loop framework**. The researcher should reassess Pakistan's trajectory — it may be a deepening reactionary trap (military-Islamist patronage network survives), a revolutionary flip candidate (collapse triggers political opening), or a partial fragmentation case (Balochistan, Pashtunistan, Sindh movements mature). No pre-decided answer — research determines the most plausible trajectory.
- **D-06:** Pakistan gets **standard-depth profiles** regardless of which trajectory the researcher identifies — economy, demographics, culture, climate. The Quartet role (nuclear deterrent anchor) must be integrated into the profile.
- **D-07:** Pakistan's Quartet role (providing the nuclear deterrent for Turkey-Saudi Arabia-Egypt-Pakistan security architecture) is a fixed decision from prior phases — this is not re-litigated. Pakistan's domestic trajectory is what's being reassessed.

### Afghanistan — Trajectory & Depth

- **D-08:** Afghanistan's **"beyond the loop" classification is reassessed within the feedback loop framework**. The transition doc classified it as having insufficient state structure for either feedback dynamic. The researcher should apply the loop properly: identify which stage Afghanistan is at (likely Stage 1 reactionary — Taliban as reactionary driver), what the forcing mechanisms are, and whether a flip, fracture, or integration pathway is plausible by 2050.
- **D-09:** Afghanistan's **KML entity is added to the Southern Asia folder** — it was removed from Central Asia in Phase 6 (D-13) and has had no KML home since. This phase gives it one.
- **D-10:** Afghanistan gets treatment appropriate to its assessed trajectory — at minimum a borders-geopolitics entry; domain profiles if the loop assessment warrants it.

### Regional Structure — No Federation

- **D-11:** **No Southern Asian federation or regional bloc forms by 2050.** India's reactionary Hindu nationalism and Pakistan's collapsed state make SAARC evolution impossible. All 8 entities remain sovereign. No merged KML polygon.
- **D-12:** **KML restructure:** Remove the `"Southern Asia (wip)"` parent folder from entity-config.json and borders.kml. Replace with individual entity entries (same pattern used for Eastern Europe entities post-Phase 8). Each entity gets its own polygon entry with (wip) removed.

### Smaller Entities — Standard-Depth Profiles

- **D-13:** **Bangladesh, Nepal, Bhutan, Sri Lanka, and Maldives all get standard-depth profiles** — economy, demographics, culture, climate for each. Same depth as India and Pakistan.
- **D-14:** Bangladesh's feedback loop trajectory is **research to determine** — climate crisis (delta flooding, ~15M climate migrants from Bangladesh delta per demographics.md), rapid development, and authoritarian-civilian governance create complex dynamics. Researcher assesses which direction the loop resolves.
- **D-15:** Nepal, Bhutan, Sri Lanka, and Maldives trajectories are **research to determine** — the researcher applies the feedback loop to each and identifies their stage and direction.
- **D-16:** Maldives is a **climate-existential case** — sea level rise of 0.35m+ by 2050 threatens habitability of low-lying atolls. The researcher should assess whether Maldives survives as a sovereign entity or becomes a climate-displacement case (population relocated to India or SEAF).

### India-Pakistan Border — Kashmir & Tri-Junction

- **D-17:** Kashmir remains a **frozen conflict** through 2050. The Line of Control is not resolved — no formal partition, no Indian absorption, no escalation to full conventional war. Pakistan's collapse weakens its military pressure on the LoC but does not force a resolution. India's RSS nationalism prevents negotiated partition.
- **D-18:** The **India-Pakistan-China tri-junction unclaimed zone** (Bir Tiwil area): this is part of the Pakistani claim per the user. The researcher should confirm the precise geography and assign it to Pakistan's territory in the 2050 snapshot — a minor territorial clarification.

### Agent's Discretion

- Exact feedback loop stage assignments for Nepal, Bhutan, Sri Lanka, Maldives (researcher determines)
- Whether Pakistan's trajectory resolves as reactionary deepening, revolutionary flip, or fragmentation
- Afghanistan's precise loop stage and profile depth
- Order of KML entity cleanup and domain doc updates within the phase wave structure
- Whether any Southern Asian entity warrants a culture.md or technology.md entry beyond the standard five domains

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Revolutionary Framework
- `meta/predictions/prediction-002-revolutionary-feedback-loop.md` — The revolutionary feedback loop framework. Stage 2-5 paths, all stage definitions. Required for assessing Pakistan, Afghanistan, and the 5 smaller entities.

### Transition Analysis — Southern Asia Section
- `2026-2050-transition/regions/asia.md` §2 (lines 39-49: India reactionary trap analysis) — Primary India analysis. RSS structural dominance, graduate unemployment, talent flight, US coercion phase. Use as baseline; researcher may update.
- `2026-2050-transition/regions/asia.md` §2 (line 49: Pakistan entry) — Brief Pakistan assessment ("full reactionary collapse"). This framing is superseded by D-05 — researcher reassesses.
- `2026-2050-transition/regions/asia.md` §3 (line 50: Bangladesh) — Brief mention only ("functional state"). Researcher expands.
- `2026-2050-transition/regions/asia.md` §9 (lines 113-114: Afghanistan) — "Beyond the loop" framing. Superseded by D-08 — researcher reassesses within loop.
- `2026-2050-transition/regions/asia.md` (lines 130-142: loop stage table) — Stage table for all Asian entities. India Stage 3-4 Degradation, Pakistan Stage 4-5 Degradation+Fractures. Update table with new assessments.

### 2050 Snapshot Domain Docs (need Southern Asia updates)
- `2050-snapshot/domains/borders-geopolitics.md` (line 382: India brief entry) — Expand India entry to full standard-depth paragraph. Add entries for Pakistan, Bangladesh, Nepal, Bhutan, Sri Lanka, Maldives, Afghanistan.
- `2050-snapshot/domains/economy.md` (lines 425-432: India ~8-line entry) — Expand India. Add Pakistan, Bangladesh, Nepal, Bhutan, Sri Lanka, Maldives entries.
- `2050-snapshot/domains/demographics.md` (line 410: India entry; lines 79,82: climate migration refs to Bangladesh and South Asia) — Expand India. Add all remaining entities.
- `2050-snapshot/domains/culture.md` — Add India, Pakistan, Bangladesh, Nepal, Bhutan, Sri Lanka, Maldives cultural profiles.
- `2050-snapshot/domains/climate.md` — Verify/add Southern Asia climate coverage: Himalayan glacier retreat, monsoon destabilization, Bangladesh delta flooding, Maldives sea-level existential threat, South Asian heat mortality.

### KML Files & Entity Config
- `2050-snapshot/kml/entity-config.json` (folder_hierarchy "Southern Asia (wip)" section) — Remove (wip) folder, add individual entity entries. Add Afghanistan entry.
- `2050-snapshot/kml/borders.kml` — Find Southern Asia (wip) folder, replace with individual country polygon entries. Add Afghanistan polygon.

### Prior Phase Context
- `.planning/phases/06-central-asia-review/06-CONTEXT.md` (D-13, D-14) — Afghanistan deferral decision. D-13: removed from Central Asia KML. D-14: "beyond the loop" framing — superseded by D-08 of this phase.
- `.planning/phases/10-southeast-asia-review/10-CONTEXT.md` — SEAF single-polygon model and sub-entry depth reference. Southern Asia does NOT follow SEAF model (D-11) — all entities remain sovereign.
- `.planning/phases/08-eastern-europe-review/08-CONTEXT.md` — Individual entity KML pattern reference (Russia, Belarus, Ukraine separate polygons). Southern Asia follows this model.

### Established Cross-References (existing docs citing Southern Asia)
- `2050-snapshot/domains/economy.md` line 72 — India as BRICS+ member. Confirm India BRICS+ awkward-member status aligns with D-03.
- `2050-snapshot/domains/economy.md` line 135 — Talent flight from India noted in labor mobility section. Confirm alignment with D-01.
- `2050-snapshot/domains/demographics.md` lines 79, 82 — Bangladesh delta migration (~15M) and South Asia monsoon belt migration (~10M). These figures feed into Bangladesh and Pakistan profiles.
- `2050-snapshot/domains/borders-geopolitics.md` line 450 — Quartet entry (Turkey-Saudi-Egypt-Pakistan). Pakistan profiles must align with this established Quartet role.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Individual entity KML pattern (Phase 8 Eastern Europe) — Russia, Belarus, Ukraine kept as separate polygons with (wip) removal. Same pattern applies to all 8 Southern Asian entities.
- Entity-config individual entry structure — Kazakhstan, Kyrgyzstan etc. (CAC) pattern for adding individual sovereign entities. Apply to Bangladesh, Nepal, Bhutan, Sri Lanka, Maldives, Afghanistan.
- Standard-depth profile format (economy.md) — India entry at lines 425-432 is the baseline; Russia/Turkey entries show standard full depth. Expand India to Russia/Turkey depth; write others at same depth.

### Established Patterns
- (wip) removal via folder restructure — "Southern Asia (wip)" folder in entity-config.json replaced with individual entity entries under Eurasia parent.
- Wave structure from prior phases: KML + entity-config (Wave 1) → borders-geopolitics.md (Wave 2) → domain docs economy + demographics (Wave 3) → culture + climate (Wave 4).
- Quartet entry (borders-geopolitics.md line 450) — Pakistan profiles must be written to align with this existing collective entry, not contradict it.

### Integration Points
- entity-config.json: Remove `"Southern Asia (wip)"` group. Add individual entries for: Bangladesh, Bhutan, India (likely already exists), Maldives, Nepal, Pakistan, Sri Lanka, Afghanistan.
- borders-geopolitics.md Asia section: Add individual entries for all 8 entities. India entry expands; others are new.
- economy.md BRICS+ section (line 72): India confirmed as BRICS+ member — awkward member characterization.
- Territorial Integrity verification table (borders-geopolitics.md line 490): India entry exists — verify and update. Add Pakistan, Bangladesh entries.

</code_context>

<specifics>
## Specific Ideas

- India's reactionary trap is the defining dynamic of Southern Asia — the region's inability to integrate is a direct consequence of India's RSS nationalism. This makes Southern Asia the "anti-SEAF" of the 2050 world: a region that should have integrated but couldn't.
- Pakistan's Quartet nuclear deterrent role is established — whatever the domestic trajectory, Pakistan retains nuclear capability as its primary strategic asset and Quartet contribution.
- The India-Pakistan-China tri-junction unclaimed zone (Bir Tiwil area) is part of the Pakistani claim — assign to Pakistan in the 2050 snapshot.
- Maldives as climate-existential case: sea level rise of 0.35m+ threatens atolls. The researcher should assess whether the Maldivian state survives as a sovereign entity or the population is climate-displaced by 2050.
- Bangladesh delta: ~15M climate migrants already noted in demographics.md. The researcher should integrate this into Bangladesh's demographic and economic profile — it's not a background fact but the central dynamic of Bangladesh's 2050 situation.
- The "beyond the loop" classification for Afghanistan should be understood as a diagnostic failure of the early framework, not a final verdict. Apply the loop properly: Taliban is a Stage 1 reactionary driver; the question is whether the forcing mechanisms (climate stress, Chinese BRI dependency, Pakistani collapse next door) produce any trajectory by 2050.

</specifics>

<deferred>
## Deferred Ideas

- **Post-2050 India trajectory** — Whether India's jobless growth crisis produces a political rupture that breaks RSS dominance in the 2050s-2060s. The transition doc flags this as a HIGH uncertainty. Deferred to 2075 snapshot phase.
- **SAARC successor or Southern Asian economic zone** — If India's reactionary trap eventually breaks, a post-2050 regional integration scenario becomes plausible. Deferred to 2075.
- **Maldives post-habitability governance** — If the Maldivian state effectively ceases (population relocated), what legal/territorial successor entity exists? Complex international law question. Deferred.
- **India-China border dynamics** — Himalayan border disputes (Aksai Chin, Arunachal Pradesh) between India and China. The US patron removal affects India's posture. Detailed analysis deferred to Western Asia or a future pass.

</deferred>

---

*Phase: 11-southern-asia-review*
*Context gathered: 2026-05-28*
