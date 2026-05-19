# Architecture: Geopolitical Forecasting Document & Map Structure

**Project:** Future Prediction (2050 / 2075 / 2100 snapshots)
**Researched:** 2026-05-19
**Mode:** Ecosystem
**Confidence:** HIGH (domain patterns from strategic foresight + KML best practices are well-established)

---

## 1. High-Level Architecture Overview

The project produces **three coordinated world-state descriptions** at quarter-century intervals, connected by **transition narratives** that explain the causal path between them. Each world-state has two parallel representations:

| Representation | Format | Purpose |
|---|---|---|
| **Written** | Markdown (6 domain files + 1 index) | Rationale, narrative, causal logic, descriptions |
| **Mapped** | KML polygons (6 domain layers + 1 root) | Geographic instantiation of the written state |

These two representations form a **bidirectional pair**: every significant geographic change described in markdown has a corresponding KML polygon, and every KML polygon references the markdown section that justifies it.

```
┌─────────────────────────────────────────────────────┐
│                   MASTER INDEX                       │
│                  (index.md)                          │
│  Links to: basemap, all milestones, all transitions  │
└──────────┬──────────┬──────────┬──────────┬──────────┘
           │          │          │          │
           ▼          ▼          ▼          ▼
     ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
     │modern-day│ │ 2050    │ │ 2075    │ │ 2100    │
     │basemap  │ │snapshot │ │snapshot │ │snapshot │
     │KML only │ │MD + KML │ │MD + KML │ │MD + KML │
     └─────────┘ └────┬────┘ └────┬────┘ └────┬────┘
                      │           │           │
                      ▼           ▼           ▼
               ┌──────────┐ ┌──────────┐ ┌──────────┐
               │Transition│ │Transition│ │Transition│
               │2026-2050 │ │2051-2075 │ │2076-2100 │
               │MD only   │ │MD only   │ │MD only   │
               └──────────┘ └──────────┘ └──────────┘
```

**Key architectural principle:** Transitions describe *how* (drivers, shocks, trends). Snapshots describe *what* (resulting configuration). The two are never conflated — a transition file doesn't redraw borders, a snapshot file doesn't explain the arc.

---

## 2. Directory & File Structure

```
future-prediction/
│
├── index.md                          # MASTER INDEX
│                                     # Links to every file in the project.
│                                     # Single entry point for navigation.
│
├── BASEMAP_README.md                 # Documents the modern-day KML basemap.
│                                     # Notes what it covers, coordinate system,
│                                     # source data, caveats.
│
├── basemap/                          # MODERN-DAY STARTING POINT
│   └── kml/
│       └── modern-day-borders.kmz    # Pre-existing basemap (user already built)
│       └── modern-day-borders.kml    # Uncompressed source (for reference/diff)
│
├── transitions/                      # ARC DOCUMENTS (markdown only)
│   ├── 2026-2050.md                  # Present day → 2050
│   ├── 2051-2075.md                  # 2050 → 2075
│   └── 2076-2100.md                  # 2075 → 2100
│
├── 2050/                             # MILESTONE 1
│   ├── index.md                      # World summary, key differences from today
│   ├── domains/                      # Domain-by-domain analysis
│   │   ├── borders-geopolitics.md    # Borders, states, alliances, zones
│   │   ├── climate.md                # Physical environment, resources
│   │   ├── technology.md             # Energy, AI, transport, space, bio
│   │   ├── economy.md                # GDP, trade blocs, resource flows
│   │   ├── demographics.md           # Population, migration, urbanization
│   │   └── culture.md                # Ideologies, media, religion, values
│   │
│   └── kml/                          # Geographic representation
│       ├── doc.kml                   # Root - NetworkLinks to all domain KMLs
│       ├── borders.kml               # Sovereignty polygons
│       ├── climate.kml               # Climate zones, resource boundaries
│       ├── technology.kml            # Infrastructure, facilities, zones
│       ├── economy.kml               # Trade corridors, economic zones
│       ├── demographics.kml          # Population density, migration routes
│       └── culture.kml               # Cultural/ideological zones
│
├── 2075/                             # MILESTONE 2 (same structure)
│   ├── index.md
│   ├── domains/
│   │   └── ...
│   └── kml/
│       └── ...
│
└── 2100/                             # MILESTONE 3 (same structure)
    ├── index.md
    ├── domains/
    │   └── ...
    └── kml/
        └── ...
```

