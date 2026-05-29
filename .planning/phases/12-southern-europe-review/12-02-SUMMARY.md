---
phase: 12-southern-europe-review
plan: "02"
subsystem: borders-geopolitics
tags: [borders-geopolitics, southern-europe, eu-federation, greco-turkish-conflict, western-balkans, microstates]
dependency_graph:
  requires: []
  provides: [southern-europe-borders-geopolitics, greco-turkish-conflict-narrative, western-balkans-trajectory]
  affects: [borders-geopolitics.md, europe.md]
tech_stack:
  added: []
  patterns: [eu-sub-entry-pattern, sovereign-standalone-entry-pattern]
key_files:
  created: []
  modified:
    - 2050-snapshot/domains/borders-geopolitics.md
    - 2026-2050-transition/regions/europe.md
decisions:
  - "Italy remains territorially unified by 2050 — northern autonomism did not cross fracture threshold before revolutionary flip"
  - "Albania/Kosovo/Montenegro/North Macedonia: EU sub-entries (accession ~2040-2046)"
  - "Serbia: sovereign through 2050 (late-stage reactionary, Russia/China hedging structural)"
  - "Bosnia-Herzegovina: sovereign through 2050 (Republika Srpska structural freeze tied to Serbia)"
  - "Monaco: special-status sovereign (Grimaldi dynasty preserved via EU framework agreement)"
  - "Vatican City: retains sui generis papal sovereignty, no EU absorption"
  - "Andorra and San Marino: absorbed into EU Federation"
metrics:
  duration: "~20 minutes"
  completed: "2026-05-28"
  tasks_completed: 2
  files_modified: 2
---

# Phase 12 Plan 02: Southern Europe Borders-Geopolitics Summary

**One-liner:** All 8 EU Southern Europe sub-entries written with full depth; Greco-Turkish conflict, TRNC partition, and frozen Aegean documented as historical facts; Serbia and Bosnia-Herzegovina as sovereign standalones.

## What Was Built

**borders-geopolitics.md:**

Added 12 new entries/sub-entries after the European Federation paragraph:

**EU Member Sub-entries (8):**
- **Italy** (significant depth): Far-right trajectory, northern autonomy risk, periphery euro dynamics, territorial integrity position (unified by 2050), revolutionary reabsorption into EU core
- **Spain** (significant depth): CATL Zaragoza anchor, renewable energy leadership, Gibraltar transfer, BRICS+ economic bridge, swing-state-to-revolutionary arc
- **Greece** (research-driven depth): Aegean island losses as historical fact, EU's most ardent EDF advocate, frozen dispute through 2050
- **Portugal** (standard depth): Atlantic Lusophone network, post-US-collapse repositioning, renewable energy
- **Cyprus** (standard depth, LOCKED D-11): Republic of Cyprus holds south, TRNC formally annexed by Turkey, EEZ revenue-sharing imposed
- **Croatia, Malta, Slovenia** (standard depth): Adriatic/Mediterranean positioning, respective national characteristics

**Western Balkans EU sub-entries (4):**
- Albania (~2040), Kosovo (~2046), Montenegro (~2040), North Macedonia (~2042) — brief accession notes with feedback loop rationale

**Microstates:** Andorra and San Marino absorbed; Monaco special-status sovereign; Vatican City sui generis

**Sovereign Balkans standalones (2):**
- **Serbia**: Late-stage reactionary, Russia/China hedging structural, talent outflow, BRI infrastructure as EU alternative
- **Bosnia-Herzegovina**: Dayton-frozen structural stasis, tied to Serbia's trajectory, Republika Srpska blocking mechanism

**Turkey entry updated:** Full Greco-Turkish conflict narrative — mid-2030s military operation, NATO Article 13 exit mechanism, frozen Aegean outcome, Cyprus TRNC annexation, EDF founding trauma

**Summary section (lines 29-30):** Southern Europe restructure note added parallel to Eastern/Northern Europe notes

**Territorial integrity table:** Europe row updated with Cyprus partition, Aegean frozen conflict, Serbia/Bosnia-Herzegovina as sovereign entities, Monaco/Vatican special status

**europe.md cross-references:** Three `→ See 2050 snapshot` annotations added to Italy and Spain entries

## Locked Scenarios Implemented

| Decision | Implementation |
|----------|---------------|
| D-09: Greco-Turkish conflict | Turkey entry + Greece sub-entry document the full scenario |
| D-10: NATO exit via Article 13 | Explicitly documented in Turkey entry |
| D-11: Frozen Aegean + TRNC annexation | Greece and Cyprus sub-entries + Turkey entry |
| D-12: Greece as EDF maximalist | Greece sub-entry leads with this framing |

## Verification

- 8 EU Southern Europe sub-entries: `grep -c "^\*\*Italy:\*\*..."` = 8 ✓
- TRNC/Northern Cyprus mentions: 5 ✓
- Aegean mentions: 4 ✓
- EDF mentions: 3 ✓
- Gibraltar mention in Spain sub-entry: 3 ✓
- Western Balkans coverage: 9 ✓
- Microstates: 4 ✓

## Deviations from Plan

None — plan executed exactly as written. All locked scenarios implemented. Western Balkans research outcomes consistent with Plan 01.

## Self-Check: PASSED

- `2050-snapshot/domains/borders-geopolitics.md` — modified with all required entries
- `2026-2050-transition/regions/europe.md` — cross-references added
- Commit 657dd01 — exists
