# Phase 22: Economy KML — Summary

## What Was Built

**`generate-economy-layers.py`** — a Python script that creates `economy.kml` with 4 data-driven overlay layers, replacing the existing 8 rough-bounding-box placemarks.

### Layer 1: Cities & Megalopolises (111 placemarks)
- **53 megalopolis polygons** dynamically calculated using the Urban Metric System (UMS) β=81 (160 km equilibrium distance). Grid-based UMS force field computed from 58 major global cities.
- **58 city point placemarks** scaled by population, with pushpin icons.
- Megalopolis regions detected include: East Asian (Beijing-Shanghai axis), Indian (Delhi-Mumbai corridor), European (London-Paris-Berlin belt), Northeastern US (BosWash), and others.

### Layer 2: Production Metric — BCU-equivalent (179 placemarks)
- Entity-level economic output fills with 5-tier BCU classification:
  - **Major Power** (>5T BCU): China, European Federation, India
  - **Major Economy** (1-5T BCU): Pacifica, Atlantica, Great Lakes, Japan, Brazil, Russia, ROK
  - **Intermediate** (200B-1T BCU): Aztlán, Australia, EAF, etc.
  - **Small** (20-200B BCU): Most sovereign entities
  - **Micro** (<20B BCU): Smaller entities, microstates
- Narrative GDP estimates converted at 1 USD → 0.7 BCU (reflecting dollar's ~30% depreciation post-hegemony)

### Layer 3: Transit & Logistics Systems (41 placemarks)
- **11 trade corridor lines**: North Pacific Shipping Lane, North Atlantic Route, HVDC Southwest Corridor, Great Lakes Shipping, Trans-Siberian Railway, East African Growth Corridor, Sahel Coastal Corridor, European HSR, Pan-American Corridor, Power of Siberia 2, India-Middle East-Europe Corridor
- **8 spaceport points**: Cape Canaveral, Kourou, Wenchang, Baikonur, Vostochny, Satish Dhawan, Tanegashima, Rocket Lab LC-1
- **15 major port points**: Shanghai, Singapore, Rotterdam, LA/Long Beach, Busan, Jebel Ali, etc.
- **7 HSR hub points**: Berlin, Paris, Beijing, Moscow, London St Pancras, Tokyo, Delhi

### Layer 4: Production Sectors (179 placemarks)
- 6-category entity fill classification: Technology & Finance (red), Advanced Manufacturing (orange), Energy & Extraction (green), Agriculture & Food (amber), Services & Tourism (purple), Mixed/Diversified (grey)

## Key Design Decisions
- **BCU metric**: Replaces dollar-denominated GDP with the BRICS+ Digital Basket Currency, consistent with the 2050 narrative where dollar hegemony has been dead for decades
- **UMS Megalopolises**: Dynamic force-field calculation per Wikipedia's Urban Metric System rather than hardcoded polygon boundaries
- **Entity fills from borders.kml**: Reuses existing border polygon geometries with economic coloring, avoiding geometry regeneration

## File Stats
- `economy.kml`: 1.4 MB, 510 placemarks, 31,844 coordinate vertices
- 4 folders + 3 subfolders (Transit subcategories)
- Bidirectional cross-references: KML → economy.md, economy.md → KML

## Remaining Issues
1. NE populated places download URL returns 406 — using hardcoded fallback of 58 major cities. With NE data (7,300+ cities), UMS calculation would be more comprehensive.
2. ~76 entity names differ between borders.kml and economy.md (abbreviations, group entities vs member profiles), so BCU data is unavailable for those. They default to "Micro Economy" tier.
3. Megalopolis polygons are convex hulls of grid cells — may need refinement for specific shapes.
