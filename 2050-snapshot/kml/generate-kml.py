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
from shapely.geometry import shape, MultiPolygon, Polygon, Point, LineString
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
        
        # Get polygon geometry — handle MultiGeometry (counties with islands, exclaves, etc.)
        geom = None
        multi_geom = pm.find(".//kml:MultiGeometry", NSMAP)
        if multi_geom is not None:
            polygons = []
            for poly_el in multi_geom.findall("kml:Polygon", NSMAP):
                g = parse_kml_polygon(poly_el)
                if g is not None:
                    polygons.append(g)
            if polygons:
                geom = MultiPolygon(polygons) if len(polygons) > 1 else polygons[0]
        else:
            polygon_el = pm.find("kml:Polygon", NSMAP)
            if polygon_el is not None:
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


def read_admin1_kml(path):
    """
    Read NE admin-1 KML, return {(iso_code, name): geometry} mapping.
    
    Natural Earth admin-1 KML has:
    - <name>RegionName</name>
    - ExtendedData > SchemaData > SimpleData with adm0_a3 (ISO country code)
    
    Returns dict keyed by (country_code, region_name).
    """
    tree = etree.parse(path)
    root = tree.getroot()
    
    placemarks = root.findall(".//kml:Placemark", NSMAP)
    
    admin1_data = {}
    for pm in placemarks:
        name_el = pm.find("kml:name", NSMAP)
        if name_el is None or not name_el.text:
            continue
        
        region_name = name_el.text.strip()
        
        # Extract country code
        country_code = None
        ext_data = pm.find("kml:ExtendedData", NSMAP)
        if ext_data is not None:
            schema_data = ext_data.find("kml:SchemaData", NSMAP)
            if schema_data is not None:
                for sd in schema_data.findall("kml:SimpleData", NSMAP):
                    field_name = sd.get("name", "")
                    if field_name in ("adm0_a3", "ADM0_A3", "gu_a3"):
                        if sd.text and sd.text.strip():
                            country_code = sd.text.strip()
                            break
                if country_code is None:
                    for sd in schema_data.findall("kml:SimpleData", NSMAP):
                        field_name = sd.get("name", "")
                        if field_name == "iso_a2":
                            if sd.text and sd.text.strip():
                                country_code = sd.text.strip()
                                break
        
        if not country_code:
            continue
        
        # Get polygon geometry
        geom = None
        multi_geom = pm.find(".//kml:MultiGeometry", NSMAP)
        if multi_geom is not None:
            polygons = []
            for poly_el in multi_geom.findall("kml:Polygon", NSMAP):
                g = parse_kml_polygon(poly_el)
                if g is not None:
                    polygons.append(g)
            if polygons:
                geom = MultiPolygon(polygons) if len(polygons) > 1 else polygons[0]
        else:
            polygon_el = pm.find("kml:Polygon", NSMAP)
            if polygon_el is not None:
                geom = parse_kml_polygon(polygon_el)
        
        if geom is None:
            continue
        
        key = (country_code, region_name)
        admin1_data[key] = geom
    
    return admin1_data


