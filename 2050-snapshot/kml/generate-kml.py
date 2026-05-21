#!/usr/bin/env python3
"""
2050 KML Map Generator

Generates six 2050 STEEP-domain KML files from county-level US boundaries +
country-level global boundaries by merging polygons per entity-config.json definitions.

Per D-19: Programmatic generation with user refinement.
Per D-02: Geographic hierarchy within files (Continent > Subregion > Entity).
Per D-05: KML format (not KMZ).
Per D-16: Douglas-Peucker simplification at ~5-20km vertex spacing.
Per D-14: Narrative-derived boundaries via county-level merging.

Outputs:
  - borders.kml: Complete world entity polygons
  - climate.kml: Climate overlay placemarks
  - technology.kml: Technology overlay placemarks
  - economy.kml: Economy overlay placemarks
  - demographics.kml: Demographics overlay placemarks (entity copies only)
  - culture.kml: Culture overlay placemarks (entity copies only)
"""

import json
import os
import re
import sys
from lxml import etree
from shapely.geometry import shape, MultiPolygon, Polygon, Point
from shapely.ops import unary_union

# Config
CONFIG_PATH = "entity-config.json"
SOURCE_DIR = "source"
OUTPUT_DIR = "."  # Output to same directory as script

# KML namespace
NS = "http://www.opengis.net/kml/2.2"
NS_GX = "http://www.google.com/kml/ext/2.2"
NSMAP = {
    None: NS,
    "gx": NS_GX,
    "kml": NS,
}
KML_ATOM = "http://www.w3.org/2005/Atom"


def load_config():
    """Load entity-config.json (single source of truth for all entity data)."""
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_PATH)
    with open(config_path) as f:
        return json.load(f)


def read_county_kml(path):
    """
    Read US county KML, return {county_identifier: dict} mapping.
    
    The Census TIGER/Line KML has:
    - <name>CountyName</name> (short name, e.g., "Brooks")
    - ExtendedData > SchemaData > SimpleData with fields:
      - STATEFP (2-digit FIPS code, e.g., "13")
      - STUSPS (state abbreviation, e.g., "GA")
      - NAMELSAD (full name, e.g., "Brooks County")
    
    Returns dict keyed by "STUSPS|county_name" with geometry, state FIPS, and county name.
    """
    tree = etree.parse(path)
    root = tree.getroot()
    
    placemarks = root.findall(".//kml:Placemark", NSMAP)
    
    county_data = {}
    for pm in placemarks:
        name_el = pm.find("kml:name", NSMAP)
        if name_el is None or not name_el.text:
            continue
        
        county_name = name_el.text.strip()
        
        # Extract ExtendedData fields
        state_fips = None
        state_usps = None
        
        ext_data = pm.find("kml:ExtendedData", NSMAP)
        if ext_data is not None:
            schema_data = ext_data.find("kml:SchemaData", NSMAP)
            if schema_data is not None:
                for sd in schema_data.findall("kml:SimpleData", NSMAP):
                    field_name = sd.get("name", "")
                    if field_name == "STATEFP" and sd.text:
                        state_fips = sd.text.strip()
                    elif field_name == "STUSPS" and sd.text:
                        state_usps = sd.text.strip()
        
        if not state_usps or not state_fips:
            continue
        
        # Get polygon geometry
        polygon_el = pm.find(".//kml:Polygon", NSMAP)
        if polygon_el is None:
            continue
        
        geom = parse_kml_polygon(polygon_el)
        if geom is None:
            continue
        
        key = f"{state_usps}|{county_name}"
        county_data[key] = {
            "geometry": geom,
            "state_fips": state_fips,
            "state_usps": state_usps,
            "county_name": county_name,
        }
    
    return county_data


def parse_kml_polygon(polygon_el):
    """
    Parse a KML Polygon element into a shapely geometry.
    Handles outer boundary rings. Returns Polygon or MultiPolygon.
    """
    outer = polygon_el.find(".//kml:outerBoundaryIs/kml:LinearRing/kml:coordinates", NSMAP)
    if outer is None or not outer.text:
        return None
    
    coords_text = outer.text.strip()
    return parse_coordinates_to_polygon(coords_text)