### File Naming Conventions

| Entity | Convention | Example |
|--------|-----------|---------|
| Milestone directories | 4-digit year | `2050/`, `2075/`, `2100/` |
| Transition files | Year range, kebab-case | `2051-2075.md` |
| Domain markdown | kebab-case, domain name | `borders-geopolitics.md` |
| Root KML | `doc.kml` (Google Earth convention) | `2050/kml/doc.kml` |
| Domain KML | kebab-case, matches markdown | `2050/kml/borders.kml` |

### Rationale

- **Flat domain structure per milestone** (no sub-sub-directories): Avoids deep nesting. Six files is manageable at one level.
- **Transitions separate from milestones**: Prevents confusion between "what happened" and "what resulted." You can read a transition without opening any snapshot.
- **kml/ subdirectory per milestone**: KML files are generated/edited in Google Earth; keeping them in a known subdirectory avoids cluttering the milestone root.
- **Standalone KML, not KMZ**: Google Earth NetworkLinks support local `.kml` files with relative paths. Keeping files uncompressed means they're Git-diffable and you can edit individual domain layers without rebuilding a KMZ archive. Export to KMZ for distribution if desired.

---

## 3. Milestone Snapshot Anatomy

### 3.1 Domain Markdown Files

Each domain file follows a **uniform template** to ensure consistency across milestones:

```markdown
# [Domain]: [Milestone Year] Snapshot

**Headline:** One-sentence characterization of the biggest change.

## Key Changes From Previous Milestone (or from present day)

- Change 1: Brief description with transition doc reference
- Change 2: Brief description with transition doc reference

## [Region/Subdomain 1]

Detailed analysis, narrative, supporting logic.
Maps to KML placemarks in [domain].kml.

### [Specific Entity or Area]
→ See KML: [Placemark Name in borders.kml]

## [Region/Subdomain 2]

...

## Driving Forces

What key drivers from the transition period produced this domain's state?
References back to transition doc section headers.

## Interactions With Other Domains

Cross-domain dependency notes (e.g., "Climate-driven migration shapes borders")
```

**Key structure rules:**
- Each major geographic entity in `borders-geopolitics.md` has a `→ See KML:` marker pointing to its KML placemark
- Each domain ends with an "Interactions With Other Domains" section to explicitly capture cross-domain coupling
- "Key Changes From Previous Milestone" creates explicit traceability back to transition docs

### 3.2 Milestone Index File

`2050/index.md` serves as the snapshot's table of contents and world-summary:

```markdown
# 2050: World Snapshot

**One-paragraph summary of the world in 2050.**

## State of the System

| Domain | Headline Change | Impact Level |
|--------|----------------|--------------|
| Borders | [headline] | High/Med |
| Climate | [headline] | High/Med |
| Technology | [headline] | High/Med |
| Economy | [headline] | High/Med |
| Demographics | [headline] | High/Med |
| Culture | [headline] | High/Med |

## Map
Open `kml/doc.kml` in Google Earth to view the 2050 world map.

## Cross-Domain Synthesis
How the six domains interact in this snapshot (1-2 paragraphs).

## Navigation
- [Borders & Geopolitics](domains/borders-geopolitics.md)
- [Climate](domains/climate.md)
- ...
- [Transition 2026-2050](../transitions/2026-2050.md)
- [Transition 2051-2075](../transitions/2051-2075.md)
```

### 3.3 KML Map Structure

Each milestone has a root `doc.kml` that uses **NetworkLinks** to load domain-specific KML files:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>2050 World</name>
    <description>Future Prediction milestone: 2050.
