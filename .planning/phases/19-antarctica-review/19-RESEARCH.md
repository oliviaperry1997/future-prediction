# Phase 19: Antarctica Review — Research

**Researched:** 2026-05-30
**Status:** Complete
**Topics:** Ice shelf boundary datasets, 2050 claim configuration, domain doc entry structure, KML claim-zone polygon strategy

---

## 1. Ice Shelf Boundary Datasets (D-03)

### Requirement
D-03 specifies that Antarctica KML polygons use **ice shelf boundaries** as the source geometry, not coastline. The existing GADM pipeline generates coastline-based polygons — this is a new data source requirement.

### Recommended Dataset: SCAR Antarctic Digital Database (ADD)

The **SCAR Antarctic Digital Database (ADD)** is the authoritative vector dataset for Antarctic geography, maintained by the Scientific Committee on Antarctic Research and hosted by the British Antarctic Survey. It provides:

- **Coastline including ice shelves** — the `medium_resolution` coastline layer includes ice shelf fronts, ice shelf grounding lines, and rock outcrop coastlines. This is what D-03 requires: polygons that extend to the ice shelf edge rather than stopping at the rock coastline.
- **Format:** Shapefile / GeoPackage, freely available at `https://www.add.scar.org/`
- **Scale:** 1:1,000,000 (medium resolution) or 1:250,000 (high resolution for Peninsula). Medium resolution is sufficient for KML generation.
- **License:** Open access, CC-BY 4.0 — compatible with project use.

### Alternative: MEaSUREs Antarctic Boundaries (NSIDC)

The NASA MEaSUREs program provides the **Antarctic Ice Shelf Boundaries** dataset at higher spatial resolution:
- **Coverage:** Ice shelf grounding lines and calving front positions derived from satellite imagery (MODIS, Landsat)
- **Format:** Shapefile, hosted at NSIDC
- **Use case:** Higher precision than ADD but more complex to process (separate coastline and grounding line layers must be merged). ADD is simpler for polygon generation.

### Recommendation
Use the **SCAR ADD medium-resolution coastline including ice shelves** as the primary source. It is purpose-built for cartographic use, freely available, and the simplest path to producing per-claim-zone KML polygons with ice-shelf-accurate boundaries. Download ADD shapefile → clip to claim-zone longitudinal sectors → convert to KML polygons → integrate into borders.kml.

### Implementation Path
1. Download ADD coastline shapefile (GeoPackage format)
2. Extract ice-shelf-inclusive coastline geometry
3. Clip to longitudinal sector boundaries (claim zones are defined by meridians)
4. Generate KML polygon for each claim zone
5. Apply entity-specific styles from user_colors.json
6. Replace existing coastline-based Antarctica polygon patches

### Fallback
If ADD download is not feasible (requires interactive web access), the existing GADM Antarctica polygon can be used as a temporary geometry with a note that ice shelf boundaries should be refined when ADD data is available. The claim-zone sector subdivision can still be applied to the existing GADM geometry.

---

## 2. 2050 Claim Configuration (D-02, D-01)

### Methodology
The 2050 claim configuration is determined by cross-referencing the original transition analysis (`antarctica.md`) against revised claimant trajectories from Phases 6-18. Each claimant's Antarctic posture was assessed for changes since the transition doc was written.

### Claim Zones (7 zones for KML)

| # | Claim Zone | Sector (Longitude) | Claimant | Status | Rationale |
|---|-----------|-------------------|----------|--------|-----------|
| 1 | **Australian Antarctic Territory** | 45°E–136°E, 142°E–160°E | Australia | Active (conservationist) | Phase 15: Revolutionary Stage 3. Largest claim (42%). $371M infrastructure program complete. Conservationist coalition leader. Claim actively administered with environmental stewardship emphasis. |
| 2 | **Ross Dependency** | 160°E–150°W | New Zealand | Active (conservationist) | Phase 15: Revolutionary Stage 4. Christchurch gateway role expanded post-US logistics collapse. Scott Base operations continue. Small but high-quality program. |
| 3 | **Adélie Land** | 136°E–142°E | France (EU Federation) | Active | Phase 14: EU Federation member. Claim channeled through EU Federation's Antarctic representation. Kerguelen Islands as logistics base. Claim wedge nested inside Australian sector. |
| 4 | **Dronning Maud Land** | 20°W–45°E | Norway (EU Federation) | Active | Phase 9: EU Federation member. Strong environmental governance tradition. Limited infrastructure but claim maintained under EU framework. |
| 5 | **Argentine-Chilean Joint Antarctic Peninsula** | 53°W–90°W | Argentina + Chile (joint) | Active (sovereignty-revolutionary) | Phase 13: Both revolutionary sovereignty states. Joint administration is the most concrete revolutionary integration outcome in Antarctica. Merged claims into single administrative zone. Absorbs dormant UK Peninsula overlap. Ushuaia and Punta Arenas as dual gateways. |
| 6 | **British Antarctic Territory (Dormant)** | 20°W–53°W | United Kingdom | Dormant (paper claim) | Phase 9: Late-revolutionary, post-Brexit capacity constrained. British Antarctic Survey continues operations but UK cannot enforce territorial claim. Non-Peninsula sector (20°W–53°W) exists only on paper. Peninsula sector (53°W–80°W) absorbed by Argentine-Chilean zone. |
| 7 | **Chinese Marie Byrd Land Zone** | 90°W–150°W | China (de facto) | Active (de facto administration) | Phase 7: Revolutionary Stage 4-5. Not a formal ATS claim — but de facto administered zone with largest infrastructure presence (6 stations, BeiDou SATCOM, krill fleet). Fills active vacuum left by US withdrawal. Marie Byrd Land is the only unclaimed sector — China administers it without formal claim, maintaining ATS Article IV fiction while exercising practical control. |

