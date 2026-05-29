---
phase: 08-eastern-europe-review
reviewed: 2026-05-27T18:00:00Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - 2050-snapshot/kml/entity-config.json
  - 2050-snapshot/kml/borders.kml
  - 2050-snapshot/domains/borders-geopolitics.md
  - 2050-snapshot/domains/economy.md
  - 2050-snapshot/domains/demographics.md
  - 2050-snapshot/domains/culture.md
  - 2050-snapshot/domains/climate.md
findings:
  critical: 1
  warning: 4
  info: 2
  total: 7
status: issues_found
---

# Phase 08: Code Review Report — Eastern Europe Review

**Reviewed:** 2026-05-27T18:00:00Z
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

Reviewed all seven files modified during the Eastern Europe review phase: entity-config.json, borders.kml, and five domain docs (borders-geopolitics.md, economy.md, demographics.md, culture.md, climate.md). The structural re-organization (EU entity creation, folder hierarchy update, Belarus/Ukraine domain doc profiles) is largely correct and internally consistent. However, one **critical** issue exists: the European Core Federation entity still contains 11 country codes that overlap with the new European Union entity, which will cause duplicate polygon generation if the KML pipeline processes both. Additionally, the EU entity scope is incomplete — it only removed 6 Eastern European member states from the entities dict while leaving 10 other EU member states as standalone entries, and the (wip) folder hierarchy still references individual EU members.

---

## Critical Issues

### CR-01: European Core Federation entity overlaps with European Union entity (11 duplicate country codes)

**File:** `2050-snapshot/kml/entity-config.json`, lines 642–671 (ECF) and lines 694–702 (EU)

**Issue:** The `"European Core Federation"` entity (line 642) defines `country_codes` that overlap with 11 of the 27 codes in the new `"European Union"` entity (line 694). These overlapping codes are:

| Code | Country | ECF (line 646) | EU (line 698) |
|------|---------|:---:|:---:|
| FIN | Finland | ✓ | ✓ |
| SWE | Sweden | ✓ | ✓ |
| DNK | Denmark | ✓ | ✓ |
| NLD | Netherlands | ✓ | ✓ |
| BEL | Belgium | ✓ | ✓ |
| LUX | Luxembourg | ✓ | ✓ |
| HUN | Hungary | ✓ | ✓ |
| SVN | Slovenia | ✓ | ✓ |
| EST | Estonia | ✓ | ✓ |
| LVA | Latvia | ✓ | ✓ |
| LTU | Lithuania | ✓ | ✓ |

If the KML generation pipeline processes both entities, all 11 countries will appear as polygons in two separate entities simultaneously — one in the ECF and one in the EU — creating visual overlap and breaking the "every entity is a single polygon" contract.

The `European Core Federation` was a v1.0 concept (Nordic Council + Benelux + Baltic states + Hungary + Slovenia) that should have been removed or converted when the full `European Union` entity was created (per D-03: "expanded to the full federal EU"). The ECF with its `#eu-core-federation` section anchor (line 669) is now a dead reference — the EU entity points to `#european-union` instead.

**Fix:** Remove the `"European Core Federation"` entity entry entirely from the `entities` dict (lines 642–671):

```json
// DELETE these lines (642-671):
"European Core Federation": {
  "type": "entity",
  "category": "global",
  "source": "group",
  "country_codes": [
    "FIN", "SWE", "NOR", "DNK", "ISL",
    "NLD", "BEL", "LUX", "HUN", "SVN",
    "EST", "LVA", "LTU"
  ],
  "subtract_admin1_per_code": {
    "NLD": ["Bonaire", "Saba", "St. Eustatius"]
  },
  "domain_doc": "2050-snapshot/domains/borders-geopolitics.md",
  "section_anchor": "eu-core-federation",
  "see_path": "See: 2050-snapshot/domains/borders-geopolitics.md#eu-core-federation"
}
```

If Norway (NOR) and Iceland (ISL) must be represented (they are in the ECF but not in the EU), either add them to the EU entity's `country_codes` array, or create a separate small entity for non-EU members.

Additionally, search all five domain docs for references to `#eu-core-federation` or `European Core Federation` and update them to reference the EU entity instead (e.g., culture.md line 235 already references EU correctly, but the cross-doc cross-references should be verified.)

---

## Warnings

### WR-01: EU member states remain as standalone entity entries in entity-config.json

**File:** `2050-snapshot/kml/entity-config.json`

| Line | Entity | Country Code | Also in EU entity |
|------|--------|:---:|:---:|
| 672 | Germany | DEU | ✓ |
| 1239 | Ireland | IRL | ✓ |
| 1248 | Spain | ESP | ✓ |
| 1257 | Portugal | PRT | ✓ |
| 1266 | Italy | ITA | ✓ |
| 1284 | Austria | AUT | ✓ |
| 1293 | Greece | GRC | ✓ |
| 1320 | Croatia | HRV | ✓ |
| 1383 | Malta | MLT | ✓ |
| 1392 | Cyprus | CYP | ✓ |

