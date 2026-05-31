---
phase: 20-africa-and-america-re-review
plan: 01
subsystem: research
tags: [research, discovery, nigeria, CAR, domain-audit, africa, americas]

# Dependency graph
requires:
  - phase: 19-antarctica-review
    provides: Completion of all regional reviews, enabling Africa & Americas re-review phase
provides:
  - Nigeria state allocation table (15 AES / 21+FCT Nigeria) per D-04
  - CAR reassessment determination (PLAUSIBLE — 9 southern prefectures to EAF)
  - Domain doc state audit (counts per subregion, creation priority, reorganization needs)
  - Cameroon fragmentation impact assessment (1→3 entities)
affects:
  - 20-02-PLAN.md (KML border changes — entity-config.json admin1_regions update)
  - 20-03-PLAN.md (borders-geopolitics Africa restructure)
  - 20-04-PLAN.md (borders-geopolitics Americas restructure)
  - 20-05-PLAN.md (Africa economy & demographics profiles)
  - 20-06-PLAN.md (Americas economy & demographics profiles)
  - 20-07-PLAN.md (Culture, climate & technology profiles)
  - 2050-snapshot/kml/entity-config.json
  - 2050-snapshot/domains/borders-geopolitics.md
  - 2050-snapshot/domains/economy.md
  - 2050-snapshot/domains/demographics.md
  - 2050-snapshot/domains/culture.md
  - 2050-snapshot/domains/climate.md
  - 2050-snapshot/domains/technology.md

# Tech tracking
tech-stack:
  added: []
  patterns: []

key-files:
  created:
    - ".planning/phases/20-africa-and-america-re-review/20-DISCOVERY.md"
  modified: []

key-decisions:
  - "Nigeria allocation (D-04): AES gets 15 states (Muslim-majority north + Kwara + Adamawa + Taraba); Nigeria gets 21 states + FCT (including Plateau, Nasarawa, Benue, Kogi moved from AES). 5 states move AES→Nigeria; 0 move Nigeria→AES."
  - "CAR reassessment: Southern CAR EAF absorption PLAUSIBLE (MEDIUM confidence). 9 southern prefectures added to EAF admin1; 7 northern prefectures remain contested/reduced CAR entity. Existing borders-geopolitics narrative consistent — requires expansion not rewrite."
  - "Cameroon fragmentation confirmed: 1 entry → 3 (AES North, Ambazonia, Rump Cameroon) needed across all domain docs."
  - "Domain doc creation ordering: borders-geopolitics (Wave 1) → economy+demographics (Wave 2) → culture+climate+tech (Wave 3). ~125 effective entities, ~750 individual sub-entries needed."
  - "Entity-config Africa folder lists ~35 entities but excludes 5 APR North African states — these need domain doc profiles under Africa > Northern Africa despite APR meta-entity."

patterns-established: []

requirements-completed: [AFAM-01, AFAM-02]

# Metrics
duration: 47min
completed: 2026-05-31
---

# Phase 20 Plan 01: Discovery & Research Summary

**Nigeria state allocation (15→AES, 21+FCT→Nigeria), CAR reassessment (PLAUSIBLE), and full domain doc state audit for ~125 Africa & Americas entities — all 3 research deliverables in 20-DISCOVERY.md (418 lines)**

## Performance

- **Duration:** 47 min
- **Started:** 2026-05-31T09:00:00Z
- **Completed:** 2026-05-31T09:47:00Z
- **Tasks:** 3
- **Files created:** 1 (20-DISCOVERY.md)

## Accomplishments