### Non-Zone Actors
| Actor | Posture | Antarctic Role |
|-------|---------|---------------|
| **Russia** (Phase 8) | Reactionary-extractive | Stations within Australian and Norwegian zones. Junior partner to China. No exclusive zone — operates grey-zone prospecting under "scientific research" cover. |
| **India** (Phase 11) | BRICS+ swing | Two stations in East Antarctica (within Australian sector). Scientific presence only, no claim assertion. BRICS+ governance position aligned with resource access. |
| **South Africa** (Phase 11) | BRICS+ member | SANAE IV station (within Norwegian sector). Cape Town as gateway port. Conservationist-leaning BRICS+ member. |
| **PPR** (Phase 15-18) | NZ successor | Limited non-claimant science collaboration. Pacific orientation aligns with conservationist goals. Budget constraints prevent large-scale commitment. |
| **Brazil** | Not in v1.1 scope | Comandante Ferraz station (within Peninsula zone). South America not reviewed. |

### Key Changes from Original Transition Doc
1. **UK downgraded:** The transition doc treated UK as conservationist coalition member with world-class BAS. Phase 9 revision (post-Brexit capacity constrained, late-revolutionary) reduces UK to paper-claim status. BAS continues operations but UK cannot enforce claim.
2. **Argentina-Chile merged:** Transition doc anticipated joint administration as "most likely outcome." Now confirmed — Peninsula administered as merged zone, absorbing UK overlap.
3. **China elevated:** Transition doc described China as "most consequential Antarctic actor." Phase 7 revision (Stage 4-5, full infrastructure dominance, US vacuum filled) confirms this trajectory. Marie Byrd Land is de facto Chinese zone.
4. **France/Norway EU-framed:** Both are now EU Federation members (Phases 14 and 9). Their Antarctic claims are channeled through EU Federation representation. This changes their claimant identity from standalone states to EU-member claimants.
5. **PPR exists:** Transition doc speculated about US successors. PPR now confirmed (Phases 15-18) as limited non-claimant participant.

### Territorial Integrity Table Update
The current Territorial Integrity table (borders-geopolitics.md line 951) describes Antarctica as "Deliberately unclaimed as sovereign territory — Antarctic Treaty System's Article IV freezing claims remains in effect." This remains technically correct — no claim zone constitutes sovereignty. But the description should be expanded to reflect the 2050 reality: ATS Article IV still in effect, but the 7 claim zones represent de facto administrative divisions under the partial opening regime. The existing language "Deliberately unclaimed" should become "Administered through 7 claim zones under ATS Article IV — claims frozen, not sovereign territory."

---

## 3. Domain Doc Entry Structure (D-05, D-06, D-07, D-08)

### Entry Format
All Antarctica domain entries use the standard `**Entity:**` format established in Phases 15-18, adapted for non-sovereign governance:

```markdown
**Antarctica:** {#antarctica} [Loop stage / governance descriptor] — [One-line summary].
- **[Dimension]:** [Specific detail with data and dynamics]
- **[Dimension]:** [Specific detail]
...
**→ See KML:** [List of claim zones]
```

### Borders-Geopolitics (D-06)
**Current state:** Single paragraph (line 923), ~4 lines. Expand to full entry.
**Entry structure:**
- Governance regime: ATS partial opening, 7 claim zones, Article IV fiction maintained
- Claim zone breakdown: Summary of each of the 7 zones (claimant, sector, status)
- Key dynamics: China's de facto control of MBL, Argentina-Chile joint administration, UK dormancy, conservationist coalition's environmental safeguards
- → See KML cross-references to all 7 claim zones
**Placement:** Standalone `### Antarctica` section replacing the current Polar Regions paragraph. The Arctic paragraph remains adjacent under `### Polar Regions` → `#### Arctic`.

