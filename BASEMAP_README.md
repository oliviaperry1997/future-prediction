---
title: Modern-Day Basemap
status: final
created: 2026-05-19
---

# Modern-Day Basemap

**Status:** Pre-existing — built by the author in Google Earth Pro.

## Location

- Source KML: `basemap/kml/modern-day-borders.kmz` (or `.kml`)
- The original modern-day basemap file should be placed here.

## Coverage

- Sovereign state boundaries as of 2026
- Maritime boundaries and Exclusive Economic Zones (EEZs)
- Major disputed territories with demarcation lines

## Coordinate System

- WGS-84 (standard for Google Earth / KML)

## Usage

- This is the t=0 starting point for all projections in this project
- Each milestone's `doc.kml` can reference this via NetworkLink for visual diff
- Current basemap covers all UN member states plus major de facto states

## Caveats

- Basemap reflects the author's best understanding of current borders
- Some disputed boundaries (Western Sahara, Kashmir, Crimea, etc.) use the de facto control line
- The basemap is for reference only — it will be modified in milestone KML files

## See Also

For basemap updates, edit the KML directly in Google Earth Pro and save back to `basemap/kml/`.
