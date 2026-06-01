#!/usr/bin/env python3
"""
Generate Köppen-Geiger climate classification layer for 2050 KML.

Reads GloH2O V3 2041-2070 SSP3-7.0 GeoTIFF, polygonizes Köppen class zones,
and produces a styled KML file organized by climate group (A/B/C/D/E).

Per D-01, D-02, D-12: Creates climate_koppen.kml for later merge into climate.kml.
Per D-03: High detail global — file size acceptable.
Per D-13: Cross-references back to climate.md.

Fallback: If GeoTIFF not available, creates approximate continental-level polygons
from narrative in climate.md (latitudinal bands).

Output: climate_koppen.kml — containing only the Köppen folder for later merge.
"""

import logging
import os
import sys
from collections import Counter, defaultdict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# --- Color scheme (standard Köppen palette from Beck et al. 2023) ---
# Format: code -> standard HEX RRGGBB (HTML notation)
KOPPEN_COLORS = {
    "Af": "#0000FF",   "Am": "#0078FF",   "Aw": "#46AAFA",
    "BWh": "#FE0000",  "BWk": "#FE9695",  "BSh": "#F5A505",  "BSk": "#FFDC7C",
    "Csa": "#FFCC00",  "Csb": "#C9C800",  "Cwa": "#C6C76A",  "Cwb": "#6C9A5E",
    "Cwc": "#7EAA7D",  "Cfa": "#96FF96",  "Cfb": "#6DB46D",  "Cfc": "#40A040",
    "Dsa": "#5EBDC9",  "Dsb": "#4DA6B8",  "Dsc": "#2F8FA5",
    "Dwa": "#5DF0F0",  "Dwb": "#41C8C8",  "Dwc": "#2CAAAA",
    "Dfa": "#00FFFF",  "Dfb": "#46D2D2",  "Dfc": "#64C8E4",  "Dfd": "#5EE0F0",
    "ET": "#964696",   "EF": "#FFFFFF",
}

KOPPEN_FULL_NAMES = {
    "Af": "Tropical Rainforest",
    "Am": "Tropical Monsoon",
    "Aw": "Tropical Savannah",
    "BWh": "Hot Desert",
    "BWk": "Cold Desert",
    "BSh": "Hot Semi-arid",
    "BSk": "Cold Semi-arid",
    "Csa": "Hot-summer Mediterranean",
    "Csb": "Warm-summer Mediterranean",
    "Cwa": "Monsoon humid subtropical",
    "Cwb": "Subtropical highland",
    "Cwc": "Cold subtropical highland",
    "Cfa": "Humid subtropical",
    "Cfb": "Oceanic",
    "Cfc": "Subpolar oceanic",
    "Dsa": "Mediterranean hot continental",
    "Dsb": "Mediterranean warm continental",
    "Dsc": "Mediterranean subarctic",
    "Dwa": "Monsoon hot continental",
    "Dwb": "Monsoon warm continental",
    "Dwc": "Monsoon subarctic",
    "Dfa": "Hot continental",
    "Dfb": "Warm continental",
    "Dfc": "Subarctic",
    "Dfd": "Extreme subarctic",
    "ET": "Tundra",
    "EF": "Frost/Ice Cap",
}

# Climate groups organized with their sub-types (5 major groups)
KOPPEN_GROUPS = {
    "A — Tropical Climates": ["Af", "Am", "Aw"],
    "B — Arid Climates": ["BWh", "BWk", "BSh", "BSk"],
    "C — Temperate Climates": ["Csa", "Csb", "Cwa", "Cwb", "Cwc", "Cfa", "Cfb", "Cfc"],
    "D — Continental Climates": ["Dsa", "Dsb", "Dsc", "Dwa", "Dwb", "Dwc", "Dfa", "Dfb", "Dfc", "Dfd"],
    "E — Polar Climates": ["ET", "EF"],
}

# All 30 codes in order
ALL_KOPPEN_CODES = [
    "Af", "Am", "Aw",
    "BWh", "BWk", "BSh", "BSk",
    "Csa", "Csb", "Cwa", "Cwb", "Cwc", "Cfa", "Cfb", "Cfc",
    "Dsa", "Dsb", "Dsc", "Dwa", "Dwb", "Dwc", "Dfa", "Dfb", "Dfc", "Dfd",
    "ET", "EF",
]

# Numeric value -> sub-type code (GloH2O V3 Beck et al. 2023 standard legend)
RASTER_LEGEND = {
    1: "Af", 2: "Am", 3: "Aw",
    4: "BWh", 5: "BWk", 6: "BSh", 7: "BSk",
    8: "Csa", 9: "Csb", 10: "Cwa", 11: "Cwb", 12: "Cwc",
    13: "Cfa", 14: "Cfb", 15: "Cfc",
    16: "Dsa", 17: "Dsb", 18: "Dsc",
    19: "Dwa", 20: "Dwb", 21: "Dwc",
    22: "Dfa", 23: "Dfb", 24: "Dfc", 25: "Dfd",
    26: "ET", 27: "EF",
}

# Cross-reference target for all placemarks
CLIMATE_MD_ANCHOR = "2050-snapshot/domains/climate.md#global-climate-state"

# --- Ecological Biomes constants ---

BIOME_COLORS = {
    "Tundra": "#A0A0A0",
    "Boreal Forest/Taiga": "#3A7D3A",
    "Temperate Forest": "#5CA65C",
    "Grassland/Savanna": "#E8D44D",
    "Desert": "#EDC58E",
    "Tropical Rainforest": "#1A5C1A",
}

# Visually distinct from Köppen color palette — uses earthy tones (grays, greens, tans, yellows)
# Köppen uses primary/secondary: blues, reds, yellow, purple, cyan, white

BIOME_NAMES = {
    "Tundra": "Tundra — Arctic fringe ecosystems (mosses, lichens, shrubs, permafrost)",
    "Boreal Forest/Taiga": "Boreal Forest/Taiga — Cold-tolerant coniferous forests and woodlands",
    "Temperate Forest": "Temperate Forest — Mixed deciduous and coniferous mid-latitude forests",
    "Grassland/Savanna": "Grassland/Savanna — Open grasslands, savanna woodlands, and shrublands",
    "Desert": "Desert — Hyper-arid and semi-arid desert ecosystems",
    "Tropical Rainforest": "Tropical Rainforest — Equatorial moist broadleaf forests",
}

# WWF TEOW biome name -> our target class (per reclassification table from DISCOVERY.md)
BIOME_RECLASSIFICATION = {
    "Tundra": "Tundra",
    "Boreal Forests/Taiga": "Boreal Forest/Taiga",
    "Temperate Coniferous Forests": "Temperate Forest",
    "Temperate Broadleaf & Mixed Forests": "Temperate Forest",
    "Tropical & Subtropical Moist Broadleaf Forests": "Tropical Rainforest",
    "Tropical & Subtropical Dry Broadleaf Forests": "Tropical Rainforest",
    "Tropical & Subtropical Coniferous Forests": "Tropical Rainforest",
    "Temperate Grasslands, Savannas & Shrublands": "Grassland/Savanna",
    "Flooded Grasslands & Savannas": "Grassland/Savanna",
    "Montane Grasslands & Shrublands": "Grassland/Savanna",
    "Deserts & Xeric Shrublands": "Desert",
    "Mediterranean Forests, Woodlands & Scrub": "Temperate Forest",
    "Mangroves": "Tropical Rainforest",
}

BIOMES_MD_ANCHOR = "2050-snapshot/domains/climate.md#global-climate-state"

# --- Refined Placemarks Constants ---

# Cross-reference anchors for the 11 thematic placemarks
# Maps placemark name -> climate.md section anchor
REFINED_ANCHORS = {
    "arctic": "2050-snapshot/domains/climate.md#arctic",
    "greenland": "2050-snapshot/domains/climate.md#greenland",
    "glaciers": "2050-snapshot/domains/climate.md#glaciers",
    "sea-level": "2050-snapshot/domains/climate.md#sea-level",
    "heatwaves": "2050-snapshot/domains/climate.md#heatwaves",
    "wildfire": "2050-snapshot/domains/climate.md#wildfire",
    "africa": "2050-snapshot/domains/climate.md#africa",
    "gulf": "2050-snapshot/domains/climate.md#west-asia--middle-east",
    "water-scarcity": "2050-snapshot/domains/climate.md#water-scarcity",
    "arctic-resources": "2050-snapshot/domains/climate.md#arctic-resource-competition",
    "technology": "2050-snapshot/domains/climate.md#to-technology",
}

# Style colors for refined placemarks
# Format: (poly_color_AARRGGBB, line_color_AARRGGBB, line_width)
REFINED_STYLE_DEFAULT = ("4055b0b0", "ff55b0b0", 0.5)  # Standard teal climate overlay
REFINED_STYLE_WATER = ("405555b0", "ff5555b0", 0.5)     # Teal-blue shift for water basins
REFINED_STYLE_ARCTIC = ("40b0b055", "ffb0b055", 0.5)    # Teal-green shift for arctic resources

APPROXIMATE_NOTE = (
    "APPROXIMATE — Narrative-derived polygon. Replace with data-driven "
    "geometry when source dataset becomes available."
)


def _make_coords_box(min_lon, min_lat, max_lon, max_lat):
    """Create a rectangular bounding box coordinate list (counterclockwise)."""
    return [
        (min_lon, min_lat), (max_lon, min_lat),
        (max_lon, max_lat), (min_lon, max_lat),
        (min_lon, min_lat),
    ]


def _make_zones_from_func(placemark_name, anchor_key, zones_data, approx=False):
    """
    Build zone list from structured zone data.

    zones_data: list of dicts with keys: zone_name, coords, desc_suffix (optional)
    Returns list of zone dicts for the aggregator.
    """
    anchor = REFINED_ANCHORS.get(anchor_key, "")
    approx_note = APPROXIMATE_NOTE if approx else ""
    zones = []

    for z in zones_data:
        desc = z.get("desc_suffix", "")
        full_desc = (
            f"{desc} "
            f"{approx_note} "
            f"See: {anchor}"
        ).strip()
        # Clean up double spaces/whitespace
        full_desc = " ".join(full_desc.split())

        zones.append({
            "name": placemark_name,
            "zone_name": z.get("zone_name", ""),
            "coords": z["coords"],
            "desc": full_desc,
            "style": REFINED_STYLE_DEFAULT,
        })

    return zones


# --- 1. Arctic Permafrost Degradation Zone ---

