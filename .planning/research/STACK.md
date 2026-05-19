# Technology Stack

**Project:** Future Prediction (Geopolitical Forecasting & World-Building)
**Researched:** 2026-05-19

## Recommended Stack

### Layer 1: Knowledge Management (Primary Authoring Environment)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Obsidian** | Latest stable | Interconnected markdown knowledge base | Only tool that combines markdown-native files, bidirectional linking, graph view, Canvas, and a mature plugin ecosystem — all offline, all local, no lock-in. Files are plain `.md` on disk. |
| **Git** | Any modern | Version control across milestone snapshots | The entire Obsidian vault is a directory of text files — git tracks every change across all 6 domains for all 3 milestones. Enables diffing scenario changes, rolling back, and branching "what-if" futures. |
| **Python 3.12+** | Latest stable | Scripting, data transformation, KML generation | Bridges the markdown knowledge base to the map output. Reads structured YAML frontmatter from Obsidian notes, generates KML files programmatically. |

### Layer 2: Map / KML Toolchain

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **simplekml** (Python package) | 1.3.6+ | Programmatic KML generation | The only actively maintained Python library purpose-built for easy KML creation. Supports all geometry types (Polygon, LineString, Point), shared styles, folders, color coding — everything needed for world maps. Avoids hand-writing error-prone XML. |
| **Google Earth Pro** | Desktop app | KML visualization, manual editing, final assembly | You already have the modern-day basemap here. It is the de facto standard for viewing KML with full 3D globe rendering, polygon styling, folder hierarchy, and time slider. Use for QA, touch-up, and final export. |
| **QGIS** | 3.40+ (optional) | Complex GIS operations if needed | Only reach for this if you need to reproject, merge shapefiles, validate polygon topology, or do spatial analysis that Google Earth can't handle. The KML Tools plugin (3.2.4) handles fast KML import/export. For this project's scope, likely unnecessary — keep in reserve. |

### Layer 3: Methodological Frameworks

| Framework | Source / Proponent | Why |
|-----------|-------------------|-----|
| **2×2 Scenario Matrix** | Royal Dutch Shell / GBN (legacy), Futures Platform, UNDP Foresight | The gold standard for geopolitical scenario planning. Identify two critical uncertainties (high impact, high uncertainty), place on axes, generate 4 contrasting futures per domain/year. Simple enough for a solo practitioner, rigorous enough for professional foresight. |
| **STEEP / Six Domains** | Multiple (Stanford Research Institute, The Futures School) | Your existing 6 domains (borders/geopolitics, climate, technology, economy, demographics, culture) map perfectly to a structured STEEP variant. Apply the 2×2 matrix independently per domain, then cross-domain consistency check. |
| **Three Horizons** | Bill Sharpe, International Futures Forum | The bridge framework. Horizon 1 = present dominant system (declining). Horizon 3 = emerging future (growing). Horizon 2 = transitional zone. Directly maps to your "trends between milestones" transition documents — explains *how* we get from 2050 → 2075 → 2100. |
| **Backcasting** | John Robinson, multiple | Start from the milestone endpoint (e.g., 2075 geopolitical map) and work backward to identify what must happen in each domain. Keeps the vision coherent. Use for each milestone after initial forward projection. |

### Supporting Libraries (Python)

| Library | Purpose | When to Use |
|---------|---------|-------------|
| **PyYAML** | Parse YAML frontmatter from Obsidian markdown files | Every time you read scenario data from `.md` files to generate KML |
| **shapely** | Validate polygon geometry before KML export | Boundary sanity checks — ensure country polygons don't self-intersect, have correct winding order, etc. |
| **pandas** | Structured data manipulation | If you have tabular scenario data (demographic projections, GDP trajectories, climate model outputs) that feed into boundary decisions |

---

## Alternatives Considered