### Economy (D-05)
**Current state:** Zero mentions. Create full entry.
**Entry structure:**
- Resource extraction under partial opening: Designated non-ice-covered zones, environmental safeguards
- Krill fisheries: Chinese fleet dominance, CCAMLR management
- Bioprospecting: Pharmaceutical and industrial enzyme development from extremophile organisms
- Logistics economy: Christchurch (NZ), Ushuaia, Punta Arenas, Cape Town, Hobart as gateway ports
- Tourism: Restricted-access adventure tourism, cruise ship operations
- Non-sovereign economic models: Revenue-sharing from mineral extraction distributed to ATS parties and conservation fund
- Research economy: Station operations, international science funding

### Demographics (D-05)
**Current state:** Zero mentions. Create full entry.
**Entry structure:**
- Permanent population: ~5,000-8,000 year-round across all stations (expanded from ~1,100 in 2020s)
- Rotating personnel: 30,000-40,000 seasonal (summer) across research, logistics, extraction, tourism
- Claimant-nationality distribution: Chinese stations largest single nationality bloc (~40% of permanent population)
- Station communities: McMurdo-area cluster (NZ/US-successor), Peninsula cluster (Argentina-Chile), East Antarctic plateau (multinational)
- Demographics of extraction workforce: Mining and logistics personnel, rotating schedules
- No indigenous population — all residents are rotational or permanent station staff

### Culture (D-05)
**Current state:** Zero mentions. Create full entry.
**Entry structure:**
- Scientific internationalism: The dominant Antarctic cultural value — cooperation across national lines
- Treaty-system institutional culture: ATS governance norms, consultative meeting diplomacy
- Claim-nationality cultures: Argentine/Chilean national identity assertion through Peninsula presence, Chinese state-directed Antarctic culture
- Emergent Antarctic identity: Multi-generation station families, Antarctic-born children, "Antarctican" self-identification
- Environmental stewardship ethos: Conservation as cultural value
- Station life subculture: Winter-over traditions, extreme environment bonding, 300 Club (sauna-to- outdoors ritual)

### Climate (D-05)
**Current state:** Referenced only as ice sheet melt driver (lines 22, 43, 359, 404). Create standalone entry.
**Entry structure:**
- Ice sheet dynamics: WAIS marine ice sheet instability active, East Antarctic Ice Sheet stable but showing marginal retreat, total ice mass loss ~1.5-2.0mm/yr sea level equivalent
- Temperature: Antarctic Peninsula warming fastest (+3°C since 1950s), interior stable
- Ice shelf collapse: Larsen C disintegrated (2030s), Thwaites Glacier retreat accelerating, Pine Island Glacier grounding line retreat
- Ecosystem change: Krill biomass decline (warming + acidification), penguin colony redistribution, invasive species introduction
- Climate research infrastructure: Continent as global climate observatory, ice core records
- Climate-driven governance pressure: Ice-free land exposure enabling extraction, sea level impacts driving global governance engagement

### Technology (D-05)
**Current state:** Zero mentions. Create full entry.
**Entry structure:**
- Station infrastructure: Renewable energy (solar/wind for coastal stations), advanced thermal insulation, water recycling
- Logistics technology: Ice-capable aircraft (ski-equipped), icebreaker fleets (Chinese Xuelong-class dominant), autonomous underwater vehicles for sub-ice survey
- Satellite coverage: BeiDou primary navigation constellation, SAR imagery for ice monitoring
- Ice-penetrating survey technology: Radar for subglacial lake mapping, seismic surveys for mineral exploration
- Extraction technology: Cold-weather mining adaptations, sub-ice drilling, environmental containment
- Scientific instrumentation: Neutrino detectors (IceCube), cosmic microwave background telescopes (South Pole Station), climate monitoring networks

### Consistency Requirements
- All entries use `**Entity:** Antarctica` format (D-07)
- All entries are standalone sections, not bundled under "Polar Regions" (D-08)
- Climate Antarctica entry must remain consistent with ice sheet melt references in existing climate.md content
- Economy demographics must acknowledge non-sovereign status (no GDP, no citizen population — instead resource revenue and station population)
- All entries cross-reference to relevant claim zones via `→ See KML:`

---

## 4. KML Claim-Zone Polygon Strategy (D-01, D-03, D-04)

### Strategy: Replace Single Polygon with 7 Claim-Zone Polygons

**Current state:** `Antarctica (wip)` folder contains a single `Antarctica` subfolder with ~27 coastline-based polygon patches representing the entire continent as one entity.

**Target state:** `Antarctica` folder containing 7 claim-zone subfolders, each with ice-shelf-boundary polygon(s) and distinct KML styles.

### Claim Zone KML Entities

