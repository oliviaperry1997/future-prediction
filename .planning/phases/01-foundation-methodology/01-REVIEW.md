---
phase: 01-foundation-methodology
reviewed: 2026-05-19T23:45:00Z
depth: standard
files_reviewed: 21
files_reviewed_list:
  - .obsidian/app.json
  - .obsidian/appearance.json
  - .obsidian/community-plugins.json
  - .obsidian/core-plugins.json
  - .obsidian/hotkeys.json
  - .gitignore
  - BASEMAP_README.md
  - templates/base.md
  - templates/domain-doc.md
  - templates/prediction.md
  - templates/counter-scenario.md
  - index.md
  - meta/predictions/prediction-001-us-dissolution.md
  - meta/predictions/prediction-002-socialist-transition.md
  - meta/predictions/prediction-003-climate-displacement.md
  - meta/predictions/prediction-004-ai-governance.md
  - meta/predictions/prediction-005-un-reconfiguration.md
  - meta/predictions/prediction-006-great-lakes-desiccation.md
  - meta/counter-scenario.md
  - meta/dashboard.md
  - meta/consistency-check.md
findings:
  critical: 0
  warning: 2
  info: 3
  total: 5
status: issues_found
---

# Phase 01: Code Review Report — Foundation & Methodology

**Reviewed:** 2026-05-19T23:45:00Z
**Depth:** standard
**Files Reviewed:** 21
**Status:** issues_found

## Summary

Reviewed 21 files from the foundation/methodology phase: Obsidian configuration, `.gitignore`, project index, document templates, prediction register (6 predictions), counter-scenario, dashboard, and consistency-check methodology. This is a documentation/wiki project — no executable code or runtime dependencies. Issues found are limited to documentation logic errors and minor quality concerns:

- **1 logic bug** in a documented Dataview fallback query (incorrect sort order)
- **1 warning** about redundant `.gitignore` patterns
- **3 info items** (YAML readability, dangling references, minor inconsistency)

No critical/security issues were found. The codebase does not contain executable code, secrets, injection vectors, or authentication mechanisms.

---

## Warnings

### WR-01: Fallback Dataview Query Sorts Confidence Incorrectly

**File:** `meta/dashboard.md:32-39`
**Issue:** The View 1 fallback query (for Dataview versions without `choice()` support) uses `SORT confidence ASC` with the stated intent "alphabetical sort: H < M < L". This claim is **factually incorrect**:
- Alphabetical order: `"HIGH"` (H=72) < `"LOW"` (L=76) < `"MEDIUM"` (M=77)
- Therefore `SORT confidence ASC` produces: **HIGH → LOW → MEDIUM**
- The intended order (from the section heading and primary query) is: **HIGH → MEDIUM → LOW**

A user relying on this fallback would see predictions sorted as: HIGH → LOW → MEDIUM (e.g., prediction-003 climate → prediction-005 UN reform → prediction-006 Great Lakes → prediction-001 US dissolution → prediction-002 socialist transition → prediction-004 AI governance). This places LOW-confidence predictions before MEDIUM-confidence ones, making it difficult to assess predictions by confidence weight.

**Fix:**
Option A (recommended): Remove the fallback entirely. `choice()` is a core Dataview function supported since Dataview v0.4.0 (2021). It is unlikely a user has Dataview installed without this function.

Option B: If keeping the fallback, fix the comment to state the actual sort order and warn the user that the fallback sorts as HIGH → LOW → MEDIUM rather than the ideal HIGH → MEDIUM → LOW:

```
> **Fallback** if `choice()` is not supported (note: this sorts HIGH → LOW → MEDIUM alphabetically):
> ```dataview
> TABLE
>   confidence AS "Confidence",
>   target_milestone AS "Target",
>   domain AS "Domain"
> FROM "meta/predictions"
> SORT confidence ASC
> ```
> **Note**: This cannot reproduce the ideal HIGH → MEDIUM → LOW order without `choice()`.
```

---

### WR-02: Redundant and Duplicative .gitignore Patterns

