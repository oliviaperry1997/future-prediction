---
phase: 06-central-asia-review
reviewed: 2026-05-27T23:30:00Z
depth: standard
files_reviewed: 6
files_reviewed_list:
  - 2050-snapshot/kml/borders.kml
  - 2050-snapshot/domains/borders-geopolitics.md
  - 2050-snapshot/domains/economy.md
  - 2050-snapshot/domains/demographics.md
  - 2050-snapshot/domains/culture.md
  - 2050-snapshot/domains/climate.md
findings:
  critical: 0
  warning: 4
  info: 5
  total: 9
status: issues_found
---

# Phase 6: Code Review Report — Central Asia Review

**Reviewed:** 2026-05-27T23:30:00Z
**Depth:** standard
**Files Reviewed:** 6
**Status:** issues_found

## Summary

Reviewed 6 source files changed during Phase 6 (central-asia-review): the KML borders file, and 5 domain documentation files (borders-geopolitics, economy, demographics, culture, climate). The implementation adds Central Asian Confederation (CAC) profiles across all required domains, removes Afghanistan from the Central Asia KML folder, removes the `(wip)` tag from the folder name, and adds exclave interior polygon holes to Kyrgyzstan and Uzbekistan. The overall quality is good — decisions from CONTEXT.md are generally followed. Four warnings and five info items were found, primarily around cross-reference integrity, population data consistency, and missing domain coverage.

## Warnings

### WR-01: Population total mismatch — CAC collective vs. sum of constituents

**File:** `2050-snapshot/domains/demographics.md:483`
**Issue:** The CAC collective profile states "Population: 80M (growing slowly)" but the five individual constituent profiles sum to 80.5M:

| Constituent | Population |
|---|---|
| Kazakhstan (line 494) | 20M |
| Uzbekistan (line 506) | 37M |
| Turkmenistan (line 517) | 6.5M |
| Kyrgyzstan (line 528) | 7M |
| Tajikistan (line 539) | 10M |
| **Total** | **80.5M** |

The 80M figure either needs to be corrected to 80.5M, or individual profiles adjusted so they sum to exactly 80M. This is a factual consistency error between a summary statement and its detailed breakdown — downstream consumers (automated tools, future cross-checks) will flag this discrepancy.

**Fix:** Either:
- Update line 483 to state "80.5M" (if 80.5 is the intended total), or
- Adjust individual figures (e.g., Kazakhstan to 19.5M) so the sum is 80M

### WR-02: KML cross-reference anchor broken — `#central-asia` does not exist in borders-geopolitics.md

**File:** `2050-snapshot/kml/borders.kml` (lines 45847, 45860, 45873, 45886, 45899, 45912 for Kazakhstan; similar for all other entities)
**Issue:** Every KML `Placemark` description references:
```
CAC member — See: 2050-snapshot/domains/borders-geopolitics.md#central-asia
```

The `#central-asia` anchor assumes a Markdown heading that generates that fragment identifier. In `borders-geopolitics.md`, the CAC entry at line 385 uses **bold text** (`**Central Asian Confederation (CAC):**`) rather than a Markdown heading (`###` or `##`). No `#central-asia` anchor exists in the document. The CAC content lives under `### Asia` at line 373, which would generate `#asia`, not `#central-asia`.

This means the link reference is non-functional for any tooling that resolves anchors. This affects all 5 constituent republic entries (Kazakhstan has 6 placemarks, Kyrgyzstan 1, Tajikistan 3, Turkmenistan 3, Uzbekistan 3).

**Fix:** Either:
- Change the text in `borders-geopolitics.md` line 385 to a proper heading, e.g., `#### Central Asian Confederation (CAC)` so a `#central-asian-confederation-cac` anchor is generated, then update KML descriptions accordingly, OR
- Change KML descriptions to reference `#asia` instead (which is a valid anchor), OR
- Use an explicit HTML anchor tag in borders-geopolitics.md: `<a name="central-asia"></a>`

### WR-03: climate.md lacks dedicated CAC collective profile section

**File:** `2050-snapshot/domains/climate.md`
**Issue:** The other four domain docs (borders-geopolitics.md lines 385-408, economy.md lines 486-539, demographics.md lines 482-547, culture.md lines 246-256) all contain a dedicated CAC collective profile with a prominent heading. Climate.md has no equivalent section. Central Asia/CAC is discussed only within the broader "Asia" regional section (line 78) and the "Resource Conflicts" section on transboundary water (line 101) and climate migration (line 91), but there is no dedicated CAC/climate profile comparable to the other domains.

