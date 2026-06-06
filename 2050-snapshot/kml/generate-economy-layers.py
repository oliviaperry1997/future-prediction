#!/usr/bin/env python3
"""
Generate economy.kml with 4 data-driven overlay layers for 2050:
1. Cities & Megalopolises — point placemarks + UMS β=81 megalopolis polygons
2. Production Metric (BCU-equivalent) — entity GDP fills converted to BCU
3. Transit & Logistics — corridors, HSR, spaceports, ports
4. Production Sectors — entity dominant sector classification

Replaces the 8 rough bounding boxes in existing economy.kml.
Output: 2050-snapshot/kml/economy.kml
"""

import logging
import os
import re
import sys
import zipfile
import io
from collections import defaultdict
from math import radians, cos, sin, asin, sqrt

import numpy as np
import requests
import shapely.geometry as geom
import shapely.ops
import simplekml
from lxml import etree
from shapely.geometry import Point, Polygon, MultiPolygon, shape
from shapely.ops import unary_union

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KML_DIR = SCRIPT_DIR
DOMAINS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "../domains"))
ECONOMY_MD = os.path.join(DOMAINS_DIR, "economy.md")
BORDERS_KML = os.path.join(KML_DIR, "borders.kml")
OUTPUT_KML = os.path.join(KML_DIR, "economy.kml")
SOURCE_DIR = os.path.join(KML_DIR, "source")
NE_PLACES_ZIP = os.path.join(SOURCE_DIR, "ne_10m_populated_places_simple.zip")

NS = "http://www.opengis.net/kml/2.2"

# --- BCU Conversion ---
# Narrative GDP estimates are in "dollars" but dollar hegemony is dead by 2050.
# BCU (BRICS+ Digital Basket Currency) is the international settlement standard.
# Based on BCU basket composition (yuan 30%, euro 20%, BCU 20%, gold 15%):
# 1 BCU ≈ 1.4 USD in real purchasing power (dollar depreciated ~30% post-hegemony)
BCU_PER_USD = 0.7  # 1 USD ≈ 0.7 BCU

# Production tiers in BCU
BCU_TIERS = [
    (5000, "Major Power", "#1a237e", "ff1a237e"),
    (1000, "Major Economy", "#283593", "ff283593"),
    (200, "Intermediate Economy", "#1565c0", "ff1565c0"),
    (20, "Small Economy", "#42a5f5", "ff42a5f5"),
    (0, "Micro Economy", "#bbdefb", "ffbbdefb"),
]

# Sector categories and colors
SECTOR_CATEGORIES = {
    "technology": ("Technology & Finance", "#d32f2f", "ffd32f2f"),
    "finance": ("Technology & Finance", "#d32f2f", "ffd32f2f"),
    "tech": ("Technology & Finance", "#d32f2f", "ffd32f2f"),
    "manufacturing": ("Advanced Manufacturing", "#f57c00", "fff57c00"),
    "manufactur": ("Advanced Manufacturing", "#f57c00", "fff57c00"),
    "automotive": ("Advanced Manufacturing", "#f57c00", "fff57c00"),
    "aerospace": ("Advanced Manufacturing", "#f57c00", "fff57c00"),
    "energy": ("Energy & Extraction", "#388e3c", "ff388e3c"),
    "extraction": ("Energy & Extraction", "#388e3c", "ff388e3c"),
    "mining": ("Energy & Extraction", "#388e3c", "ff388e3c"),
    "oil": ("Energy & Extraction", "#388e3c", "ff388e3c"),
    "gas": ("Energy & Extraction", "#388e3c", "ff388e3c"),
    "renewable": ("Energy & Extraction", "#2e7d32", "ff2e7d32"),
    "hydro": ("Energy & Extraction", "#2e7d32", "ff2e7d32"),
    "agriculture": ("Agriculture & Food", "#ff8f00", "ffff8f00"),
    "agricultur": ("Agriculture & Food", "#ff8f00", "ffff8f00"),
    "agri": ("Agriculture & Food", "#ff8f00", "ffff8f00"),
    "food": ("Agriculture & Food", "#ff8f00", "ffff8f00"),
    "tourism": ("Services & Tourism", "#7b1fa2", "ff7b1fa2"),
    "tourism": ("Services & Tourism", "#7b1fa2", "ff7b1fa2"),
    "services": ("Services & Tourism", "#7b1fa2", "ff7b1fa2"),
    "hospitality": ("Services & Tourism", "#7b1fa2", "ff7b1fa2"),
    "retail": ("Services & Tourism", "#7b1fa2", "ff7b1fa2"),
    "mixed": ("Mixed/Diversified", "#616161", "ff616161"),
    "diversified": ("Mixed/Diversified", "#616161", "ff616161"),
}

DEFAULT_SECTOR = ("Mixed/Diversified", "#616161", "ff616161")


# ============================================================
# STEP 1: Parse economy.md entity profiles
# ============================================================

