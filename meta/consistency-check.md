---
title: Cross-Domain Consistency Check
status: draft
created: 2026-05-19
updated: 2026-05-19
tags: [consistency, methodology, review]
---

# Cross-Domain Consistency Check

> **Purpose:** Ensure that assumptions made in one STEEP domain do not contradict assumptions in another.
> **Process:** Dataview queries surface claims → Author reviews for conflicts → Flagged items are resolved.
> **Authority:** The author is the consistency engine. This document supports but does not automate the review.

## When to Run a Consistency Check

Run this check before finalizing any milestone. The review cadence is:

1. **After first draft** of all domain documents for a milestone — check for obvious contradictions
2. **Before finalizing** a milestone — thorough cross-domain reconciliation
3. **When significant new evidence** changes a key assumption — spot-check affected domains
4. **Before starting the next milestone** — ensure the existing foundation is consistent

## Dataview Queries

### Q1: Predictions Grouped by Domain

Use this to see all predictions within each STEEP domain. Read across rows: do any predictions in one domain implicitly rely on assumptions that conflict with predictions in another domain?

```dataview
TABLE
  rows.title AS "Prediction",
  rows.confidence AS "Confidence",
  rows.target_milestone AS "Target",
  rows.falsifiable_statement AS "Claim"
FROM "meta/predictions"
GROUP BY domain
SORT domain ASC
```

### Q2: Predictions by Domain Cross-Reference

For each prediction, shows which domain document it references. Use this to verify that each prediction's `doc_ref` target exists and corresponds to a real domain analysis.

```dataview
TABLE
  doc_ref AS "Domain Document Reference",
  domain AS "Domain",
  target_milestone AS "Milestone"
FROM "meta/predictions"
WHERE doc_ref
SORT domain ASC, target_milestone ASC
```

### Q3: High-Impact Claims (HIGH Confidence)

HIGH confidence predictions carry the most weight — they're the ones most likely to be treated as established fact. They need the most careful cross-domain checking.

```dataview
TABLE
  title AS "Prediction",
  domain AS "Domain",
  target_milestone AS "Target",
  falsifiable_statement AS "Claim"
FROM "meta/predictions"
WHERE confidence = "HIGH"
SORT domain ASC
```

## Review Process

### Step 1: Domain-by-Domain Review

For each domain (borders, climate, technology, economy, demographics, culture):

1. Open the domain document for the milestone being reviewed
2. Note the key assumptions and claimed states (e.g., "Great Lakes water levels drop 2m by 2075")
3. Check Q1 results for predictions in this domain
4. Verify that predictions in this domain are consistent with the domain doc's narrative

### Step 2: Cross-Domain Pair Check

Check domain pairs for consistency conflicts. The most important pairs to check:

| Domain A | Domain B | Common Conflict Pattern |
|----------|----------|------------------------|
| Climate | Borders | Climate-driven migration changes borders; borders constrain migration response |
| Climate | Economy | Climate impacts constrain economic assumptions; economic capacity determines adaptation |
| Technology | Economy | Tech transformation pace must match economic structure assumptions |
| Economy | Demographics | Economic system determines population distribution; demographics constrain labor force |
| Demographics | Borders | Population distribution drives territorial claims; borders channel migration |
| Culture | All | Ideological shifts enable or constrain all other domain changes |

For each pair:
1. Read the "Interactions With Other Domains" section in both domain docs
2. Check Q3 for HIGH confidence predictions in both domains
3. Ask: "If Domain A says X, can Domain B's claims still be true?"
4. Record any contradictions in the Consistency Map below

### Step 3: Reconciliation

When a conflict is found:
1. **Flag it** in the Consistency Map with status "Conflict"
2. **Determine severity:** Does the conflict break the milestone's internal logic, or is it a minor tweak?
3. **Resolve:** Edit one or both domain docs to remove the contradiction
4. **Propagate:** Check if the resolution affects other domains or predictions
5. **Re-check:** Re-run the pair checks for affected domains

### Step 4: Finalize

When no conflicts remain:
1. Mark all consistency map items as "✓ Resolved"
2. Update the milestone status to "consistent"
3. Commit the milestone

## Cross-Domain Consistency Map

Populate this table during each milestone review. Each row is a claim that appears in one domain and has implications for another.

| Claim | Appears In (Domain) | Affects (Domain) | Status |
|-------|---------------------|-------------------|--------|
| _(Add rows during review)_ | | | |

### Status Values

- **✓** — Checked and consistent
- **⚠** — Potential conflict, needs review
- **✗** — Confirmed conflict, needs resolution
- **—** — Not yet checked

## Quick Reference: Domain Boundary Conditions

The following are the most assumption-sensitive variables across domains. When any of these change in one domain, check ALL other domains for ripple effects.

- **Climate trajectory** (warming scenario, sea-level rise, extreme event frequency)
- **US collapse timeline** (affects every other domain)
- **Technology breakthrough level** (especially energy, AI, biotechnology)
- **Demographic variant** (UN high/medium/low, migration assumptions)
- **Economic system type** (capitalist/socialist/mixed, degree of state control)
- **Ideological landscape** (dominant belief systems, international norms)
