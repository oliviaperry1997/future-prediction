# Phase 20: Africa and America Re-review - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-31
**Phase:** 20-africa-and-america-re-review
**Areas discussed:** Phase scope, Northern America depth, KML scope, Cameroon/CAR fragmentation, Documentation format, Northern America format, Sahel-Nigeria border, Work organization, Cameroon boundaries, Nigeria partition details, CAR reassessment, Section organization

---

## Phase Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Split: Africa Phase 20, Americas Phase 21 | Africa (35 entities) as Phase 20, Americas (85 entities) as a separate follow-on phase | |
| Single mega-phase: all 120 entities | One phase covering both Africa and Americas | ✓ |
| Split by UN subregion (8+ phases) | Each subregion gets its own phase | |

**User's choice:** Single mega-phase
**Notes:** These continents are merged because the user already reviewed them outside of GSD workflows — they're mostly done already. Aside from some potential minor KML changes around West Africa, the main concern is bringing documentation up to the same level as the other continents.

## Northern America Depth

| Option | Description | Selected |
|--------|-------------|----------|
| Audit-level check | Review existing profiles for consistency with revolutionary feedback loop; no full rewrite | |
| Full re-review | Entity-by-entity re-assessment matching prior v1.1 depth for every successor state | ✓ |

**User's choice:** Full re-review, but focused on format conversion
**Notes:** Building up the documentation profiles to make sure they're at the same level of depth as the rest of the project. The content already exists from Phase 3-4 — this is about structural format conversion to v1.1 format with → See KML markers.

## KML Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal KML changes | Only fix KML entity mismatches or naming issues found during review | |
| Full KML audit | Systematically verify every Africa/America entity polygon, entity-config entry, and user_colors entry | ✓ |

**User's choice:** Targeted KML changes, not full audit
**Notes:** Minor border changes: reworking the border between Sahel and Nigeria, possible Cameroon and CAF fragmentation.

## Cameroon & CAR Fragmentation

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — create fragment KML entities | Split Cameroon into 3 and CAR into 2 KML entities | |
| No — keep current single entities | Leave them as single KML entities | |
| Yes for Cameroon, skip CAR | Cameroon fragmentation is more consequential; leave CAR single | ✓ (variant) |

**User's choice:** "Cameroon split, CAR reassess"
**Notes:** Cameroon split is confirmed. CAR needs reassessment to determine if the split is plausible before implementing.

## Documentation Format

| Option | Description | Selected |
|--------|-------------|----------|
| Entity-by-entity sub-entries | Individual profiles for each of 120 Africa/Americas entities, matching prior v1.1 format | ✓ |
| Consolidated regional entries | Broader regional profiles per subregion rather than per-entity | |

**User's choice:** Entity-by-entity sub-entries

## Northern America Format

| Option | Description | Selected |
|--------|-------------|----------|
| Full v1.1 format conversion | Update all 40 Northern America entities to match v1.1 sub-entry format with → See KML markers | ✓ |
| Existing format is fine | Keep existing Phase 3-4 format | |

**User's choice:** Full v1.1 format conversion

## Sahel-Nigeria Border

| Option | Description | Selected |
|--------|-------------|----------|
| Current partition is correct | Proceed with existing Sahel-Nigeria boundary in entity-config | |
| Need to adjust some states | Some states along the border should move between AES and Nigeria rump | ✓ |

**User's choice:** Need to adjust
**Notes:** Muslim-majority northern region goes to AES, rest goes to Nigeria. Unsure exactly which states go where (use researcher). They should be contiguous with one another. Nigeria should still hold the FCT.

## Work Organization

| Option | Description | Selected |
|--------|-------------|----------|
| 2 plans: Africa docs + Americas docs | Plan 1: all Africa entity profiles across 5 docs. Plan 2: all Americas entity profiles across 5 docs | |
| Multiple plans per subregion | Each subregion gets its own plan (Western Africa, Caribbean, etc.) | ✓ |

**User's choice:** Multiple plans per subregion

## Cameroon Boundaries

| Option | Description | Selected |
|--------|-------------|----------|
| Anglophone regions (NW + SW) | Ambazonia = Northwest and Southwest regions of Cameroon | ✓ |
| Researcher discretion | Let the researcher determine the exact boundaries | |

**User's choice:** Anglophone regions (NW + SW)

## Nigeria Partition Details

| Option | Description | Selected |
|--------|-------------|----------|
| Benue and Kogi stay with AES | Keep the current border | |
| Move Benue and Kogi to Nigeria rump | These Middle Belt states should be part of Nigeria | |
| You'll specify in the plan | The planner/executor will need to check with you on specific state allocations | ✓ (conceptually) |

**User's choice:** Researcher determines from religious demographics
**Notes:** Muslim-majority → AES, rest → Nigeria. Contiguous. FCT stays with Nigeria.

## CAR Reassessment

| Option | Description | Selected |
|--------|-------------|----------|
| Keep single entity with contested-north narrative | CAR remains one KML entity | |
| Split into 2 KML entities | Create EAF-administered south and contested north as separate KML placemarks | |
| Reassess first | Check plausibility before deciding | ✓ |

**User's choice:** Reassess to see if the split is plausible.
**Notes:** If plausible: add CAR admin1 regions to EAF (don't create separate entity), remove from CAR. If not: keep single entity, rewrite docs.

## Section Organization

| Option | Description | Selected |
|--------|-------------|----------|
| Consolidate all Americas under one section | One Americas section with all entities | |
| Keep separate US section + new Americas subsection | Add new Africa and Americas sections alongside existing US Successor States | ✓ (reorganized) |

**User's choice:** Sort by UN geoscheme, remove "US Successor States" distinction.
**Notes:** Northern America, Central America, South America, Caribbean, Africa subregions.

---

## Agent's Discretion

- Exact Nigeria state allocation (researcher determines from Nigeria admin1 religious demographic data)
- CAR reassessment outcome (researcher judges plausibility)
- Exact plan boundaries per subregion
- Entity depth variation within standard v1.1 format
- Whether any subregions can be combined

## Deferred Ideas

None — discussion stayed within phase scope.
