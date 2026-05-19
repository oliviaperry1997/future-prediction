---
title: Prediction Register Dashboard
status: draft
created: 2026-05-19
updated: 2026-05-19
tags: [dashboard, dataview, predictions]
---

# Prediction Register Dashboard

> Use this dashboard in Obsidian's Reading mode (not Source/Edit mode) to see live Dataview query results.
> Queries read from `meta/predictions/` — predictions are individual `.md` files with YAML frontmatter.

## View 1: Predictions by Confidence (HIGH → MEDIUM → LOW)

Predictions sorted by confidence level descending, showing title, target milestone, domain, and status.

```dataview
TABLE
  confidence AS "Confidence",
  target_milestone AS "Target",
  domain AS "Domain",
  status AS "Status",
  falsifiable_statement AS "Falsifiable Claim"
FROM "meta/predictions"
SORT
  choice(confidence = "HIGH", 0, confidence = "MEDIUM", 1, 2) ASC,
  target_milestone ASC
```

## View 2: Predictions by Target Milestone

Predictions grouped by target milestone year, showing confidence level and domain. Useful for milestone-level calibration reviews.

```dataview
TABLE
  target_milestone AS "Target Milestone",
  rows.title AS "Predictions",
  rows.confidence AS "Confidence",
  rows.domain AS "Domain"
FROM "meta/predictions"
GROUP BY target_milestone
SORT target_milestone ASC
```

## View 3: Predictions by Domain

Predictions grouped by STEEP domain, showing count and confidence distribution per domain. Use this for cross-domain consistency reviews.

```dataview
TABLE
  rows.title AS "Predictions",
  rows.confidence AS "Confidence",
  rows.target_milestone AS "Target"
FROM "meta/predictions"
GROUP BY domain
SORT domain ASC
```

## View 4: Predictions by Status

Filters predictions by their review status (draft / review / final). Use this to track which predictions have been reviewed.

```dataview
TABLE
  status AS "Status",
  confidence AS "Confidence",
  target_milestone AS "Target",
  domain AS "Domain"
FROM "meta/predictions"
WHERE status != "final"
SORT status ASC, confidence ASC
```

## View 5: Recently Added / Updated

Shows the most recently created or updated predictions, limited to the 10 most recent.

```dataview
TABLE
  created AS "Created",
  updated AS "Updated",
  confidence AS "Confidence",
  domain AS "Domain"
FROM "meta/predictions"
SORT created DESC
LIMIT 10
```

## Usage Notes

- **Refresh:** Dataview auto-refreshes when you open the file or switch to it
- **Reading mode:** Results only render in Reading mode (not Source/Edit or Live Preview)
- **Adding predictions:** Create a new file in `meta/predictions/` with the prediction template — Dataview picks it up automatically
- **Status workflow:** `draft` → `review` → `final` — update the status field as predictions are reviewed against new evidence