**Issue:** The phase removed 7 Eastern European member states (Poland, Czechia, Slovakia, Hungary, Romania, Bulgaria) and Moldova from the entities dict, but left 10 other EU member states as standalone entity entries. These entities sit alongside the new merged EU entity with overlapping `country_codes`. When the KML pipeline processes the entities dict, it will generate both the EU merged polygon AND individual country polygons for these 10 countries, creating overlapping geometry.

The `folder_hierarchy` still references these countries in (wip) folders (e.g., `"Western Europe (wip)": ["Austria", "Belgium", "France", "Germany", ...]`), which will cause duplicate rendering when those (wip) tags are removed.

**Fix:** This phase scoped changes only to the Eastern Europe region. The (wip) tags on Western/Southern/Northern Europe signal that those re-organizations are deferred. Therefore this is not a blocker for this phase, but the inconsistency must be documented and resolved in a future phase before the (wip) tags are removed. Two approaches:

1. **Deferred cleanup (recommended):** Document this in the phase plan for each remaining European sub-region that when (wip) tags are removed, all individual EU member entities must be deleted from the entities dict and their folder_hierarchy entries must be removed or replaced with a single `"European Union"` entry.
2. **Immediate fix (cleaner):** Remove all standalone EU-member entities now and remove them from all (wip) folder hierarchies. This is a one-time cleanup that prevents future confusion.

### WR-02: European Core Federation entity is orphaned — defined but not placed in any folder

**File:** `2050-snapshot/kml/entity-config.json`, lines 642–671

**Issue:** The `"European Core Federation"` entity is defined in the `entities` dict but does not appear in any `folder_hierarchy` entry. It is an orphaned entity — the pipeline will never render it through the folder-based placement system, but it remains in the data as dead configuration. This creates confusion about whether the ECF is active or retired, and its overlapping `country_codes` (CR-01) could still cause issues if any code path iterates the entities dict directly.

Additionally, the `section_anchor` and `see_path` point to `#eu-core-federation` in borders-geopolitics.md, but that anchor does not exist — borders-geopolitics.md only has `#european-union` (line 277), `#russia` (line 281), `#belarus` (line 283), and `#ukraine` (line 285) as Europe-related entity sections. A link resolver would return a 404-style broken anchor.

**Fix:** Same as CR-01 — remove the ECF entity entirely and redirect any cross-references to the EU entry. If non-EU members (NOR, ISL) need representation, create a minimal entity or add them to the EU's country_codes.

### WR-03: Russia population figure differs by 10–15M between domain docs

**Files:**
- `2050-snapshot/domains/borders-geopolitics.md`, line 281: `"Population ~120-125M"`
- `2050-snapshot/domains/demographics.md`, line 507: `"Population: 135M"`
- `2050-snapshot/domains/economy.md`, line 511: `"Population ~120-125M"`

**Issue:** The Russia population in `demographics.md` (135M) is 10–15M higher than the figure in `borders-geopolitics.md` and `economy.md` (120–125M). This is a 10–12% discrepancy, far beyond rounding error. The Union State summary line in demographics.md (line 516: "combined Union State population is ~157-162M") is also inconsistent — if Russia is 135M and the combined total is 157–162M, then Belarus (~9M) + Ukraine (~28M) = only 37M, making Russia's implied share 120–125M (which contradicts the stated 135M).

**Fix:** Reconcile the Russia population figure across all three docs. Pick one canonical number:
- If **120–125M** is correct (borders-geopolitics, economy): update demographics.md line 507 from `135M` to `~120-125M`, and update line 516 combined total accordingly to `~157-162M`.
- If **135M** is correct (demographics): update borders-geopolitics.md line 281 and economy.md line 511 to `~135M`.

### WR-04: Domain doc cross-references still reference `#eu-core-federation` instead of `#european-union`

**Files:**
- `2050-snapshot/domains/economy.md`, line 83: `[European Union](../../2050-snapshot/domains/borders-geopolitics.md#europe)` — links to `#europe` which is correct but says "European Union"
- `2050-snapshot/domains/borders-geopolitics.md`, line 464 (coverage table): `| Europe | European Union (federal) + United Kingdom + Russia + Belarus + Ukraine + Turkey | §Europe |` — links to `§Europe` which works

**Issue:** Several domain docs still contain references to the old `#eu-core-federation` anchor which no longer exists. For example, the `"European Core Federation"` entity entry in entity-config.json (line 669) points to `#eu-core-federation`. The borders-geopolitics.md no longer has an `#eu-core-federation` anchor — the unified `#european-union` anchor replaced it.

Additionally, some economy.md cross-references to the EU use descriptive text that implies the old core/periphery model rather than the unified federal EU (e.g., references to "Nordic-Benelux" and "reactionary periphery" in climate.md lines 74–76, while the new EU is supposed to be fully unified).

