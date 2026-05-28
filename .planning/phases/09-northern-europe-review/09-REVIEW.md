---
phase: 09-northern-europe-review
reviewed: 2026-05-28T18:00:00Z
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

# Phase 09: Code Review Report — Northern Europe Review

**Reviewed:** 2026-05-28T18:00:00Z
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

This phase restructured the Northern Europe geopolitical region in the 2050 snapshot: Norway and Iceland joined the European Federation, Scotland exited the UK to join the EU, Northern Ireland reunified with Ireland, and the UK underwent a late revolutionary flip (~2045-2048). The changes are reflected across 7 files — entity-config.json (entity restructuring, new entities, renamed entities), borders.kml (restructured folder hierarchy, removed Norway Placemarks, added Russia archipelago Placemarks), and 4 domain documents (updated references from "European Union" to "European Federation" and added Northern Europe narrative).

Key issues found: the UK entity config does not exclude Scotland/Northern Ireland territory from its GBR-derived polygon (causing territorial overlap with the EU); multiple stale anchor references remain from the EU→European Federation rename; and a non-standard data field on the UK entity breaks schema consistency.

---

## Critical Issues

### CR-01: UK entity polygon includes Scotland and Northern Ireland territory

**File:** `2050-snapshot/kml/entity-config.json:622`
**Issue:** The United Kingdom entity uses `"source": "group"` with `"country_codes": ["GBR", "SHN"]` and has **no** `subtract_admin1` or `subtract_admin1_per_code` configuration. The ISO 3166-1 alpha-3 code `GBR` covers England, Scotland, Wales, and Northern Ireland as a single geographical unit. Per the narrative in `borders-geopolitics.md` (line 280):

> "Scotland exited ~2035-2038 following a second independence referendum and acceded directly to the federal EU — Scotland is an EU subdivision, not part of the UK in 2050."
> "**Northern Ireland** reunified with Ireland following a ~2030s border poll… Northern Ireland is part of Ireland, which is an EU subdivision."

Without a subtraction mechanism, the auto-generated KML polygon for the United Kingdom would incorrectly include Scotland and Northern Ireland territory. The European Federation's `country_codes` do not include Scotland (no ISO 3166-1 alpha-3 code `SCT` exists for Scotland), so Scotland's territory would also be absent from the EU polygon — creating a **territorial gap**.

Additionally, `country_code: "GBR"` includes Wales (which is still part of the UK — correct), but there is no explicit `keep_unified` or `subtract` logic to isolate England-and-Wales territory from Scotland-and-NI.

**Fix:** Add `subtract_admin1_per_code` to the UK entity to exclude Scotland and Northern Ireland from the GBR polygon:
```json
"United Kingdom": {
  "type": "entity",
  "category": "global",
  "source": "group",
  "keep_unified": true,
  "country_codes": ["GBR", "SHN"],
  "subtract_admin1_per_code": {
    "GBR": ["Scotland", "Northern Ireland"]
  },
  ...
}
```
Alternatively, switch the UK to `"source": "manual"` with a precomputed KML that excludes Scotland and Northern Ireland. If the GADM admin1 names differ (e.g., "Scotland", "Northern Ireland" in Natural Earth admin1), verify the exact strings in the source data.

---

## Warnings

### WR-01: European Federation entity retains stale "european-union" section_anchor

**File:** `2050-snapshot/kml/entity-config.json:650-652`
**Issue:** The European Federation entity has:
```json
"section_anchor": "european-union",
"see_path": "See: 2050-snapshot/domains/borders-geopolitics.md#european-union"
```
The entity was renamed from "European Union" to "European Federation" in this phase, but the anchor reference was not updated. The corresponding heading in `borders-geopolitics.md` (line 278) uses `**European Federation:**` as bold text under `### Europe`. The auto-generated markdown anchor from the `### Europe` heading would be `#europe`, not `#european-union`. This creates a dead link in the see_path references.

The Åland Islands entity (line 1345-1347) has the same stale reference:
```json
"section_anchor": "european-union",
"see_path": "See: 2050-snapshot/domains/borders-geopolitics.md#european-union"
```