def parse_economy_md():
    """Extract entity economic data from economy.md.
    Returns dict: entity_name -> {gdp_str, sectors_str, model_str, bloc_str, tier}
    """
    if not os.path.exists(ECONOMY_MD):
        log.error(f"economy.md not found: {ECONOMY_MD}")
        return {}

    with open(ECONOMY_MD) as f:
        text = f.read()

    entities = {}
    sections = re.split(r'^### ', text, flags=re.MULTILINE)
    for sec in sections:
        if 'Economic Profiles' not in sec[:60]:
            continue
        blocks = re.split(r'(?=^\*\*[A-Z][^*]+:\*\*$)', sec, flags=re.MULTILINE)
        for block in blocks:
            m = re.match(r'^\*\*([^*]+):\*\*', block)
            if not m:
                continue
            name = m.group(1).strip()
            gdp_m = re.search(r'- \*\*GDP:\*\* (.+)', block)
            sector_m = re.search(r'- \*\*Dominant sectors:\*\* (.+)', block)
            model_m = re.search(r'- \*\*Economic model:\*\* (.+)', block)
            bloc_m = re.search(r'- \*\*Trade partners and bloc alignment:\*\* (.+)', block)
            gdp_str = gdp_m.group(1).strip() if gdp_m else ""
            entities[name] = {
                "gdp_str": gdp_str,
                "sectors_str": sector_m.group(1).strip() if sector_m else "",
                "model_str": model_m.group(1).strip() if model_m else "",
                "bloc_str": bloc_m.group(1).strip() if bloc_m else "",
            }
    log.info(f"Parsed {len(entities)} entity profiles from economy.md")
    return entities


def parse_gdp_to_bcu(gdp_str):
    """Convert narrative GDP string to BCU-equivalent value in billions."""
    if not gdp_str:
        return None
    gdp_str = gdp_str.replace("~", "").replace(",", "").strip()
    # Handle $XXXB placeholders
    if "XXX" in gdp_str:
        return None
    # Extract number
    m = re.search(r'[\$]?([\d.]+)\s*([TtBbMm])', gdp_str)
    if not m:
        return None
    val = float(m.group(1))
    unit = m.group(2).upper()
    if unit == "T":
        val *= 1000
    elif unit == "M":
        val /= 1000
    return val * BCU_PER_USD


def classify_bcu_tier(bcu_billions):
    """Classify BCU value into production tier."""
    if bcu_billions is None:
        return BCU_TIERS[-1][1], BCU_TIERS[-1][2], BCU_TIERS[-1][3]  # Unknown -> micro
    for threshold, label, color, kml_color in BCU_TIERS:
        if bcu_billions >= threshold:
            return (label, color, kml_color)
    return BCU_TIERS[-1][1], BCU_TIERS[-1][2], BCU_TIERS[-1][3]


def classify_sector(sectors_str):
    """Classify entity by dominant sector."""
    if not sectors_str:
        return DEFAULT_SECTOR
    sectors_lower = sectors_str.lower()
    scores = defaultdict(int)
    for keyword, (cat, color, kml_color) in SECTOR_CATEGORIES.items():
        if keyword in sectors_lower:
            scores[cat] += 1
    if not scores:
        return DEFAULT_SECTOR
    best_cat = max(scores, key=scores.get)
    for keyword, (cat, color, kml_color) in SECTOR_CATEGORIES.items():
        if cat == best_cat:
            return (cat, color, kml_color)
    return DEFAULT_SECTOR


# ============================================================
# STEP 2: Extract entity polygons from borders.kml
# ============================================================

def parse_kml_coords(coord_text):
    """Parse KML coordinates text into list of (lon, lat) tuples."""
    coords = []
    for line in coord_text.strip().split():
        parts = line.strip().split(",")
        if len(parts) >= 2:
            try:
                coords.append((float(parts[0]), float(parts[1])))
            except ValueError:
                pass
    return coords


def extract_entity_polygons():
    """Extract polygon geometries from borders.kml by entity name.
    Returns dict: entity_name -> list of coordinate strings (for simplekml)
    """
    if not os.path.exists(BORDERS_KML):
        log.error(f"borders.kml not found: {BORDERS_KML}")
        return {}

    tree = etree.parse(BORDERS_KML)
    root = tree.getroot()
    nsmap = {"kml": NS}

    entity_polys = {}
    folders = root.findall(f".//{{{NS}}}Folder")
    for folder in folders:
        folder_name_el = folder.find(f"{{{NS}}}name")
        if folder_name_el is None:
            continue
        placemarks = folder.findall(f".//{{{NS}}}Placemark")
        for pm in placemarks:
            name_el = pm.find(f"{{{NS}}}name")
            if name_el is None:
                continue
            entity_name = name_el.text.strip()

            coords_list = []
            for poly_el in pm.findall(f".//{{{NS}}}Polygon"):
                outer = poly_el.find(f".//{{{NS}}}outerBoundaryIs/{{{NS}}}LinearRing/{{{NS}}}coordinates")
                if outer is not None and outer.text:
                    coords_list.append(outer.text.strip())
            if not coords_list:
                for mg in pm.findall(f".//{{{NS}}}MultiGeometry/{{{NS}}}Polygon"):
                    outer = mg.find(f".//{{{NS}}}outerBoundaryIs/{{{NS}}}LinearRing/{{{NS}}}coordinates")
                    if outer is not None and outer.text:
                        coords_list.append(outer.text.strip())

            if coords_list:
                entity_polys[entity_name] = coords_list

    log.info(f"Extracted {len(entity_polys)} entity polygons from borders.kml")
    return entity_polys