**File:** `.gitignore:3-4`
**Issue:** Patterns `*.DS_Store` (line 3) and `.DS_Store` (line 4) are both present. The `.DS_Store` pattern (without wildcard prefix) already matches `.DS_Store` files at any directory depth — this is how gitignore patterns without `/` work. The `*.DS_Store` pattern only matches files like `foo.DS_Store` (any characters before `.DS_Store`), which do not exist as a concern. One of the two patterns is entirely redundant.

**Fix:** Remove `*.DS_Store` (line 3) and keep only `.DS_Store` (line 4):

```
# macOS metadata
.DS_Store
```

---

## Info

### IN-01: Extremely Long Single-Line YAML Value in counter-scenario.md

**File:** `meta/counter-scenario.md:7`
**Issue:** The `alternative_thesis` field is approximately 290 characters on a single line:

```yaml
alternative_thesis: Revolutionary movements gain sufficient national strength to overcome regional reactionary insurgencies and secessionist movements, consolidating the United States as a single socialist state rather than fragmenting into multiple successor polities.
```

This makes the YAML frontmatter harder to read and edit. YAML supports block scalar syntax for long values.

**Fix:** Use YAML block scalar (`>`) to wrap across multiple lines:

```yaml
alternative_thesis: >
  Revolutionary movements gain sufficient national strength to overcome
  regional reactionary insurgencies and secessionist movements, consolidating
  the United States as a single socialist state rather than fragmenting into
  multiple successor polities.
```

---

### IN-02: All Prediction Files Reference Non-Existent Domain Documents

**File:** All 6 prediction files under `meta/predictions/`
- `meta/predictions/prediction-001-us-dissolution.md:11` → `2050-snapshot/domains/borders-geopolitics.md`
- `meta/predictions/prediction-002-socialist-transition.md:11` → `2050-snapshot/domains/economy.md`
- `meta/predictions/prediction-003-climate-displacement.md:11` → `2050-snapshot/domains/climate.md`
- `meta/predictions/prediction-004-ai-governance.md:11` → `2050-snapshot/domains/technology.md`
- `meta/predictions/prediction-005-un-reconfiguration.md:11` → `2050-snapshot/domains/borders-geopolitics.md`
- `meta/predictions/prediction-006-great-lakes-desiccation.md:11` → `2075-snapshot/domains/climate.md`

**Issue:** All `doc_ref` frontmatter fields point to domain documents that have not yet been created (none of the `2050-snapshot/`, `2075-snapshot/`, or `2100-snapshot/` directories have `domains/` subdirectories). This is expected in Phase 1 since the milestone documents are to be written in later phases. However, there is no tracking mechanism or validation to detect when a `doc_ref` remains unresolved after its target milestone is supposedly complete. This creates a risk of stale/broken references.

**Fix (optional):** Add a `doc_ref_status` field to the prediction template that tracks whether the target has been verified to exist:

```yaml
doc_ref: 2050-snapshot/domains/borders-geopolitics.md
doc_ref_exists: false   # Set to true when domain doc is created and verified
```

Or add a validation step in `meta/consistency-check.md` to include a "Verify all `doc_ref` targets exist" checklist item.

---

### IN-03: Number of Successor States in prediction-001 Reasoning vs Falsifiable Statement

**File:** `meta/predictions/prediction-001-us-dissolution.md:9,31`
**Issue:** The falsifiable statement says "at least three successor states recognized by a majority of UN member states" (line 9), while the reasoning section says "Four to six successor states are the most likely outcome" (line 31). These are not strictly contradictory — the FS sets a minimum bound of 3, and the reasoning discusses 4-6 as the likely range — but a reader encountering both figures may be confused whether the lower bound is 3 or 4. Clarity would be improved by aligning the figures or explicitly noting the relationship.

**Fix:** Add a clarifying sentence in the reasoning:

```markdown
Four to six successor states are the most likely outcome (consistent with the minimum of 3
specified in the falsifiable statement)...
```

Alternatively, adjust the falsifiable statement to "at least four" or add a note that 3 is a deliberately conservative lower bound.

---

_Reviewed: 2026-05-19T23:45:00Z_
_Reviewer: gsd-code-reviewer_
_Depth: standard_