**Fix:** Search all domain docs for `#eu-core-federation` and `European Core Federation` strings. Replace each with `#european-union` and `European Union` respectively. Update entity-config.json's `"European Core Federation"` → `"European Union"` pointer (when removing the ECF per CR-01).

---

## Info

### IN-01: borders.kml — EU folder only contains 6 of 27 member polygons

**File:** `2050-snapshot/kml/borders.kml`, lines 49331–49410

**Issue:** The `European Union` folder under `Eastern Europe` contains only 6 placemarks (Bulgaria, Czechia, Hungary, Poland, Romania, Slovakia). These are the 6 Eastern European member states that were merged. The remaining 21 EU member states (all Western, Northern, and Southern members) still have their individual country folders/placemarks elsewhere in the KML under (wip) regional folders. This is the KML-side manifestation of the incomplete entity-config migration noted in WR-01. The (wip) tags signal that these will be addressed in future phases.

**Suggestion:** Add a KML comment in the European Union folder (next to the existing comment at line 49330) documenting that the EU folder only contains the former Eastern European subdivision polygons for now, and that the full EU polygon merge (Western, Northern, Southern members) is deferred until those regions' (wip) tags are removed. This prevents confusion for future editors.

### IN-02: borders.kml — Moldova removal leaves no trace of entity fate

**File:** `2050-snapshot/kml/borders.kml`, lines 49328–49330

**Issue:** The Moldova folder was removed with no residual comment explaining that its territory is now part of the EU (via Romania). A future editor unfamiliar with the lore might wonder why Moldova is missing. The Phase 5 KML generation pattern includes annotation comments (as seen at line 49330 about Crimea/Transnistria), suggesting this is a deliberate practice.

**Suggestion:** Add a brief XML comment near the Eastern Europe folder opening tag (line 49328 or 49330):

```xml
<!-- Moldova removed: territory absorbed into Romania (EU member), now part of European Union polygon. Transnistria absorbed into Ukraine. -->
```

---

## Summary Table

| ID | Severity | File | Line(s) | Issue |
|:--:|:--------:|------|:-------:|-------|
| CR-01 | **Critical** | entity-config.json | 642–671, 694–702 | ECF and EU have 11 overlapping country codes |
| WR-01 | Warning | entity-config.json | 672, 1239–1392 | 10 EU member states remain as standalone entities |
| WR-02 | Warning | entity-config.json | 642–671 | ECF is orphaned (defined, not in any folder) |
| WR-03 | Warning | demographics.md, borders-geopolitics.md | 507, 281 | Russia population differs by 10–15M across docs |
| WR-04 | Warning | entity-config.json, borders-geopolitics.md | 669, 277 | Cross-reference dead anchor `#eu-core-federation` |
| IN-01 | Info | borders.kml | 49331–49410 | EU folder only has 6 of 27 member polygons |
| IN-02 | Info | borders.kml | 49328–49330 | Moldova removal lacks explanatory comment |

---

## Verified as Correct

The following aspects of the phase implementation are correct and require no changes:

- **EU entity setup:** 27 country codes for all 27 EU member states — correct ISO 3166-1 alpha-3 codes, valid set ✅
- **Entity removals:** Poland, Czechia, Slovakia, Hungary, Romania, Bulgaria, Moldova correctly removed from entities dict ✅
- **Belarus entity:** `section_anchor: "belarus"` and `see_path` with `#belarus` — correct ✅
- **Ukraine entity:** `section_anchor: "ukraine"` and `see_path` with `#ukraine` — correct ✅
- **EU entity:** `section_anchor: "european-union"` and `see_path` with `#european-union` — correct ✅
- **Folder hierarchy:** `"Eastern Europe": ["European Union", "Russia", "Belarus", "Ukraine"]` — correct, no (wip) tag ✅
- **KML anchors:** All placemarks use correct description anchors (#european-union, #belarus, #russia, #ukraine) ✅
- **KML folder structure:** European Union folder with 6 merged placemarks, no Moldova folder, Belarus/Russia/Ukraine folders intact ✅
- **Domain doc profiles:** Belarus, Ukraine, and expanded EU profiles present in all 5 domain docs with standard depth ✅
- **borders-geopolitics.md Europe section:** New `### Europe` heading (line 275) with EU, UK, Russia, Belarus, Ukraine, Moldova, Turkey entries — correct anchor structure ✅
- **economy.md transition doc link:** `[European Union](../../2050-snapshot/domains/borders-geopolitics.md#europe)` — `#europe` correctly matches `### Europe` heading in borders-geopolitics.md ✅
- **Climate.md updates:** "Eastern Europe and the European Union" and "Russia" sections added — correct coverage ✅

---

_Reviewed: 2026-05-27T18:00:00Z_
_Reviewer: gsd-code-reviewer (standard depth)_
_Phase: 08-eastern-europe-review_