| Category | Recommended | Alternative(s) | Why Not |
|----------|-------------|----------------|---------|
| Knowledge base | Obsidian | Notion, Roam Research, Logseq, Foam | **Notion**: cloud-only, proprietary format, no offline graph view. **Roam**: subscription, proprietary, marks you as dependent on a startup. **Logseq**: close second (open source, markdown), but Obsidian's Canvas and plugin maturity are decisive for visual scenario mapping. **Foam (VS Code)**: too bare-bones, no graph view worth using. |
| KML generation | simplekml (Python) | pyKML, GDAL/OGR, hand-written XML | **pyKML**: unmaintained (last release 2014), Python 2 era. **GDAL/OGR**: overkill for writing KML from structured data — it is a swiss-army knife for GIS conversions, not a friendly KML authoring library. **Hand-written XML**: error-prone, no validation, no style helpers. simplekml is the right abstraction. |
| Map workflow | Google Earth Pro | Mapbox, CesiumJS, Kepler.gl | Those are web-native visualization tools. This project outputs KML files, not interactive web maps. Google Earth Pro is the intended consumer. Adding a web map layer is scope creep. |
| Scenario method | 2×2 Matrix + 3 Horizons | Delphi Method, Cross-Impact Analysis, System Dynamics, Agent-Based Modeling | **Delphi**: requires expert panels — solo project. **Cross-Impact**: requires probability matrices that create false precision at 50-75 year horizons. **System Dynamics / ABM**: massive overengineering for a structured writing project. The 2×2 matrix gives you rigor without simulation complexity. |

---

## Installation

### Required

```bash
# Core knowledge base tool
# Download from https://obsidian.md — no package manager needed

# Python environment
brew install python@3.12  # macOS

pip install simplekml PyYAML

# Git (likely already installed)
git --version  # verify
```

### Optional (reserve tools)

```bash
pip install shapely pandas

# QGIS: Download from https://qgis.org — standalone installer
```