**Fix:** Update to reference the correct anchor. Either:
- Change to `"europe"` (matching the H3 `### Europe` heading) and update see_path to `#europe`, or
- Add an explicit markdown anchor `{#european-federation}` in `borders-geopolitics.md` at the European Federation entry and change anchor to `"european-federation"`:
```json
"section_anchor": "european-federation",
"see_path": "See: 2050-snapshot/domains/borders-geopolitics.md#european-federation"
```

### WR-02: Domain overlay descriptions reference stale "#european-union" anchors

**File:** `2050-snapshot/kml/entity-config.json:2755, 2769, 2783`
**Issue:** Three domain overlay entries reference `#european-union` anchors that no longer exist after the rename:

- Line 2755: `"description": "See: 2050-snapshot/domains/economy.md#european-union"` (economy overlay)
- Line 2769: `"description": "See: 2050-snapshot/domains/demographics.md#european-union"` (demographics overlay)
- Line 2783: `"description": "See: 2050-snapshot/domains/culture.md#european-union"` (culture overlay)

In all three domain docs, the heading text was updated to "European Federation" but the overlay description references in entity-config.json still point to `#european-union` anchors.

**Fix:** Update all three to match:
```json
"description": "See: 2050-snapshot/domains/economy.md#european-federation"
```
```json
"description": "See: 2050-snapshot/domains/demographics.md#european-federation"
```
```json
"description": "See: 2050-snapshot/domains/culture.md#european-federation"
```

### WR-03: KML North Sea/Arctic Placemarks removed without matching EU absorption documentation

**File:** `2050-snapshot/kml/borders.kml` (diff — Norway Placemarks replaced with Russia Placemarks)
**Issue:** The KML diff shows all 25+ Norwegian archipelago Placemarks (covering mainland Norway coastal polygons, Svalbard, Jan Mayen, and other North Atlantic/Arctic islands) being removed and replaced with Russian Far East archipelago Placemarks. The KML comment (line 58422) states: "Svalbard treaty status superseded by EU Arctic governance framework. Faroe Islands joined the EU with Denmark."

However, there is no explicit Placemark or folder for Svalbard, Jan Mayen, or the Faroe Islands under the European Federation or Northern Europe folders in the KML. If these territories were simply absorbed into the EU's auto-generated polygon from the `NOR` and `FRO`/`DNK` country codes, this is architecturally acceptable — but the KML restructuring is removing the individual Placemarks that previously gave these islands visible boundary detail.

The risk is that the auto-generated EU polygon (using 1:10m country data) may not render Svalbard/Jan Mayen at the same resolution as the removed manual Placemarks, creating an apparent territorial gap or degraded visual fidelity in the Arctic region.

**Fix:** Either (a) confirm that the KML generation tool includes Svalbard/Jan Mayen as part of the NOR country-code polygon, documented explicitly in a KML comment, or (b) add explicit Placemarks for Svalbard, Jan Mayen, and Faroe Islands within the European Federation folder if the auto-generated polygon loses them.

### WR-04: La Réunion and Mayotte entities created without narrative documentation

**File:** `2050-snapshot/kml/entity-config.json:2071-2090` (new entities)
**File:** `2050-snapshot/domains/borders-geopolitics.md` (no mention of either)
**Issue:** Two new entities — La Réunion and Mayotte — were added to `entity-config.json` as `source: "admin1"` from `country_code: "FRA"` and placed in the `Eastern Africa` folder hierarchy. Their `see_path` both point to the generic `borders-geopolitics.md` without section anchors, and there is **no narrative description** in `borders-geopolitics.md` explaining their status in 2050.

The European Federation entity subtracts both `La Réunion` and `Mayotte` from FRA via `subtract_admin1_per_code`, which implies they are independent entities in 2050. However the borders-geopolitics.md only documents the Caribbean territories' sovereignty transition ("Every British, Dutch, and French overseas territory in the Caribbean achieved full sovereignty and CARICOM membership") — it does not cover the Indian Ocean territories. A reader has no way to understand whether La Réunion and Mayotte are independent, still French/EU territory, or under some other governance arrangement.