# ============================================================
# STEP 3: Download & process NE populated places
# ============================================================

NE_PLACES_URL = (
    "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/"
    "10m/cultural/ne_10m_populated_places_simple.zip"
)

# Fallback major cities if NE download fails
FALLBACK_CITIES = [
    ("Tokyo", 35.7, 139.7, 37400000),
    ("Shanghai", 31.2, 121.5, 26300000),
    ("Beijing", 39.9, 116.4, 21700000),
    ("Delhi", 28.6, 77.2, 29300000),
    ("Mumbai", 19.1, 72.9, 20600000),
    ("São Paulo", -23.5, -46.6, 22000000),
    ("Mexico City", 19.4, -99.1, 21700000),
    ("Cairo", 30.0, 31.2, 20400000),
    ("Dhaka", 23.8, 90.4, 20200000),
    ("Osaka", 34.7, 135.5, 19200000),
    ("Karachi", 24.9, 67.0, 16000000),
    ("Buenos Aires", -34.6, -58.4, 15200000),
    ("Kolkata", 22.6, 88.4, 14800000),
    ("Lagos", 6.5, 3.4, 14400000),
    ("Guangzhou", 23.1, 113.3, 13800000),
    ("Manila", 14.6, 121.0, 13500000),
    ("Jakarta", -6.2, 106.8, 13500000),
    ("Shenzhen", 22.5, 114.1, 12500000),
    ("Seoul", 37.6, 127.0, 12000000),
    ("Los Angeles", 34.1, -118.2, 12400000),
    ("New York", 40.7, -74.0, 18800000),
    ("London", 51.5, -0.1, 9500000),
    ("Paris", 48.9, 2.3, 11000000),
    ("Berlin", 52.5, 13.4, 6000000),
    ("Istanbul", 41.0, 28.9, 15500000),
    ("Moscow", 55.8, 37.6, 12500000),
    ("Bangkok", 13.8, 100.5, 10500000),
    ("Ho Chi Minh City", 10.8, 106.7, 8900000),
    ("Tehran", 35.7, 51.4, 9400000),
    ("Riyadh", 24.7, 46.7, 7700000),
    ("Baghdad", 33.3, 44.4, 6800000),
    ("Kinshasa", -4.3, 15.3, 13400000),
    ("Lima", -12.0, -77.0, 10400000),
    ("Bogotá", 4.7, -74.1, 10800000),
    ("Santiago", -33.4, -70.6, 6700000),
    ("Toronto", 43.7, -79.4, 6300000),
    ("Chicago", 41.9, -87.6, 8700000),
    ("Houston", 29.8, -95.4, 6300000),
    ("Atlanta", 33.7, -84.4, 5800000),
    ("Miami", 25.8, -80.2, 6100000),
    ("San Francisco", 37.8, -122.4, 4700000),
    ("Seattle", 47.6, -122.3, 4000000),
    ("Denver", 39.7, -105.0, 2900000),
    ("Sydney", -33.9, 151.2, 5300000),
    ("Melbourne", -37.8, 144.9, 5000000),
    ("Nairobi", -1.3, 36.8, 5500000),
    ("Cape Town", -33.9, 18.4, 4600000),
    ("Johannesburg", -26.2, 28.0, 5800000),
    ("Lahore", 31.5, 74.3, 12500000),
    ("Bangalore", 12.9, 77.6, 12600000),
    ("Chennai", 13.1, 80.3, 10600000),
    ("Hyderabad", 17.4, 78.5, 9700000),
    ("Ahmedabad", 23.0, 72.6, 8100000),
    ("Kuala Lumpur", 3.1, 101.7, 8200000),
    ("Singapore", 1.3, 103.8, 5900000),
    ("Hong Kong", 22.3, 114.2, 7500000),
    ("Taipei", 25.0, 121.5, 6800000),
    ("Dubai", 25.2, 55.3, 4300000),
]


