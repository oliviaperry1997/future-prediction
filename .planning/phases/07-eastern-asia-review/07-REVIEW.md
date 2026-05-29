---
phase: 07-eastern-asia-review
reviewed: 2026-05-27T00:00:00Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - 2050-snapshot/kml/borders.kml
  - 2050-snapshot/kml/entity-config.json
  - 2050-snapshot/domains/borders-geopolitics.md
  - 2050-snapshot/domains/economy.md
  - 2050-snapshot/domains/demographics.md
  - 2050-snapshot/domains/culture.md
  - 2050-snapshot/domains/climate.md
findings:
  critical: 0
  warning: 9
  info: 2
  total: 11
status: issues_found
---

# Phase 7: Code Review Report

**Reviewed:** 2026-05-27
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found (no critical/blocker, 9 warnings, 2 info)

## Summary

Seven data/configuration files for the 2050 snapshot were reviewed: the KML borders file, entity configuration JSON, and five domain snapshot markdown documents (borders-geopolitics, economy, demographics, culture, climate). No security vulnerabilities, hardcoded secrets, or code-level bugs were found. However, significant **cross-document data inconsistencies** were identified — population figures and migration statistics diverge between domain snapshots, which could undermine downstream consumers (visualizations, KML generation, narrative coherence). No critical/blocker issues were identified (no crashes, security, or data-loss risks), but the data integrity warnings should be resolved before this content is treated as an authoritative snapshot.

---

## Warnings

### WR-01: Population Inconsistency — Great Lakes (economy.md vs demographics.md)

**File:** `2050-snapshot/domains/economy.md:184` and `2050-snapshot/domains/demographics.md:128`
**Issue:** economy.md reports Great Lakes population as "~50M" but demographics.md reports it as "30M". This is a 40% discrepancy and affects GDP-per-capita calculations and labor force modeling.
**Fix:** Determine the authoritative population figure (demographics.md should be the source of truth for population data) and propagate it consistently to economy.md and any other domain documents. Update economy.md line 184 from "~50M" to "30M" (or vice versa after verification).

### WR-02: Population Inconsistency — Hawaiian Free State (economy.md vs demographics.md)

**File:** `2050-snapshot/domains/economy.md:224` and `2050-snapshot/domains/demographics.md:164`
**Issue:** economy.md reports HFS population as "~1.4M" but demographics.md reports "1.8M".
**Fix:** Align the figures. If demographics.md is authoritative, update economy.md line 224 from "~1.4M" to "1.8M".

### WR-03: Population Inconsistency — Aztlán (economy.md vs demographics.md)

**File:** `2050-snapshot/domains/economy.md:214` and `2050-snapshot/domains/demographics.md:152`
**Issue:** economy.md reports Aztlán population as "~12M" but demographics.md reports "18M".
**Fix:** Align the figures. Update economy.md line 214 from "~12M" to "18M" (or resolve which is correct).

### WR-04: Population Inconsistency — Front Range Socialist Republic (economy.md vs demographics.md)

**File:** `2050-snapshot/domains/economy.md:204` and `2050-snapshot/domains/demographics.md:140`
**Issue:** economy.md reports FRSR population as "~5M" but demographics.md reports "8M".
**Fix:** Align the figures. Update economy.md line 204 from "~5M" to "8M" (or resolve).

### WR-05: Population Inconsistency — Tlingit Aaní (economy.md vs demographics.md)

**File:** `2050-snapshot/domains/economy.md:286` and `2050-snapshot/domains/demographics.md:249`
**Issue:** economy.md reports Tlingit Aaní population as "~75K" but demographics.md reports "180K".
**Fix:** Align the figures. Update economy.md line 286 from "~75K" to "180K" (or resolve).

### WR-06: Population Inconsistency — Haudenosaunee Confederacy (economy.md vs demographics.md)

**File:** `2050-snapshot/domains/economy.md:296` and `2050-snapshot/domains/demographics.md:261`
**Issue:** economy.md reports Haudenosaunee population as "~50K+" but demographics.md reports "150K".
**Fix:** Align the figures. Update economy.md line 296 from "~50K+" to "150K" (or resolve).

### WR-07: Inconsistent Climate Migration Arithmetic

