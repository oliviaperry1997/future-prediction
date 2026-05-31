---
phase: 20-africa-and-america-re-review
plan: 03
subsystem: borders-geopolitics
tags: [africa, un-geoscheme, v1.1-format, entity-entries, borders-geopolitics, cameroon-fragmentation, car-reassessment, sahel-nigeria]

requires:
  - phase: 20-02
    provides: Updated entity-config.json with canonical Africa border changes (3 KML changes), Ambazonia entity, regenerated KMLs

provides:
  - Restructured Africa section in borders-geopolitics.md organized by UN geoscheme subregions
  - 41 entity-by-entity v1.1 structured entries for all Africa entities
  - Cameroon 3-way fragmentation reflected in entity entries
  - CAR reassessment outcome documented in entity entry
  - Sahel-Nigeria canonical border allocation reflected in AES/Nigeria entries

affects:
  - 20-04 through 20-09: Domain doc entity profiles (economy, demographics, culture, climate, technology) must reference this same entity set and subregion organization

tech-stack:
  added: []
  patterns:
    - "UN geoscheme subregion headers in bold format: **Western Africa:**"
    - "v1.1 entity entry format: bold name, Revolutionary Stage X-Y, em-dash one-line status, structured bullets, KML ref, transition doc link"
    - "APR member states (Egypt, Libya, Tunisia, Algeria, Sudan) included under Northern Africa with → See KML: Arab Popular Republic"

key-files:
  created: []
  modified:
    - 2050-snapshot/domains/borders-geopistics.md

key-decisions:
  - "Northern Africa section includes 6 entities (Egypt, Libya, Tunisia, Algeria, Morocco, Sudan) — the 5 APR members use → See KML: Arab Popular Republic, Morocco uses → See KML: Morocco (standalone entity)"
  - "Congo (Kinshasa) narrative integrated as EAF member sub-entry (blockquote style) rather than standalone entity entry — no standalone Congo (Kinshasa) KML entity exists in entity-config"
  - "Eritrea uses 'Stage 1-2 Reactionary Stasis' label rather than Revolutionary Stage — consistent with transition doc assessment that it has not yet flipped"
  - "Chad and Equatorial Guinea use 'Beyond Loop' label — consistent with transition doc placement outside revolutionary/reactionary binary"

requirements-completed:
  - AFAM-01

# Metrics
duration: 2m 26s
completed: 2026-05-31
---

# Phase 20 Plan 03: Africa borders-geopolitics.md Restructure

**Restructured the Africa section in borders-geopolitics.md from a single narrative block into 5 UN-geoscheme-organized subsections with entity-by-entity v1.1 structured entries for all 41 Africa entities, reflecting KML changes from Plan 02 (Cameroon fragmentation, CAR reassessment, Sahel-Nigeria border)**

## Performance

- **Duration:** 2m 26s
- **Started:** 2026-05-31T10:33:48Z
- **Completed:** 2026-05-31T10:36:14Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments

- **Full restructure:** Africa section reorganized from single narrative block (81 lines) into structured format (324 lines) organized under 5 UN geoscheme subregion headers
- **41 entity entries in v1.1 format:** Each entity now has bold name, Revolutionary Stage assignment, structured bullet categories, → See KML reference, and → See transition doc link
- **Cameroon fragmentation:** 3-way split reflected across 3 entries — AES (northern CMR regions in Territorial integrity), Ambazonia (new standalone entry in Middle Africa), Cameroon (rump reduced to Francophone south)
- **CAR reassessment:** DISCOVERY.md determination implemented — 9 southern prefectures listed as EAF-absorbed, 7 northern prefectures documented as contested zone between AES and EAF
- **Sahel-Nigeria border:** AES entry references 15 Nigerian states + 3 northern Cameroon regions; Nigeria entry references 22 states + FCT — matching the canonical allocation from DISCOVERY.md
- **Existing content preserved:** All substantive claims from original narrative restructured into bullets — verified 12+ key phrases present post-edit
- **North African APR members:** Egypt, Libya, Tunisia, Algeria, Sudan included under Northern Africa with → See KML: Arab Popular Republic; Morocco standalone with → See KML: Morocco
- **Southern Africa added:** Botswana, Eswatini, Namibia, South Africa entries synthesized from transition doc (only South Africa had existing narrative content)

## Task Commits

| # | Name | Type | Hash |
|---|------|------|------|
| 1 | Restructure Africa section into UN geoscheme v1.1 entries | feat | `54b5085` |

## Files Created/Modified

- `2050-snapshot/domains/borders-geopolitics.md` — Modified: Africa section restructured (+324/-81 lines)

## Decisions Made

- **Congo (Kinshasa) handling:** Since entity-config.json has no standalone "Congo (Kinshasa)" entity, the DRC content is integrated as a blockquote sub-entry within the EAF entry rather than as its own entity entry with a separate KML reference.
- **Eritrea stage label:** Uses "Stage 1-2 Reactionary Stasis" rather than "Revolutionary Stage" to match transition doc assessment that Eritrea is pre-flip but not yet in the revolutionary track.
- **Beyond Loop labels:** Chad and Equatorial Guinea use "Beyond Loop" instead of revolutionary stage numbers — matching their placement outside the revolutionary/reactionary binary in the transition doc.
- **APR member KML references:** Five North African APR members (Egypt, Libya, Tunisia, Algeria, Sudan) reference "→ See KML: Arab Popular Republic" since entity-config lists them under the APR meta-entity, not as standalone Africa entities.

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None — all 41 entity entries have complete v1.1 format with stage assignments, substantive bullets, and cross-references.

## Threat Flags

None — static markdown editing, no new trust boundaries introduced.

## Self-Check: PASSED

- 5 UN subregion headers present: Western Africa, Eastern Africa, Middle Africa, Northern Africa, Southern Africa ✓
- Ambazonia entry exists with → See KML: Ambazonia ✓
- ≥25 KML references in Africa section (46 found) ✓
- Cameroon 3-way split: AES (northern CMR), Ambazonia (NW+SW), Cameroon (Francophone south) ✓
- Sahel-Nigeria canonical border: 15 AES states, 22 Nigeria states+FCT ✓
- CAR reassessment: 9 EAF-absorbed prefectures, 7 contested northern prefectures ✓
- Content preserved: all 12 verification phrases present ✓
- Asia section boundary intact (### Asia at line 694) ✓

## Next Phase Readiness

- **borders-geopolitics.md ready for all downstream domain doc work.** Africa section now has entity entries matching entity-config entity names, providing the structural template for economy, demographics, culture, climate, and technology profiles (Plans 04-09).
- Subregion organization (UN geoscheme) is consistent with D-07 and matches entity-config.json folder_hierarchy.
- Entity set reflects all Plan 02 KML changes: Ambazonia included, Cameroon 3-way reflected, CAR reduced, EAF expanded, AES/Nigeria borders canonical.

---

*Phase: 20-africa-and-america-re-review*
*Completed: 2026-05-31*