def parse_coordinates_to_polygon(coords_text):
    """Parse KML coordinates string into shapely Polygon."""
    points = []
    for line in coords_text.strip().split():
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) >= 2:
            try:
                lon = float(parts[0])
                lat = float(parts[1])
                points.append((lon, lat))
            except (ValueError, IndexError):
                continue
    
    if len(points) < 3:
        return None
    
    # Ensure the ring is closed
    if points[0] != points[-1]:
        points.append(points[0])
    
    return Polygon(points)


def read_global_kml(path):
    """
    Read global country KML, return two mappings:
      - by_name: {country_name: shapely.geometry}
      - by_code: {iso_a3_code: shapely.geometry}
    
    Natural Earth KML has:
    - <name>CountryName</name>
    - ExtendedData > SchemaData > SimpleData with field ADM0_A3 (ISO_A3 code)
    Also handles ADM0_A3 variants (ISO_A3_EH, etc.)
    """
    tree = etree.parse(path)
    root = tree.getroot()
    
    placemarks = root.findall(".//kml:Placemark", NSMAP)
    
    by_name = {}
    by_code = {}
    
    for pm in placemarks:
        name_el = pm.find("kml:name", NSMAP)
        if name_el is None or not name_el.text:
            continue
        
        name = name_el.text.strip()
        
        # Extract ISO_A3 code from ExtendedData > SchemaData > SimpleData
        iso_code = None
        ext_data = pm.find("kml:ExtendedData", NSMAP)
        if ext_data is not None:
            schema_data = ext_data.find("kml:SchemaData", NSMAP)
            if schema_data is not None:
                for sd in schema_data.findall("kml:SimpleData", NSMAP):
                    field_name = sd.get("name", "")
                    if field_name in ("ADM0_A3", "ADM0_A3_IS", "ISO_A3", "ISO_A3_EH"):
                        if sd.text and sd.text.strip():
                            iso_code = sd.text.strip()
                            break
        
        # Get polygon geometry
        geom = None
        polygon_el = pm.find(".//kml:Polygon", NSMAP)
        if polygon_el is not None:
            geom = parse_kml_polygon(polygon_el)
        else:
            # Check for MultiGeometry
            multi_geom = pm.find(".//kml:MultiGeometry", NSMAP)
            if multi_geom is not None:
                polygons = []
                for poly_el in multi_geom.findall("kml:Polygon", NSMAP):
                    g = parse_kml_polygon(poly_el)
                    if g is not None:
                        polygons.append(g)
                if polygons:
                    geom = MultiPolygon(polygons) if len(polygons) > 1 else polygons[0]
        
        if geom is None:
            continue
        
        by_name[name] = geom
        if iso_code:
            by_code[iso_code] = geom
    
    return by_name, by_code


def match_counties(county_data, config_entries):
    """
    Match counties based on entity config county filters.
    
    Uses state_usps (state abbreviation like "CA") from the parsed county data,
    matching against entity-config.json which uses state abbreviations.
    """
    matched = []
    unmatched_patterns = []
    
    for entry in config_entries:
        state = entry["state"]
        county_pattern = entry["county"]
        
        pattern = re.compile(county_pattern, re.IGNORECASE)
        
        found = False
        for key, data in county_data.items():
            if data["state_usps"] == state and pattern.match(data["county_name"]):
                matched.append(data["geometry"])
                found = True
        
        if not found:
            unmatched_patterns.append(f"No match: {state}/{county_pattern}")
    
    return matched, unmatched_patterns


def merge_polygons(geometries):
    """Merge multiple polygon geometries into a single simplified polygon using unary_union."""
    if not geometries:
        return None
    
    # Filter out None and invalid geometries
    valid = [g for g in geometries if g is not None and g.is_valid]
    
    if not valid:
        return None
    
    if len(valid) == 1:
        return valid[0]
    
    try:
        merged = unary_union(valid)
        return merged
    except Exception:
        # Fallback: return the first valid geometry
        return valid[0]


def simplify_polygon(geom, tolerance=0.02):
    """
    Douglas-Peucker simplification.
    tolerance=0.02 degrees ≈ ~2.2km at mid-latitudes.
    Per D-16: target 5-20km vertex spacing.
    """
    if geom is None:
        return None
    
    try:
        simplified = geom.simplify(tolerance, preserve_topology=True)
        return simplified
    except Exception as e:
        print(f"  Warning: simplification failed ({e}), using unsimplified geometry")
        return geom