**Fix:** Add a paragraph in `2050-snapshot/domains/borders-geopolitics.md` (e.g., after the Caribbean section or in a new Indian Ocean section) documenting the status of La Réunion and Mayotte:
```markdown
**French Indian Ocean Territories:** La Réunion and Mayotte — former French overseas departments in the Indian Ocean — achieved sovereignty following France's post-EU retrenchment in the 2030s-2040s. La Réunion (population ~900K) oriented toward the EAF and Indian Ocean Commission as an associate member. Mayotte (population ~300K) followed a similar trajectory, maintaining close ties with Comoros neighbors. Both are independent sovereign states, not constituent parts of the European Federation.
```

---

## Info

### IN-01: UK entity contains non-standard schema fields

**File:** `2050-snapshot/kml/entity-config.json:631-632`
**Issue:** The UK entity has two custom fields not present on any other entity in the configuration:
```json
"classification": "revolutionary (late flip ~2045-2048)",
"notes": "Scotland exited ~2035-2038 to join EU; Isle of Man, Channel Islands remain as Crown Dependencies"
```
These fields are not part of the documented entity schema (compare with the `"European Federation"` entity or any other entity — none have `classification` or `notes` fields). If the KML generation tool or validation scripts operate on a fixed schema, these extra fields may cause validation warnings or be silently ignored, and the information they contain would be invisible in the rendered output.

The narrative content belongs in the `see_path` document (`borders-geopolitics.md`), where it is already described in detail (line 280).

**Fix:** Remove the non-standard fields:
```json
"United Kingdom": {
  "type": "entity",
  "category": "global",
  "source": "group",
  "keep_unified": true,
  "country_codes": ["GBR", "SHN"],
  "domain_doc": "2050-snapshot/domains/borders-geopolitics.md",
  "section_anchor": "united-kingdom",
  "see_path": "See: 2050-snapshot/domains/borders-geopolitics.md#united-kingdom"
}
```

### IN-02: Very long line in borders-geopolitics.md UK section

**File:** `2050-snapshot/domains/borders-geopolitics.md:280`
**Issue:** The UK description paragraph is so long that it exceeds 2,000 characters and was truncated by the Read tool. This makes the section harder to maintain, review, and read in standard terminal widths. The UK section contains a single paragraph covering: trajectory (reactionary slide → late flip), Scotland exit, Northern Ireland reunification, Caribbean territory losses, Crown Dependencies, Gibraltar transfer, Saint Helena retention, and the revolutionary government's early actions.

**Fix:** Split into multiple paragraphs by topic:
```markdown
**United Kingdom:** A late-revolutionary nuclear-armed middle power — the UK undergoes a reactionary-to-revolutionary transition in the late 2040s. Trajectory: reactionary post-Brexit isolation through ~2035 (Scotland exit, City loses dollar-clearing, US collapse), reactionary trap ~2035-2045 (economic contraction, political paralysis, loss of global financial role), then a **revolutionary flip ~2045-2048** driven by the convergence of economic necessity (post-dollar, post-City), political realignment (Labour/left-green coalition capitalizing on post-Brexit exhaustion and the US collapse), and the demonstration effect of the federal EU next door. By 2050, the UK is in **early-stage revolutionary state** — nationalizing strategic industries, rebuilding the welfare state, reorienting foreign policy away from the US special relationship (now defunct) toward European engagement, and managing the contraction of a post-imperial economy.

**Territorial changes:** Scotland exited ~2035-2038 following a second independence referendum and acceded directly to the federal EU — Scotland is an EU subdivision, not part of the UK in 2050. **Northern Ireland** reunified with Ireland following a ~2030s border poll — the post-Brexit structural logic (Scotland in EU, UK outside, Good Friday Agreement framework preserved through EU membership) made unification overwhelming; Northern Ireland is part of Ireland, which is an EU subdivision. **Gibraltar** transferred to Spain (~2030s-2040s) as part of the broader post-Brexit, post-dollar settlement. The UK lost all Caribbean overseas territories to CARICOM, but retains Saint Helena, Ascension, and Tristan da Cunha (~6K combined population) in the South Atlantic. **Isle of Man and Channel Islands** are Crown Dependencies following the UK — outside the EU, with UK diplomatic representation.

**Economy:** London retains its role as a specialized financial center but at greatly reduced global weight — the City's foreign exchange dominance (40%+ of global FX) collapsed with the dollar's reserve status.
```

---

_Reviewed: 2026-05-28T18:00:00Z_
_Reviewer: gsd-code-reviewer (standard depth)_
