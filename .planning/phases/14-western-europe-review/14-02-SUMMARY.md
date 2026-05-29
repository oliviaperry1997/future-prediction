---
phase: 14-western-europe-review
plan: 02
name: "Borders-Geopolitics: Western EU sub-entries + Key Changes bullet"
subsystem: borders-geopolitics
tags: [western-europe, european-federation, sub-entries, borders, geopolitics]
dependency_graph:
  requires: [14-01-PLAN.md — KML & Entity Config complete]
  provides: [borders-geopolitics Western Europe content for 14-03, 14-04]
  affects: [economy.md, demographics.md, culture.md, climate.md]
tech-stack:
  added: []
  patterns: [Phase 12 sub-entry format replicated in European Federation section]
key-files:
  created: []
  modified: [2050-snapshot/domains/borders-geopolitics.md]
metrics:
  duration: 87s
  completed: "2026-05-29"
decisions: []
---

# Phase 14 Plan 02: Borders-Geopolitics Western EU Sub-entries Summary

**One-liner:** Added Western Europe restructured Key Changes bullet and 6 individual sub-entries (France, Germany, Netherlands, Belgium, Austria, Luxembourg) to the European Federation section of borders-geopolitics.md, following Phase 12 Southern Europe precedent and all D-07 through D-12 decisions.

## Summary

Added comprehensive Western Europe coverage to `2050-snapshot/domains/borders-geopolitics.md`:

### Task 1 — Key Changes Bullet
- **Commit:** `c27e32b`
- Inserted "Western Europe restructured" bullet in Key Changes section (line 31, after Southern Europe, before Phase 13 entry)
- ~200-word paragraph covering Switzerland/Liechtenstein EU accession, French territorial fracture, German AfD recovery trajectory, and EDF formation context
- References all 6 Western EU member trajectories at appropriate depth per D-07

### Task 2 — 6 Western EU Sub-entries
- **Commit:** `cedeab4`
- Added comment marker `<!-- Western Europe reviewed Phase 14 (2026-05-29) -->` following Phase 12 pattern
- **France** (substantial depth, lines 301-304): Bardella-era degradation (2027-2043), Corsica/Brittany separation as EU Federation subdivisions (D-09), rump France left reboot (D-10), nuclear deterrent federalization into European Nuclear Command (D-08). One substantial paragraph covering all territorial and nuclear trajectory.
- **Germany** (substantial depth, lines 306-309): AfD era (~2029-2044), deindustrialization and foreign worker exodus, US base transfer to EDF (D-11) with Ramstein as EDF central command, green-left reboot (~2044-2046), re-emergence as EU's leading industrial power (D-12).
- **Netherlands** (research-driven depth, lines 311-314): PVV/Wilders far-right government (2024-2026), rapid collapse, Jetten cabinet 2026, reactionary reversal counterexample. Full characterization of how the Netherlands became EU core's primary evidence that far-right waves can be reversed within an electoral cycle.
- **Belgium** (standard depth, lines 316-319): N-VA ambiguous trajectory, Flemish nationalist right governance, cordon sanitaire excluding Vlaams Belang, resolution toward EU federal framework rather than Belgian fragmentation.
- **Austria** (standard depth, lines 321-324): "Reactionary but small — degrades without fragmenting" dynamic, FPÖ era through 2030s, slow-burn economic decline vs catastrophic collapse, EU structural transfers preventing fragmentation.
- **Luxembourg** (standard depth, lines 326-329): Financial center and EU institutional hub status, structural revolutionary-core alignment regardless of domestic politics, trajectory determined by external forces (dollar collapse, Benelux integration, EU institutional consolidation).

Sub-entries placed after Slovenia (last Mediterranean EU entry) and before Albania (first Western Balkans accession entry), following Phase 12 ordering pattern. No standalone Switzerland profile created (per D-02).

## Deviations from Plan

None — plan executed exactly as written.

## Verification Results

- `grep "Western Europe restructured"` returns exactly 1 line (line 31 in Key Changes section)
- All 6 sub-entry markers found: `**France:**`, `**Germany:**`, `**Netherlands:**`, `**Belgium:**`, `**Austria:**`, `**Luxembourg:**`
- Comment marker `Western Europe reviewed Phase 14` present
- No standalone Switzerland sub-entry created
- All entries within European Federation section, after Slovenia, before Albania
- All entries respect existing cross-reference format (`**→ See KML: European Federation**`)

## Self-Check: PASSED