- **Nigeria state allocation (Task 1):** Applied D-04 criteria (Muslim-majority >50% + contiguity + FCT-with-Nigeria) across all 36 states + FCT using Pew, Afrobarometer, CIA World Factbook, State Dept IRF, and Statista data. Result: AES gets 15 Muslim-majority states (core north + Kwara, Adamawa, Taraba); Nigeria gets 21 states + FCT (including Plateau, Nasarawa, Benue, Kogi reassigned from AES). Both zones verified contiguous. 5 states move AES→Nigeria; 0 move Nigeria→AES.
- **CAR reassessment (Task 2):** Evaluated EAF absorption of southern CAR against 6 factors: DRC member as vector, Russian patron withdrawal, rubber-banding effect, economic alignment, Chad domino dynamic, and low absorption cost. Ruled PLAUSIBLE at MEDIUM confidence. 9 southern prefectures (Bangui, Lobaye, Ombella-M'Poko, Sangha-Mbaéré, Basse-Kotto, Mbomou, Haut-Mbomou, Kémo, Nana-Grébizi) allocated to EAF admin1. 7 northern prefectures remain contested/reduced CAR.
- **Domain doc state audit (Task 3):** Read all 6 STEEP domain docs (economy 976 lines, demographics 1046, culture 600, climate 428, technology 168, borders-geopolitics 1040). Documented per-subregion entity profile counts. Grand total: ~125 effective entities (35 Africa config + 5 APR members + 85 Americas) needing ~750 individual sub-entries across 6 docs.
- **Cameroon fragmentation impact:** Confirmed 1→3 entity expansion needed (AES North, Ambazonia, Rump Cameroon) across all domain docs.
- **US successor states counted:** 24 existing profiles in economy + demographics + culture need v1.1 format conversion and integration into Northern America section.

## Task Commits

All 3 tasks contributed to the single 20-DISCOVERY.md artifact — committed as one atomic deliverable:

1. **All tasks (shared artifact):** `c2a17c0` (docs)

**Plan metadata:** (included in same commit)

## Files Created/Modified

- `.planning/phases/20-africa-and-america-re-review/20-DISCOVERY.md` — 418-line discovery document covering Nigeria allocation, CAR reassessment, and domain doc state audit

## Decisions Made

- **Nigeria allocation (D-04 applied):** AES = 15 states (Sokoto, Zamfara, Katsina, Kano, Jigawa, Yobe, Borno, Bauchi, Gombe, Kebbi, Niger, Kaduna, Kwara, Adamawa, Taraba). Nigeria = 21 states + FCT (including Plateau, Nasarawa, Benue, Kogi reassigned from AES; FCT forced to Nigeria). Net config change: AES 20→15 regions; Nigeria 17→22 regions.
- **CAR reassessment:** Southern CAR EAF absorption is PLAUSIBLE (MEDIUM confidence). Existing borders-geopolitics narrative (line 427) is consistent — requires expansion with specific prefectures, not a rewrite.
- **Cameroon fragmentation:** Confirmed as 1→3 entity split. AES North (3 northern regions), Ambazonia (2 Anglophone regions), Rump Cameroon (5+ Francophone regions).
- **Domain doc creation priority:** borders-geopolitics (Wave 1, reorganizes existing content) → economy + demographics (Wave 2, new profiles with USSS conversion) → culture + climate + technology (Wave 3, new profiles for all entities).
- **APR North African coverage:** Egypt, Libya, Tunisia, Algeria, Sudan are in APR meta-entity but need individual domain doc profiles under Africa > Northern Africa. This adds 5 entities beyond the 35 in the entity-config Africa folder.

## Deviations from Plan

None — plan executed exactly as written. All 3 research tasks completed and documented in 20-DISCOVERY.md.

### Auto-fixed Issues

None. Plan was a research/discovery plan with no code or infra changes.

## Issues Encountered

None. Web research sources (Pew, Afrobarometer, CIA World Factbook) provided sufficient data for all determinations. CAR assessment confidence capped at MEDIUM due to inherent uncertainty in EAF governance trajectory — documented in DISCOVERY.md.

## User Setup Required

None — research-only plan with no external service configuration.

## Next Phase Readiness

- **Plan 02 (KML Border Changes):** Ready to proceed. Nigeria state allocation table provides exact admin1_regions lists for entity-config.json. CAR prefecture allocation provides EAF admin1 additions. Cameroon 3-way fragmentation documented.
- **Plans 03-04 (borders-geopolitics restructure):** Ready. Domain doc state audit provides precise existing content vs gaps. Reorganization plans documented per D-07.
- **Plans 05-07 (domain profile creation):** Ready. Entity count summary by subregion provides exact number of profiles needed per doc. US successor states counted for v1.1 format conversion.

---

*Phase: 20-africa-and-america-re-review*
*Completed: 2026-05-31*