def geom_to_coords(geom):
    """
    Convert a shapely geometry to KML coordinates string.
    For MultiPolygon, returns list of coordinate strings (one per polygon).
    """
    if geom is None:
        return []
    
    def ring_to_coords(ring):
        coords = []
        # ring is a linear ring (sequence of (x, y) tuples)
        for x, y in ring.coords:
            coords.append(f"{x:.6f},{y:.6f},0")
        return " ".join(coords)
    
    result = []
    
    if geom.geom_type == "Polygon":
        coords_str = ring_to_coords(geom.exterior)
        if coords_str:
            result.append(coords_str)
    elif geom.geom_type == "MultiPolygon":
        for poly in geom.geoms:
            coords_str = ring_to_coords(poly.exterior)
            if coords_str:
                result.append(coords_str)
    else:
        print(f"  Warning: unexpected geometry type: {geom.geom_type}")
    
    return result


def make_cascading_style(kml_id, line_color, line_width, poly_color):
    """
    Create a gx:CascadingStyle element matching Earth Current.kml pattern.
    """
    style = etree.SubElement(
        etree.Element("{http://www.opengis.net/kml/2.2}Placeholder"),  # temporary
        f"{{{NS_GX}}}CascadingStyle",
        nsmap=NSMAP
    )
    # Reset with proper attributes
    style.clear()
    style = etree.Element(
        f"{{{NS_GX}}}CascadingStyle",
        nsmap=NSMAP,
        attrib={f"{{{NS}}}id": kml_id}
    )
    
    inner_style = etree.SubElement(style, f"{{{NS}}}Style")
    
    # IconStyle (minimal)
    icon_style = etree.SubElement(inner_style, f"{{{NS}}}IconStyle")
    icon = etree.SubElement(icon_style, f"{{{NS}}}Icon")
    icon_href = etree.SubElement(icon, f"{{{NS}}}href")
    icon_href.text = "https://earth.google.com/earth/document/icon?color=1976d2&id=2000&scale=4"
    hot_spot = etree.SubElement(icon_style, f"{{{NS}}}hotSpot")
    hot_spot.set("x", "64")
    hot_spot.set("y", "128")
    hot_spot.set("xunits", "pixels")
    hot_spot.set("yunits", "insetPixels")
    
    # LabelStyle (empty)
    label_style = etree.SubElement(inner_style, f"{{{NS}}}LabelStyle")
    
    # LineStyle
    line_style = etree.SubElement(inner_style, f"{{{NS}}}LineStyle")
    line_color_el = etree.SubElement(line_style, f"{{{NS}}}color")
    line_color_el.text = line_color
    line_width_el = etree.SubElement(line_style, f"{{{NS}}}width")
    line_width_el.text = str(line_width)
    
    # PolyStyle
    poly_style = etree.SubElement(inner_style, f"{{{NS}}}PolyStyle")
    poly_color_el = etree.SubElement(poly_style, f"{{{NS}}}color")
    poly_color_el.text = poly_color
    
    # BalloonStyle (hidden)
    balloon_style = etree.SubElement(inner_style, f"{{{NS}}}BalloonStyle")
    display_mode = etree.SubElement(balloon_style, f"{{{NS}}}displayMode")
    display_mode.text = "hide"
    
    return style


def make_style_map(kml_id, normal_style_id, highlight_style_id):
    """Create a StyleMap element."""
    style_map = etree.Element(f"{{{NS}}}StyleMap", attrib={f"{{{NS}}}id": kml_id})
    
    # Normal pair
    pair_normal = etree.SubElement(style_map, f"{{{NS}}}Pair")
    key_normal = etree.SubElement(pair_normal, f"{{{NS}}}key")
    key_normal.text = "normal"
    style_url_normal = etree.SubElement(pair_normal, f"{{{NS}}}styleUrl")
    style_url_normal.text = f"#{normal_style_id}"
    
    # Highlight pair
    pair_highlight = etree.SubElement(style_map, f"{{{NS}}}Pair")
    key_highlight = etree.SubElement(pair_highlight, f"{{{NS}}}key")
    key_highlight.text = "highlight"
    style_url_highlight = etree.SubElement(pair_highlight, f"{{{NS}}}styleUrl")
    style_url_highlight.text = f"#{highlight_style_id}"
    
    return style_map


