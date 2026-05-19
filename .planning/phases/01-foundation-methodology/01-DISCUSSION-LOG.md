# Phase 1: Foundation & Methodology - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-19
**Phase:** 01-foundation-methodology
**Areas discussed:** Vault location & directory layout, YAML frontmatter schemas, Prediction register & counter-scenario, Cross-domain consistency

---

## Vault Location & Directory Layout

| Option | Description | Selected |
|--------|-------------|----------|
| In-repo vault (Recommended) | Creates .obsidian/ alongside .planning/. Everything in one place, easy git tracking, single workspace | ✓ |
| Separate directory | Vault lives outside the repo. Needs manual linking | |

**User's choice:** In-repo vault
**Notes:** User wants the vault inside the project repo

| Option | Description | Selected |
|--------|-------------|----------|
| Flat per milestone (Recommended) | Each milestone gets a folder. Numbered prefixes for domain docs | ✓ |
| Domain-first hierarchy | Each domain gets a folder, with milestone sub-folders | |
| Hybrid | Milestones with domain subdirs | |

**User's choice:** Flat per milestone

| Option | Description | Selected |
|--------|-------------|----------|
| Templates + Meta + Sources + Index | Standard supporting dirs structure | ✓ |
| Minimal | Just templates + content | |

**User's choice:** Templates + Meta + Sources + Index

---

## YAML Frontmatter Schemas

| Option | Description | Selected |
|--------|-------------|----------|
| Standardized required + optional fields | Required: title, domain, milestone, status, created, updated. Optional: tags, confidence_crossrefs | ✓ |
| Minimal frontmatter | Just title, domain, milestone | |

**User's choice:** Standardized with required + optional fields

| Option | Description | Selected |
|--------|-------------|----------|
| Shared base + extensions (Recommended) | Common fields on all docs, domain-specific fields per type | ✓ |
| Separate schemas per type | Each type has its own schema | |

**User's choice:** Shared base + extensions

---

## Prediction Register & Counter-Scenario

| Option | Description | Selected |
|--------|-------------|----------|
| Individual prediction notes (Recommended) | Each prediction is its own .md with YAML frontmatter | ✓ |
| Single master list | One file with a table | |

**User's choice:** Individual prediction notes

| Option | Description | Selected |
|--------|-------------|----------|
| HIGH / MEDIUM / LOW with criteria (Recommended) | Three-tier with written criteria | ✓ |
| Numbered 1-5 | More granular but harder to calibrate | |
| Percentage estimate | Most granular but false precision | |

**User's choice:** HIGH / MEDIUM / LOW with criteria

| Option | Description | Selected |
|--------|-------------|----------|
| Single structured document (Recommended) | One /meta/counter-scenario.md | ✓ |
| Directory of docs | One file per domain | |

**User's choice:** Single structured document

| Option | Description | Selected |
|--------|-------------|----------|
| Standard alternatives | US adapts / Multi-polar fragmentation / Authoritarian consolidation | |
| User's custom thesis | Clean revolution — revolutionary movements win nationwide, consolidating as a single socialist state | ✓ |

**User's choice:** Custom: "clean revolution" thesis where revolutionary movements overcome reactionary movements nationwide to form a single socialist state, contrasting with the primary scenario's region-by-region fragmentation.

| Option | Description | Selected |
|--------|-------------|----------|
| Confidence + milestone views | Two main queries: by confidence, by milestone | |
| Full dashboard (Recommended) | Multiple views: confidence, milestone, domain, status, recent | ✓ |

**User's choice:** Full dashboard

---

## Cross-Domain Consistency

| Option | Description | Selected |
|--------|-------------|----------|
| Dataview + manual review (Recommended) | /meta/consistency-check.md with Dataview queries, author reviews flagged items | ✓ |
| Dedicated cross-ref YAML fields | conflicts_with and consistent_with fields | |
| Simple checklist | Manual checklist before finalizing | |

**User's choice:** Dataview + manual review

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — predictions reference domain docs (Recommended) | Each prediction has a doc_ref field linking to domain doc | ✓ |
| No — keep predictions independent | Cross-referencing happens manually | |

**User's choice:** Yes — predictions reference domain docs

---

## the agent's Discretion

- Milestone folder naming conventions and file naming patterns
- Template styling and YAML layout details
- Dataview query implementation syntax
- Consistency check review cadence
- Root index.md content
- .gitignore additions for .obsidian/

## Deferred Ideas

- Prediction register review and calibration tracking — future methodology phase
- Synthesis and retrospective across milestones
- KML tooling improvements (confidence-encoded opacity, NetworkLink, shared styles)
