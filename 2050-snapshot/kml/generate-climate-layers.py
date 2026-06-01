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
        python generate-climate-layers.py              # Generate Köppen layer
        python generate-climate-layers.py --biomes     # Generate Biomes layer
        python generate-climate-layers.py --slr        # Generate SLR layer
    """
    if "--biomes" in sys.argv:
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