def make_placemark(name, coords_list, description=None, style_url=None):
    """
    Create a KML Placemark element with polygon.
    coords_list is a list of coordinate strings (one per polygon ring).
    """
    placemark = etree.Element(f"{{{NS}}}Placemark")
    
    # Name
    name_el = etree.SubElement(placemark, f"{{{NS}}}name")
    name_el.text = name
    
    # Style URL
    if style_url:
        style_url_el = etree.SubElement(placemark, f"{{{NS}}}styleUrl")
        style_url_el.text = f"#{style_url}"
    
    # Description
    if description:
        desc_el = etree.SubElement(placemark, f"{{{NS}}}description")
        desc_el.text = description
    
    # Polygon geometry
    for i, coords_text in enumerate(coords_list):
        polygon = etree.SubElement(placemark, f"{{{NS}}}Polygon")
        
        # Altitude mode (clamp to ground)
        alt_mode = etree.SubElement(polygon, f"{{{NS}}}altitudeMode")
        alt_mode.text = "clampToGround"
        
        outer_boundary = etree.SubElement(polygon, f"{{{NS}}}outerBoundaryIs")
        linear_ring = etree.SubElement(outer_boundary, f"{{{NS}}}LinearRing")
        coords_el = etree.SubElement(linear_ring, f"{{{NS}}}coordinates")
        coords_el.text = coords_text
    
    return placemark


def make_folder(name, children):
    """
    Create a KML Folder element.
    children can be a list of Placemarks or sub-Folders.
    """
    folder = etree.Element(f"{{{NS}}}Folder")
    
    name_el = etree.SubElement(folder, f"{{{NS}}}name")
    name_el.text = name
    
    for child in children:
        folder.append(child)
    
    return folder


def make_document(name, folder_elements, styles_list, style_maps_list):
    """Build complete KML Document with styles and folder hierarchy."""
    document = etree.Element(f"{{{NS}}}Document")
    
    # Document name
    name_el = etree.SubElement(document, f"{{{NS}}}name")
    name_el.text = name
    
    # Visibility (hidden by default - user enables in Google Earth)
    visibility = etree.SubElement(document, f"{{{NS}}}visibility")
    visibility.text = "0"
    
    # Add styles
    for style in styles_list:
        document.append(style)
    
    # Add style maps
    for style_map in style_maps_list:
        document.append(style_map)
    
    # Add folders
    for folder in folder_elements:
        document.append(folder)
    
    return document


def build_kml_tree(document):
    """Wrap Document in a KML element with proper namespaces."""
    kml = etree.Element(
        f"{{{NS}}}kml",
        nsmap={
            None: NS,
            "gx": NS_GX,
        }
    )
    kml.append(document)
    return kml