| # | Entity ID | KML Folder Name | Style | Sector Boundaries |
|---|-----------|----------------|-------|-------------------|
| 1 | `Australian Antarctic Territory` | Australian Antarctic Territory | #1f2d4a (keep existing Antarctica style) | 45°E–136°E, 142°E–160°E |
| 2 | `Ross Dependency` | Ross Dependency | New style (NZ-associated) | 160°E–150°W |
| 3 | `Adélie Land` | Adélie Land | New style (EU/France-associated) | 136°E–142°E |
| 4 | `Dronning Maud Land` | Dronning Maud Land | New style (EU/Norway-associated) | 20°W–45°E |
| 5 | `Argentine-Chilean Peninsula` | Argentine-Chilean Peninsula | New style | 53°W–90°W |
| 6 | `British Antarctic Territory` | British Antarctic Territory | Grey/transparent (dormant) | 20°W–53°W |
| 7 | `Chinese Marie Byrd Land` | Chinese Marie Byrd Land | New style (China-associated) | 90°W–150°W |

### Style Strategy
- Australian Antarctic Territory: Keep existing Antarctica color `#1f2d4a` (dark navy — already associated with ATA)
- NZ Ross Dependency: New style, dark green/teal (NZ-associated)
- Adélie Land + Dronning Maud Land: EU-associated blue tones
- Argentine-Chilean Peninsula: Warm red/brown (South American-associated)
- British Antarctic Territory (Dormant): Pale grey with reduced opacity (signals dormancy)
- Chinese Marie Byrd Land: Red (China-associated)

If `user_colors.json` needs new entries, add hex/kml_fill/kml_line for each new entity. Use `gsd-sdk query user-colors add` or manual JSON insertion.

### KML Technical Approach
1. **Source geometry:** SCAR ADD ice-shelf-inclusive coastline (see Section 1)
2. **Clipping:** Clip ADD coastline to longitudinal sector boundaries. Each sector is bounded by two meridians and the South Pole.
3. **Polygon construction:** For each sector, construct a polygon bounded by:
   - Coastline (ice shelf edge, from ADD)
   - Sector boundary meridians (two lines of longitude from coast to South Pole)
   - South Pole point (90°S — the convergence point of all meridians)
4. **Multiple patches:** Some sectors may produce multiple polygon patches (e.g., Australian claim is split by Adélie Land wedge). Generate separate `<Placemark>` for each contiguous patch.
5. **Altitude mode:** Set `<altitudeMode>clampToGround</altitudeMode>` (consistent with existing KML)
6. **Description:** Each Placemark gets `→ See KML: [Claim Zone Name]` and cross-reference to borders-geopolitics.md anchor

### entity-config.json Updates
1. Rename folder group `"Antarctica (wip)"` → `"Antarctica"` (D-04)
2. Replace single entity `"Antarctica"` with 7 claim-zone entities
3. Each entity entry follows standard format:
```json
"AAT": {
  "type": "entity",
  "category": "global",
  "source": "custom",
  "country_code": "ATA-AUS",
  "domain_doc": "2050-snapshot/domains/borders-geopolitics.md",
  "section_anchor": "antarctica",
  "see_path": "See: 2050-snapshot/domains/borders-geopolitics.md#antarctica"
}
```
4. Folder hierarchy updated to:
```json
"Antarctica": [
  "Australian Antarctic Territory",
  "Ross Dependency", 
  "Adélie Land",
  "Dronning Maud Land",
  "Argentine-Chilean Peninsula",
  "British Antarctic Territory",
  "Chinese Marie Byrd Land"
]
```

### user_colors.json Updates
Add 6 new color entries (Australian Antarctic Territory keeps existing `#1f2d4a`). Each entry specifies hex, kml_fill (AABBGGRR format), kml_line, and width.

### (wip) Removal (D-04)
After all polygon edits and entity-config updates, rename `Antarctica (wip)` folder to `Antarctica` in both borders.kml and entity-config.json `folder_hierarchy`. This follows the standard phase completion pattern used in all prior review phases (6-18).

---

## Research Summary

| # | Topic | Finding | Implementation |
|---|-------|---------|---------------|
| 1 | Ice shelf dataset | SCAR ADD medium-resolution coastline including ice shelves | Download GeoPackage → clip to sectors → generate KML polygons |
| 2 | 2050 claim configuration | 7 claim zones: AUS, NZ, FR, NO, ARG-CHL, UK (dormant), CHN (de facto) | 7 KML subfolders, 7 entity-config entries, 6 new styles |
| 3 | Domain doc structure | Full entries across all 6 STEEP domains using standard `**Entity:** Antarctica` format, standalone sections | 5 new doc entries (economy, demographics, culture, climate, technology) + borders-geopolitics expansion |
| 4 | KML polygon strategy | Sector-based clipping of ice shelf coastline, 7 claim-zone polygons replacing single continent polygon | Python generation or manual KML construction using ADD geometry |

---

*Research for Phase 19: Antarctica Review. Last updated: 2026-05-30.*