Open individual domain KML files directly to edit them.
See ../index.md for written analysis.</description>

    <Folder>
      <name>Domain Layers - 2050</name>

      <NetworkLink>
        <name>Borders & Geopolitics</name>
        <description>Sovereignty boundaries. See domains/borders-geopolitics.md</description>
        <Link><href>borders.kml</href></Link>
      </NetworkLink>

      <NetworkLink>
        <name>Climate</name>
        <description>Climate zones, resource boundaries. See domains/climate.md</description>
        <Link><href>climate.kml</href></Link>
      </NetworkLink>

      <!-- ... (one NetworkLink per domain) ... -->
    </Folder>

    <Folder>
      <name>Reference Layers</name>
      <NetworkLink>
        <name>Modern-Day Borders (for comparison)</name>
        <Link><href>../../../basemap/kml/modern-day-borders.kml</href></Link>
      </NetworkLink>
      <!-- Optional: grass-cover overlays, legend etc. -->
    </Folder>
  </Document>
</kml>
```

**Each domain KML** (e.g., `borders.kml`) contains:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Borders & Geopolitics (2050)</name>
    <description>
      Open `2050/domains/borders-geopolitics.md` for the written rationale
      behind every border in this file.
    </description>

    <Folder>
      <name>North America</name>
      <Placemark>
        <name>North American Federation</name>
        <description>
          Formed 2045 after US dissolution.
          See: 2050/domains/borders-geopolitics.md → North American Federation
          Key change from basemap: USA, Canada, Mexico merged into single federation.
        </description>
        <Polygon>
          <outerBoundaryIs><LinearRing><coordinates>...
          </coordinates></LinearRing></outerBoundaryIs>
        </Polygon>
      </Placemark>
      <!-- ... more placemarks ... -->
    </Folder>

    <Folder>
      <name>Europe</name>
      <!-- ... -->
    </Folder>
  </Document>
</kml>
```