---

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT                            │
│                                                             │
│  milestone-2050/     milestone-2075/     milestone-2100/    │
│  ├── geopolitics.md   ├── geopolitics.md   ├── geopolitics.md│
│  ├── climate.md       ├── climate.md       ├── climate.md   │
│  ├── technology.md    ├── technology.md    ├── technology.md│
│  ├── economy.md       ├── economy.md       ├── economy.md   │
│  ├── demographics.md  ├── demographics.md  ├── demographics.md│
│  └── culture.md       └── culture.md       └── culture.md  │
│                                                             │
│  transitions/                                               │
│  ├── 2050-to-2075.md                                        │
│  └── 2075-to-2100.md                                        │
│                                                             │
│  YAML frontmatter in each .md file contains:                │
│  ---                                                        │
│  milestone: 2050                                            │
│  domain: geopolitics                                        │
│  borders: [list of changed boundaries]                      │
│  tags: [scenario-tag, region-tag]                           │
│  ---                                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Python script reads frontmatter
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                GENERATE_KML.PY                               │
│                                                             │
│  1. Parse YAML frontmatter from all milestone-2050/*.md     │
│  2. Map scenario boundary changes to polygon operations     │
│  3. Generate milestone-2050.kml with:                       │
│     - Polygons for each recognized polity                   │
│     - Folder hierarchy by region / domain                   │
│     - Color coding by alliance, stability, etc.            │
│     - Styled placemarks with scenario description balloons  │
│  4. Output: .planning/maps/milestone-2050.kml              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                QA IN GOOGLE EARTH PRO                        │
│                                                             │
│  - Load generated KML                                       │
│  - Visual check: polygon alignment, borders, labels         │
│  - Manual touch-up for edge cases                           │
│  - Export final version to milestone-2050.kmz               │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Rationales

**Why Obsidian over all alternatives:** This project produces markdown files, period. Obsidian is the best *markdown reading/writing environment* that also offers graph visualization, Canvas for spatial layout of scenarios, Dataview for querying notes by YAML frontmatter, and works fully offline with files you control. Every other note tool either locks you into a format (Notion, Roam) or lacks the rich linking and querying (VS Code + Foam, plain text editor).

**Why simplekml over raw XML or GDAL:** KML is XML. You *can* write it with string templates. You *shouldn't*, because at map scale with dozens of polygons, styled folders, and description balloons, malformed XML will silently break your maps. simplekml gives you a clean Python API, validates structure, and handles the shared-style optimization that keeps file sizes manageable. GDAL's KML driver is designed for format conversion pipelines, not authoring.

**Why the 2×2 matrix over more complex methods:** This is a solo project, not a think tank. The 2×2 matrix forces you to identify the two MOST IMPORTANT uncertainties per domain and commit to a position. It prevents the "everything is uncertain" paralysis. At 50-75 year horizons, detailed probabilistic forecasts are theater anyway — what matters is internal consistency and narrative plausibility. The 2×2 matrix gives you that without false precision.

**Why Three Horizons for transition docs:** Your transition documents connect the milestones. The Three Horizons framework gives you a vocabulary for describing the decline of the old order (H1), the experiments and turbulence of transition (H2), and the emergence of the new order (H3). This is exactly what you need for "how the world transforms between 2050 and 2075."

---

## What NOT to Use

| Tool | Why Not |
|------|---------|
| **Notion** | Cloud dependency, proprietary format, no offline graph view, slow with large databases, exports to broken markdown. Poison for a 50-year project. |
| **Roam Research** | $30/mo subscription, proprietary, startup risk. Your notes should outlive any company. |
| **CesiumJS / Mapbox** | Web-native map frameworks. They require servers, API keys, and JavaScript. This is a KML project. Google Earth Pro already does everything needed. |
| **AI forecasting tools (MyndField, etc.)** | Simulation engines that produce probability distributions. They operate at short timescales (months to a few years) and require live data feeds. At 50+ year horizons their outputs are meaningless — and they do not produce editable markdown or KML. |
| **Spreadsheet-based scenario planning** | Excel/Google Sheets tempts you to quantify the unquantifiable. 50-year forecasts should be narrative and structured, not pseudo-quantitative. Obsidian markdown keeps the emphasis on your reasoning, not false precision. |
| **Jupyter Notebooks** | Overkill for a project whose primary artifact is markdown text. Python scripts for KML generation are fine as standalone `.py` files. Notebooks add complexity and a dependency on the Jupyter runtime for no benefit. |

---

## Sources

- **Obsidian**: https://obsidian.md — official site; tested personally
- **simplekml**: https://simplekml.readthedocs.io/en/latest/ — documentation v1.3.6
- **simplekml PyPI**: https://pypi.org/project/simplekml/ — confirmed latest release Sep 2021, stable, production-grade
- **Google Earth Pro**: https://earth.google.com — desktop application
- **QGIS KML Tools plugin**: https://plugins.qgis.org/plugins/kmltools/ — v3.2.4 released 2026-03-12
- **2×2 Scenario Matrix**: UNDP Foresight Toolkit (https://www.undp.org/future-development/chapter-2-identifying-development-challenges/creative-approach-creative-approach-overview/creative-approach-2x2-scenarios) and Futures Platform (https://www.futuresplatform.com/blog/2x2-scenario-planning-matrix-guideline)
- **Three Horizons**: Bill Sharpe, International Futures Forum (https://www.insightandforesight.com.au/)
- **STEEP Framework**: Stanford Research Institute, The Futures School
- **Dataview plugin**: https://blacksmithgu.github.io/obsidian-dataview/ — 4.1M+ downloads, 8.9K GitHub stars
- **Extended Graph plugin**: https://github.com/ElsaTam/obsidian-extended-graph — 50K+ downloads, adds node shapes/images/stats to graph view
- **Backcasting methodology**: John Robinson, "Future subjunctive: backcasting as social learning" (2003), *Futures* 35(8)
