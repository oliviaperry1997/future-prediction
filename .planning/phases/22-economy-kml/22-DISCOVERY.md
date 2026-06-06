# Phase 22: Economy KML — Discovery & Data Sourcing

## Overview

Replace the existing economy.kml (8 rough bounding boxes) with 4 data-driven overlay layers for the 2050 economic landscape. All layers are narrative-derived from economy.md entity profiles and Natural Earth open data.

## Layer 1: Cities & Megalopolises

### Data Sources
- **Natural Earth Populated Places (ne_10m_populated_places_simple)**: ~7,300 global cities with population estimates. Downloaded from Natural Earth (naturalearthdata.com). License: public domain.
- **Entity population data**: From demographics.md entity profiles for 2050-specific urban context.

### Megalopolis Calculation: Urban Metric System (UMS)
The UMS formula from Wikipedia defines urban regions via a force-field model:
- Attractive force: A = 1/(1 + d) per inhabitant
- Repulsive force: R = 1/(β + d/2) per inhabitant
- Net force: F = A - R
- β = 81 defines "Megalopolis" — equilibrium at 160 km distance

Implementation approach:
1. Filter NE populated places to cities > 200K population
2. Create a 0.2° global grid over habitable land areas
3. Compute net UMS force at each grid cell from nearby cities (summed, weighted by population/100K)
4. Threshold: cells with F > 0.001 qualify as megalopolis-class
5. Cluster neighboring cells and polygonize

Confidence: MEDIUM — UMS is theoretically sound but NE city population data is current, not 2050. Megalopolis extents are approximate.

### City Point Selection
- Major global cities (> 1M population from NE) with 2050 adjustments
- Additional 2050-relevant cities from narrative (e.g., new capitals, expanded hubs)
- ~50 point placemarks scaled by economic significance

## Layer 2: Production Metric (BCU-Equivalent)

### Data Sources
- **economy.md entity profiles**: GDP estimates in USD for ~200 entities
- **BCU conversion**: The narrative describes BCU as replacing dollar for international settlement. Dollar's share is ~15% of global reserves and declining.

### BCU Conversion Approach
The narrative GDP figures are denominated in "dollars" but this is effectively a 2020-present day narrative convenience. For the BCU-equivalent layer:
- Use the narrative GDP numbers as a proxy for real economic output
- Label the layer as "BCU-equivalent economic output"
- The BCU basket composition (yuan 30%, euro 20%, BCU 20%, gold 15%, etc.) means 1 BCU ≈ 1.3-1.5 USD in purchasing power (since dollar has depreciated)

For entities with $XXXB placeholders (9 African entities): estimate from sector descriptions, regional peers, and population.

### Classification Tiers
- **Major** (>5T BCU): China, European Federation, India
- **Large** (1-5T BCU): Pacifica, Atlantica, Great Lakes, Japan, Brazil, Russia, ROK
- **Intermediate** (200B-1T BCU): Most sovereign states, Aztlán, Australia, EAF, etc.
- **Small** (20-200B BCU): Smaller entities and microstates
- **Micro** (<20B BCU): Island microstates, small territories

## Layer 3: Transit & Logistics Systems

### Data Sources
- **economy.md analysis sections**: Trade corridors, shipping routes, energy infrastructure mentioned in narrative
- **Natural Earth**: Roads (ne_10m_roads), railroads (ne_10m_railroads), ports, airports — for reference geometry
- **Narrative-specific corridors**: Mentioned in trade bloc sections

### Transit Corridors (from narrative)
1. **Pacific-Asia shipping**: Pacifica → East Asia (primary BRICS+ trade route)
2. **North Atlantic route**: Atlantica → European Federation
3. **HVDC corridors**: Aztlán → Pacifica (electricity exports)
4. **Great Lakes shipping**: Great Lakes ↔ Canada rump
5. **Trans-Siberian**: Russia ↔ China (energy, rail)
6. **African growth corridors**: EAF ports → inland, AES → coastal West Africa
7. **Pan-American corridors**: Mexico/Aztlán → Central America
8. **European high-speed rail**: EF integrated HSR network
9. **Spaceports**: Cape Canaveral/spaceport-canaveral, Kourou, Wenchang, Baikonur, expanded sites
10. **BRICS+ energy pipelines**: Russia → China (Power of Siberia 2), Central Asia → China

### Node Placemarks
- Major ports (Shanghai, Singapore, Rotterdam, Los Angeles/Long Beach, etc.)
- High-speed rail hubs
- Spaceports (operational in 2050)
- BRICS+ financial nodes (clearing house, MDB HQ)

## Layer 4: Production Sectors

### Data Sources
- **economy.md entity profiles**: Dominant sectors field for each entity
- **Category mapping**: Map narrative sector descriptions to 6 sector types

### Sector Categories
1. **Technology & Finance**: AI, software, fintech, semiconductor design
2. **Advanced Manufacturing**: Automotive, machinery, steel, aerospace, chemicals
3. **Energy & Extraction**: Oil/gas, mining, renewables (hydro, solar, wind)
4. **Agriculture & Food**: Crop production, livestock, agribusiness
5. **Services & Tourism**: Tourism, hospitality, retail, business services
6. **Mixed/Diversified**: Multiple sectors without clear dominance

## Processing Pipeline

### Step 1: Extract entity data from economy.md
Python regex parsing of entity blocks:
```
**Entity Name:**
- **GDP:** ~$X.XXT
- **Dominant sectors:** ...
- **Economic model:** ...
- **Trade partners:** ...
```

### Step 2: Download NE populated places if not present
- URL: https://naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_populated_places_simple.zip

### Step 3: Generate each layer
- Cities/Megalopolises: NE data → UMS calculation → KML points + polygons
- BCU overlay: Parse → convert → classify → KML entity fills
- Transit: Hard-coded corridor geometries from narrative → KML lines + points
- Sectors: Parse → classify → KML entity fills (separate folder + style)

### Step 4: Merge into economy.kml
- All 4 folders in a single Document
- Standard Google Earth styles with 50% opacity fills
- Bi-directional cross-references

## Environment Requirements
- Python packages: shapely, numpy, scipy, simplekml, requests, fiona, lxml
- All already installed except possibly requests (for NE download)

## Confidence Assessment

| Layer | Confidence | Rationale |
|-------|-----------|-----------|
| Cities & Megalopolises | MEDIUM | UMS is sound but NE data is current, not 2050 |
| BCU Overlay | HIGH | Entity GDP data is in narrative; conversion is simple |
| Transit & Logistics | MEDIUM | Corridors are narrative-derived; geometry is approximate |
| Production Sectors | HIGH | Directly from entity profiles; classification is straightforward |

## References
- Urban Metric System: Wikipedia "Megalopolis" article
- Natural Earth populated places: naturalearthdata.com
- Economy entity profiles: 2050-snapshot/domains/economy.md
- Entity config for geometry: 2050-snapshot/kml/entity-config.json