def load_city_data():
    """Load city data from NE populated places or fallback.
    Returns list of (name, lat, lon, pop) for cities with pop > 200K.
    """
    # Try NE data first
    if os.path.exists(NE_PLACES_ZIP):
        cities = []
        try:
            with zipfile.ZipFile(NE_PLACES_ZIP) as z:
                shp_files = [n for n in z.namelist() if n.endswith(".shp")]
                if shp_files:
                    import fiona
                    import tempfile
                    with tempfile.TemporaryDirectory() as tmpdir:
                        z.extractall(tmpdir)
                        shp_path = os.path.join(tmpdir, shp_files[0])
                        with fiona.open(shp_path) as src:
                            for feat in src:
                                props = feat["properties"]
                                pop = props.get("POP_MAX", 0) or props.get("POP_OTHER", 0) or 0
                                if pop < 200000:
                                    continue
                                name = props.get("NAME", "")
                                lat = props.get("LATITUDE", 0)
                                lon = props.get("LONGITUDE", 0)
                                if name and lat and lon:
                                    cities.append((name, lat, lon, pop))
            log.info(f"Loaded {len(cities)} cities from NE data")
            return cities
        except Exception as e:
            log.warning(f"Error loading NE data: {e}")

    # Fallback to hardcoded cities
    log.info(f"Using fallback city list ({len(FALLBACK_CITIES)} cities)")
    return list(FALLBACK_CITIES)