This creates an asymmetry that will compound if future phases add climate-specific content — data at the entity level (constituent republic climate vulnerabilities, adaptation capacity, specific climate migration estimates) is missing and not consistently findable.

**Fix:** Add a `#### Central Asian Confederation (CAC)` subsection in climate.md with standardized fields — CAC-wide climate vulnerability summary (glacier melt, water stress, desertification, extreme heat risk), per-constituent-republic variance, adaptation capacity and confederal water management framework, and climate migration estimates. See economy.md's CAC profile (lines 486-493) for the standard profile format.

### WR-04: KML innerBoundaryIs exclave holes are unnamed — cannot identify which exclave

**File:** `2050-snapshot/kml/borders.kml` (lines 45936-45951 for Kyrgyzstan, 46077-46081 for Uzbekistan)
**Issue:** The interior polygon holes for Ferghana Valley exclaves have no `<name>` tags. Kyrgyzstan has 3 inner holes (lines 45936-45951) and Uzbekistan has 1 inner hole (lines 46077-46081). Without named annotations, there is no way to identify which exclave each hole represents (Sokh, Shakhimardan, Vorukh, Barak, etc.).

This violates the pattern established by the parent Placemarks, all of which have `<name>Kazakhstan</name>` etc. The exclaves should follow the same convention.

**Fix:** Add `<name>` elements to each innerBoundaryIs, e.g.:
```xml
<innerBoundaryIs>
  <LinearRing>
    <name>Sokh exclave (Uzbekistan-in-Kyrgyzstan)</name>
    <coordinates>71.05,39.95,0 ...</coordinates>
  </LinearRing>
</innerBoundaryIs>
```

Also note: the current coordinates are rectangular approximations. The exclaves have well-documented geographic coordinates — see D-11 and the agent's discretionary note on exclave coordinate verification.

## Info

### IN-01: KML exclave coordinates are rectangular approximations

**File:** `2050-snapshot/kml/borders.kml` (lines 45936-45951, 46077-46081)
**Issue:** The innerBoundaryIs coordinates for Kyrgyzstan and Uzbekistan exclaves are simple rectangular placeholders (e.g., `71.05,39.95,0 71.20,39.95,0 71.20,40.07,0 71.05,40.07,0 71.05,39.95,0`). The Ferghana Valley exclaves (Sokh, Shakhimardan, Vorukh, Barak) have specific, non-rectangular boundaries that these approximations do not reflect. The CONTEXT.md (agents' discretion item) defers "exclave coordinate accuracy verification method" to the agent.

**Fix:** Update the innerBoundaryIs coordinates to reflect actual exclave boundaries using source data (referenced `2050-snapshot/kml/source/global-countries.kml` or authoritative boundary sources for Sokh, Shakhimardan, Vorukh, Barak). If precise coordinates are unavailable, add a comment noting these are approximations.

### IN-02: Economy.md CAC profile — "aggregate TFR ~2.8" not flagged as demographic domain

**File:** `2050-snapshot/domains/economy.md` (not present)
**Issue:** The economy.md CAC profile (lines 486-493) does not include a TFR figure. This is acceptable (TFR belongs in demographics), but the CAC collective profile in economy.md is slightly thinner than the demographics.md equivalent. No functional issue — the economy profile covers GDP, sectors, trade, and economic model as expected per D-07.

No fix needed — this is a style observation for future profile consistency.

### IN-03: Culture.md "Tajikistan" entry contains civil war death toll without attribution

**File:** `2050-snapshot/domains/culture.md:256`
**Issue:** The Tajikistan profile states "a conflict that killed 50,000-100,000, displaced 1.2M" — specific numbers without citation. This is speculative future history and the numbers are internally consistent with the document's fictional framing, but the specificity contrasts with the more qualitative tone of other profiles in the same section (e.g., Turkmenistan profile at line 252). Not a bug, but notable unevenness in profile construction.

No fix needed — informational observation.

### IN-04: KML Central Asia folder — `(wip)` tag confirmed removed (D-10 compliant)

**File:** `2050-snapshot/kml/borders.kml:45841`
**Issue:** Confirmation: The Central Asia folder name is `<name>Central Asia</name>` with no `(wip)` suffix. This is correct per D-10. No action needed.

### IN-05: KML Afghanistan confirmed removed from Central Asia (D-13 compliant)

**File:** `2050-snapshot/kml/borders.kml` (lines 45838-46084)
**Issue:** Confirmation: The Central Asia folder contains exactly 5 country subfolders: Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Uzbekistan. Afghanistan is not present. This is correct per D-13. No action needed.

---

_Reviewed: 2026-05-27T23:30:00Z_
_Reviewer: gsd-code-reviewer (standard depth)_
_Depth: standard_