def refine_arctic_permafrost():
    """
    Arctic Permafrost Degradation Zone — multi-polygon across Siberia, Alaska, Canada.

    Fallback from climate.md: Permafrost across Siberia, Alaska, and northern Canada
    above 60°N excluding Greenland ice sheet.

    Returns:
        list of zone dicts (Siberian, Alaskan, Canadian permafrost zones)
    """
    anchor = REFINED_ANCHORS["arctic"]
    approx = APPROXIMATE_NOTE

    zones = []

    # Siberian permafrost: ~60-180°E, 60-75°N — detailed polygon tracing permafrost extent
    siberia_coords = [
        (60, 60), (75, 60), (85, 61), (95, 63), (105, 64), (115, 64),
        (125, 63), (135, 62), (145, 61), (155, 60), (165, 60),
        (175, 62), (180, 66), (180, 75), (170, 76), (160, 75),
        (150, 74), (140, 74), (130, 73), (120, 72), (110, 72),
        (100, 71), (90, 70), (80, 68), (70, 66), (60, 65), (60, 60),
    ]
    zones.append({
        "name": "Arctic Permafrost Degradation Zone",
        "zone_name": "Siberian Permafrost",
        "coords": siberia_coords,
        "desc": (
            "Siberian permafrost zone — continuous and discontinuous permafrost "
            "across the Siberian Arctic. Methane release from thawing yedoma "
            "permafrost is a major positive feedback to global warming. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Alaskan permafrost: ~170-140°W, 60-72°N
    alaska_coords = [
        (-170, 60), (-165, 60), (-160, 61), (-155, 62), (-150, 63),
        (-145, 63), (-140, 60), (-140, 72), (-145, 72), (-150, 71),
        (-155, 71), (-160, 70), (-165, 68), (-170, 66), (-170, 60),
    ]
    zones.append({
        "name": "Arctic Permafrost Degradation Zone",
        "zone_name": "Alaskan Permafrost",
        "coords": alaska_coords,
        "desc": (
            "Alaskan permafrost zone — North Slope and interior Alaska. "
            "Active layer depth has increased 30-100cm, destabilizing infrastructure. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Canadian permafrost: ~140-60°W, 60-75°N (continental Canada, excluding Greenland)
    canada_coords = [
        (-140, 60), (-130, 60), (-120, 61), (-110, 62), (-100, 63),
        (-90, 64), (-80, 65), (-70, 66), (-60, 67),
        (-60, 75), (-70, 73), (-80, 72), (-90, 72),
        (-100, 72), (-110, 71), (-120, 69), (-130, 67),
        (-140, 65), (-140, 60),
    ]
    zones.append({
        "name": "Arctic Permafrost Degradation Zone",
        "zone_name": "Canadian Permafrost",
        "coords": canada_coords,
        "desc": (
            "Canadian permafrost zone — northern Canada excluding the Greenland ice sheet. "
            "Infrastructure damage from permafrost thaw affects roads, buildings, and airports. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    return zones


# --- 2. Greenland Ice Sheet Retreat Zone ---

def refine_greenland_ice():
    """
    Greenland Ice Sheet Retreat Zone — single polygon covering Greenland ice sheet.

    Fallback: Greenland polygon showing ice sheet extent (~80% of island).

    Returns:
        list with one zone dict
    """
    anchor = REFINED_ANCHORS["greenland"]
    approx = APPROXIMATE_NOTE

    # Greenland ice sheet outline (approximate, ~80% of island area)
    greenland_coords = [
        (-55, 60), (-48, 60), (-44, 62), (-42, 64), (-40, 66),
        (-38, 68), (-36, 70), (-34, 72), (-32, 75), (-30, 78),
        (-28, 80), (-25, 82), (-20, 82), (-18, 80), (-16, 78),
        (-18, 76), (-20, 74), (-22, 72), (-22, 70), (-20, 68),
        (-22, 66), (-24, 64), (-28, 62), (-35, 61), (-42, 60),
        (-48, 60), (-55, 60),
    ]

    return [{
        "name": "Greenland Ice Sheet Retreat Zone",
        "zone_name": "",
        "coords": greenland_coords,
        "desc": (
            "Greenland ice sheet — mass loss ~300-400 Gt/yr contributing "
            "~0.8-1.0 mm/yr to global sea level rise. The equilibrium line "
            "has migrated 200-400m upward in elevation since the early 2020s. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    }]


# --- 3. Glacier Mass Loss Extent ---

def refine_glaciers():
    """
    Glacier Mass Loss Extent — multi-polygon for major glacierized regions.

    6+ regional polygons: Himalayas, Andes, Alps, Alaska Range, Rockies, Kilimanjaro.

    Returns:
        list of zone dicts
    """
    anchor = REFINED_ANCHORS["glaciers"]
    approx = APPROXIMATE_NOTE

    zones = []

    # Himalayas/Karakoram: 28-32°N, 75-95°E
    himalayas_coords = [
        (75, 28), (78, 27), (82, 27), (85, 28), (88, 28), (90, 29),
        (95, 30), (95, 32), (92, 32), (88, 31), (85, 31), (80, 31),
        (77, 30), (75, 29), (75, 28),
    ]
    zones.append({
        "name": "Glacier Mass Loss Extent",
        "zone_name": "Himalayas-Karakoram",
        "coords": himalayas_coords,
        "desc": (
            "Himalayan and Karakoram glacier zone — 40-60% mass loss since 1990s. "
            "Threatens dry-season water supply for 1.5+ billion people across the "
            "Indus, Ganges, and Brahmaputra basins. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Andes: 10°S-50°S, 70-80°W
    andes_coords = [
        (-80, -10), (-70, -10), (-72, -20), (-70, -30), (-72, -35),
        (-70, -40), (-72, -45), (-70, -50), (-76, -50), (-74, -45),
        (-76, -40), (-74, -35), (-76, -30), (-74, -20), (-78, -15),
        (-80, -10),
    ]
    zones.append({
        "name": "Glacier Mass Loss Extent",
        "zone_name": "Andes",
        "coords": andes_coords,
        "desc": (
            "Andean glacier zone — tropical glaciers functionally extinct "
            "below 5,500m. Water supply threatened for La Paz, Quito, Lima, Bogotá. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Alps: 45-48°N, 6-15°E
    alps_coords = [
        (6, 45), (7, 45), (8, 45), (10, 45), (12, 45),
        (15, 46), (15, 48), (12, 47), (10, 47), (8, 47),
        (7, 46), (6, 46), (6, 45),
    ]
    zones.append({
        "name": "Glacier Mass Loss Extent",
        "zone_name": "European Alps",
        "coords": alps_coords,
        "desc": (
            "Alpine glacier zone — 50-60% volume loss since 2000. "
            "Summer ski tourism eliminated; hydropower reduced 15-25%. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Alaska Range: 60-65°N, 140-150°W
    alaska_range_coords = [
        (-150, 60), (-145, 61), (-140, 62), (-140, 65), (-145, 64),
        (-148, 63), (-150, 62), (-150, 60),
    ]
    zones.append({
        "name": "Glacier Mass Loss Extent",
        "zone_name": "Alaska Range",
        "coords": alaska_range_coords,
        "desc": (
            "Alaskan glacier zone — includes major glaciers of the Alaska Range "
            "and coastal mountains. Rapid retreat accelerating sea level contribution. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Rockies: 35-50°N, 105-115°W
    rockies_coords = [
        (-115, 35), (-110, 35), (-105, 38), (-105, 42),
        (-108, 45), (-105, 48), (-110, 50), (-115, 48),
        (-115, 42), (-115, 35),
    ]
    zones.append({
        "name": "Glacier Mass Loss Extent",
        "zone_name": "Rocky Mountains",
        "coords": rockies_coords,
        "desc": (
            "Rocky Mountain glacier zone — reduced snowpack threatens "
            "water supply for western US and Canada. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Kilimanjaro: ~3°S, 37°E
    kilimanjaro_coords = [
        (37.1, -3.2), (37.3, -3.2), (37.4, -3.0), (37.4, -2.9),
        (37.3, -2.8), (37.1, -2.8), (37.0, -2.9), (37.0, -3.1),
        (37.1, -3.2),
    ]
    zones.append({
        "name": "Glacier Mass Loss Extent",
        "zone_name": "Kilimanjaro, East Africa",
        "coords": kilimanjaro_coords,
        "desc": (
            "Kilimanjaro glacier zone — tropical glaciers functionally extinct below 5,500m. "
            "East African glacier loss threatens regional water supply. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    return zones


# --- 4. Sea Level Impact Zones ---

def refine_sealevel():
    """
    Sea Level Impact Zones — coastal low-elevation zones for major coastal regions.

    Broader than the 6 SLR hotspot regions from Plan 03 — covers all
    major coastal low-elevation zones referenced in climate.md §Key Changes.

    Returns:
        list of zone dicts
    """
    anchor = REFINED_ANCHORS["sea-level"]
    approx = APPROXIMATE_NOTE

    zones = []

    coastal_regions = [
        {
            "zone": "Bangladesh — Ganges-Brahmaputra Delta",
            "coords": [
                (88, 21), (89, 21.5), (90, 22), (91, 22.5), (92, 23),
                (92, 24), (91, 24), (90, 23.5), (89, 23), (88, 22.5),
                (88, 21),
            ],
        },
        {
            "zone": "Mekong Delta — Vietnam",
            "coords": [
                (104.5, 8.5), (106, 8.5), (107, 9), (107, 10.5),
                (106, 10.5), (104.5, 10), (104.5, 8.5),
            ],
        },
        {
            "zone": "Nile Delta — Egypt",
            "coords": [
                (29.5, 30), (30.5, 30), (31.5, 30.5), (32, 31),
                (31.5, 31.5), (31, 31.5), (30, 31), (29.5, 30.5),
                (29.5, 30),
            ],
        },
        {
            "zone": "US Gulf Coast",
            "coords": [
                (-96, 28), (-94, 28.5), (-92, 29), (-90, 29.5),
                (-88, 30), (-88, 31), (-90, 31), (-92, 30.5),
                (-94, 30), (-96, 29.5), (-96, 28),
            ],
        },
        {
            "zone": "US East Coast — Mid-Atlantic",
            "coords": [
                (-77, 36), (-75, 36), (-74, 38), (-74, 40),
                (-75, 41), (-76, 41), (-77, 40), (-77, 38),
                (-77, 36),
            ],
        },
        {
            "zone": "Netherlands — North Sea Coast",
            "coords": [
                (3, 51), (4, 51.5), (5, 52), (6, 52.5), (7, 53),
                (8, 53.5), (8, 54), (7, 54), (6, 53.5), (5, 53),
                (4, 52.5), (3, 52), (3, 51),
            ],
        },
        {
            "zone": "Pacific Atolls — Tuvalu, Kiribati, Marshall Islands, Maldives",
            "coords": [
                # Rough polygon covering Pacific atoll zones
                (172, -10), (180, -8), (180, 10), (172, 8),
                (160, 5), (140, 0), (120, -5), (100, -5),
                (73, 3), (73, 5), (100, 0), (120, 5),
                (140, 10), (160, 10), (172, -10),
            ],
        },
        {
            "zone": "Shanghai — Yangtze Delta",
            "coords": [
                (121, 30.5), (122, 30.5), (122, 31.5), (121.5, 31.8),
                (121, 31.5), (121, 30.5),
            ],
        },
        {
            "zone": "South American Atlantic Coast",
            "coords": [
                (-58, -35), (-52, -34), (-48, -30), (-42, -25),
                (-40, -20), (-38, -15), (-38, -12), (-40, -12),
                (-42, -20), (-48, -25), (-52, -30), (-58, -33),
                (-58, -35),
            ],
        },
        {
            "zone": "West Africa — Gulf of Guinea Coast",
            "coords": [
                (-8, 4.5), (-5, 4.5), (-2, 5), (0, 5),
                (2, 5), (5, 5), (8, 4.5), (8, 6),
                (5, 6), (2, 5.5), (0, 5.5), (-2, 5.5),
                (-5, 5), (-8, 5), (-8, 4.5),
            ],
        },
    ]

    for region in coastal_regions:
        zones.append({
            "name": "Sea Level Impact Zones",
            "zone_name": region["zone"],
            "coords": region["coords"],
            "desc": (
                f"Coastal low-elevation zone — {region['zone']}. "
                f"Sea level rise of +0.35m by 2050 (global mean) with regional "
                f"variation due to subsidence, tidal amplification, and ocean dynamics. "
                f"{approx} "
                f"See: {anchor}"
            ),
            "style": REFINED_STYLE_DEFAULT,
        })

    return zones


# --- 5. Extreme Heat Zones ---

def refine_heat():
    """
    Extreme Heat Zones — 4 regional polygons.

    Indus Valley, Persian Gulf coastal zone, Sahel belt, US Southwest.

    Returns:
        list of zone dicts
    """
    anchor = REFINED_ANCHORS["heatwaves"]
    approx = APPROXIMATE_NOTE

    zones = []

    # Indus Valley: 22-32°N, 68-78°E
    indus_coords = [
        (68, 22), (70, 22), (72, 23), (74, 24), (76, 25),
        (78, 28), (78, 32), (76, 32), (74, 30), (72, 28),
        (70, 26), (68, 24), (68, 22),
    ]
    zones.append({
        "name": "Extreme Heat Zones",
        "zone_name": "Indus Valley",
        "coords": indus_coords,
        "desc": (
            "Indus Valley heat zone — routinely exceeds 50°C. "
            "Wet-bulb temperatures approach survivability threshold during peak events. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Persian Gulf coastal: 22-30°N, 46-58°E
    gulf_coords = [
        (46, 22), (48, 22), (50, 23), (52, 24), (54, 25),
        (56, 26), (58, 27), (58, 30), (56, 30), (54, 28),
        (52, 27), (50, 26), (48, 25), (46, 24), (46, 22),
    ]
    zones.append({
        "name": "Extreme Heat Zones",
        "zone_name": "Persian Gulf",
        "coords": gulf_coords,
        "desc": (
            "Persian Gulf heat zone — wet-bulb temperatures exceed "
            "human survivability threshold (35°C) for brief periods. "
            "Outdoor labor lethal without artificial cooling. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Sahel belt: 10-20°N, 15°W-40°E
    sahel_coords = [
        (-15, 10), (-10, 10), (-5, 11), (0, 12), (5, 13),
        (10, 14), (15, 15), (20, 15), (25, 16), (30, 17),
        (35, 18), (40, 20), (40, 18), (35, 16), (30, 15),
        (25, 14), (20, 13), (15, 12), (10, 11), (5, 11),
        (0, 10), (-5, 10), (-10, 9), (-15, 9), (-15, 10),
    ]
    zones.append({
        "name": "Extreme Heat Zones",
        "zone_name": "Sahel Belt",
        "coords": sahel_coords,
        "desc": (
            "Sahel heat zone — 15-25% rainfall decline combined with "
            "temperature increases of 2-3°C. Agricultural viability collapsed "
            "in worst-affected zones. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # US Southwest: 30-40°N, 105-120°W
    ussw_coords = [
        (-120, 30), (-115, 30), (-110, 31), (-105, 33),
        (-105, 36), (-108, 38), (-110, 40), (-115, 40),
        (-120, 38), (-120, 35), (-120, 30),
    ]
    zones.append({
        "name": "Extreme Heat Zones",
        "zone_name": "US Southwest",
        "coords": ussw_coords,
        "desc": (
            "US Southwest heat zone — decade-scale megadrought ongoing since "
            "early 2000s. Colorado River flows at 30-40% of early-21st-century baseline. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    return zones


# --- 6. Fire Regime Shift ---

def refine_fire():
    """
    Fire Regime Shift — 5 regional polygons.

    Western US/Canada, Siberia, Australia, Mediterranean, Amazon.

    Returns:
        list of zone dicts
    """
    anchor = REFINED_ANCHORS["wildfire"]
    approx = APPROXIMATE_NOTE

    zones = []

    # Western US/Canada: 30-55°N, 120-130°W
    wus_coords = [
        (-130, 30), (-118, 30), (-115, 32), (-115, 35),
        (-118, 38), (-120, 42), (-120, 45), (-118, 48),
        (-120, 50), (-125, 52), (-130, 55), (-130, 50),
        (-130, 40), (-130, 30),
    ]
    zones.append({
        "name": "Fire Regime Shift",
        "zone_name": "Western US/Canada",
        "coords": wus_coords,
        "desc": (
            "Western US/Canada fire regime — area burned annually increased 2-3x. "
            "Fire seasons 30-50 days longer. Pyrocumulonimbus clouds inject smoke "
            "into stratosphere. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Siberia: 50-70°N, 60-180°E
    siberia_fire_coords = [
        (60, 50), (80, 50), (100, 52), (120, 54), (140, 56),
        (160, 58), (180, 60), (180, 70), (160, 68), (140, 66),
        (120, 64), (100, 62), (80, 60), (60, 58), (60, 50),
    ]
    zones.append({
        "name": "Fire Regime Shift",
        "zone_name": "Siberia",
        "coords": siberia_fire_coords,
        "desc": (
            "Siberian fire regime — most dramatic boreal increase. "
            "Fires in previously fire-resistant peatlands release carbon stored for millennia. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Australia: 20-40°S, 115-155°E
    aus_coords = [
        (115, -40), (120, -38), (125, -35), (130, -33),
        (135, -30), (140, -28), (145, -25), (150, -22),
        (155, -20), (155, -25), (150, -27), (145, -30),
        (140, -33), (135, -36), (130, -38), (125, -40),
        (115, -40),
    ]
    zones.append({
        "name": "Fire Regime Shift",
        "zone_name": "Australia",
        "coords": aus_coords,
        "desc": (
            "Australian fire regime — Black Summer (2019-20) is now a typical "
            "fire season. Area burned 2-3x higher than pre-2019 baseline. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Mediterranean Basin: 35-45°N, 10°W-40°E
    med_coords = [
        (-10, 35), (-5, 36), (0, 37), (5, 38), (10, 39),
        (15, 40), (20, 41), (25, 42), (30, 43), (35, 44),
        (40, 45), (40, 42), (35, 40), (30, 38), (25, 37),
        (20, 36), (15, 35), (10, 35), (5, 35), (0, 35),
        (-5, 35), (-10, 35),
    ]
    zones.append({
        "name": "Fire Regime Shift",
        "zone_name": "Mediterranean Basin",
        "coords": med_coords,
        "desc": (
            "Mediterranean fire regime — wildfire seasons 60+ days longer. "
            "Southern Spain, Italy, Greece, Turkey face desertification. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    # Amazon: 15°S-5°N, 40-80°W
    amazon_coords = [
        (-80, -15), (-72, -15), (-65, -12), (-60, -8),
        (-55, -5), (-50, -2), (-45, 0), (-40, 3),
        (-40, 5), (-45, 5), (-50, 4), (-55, 2),
        (-60, 0), (-65, -2), (-70, -5), (-75, -8),
        (-80, -10), (-80, -15),
    ]
    zones.append({
        "name": "Fire Regime Shift",
        "zone_name": "Amazon Basin",
        "coords": amazon_coords,
        "desc": (
            "Amazon fire regime — basin crossed dieback threshold in August 2047. "
            "Ecological collapse underway with savannization of 30-50% of forest area. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    })

    return zones


# --- 7. Sahel Degradation Zone ---

def refine_sahel():
    """
    Sahel Degradation Zone — multi-polygon per Sahel country.

    5 country polygons: Mali, Burkina Faso, Niger, Chad, Sudan.

    Returns:
        list of zone dicts
    """
    anchor = REFINED_ANCHORS["africa"]
    approx = APPROXIMATE_NOTE

    zones = []

    # Coordinates from approximate country boundaries
    sahel_countries = [
        {
            "name": "Mali",
            "coords": [
                (-12, 10), (-12, 15), (-8, 16), (-5, 17),
                (-4, 20), (-4, 25), (0, 25), (4, 25),
                (4, 20), (4, 15), (4, 12), (2, 10),
                (0, 10), (-4, 10), (-8, 10), (-12, 10),
            ],
        },
        {
            "name": "Burkina Faso",
            "coords": [
                (-5, 9.5), (-5, 12), (-2, 13), (0, 13),
                (2, 13), (2, 11), (2, 9.5), (0, 9.5),
                (-2, 9.5), (-5, 9.5),
            ],
        },
        {
            "name": "Niger",
            "coords": [
                (0, 12), (2, 12), (4, 13), (8, 14),
                (12, 14), (16, 16), (16, 20), (12, 20),
                (8, 22), (6, 23), (4, 23), (2, 20),
                (0, 18), (0, 14), (0, 12),
            ],
        },
        {
            "name": "Chad",
            "coords": [
                (14, 8), (16, 8), (18, 8), (20, 9),
                (22, 11), (24, 14), (24, 18), (22, 20),
                (20, 22), (18, 22), (16, 20), (14, 18),
                (14, 15), (14, 12), (14, 8),
            ],
        },
        {
            "name": "Sudan",
            "coords": [
                (22, 10), (24, 10), (26, 10), (28, 12),
                (30, 14), (32, 16), (34, 18), (36, 20),
                (38, 22), (36, 24), (34, 24), (32, 22),
                (30, 20), (28, 18), (26, 16), (24, 14),
                (22, 12), (22, 10),
            ],
        },
    ]

    for country in sahel_countries:
        zones.append({
            "name": "Sahel Degradation Zone",
            "zone_name": country["name"],
            "coords": country["coords"],
            "desc": (
                f"{country['name']} — Sahel country experiencing 15-25% rainfall decline "
                f"and 2-3°C temperature increase. Agricultural viability collapsed in "
                f"worst-affected zones. Single largest climate-driven humanitarian disaster. "
                f"{approx} "
                f"See: {anchor}"
            ),
            "style": REFINED_STYLE_DEFAULT,
        })

    return zones


# --- 8. Extreme Heat — Persian Gulf ---

def refine_persian_gulf():
    """
    Extreme Heat — Persian Gulf — single detailed coastal polygon.

    Persian Gulf coastline + 50km inland buffer (22-32°N, 46-58°E).

    Returns:
        list with one zone dict
    """
    anchor = REFINED_ANCHORS["gulf"]
    approx = APPROXIMATE_NOTE

    # Detailed polygon following Persian Gulf coastline with inland buffer
    gulf_coords = [
        (46, 22), (48, 22), (49, 23), (50, 23.5), (51, 24),
        (52, 24.5), (53, 25), (54, 25.5), (55, 26), (56, 26.5),
        (57, 27), (58, 27.5), (58, 30), (57, 30), (56, 29),
        (54, 28), (52, 27.5), (50, 27), (49, 26), (48, 25.5),
        (47, 25), (46, 24), (46, 22),
    ]

    return [{
        "name": "Extreme Heat — Persian Gulf",
        "zone_name": "",
        "coords": gulf_coords,
        "desc": (
            "Persian Gulf extreme heat zone — wet-bulb temperatures exceed "
            "human survivability threshold (35°C) for brief annual periods. "
            "Summer temperatures routinely exceed 50°C in Iraq, Kuwait, "
            "Saudi Arabia, and Iran. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_DEFAULT,
    }]


# --- 9. Transboundary Water Conflict Basins ---

def _try_read_hydrosheds_basin(continent_code, bbox):
    """
    Attempt to read HydroSHEDS sub-basins within a bounding box.

    Args:
        continent_code: 'as', 'af', 'eu', 'na', 'sa', 'si', 'au'
        bbox: (min_lon, min_lat, max_lon, max_lat)

    Returns:
        Shapely MultiPolygon or None if data unavailable
    """
    from shapely.geometry import shape, box
    from shapely.ops import unary_union

    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, "source", f"hybas_{continent_code}_lev04_v1c.zip")

    if not os.path.isfile(zip_path):
        return None

    try:
        import fiona
        search_box = box(*bbox)
        basin_polys = []

        with fiona.open(f"zip://{zip_path}") as src:
            for feat in src:
                geom = shape(feat["geometry"])
                if geom.intersects(search_box):
                    if not geom.is_empty and geom.is_valid:
                        basin_polys.append(geom)

        if not basin_polys:
            return None

        merged = unary_union(basin_polys)
        if merged.is_empty:
            return None

        # Simplify for KML size
        simplified = merged.simplify(0.02, preserve_topology=True)
        return simplified

    except Exception as e:
        log.warning(f"HydroSHEDS read failed for {continent_code}: {e}")
        return None


def refine_water_basins():
    """
    Transboundary Water Conflict Basins — 9 individual watershed polygons.

    Data-driven (primary): Uses HydroSHEDS HydroBASINS level 4 data.
    Fallback: Approximate bounding polygons from known river basin extents.

    Basins: Indus, Nile, Mekong, Colorado, Amu Darya, Tigris-Euphrates,
            Dnieper, Yellow River, Amur/Heilongjiang.

    Returns:
        list of zone dicts
    """
    anchor = REFINED_ANCHORS["water-scarcity"]

    # Basin bounding boxes for HydroSHEDS lookup + fallback
    # (continent_code, bbox(min_lon, min_lat, max_lon, max_lat), name)
    basin_defs = [
        ("as", (65, 22, 82, 38), "Indus River Basin"),
        ("af", (25, -5, 50, 20), "Nile River Basin"),
        ("as", (95, 8, 110, 35), "Mekong River Basin"),
        ("na", (-114, 30, -105, 41), "Colorado River Basin"),
        ("as", (55, 34, 75, 44), "Amu Darya / Syr Darya Basin"),
        ("as", (35, 28, 50, 40), "Tigris-Euphrates Basin"),
        ("eu", (28, 48, 38, 57), "Dnieper River Basin"),
        ("as", (95, 32, 115, 42), "Yellow River Basin"),
        ("si", (108, 40, 145, 58), "Amur / Heilongjiang Basin"),
    ]

    # Fallback approximate polygons per basin (known river basin extents)
    fallback_coords = {
        "Indus River Basin": [
            (65, 22), (68, 24), (70, 26), (72, 28), (74, 30),
            (76, 32), (78, 34), (82, 36), (82, 38), (80, 38),
            (78, 36), (76, 34), (74, 32), (72, 30), (70, 28),
            (68, 26), (66, 24), (65, 22),
        ],
        "Nile River Basin": [
            (25, -5), (28, -5), (30, -3), (32, 0), (34, 5),
            (36, 10), (38, 15), (40, 20), (50, 20), (50, 18),
            (48, 15), (46, 12), (44, 10), (42, 5), (40, 0),
            (38, -2), (36, -4), (34, -5), (30, -5), (25, -5),
        ],
        "Mekong River Basin": [
            (95, 8), (98, 8), (100, 10), (102, 12), (104, 14),
            (106, 16), (108, 18), (110, 22), (110, 35), (108, 35),
            (106, 30), (104, 25), (102, 20), (100, 16), (98, 14),
            (96, 12), (95, 10), (95, 8),
        ],
        "Colorado River Basin": [
            (-114, 30), (-112, 31), (-110, 32), (-108, 34),
            (-106, 36), (-105, 38), (-105, 41), (-108, 41),
            (-110, 40), (-112, 39), (-114, 37), (-114, 35),
            (-114, 33), (-114, 30),
        ],
        "Amu Darya / Syr Darya Basin": [
            (55, 34), (58, 34), (60, 36), (62, 38), (65, 40),
            (68, 42), (70, 44), (75, 44), (75, 42), (72, 40),
            (68, 38), (65, 36), (62, 35), (58, 35), (55, 34),
        ],
        "Tigris-Euphrates Basin": [
            (35, 28), (36, 30), (38, 32), (40, 34), (42, 36),
            (44, 38), (46, 40), (50, 40), (50, 38), (48, 36),
            (46, 34), (44, 32), (42, 30), (40, 29), (38, 28),
            (35, 28),
        ],
        "Dnieper River Basin": [
            (28, 48), (30, 48), (32, 49), (34, 50), (36, 52),
            (38, 54), (38, 57), (36, 57), (34, 55), (32, 53),
            (30, 51), (28, 50), (28, 48),
        ],
        "Yellow River Basin": [
            (95, 32), (98, 32), (100, 34), (102, 36), (105, 38),
            (108, 40), (112, 42), (115, 42), (115, 40), (112, 38),
            (108, 36), (105, 35), (102, 34), (100, 33), (98, 32),
            (95, 32),
        ],
        "Amur / Heilongjiang Basin": [
            (108, 40), (112, 40), (115, 42), (118, 44), (120, 46),
            (125, 48), (130, 50), (135, 52), (140, 54), (145, 56),
            (145, 58), (142, 58), (138, 56), (132, 54), (128, 52),
            (124, 50), (120, 48), (115, 46), (112, 44), (108, 42),
            (108, 40),
        ],
    }

    zones = []

    for continent_code, bbox, basin_name in basin_defs:
        # Try data-driven: HydroSHEDS
        geom = _try_read_hydrosheds_basin(continent_code, bbox)

        if geom is not None:
            if geom.geom_type == "Polygon":
                coords = [(x, y) for x, y in geom.exterior.coords]
            elif geom.geom_type == "MultiPolygon":
                # Take the largest component
                parts = sorted(geom.geoms, key=lambda p: p.area, reverse=True)
                coords = [(x, y) for x, y in parts[0].exterior.coords]
            else:
                coords = fallback_coords[basin_name]

            desc_prefix = f"{basin_name} — HydroSHEDS-derived watershed polygon."
        else:
            # Fallback: approximate polygon
            coords = fallback_coords.get(basin_name, [])
            desc_prefix = (
                f"{basin_name} — APPROXIMATE watershed boundary. "
                f"HydroSHEDS data unavailable for this region."
            )

        if not coords:
            continue

        zones.append({
            "name": "Transboundary Water Conflict Basins",
            "zone_name": basin_name,
            "coords": coords,
            "desc": (
                f"{desc_prefix} "
                f"Transboundary basin under water scarcity stress in 2050. "
                f"See: {anchor}"
            ),
            "style": REFINED_STYLE_WATER,
        })

    return zones


# --- 10. Arctic Resource Zones ---

def refine_arctic_resources():
    """
    Arctic Resource Zones — 5 sector polygons around the Arctic.

    Russian, Canadian, US/Alaskan, Norwegian, Greenlandic/Danish sectors.

    Returns:
        list of zone dicts
    """
    anchor = REFINED_ANCHORS["arctic-resources"]
    approx = APPROXIMATE_NOTE

    zones = []

    # Russian Arctic sector: ~30°E to ~180°E, above 66.5°N
    russian_coords = [
        (30, 66.5), (40, 67), (50, 68), (65, 69), (80, 70),
        (95, 71), (110, 72), (125, 73), (140, 74), (155, 75),
        (170, 76), (180, 77), (180, 90), (170, 90), (155, 90),
        (140, 90), (125, 90), (110, 90), (95, 90), (80, 90),
        (65, 90), (50, 90), (40, 90), (30, 90), (30, 66.5),
    ]
    zones.append({
        "name": "Arctic Resource Zones",
        "zone_name": "Russian Arctic Sector",
        "coords": russian_coords,
        "desc": (
            "Russian Arctic sector — extensive Northern Sea Route (ice-free 5-7 months/year). "
            "Nuclear-powered icebreakers based in Murmansk. Permafrost thaw affects 65% "
            "of Russian territory. Oil, gas, and mineral resources. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_ARCTIC,
    })

    # Canadian Arctic sector: ~60°W to ~140°W, above 66.5°N
    canadian_coords = [
        (-140, 66.5), (-130, 67), (-120, 68), (-110, 69),
        (-100, 70), (-90, 71), (-80, 72), (-70, 73),
        (-60, 74), (-60, 90), (-70, 90), (-80, 90),
        (-90, 90), (-100, 90), (-110, 90), (-120, 90),
        (-130, 90), (-140, 90), (-140, 66.5),
    ]
    zones.append({
        "name": "Arctic Resource Zones",
        "zone_name": "Canadian Arctic Sector",
        "coords": canadian_coords,
        "desc": (
            "Canadian Arctic sector — Northwest Passage shipping route. "
            "Permafrost infrastructure damage. Arctic sovereignty claims "
            "including extended continental shelf submission. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_ARCTIC,
    })

    # US/Alaskan Arctic sector: ~140°W to ~180°W, above 66.5°N
    us_arctic_coords = [
        (-180, 66.5), (-170, 67), (-160, 68), (-150, 69),
        (-140, 70), (-140, 90), (-150, 90), (-160, 90),
        (-170, 90), (-180, 90), (-180, 66.5),
    ]
    zones.append({
        "name": "Arctic Resource Zones",
        "zone_name": "US/Alaskan Arctic Sector",
        "coords": us_arctic_coords,
        "desc": (
            "US/Alaskan Arctic sector — North Slope oil and gas reserves. "
            "Permafrost thaw affecting infrastructure. Arctic strategic importance. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_ARCTIC,
    })

    # Norwegian Arctic sector: ~30°E to ~10°W, above 66.5°N
    norwegian_coords = [
        (-10, 66.5), (0, 67), (10, 68), (20, 69),
        (30, 70), (30, 90), (20, 90), (10, 90),
        (0, 90), (-10, 90), (-10, 66.5),
    ]
    zones.append({
        "name": "Arctic Resource Zones",
        "zone_name": "Norwegian Arctic Sector",
        "coords": norwegian_coords,
        "desc": (
            "Norwegian Arctic sector — Svalbard archipelago, Barents Sea oil and gas. "
            "Strategic position for Arctic shipping and research. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_ARCTIC,
    })

    # Greenlandic/Danish Arctic sector: ~10°W to ~60°W, above 66.5°N
    greenlandic_coords = [
        (-60, 66.5), (-50, 67), (-40, 68), (-30, 69),
        (-20, 70), (-10, 71), (-10, 90), (-20, 90),
        (-30, 90), (-40, 90), (-50, 90), (-60, 90),
        (-60, 66.5),
    ]
    zones.append({
        "name": "Arctic Resource Zones",
        "zone_name": "Greenlandic/Danish Arctic Sector",
        "coords": greenlandic_coords,
        "desc": (
            "Greenlandic/Danish Arctic sector — Greenland ice sheet mineral resources. "
            "Ice sheet melt opening new shipping routes and resource access. "
            "Greenland's strategic position between North America and Europe. "
            f"{approx} "
            f"See: {anchor}"
        ),
        "style": REFINED_STYLE_ARCTIC,
    })

    return zones


# --- 11. Desalination and Adaptation Infrastructure ---

def refine_desalination():
    """
    Desalination and Adaptation Infrastructure — point-based placemarks.

    Locations from climate.md narrative:
    - Desalination plants: Saudi Arabia, Israel/APR, UAE, California/Pacifica, Australia, Singapore
    - Coastal defenses: Netherlands, London Thames Barrier, Shanghai, New York Harbor

    Returns:
        list of zone dicts (point placemarks)
    """
    anchor = REFINED_ANCHORS["technology"]

    points = [
        {
            "zone_name": "Saudi Arabia — Desalination Hub",
            "coords": [(50.2, 26.4)],
            "desc": (
                "Major desalination plant cluster — Saudi Arabia's water supply "
                "is critically dependent on desalination. The world's largest "
                "desalination producer."
            ),
        },
        {
            "zone_name": "Israel / APR — Desalination",
            "coords": [(34.8, 32.6)],
            "desc": (
                "Advanced desalination infrastructure — Israel/APR operates "
                "some of the world's most efficient reverse-osmosis plants, "
                "supplying ~80% of domestic water."
            ),
        },
        {
            "zone_name": "UAE — Desalination",
            "coords": [(55.3, 25.2)],
            "desc": (
                "UAE desalination capacity — extensive thermal and reverse-osmosis "
                "desalination supporting urban and industrial water needs."
            ),
        },
        {
            "zone_name": "California/Pacifica — Desalination",
            "coords": [(-117.0, 33.0)],
            "desc": (
                "Pacifica desalination plants — drought-driven investment in "
                "coastal desalination infrastructure for Southern California."
            ),
        },
        {
            "zone_name": "Australia — Desalination",
            "coords": [(151.2, -33.8)],
            "desc": (
                "Australian desalination plants — Sydney and other major cities "
                "depend on desalination for drought security."
            ),
        },
        {
            "zone_name": "Singapore — Desalination",
            "coords": [(103.8, 1.3)],
            "desc": (
                "Singapore desalination and NEWater — advanced water recycling "
                "and desalination for water-independent city-state."
            ),
        },
        {
            "zone_name": "Netherlands — Coastal Defenses",
            "coords": [(4.3, 52.0)],
            "desc": (
                "Dutch Delta Works and North Sea protection — the world's most "
                "advanced sea defense system, continuously upgraded for 0.35m+ SLR."
            ),
        },
        {
            "zone_name": "London — Thames Barrier",
            "coords": [(0.0, 51.5)],
            "desc": (
                "Thames Barrier — London's primary flood defense. Regularly "
                "closed due to storm surge + sea level rise combination."
            ),
        },
        {
            "zone_name": "Shanghai — Coastal Defenses",
            "coords": [(121.5, 31.2)],
            "desc": (
                "Shanghai flood defense system — extensive sea walls and barriers "
                "protecting China's economic center from storm surge and SLR."
            ),
        },
        {
            "zone_name": "New York Harbor — Coastal Defenses",
            "coords": [(-74.0, 40.7)],
            "desc": (
                "New York Harbor storm surge barrier — post-Sandy investment "
                "in harbor-scale flood protection infrastructure."
            ),
        },
    ]

    zones = []
    for pt in points:
        full_desc = (
            f"{pt['desc']} "
            f"See: {anchor}"
        )
        zones.append({
            "name": "Desalination and Adaptation Infrastructure",
            "zone_name": pt["zone_name"],
            "coords": pt["coords"],
            "desc": full_desc,
            "style": REFINED_STYLE_DEFAULT,
            "is_point": True,
        })

    return zones


# --- Aggregator ---

REFINED_FUNCTIONS = [
    refine_arctic_permafrost,
    refine_greenland_ice,
    refine_glaciers,
    refine_sealevel,
    refine_heat,
    refine_fire,
    refine_sahel,
    refine_persian_gulf,
    refine_water_basins,
    refine_arctic_resources,
    refine_desalination,
]


def refine_all_placemarks(output_path="climate_refined.kml"):
    """
    Generate refined Climate folder with all 11 thematic placemarks upgraded
    from rough bounding boxes to accurate multi-polygon geometries.

    Each refine function returns zones with name, coords, description, and style.
    Multi-polygon placemarks get a Folder with per-zone Placemarks.
    Single-polygon placemarks get a Folder with one Placemark.
    Point placemarks use Point geometry with descriptive text.

    Args:
        output_path: Path for output KML file (default: climate_refined.kml).

    Returns:
        Path to generated KML file, or None if generation failed.
    """
    import simplekml
    from shapely.geometry import Point as ShapelyPoint

    kml = simplekml.Kml(name="Climate (Refined)")
    root_folder = kml.newfolder(name="Climate")

    total_placemarks = 0
    total_vertices = 0

    for refine_fn in REFINED_FUNCTIONS:
        fn_name = refine_fn.__name__
        log.info(f"Generating zones from {fn_name}...")

        zones = refine_fn()
        if not zones:
            log.warning(f"  {fn_name}: no zones returned")
            continue

        placemark_name = zones[0]["name"]

        if len(zones) == 1 and not zones[0].get("is_point"):
            # Single polygon placemark — create a folder with one polygon
            z = zones[0]
            zone_folder = root_folder.newfolder(name=placemark_name)
            poly_color, line_color, line_width = z["style"]

            coords_list = z["coords"]
            if len(coords_list) >= 4:
                kml_coords = [(x, y, 0) for x, y in coords_list]
                pm = zone_folder.newpolygon(
                    name=placemark_name,
                    description=z["desc"],
                    outerboundaryis=kml_coords,
                )
                pm.style.polystyle.color = poly_color
                pm.style.polystyle.outline = 1
                pm.style.linestyle.color = line_color
                pm.style.linestyle.width = line_width
                pm.altitudemode = simplekml.AltitudeMode.clamptoground
                total_placemarks += 1
                total_vertices += len(kml_coords)

        elif len(zones) >= 2 or zones[0].get("is_point"):
            # Multi-polygon or point placemark — create a folder
            multi_folder = root_folder.newfolder(name=placemark_name)

            for z in zones:
                poly_color, line_color, line_width = z["style"]
                zone_name = z["zone_name"] if z["zone_name"] else placemark_name

                if z.get("is_point"):
                    # Point placemark
                    lon, lat = z["coords"][0]
                    pm = multi_folder.newpoint(
                        name=zone_name,
                        description=z["desc"],
                        coords=[(lon, lat, 0)],
                    )
                    # Use a visible icon
                    pm.style.iconstyle.color = poly_color
                    pm.style.iconstyle.scale = 0.8
                    pm.altitudemode = simplekml.AltitudeMode.clamptoground
                    total_placemarks += 1
                else:
                    coords_list = z["coords"]
                    if len(coords_list) >= 4:
                        kml_coords = [(x, y, 0) for x, y in coords_list]
                        pm = multi_folder.newpolygon(
                            name=zone_name,
                            description=z["desc"],
                            outerboundaryis=kml_coords,
                        )
                        pm.style.polystyle.color = poly_color
                        pm.style.polystyle.outline = 1
                        pm.style.linestyle.color = line_color
                        pm.style.linestyle.width = line_width
                        pm.altitudemode = simplekml.AltitudeMode.clamptoground
                        total_placemarks += 1
                        total_vertices += len(kml_coords)

        else:
            log.warning(f"  {fn_name}: unexpected zone structure — skipping")

        log.info(
            f"  {fn_name}: {len(zones)} zones processed"
        )

    kml.save(output_path)
    file_size = os.path.getsize(output_path)
    log.info(
        f"Refined placemarks KML saved: {output_path} ({file_size:,} bytes, "
        f"{len(REFINED_FUNCTIONS)} placemark groups, "
        f"{total_placemarks} total zone placemarks, "
        f"{total_vertices} polygon vertices)"
    )

    return output_path if os.path.isfile(output_path) else None


# --- Sea Level Rise constants ---

SLR_REGIONS = [
    {
        "name": "Bangladesh Delta Inundation Zone",
        "bbox": (88, 93, 21, 24),
        "desc": "Ganges-Brahmaputra-Meghna delta — densely populated low-lying coastal zone",
    },
    {
        "name": "Mekong Delta Inundation Zone",
        "bbox": (105, 107, 8.5, 10.5),
        "desc": "Vietnam's Mekong Delta — primary rice-growing region, extreme flood risk",
    },
    {
        "name": "Nile Delta Inundation Zone",
        "bbox": (30, 32, 30, 31.5),
        "desc": "Egypt's Nile Delta fan — agricultural heartland and population center",
    },
    {
        "name": "US Gulf Coast Inundation Zone",
        "bbox": (-96, -88, 28, 31),
        "desc": "Houston to Mobile — hurricane-prone coastal urban corridor",
    },
    {
        "name": "Pacific Atolls Inundation Zone",
        "atolls": [
            ("Tuvalu", 179.2, -8.5),
            ("Kiribati", 173.0, 1.5),
            ("Marshall Islands", 171.0, 7.0),
            ("Maldives", 73.5, 3.0),
        ],
        "desc": "Low-lying atoll nations — maximum elevation <2m, extreme SLR vulnerability",
    },
    {
        "name": "Netherlands Inundation Zone",
        "bbox": (3, 8, 51, 54),
        "desc": "Dutch coastal zone — polder landscape already below sea level",
    },
]

SLR_MD_ANCHOR = "2050-snapshot/domains/climate.md#sea-level"

# --- Helper functions ---

def hex_to_kml_color(hex_color, alpha="80"):
    """
    Convert #RRGGBB to AARRGGBB KML color format.
    Matches the project convention used in climate.kml and entity-config.json.
    Alpha 80 = ~50% opacity (semi-transparent overlay).
    """
    hex_color = hex_color.lstrip("#")
    return f"{alpha}{hex_color}"


def make_description(subtype_code):
    """Build the KML description with cross-reference."""
    full_name = KOPPEN_FULL_NAMES.get(subtype_code, subtype_code)
    return (
        f"Köppen-Geiger climate zone: {subtype_code} ({full_name})"
        f" — 2050 projection under SSP3-7.0."
        f" See: {CLIMATE_MD_ANCHOR}"
    )


def koppen_type_sorter_key(code):
    """
    Return a stable ordering key for Köppen codes.
    Groups: A=0, B=1, C=2, D=3, E=4, then index within group.
    """
    group_order = {c: i for i, codes in enumerate(KOPPEN_GROUPS.values()) for c in codes}
    return group_order.get(code, 99)


# --- Fallback generation (when GeoTIFF unavailable) ---

def create_fallback_polygons(code):
    """
    Create approximate latitudinal-band polygon(s) for a Köppen sub-type.
    Used when the real GloH2O GeoTIFF is not available.

    Returns list of (lon, lat) exterior ring coordinate lists.
    Each sub-type within a group gets a longitudinal slice to avoid
    all subtypes overlapping identically.
    """
    from shapely.geometry import Polygon

    # Collect all subtypes in the same group as this code
    all_in_group = []
    for group_codes in KOPPEN_GROUPS.values():
        if code in group_codes:
            all_in_group = sorted(group_codes)
            break

    if not all_in_group:
        return []

    idx = all_in_group.index(code)
    n = len(all_in_group)

    # Assign each subtype a longitudinal slice of the global band
    slice_width = 360.0 / n
    lon_start = -180.0 + idx * slice_width
    lon_end = lon_start + slice_width

    # Set latitude bounds based on climate group
    first_letter = code[0]
    if first_letter == "A":
        lat_min, lat_max = -15, 15
    elif first_letter == "B":
        lat_min, lat_max = 15, 38
    elif first_letter == "C":
        lat_min, lat_max = 30, 55
    elif first_letter == "D":
        lat_min, lat_max = 45, 65
    elif first_letter == "E":
        if code == "ET":
            lat_min, lat_max = 60, 72  # Tundra (land masses extend this far north)
        else:
            lat_min, lat_max = 72, 85  # Ice cap
    else:
        return []

    # Build the ring: counterclockwise for exterior
    ring = [
        (lon_end, lat_min),
        (lon_end, lat_max),
        (lon_start, lat_max),
        (lon_start, lat_min),
        (lon_end, lat_min),  # close
    ]
    return [ring]


def generate_fallback_koppen_kml(script_dir):
    """
    Generate approximate Köppen zones using latitudinal-band fallback.
    Called when the GeoTIFF source data is unavailable.
    """
    log.info("GeoTIFF not found — generating approximate fallback Köppen layer")
    log.info("NOTE: Fallback uses latitudinal-band approximations from climate.md narrative")
    log.info("      Replace with real GeoTIFF data when source becomes available")

    from shapely.geometry import Polygon

    subtype_polygons = defaultdict(list)
    total_vertices = 0
    total_polygons = 0

    for code in ALL_KOPPEN_CODES:
        rings = create_fallback_polygons(code)
        for ring in rings:
            if len(ring) < 4:
                continue
            poly = Polygon(ring)
            if poly.is_empty or not poly.is_valid:
                continue
            subtype_polygons[code].append(poly)
            total_polygons += 1
            total_vertices += len(ring)

    log.info(
        f"Fallback generated {total_polygons} polygons "
        f"({total_vertices} total vertices) across {len(subtype_polygons)} sub-types"
    )

    return subtype_polygons


# --- GeoTIFF-based generation ---

def generate_from_geotiff(geotiff_path, script_dir):
    """
    Generate Köppen zones from GloH2O V3 2041-2070 SSP3-7.0 GeoTIFF.
    Polygonizes contiguous zones of the same class, simplifies geometry,
    and organizes into the KML hierarchy.

    Per T-21-04: Validates simplified polygons for self-intersection via
    shapely.is_valid before writing KML.
    Per T-21-05: Prints histogram of raster values before mapping.
    """
    import rasterio
    from rasterio.features import shapes
    from shapely.geometry import shape as shp_shape
    from shapely.ops import unary_union

    log.info(f"Reading GeoTIFF: {geotiff_path}")

    with rasterio.open(geotiff_path) as src:
        band = src.read(1)
        transform = src.transform
        crs = src.crs

        log.info(f"  Raster shape: {band.shape}, CRS: {crs}")

        # Print value histogram (T-21-05)
        unique, counts = Counter(band[band != src.nodata]).most_common()
        if not unique:
            unique, counts = Counter(band.flatten()).most_common()

        log.info(f"  Unique pixel values found: {len(unique)}")
        for val, cnt in unique[:35]:
            code = RASTER_LEGEND.get(val, "UNKNOWN")
            log.info(f"    Value {val:3d} ({code:>4s}): {cnt:>10,d} pixels")

        # Polygonize: convert raster zones to vector polygons
        log.info("  Polygonizing raster zones...")
        results = (
            (shp_shape(geom).simplify(0.02, preserve_topology=True), value)
            for geom, value in shapes(band, mask=band != src.nodata, transform=transform)
        )

        # Group polygons by Köppen sub-type code
        subtype_polygons = defaultdict(list)
        total_raw_count = 0
        total_simplified_count = 0
        total_simplified_vertices = 0

        for poly, value in results:
            total_raw_count += 1
            code = RASTER_LEGEND.get(int(value))
            if code is None:
                continue

            # Douglas-Peucker simplification (D-16 convention, 0.02° ~2.2km)
            simplified = poly.simplify(0.02, preserve_topology=True)

            # T-21-04: Validate simplified polygon
            if simplified.is_empty:
                continue
            if simplified.geom_type == "Polygon":
                if simplified.exterior is None or len(simplified.exterior.coords) < 4:
                    continue
                if not simplified.is_valid:
                    repaired = simplified.buffer(0)
                    if repaired.is_empty or not repaired.is_valid:
                        continue
                    simplified = repaired
                subtype_polygons[code].append(simplified)
                total_simplified_count += 1
                total_simplified_vertices += len(simplified.exterior.coords)
            elif simplified.geom_type == "MultiPolygon":
                for part in simplified.geoms:
                    if not part.is_empty and part.is_valid and len(part.exterior.coords) >= 4:
                        subtype_polygons[code].append(part)
                        total_simplified_count += 1
                        total_simplified_vertices += len(part.exterior.coords)

        log.info(
            f"  Polygonization: {total_raw_count} raw → "
            f"{total_simplified_count} valid simplified polygons "
            f"({total_simplified_vertices} vertices)"
        )

        # Report per sub-type counts
        for code in sorted(subtype_polygons, key=koppen_type_sorter_key):
            poly_count = len(subtype_polygons[code])
            vertex_count = sum(
                len(p.exterior.coords) if p.geom_type == "Polygon"
                else sum(len(part.exterior.coords) for part in p.geoms)
                for p in subtype_polygons[code]
            )
            log.info(f"    {code} ({KOPPEN_FULL_NAMES[code]}): {poly_count} polygons, {vertex_count} vertices")

        # Report missing sub-types
        present_codes = set(subtype_polygons.keys())
        missing = set(ALL_KOPPEN_CODES) - present_codes
        if missing:
            log.warning(f"  Missing sub-types (no polygons found): {sorted(missing)}")

        return subtype_polygons


# --- KML building ---

def build_koppen_kml(subtype_polygons, output_path):
    """
    Build the Köppen KML structure using simplekml.

    Structure:
    - Root folder: "Köppen-Geiger Climate Classification (2050)"
      - A — Tropical Climates
        - Af folder → placemarks
        - Am folder → placemarks
        - Aw folder → placemarks
      - B — Arid Climates
        - ...
      - C — Temperate Climates
      - D — Continental Climates
      - E — Polar Climates
    """
    import simplekml

    kml = simplekml.Kml(name="Köppen-Geiger Climate Classification (2050)")
    koppen_root = kml.newfolder(name="Köppen-Geiger Climate Classification (2050)")

    # Build group folders
    group_folders = {}
    for group_name in KOPPEN_GROUPS:
        gf = koppen_root.newfolder(name=group_name)
        group_folders[group_name] = gf

    total_placemarks = 0
    total_vertices = 0

    # Iterate groups in order, then subtypes within groups
    for group_name, subtype_codes in KOPPEN_GROUPS.items():
        group_folder = group_folders[group_name]

        for code in subtype_codes:
            polygons = subtype_polygons.get(code, [])

            if not polygons:
                # Create a placeholder folder with note (not a polygon to avoid empty geometry)
                subtype_folder = group_folder.newfolder(name=code)
                note_pm = subtype_folder.newpoint(
                    name=f"{code} — {KOPPEN_FULL_NAMES.get(code, '')}",
                    description=(
                        f"{code} — No polygon data available for "
                        f"this Köppen sub-type in the current source. "
                        f"See: {CLIMATE_MD_ANCHOR}"
                    ),
                    coords=[(0, 0)],  # off-map placeholder, not a geographic polygon
                )
                note_pm.style.iconstyle.icon.href = ""
                note_pm.style.iconstyle.color = "00000000"  # invisible
                continue

            subtype_folder = group_folder.newfolder(name=code)

            # Set default style for this subtype — applies to all contained placemarks
            hex_color = KOPPEN_COLORS.get(code, "#CCCCCC")
            poly_color = hex_to_kml_color(hex_color, alpha="80")
            line_color = hex_to_kml_color(hex_color, alpha="FF")

            for poly in polygons:
                if poly.is_empty:
                    continue

                if poly.geom_type == "Polygon":
                    coords_list = list(poly.exterior.coords)
                    if len(coords_list) < 4:
                        continue

                    # Convert to (lon, lat, 0) format for simplekml
                    kml_coords = [(x, y, 0) for x, y in coords_list]

                    pm = subtype_folder.newpolygon(
                        name=f"{code}",
                        description=make_description(code),
                        outerboundaryis=kml_coords,
                    )
                    pm.style.polystyle.color = poly_color
                    pm.style.polystyle.outline = 1
                    pm.style.linestyle.color = line_color
                    pm.style.linestyle.width = 0.5
                    pm.altitudemode = simplekml.AltitudeMode.clamptoground

                    total_placemarks += 1
                    total_vertices += len(kml_coords)

                elif poly.geom_type == "MultiPolygon":
                    for part in poly.geoms:
                        if part.is_empty:
                            continue
                        coords_list = list(part.exterior.coords)
                        if len(coords_list) < 4:
                            continue
                        kml_coords = [(x, y, 0) for x, y in coords_list]

                        pm = subtype_folder.newpolygon(
                            name=f"{code}",
                            description=make_description(code),
                            outerboundaryis=kml_coords,
                        )
                        pm.style.polystyle.color = poly_color
                        pm.style.polystyle.outline = 1
                        pm.style.linestyle.color = line_color
                        pm.style.linestyle.width = 0.5
                        pm.altitudemode = simplekml.AltitudeMode.clamptoground

                        total_placemarks += 1
                        total_vertices += len(kml_coords)

    log.info(
        f"KML built: {total_placemarks} placemarks, "
        f"{total_vertices} vertices across {len(subtype_polygons)} sub-types"
    )

    kml.save(output_path)
    file_size = os.path.getsize(output_path)
    log.info(f"Written: {output_path} ({file_size:,} bytes)")

    return kml


# --- Main public API ---

def generate_koppen_kml(output_path="climate_koppen.kml"):
    """
    Main entry point for generating the Köppen-Geiger KML layer.

    Args:
        output_path: Path for output KML file (default: climate_koppen.kml).

    Returns:
        Path to the generated KML file, or None if generation failed.
    """
    # Determine paths relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    geotiff_path = os.path.join(script_dir, "source", "koppen_2041-2070_ssp370.tif")

    if not os.path.isfile(geotiff_path):
        log.warning(
            f"Köppen source GeoTIFF not found at {geotiff_path}.\n"
            f"  Download from GloH2O V3 figshare (DOI 10.6084/m9.figshare.21789074)\n"
            f"  or run download-data.py from Plan 01.\n"
            f"  Falling back to approximate latitudinal-band approximation."
        )
        subtype_polygons = generate_fallback_koppen_kml(script_dir)
        if not subtype_polygons:
            log.error("Fallback generation produced no polygons — aborting")
            return None
        build_koppen_kml(subtype_polygons, output_path)
        return output_path if os.path.isfile(output_path) else None

    try:
        subtype_polygons = generate_from_geotiff(geotiff_path, script_dir)
        if not subtype_polygons:
            log.error("GeoTIFF polygonization produced no polygons — aborting")
            return None
        build_koppen_kml(subtype_polygons, output_path)
        return output_path if os.path.isfile(output_path) else None
    except Exception as e:
        log.error(f"GeoTIFF processing failed: {e}")
        log.info("Falling back to approximate latitudinal-band polygons...")
        subtype_polygons = generate_fallback_koppen_kml(script_dir)
        if not subtype_polygons:
            log.error("Fallback generation also failed")
            return None
        build_koppen_kml(subtype_polygons, output_path)
        return output_path if os.path.isfile(output_path) else None


# --- Ecological Biomes generation ---

def generate_biomes_kml(output_path="climate_biomes.kml"):
    """
    Generate the Ecological Biomes (2050) KML layer.

    Approach A (data-driven per D-05):
        1. Read WWF Terrestrial Ecoregions from source/wwf_ecoregions/ using fiona
        2. Reclassify WWF biome types into our 6 target classes
        3. Merge and simplify polygons per class

    Approach B (fallback — narrative-derived from climate.md):
        Create approximate geographic bounding polygons for each biome type.

    Output: climate_biomes.kml — containing only the biomes folder for later merge.

    Returns:
        Path to generated KML file, or None if generation failed.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wwf_path = os.path.join(script_dir, "source", "wwf_ecoregions", "wwf_terrestrial_ecoregions.shp")

    if os.path.isfile(wwf_path):
        log.info(f"WWF ecoregions found at {wwf_path}")
        _generate_biomes_from_wwf(wwf_path, output_path)
    else:
        log.warning(
            f"WWF ecoregions shapefile not found at {wwf_path}.\n"
            f"  Download from: https://www.worldwildlife.org/publications/"
            f"terrestrial-ecoregions-of-the-world\n"
            f"  Place in: source/wwf_ecoregions/\n"
            f"  Falling back to narrative-derived approximate polygons."
        )
        _generate_biomes_fallback(output_path)

    return output_path if os.path.isfile(output_path) else None


def _generate_biomes_from_wwf(wwf_path, output_path):
    """
    Data-driven biomes generation from WWF Terrestrial Ecoregions.

    Reads shapefile with fiona, reclassifies biome types, merges and
    simplifies polygons, writes styled KML with simplekml.
    """
    import fiona
    from shapely.geometry import shape as shp_shape
    from shapely.ops import unary_union

    log.info(f"Reading WWF ecoregions: {wwf_path}")

    reclassified = defaultdict(list)

    with fiona.open(wwf_path) as src:
        for feature in src:
            props = feature["properties"]
            # Try multiple possible field names for WWF biome type
            wwf_biome = (
                props.get("BIOME_NAME")
                or props.get("BIOME")
                or props.get("biome_name")
                or props.get("biome")
            )
            if wwf_biome not in BIOME_RECLASSIFICATION:
                continue

            target_class = BIOME_RECLASSIFICATION[wwf_biome]
            geom = shp_shape(feature["geometry"])
            simplified = geom.simplify(0.02, preserve_topology=True)
            if not simplified.is_empty and simplified.is_valid:
                reclassified[target_class].append(simplified)

    # Merge polygons per target class (dissolve by biome type)
    import simplekml

    merged = {}
    for target_class, polygons in reclassified.items():
        if not polygons:
            continue
        merged[target_class] = unary_union(polygons)
        log.info(f"  {target_class}: {len(polygons)} ecoregions merged")

    populated = {k: v for k, v in merged.items() if not v.is_empty}
    log.info(f"Reclassified into {len(populated)} target biome types")
    missing = set(BIOME_COLORS) - set(populated)
    if missing:
        log.warning(f"Biomes with no data: {missing}")

    # Build KML
    kml = simplekml.Kml(name="Ecological Biomes (2050)")
    root_folder = kml.newfolder(name="Ecological Biomes (2050)")

    for biome_name in BIOME_COLORS:
        if biome_name not in populated:
            continue

        bf = root_folder.newfolder(name=biome_name)
        hex_color = BIOME_COLORS[biome_name]
        poly_color = hex_to_kml_color(hex_color, alpha="60")
        line_color = hex_to_kml_color(hex_color, alpha="FF")

        merged_geom = populated[biome_name]
        if merged_geom.geom_type == "Polygon":
            polygons_to_write = [merged_geom]
        elif merged_geom.geom_type == "MultiPolygon":
            polygons_to_write = list(merged_geom.geoms)
        else:
            continue

        for poly in polygons_to_write:
            if len(poly.exterior.coords) < 4:
                continue
            kml_coords = [(x, y, 0) for x, y in poly.exterior.coords]
            pm = bf.newpolygon(
                name=biome_name,
                description=(
                    f"Ecological biome zone — 2050 projection. "
                    f"See: {BIOMES_MD_ANCHOR}"
                ),
                outerboundaryis=kml_coords,
            )
            pm.style.polystyle.color = poly_color
            pm.style.polystyle.outline = 1
            pm.style.linestyle.color = line_color
            pm.style.linestyle.width = 0.5
            pm.altitudemode = simplekml.AltitudeMode.clamptoground

    kml.save(output_path)
    file_size = os.path.getsize(output_path)
    log.info(f"WWF-derived biomes KML saved: {output_path} ({file_size:,} bytes)")
    return kml


def _generate_biomes_fallback(output_path):
    """
    Generate approximate biome polygons from climate.md narrative descriptions.

    Per D-05 discretion: uses narrative-derived approximate geographic polygons
    when WWF ecoregions source data is unavailable.

    Per T-21-09: Fallback polygons marked as APPROXIMATE in description.
    """
    import simplekml
    from shapely.geometry import Polygon

    log.info("Generating fallback biome polygons from climate.md narrative")

    # Approximate geographic extent polygons for each of the 6 biome types.
    # Derived from known global biome distributions described in climate.md.
    biome_regions = {
        "Tundra": [
            # Arctic fringe: 65°N+ around the globe (northern coasts and islands)
            Polygon([(-180, 65), (180, 65), (180, 85), (-180, 85), (-180, 65)]),
        ],
        "Boreal Forest/Taiga": [
            # Northern band: 50-65°N across North America and Eurasia
            Polygon([(-170, 50), (-55, 50), (-55, 65), (-170, 65), (-170, 50)]),  # Alaska/Canada
            Polygon([(-15, 50), (180, 50), (180, 65), (-15, 65), (-15, 50)]),   # Scandinavia/Russia
        ],
        "Temperate Forest": [
            # Eastern North America (30-50°N)
            Polygon([(-100, 30), (-55, 30), (-55, 50), (-100, 50), (-100, 30)]),
            # Western/Central Europe (35-55°N)
            Polygon([(-10, 35), (35, 35), (35, 55), (-10, 55), (-10, 35)]),
            # Eastern Asia (25-50°N)
            Polygon([(100, 25), (145, 25), (145, 50), (100, 50), (100, 25)]),
            # SE Australia / New Zealand (25-47°S)
            Polygon([(140, -47), (180, -47), (180, -25), (140, -25), (140, -47)]),
            # Southern Chile / Argentina (35-56°S)
            Polygon([(-76, -56), (-64, -56), (-64, -35), (-76, -35), (-76, -56)]),
        ],
        "Grassland/Savanna": [
            # Sahel transition zone (8-18°N across Africa)
            Polygon([(-18, 8), (40, 8), (40, 18), (-18, 18), (-18, 8)]),
            # East African savanna (5°S-5°N)
            Polygon([(28, -5), (42, -5), (42, 5), (28, 5), (28, -5)]),
            # Central Asian steppe (40-55°N)
            Polygon([(50, 40), (90, 40), (90, 55), (50, 55), (50, 40)]),
            # North American Great Plains (28-52°N)
            Polygon([(-105, 28), (-95, 28), (-95, 52), (-105, 52), (-105, 28)]),
            # South American Pampas (25-40°S)
            Polygon([(-65, -40), (-55, -40), (-55, -25), (-65, -25), (-65, -40)]),
        ],
        "Desert": [
            # Sahara (18-35°N, North Africa)
            Polygon([(-18, 18), (40, 18), (40, 35), (-18, 35), (-18, 18)]),
            # Arabian Peninsula (12-32°N)
            Polygon([(35, 12), (60, 12), (60, 32), (35, 32), (35, 12)]),
            # Gobi / Central Asian deserts (40-48°N)
            Polygon([(85, 40), (115, 40), (115, 48), (85, 48), (85, 40)]),
            # Australian interior (18-35°S)
            Polygon([(115, -35), (150, -35), (150, -18), (115, -18), (115, -35)]),
            # Kalahari / Namib (18-30°S)
            Polygon([(12, -30), (30, -30), (30, -18), (12, -18), (12, -30)]),
            # Atacama / Patagonia (24-52°S)
            Polygon([(-75, -52), (-65, -52), (-65, -24), (-75, -24), (-75, -52)]),
        ],
        "Tropical Rainforest": [
            # Amazon basin (15°S-5°N)
            Polygon([(-82, -15), (-45, -15), (-45, 5), (-82, 5), (-82, -15)]),
            # Congo basin (8°S-6°N)
            Polygon([(8, -8), (32, -8), (32, 6), (8, 6), (8, -8)]),
            # Southeast Asia / Indonesia (12°S-12°N)
            Polygon([(95, -12), (150, -12), (150, 12), (95, 12), (95, -12)]),
            # Central America / Caribbean (5-18°N)
            Polygon([(-92, 5), (-78, 5), (-78, 18), (-92, 18), (-92, 5)]),
        ],
    }

    kml = simplekml.Kml(name="Ecological Biomes (2050)")
    root_folder = kml.newfolder(name="Ecological Biomes (2050)")

    total_placemarks = 0
    total_vertices = 0
    fallback_note = (
        "APPROXIMATE — Replace with data-driven polygons when WWF "
        "T errestrial Ecoregions source becomes available."
    )

    for biome_name in BIOME_COLORS:
        regions = biome_regions.get(biome_name, [])
        if not regions:
            continue

        bf = root_folder.newfolder(name=biome_name)
        hex_color = BIOME_COLORS[biome_name]
        poly_color = hex_to_kml_color(hex_color, alpha="60")
        line_color = hex_to_kml_color(hex_color, alpha="FF")

        for poly in regions:
            coords_list = list(poly.exterior.coords)
            kml_coords = [(x, y, 0) for x, y in coords_list]

            pm = bf.newpolygon(
                name=biome_name,
                description=(
                    f"{BIOME_NAMES.get(biome_name, biome_name)} — 2050 projection. "
                    f"{fallback_note} "
                    f"See: {BIOMES_MD_ANCHOR}"
                ),
                outerboundaryis=kml_coords,
            )
            pm.style.polystyle.color = poly_color
            pm.style.polystyle.outline = 1
            pm.style.linestyle.color = line_color
            pm.style.linestyle.width = 0.5
            pm.altitudemode = simplekml.AltitudeMode.clamptoground

            total_placemarks += 1
            total_vertices += len(kml_coords)

    kml.save(output_path)
    file_size = os.path.getsize(output_path)
    log.info(
        f"Biomes KML saved: {output_path} ({file_size:,} bytes, "
        f"{total_placemarks} placemarks, {total_vertices} vertices)"
    )
    return kml


# --- Sea Level Rise Inundation generation ---

def generate_slr_kml(output_path="climate_slr.kml"):
    """
    Generate the Sea Level Rise Inundation (0.35m) KML layer.

    Approach A (data-driven per D-05):
        1. For each SLR target region, open DEM tiles from source/dem_tiles/
        2. Mask to elevation <= 0.35m within bounding box
        3. Polygonize masked area using rasterio.features.shapes()
        4. Simplify polygons

    Approach B (fallback — narrative-derived from climate.md):
        Create approximate coastal inundation polygons for each region.

    Output: climate_slr.kml — containing only the SLR folder for later merge.

    Returns:
        Path to generated KML file, or None if generation failed.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dem_dir = os.path.join(script_dir, "source", "dem_tiles")

    if os.path.isdir(dem_dir) and any(f.endswith((".tif", ".tiff")) for f in os.listdir(dem_dir)):
        log.info(f"DEM tiles found in {dem_dir}")
        _generate_slr_from_dem(dem_dir, output_path)
    else:
        log.warning(
            f"DEM tiles not found in {dem_dir}.\n"
            f"  Download SRTM or COP30 tiles for each SLR target region.\n"
            f"  Falling back to narrative-derived approximate polygons."
        )
        _generate_slr_fallback(output_path)

    return output_path if os.path.isfile(output_path) else None


def _generate_slr_from_dem(dem_dir, output_path):
    """
    Data-driven SLR inundation generation from DEM tiles.

    Reads DEM tiles with rasterio for each SLR target region,
    extracts elevation <= 0.35m zones, polygonizes and simplifies.
    """
    import rasterio
    from rasterio.features import shapes as rio_shapes
    from shapely.geometry import shape as shp_shape
    from shapely.ops import unary_union

    log.info(f"Processing DEM tiles from {dem_dir}")
    import simplekml

    kml = simplekml.Kml(name="Sea Level Rise Inundation (0.35m)")
    root_folder = kml.newfolder(name="Sea Level Rise Inundation (0.35m)")

    slr_poly_color = "6055b0b0"
    slr_line_color = "ff55b0b0"

    dem_files = sorted([
        os.path.join(dem_dir, f)
        for f in os.listdir(dem_dir)
        if f.endswith((".tif", ".tiff"))
    ])

    total_placemarks = 0

    for region in SLR_REGIONS:
        if "bbox" not in region:
            continue

        min_lon, max_lon, min_lat, max_lat = region["bbox"]
        region_polygons = []

        for dem_path in dem_files:
            try:
                with rasterio.open(dem_path) as src:
                    # Crop to bounding box
                    window = src.window(min_lon, min_lat, max_lon, max_lat)
                    if window.col_off is None or window.row_off is None:
                        continue

                    band = src.read(1, window=window)
                    transform = src.window_transform(window)

                    # Mask for elevation <= 0.35m
                    mask = (band <= 0.35) & (band != src.nodata)

                    if not mask.any():
                        continue

                    # Polygonize
                    for geom, val in rio_shapes(
                        mask.astype("uint8"),
                        mask=mask,
                        transform=transform,
                    ):
                        if val != 1:
                            continue
                        poly = shp_shape(geom)
                        simplified = poly.simplify(0.005, preserve_topology=True)
                        if not simplified.is_empty and simplified.is_valid:
                            region_polygons.append(simplified)

            except Exception as e:
                log.warning(f"  Error processing {os.path.basename(dem_path)}: {e}")
                continue

        if region_polygons:
            merged = unary_union(region_polygons)
            log.info(f"  {region['name']}: {len(region_polygons)} polygons merged")

            if merged.geom_type == "Polygon":
                polygons_to_write = [merged]
            elif merged.geom_type == "MultiPolygon":
                polygons_to_write = list(merged.geoms)
            else:
                continue

            for poly in polygons_to_write:
                if len(poly.exterior.coords) < 4:
                    continue
                kml_coords = [(x, y, 0) for x, y in poly.exterior.coords]
                pm = root_folder.newpolygon(
                    name=region["name"],
                    description=(
                        f"Sea level rise inundation zone (+0.35m by 2050). "
                        f"{region['desc']} "
                        f"See: {SLR_MD_ANCHOR}"
                    ),
                    outerboundaryis=kml_coords,
                )
                pm.style.polystyle.color = slr_poly_color
                pm.style.polystyle.outline = 1
                pm.style.linestyle.color = slr_line_color
                pm.style.linestyle.width = 0.5
                pm.altitudemode = simplekml.AltitudeMode.clamptoground
                total_placemarks += 1
        else:
            log.warning(f"  {region['name']}: no inundation polygons found from DEM")
            # Create placeholder with note
            note_pm = root_folder.newpoint(
                name=region["name"],
                description=(
                    f"Sea level rise inundation zone (+0.35m by 2050). "
                    f"No DEM-derived polygons available for this region. "
                    f"{region['desc']} "
                    f"See: {SLR_MD_ANCHOR}"
                ),
                coords=[(0, 0)],
            )
            note_pm.style.iconstyle.icon.href = ""
            note_pm.style.iconstyle.color = "00000000"

    kml.save(output_path)
    file_size = os.path.getsize(output_path)
    log.info(f"DEM-derived SLR KML saved: {output_path} ({file_size:,} bytes, {total_placemarks} placemarks)")
    return kml


def _generate_slr_fallback(output_path):
    """
    Generate approximate SLR inundation polygons from climate.md narrative.

    Per D-05 discretion: uses narrative-derived approximate geographic polygons
    when DEM source data is unavailable.
    Per T-21-08: +0.35m is a global mean; local effects vary — noted as approximate.
    Per T-21-09: Fallback polygons marked as APPROXIMATE in description.
    """
    import simplekml
    from shapely.geometry import Polygon, box

    log.info("Generating fallback SLR inundation polygons from climate.md narrative")

    kml = simplekml.Kml(name="Sea Level Rise Inundation (0.35m)")
    root_folder = kml.newfolder(name="Sea Level Rise Inundation (0.35m)")

    # Semi-transparent teal matching entity-config.json climate-overlay convention
    # lineColor: ff55b0b0, polyColor: 4055b0b0 — but with 60 alpha for more visibility
    slr_poly_color = "6055b0b0"
    slr_line_color = "ff55b0b0"

    total_placemarks = 0
    fallback_note = (
        "APPROXIMATE — Replace with DEM-derived polygon when elevation "
        "source data becomes available. +0.35m is a global mean; local "
        "effects vary due to subsidence, tides, and storm surge."
    )

    for region in SLR_REGIONS:
        name = region["name"]

        if "bbox" in region:
            min_lon, max_lon, min_lat, max_lat = region["bbox"]
            poly = box(min_lon, min_lat, max_lon, max_lat)
            coords_list = list(poly.exterior.coords)
            kml_coords = [(x, y, 0) for x, y in coords_list]

            pm = root_folder.newpolygon(
                name=name,
                description=(
                    f"Sea level rise inundation zone (+0.35m by 2050). "
                    f"{fallback_note} "
                    f"{region['desc']} "
                    f"See: {SLR_MD_ANCHOR}"
                ),
                outerboundaryis=kml_coords,
            )
            pm.style.polystyle.color = slr_poly_color
            pm.style.polystyle.outline = 1
            pm.style.linestyle.color = slr_line_color
            pm.style.linestyle.width = 0.5
            pm.altitudemode = simplekml.AltitudeMode.clamptoground
            total_placemarks += 1

        elif "atolls" in region:
            for atoll_name, atoll_lon, atoll_lat in region["atolls"]:
                # Small bounding box (~2km²) around each atoll
                buffer = 0.02  # ~2km at equator
                poly = box(atoll_lon - buffer, atoll_lat - buffer,
                          atoll_lon + buffer, atoll_lat + buffer)
                coords_list = list(poly.exterior.coords)
                kml_coords = [(x, y, 0) for x, y in coords_list]

                pm = root_folder.newpolygon(
                    name=f"{name} — {atoll_name}",
                    description=(
                        f"Sea level rise inundation zone (+0.35m by 2050). "
                        f"{fallback_note} "
                        f"{region['desc']} "
                        f"See: {SLR_MD_ANCHOR}"
                    ),
                    outerboundaryis=kml_coords,
                )
                pm.style.polystyle.color = slr_poly_color
                pm.style.polystyle.outline = 1
                pm.style.linestyle.color = slr_line_color
                pm.style.linestyle.width = 0.5
                pm.altitudemode = simplekml.AltitudeMode.clamptoground
                total_placemarks += 1

    kml.save(output_path)
    file_size = os.path.getsize(output_path)
    log.info(
        f"SLR KML saved: {output_path} ({file_size:,} bytes, "
        f"{total_placemarks} placemarks)"
    )
    return kml


def main():
    """CLI entry point.

    Usage:
        python generate-climate-layers.py                    # Generate Köppen layer
        python generate-climate-layers.py --biomes           # Generate Biomes layer
        python generate-climate-layers.py --slr              # Generate SLR layer
        python generate-climate-layers.py --refine           # Generate refined placemarks
    """
    if "--refine" in sys.argv:
        result = refine_all_placemarks()
        if result:
            print(f"Refined placemarks KML generated: {result}")
        else:
            print("Failed to generate refined placemarks KML")
            sys.exit(1)
    elif "--biomes" in sys.argv:
        result = generate_biomes_kml()
        if result:
            print(f"Biomes KML generated: {result}")
        else:
            print("Failed to generate biomes KML")
            sys.exit(1)
    elif "--slr" in sys.argv:
        result = generate_slr_kml()
        if result:
            print(f"SLR KML generated: {result}")
        else:
            print("Failed to generate SLR KML")
            sys.exit(1)
    else:
        # Default behavior: generate Köppen layer
        output_path = "climate_koppen.kml"
        if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
            output_path = sys.argv[1]

        result = generate_koppen_kml(output_path)
        if result:
            print(f"Köppen KML generated: {result}")
        else:
            print("Failed to generate Köppen KML")
            sys.exit(1)


if __name__ == "__main__":
    main()