**File:** `2050-snapshot/domains/climate.md:88-94`
**Issue:** The text states total cumulative climate migrants are "50-80 million globally" (line 90). It then says ~60% is internal displacement and ~40% is cross-border (line 93). However, line 91 lists cross-border as "~55M" — which alone would imply a minimum total of ~137M (55M / 0.40). The "55M" cross-border figure contradicts the 50-80M total. Additionally, the sum of disaggregated source-region figures (~20M Sahel + ~15M South Asia + ~5M Mekong + ~1M Pacific + ~5M Middle East + others ≈ 55M+ if Central Asia and East Asia are included) also exceeds 50-80M.
**Fix:** Reconcile the arithmetic. Either the total should be closer to 130-150M (matching the ~55M cross-border figure at 40%), or the cross-border figure should be reduced to ~20-32M (40% of 50-80M). Ensure the disaggregated source-region numbers sum consistently to the stated total. This is a first-order figure cited across multiple domain documents, so resolving it is high priority.

### WR-08: Non-Standard ISO Country Codes in entity-config.json

**File:** `2050-snapshot/kml/entity-config.json:1058` (Palestine) and `:1429` (Kosovo)
**Issue:** The entity-config uses `"country_code": "PSX"` for Palestine and `"country_code": "KOS"` for Kosovo. These are not standard ISO 3166-1 alpha-3 codes (Palestine is `PSE`, Kosovo is `XKX` or `UNK` in common practice). If the KML generation pipeline relies on ISO-standard country codes for GADM or Natural Earth lookups, these non-standard codes will cause lookup failures.
**Fix:** Change Palestine's `country_code` to `"PSE"` (ISO 3166-1 alpha-3) and Kosovo's to `"XKX"` (commonly used alpha-3 for Kosovo in GADM/Natural Earth datasets) or verify that the KML generator uses a custom lookup that accepts `PSX`/`KOS`. If custom codes are intentionally supported, document this in the `description` field.

### WR-09: Korea Unification Reference Contradicts Entity Separation

**File:** `2050-snapshot/domains/borders-geopolitics.md:501`
**Issue:** The "Key Uncertainties" section asks about "Korean unification durability" and references how "the DPRK-ROK unified state maintains cohesion." However, the entire document (and entity-config.json) treats ROK and DPRK as separate, non-unified entities. There is no unified Korean state described anywhere in the 2050 snapshot. This uncertainty item references a state that does not exist in the document's own schema.
**Fix:** Either (a) remove the unification uncertainty item since it references a non-existent state, or (b) rephrase it as a future-outlook question (e.g., "Whether the DPRK-ROK divide persists beyond 2050") that matches the documented reality of two separate states.

---

## Info

### IN-01: Empty `section_anchor` Fields for Many Entities

**File:** `2050-snapshot/kml/entity-config.json` (multiple entities, e.g., lines 1143, 1152, 1161, etc.)
**Issue:** Approximately 50+ entities have `"section_anchor": ""` with their `see_path` pointing to the main document rather than a specific section. This is intentional for entities without dedicated sections, but it means the `see_path` can't deep-link. Consider adding minimal anchor sections for completeness or documenting that empty anchors are expected.
**Fix:** Either add stub section anchors in borders-geopolitics.md for these entities, or add a comment in the config noting that empty section anchors are intentional for entities without dedicated writeups. Currently it's ambiguous whether this is a TODO or by design.

### IN-02: Forward References to Potentially Non-Existent Prediction Documents

**File:** `2050-snapshot/domains/borders-geopolitics.md:394` (prediction-002), `2050-snapshot/domains/climate.md:99` (prediction-008, prediction-003)
**Issue:** Multiple domain documents reference "prediction-002," "prediction-003," and "prediction-008" without providing file paths. These prediction documents may not yet exist in the repository or may be located in a different directory structure. If these are navigable references, they should include relative paths; if they're forward references to content not yet created, they should be marked as such.
**Fix:** Verify that prediction-002, prediction-003, and prediction-008 documents exist in the repo. If they do, add relative paths (e.g., `[prediction-002](../predictions/prediction-002.md)`). If they're planned but not yet created, mark them clearly (e.g., `[prediction-002 — PENDING]`).

---

_Reviewed: 2026-05-27_
_Reviewer: the agent (gsd-code-reviewer)_
_Depth: standard_
