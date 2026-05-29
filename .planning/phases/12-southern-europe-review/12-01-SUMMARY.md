---
phase: 12-southern-europe-review
plan: "01"
subsystem: kml
tags: [kml, entity-config, southern-europe, western-balkans, turkey, northern-cyprus]
dependency_graph:
  requires: []
  provides: [entity-config-southern-europe, borders-kml-southern-europe, northern-cyprus-polygon]
  affects: [entity-config.json, borders.kml]
tech_stack:
  added: []
  patterns: [python-json-surgery, kml-folder-restructure]
key_files:
  created: []
  modified:
    - 2050-snapshot/kml/entity-config.json
    - 2050-snapshot/kml/borders.kml
decisions:
  - "Albania, Kosovo, Montenegro, North Macedonia assessed as EU Federation members by 2050 (~2038-2044)"
  - "Serbia and Bosnia-Herzegovina remain sovereign through 2050 (Russia hedging / Republika Srpska dysfunction)"
  - "Kosovo uses KOS (existing country_code) when added to EU Federation country_codes"
  - "Northern Cyprus polygon uses approximate Attila Line coordinates — TODO comment included for precise replacement"
metrics:
  duration: "~15 minutes"
  completed: "2026-05-28"
  tasks_completed: 2
  files_modified: 2
---

# Phase 12 Plan 01: KML/Entity-Config Cleanup Summary

**One-liner:** Southern Europe (wip) renamed, Turkey extracted standalone, 4 Balkans absorbed into EU Federation, Northern Cyprus sub-polygon added to Turkey's KML.

## What Was Built

Restructured the Southern Europe KML folder and entity configuration to reflect the 2050 state:

**entity-config.json:**
- `"Southern Europe (wip)"` → `"Southern Europe"` in `folder_hierarchy.Eurasia`
- Turkey removed from Southern Europe folder
- Albania (ALB), Kosovo (KOS), Montenegro (MNE), North Macedonia (MKD) removed as individual entities and absorbed into European Federation `country_codes`
- Bosnia-Herzegovina and Serbia remain as individual entities with populated `section_anchor` values (`"bosnia-and-herzegovina"` and `"serbia"`)
- European Federation `country_codes` now includes 36 entries (32 original + 4 new Balkans)

**borders.kml:**
- `Southern Europe (wip)` folder renamed to `Southern Europe`
- Albania, Kosovo, Montenegro, North Macedonia `<Folder>` blocks removed (EU Federation polygon covers their territory)
- Turkey `<Folder>` extracted from Southern Europe, now standalone at Eurasia level
- Northern Cyprus `<Placemark>` added within Turkey's `<Folder>` with approximate Attila Line coordinates and a TODO comment for precise polygon replacement from Cyprus boundary source

## Western Balkans EU Accession Research

Applied the revolutionary feedback loop framework to each entity:

| Entity | Decision | Timeline | Rationale |
|--------|----------|----------|-----------|
| Albania | EU by ~2040 | ~2038-2042 | High EU enthusiasm, small/manageable, revolutionary trajectory |
| Kosovo | EU by ~2046 | ~2044-2048 | Spain non-recognition resolved after Spain's revolutionary flip ~2043; 5 non-recognizing members all flip by ~2040s |
| Montenegro | EU by ~2040 | ~2038-2042 | Most advanced EU candidate; small state, stable enough |
| North Macedonia | EU by ~2042 | ~2040-2044 | Name dispute resolved (2018); steady candidate trajectory |
| Serbia | **Sovereign** | — | Russia/China hedging structural; US collapse removes "choose" pressure; reactionary degradation but not yet flip |
| Bosnia-Herzegovina | **Sovereign** | — | Republika Srpska blocks entity-level consensus; tied to Serbia's trajectory; governance dysfunction persists |

## Verification

- `python3 -c "import json; json.load(open('2050-snapshot/kml/entity-config.json'))"` — PASS
- `python3 -c "import xml.etree.ElementTree as ET; ET.parse('2050-snapshot/kml/borders.kml')"` — PASS
- `grep "Southern Europe (wip)" entity-config.json` — no matches
- `grep "Southern Europe (wip)" borders.kml` — no matches
- `grep "Northern Cyprus" borders.kml` — 1 match (Turkey folder)
- European Federation country_codes contains all 8 Southern EU members + 4 Balkans ISO codes — PASS

## Deviations from Plan

None — plan executed exactly as written. Western Balkans accession research produced: 4 EU joiners (ALB/KOS/MNE/MKD), 2 sovereign remainders (SRB/BIH).

## Known Stubs

**Northern Cyprus polygon coordinates:** The Attila Line polygon uses approximate coordinates (~35.1°N latitude) with a `<!-- TODO: Replace with precise Northern Cyprus polygon -->` comment. The approximate coordinates capture the northern ~37% of Cyprus but are not derived from a precise boundary source. The `source/` directory did not contain Cyprus KML/shapefile data — precise coordinates deferred.

## Self-Check: PASSED

- `2050-snapshot/kml/entity-config.json` — modified and valid
- `2050-snapshot/kml/borders.kml` — modified and valid
- Commit d6cfd8e — exists