**KML organization principles:**
- Group polygons by region/continent in `<Folder>` elements (matches markdown's regional structure)
- Every `<Placemark>` `<description>` includes a back-reference to the relevant markdown file and section
- Every border change from the modern-day basemap is explicitly noted in the `<description>`
- Use consistent color/style schemes across milestones: e.g., all North American Federation polygons use the same style in 2050, 2075, 2100 (so you can visually track continuity)

---

## 4. Transition Document Anatomy

Transition documents are **narrative-only** (no separate KML). They describe the causal pathway between snapshots.

```markdown
# 2026-2050: Transition

**Time span:** 2026 to 2050 (25 years)

## Arc Summary

2-3 paragraphs describing the overall direction of change.
What collapsed, what emerged, what was the dominant logic?

## Timeline of Key Events

| Year | Event | Domain(s) Affected | Impact |
|------|-------|--------------------|--------|
| 2028 | [major event] | Borders, Economy | Triggered X |
| 2032 | [major event] | Climate, Demographics | Accelerated Y |
| ... | ... | ... | ... |

## Driver Analysis (STEEP Framework)

One section per `→ Domain`, describing the key drivers that shaped that domain's 2050 state.

### Borders & Geopolitics
[Drivers, key decisions, wars, treaties, collapses]

### Climate
[Climate trajectory, tipping points, resource pressures]

### Technology
[Breakthroughs, bottlenecks, diffusion patterns]

### Economy
[Reconfigurations, crises, new systems]

### Demographics
[Migration waves, population shifts, disease]

### Culture
[Ideological shifts, information ecosystems]

## Causal Chain Summary

```
2028: Event A ──→ 2032: Consequence B ──→ 2040: Systemic shift C ──→ 2050: State D
        │                    │
        ▼                    ▼
  2030: Side-effect E    2035: Side-effect F
```

## Cross-Domain Feedback Loops

Which domains reinforced or counteracted each other during this period.

## Open Uncertainties

Things that could have gone differently. Alternate forks the author considered.
```

### Relationship Between Transitions and Snapshots

```
Transition 2026-2050      2050 Snapshot
┌──────────────────┐     ┌──────────────────────┐
│ Driver X ────────┼────►│ borders-geopolitics  │
│ Driver Y ────────┼────►│ (resulting state)    │
│ Driver Z ────────┼────►│                      │
│                  │     │   ▲ See KML markers   │
│ Timeline of     │     │   │ linking to KML    │
│ events leading  │     │   │ polygons          │
│ to each domain  │     └───┼──────────────────┘
│ state           │         │
└──────────────────┘         │
                             ▼
                    ┌──────────────────────┐
                    │ 2050/kml/            │
                    │ borders.kml          │
                    │ (polygons with       │
                    │  back-references to  │
                    │  markdown)           │
                    └──────────────────────┘
```

**Information flow is unidirectional:** Transitions → Snapshots (written) → KML (mapped). You can always trace a KML polygon back through markdown to the transition driver that created it.

---

## 5. Cross-Referencing System

Three types of cross-reference ensure internal consistency:

### 5.1 Markdown → KML

In markdown domain files, use the marker `→ See KML:` to point to specific placemarks:

```markdown
### North American Federation
Formed in 2045 from the dissolution of the United States, Canada, and Mexico.
→ See KML: [North American Federation in 2050/kml/borders.kml]
```

**Convention:** `→ See KML: [Placemark Name in filename.kml]`

### 5.2 KML → Markdown

In KML `<description>` elements, reference the corresponding markdown:

```xml
<description>
  Formed 2045 after US dissolution.
  See: 2050/domains/borders-geopolitics.md → North American Federation
  Key change from basemap: USA, Canada, Mexico merged.
</description>
```

**Convention:** `See: [relative-path.md] → [Section Heading]`

### 5.3 Transition → Snapshot

In transition docs, reference the snapshot domain file that results from a driver:

```markdown
### Border Realignment
The collapse of US federal authority in the 2030s led to...
→ Result: See 2050/domains/borders-geopolitics.md for the border configuration.
```

**Convention:** `→ Result: See [milestone]/domains/[domain].md`

### 5.4 Master Index

`index.md` at the project root links to everything:

```markdown
# Future Prediction: Project Index

## Milestones
- [2050 Snapshot](2050/index.md)
- [2075 Snapshot](2075/index.md)
- [2100 Snapshot](2100/index.md)

## Transitions
- [2026-2050: Collapse & Realignment](transitions/2026-2050.md)
- [2051-2075: Transitional Chaos](transitions/2051-2075.md)
- [2076-2100: Consolidation](transitions/2076-2100.md)

## Basemap
- [Modern-Day Borders](BASEMAP_README.md)
```

---

## 6. Domain Content Templates

Each domain should answer specific questions for each milestone. These ensure coverage consistency:

### 6.1 `borders-geopolitics.md`

| Question | KML Element |
|----------|-------------|
| What sovereign states exist? | Polygon per state |
| What alliances/blocs exist? | Colored regions or overlay |
| Which borders changed since last milestone? | Highlighted border lines |
| What zones are disputed or contested? | Hatched polygons |
| What supranational organizations govern supranational space? | Regional polygons |
| Which areas are ungoverned or chaotic? | Styled polygons |

### 6.2 `climate.md`

| Question | KML Element |
|----------|-------------|
| What are the major climate zones? | Colored climate zone polygons |
| Which areas are uninhabitable? | Red/black hazard zones |
| Where are key resource deposits (water, arable land)? | Point placemarks |
| What are the agricultural zones? | Green polygon overlays |
| Which coastlines are lost to sea-level rise? | Blue encroachment polygons |
| Where are major weather event corridors? | Path/line features |

### 6.3 `technology.md`

| Question | KML Element |
|----------|-------------|
| What major energy infrastructure exists? | Point placemarks + lines for grids |
| Where are major AI/industrial hubs? | Point placemarks |
| What transportation corridors exist? | Line strings |
| What space infrastructure is relevant? | Point placemarks + orbits |
| What zones are under technological control (e.g., drone surveillance zones)? | Polygons |

### 6.4 `economy.md`

| Question | KML Element |
|----------|-------------|
| What are the major trade blocs? | Colored regional polygons |
| What are the key trade corridors (sea, land)? | Line strings |
| Where are resource extraction zones? | Point/polygon placemarks |
| What are the major financial centers? | Point placemarks |
| Which areas are economically collapsed/thriving? | Styled polygons |

### 6.5 `demographics.md`

| Question | KML Element |
|----------|-------------|
| Where are population centers? | Heatmap overlay or point density |
| What are the major migration routes? | Arrow path lines |
| What is the urbanization pattern? | Urban extent polygons |
| What areas are depopulated? | Styled polygons |
| Where are refugee/displaced populations concentrated? | Point/polygon placemarks |

### 6.6 `culture.md`

| Question | KML Element |
|----------|-------------|
| What ideological/religious zones exist? | Colored regional polygons |
| What are the dominant information ecosystems? | Regional polygons |
| Where are culture-producing centers? | Point placemarks |
| What zones have culture clash or conflict? | Hatched boundary zones |

---

## 7. KML Organization Strategy

### 7.1 Why Separate KML Files (Not KMZ)

| Concern | Separate KML files | Single monolithic KMZ |
|---------|-------------------|---------------------|
| **Git diff-ability** | Can diff individual polygon changes | Binary blob, no diff |
| **Edit modularity** | Edit one domain's geography without touching others | Must rebuild entire KMZ |
| **Parallel editing** | Could edit borders.kml and climate.kml simultaneously | Single-file bottleneck |
| **Lazy loading** | NetworkLinks load on demand (GE only fetches visible layers) | Whole file loads at once |
| **Cross-milestone comparison** | Can load 2050/borders.kml + 2075/borders.kml as separate layers | Harder to mix from same KMZ |

### 7.2 Style Strategy

Define a **color palette and style scheme** per domain, **consistent across milestones**:

| Domain | Base Color | Purpose |
|--------|-----------|---------|
| Borders | Entity-specific (e.g., blue for federations, red for collapsed states) | Sovereignty |
| Climate | Green→brown gradient (habitable→desert), blue (water), red (hazard) | Physical state |
| Technology | Yellow/orange | Infrastructure |
| Economy | Purple/magenta | Economic zones |
| Demographics | Gray/blue heat | Population |
| Culture | Teal/green | Ideological zones |

Use KML `<Style>` definitions at the top of each domain KML to keep styling consistent.

### 7.3 Reference Layer: Modern-Day Basemap

Optionally, each milestone's `doc.kml` can NetworkLink to the modern-day basemap as a semi-transparent reference, enabling visual diff in Google Earth:

```xml
<NetworkLink>
  <name>Modern-Day Borders (reference)</name>
  <visibility>0</visibility>  <!-- Off by default; user toggles -->
  <Link><href>../../../basemap/kml/modern-day-borders.kml</href></Link>
</NetworkLink>
```

### 7.4 Editing Workflow

1. Open milestone's `doc.kml` in Google Earth (loads all domain layers)
2. To edit a domain (e.g., draw new borders):
   - In Google Earth Places panel, right-click the NetworkLink → "Save Place As..." → save as KML
   - Edit the KML file directly, OR use Google Earth to modify the loaded features
   - Google Earth's "Save Place As..." on a NetworkLink destination overwrites the original `.kml` file
   - Verify the change with `git diff`

**Workflow note:** Google Earth edits loaded KML in memory. To persist edits, you must explicitly save. The cleanest workflow is:
- Load `doc.kml` in Google Earth
- Edit polygons in the 3D viewer
- Right-click the domain folder → "Save Place As..." → overwrite the domain's `.kml` file
- Commit changes via Git

---

## 8. Build Order & Dependencies

### 8.1 Critical Dependency Path

```
Basemap (exists)
    │
    ▼
Transition 2026-2050 ────► 2050 markdown ────► 2050 KML
                                      │
                                      ▼
                            Transition 2051-2075 ────► 2075 markdown ────► 2075 KML
                                                                 │
                                                                 ▼
                                                       Transition 2076-2100 ────► 2100 markdown ────► 2100 KML
```

Each milestone's markdown depends on the transition that precedes it (to know what *happened*). Each milestone's KML depends on its own markdown (to know what to *draw*). But there is a choice in whether to build milestones sequentially or in parallel at a high level.

### 8.2 Build Order Options

**Option A: Sequential (Recommended for this project)**

| Phase | Builds | Depends On |
|-------|--------|------------|
| 1 | Transition 2026-2050 | Basemap |
| 2 | 2050 domains (6 files) | Transition 2026-2050 |
| 3 | 2050 KML layers (7 files) | 2050 domains |
| 4 | Transition 2051-2075 | 2050 domains |
| 5 | 2075 domains (6 files) | Transition 2051-2075 |
| 6 | 2075 KML layers (7 files) | 2075 domains |
| 7 | Transition 2076-2100 | 2075 domains |
| 8 | 2100 domains (6 files) | Transition 2076-2100 |
| 9 | 2100 KML layers (7 files) | 2100 domains |
| 10 | Master index + BASEMAP_README | All of the above |

**Rationale for sequential:** Since the project has a strong central thesis (US collapse → socialist transition), each milestone builds causally on the previous one. Writing 2050 first establishes the collapse trajectory. 2075 extends the resulting system. 2100 resolves it. This avoids the cognitive overhead of tracking multiple parallel timelines.

**Option B: Top-down arc first, then fill**

| Phase | Builds |
|-------|--------|
| 1 | All three transitions (sketch) |
| 2 | All three milestone indices (sketch) |
| 3 | 2050 full detail → 2075 → 2100 |

**Why not recommend this:** The project is solo. There's no collaboration benefit to having all milestones sketched simultaneously. And detailed work on 2050 will reveal implications that change the 2075 plan — better to let each milestone inform the next.

### 8.3 Per-Domain Build Order Within a Milestone

Within a single milestone, domains should be written in dependency order:

```
borders-geopolitics (primary: sets territorial framework)
    │
    ├──► climate (depends on knowing which polities control which geography)
    ├──► technology (depends on knowing which polities invest in what)
    │
    ▼
economy (depends on borders + technology + climate)
    │
    ├──► demographics (depends on economy + climate + borders)
    │
    ▼
culture (depends on all of the above)
```

**Recommended writing order within one milestone:**
1. `borders-geopolitics.md` (the foundational layer)
2. `climate.md` (physical constraints)
3. `technology.md` (capabilities)
4. `economy.md` (flows & resources)
5. `demographics.md` (human distribution)
6. `culture.md` (emergent ideology — sits on top of everything)

The corresponding KML files follow the same order (draw borders first, add layers on top).

### 8.4 File Count Summary

| Phase | Files Created | Total Project Files |
|-------|--------------|-------------------|
| Basemap | 1 (README) + existing KML | 2 |
| Transition 2026-2050 | 1 | 3 |
| 2050 domains | 7 (index + 6 domains) | 10 |
| 2050 KML | 7 (doc + 6 domain layers) | 17 |
| Transition 2051-2075 | 1 | 18 |
| 2075 domains | 7 | 25 |
| 2075 KML | 7 | 32 |
| Transition 2076-2100 | 1 | 33 |
| 2100 domains | 7 | 40 |
| 2100 KML | 7 | 47 |
| Master index | 1 | 48 |

**Total: ~48 files**, not including any reference materials. Each milestone is 14 files (1 index + 6 domain MD + 1 doc.kml + 6 domain KML).

---

## 9. Consistency Mechanisms

### 9.1 Automatic Consistency Checks (Manual, No Tooling)

Since this is a solo markdown+Git project (no app code), consistency is maintained by:

1. **KML count audit:** For any entity in `borders-geopolitics.md` with a `→ See KML:` marker, verify the named placemark exists in the corresponding KML file.
2. **Reverse KML audit:** For any non-trivial polygon in a KML file, verify the `See:` back-reference in its description resolves to a real section in the corresponding markdown.
3. **Transition → snapshot audit:** Every `→ Result:` reference in a transition doc must link to a real file and section.
4. **Style consistency:** Spot-check that like entities use the same KML `<Style>` across milestones (e.g., "North American Federation" in 2050 uses the same color as in 2075).

### 9.2 Cross-Domain Consistency

Each domain file's "Interactions With Other Domains" section explicitly calls out dependencies. The project index can serve as a consistency map:

```markdown
## Cross-Domain Consistency Map

| Claim | Appears In | Also Affects | Status |
|-------|-----------|--------------|--------|
| North American Federation formed 2045 | 2050/borders.md | 2050/economy.md (single market), 2050/culture.md (new identity) | ✓ |
| Great Lakes desiccated by 2070 | 2075/climate.md | 2075/borders.md (new US-Canada water boundary), 2075/economy.md (loss of shipping) | ? |
```

### 9.3 Version Control Strategy

| File Type | Git Tracking | Notes |
|-----------|-------------|-------|
| `.md` files | Track normally | All markdown is plain text, easily diffed |
| `.kml` files | Track normally | KML is XML, Git-diffable |
| `.kmz` files | Track via Git LFS | Binary, only if exported for distribution |
| Generated exports | `.gitignore` | Any auto-generated PDFs, etc. |

`.gitignore` should include:
```
# Generated/binary files
*.kmz
.DS_Store
```

---

## 10. Information Architecture Diagram

```
                                       ┌─────────────────────────────┐
                                       │         index.md           │
                                       │  (project entry point)     │
                                       └──────┬──────────┬──────────┘
                                              │          │
                    ┌─────────────────────────┘          └─────────────┐
                    ▼                                                    ▼
        ┌───────────────────┐                              ┌──────────────────────┐
        │  BASEMAP_README   │                              │  2050/index.md       │
        │  (documents KML)  │                              │  (snapshot summary)  │
        └───────────────────┘                              └──────────┬───────────┘
                                                                     │
                                                                     ▼
        ┌───────────────────┐                              ┌──────────────────────┐
        │  2026-2050.md     │◄─────provides arc─────►      │  domains/            │
        │  (transition)     │                              │  ├── borders-geopol  │
        └───────────────────┘                              │  ├── climate         │
                                                           │  ├── technology      │
        ┌───────────────────┐                              │  ├── economy         │
        │  2051-2075.md     │◄─────provides arc─────►      │  ├── demographics    │
        │  (transition)     │                              │  └── culture         │
        └───────────────────┘                              └──────────┬───────────┘
                                                                     │
        ┌───────────────────┐                              ┌──────────▼───────────┐
        │  2076-2100.md     │◄─────provides arc─────►      │  2050/kml/           │
        │  (transition)     │                              │  ├── doc.kml (root)  │
        └───────────────────┘                              │  ├── borders.kml     │
                                                           │  ├── climate.kml     │
                                                           │  ├── technology.kml  │
                                                           │  ├── economy.kml     │
                                                           │  ├── demographics.kml│
                                                           │  └── culture.kml     │
                                                           └──────────────────────┘

                                                                    │
                                                            (same structure for
                                                             2075/ and 2100/)

LEGEND:
────►  "references" or "depends on"
~~~~►  "links to"
```

### Information Flow Direction

```
Transition (drivers) ──► Snapshot Markdown (state) ──► KML (geography)
     causal logic            domain descriptions           polygons
     [why]                   [what]                        [where]
```

Each layer adds specificity. The transition says "the US collapsed." The markdown says "the North American Federation formed, comprising the former US, Canada, and Mexico, with these specific borders." The KML draws the exact polygon.

---

## 11. Scalability Considerations

| Concern | Current Scale (48 files, 3 milestones) | If Extended to N Milestones |
|---------|---------------------------------------|-----------------------------|
| Directory depth | 3 levels max (e.g., `2050/domains/borders.md`) | Same 3-level structure per milestone — flat scaling |
| KML loading | ~6 domain KMLs per milestone via NetworkLinks | One `doc.kml` per milestone; Google Earth handles 20+ NetworkLinks easily |
| Cross-references | Manual text markers | Would need tooling at 10+ milestones |
| File naming | Convention-based | Convention holds; milestones are keyed by year so adding 2030 or 2125 slots in naturally |
| Git repo size | Small (text files, ~100KB) | Still small unless KML files contain massive polygonal data (>50K points each). If so, simplify geometry in QGIS. |

---

## 12. Sources & References

| Source | What It Informed | Confidence |
|--------|-----------------|------------|
| [Google KML Tutorial - Network Links](https://developers.google.com/kml/documentation/kml_tut) | Multi-file KML architecture via NetworkLinks with local relative paths | HIGH — official Google documentation |
| [Google KMZ Files Documentation](https://developers.google.com/kml/documentation/kmzarchives) | Rationale for keeping KML flat over KMZ for Git-diffability | HIGH — official format doc |
| [StackOverflow: Building Large KML Files](https://stackoverflow.com/questions/7435196/building-large-kml-file) | NetworkLink + Folder patterns for organizing KML layers | MEDIUM — confirmed by official docs |
| [FEMA Strategic Foresight 2050 Report](https://www.fema.gov/emergency-managers/practitioners/strategic-foresight) | STEEP framework, scenario planning, domain segmentation model | HIGH — US government foresight methodology |
| [UK Government Futures Toolkit](https://www.gov.uk/government/publications/futures-toolkit-for-policy-makers-and-analysts/the-futures-toolkit-html) | PESTLE/STEEP domain categories, driver mapping methodology | HIGH — UK government toolkit |
| [OECD Global Scenarios 2035](https://www.oecd.org/content/dam/oecd/en/publications/reports/2021/05/global-scenarios-2035_72de6a64/df7ebc33-en.pdf) | Scenario + transition document relationship patterns | MEDIUM — established foresight practice |
| [RAND: Coast Guard Evergreen Scenarios](https://www.rand.org/content/dam/rand/pubs/research_reports/RR3100/RR3147/RAND_RR3147.pdf) | Scenario families, stressors-and-shocks framework | HIGH — RAND methodology |
| [Journal of Futures Studies: Transition Scenarios via Backcasting](https://jfsdigital.org/articles-and-essays/vol-24-no-1-september-2019/transition-scenarios-via-backcasting/) | Backcasting from future milestones, midway points, driver state tables | MEDIUM — academic literature |
| [USA Foresight Guide: STEEP to STEEPS](http://www.foresightguide.com/horizon-scanning-frameworks/) | Domain taxonomy rationale (S+T+E+E+P(+S/D) variants) | MEDIUM — practitioner blog, corroborated by UK toolkit |
| [Geopol-Forecaster project (danielrosehill)](https://github.com/danielrosehill/Geopol-Forecaster) | SITREP-first document architecture, structured output per lens, numbered file conventions | MEDIUM — open-source project, mirrors some patterns |
| [Aerotas KML Workflow Guide](https://aerotas.com/resources/working-with-aerotas/creating-a-kml-kmz-with-google-earth/) | Google Earth Pro polygon creation and save workflow | HIGH — operational guide |

---

## 13. Open Questions / Phase-Level Research Needs

| Question | Relevant Phase | Why It's Not Resolved Here |
|----------|---------------|---------------------------|
| Should KML styles be defined inline per-file or in a shared library file? | Phase 1 (basemap + 2050) | Need to decide after seeing how much style reuse occurs |
| Does the Google Earth NetworkLink refresh behavior work reliably with local relative paths on macOS? | Phase 1 (2050 KML) | Platform-specific; needs testing; falls back to opening individual domain KMLs manually |
| Should KML reference polygons from the basemap be copied into each milestone (practical) or NetworkLinked (consistent)? | Phase 1 (2050 KML) | Tradeoff between self-contained milestones vs. single source of truth |
| Is there enough cross-domain coupling to warrant a formal dependency matrix beyond the "Interactions" section? | After Phase 2 (2075) | Need to see how complex the coupling actually gets |
| Should domain files within a milestone reference each other with `→ Cross-ref:` markers for internal consistency? | Phase 2 (2050 domains) | Design decision; currently implicit in "Interactions" sections but could be more explicit |
