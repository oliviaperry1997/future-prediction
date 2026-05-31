---
phase: 20-africa-and-america-re-review
plan: 04
subsystem: borders-geopolitics
tags: [americas, restructure, un-geoscheme, v1.1-format]
dependency_graph:
  requires: []
  provides: [AFAM-02]
  affects: []
tech-stack:
  added: []
  patterns: [v1.1-entity-format, un-geoscheme-organization]
key-files:
  created: []
  modified:
    - 2050-snapshot/domains/borders-geopistics.md
decisions: []
metrics:
  duration: "~15min"
  completed_date: "2026-05-31"
---

# Phase 20 Plan 04: Americas sections restructure to UN geoscheme with v1.1 format

**One-liner:** Americas sections in borders-geopolitics.md reorganized from 5 legacy headers (Former United States Territory, North America Beyond Former US, Caribbean, South America, Gran Colombia, Central America) to 4 UN geoscheme subregions (Northern America, Caribbean, Central America, South America) with all ~85 entities converted to v1.1 structured format including → See KML markers.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Reorganize Americas into UN geoscheme headers with Northern America integration | `3cb8bd4` | `2050-snapshot/domains/borders-geopolitics.md` |

## Detailed Outcomes

### Structural Changes

- **Northern America** (new section): Integrated all US successor states (~30 entities: revolutionary, indigenous, reactionary, degrading rumps) with Canadian successor states (Canada rump, Quebec Republic, Maritime Republic, Newfoundland, Manitoba, Denendeh, Inuit Nunangat) plus St. Pierre and Miquelon, absorbed Canadian territory notes, and Labrador Triangle flashpoint
- **Caribbean** (preserved + formatted): Existing 28+ entity entries preserved with `**Caribbean:**` sub-header added; all entities retain their → See KML markers and existing content
- **South America** (restructured): Merged former `### South America` and `### Gran Colombia` sections into unified section with `**South America:**` sub-header; converted Brazil, Argentina, Lithium Triangle, Gran Colombia, Peru, Cayenne to v1.1 format; added Paraguay entry
- **Central America** (restructured + Mexico moved): Added `**Central America:**` sub-header; moved Mexico from Northern America to Central America per UN geoscheme; converted CAF, Costa Rica, Panama, Belize to v1.1 format

### Format Conversion

All entity entries converted from narrative-format to v1.1 structured format:
- Bold lead sentence: `**Entity Name:** Stage X — characterization`
- Bullet categories: `- **Strategic posture:**`, `- **Economic character:**`, `- **Key dynamic:**`
- `- **→ See KML: Entity Name**` on all entities
- `- → See transition doc:` references included for major entities

### Content Preserved

All existing substantive content preserved throughout — the restructuring reformatted existing analysis without rewriting. Canada fragmentation framing paragraphs, Caribbean transformation analysis, Central America's three-force reconfiguration framework, and South America's Per/Gran Colombia/Guianas entries all retained.

## Deviations from Plan

None — plan executed exactly as written.

## Success Criteria

- [x] Americas sections reorganized: Northern America, Caribbean, Central America, South America
- [x] Each section has a `**REGION:**` sub-header in bold
- [x] All ~85 Americas entities have v1.1 structured entries
- [x] US successor states content preserved, converted to new format
- [x] → See KML markers added throughout
- [x] Old section headers (### Former United States Territory, ### North America (Beyond Former US), ### Gran Colombia) removed
- [x] Old subheaders (#### Revolutionary States, etc.) removed
- [x] Existing narrative content preserved
- [x] Mexico moved to Central America per UN geoscheme
- [x] 11/11 automated verification checks passed

## Self-Check: PASSED

- `2050-snapshot/domains/borders-geopolitics.md` modified: verified via grep for all 4 UN subregion headers, entity counts, and old header removal
- Commit `3cb8bd4` exists in git log