def write_kml_file(kml_element, filename):
    """Write the KML tree to a file with proper XML declaration."""
    tree = etree.ElementTree(kml_element)
    
    # Pretty-print
    xml_bytes = etree.tostring(kml_element, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    
    output_path = os.path.join(os.path.dirname(__file__), filename)
    with open(output_path, "wb") as f:
        f.write(xml_bytes)
    
    print(f"  Written: {filename} ({len(xml_bytes)} bytes)")


# State FIPS code mapping (for Census TIGER/Line data)
STATE_FIPS_MAP = {
    "AL": "01", "AK": "02", "AZ": "04", "AR": "05", "CA": "06",
    "CO": "08", "CT": "09", "DE": "10", "DC": "11", "FL": "12",
    "GA": "13", "HI": "15", "ID": "16", "IL": "17", "IN": "18",
    "IA": "19", "KS": "20", "KY": "21", "LA": "22", "ME": "23",
    "MD": "24", "MA": "25", "MI": "26", "MN": "27", "MS": "28",
    "MO": "29", "MT": "30", "NE": "31", "NV": "32", "NH": "33",
    "NJ": "34", "NM": "35", "NY": "36", "NC": "37", "ND": "38",
    "OH": "39", "OK": "40", "OR": "41", "PA": "42", "RI": "44",
    "SC": "45", "SD": "46", "TN": "47", "TX": "48", "UT": "49",
    "VT": "50", "VA": "51", "WA": "53", "WV": "54", "WI": "55",
    "WY": "56",
}


# Style generation counters
_style_counter = 0


def generate_style_id(prefix="__managed_style_"):
    """Generate unique style ID following Earth Current.kml convention."""
    global _style_counter
    _style_counter += 1
    # Generate a hex-like suffix similar to Google Earth's convention
    return f"{prefix}{_style_counter:016X}"


def generate_borders_kml(config, county_data, global_by_name, global_by_code):
    """
    Generate borders.kml — authoritative entity polygon layer.
    Per D-03: borders.kml contains ALL entity polygons.
    Per D-07: All 19 US successor states + indigenous nations + global powers.
    Per D-09: Fragmented entities as sub-polygon collections.
    Per D-10: 2050-specific modifications applied.
    Per D-15: Folder hierarchy serves as verification checklist.
    """
    print("Generating borders.kml...")
    
    styles_list = []
    style_maps_list = []
    top_folders = []
    
    # Generate style definitions
    style_configs = {
        "default-polygon": config["styles"]["default-polygon"],
        "indigenous-polygon": config["styles"]["indigenous-polygon"],
        "reactionary-polygon": config["styles"]["reactionary-polygon"],
        "fragmented-entity": config["styles"]["fragmented-entity"],
        "modification-2050": config["styles"]["modification-2050"],
    }
    
    style_ids = {}
    for style_name, style_cfg in style_configs.items():
        normal_id = generate_style_id()
        highlight_id = generate_style_id()
        
        style_normal = make_cascading_style(
            normal_id,
            style_cfg["lineColor"],
            style_cfg["lineWidth"],
            style_cfg["polyColor"],
        )
        style_highlight = make_cascading_style(
            highlight_id,
            style_cfg["lineColor"],
            min(style_cfg["lineWidth"] + 0.5, 3.0),
            style_cfg["polyColor"],
        )
        style_map = make_style_map(generate_style_id(), normal_id, highlight_id)
        
        styles_list.extend([style_normal, style_highlight])
        style_maps_list.append(style_map)
        style_ids[style_name] = style_map.get(f"{{{NS}}}id")
    
    # Build entity polygons
    entity_polygons = {}  # entity_name -> [coord_strings]
    entity_errors = []    # track warnings
    
    for entity_name, entity_cfg in config["entities"].items():
        source_type = entity_cfg.get("source", "none")
        
        if source_type == "county":
            # Process county-based entities (US successor states)
            matches, warnings = match_counties(
                county_data,
                entity_cfg.get("counties", [])
            )
            
            if warnings:
                for w in warnings:
                    entity_errors.append(f"  [{entity_name}] {w}")
            
            merged = merge_polygons(matches)
            if merged is not None:
                simplified = simplify_polygon(merged, tolerance=0.02)
                coords = geom_to_coords(simplified)
                if coords:
                    entity_polygons[entity_name] = {
                        "coords": coords,
                        "type": "county",
                        "cfg": entity_cfg,
                    }
            else:
                entity_errors.append(f"  [{entity_name}] No polygons merged (county data missing)")
        
        elif source_type == "country":
            # Single country entity
            country_code = entity_cfg.get("country_code")
            geom = global_by_code.get(country_code)
            
            if geom is not None:
                simplified = simplify_polygon(geom, tolerance=0.02)
                coords = geom_to_coords(simplified)
                if coords:
                    entity_polygons[entity_name] = {
                        "coords": coords,
                        "type": "country",
                        "cfg": entity_cfg,
                    }
            else:
                entity_errors.append(f"  [{entity_name}] Country code {country_code} not found in global data")
        
        elif source_type == "group":
            # Group of countries merged into one entity
            country_codes = entity_cfg.get("country_codes", [])
            geoms = []
            for code in country_codes:
                g = global_by_code.get(code)
                if g is not None:
                    geoms.append(g)
                else:
                    entity_errors.append(f"  [{entity_name}] Country code {code} not found")
            
            merged = merge_polygons(geoms)
            if merged is not None:
                simplified = simplify_polygon(merged, tolerance=0.02)
                coords = geom_to_coords(simplified)
                if coords:
                    entity_polygons[entity_name] = {
                        "coords": coords,
                        "type": "group",
                        "cfg": entity_cfg,
                    }
            else:
                entity_errors.append(f"  [{entity_name}] No polygon data for any country in group")
        
        elif source_type == "rough_polygon":
            # Entity defined by approximate coordinates
            approx_coords = entity_cfg.get("approximate_coords", [])
            if approx_coords and len(approx_coords) >= 6:
                coords_parts = []
                for i in range(0, len(approx_coords), 2):
                    lon = approx_coords[i]
                    lat = approx_coords[i + 1]
                    coords_parts.append(f"{lon:.6f},{lat:.6f},0")
                # Close the ring
                first_lon = approx_coords[0]
                first_lat = approx_coords[1]
                coords_parts.append(f"{first_lon:.6f},{first_lat:.6f},0")
                
                entity_polygons[entity_name] = {
                    "coords": [" ".join(coords_parts)],
                    "type": "rough_polygon",
                    "cfg": entity_cfg,
                }
        
        elif source_type == "no_polygon":
            # Entity with no terrestrial polygon (orbital, lunar, etc.)
            entity_errors.append(f"  [{entity_name}] No terrestrial polygon (informational only)")
            continue
        
        elif source_type == "none":
            # Entity with no polygon (e.g., Haudenosaunee — within NEC territory)
            entity_errors.append(f"  [{entity_name}] No polygon (within another entity's territory)")
            continue
    
    # Build folder hierarchy from config - handles arbitrary nesting depth
    hierarchy = config["folder_hierarchy"]
    
    def build_entity_folder(entity_name, poly_dict, style_ids_dict, cfg):
        """Create a KML Folder for a single entity, containing its placemark(s)."""
        if entity_name not in poly_dict:
            return None
        
        poly_data = poly_dict[entity_name]
        style_key = "default-polygon"
        category = poly_data["cfg"].get("category", "")
        
        if category == "indigenous":
            style_key = "indigenous-polygon"
        elif category == "reactionary":
            style_key = "reactionary-polygon"
        elif category == "fragmented":
            style_key = "fragmented-entity"
        
        style_id = style_ids_dict.get(style_key)
        see_path = poly_data["cfg"].get("see_path", "")
        is_fragmented = poly_data["cfg"].get("fragmented", False)
        
        if is_fragmented:
            # Fragmentd entity: folder with sub-polygon placemarks
            sub_polygons_config = cfg.get("fragmented_entities", {}).get(entity_name, {})
            sub_names = sub_polygons_config.get("sub_polygons", [])
            
            sub_placemarks = []
            for sub_name in sub_names:
                pm = make_placemark(
                    sub_name,
                    poly_data["coords"],
                    description=see_path,
                    style_url=style_id,
                )
                sub_placemarks.append(pm)
            
            return make_folder(entity_name, sub_placemarks)
        else:
            # Standard entity: single polygon placemark
            pm = make_placemark(
                entity_name,
                poly_data["coords"],
                description=see_path,
                style_url=style_id,
            )
            return make_folder(entity_name, [pm])
    
    def build_hierarchy_folders(node, name):
        """
        Recursively build KML Folder elements from the hierarchy tree.
        - If node is a dict: intermediate level with sub-categories
        - If node is a (non-empty) list of strings: leaf level containing entity names
        - If node is an empty list []: check if name matches an entity key
          (for cases like "Canada": [] where the key IS the entity name)
        - If node is None or not recognized: empty folder
        """
        children = []
        
        if isinstance(node, dict):
            # Intermediate level: sub-categories
            for key, value in node.items():
                child_folder = build_hierarchy_folders(value, key)
                if child_folder is not None:
                    children.append(child_folder)
        
        elif isinstance(node, list):
            if len(node) > 0:
                # Leaf level with entity names
                for entity_name in node:
                    if entity_name not in entity_polygons:
                        continue
                    
                    entity_folder = build_entity_folder(entity_name, entity_polygons, style_ids, config)
                    if entity_folder is not None:
                        children.append(entity_folder)
            else:
                # Empty list: try to interpret the key name as an entity name
                if name in entity_polygons:
                    entity_folder = build_entity_folder(name, entity_polygons, style_ids, config)
                    if entity_folder is not None:
                        return entity_folder
                # If not an entity, create empty folder
                return make_folder(name, [])
        
        return make_folder(name, children)
    
    for continent, subregions in hierarchy.items():
        continent_folder = build_hierarchy_folders(subregions, continent)
        top_folders.append(continent_folder)
    
    # Add 2050 modifications as a special folder
    mod_children = []
    for mod_name, mod_cfg in config.get("modifications_2050", {}).items():
        approx_coords = mod_cfg.get("approximate_coords", [])
        if approx_coords and len(approx_coords) >= 6:
            coords_parts = []
            for i in range(0, len(approx_coords), 2):
                lon = approx_coords[i]
                lat = approx_coords[i + 1]
                coords_parts.append(f"{lon:.6f},{lat:.6f},0")
            first_lon = approx_coords[0]
            first_lat = approx_coords[1]
            coords_parts.append(f"{first_lon:.6f},{first_lat:.6f},0")
            
            mod_pm = make_placemark(
                mod_name,
                [" ".join(coords_parts)],
                description=mod_cfg.get("see_path", mod_cfg.get("description", "")),
                style_url=style_ids.get("modification-2050"),
            )
            mod_children.append(mod_pm)
    
    if mod_children:
        mod_folder = make_folder("2050 Modifications", mod_children)
        top_folders.append(mod_folder)
    
    # Print warnings for entities without polygons
    for err in entity_errors:
        print(err)
    
    # Build document
    doc = make_document("2050 Borders", top_folders, styles_list, style_maps_list)
    kml = build_kml_tree(doc)
    write_kml_file(kml, os.path.join(OUTPUT_DIR, "borders.kml"))
    
    return entity_polygons, style_ids


def generate_domain_kml(domain_name, config, entity_polygons, style_ids):
    """
    Generate domain-specific overlay KML.
    Per D-04: Domain-specific placemarks are rough polygon overlays.
    Per D-08: Each domain's KML includes overlay placemarks corresponding to its → See KML: markers.
    """
    print(f"Generating {domain_name}.kml...")
    
    overlays = config.get("domain_overlays", {}).get(domain_name, [])
    
    if not overlays:
        # Write minimal KML with empty folder
        styles_list = []
        style_maps_list = []
        
        doc = make_document(
            f"2050 {domain_name.capitalize()}",
            [make_folder(domain_name.capitalize(), [])],
            styles_list,
            style_maps_list,
        )
        kml = build_kml_tree(doc)
        write_kml_file(kml, os.path.join(OUTPUT_DIR, f"{domain_name}.kml"))
        return
    
    styles_list = []
    style_maps_list = []
    
    # Domain-specific style
    overlay_style_key = f"{domain_name}-overlay"
    if overlay_style_key in config["styles"]:
        style_cfg = config["styles"][overlay_style_key]
    else:
        style_cfg = config["styles"]["overlay-zone"]
    
    normal_id = generate_style_id()
    highlight_id = generate_style_id()
    
    style_normal = make_cascading_style(
        normal_id,
        style_cfg["lineColor"],
        style_cfg["lineWidth"],
        style_cfg["polyColor"],
    )
    style_highlight = make_cascading_style(
        highlight_id,
        style_cfg["lineColor"],
        min(style_cfg["lineWidth"] + 0.5, 3.0),
        style_cfg["polyColor"],
    )
    style_map = make_style_map(generate_style_id(), normal_id, highlight_id)
    
    styles_list.extend([style_normal, style_highlight])
    style_maps_list.append(style_map)
    overlay_style_id = style_map.get(f"{{{NS}}}id")
    
    placemarks = []
    
    for overlay in overlays:
        overlay_type = overlay.get("type", "rough_polygon")
        name = overlay.get("name", "Unnamed")
        description = overlay.get("description", "")
        
        if overlay_type == "entity_copy":
            # Copy polygon from entity borders data
            source_entity = overlay.get("source_entity", "")
            if source_entity in entity_polygons:
                poly_data = entity_polygons[source_entity]
                pm = make_placemark(
                    name,
                    poly_data["coords"],
                    description=description,
                    style_url=overlay_style_id,
                )
                placemarks.append(pm)
            else:
                print(f"  Warning: entity_copy source '{source_entity}' not found for '{name}'")
        
        elif overlay_type == "rough_polygon":
            # Approximate bounding polygon
            approx_coords = overlay.get("approximate_coords", [])
            if approx_coords and len(approx_coords) >= 6:
                coords_parts = []
                for i in range(0, len(approx_coords), 2):
                    lon = approx_coords[i]
                    lat = approx_coords[i + 1]
                    coords_parts.append(f"{lon:.6f},{lat:.6f},0")
                first_lon = approx_coords[0]
                first_lat = approx_coords[1]
                coords_parts.append(f"{first_lon:.6f},{first_lat:.6f},0")
                
                pm = make_placemark(
                    name,
                    [" ".join(coords_parts)],
                    description=description,
                    style_url=overlay_style_id,
                )
                placemarks.append(pm)
        
        elif overlay_type == "no_polygon":
            # Placemark without polygon (informational only)
            pm = make_placemark(
                name,
                [],
                description=description,
            )
            placemarks.append(pm)
    
    folder = make_folder(domain_name.capitalize(), placemarks)
    doc = make_document(
        f"2050 {domain_name.capitalize()}",
        [folder],
        styles_list,
        style_maps_list,
    )
    kml = build_kml_tree(doc)
    write_kml_file(kml, os.path.join(OUTPUT_DIR, f"{domain_name}.kml"))


def verify_outputs():
    """Verify that all 6 KML files were generated with valid content."""
    domains = ["borders", "climate", "technology", "economy", "demographics", "culture"]
    output_dir = os.path.join(os.path.dirname(__file__), OUTPUT_DIR)
    
    all_ok = True
    for domain in domains:
        path = os.path.join(output_dir, f"{domain}.kml")
        if os.path.exists(path):
            try:
                tree = etree.parse(path)
                placemarks = tree.findall(".//kml:Placemark", NSMAP)
                print(f"  {domain}.kml: {len(placemarks)} placemarks, {os.path.getsize(path)} bytes")
            except Exception as e:
                print(f"  {domain}.kml: PARSE ERROR — {e}")
                all_ok = False
        else:
            print(f"  {domain}.kml: MISSING")
            all_ok = False
    
    return all_ok


def main():
    """Main entry point."""
    print("=" * 60)
    print("2050 KML Map Generator")
    print("=" * 60)
    print()
    
    # Load config
    print("Loading entity config...")
    config = load_config()
    print(f"  {len(config['entities'])} entities defined")
    print(f"  {sum(len(v) for v in config['domain_overlays'].values())} overlay placemarks")
    print()
    
    # Read source data
    script_dir = os.path.dirname(__file__)
    county_path = os.path.join(script_dir, SOURCE_DIR, "us-counties.kml")
    global_path = os.path.join(script_dir, SOURCE_DIR, "global-countries.kml")
    
    if not os.path.exists(county_path):
        print(f"ERROR: County source not found: {county_path}")
        print("Run Task 1 first to download source KML datasets.")
        sys.exit(1)
    
    if not os.path.exists(global_path):
        print(f"ERROR: Global source not found: {global_path}")
        print("Run Task 1 first to download source KML datasets.")
        sys.exit(1)
    
    print("Reading US county KML...")
    county_data = read_county_kml(county_path)
    print(f"  Loaded {len(county_data)} counties")
    print()
    
    print("Reading global country KML...")
    global_by_name, global_by_code = read_global_kml(global_path)
    print(f"  Loaded {len(global_by_name)} countries by name, {len(global_by_code)} by code")
    print()
    
    # Generate borders.kml (entity polygons)
    entity_polygons, style_ids = generate_borders_kml(
        config, county_data, global_by_name, global_by_code
    )
    print(f"  Generated {len(entity_polygons)} entity polygons")
    print()
    
    # Generate domain overlay KMLs
    domains = ["climate", "technology", "economy", "demographics", "culture"]
    for domain in domains:
        generate_domain_kml(domain, config, entity_polygons, style_ids)
        print()
    
    # Verify outputs
    print("Verifying outputs...")
    if verify_outputs():
        print()
        print("SUCCESS: All 6 KML files generated.")
    else:
        print()
        print("WARNING: Some output files may have issues.")
    
    print()
    print("Per D-19: Open generated KMLs in Google Earth Pro for refinement.")
    print("Polygons use Douglas-Peucker simplification at ~2km vertex spacing.")
    print("Approximate overlay polygons will need manual adjustment in Google Earth Pro.")


if __name__ == "__main__":
    main()
