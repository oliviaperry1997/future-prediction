# Phase 5: 2050 KML Maps & Integration — Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in CONTEXT.md — this log preserves the discussion flow.

**Date:** 2026-05-21
**Phase:** 05-2050-kml-maps-integration
**Mode:** discuss (interactive)

## Areas Discussed

### 1. KML File Structure & Layer Organization

| Question | Options Presented | User Selection | Notes |
|----------|-----------------|----------------|-------|
| KML file organization | Single per entity / One per domain / Single monolithic | Freeform: "Whatever allows me to apply my own formatting in Google Earth" | User prioritizes styling control in Google Earth Pro. Research confirmed: folders enable bulk restyling. |
| Folder hierarchy | Flattened list / Categorized by entity type / Geographic hierarchy | Geographic hierarchy (like basemap) | Mirrors the Earth Current.kml basemap: Continent > Subregion > Entity |
| Entity coverage in domain KMLs | All entities in every file / Entity polygons only in borders.kml | Entity polygons only in borders.kml | borders.kml is the authoritative geographic layer |
| Overlay placemarks | Point placemarks / Rough polygon overlays / Folder-level annotations | Rough polygon overlays | Domain-specific overlays drawn as polygons, not points |
| More questions? | Yes / No | No — moved to next area | |

### 2. Scope of KML Content: What Gets Mapped Beyond Borders

(Handled in conjunction with area 1 — decisions merged)

### 3. Cross-Reference Format & Bidirectional Linking

| Question | Options Presented | User Selection | Notes |
|----------|-----------------|----------------|-------|
| KML→markdown format | Full relative paths / Just section / Both | Full relative file paths with section anchors | e.g., `See: 2050-snapshot/domains/borders-geopolitics.md#pacific-peoples-republic` |
| Overlay placemark descriptions | Inline description / Inline + excerpt | Inline description in each overlay placemark | Simple See: path, no balloon excerpt |
| Fragmented entity handling | Single collective polygon / Multiple sub-entity polygons | Multiple sub-entity polygons | Atlantic South, Appalachian Zone, Mountain Tapestry as sub-polygons |
| More questions? | Yes / No | No — moved to next area | |

### 4. Territorial Verification & Polygon Detail

| Question | Options Presented | User Selection | Notes |
|----------|-----------------|----------------|-------|
| Polygon detail level | State-line-based / Narrative-derived | Detailed narrative-derived boundaries | Based on borders-geopolitics.md descriptions |
| Verification approach | Manual checklist doc / In-KML folder structure | In-KML folder structure as verification | KML Places panel is the checklist |
| Polygon creation process | User draws from specs / Script generates / Hybrid | Generate KML from a script | User will refine in Google Earth Pro |
| US successor state source data | Placeholder coords / State KML dataset | County-level polygon data | PPR = CA+OR+WA+Clark County NV needs county precision |
| Global entity source data | Extracted from basemap / Fresh KML dataset | Fresh global KML dataset | From geoBoundaries or Census |
| Antarctica | In borders.kml / Separate file | Include in borders.kml | Per D-29 — deliberate resolution required |
| Additional area: polygon resolution | Full resolution / Simplified / Match basemap | ~5-20km vertex spacing | Apply Douglas-Peucker simplification |
| 2050-specific global modifications | Use basemap as-is / Draw 2050-specific | Draw 2050-specific modifications | Palestine, Israel, EU, Canada-Quebec, etc. |

## Key Decisions Summary

- One KML per STEEP domain, geographic hierarchy inside
- Entity polygons only in borders.kml; domain KMLs are overlay-only
- Full relative paths in See: fields for KML→markdown
- County-level source for US entities, country-level for global
- Narrative-derived boundaries with 5-20km vertex spacing
- In-KML folder hierarchy as verification checklist
- Programmatic generation with user refinement in Google Earth Pro
- KML format (not KMZ)
- Fragmented entities as sub-polygons
- 2050-specific modifications for all described global border changes

## Deferred Ideas Captured

- V2 KML tooling (confidence-encoded opacity, NetworkLink, shared styles)
- Economic/demographic zone KML layers
- Automated boundary verification script
- Entity-level language profiles in KML

---

*Discussion recorded: 2026-05-21*