def compute_megalopolis_polygons(cities):
    """Compute megalopolis polygons using UMS β=81 approach.
    
    UMS formula: F = A - R where A=1/(1+d), R=1/(β+d/2), β=81
    Equilibrium at d=160km for β=81.
    
    Simplified grid-based implementation:
    1. Create coarse grid over populated land areas
    2. Compute UMS net force from all nearby cities
    3. Threshold to find megalopolis-class cells
    4. Cluster and polygonize
    """
    if len(cities) < 50:
        log.warning(f"Too few cities ({len(cities)}) for UMS calculation")
        return []

    log.info("Computing UMS β=81 megalopolis regions...")

    BETA = 81.0
    THRESHOLD = 0.0005  # Net force threshold for megalopolis classification

    # Define grid bounds (rough populated world extent)
    LON_MIN, LON_MAX = -170, 180
    LAT_MIN, LAT_MAX = -55, 75
    STEP = 0.5  # 0.5° grid — ~55 km at equator

    lon_bins = int((LON_MAX - LON_MIN) / STEP) + 1
    lat_bins = int((LAT_MAX - LAT_MIN) / STEP) + 1

    # Pre-compute city arrays for speed
    city_lats = np.array([c[1] for c in cities])
    city_lons = np.array([c[2] for c in cities])
    city_pops = np.array([max(c[3], 200000) for c in cities], dtype=float)
    city_weights = city_pops / 100000.0  # Normalize weight

    def haversine(lon1, lat1, lon2, lat2):
        """Haversine distance in km."""
        R = 6371.0
        dlon = radians(lon2 - lon1)
        dlat = radians(lat2 - lat1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        return R * c

    # Sample grid at STEP intervals — compute UMS force
    grid_cells = []
    max_force = 0

    for i in range(lat_bins):
        lat = LAT_MIN + i * STEP
        if lat < -55 or lat > 72:
            continue
        row_cells = []
        for j in range(lon_bins):
            lon = LON_MIN + j * STEP
            # Skip oceans (rough check — skip cells that are clearly all ocean)
            # Calculate force from all nearby cities within 500km
            force = 0.0
            for ci in range(len(cities)):
                d = haversine(lon, lat, city_lons[ci], city_lats[ci])
                if d > 500:  # Skip cities beyond 500 km — negligible contribution
                    continue
                w = city_weights[ci]
                A = w / (1.0 + d)
                R = w / (BETA + d / 2.0)
                force += A - R

            if force > max_force:
                max_force = force
            if force > THRESHOLD:
                grid_cells.append((lon, lat, force))
        if i % 20 == 0:
            log.info(f"  UMS grid row {i}/{lat_bins}, max force so far: {max_force:.6f}")

    log.info(f"  UMS grid complete: {len(grid_cells)} megalopolis cells, max force: {max_force:.6f}")
    if len(grid_cells) < 10:
        log.warning("Too few megalopolis cells — adjust threshold")
        return []

    # Cluster cells into regions using DBSCAN-like adjacency
    cell_set = set((lon, lat) for lon, lat, _ in grid_cells)

    def get_adjacent(lon, lat):
        """Get adjacent grid cells (8-direction)."""
        adj = []
        for dl in [-STEP, 0, STEP]:
            for db in [-STEP, 0, STEP]:
                if dl == 0 and db == 0:
                    continue
                nl, nb = round(lon + dl, 6), round(lat + db, 6)
                # Round to STEP precision
                nl = round(nl / STEP) * STEP
                nb = round(nb / STEP) * STEP
                if (nl, nb) in cell_set:
                    adj.append((nl, nb))
        return adj

    # Find connected components
    visited = set()
    clusters = []
    for lon, lat, _ in grid_cells:
        key = (round(lon / STEP) * STEP, round(lat / STEP) * STEP)
        if key in visited:
            continue
        cluster = []
        stack = [key]
        while stack:
            ck = stack.pop()
            if ck in visited:
                continue
            visited.add(ck)
            cluster.append(ck)
            for adj in get_adjacent(ck[0], ck[1]):
                if adj not in visited:
                    stack.append(adj)
        if len(cluster) >= 4:  # Minimum cluster size (4 cells → ~1° region)
            clusters.append(cluster)

    log.info(f"  Found {len(clusters)} megalopolis clusters")

    # Convert clusters to polygons
    result_polys = []
    for cluster in clusters:
        if len(cluster) < 4:
            continue
        points = [Point(lon + STEP / 2, lat + STEP / 2) for lon, lat in cluster]
        if len(points) < 3:
            continue
        # Convex hull of cluster centers
        mp = unary_union(points)
        hull = mp.convex_hull.buffer(0.5)  # Expand slightly
        if hull is not None and not hull.is_empty:
            result_polys.append(hull)

    log.info(f"  Generated {len(result_polys)} megalopolis polygons")
    return result_polys


# ============================================================
# STEP 4: Define transit corridors and nodes
# ============================================================

TRANSIT_CORRIDORS = [
    {
        "name": "North Pacific Shipping Lane",
        "description": "Primary BRICS+ trade corridor: Pacifica ↔ East Asia. Los Angeles/Long Beach → Shanghai → Yokohama.",
        "coords": [
            (-118.25, 33.75), (-130.0, 35.0), (-150.0, 38.0),
            (-170.0, 40.0), (175.0, 38.0), (155.0, 35.0),
            (139.7, 35.5), (121.5, 31.2),
        ],
    },
    {
        "name": "North Atlantic Route",
        "description": "Atlantica ↔ European Federation commercial shipping. New York/Atlanta → London/Rotterdam.",
        "coords": [
            (-74.0, 40.7), (-60.0, 42.0), (-40.0, 44.0),
            (-20.0, 46.0), (-10.0, 48.0), (4.5, 51.9),
        ],
    },
    {
        "name": "HVDC Southwest Corridor",
        "description": "Aztlán → Pacifica high-voltage DC electricity transmission. Sonoran solar ↔ California load centers.",
        "coords": [
            (-112.0, 32.0), (-114.0, 34.0), (-116.0, 36.0),
            (-118.0, 38.0), (-119.0, 40.0),
        ],
    },
    {
        "name": "Great Lakes Shipping Corridor",
        "description": "Great Lakes ↔ Canada rump via Lake Superior. Duluth → Thunder Bay — grain, iron ore, manufactured goods.",
        "coords": [
            (-92.1, 46.8), (-89.5, 48.0), (-86.5, 47.5),
            (-84.5, 46.5), (-82.5, 45.5), (-79.0, 44.0),
        ],
    },
    {
        "name": "Trans-Siberian Railway",
        "description": "Russia → China energy and freight corridor. Moscow → Beijing via Kazakhstan.",
        "coords": [
            (37.6, 55.8), (50.0, 56.0), (60.0, 55.0),
            (70.0, 55.0), (80.0, 56.0), (90.0, 56.0),
            (100.0, 55.0), (110.0, 53.0), (116.4, 39.9),
        ],
    },
    {
        "name": "East African Growth Corridor",
        "description": "EAF port corridor: Dar es Salaam → Nairobi → Kampala → Juba. East African Confederation primary trade axis.",
        "coords": [
            (39.3, -6.8), (36.8, -1.3), (32.5, 0.3), (31.6, 4.8),
        ],
    },
    {
        "name": "Sahel Coastal Corridor",
        "description": "AES → Gulf of Guinea access corridor. Gold and agricultural exports via Côte d'Ivoire and Ghana ports.",
        "coords": [
            (-8.0, 15.0), (-6.0, 13.0), (-4.0, 10.0),
            (-2.0, 8.0), (0.0, 6.0), (1.0, 5.5),
        ],
    },
    {
        "name": "European High-Speed Rail Network",
        "description": "European Federation integrated HSR: Paris → Brussels → Amsterdam → Berlin → Warsaw.",
        "coords": [
            (2.3, 48.9), (4.4, 50.8), (4.9, 52.4),
            (13.4, 52.5), (21.0, 52.2),
        ],
    },
    {
        "name": "Pan-American Corridor",
        "description": "Mexico/Aztlán → Central America trade corridor. Mexico City → Guatemala City → San Salvador.",
        "coords": [
            (-99.1, 19.4), (-96.0, 18.0), (-92.0, 16.0),
            (-90.5, 14.6), (-89.2, 13.7),
        ],
    },
    {
        "name": "Power of Siberia 2 Pipeline",
        "description": "Russia → China natural gas pipeline. Yamal fields → China via Mongolia.",
        "coords": [
            (70.0, 60.0), (80.0, 58.0), (90.0, 55.0),
            (100.0, 52.0), (106.0, 48.0), (110.0, 43.0),
        ],
    },
    {
        "name": "India-Middle East-Europe Corridor",
        "description": "BRICS+ logistics corridor: Mumbai → Gulf → Mediterranean via Suez.",
        "coords": [
            (72.9, 19.1), (67.0, 24.0), (58.0, 26.0),
            (50.0, 28.0), (40.0, 32.0), (32.0, 31.0),
            (30.0, 31.0), (25.0, 36.0), (20.0, 38.0),
            (15.0, 40.0), (10.0, 45.0),
        ],
    },
]

SPACEPORTS = [
    ("Cape Canaveral Spaceport", 28.5, -80.6, "Major orbital launch facility — Atlantica/Federal. Expanded operations post-2040, commercial and government launches."),
    ("Guiana Space Centre (Kourou)", 5.2, -52.8, "European Federation primary launch facility. Modernized with reusable vehicle infrastructure."),
    ("Wenchang Spaceport", 19.6, 110.9, "China's primary coastal launch site. Expanded for heavy-lift and crewed missions."),
    ("Baikonur Cosmodrome", 45.9, 63.3, "Russia/Kazakhstan — legacy facility, reduced role. Kazakhstan retains operational control; leased to BRICS+ consortium."),
    ("Vostochny Cosmodrome", 51.8, 128.3, "Russia's primary domestic spaceport. Civil and military launches."),
    ("Satish Dhawan Space Centre", 13.7, 80.2, "India's primary launch facility. Expanded for commercial launch services."),
    ("Tanegashima Space Center", 30.4, 131.0, "Japan — JAXA primary launch site. Focus on scientific and commercial LEO launches."),
    ("Rocket Lab Launch Complex 1", -39.3, 177.9, "New Zealand — commercial small-sat launch facility. Expanded under post-US Pacific framework."),
]

MAJOR_PORTS = [
    ("Shanghai", 31.2, 121.5, "World's largest port — China. Yangshan deep-water terminal expanded."),
    ("Singapore", 1.3, 103.8, "Global transshipment hub — SEAF. Tuas mega-port fully operational."),
    ("Rotterdam", 51.9, 4.5, "Europe's largest port — European Federation. Fully automated operations."),
    ("Los Angeles/Long Beach", 33.8, -118.3, "Primary Pacifica port — largest Americas container port."),
    ("Tianjin", 39.1, 117.7, "North China primary port — Beijing's maritime gateway."),
    ("Ningbo-Zhoushan", 29.9, 122.0, "China — global top 3 by throughput. Industrial and container."),
    ("Busan", 35.1, 129.0, "ROK primary port — transshipment and industrial."),
    ("Jebel Ali (Dubai)", 25.0, 55.1, "Arab Popular Republic primary port — regional transshipment hub."),
    ("Port of New York/New Jersey", 40.7, -74.0, "Atlantica primary port — container and bulk."),
    ("Antwerp-Bruges", 51.2, 4.4, "European Federation — second-largest EU port. Chemicals and containers."),
    ("Qingdao", 36.1, 120.3, "China — major industrial and container port."),
    ("Guangzhou", 23.1, 113.3, "South China primary port — Pearl River Delta."),
    ("Mundra", 22.8, 69.7, "India's largest container port — Gujarat."),
    ("Colombo", 6.9, 79.9, "South Asia transshipment hub — Sri Lanka. BRICS+ investment expanded capacity."),
    ("Dar es Salaam", -6.8, 39.3, "EAF primary port — East African trade corridor."),
]

MAJOR_RAIL_HUBS = [
    ("Berlin Hbf", 52.5, 13.4, "European Federation central rail hub — HSR network nexus."),
    ("Paris Gare du Nord", 48.9, 2.3, "EF — HSR hub connecting London, Brussels, Amsterdam, Cologne."),
    ("Beijing Fengtai", 39.9, 116.4, "China's HSR hub — national network center."),
    ("Moscow Kiyevsky", 55.8, 37.6, "Russia — Trans-Siberian and European network hub."),
    ("London St Pancras", 51.5, -0.1, "Atlantica/UK — HSR to Europe via Channel Tunnel (EF-managed)."),
    ("Tokyo Station", 35.7, 139.8, "Japan — Shinkansen HSR hub."),
    ("Delhi HSR Terminal", 28.6, 77.2, "India — expanding HSR network hub (Mumbai-Delhi corridor)."),
]

# ============================================================
# STEP 5: Build KML
# ============================================================

def build_economy_kml(entity_data, entity_polys, cities, megalopolis_polys):
    """Build economy.kml with all 4 layers."""
    kml = simplekml.Kml(name="2050 Economy")
    kml.document.name = "2050 Economy"

    # ============================================================
    # LAYER 1: Cities & Megalopolises
    # ============================================================
    cities_fol = kml.newfolder(name="Cities & Megalopolises")
    cities_fol.visibility = 0

    # Megalopolis polygons
    for i, poly in enumerate(megalopolis_polys):
        name = f"Megalopolis Region {i + 1}"
        if poly.geom_type == "Polygon":
            coords = list(poly.exterior.coords)
            p = cities_fol.newpolygon(name=name)
            p.description = f"UMS β=81 megalopolis region. See: 2050-snapshot/domains/economy.md"
            p.style.linestyle.color = simplekml.Color.changealphaint(180, "ff6a1b9a")
            p.style.linestyle.width = 0.5
            p.style.polystyle.color = simplekml.Color.changealphaint(40, "6a1b9a")
            p.altitudemode = simplekml.AltitudeMode.clamptoground
            p.outerboundaryis = [(lon, lat) for lon, lat in coords]
        elif poly.geom_type == "MultiPolygon":
            for j, subpoly in enumerate(poly.geoms):
                coords = list(subpoly.exterior.coords)
                p = cities_fol.newpolygon(name=f"{name} - Part {j + 1}")
                p.description = f"UMS β=81 megalopolis region. See: 2050-snapshot/domains/economy.md"
                p.style.linestyle.color = simplekml.Color.changealphaint(180, "ff6a1b9a")
                p.style.linestyle.width = 0.5
                p.style.polystyle.color = simplekml.Color.changealphaint(40, "6a1b9a")
                p.altitudemode = simplekml.AltitudeMode.clamptoground
                p.outerboundaryis = [(lon, lat) for lon, lat in coords]

    # City points (top cities by population)
    sorted_cities = sorted(cities, key=lambda c: -c[3])
    for name, lat, lon, pop in sorted_cities[:80]:
        size = min(max(pop / 1000000, 0.3), 2.0)
        p = cities_fol.newpoint(name=f"{name} ({pop // 1000000}M)")
        p.coords = [(lon, lat)]
        p.description = f"Population: {pop:,} (NE estimate). See: 2050-snapshot/domains/economy.md"
        p.style.iconstyle.icon.href = (
            "http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png"
        )
        p.style.iconstyle.scale = size * 0.4
        p.altitudemode = simplekml.AltitudeMode.clamptoground

    log.info(f"Layer 1: {len(megalopolis_polys)} megalopolis polygons + {min(80, len(sorted_cities))} cities")

    # ============================================================
    # LAYER 2: Production Metric (BCU-equivalent)
    # ============================================================
    bcu_fol = kml.newfolder(name="Production Metric (BCU-equivalent)")
    bcu_fol.visibility = 0

    # Add legend-style description
    desc_lines = ["BCU-equivalent economic output tiers:", ""]
    for threshold, label, _, _ in BCU_TIERS:
        if threshold > 0:
            desc_lines.append(f">{threshold}B BCU: {label}")
        else:
            desc_lines.append(f"<20B BCU: {label}")
    desc_lines.append("")
    desc_lines.append("1 BCU ≈ 1.4 USD (dollar has depreciated ~30% post-hegemony)")
    bcu_fol.description = "\n".join(desc_lines)

    matched = 0
    for ename, coords_list in entity_polys.items():
        # Look up in entity data
        edata = entity_data.get(ename, {})
        gdp_str = edata.get("gdp_str", "")
        bcu_val = parse_gdp_to_bcu(gdp_str)
        tier, color, kml_color = classify_bcu_tier(bcu_val)

        for ci, coords_text in enumerate(coords_list):
            parsed = parse_kml_coords(coords_text)
            if len(parsed) < 3:
                continue
            coord_pairs = [(lon, lat) for lon, lat in parsed]
            suffix = f" ({ci + 1})" if len(coords_list) > 1 else ""
            p = bcu_fol.newpolygon(name=f"{ename}{suffix}")
            bcu_desc = f"{bcu_val:.0f}B BCU equivalent" if bcu_val is not None else "BCU data unavailable"
            p.description = (
                f"Economic output: {gdp_str if gdp_str else 'Unknown'} → "
                f"{bcu_desc}\n"
                f"Tier: {tier}\n"
                f"See: 2050-snapshot/domains/economy.md"
            )
            p.style.linestyle.color = simplekml.Color.changealphaint(180, kml_color)
            p.style.linestyle.width = 0.5
            p.style.polystyle.color = simplekml.Color.changealphaint(80, kml_color)
            p.altitudemode = simplekml.AltitudeMode.clamptoground
            p.outerboundaryis = coord_pairs
            matched += 1

    log.info(f"Layer 2: {matched} entity placemarks with BCU colors")

    # ============================================================
    # LAYER 3: Transit & Logistics
    # ============================================================
    transit_fol = kml.newfolder(name="Transit & Logistics Systems")
    transit_fol.visibility = 0

    # Corridor lines
    for corridor in TRANSIT_CORRIDORS:
        coords = [(lon, lat) for lon, lat in corridor["coords"]]
        ls = transit_fol.newlinestring(name=corridor["name"])
        ls.description = corridor["description"] + "\nSee: 2050-snapshot/domains/economy.md"
        ls.coords = coords
        ls.style.linestyle.color = simplekml.Color.changealphaint(220, "ffc107")
        ls.style.linestyle.width = 2.0
        ls.altitudemode = simplekml.AltitudeMode.clamptoground

    # Spaceport points
    spaceports_fol = transit_fol.newfolder(name="Spaceports")
    for name, lat, lon, desc in SPACEPORTS:
        p = spaceports_fol.newpoint(name=name)
        p.coords = [(lon, lat)]
        p.description = desc + "\nSee: 2050-snapshot/domains/economy.md"
        p.style.iconstyle.icon.href = (
            "http://maps.google.com/mapfiles/kml/shapes/astronaut.png"
        )
        p.style.iconstyle.scale = 0.8
        p.altitudemode = simplekml.AltitudeMode.clamptoground

    # Major port points
    ports_fol = transit_fol.newfolder(name="Major Ports")
    for name, lat, lon, desc in MAJOR_PORTS:
        p = ports_fol.newpoint(name=name)
        p.coords = [(lon, lat)]
        p.description = desc + "\nSee: 2050-snapshot/domains/economy.md"
        p.style.iconstyle.icon.href = (
            "http://maps.google.com/mapfiles/kml/shapes/port.png"
        )
        p.style.iconstyle.scale = 0.7
        p.altitudemode = simplekml.AltitudeMode.clamptoground

    # HSR hub points
    hsr_fol = transit_fol.newfolder(name="High-Speed Rail Hubs")
    for name, lat, lon, desc in MAJOR_RAIL_HUBS:
        p = hsr_fol.newpoint(name=name)
        p.coords = [(lon, lat)]
        p.description = desc + "\nSee: 2050-snapshot/domains/economy.md"
        p.style.iconstyle.icon.href = (
            "http://maps.google.com/mapfiles/kml/shapes/rail.png"
        )
        p.style.iconstyle.scale = 0.7
        p.altitudemode = simplekml.AltitudeMode.clamptoground

    n_transit = len(TRANSIT_CORRIDORS) + len(SPACEPORTS) + len(MAJOR_PORTS) + len(MAJOR_RAIL_HUBS)
    log.info(f"Layer 3: {len(TRANSIT_CORRIDORS)} corridors + {len(SPACEPORTS)} spaceports + {len(MAJOR_PORTS)} ports + {len(MAJOR_RAIL_HUBS)} HSR hubs")

    # ============================================================
    # LAYER 4: Production Sectors
    # ============================================================
    sector_fol = kml.newfolder(name="Production Sectors")
    sector_fol.visibility = 0

    desc_lines = ["Dominant production sector by entity:", ""]
    seen_cats = set()
    for keyword, (cat, color, kml_color) in SECTOR_CATEGORIES.items():
        if cat not in seen_cats:
            seen_cats.add(cat)
            desc_lines.append(f"● {cat}")
    sector_fol.description = "\n".join(desc_lines)

    matched_sectors = 0
    for ename, coords_list in entity_polys.items():
        edata = entity_data.get(ename, {})
        sectors_str = edata.get("sectors_str", "")
        cat, color, kml_color = classify_sector(sectors_str)

        for ci, coords_text in enumerate(coords_list):
            parsed = parse_kml_coords(coords_text)
            if len(parsed) < 3:
                continue
            coord_pairs = [(lon, lat) for lon, lat in parsed]
            suffix = f" ({ci + 1})" if len(coords_list) > 1 else ""
            p = sector_fol.newpolygon(name=f"{ename}{suffix}")
            p.description = (
                f"Dominant sector: {cat}\n"
                f"Sectors: {sectors_str[:200]}\n"
                f"See: 2050-snapshot/domains/economy.md"
            )
            p.style.linestyle.color = simplekml.Color.changealphaint(180, kml_color)
            p.style.linestyle.width = 0.5
            p.style.polystyle.color = simplekml.Color.changealphaint(80, kml_color)
            p.altitudemode = simplekml.AltitudeMode.clamptoground
            p.outerboundaryis = coord_pairs
            matched_sectors += 1

    log.info(f"Layer 4: {matched_sectors} entity placemarks by sector")

    # Save
    kml.save(OUTPUT_KML)
    log.info(f"Saved economy.kml to {OUTPUT_KML}")
    return True


# ============================================================
# MAIN
# ============================================================

def main():
    log.info("=== Economy KML Generator ===")

    # Step 1: Parse economy.md
    entity_data = parse_economy_md()

    # Step 2: Extract entity polygons from borders.kml
    entity_polys = extract_entity_polygons()
    if not entity_polys:
        log.error("No entity polygons extracted — cannot proceed")
        return False

    # Step 3: Get city data (try NE download, fallback to hardcoded)
    if not os.path.exists(NE_PLACES_ZIP):
        try:
            os.makedirs(SOURCE_DIR, exist_ok=True)
            log.info(f"Downloading NE populated places...")
            r = requests.get(NE_PLACES_URL, timeout=60)
            r.raise_for_status()
            with open(NE_PLACES_ZIP, "wb") as f:
                f.write(r.content)
            log.info(f"Downloaded {len(r.content)} bytes")
        except Exception as e:
            log.warning(f"NE download failed: {e}")
    cities = load_city_data()

    # Step 4: Compute megalopolis polygons
    megalopolis_polys = []
    if cities:
        megalopolis_polys = compute_megalopolis_polygons(cities)
    else:
        log.warning("No city data available — skipping megalopolis layer")

    # Step 5: Build KML
    success = build_economy_kml(entity_data, entity_polys, cities, megalopolis_polys)

    if success:
        log.info("=== Economy KML generation complete ===")
    return success


if __name__ == "__main__":
    main()