def read_global_kml(path):
    """
    Read global country KML, return three mappings:
      - by_name: {country_name: shapely.geometry}
      - by_code: {iso_a3_code: shapely.geometry}
      - code_to_name: {iso_a3_code: country_name}
    
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
    code_to_name = {}
    
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
        # Check for MultiGeometry first — when both Polygon and MultiGeometry
        # exist (e.g., China, Russia, Canada), MultiGeometry has ALL polygons
        # while a bare Polygon may only contain a tiny island.
        multi_geom = pm.find(".//kml:MultiGeometry", NSMAP)
        if multi_geom is not None:
            polygons = []
            for poly_el in multi_geom.findall("kml:Polygon", NSMAP):
                g = parse_kml_polygon(poly_el)
                if g is not None:
                    polygons.append(g)
            if polygons:
                geom = MultiPolygon(polygons) if len(polygons) > 1 else polygons[0]
        else:
            # No MultiGeometry — check for single Polygon
            polygon_el = pm.find("kml:Polygon", NSMAP)
            if polygon_el is not None:
                geom = parse_kml_polygon(polygon_el)
        
        if geom is None:
            continue
        
        by_name[name] = geom
        if iso_code:
            by_code[iso_code] = geom
            code_to_name[iso_code] = name
    
    return by_name, by_code, code_to_name


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
        if merged.geom_type == 'MultiPolygon' and len(merged.geoms) > 1:
            merged = merged.buffer(0.0001).buffer(-0.0001)
        return merged
    except Exception:
        # Fallback: return the first valid geometry
        return valid[0]


def simplify_polygon(geom, tolerance=0.01):
    """
    Douglas-Peucker simplification.
    tolerance=0.01 degrees ≈ ~1.1km at mid-latitudes.
    Per D-16: target 5-20km vertex spacing.
    With 1:10m/1:500k source data, 0.01 preserves sufficient detail
    while keeping KML files at manageable size (~5-20km effective spacing).
    """
    if geom is None:
        return None
    
    try:
        simplified = geom.simplify(tolerance, preserve_topology=True)
        return simplified
    except Exception as e:
        print(f"  Warning: simplification failed ({e}), using unsimplified geometry")
        return geom


def remove_slivers(geom, min_area_ratio=0.00001):
    """
    Remove sliver polygons from a MultiPolygon result (e.g. after difference).
    Keeps only polygons whose area is at least min_area_ratio of the largest polygon.
    For a single Polygon, returns it as-is.
    """
    if geom is None or geom.is_empty:
        return geom
    if geom.geom_type == "Polygon":
        return geom
    if geom.geom_type == "MultiPolygon":
        polys = list(geom.geoms)
        if len(polys) <= 1:
            return geom
        areas = [p.area for p in polys]
        max_area = max(areas)
        keep = [p for p, a in zip(polys, areas) if a >= max_area * min_area_ratio]
        if len(keep) == 0:
            return None
        if len(keep) == 1:
            return keep[0]
        return MultiPolygon(keep)
    return geom


def load_border_line(path):
    """
    Load a border LineString from a KML file.
    Returns a shapely LineString with consecutive duplicate points removed.
    """
    tree = etree.parse(path)
    root = tree.getroot()
    coords_el = root.find('.//kml:coordinates', NSMAP)
    if coords_el is None or not coords_el.text:
        raise ValueError(f"No coordinates found in border KML: {path}")
    pts = []
    for pt in coords_el.text.strip().split():
        p = pt.split(',')
        if len(p) >= 2:
            pts.append((float(p[0]), float(p[1])))
    if len(pts) < 2:
        raise ValueError(f"Border KML has fewer than 2 points: {path}")
    # Remove consecutive duplicate points (within 1e-7 tolerance)
    clean = [pts[0]]
    for pt in pts[1:]:
        d = ((pt[0] - clean[-1][0])**2 + (pt[1] - clean[-1][1])**2)**0.5
        if d > 1e-7:
            clean.append(pt)
    return LineString(clean)


def extend_border_line(line):
    """
    Extend the border line at both ends to fully bisect the combined polygon.
    West extension: from the northern endpoint west into the Pacific (-115°W).
    East extension: from the southern endpoint east into the Gulf / toward Atlantic.
    Returns a continuous LineString.
    """
    coords = list(line.coords)
    if len(coords) < 2:
        return line

    north_pt = coords[0]
    south_pt = coords[-1]

    # Western extension: go west from north_pt into the Pacific to bisect Baja/Mexico
    west_ext = [(-115.0, north_pt[1])]

    # Eastern extension: go east from south_pt to bisect the Gulf
    east_ext = [(-90.0, south_pt[1])]

    # Assemble: west_ext → coords → east_ext
    extended_coords = west_ext + coords + east_ext
    clean = [extended_coords[0]]
    for pt in extended_coords[1:]:
        d = ((pt[0] - clean[-1][0])**2 + (pt[1] - clean[-1][1])**2)**0.5
        if d > 1e-7:
            clean.append(pt)
    return LineString(clean)


def split_along_border(geom, line, keep_side):
    """
    Split a geometry along an extended border line and keep fragments
    on the specified side ('southwest' or 'northeast').
    Uses shapely.ops.split() — no polygon clipping, no straight edges.
    """
    from shapely.ops import split
    
    # Ensure clean inputs
    geom = geom.buffer(0)
    line = line.buffer(0.00001).simplify(0.0001)
    
    try:
        fragments = split(geom, line)
    except Exception:
        return geom  # split failed, return original
    
    if fragments.geom_type == 'GeometryCollection':
        pieces = list(fragments.geoms)
    else:
        pieces = [fragments]
    
    kept = []
    for piece in pieces:
        if piece.is_empty:
            continue
        # Determine which side the piece is on
        centroid = piece.centroid
        # Project centroid onto line, compare
        proj_dist = line.project(centroid)
        proj_pt = line.interpolate(proj_dist)
        
        # Cross product to determine side
        # Get the line direction at the projected point
        if proj_dist < line.length - 0.0001:
            next_pt = line.interpolate(proj_dist + 0.0001)
        else:
            next_pt = line.interpolate(proj_dist - 0.0001)
        
        dx = next_pt.x - proj_pt.x
        dy = next_pt.y - proj_pt.y
        cx = centroid.x - proj_pt.x
        cy = centroid.y - proj_pt.y
        
        # Cross product: positive = left of line (SW), negative = right (NE)
        # Line goes NW→SE, so left = SW, right = NE
        cross = dx * cy - dy * cx
        
        if keep_side == 'southwest':
            if cross >= -1e-10:
                kept.append(piece)
        elif keep_side == 'northeast':
            if cross <= 1e-10:
                kept.append(piece)
    
    if not kept:
        return geom  # nothing kept, return original
    
    merged = unary_union(kept)
    return merged


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
        attrib={"id": kml_id}
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
    style_map = etree.Element(f"{{{NS}}}StyleMap", attrib={"id": kml_id})
    
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


def make_polygon_element(coords_text):
    """Create a single KML Polygon element with the given coordinates."""
    polygon = etree.Element(f"{{{NS}}}Polygon")
    alt_mode = etree.SubElement(polygon, f"{{{NS}}}altitudeMode")
    alt_mode.text = "clampToGround"
    outer_boundary = etree.SubElement(polygon, f"{{{NS}}}outerBoundaryIs")
    linear_ring = etree.SubElement(outer_boundary, f"{{{NS}}}LinearRing")
    coords_el = etree.SubElement(linear_ring, f"{{{NS}}}coordinates")
    coords_el.text = coords_text
    return polygon


def make_placemark(name, coords_text, description=None, style_url=None):
    """
    Create a KML Placemark element with a single polygon.
    coords_text is a single KML coordinates string (e.g. "lon,lat,0 lon,lat,0...").
    Pass empty string for placemarks without geometry (no_polygon type).
    """
    placemark = etree.Element(f"{{{NS}}}Placemark")
    
    name_el = etree.SubElement(placemark, f"{{{NS}}}name")
    name_el.text = name
    
    if style_url:
        style_url_el = etree.SubElement(placemark, f"{{{NS}}}styleUrl")
        style_url_el.text = f"#{style_url}"
    
    if description:
        desc_el = etree.SubElement(placemark, f"{{{NS}}}description")
        desc_el.text = description
    
    if coords_text:
        placemark.append(make_polygon_element(coords_text))
    
    return placemark


def make_placemark_multi(name, coords_list, description=None, style_url=None):
    """
    Create a KML Placemark with multiple polygons wrapped in MultiGeometry.
    Used by domain overlay KMLs where individual polygon styling isn't needed.
    coords_list is a list of KML coordinate strings.
    """
    placemark = etree.Element(f"{{{NS}}}Placemark")
    
    name_el = etree.SubElement(placemark, f"{{{NS}}}name")
    name_el.text = name
    
    if style_url:
        style_url_el = etree.SubElement(placemark, f"{{{NS}}}styleUrl")
        style_url_el.text = f"#{style_url}"
    
    if description:
        desc_el = etree.SubElement(placemark, f"{{{NS}}}description")
        desc_el.text = description
    
    if len(coords_list) == 1:
        placemark.append(make_polygon_element(coords_list[0]))
    elif len(coords_list) > 1:
        multi = etree.SubElement(placemark, f"{{{NS}}}MultiGeometry")
        for ct in coords_list:
            multi.append(make_polygon_element(ct))
    
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


def generate_borders_kml(config, county_data, global_by_name, global_by_code, code_to_name, admin1_data):
    """
    Generate borders.kml — authoritative entity polygon layer.
    """
    print("Generating borders.kml...")
    
    # Load user's per-entity colors from manual KML styling
    script_dir = os.path.dirname(__file__)
    colors_path = os.path.join(script_dir, "user_colors.json")
    user_colors = {}
    if os.path.exists(colors_path):
        with open(colors_path) as f:
            user_colors = json.load(f)
        print(f"  Loaded {len(user_colors)} per-entity color assignments")
    else:
        user_colors = {}
    
    styles_list = []
    style_maps_list = []
    top_folders = []
    
    # Default fallback style (gray) for entities without user colors
    _fallback_color_count = [0]
    
    def get_entity_style(entity_name, geometry_present=True):
        """
        Get or create a style for an entity.
        Uses the user's color if available; otherwise generates a fallback.
        Returns (normal_style_id, highlight_style_id, style_map_id)
        """
        nonlocal styles_list, style_maps_list
        
        color_info = user_colors.get(entity_name)
        
        if color_info:
            kml_fill = color_info.get("kml_fill", "80586b34")
            kml_line = color_info.get("kml_line", "ff" + kml_fill[2:])
            line_width = color_info.get("width", 1.0)
            highlight_width = min(line_width + 0.5, 3.0)
        else:
            _fallback_color_count[0] += 1
            # Generate a deterministic color from entity name hash
            import hashlib
            h = hashlib.md5(entity_name.encode()).hexdigest()
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
            kml_fill = f"80{b:02x}{g:02x}{r:02x}"
            kml_line = f"ff{b:02x}{g:02x}{r:02x}"
            line_width = 1.0
            highlight_width = 1.5
        
        normal_id = generate_style_id()
        highlight_id = generate_style_id()
        style_map_id = generate_style_id()
        
        style_normal = make_cascading_style(normal_id, kml_line, line_width, kml_fill)
        style_highlight = make_cascading_style(highlight_id, kml_line, highlight_width, kml_fill)
        style_map = make_style_map(style_map_id, normal_id, highlight_id)
        
        styles_list.append(style_normal)
        styles_list.append(style_highlight)
        style_maps_list.append(style_map)
        
        return normal_id, highlight_id, style_map_id
    
    # Build entity polygons
    entity_polygons = {}
    entity_errors = []
    groups_expanded = {}
    entity_styles = {}
    
    for entity_name, entity_cfg in config["entities"].items():
        source_type = entity_cfg.get("source", "none")
        
        if source_type == "county":
            matches, warnings = match_counties(
                county_data,
                entity_cfg.get("counties", [])
            )
            
            if warnings:
                for w in warnings:
                    entity_errors.append(f"  [{entity_name}] {w}")
            
            merged = merge_polygons(matches)
            if merged is not None:
                simplified = simplify_polygon(merged, tolerance=0.01)
                coords = geom_to_coords(simplified)
                if coords:
                    entity_polygons[entity_name] = {
                        "coords": coords,
                        "type": "county",
                        "cfg": entity_cfg,
                    }
                    _, _, style_id = get_entity_style(entity_name)
                    entity_styles[entity_name] = style_id
            else:
                entity_errors.append(f"  [{entity_name}] No polygons merged (county data missing)")
        
        elif source_type == "country":
            country_code = entity_cfg.get("country_code")
            geom = global_by_code.get(country_code)
            
            if geom is not None:
                # Subtract admin-1 regions from country polygon
                subtract_admin1 = entity_cfg.get("subtract_admin1", [])
                if subtract_admin1 and admin1_data:
                    for region_name in subtract_admin1:
                        admin1_geom = admin1_data.get((country_code, region_name))
                        if admin1_geom is not None:
                            geom = geom.difference(admin1_geom)
                        else:
                            entity_errors.append(f"  [{entity_name}] Subtract admin1 '{region_name}' not found")
                    geom = remove_slivers(geom)
                
                # Add additional county territory to country polygon (e.g., Mexico + Aztlán)
                add_counties = entity_cfg.get("add_counties", [])
                if add_counties:
                    county_matches, cw = match_counties(county_data, add_counties)
                    if cw:
                        for w in cw:
                            entity_errors.append(f"  [{entity_name}] add_counties: {w}")
                    if county_matches:
                        cm = merge_polygons(county_matches)
                        if cm is not None:
                            cm = remove_slivers(cm)
                            geom = geom.union(cm)
                
                # Add additional country territories (e.g., France + Fr. S. Antarctic Lands)
                add_country_codes = entity_cfg.get("add_country_codes", [])
                if add_country_codes:
                    for cc in add_country_codes:
                        g = global_by_code.get(cc)
                        if g is not None:
                            geom = geom.union(g)
                        else:
                            entity_errors.append(f"  [{entity_name}] add_country_codes: '{cc}' not found")
                
                simplified = simplify_polygon(geom, tolerance=0.01)
                coords = geom_to_coords(simplified)
                if coords:
                    entity_polygons[entity_name] = {
                        "coords": coords,
                        "type": "country",
                        "cfg": entity_cfg,
                    }
                    _, _, style_id = get_entity_style(entity_name)
                    entity_styles[entity_name] = style_id
            else:
                entity_errors.append(f"  [{entity_name}] Country code {country_code} not found in global data")
        
        elif source_type == "admin1":
            country_code = entity_cfg.get("country_code")
            admin1_name = entity_cfg.get("admin1_name")
            geom = admin1_data.get((country_code, admin1_name))
            
            if geom is not None:
                simplified = simplify_polygon(geom, tolerance=0.01)
                coords = geom_to_coords(simplified)
                if coords:
                    entity_polygons[entity_name] = {
                        "coords": coords,
                        "type": "admin1",
                        "cfg": entity_cfg,
                    }
                    _, _, style_id = get_entity_style(entity_name)
                    entity_styles[entity_name] = style_id
            else:
                entity_errors.append(f"  [{entity_name}] Admin1 '{admin1_name}' in {country_code} not found")
        
        elif source_type == "group":
            country_codes = entity_cfg.get("country_codes", [])
            keep_unified = entity_cfg.get("keep_unified", False)
            
            if keep_unified:
                geoms = []
                for code in country_codes:
                    g = global_by_code.get(code)
                    if g is not None:
                        geoms.append(g)
                    else:
                        entity_errors.append(f"  [{entity_name}] Country code {code} not found")
                
                # Add admin-1 regions to merged polygon
                for admin1_ref in entity_cfg.get("admin1_regions", []):
                    cc = admin1_ref.get("country_code")
                    rn = admin1_ref.get("admin1_name")
                    admin1_geom = admin1_data.get((cc, rn))
                    if admin1_geom is not None:
                        geoms.append(admin1_geom)
                    else:
                        entity_errors.append(f"  [{entity_name}] Admin1 region '{rn}' in {cc} not found")
                
                merged = merge_polygons(geoms)
                if merged is not None:
                    simplified = simplify_polygon(merged, tolerance=0.01)
                    coords = geom_to_coords(simplified)
                    if coords:
                        entity_polygons[entity_name] = {
                            "coords": coords,
                            "type": "group",
                            "cfg": entity_cfg,
                        }
                        _, _, style_id = get_entity_style(entity_name)
                        entity_styles[entity_name] = style_id
                else:
                    entity_errors.append(f"  [{entity_name}] No polygon data for any country in group")
            else:
                geoms = []
                expanded_names = []
                subtract_per_code = entity_cfg.get("subtract_admin1_per_code", {})
                for code in country_codes:
                    g = global_by_code.get(code)
                    if g is not None:
                        # Apply per-code admin1 subtraction
                        code_subtract = subtract_per_code.get(code, [])
                        if code_subtract and admin1_data:
                            for region_name in code_subtract:
                                admin1_geom = admin1_data.get((code, region_name))
                                if admin1_geom is not None:
                                    g = g.difference(admin1_geom)
                                else:
                                    entity_errors.append(f"  [{entity_name}] Subtract admin1 '{region_name}' for {code} not found")
                            g = remove_slivers(g)
                        geoms.append(g)
                        country_name = code_to_name.get(code, f"{entity_name} - {code}")
                        simplified = simplify_polygon(g, tolerance=0.01)
                        coords = geom_to_coords(simplified)
                        if coords:
                            entity_polygons[country_name] = {
                                "coords": coords,
                                "type": "country",
                                "cfg": entity_cfg,
                            }
                            expanded_names.append(country_name)
                            _, _, style_id = get_entity_style(country_name)
                            entity_styles[country_name] = style_id
                    else:
                        entity_errors.append(f"  [{entity_name}] Country code {code} not found")
                
                if expanded_names:
                    groups_expanded[entity_name] = expanded_names
                    merged = merge_polygons(geoms)
                    if merged is not None:
                        simplified = simplify_polygon(merged, tolerance=0.01)
                        coords = geom_to_coords(simplified)
                        if coords:
                            entity_polygons[entity_name] = {
                                "coords": coords,
                                "type": "group",
                                "cfg": entity_cfg,
                            }
                else:
                    entity_errors.append(f"  [{entity_name}] No polygon data for any country in group")
        
        elif source_type == "manual":
            manual_path = entity_cfg.get("manual_path", "")
            if manual_path:
                full_path = os.path.join(os.path.dirname(__file__), manual_path)
                if os.path.exists(full_path):
                    manual_tree = etree.parse(full_path)
                    manual_root = manual_tree.getroot()
                    coords = manual_root.findall(".//kml:coordinates", NSMAP)
                    if coords:
                        coord_strings = [c.text.strip() for c in coords if c.text]
                        entity_polygons[entity_name] = {
                            "coords": coord_strings,
                            "type": "manual",
                            "cfg": entity_cfg,
                        }
                        _, _, style_id = get_entity_style(entity_name)
                        entity_styles[entity_name] = style_id
                    else:
                        entity_errors.append(f"  [{entity_name}] No coordinates found in manual KML")
                else:
                    entity_errors.append(f"  [{entity_name}] Manual KML not found: {manual_path}")
            else:
                entity_errors.append(f"  [{entity_name}] Manual source requires manual_path")
        
        elif source_type == "rough_polygon":
            approx_coords = entity_cfg.get("approximate_coords", [])
            if approx_coords and len(approx_coords) >= 6:
                coords_parts = []
                for i in range(0, len(approx_coords), 2):
                    lon = approx_coords[i]
                    lat = approx_coords[i + 1]
                    coords_parts.append(f"{lon:.6f},{lat:.6f},0")
                first_lon = approx_coords[0]
                first_lat = approx_coords[1]
                coords_parts.append(f"{first_lon:.6f},{first_lat:.6f},0")
                
                entity_polygons[entity_name] = {
                    "coords": [" ".join(coords_parts)],
                    "type": "rough_polygon",
                    "cfg": entity_cfg,
                }
                _, _, style_id = get_entity_style(entity_name)
                entity_styles[entity_name] = style_id
        
        elif source_type == "no_polygon":
            entity_errors.append(f"  [{entity_name}] No terrestrial polygon (informational only)")
            continue
        
        elif source_type == "none":
            entity_errors.append(f"  [{entity_name}] No polygon (within another entity's territory)")
            continue
    
    if _fallback_color_count[0] > 0:
        print(f"  {_fallback_color_count[0]} entities used fallback (auto-generated) colors")
    
    # Post-processing: if Mexico and Texas both specify clip_line to the same file,
    # combine their polygons, split along the border line, and reassign fragments.
    clip_pairs = []
    for ename, ecfg in config["entities"].items():
        cl = ecfg.get("clip_line")
        if cl:
            clip_pairs.append((ename, cl))
    
    # Group entities by clip_line path
    from collections import defaultdict
    clip_groups = defaultdict(list)
    for ename, cl in clip_pairs:
        clip_groups[cl["path"]].append((ename, cl["side"]))
    
    for path, group in clip_groups.items():
        if len(group) != 2:
            continue  # need exactly 2 entities sharing one border line
        
        (ename_a, side_a), (ename_b, side_b) = group
        if side_a == side_b:
            continue  # need opposite sides
        
        if ename_a not in entity_polygons or ename_b not in entity_polygons:
            continue
        
        print(f"  Combined split: {'/'.join(f'{en} ({sd})' for en, sd in group)} along {path}")
        
        try:
            border_line = load_border_line(os.path.join(script_dir, path))
            
            # Reconstruct both geometries from their coords
            poly_a = entity_polygons[ename_a]
            poly_b = entity_polygons[ename_b]
            
            a_geoms = []
            for ct in poly_a["coords"]:
                pts = [(float(p.split(",")[0]), float(p.split(",")[1])) for p in ct.strip().split() if "," in p]
                if len(pts) >= 3:
                    if pts[0] != pts[-1]: pts.append(pts[0])
                    try: a_geoms.append(Polygon(pts))
                    except: pass
            
            b_geoms = []
            for ct in poly_b["coords"]:
                pts = [(float(p.split(",")[0]), float(p.split(",")[1])) for p in ct.strip().split() if "," in p]
                if len(pts) >= 3:
                    if pts[0] != pts[-1]: pts.append(pts[0])
                    try: b_geoms.append(Polygon(pts))
                    except: pass
            
            if not a_geoms or not b_geoms:
                continue
            
            # Combine both into one blob
            combined = unary_union(a_geoms + b_geoms)
            combined = combined.buffer(0)
            
            # Split along the border line
            from shapely.ops import split
            try:
                fragments = split(combined, border_line)
            except Exception:
                try:
                    fragments = split(combined, border_line.buffer(1e-7))
                except Exception as e2:
                    raise e2
            
            if fragments.geom_type == 'GeometryCollection':
                pieces = list(fragments.geoms)
            else:
                pieces = [fragments]
            
            # Assign each piece to the correct side
            sw_pieces = []
            ne_pieces = []
            for piece in pieces:
                if piece.is_empty or piece.area < 1e-8:
                    continue
                centroid = piece.centroid
                proj_dist = border_line.project(centroid)
                proj_pt = border_line.interpolate(min(proj_dist, border_line.length - 0.00001))
                next_pt = border_line.interpolate(min(proj_dist + 0.00001, border_line.length))
                
                dx = next_pt.x - proj_pt.x
                dy = next_pt.y - proj_pt.y
                cx = centroid.x - proj_pt.x
                cy = centroid.y - proj_pt.y
                cross = dx * cy - dy * cx
                
                # cross > 0 = NE of line (for N→S line), cross < 0 = SW
                # Our line goes N→S (north extension → border → south extension)
                if cross >= -1e-10:
                    ne_pieces.append(piece)
                else:
                    sw_pieces.append(piece)
            
            # Map sides to entity names and their poly data
            ename_sw = next(en for en, sd in group if sd == "southwest")
            ename_ne = next(en for en, sd in group if sd == "northeast")
            poly_sw = entity_polygons.get(ename_sw, {})
            poly_ne = entity_polygons.get(ename_ne, {})
            
            # Regenerate entity polygons
            if sw_pieces:
                sw_merged = unary_union(sw_pieces)
                sw_merged = remove_slivers(sw_merged)
                sw_simple = simplify_polygon(sw_merged, 0.01)
                sw_coords = geom_to_coords(sw_simple)
                if sw_coords:
                    entity_polygons[ename_sw] = {
                        "coords": sw_coords,
                        "type": poly_sw.get("type", "country"),
                        "cfg": poly_sw.get("cfg", {}),
                    }
                else:
                    entity_errors.append(f"  Combined split [{ename_sw}]: geom_to_coords returned empty")
            
            if ne_pieces:
                ne_merged = unary_union(ne_pieces)
                ne_merged = remove_slivers(ne_merged)
                ne_simple = simplify_polygon(ne_merged, 0.01)
                ne_coords = geom_to_coords(ne_simple)
                if ne_coords:
                    entity_polygons[ename_ne] = {
                        "coords": ne_coords,
                        "type": poly_ne.get("type", "county"),
                        "cfg": poly_ne.get("cfg", {}),
                    }
                else:
                    entity_errors.append(f"  Combined split [{ename_ne}]: geom_to_coords returned empty")
            
            print(f"    Split into {len(sw_pieces)} SW + {len(ne_pieces)} NE fragments")
        except Exception as e:
            entity_errors.append(f"  Combined split [{ename_a}/{ename_b}]: {e}")
    
    # Build folder hierarchy from config
    hierarchy = config["folder_hierarchy"]
    
    def build_entity_folder(entity_name, poly_dict, cfg):
        """Create a KML Folder for a single entity with per-polygon Placemarks."""
        if entity_name not in poly_dict:
            return None
        
        poly_data = poly_dict[entity_name]
        style_id = entity_styles.get(entity_name)
        see_path = poly_data["cfg"].get("see_path", "")
        is_fragmented = poly_data["cfg"].get("fragmented", False)
        
        placemarks = []
        coords_list = poly_data["coords"]
        
        if is_fragmented:
            sub_polygons_config = cfg.get("fragmented_entities", {}).get(entity_name, {})
            sub_names = sub_polygons_config.get("sub_polygons", [])
            for ct in coords_list:
                parent_pm = make_placemark(entity_name, ct, description=see_path, style_url=style_id)
                placemarks.append(parent_pm)
            for sub_name in sub_names:
                for ct in coords_list:
                    pm = make_placemark(sub_name, ct, description=see_path, style_url=style_id)
                    placemarks.append(pm)
        else:
            for ct in coords_list:
                pm = make_placemark(entity_name, ct, description=see_path, style_url=style_id)
                placemarks.append(pm)
        
        return make_folder(entity_name, placemarks)
    
    def build_hierarchy_folders(node, name):
        children = []
        
        if isinstance(node, dict):
            for key, value in node.items():
                child_folder = build_hierarchy_folders(value, key)
                if child_folder is not None:
                    children.append(child_folder)
        
        elif isinstance(node, list):
            if len(node) > 0:
                for entity_name in node:
                    if entity_name in groups_expanded:
                        sub_children = []
                        for cname in groups_expanded[entity_name]:
                            if cname in entity_polygons:
                                ef = build_entity_folder(cname, entity_polygons, config)
                                if ef is not None:
                                    sub_children.append(ef)
                        if sub_children:
                            children.append(make_folder(entity_name, sub_children))
                    elif entity_name in entity_polygons:
                        entity_folder = build_entity_folder(entity_name, entity_polygons, config)
                        if entity_folder is not None:
                            children.append(entity_folder)
            else:
                if name in groups_expanded:
                    sub_children = []
                    for cname in groups_expanded[name]:
                        if cname in entity_polygons:
                            ef = build_entity_folder(cname, entity_polygons, config)
                            if ef is not None:
                                sub_children.append(ef)
                    return make_folder(name, sub_children) if sub_children else make_folder(name, [])
                elif name in entity_polygons:
                    entity_folder = build_entity_folder(name, entity_polygons, config)
                    if entity_folder is not None:
                        return entity_folder
                return make_folder(name, [])
        
        return make_folder(name, children)
    
    for continent, subregions in hierarchy.items():
        continent_folder = build_hierarchy_folders(subregions, continent)
        top_folders.append(continent_folder)
    
    for err in entity_errors:
        print(err)
    
    doc = make_document("2050 Borders", top_folders, styles_list, style_maps_list)
    kml = build_kml_tree(doc)
    write_kml_file(kml, os.path.join(OUTPUT_DIR, "borders.kml"))
    
    print(f"  Generated {len(entity_polygons)} entity polygons")
    
    return entity_polygons, entity_styles


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
            # Copy polygon from entity borders data (use MultiGeometry for overlays)
            source_entity = overlay.get("source_entity", "")
            if source_entity in entity_polygons:
                poly_data = entity_polygons[source_entity]
                pm = make_placemark_multi(
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
                    " ".join(coords_parts),
                    description=description,
                    style_url=overlay_style_id,
                )
                placemarks.append(pm)
        
        elif overlay_type == "no_polygon":
            # Placemark without polygon (informational only)
            pm = make_placemark(
                name,
                "",
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
    county_path = os.path.join(script_dir, SOURCE_DIR, "us-counties-500k.kml")
    global_path = os.path.join(script_dir, SOURCE_DIR, "global-countries-10m.kml")
    admin1_path = os.path.join(script_dir, SOURCE_DIR, "ne-admin1-10m.kml")
    
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
    global_by_name, global_by_code, global_code_to_name = read_global_kml(global_path)
    print(f"  Loaded {len(global_by_name)} countries by name, {len(global_by_code)} by code")
    print()
    
    admin1_data = {}
    if os.path.exists(admin1_path):
        print("Reading admin-1 KML...")
        admin1_data = read_admin1_kml(admin1_path)
        print(f"  Loaded {len(admin1_data)} admin-1 regions")
        print()
    
    # Generate borders.kml (entity polygons)
    entity_polygons, entity_styles = generate_borders_kml(
        config, county_data, global_by_name, global_by_code, global_code_to_name, admin1_data
    )
    print()
    
    # Generate domain overlay KMLs
    domains = ["climate", "technology", "economy", "demographics", "culture"]
    for domain in domains:
        generate_domain_kml(domain, config, entity_polygons, entity_styles)
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
