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


def read_county_kml(path, fallback_path=None, prefer_low_res=None):
    """
    Read US county KML, return {county_identifier: dict} mapping.
    
    Supports two KML formats:
    - Census TIGER/Line (500k): uses GEOID for unique county+city keys
    - Census TIGER/Line (full): same fields, GEOID disambiguates city/county pairs
    
    ExtendedData > SchemaData > SimpleData fields:
      - STATEFP (2-digit FIPS code, e.g., "13")
      - STUSPS (state abbreviation, e.g., "GA")
      - NAMELSAD (full name, e.g., "Brooks County")
      - GEOID (unique identifier, e.g., "13019")
    
    When a fallback_path is provided, entries from the primary file that collide
    on the same "STUSPS|county_name" key (due to missing GEOID in 500k data)
    are replaced with properly-disambiguated entries from the fallback file.
    
    prefer_low_res: dict mapping "STUSPS" -> [county_name, ...]; these counties
                    use the lower-resolution (20m) data for cleaner boundaries.
    
    Returns dict keyed by GEOID (or "STUSPS|county_name" fallback).
    """
    tree = etree.parse(path)
    root = tree.getroot()
    
    placemarks = root.findall(".//kml:Placemark", NSMAP)
    
    county_data = {}
    seen_base_keys = {}
    collision_base_keys = set()
    for pm in placemarks:
        name_el = pm.find("kml:name", NSMAP)
        if name_el is None or not name_el.text:
            continue
        
        county_name = name_el.text.strip()
        
        # Extract ExtendedData fields
        state_fips = None
        state_usps = None
        geo_id = None
        full_name = None
        
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
                    elif field_name == "GEOID" and sd.text:
                        geo_id = sd.text.strip()
                    elif field_name == "NAMELSAD" and sd.text:
                        full_name = sd.text.strip()
        
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
        
        # Use GEOID as key for uniqueness (handles city/county same-name pairs)
        if geo_id:
            key = geo_id
        else:
            base_key = f"{state_usps}|{county_name}"
            if base_key in seen_base_keys:
                collision_base_keys.add(base_key)
            seen_base_keys[base_key] = True
            key = base_key
        
        county_data[key] = {
            "geometry": geom,
            "state_fips": state_fips,
            "state_usps": state_usps,
            "county_name": county_name,
            "full_name": full_name or county_name,
        }
    
    # Phase 2: Replace collided entries with properly-disambiguated fallback data
    if collision_base_keys and fallback_path and os.path.exists(fallback_path):
        fb_tree = etree.parse(fallback_path)
        fb_root = fb_tree.getroot()
        fb_placemarks = fb_root.findall(".//kml:Placemark", NSMAP)
        
        fb_by_name = {}
        for pm in fb_placemarks:
            name_el = pm.find("kml:name", NSMAP)
            if name_el is None or not name_el.text:
                continue
            fb_county_name = name_el.text.strip()
            
            fb_state_usps = None
            fb_geo_id = None
            fb_full_name = None
            ext_data = pm.find("kml:ExtendedData", NSMAP)
            if ext_data is not None:
                schema_data = ext_data.find("kml:SchemaData", NSMAP)
                if schema_data is not None:
                    for sd in schema_data.findall("kml:SimpleData", NSMAP):
                        field_name = sd.get("name", "")
                        if field_name == "STUSPS" and sd.text:
                            fb_state_usps = sd.text.strip()
                        elif field_name == "GEOID" and sd.text:
                            fb_geo_id = sd.text.strip()
                        elif field_name == "NAMELSAD" and sd.text:
                            fb_full_name = sd.text.strip()
            if not fb_state_usps or not fb_geo_id:
                continue
            
            fb_base_key = f"{fb_state_usps}|{fb_county_name}"
            if fb_base_key not in collision_base_keys:
                continue
            
            # Parse geometry
            fb_geom = None
            fb_mg = pm.find(".//kml:MultiGeometry", NSMAP)
            if fb_mg is not None:
                fb_polys = []
                for pe in fb_mg.findall("kml:Polygon", NSMAP):
                    g = parse_kml_polygon(pe)
                    if g is not None:
                        fb_polys.append(g)
                if fb_polys:
                    fb_geom = MultiPolygon(fb_polys) if len(fb_polys) > 1 else fb_polys[0]
            else:
                fb_pe = pm.find("kml:Polygon", NSMAP)
                if fb_pe is not None:
                    fb_geom = parse_kml_polygon(fb_pe)
            if fb_geom is None:
                continue
            
            fb_by_name.setdefault(fb_base_key, []).append({
                "geometry": fb_geom,
                "state_fips": None,
                "state_usps": fb_state_usps,
                "county_name": fb_county_name,
                "full_name": fb_full_name or fb_county_name,
                "geo_id": fb_geo_id,
            })
        
        # Replace collided entries with disambiguated fallback entries
        for base_key in list(collision_base_keys):
            disambig_entries = fb_by_name.get(base_key, [])
            if not disambig_entries:
                continue
            if base_key in county_data:
                del county_data[base_key]
            for entry in disambig_entries:
                disp_key = f"{base_key}|{entry['full_name']}"
                county_data[disp_key] = entry
        
        # Log summary
        for base_key in sorted(collision_base_keys):
            fb_entries = fb_by_name.get(base_key, [])
            fb_names = [e['full_name'] for e in fb_entries]
            print(f"  [fallback] {base_key} → {fb_names}")
    
    # Phase 3: Override specific counties with low-res (20m) data for cleaner boundaries
    if prefer_low_res and fallback_path and os.path.exists(fallback_path):
        lr_tree = etree.parse(fallback_path)
        lr_root = lr_tree.getroot()
        lr_placemarks = lr_root.findall(".//kml:Placemark", NSMAP)
        
        # Build reverse lookup: (STUSPS, county_name) -> key in county_data
        reverse_lookup = {}
        for key, entry in county_data.items():
            stusps = entry.get("state_usps")
            cname = entry.get("county_name")
            if stusps and cname:
                reverse_lookup[(stusps, cname)] = key
        
        for pm in lr_placemarks:
            name_el = pm.find("kml:name", NSMAP)
            if name_el is None or not name_el.text:
                continue
            lr_name = name_el.text.strip()
            
            lr_stusps = None
            ext_data = pm.find("kml:ExtendedData", NSMAP)
            if ext_data is not None:
                schema_data = ext_data.find("kml:SchemaData", NSMAP)
                if schema_data is not None:
                    for sd in schema_data.findall("kml:SimpleData", NSMAP):
                        if sd.get("name", "") == "STUSPS" and sd.text:
                            lr_stusps = sd.text.strip()
            
            if not lr_stusps:
                continue
            
            # Check if this (STUSPS, county_name) is in the override list
            override_names = prefer_low_res.get(lr_stusps, [])
            if lr_name not in override_names:
                continue
            
            # Find existing key
            existing_key = reverse_lookup.get((lr_stusps, lr_name))
            if existing_key is None:
                continue
            
            # Parse geometry from low-res file
            lr_geom = None
            lr_mg = pm.find(".//kml:MultiGeometry", NSMAP)
            if lr_mg is not None:
                lr_polys = []
                for pe in lr_mg.findall("kml:Polygon", NSMAP):
                    g = parse_kml_polygon(pe)
                    if g is not None:
                        lr_polys.append(g)
                if lr_polys:
                    lr_geom = MultiPolygon(lr_polys) if len(lr_polys) > 1 else lr_polys[0]
            else:
                lr_pe = pm.find("kml:Polygon", NSMAP)
                if lr_pe is not None:
                    lr_geom = parse_kml_polygon(lr_pe)
            
            if lr_geom is None:
                print(f"  Warning: no geometry for low-res override '{lr_stusps}|{lr_name}'")
                continue
            
            county_data[existing_key]["geometry"] = lr_geom
            print(f"  [low-res] {lr_stusps}|{lr_name} overridden with 20m data")
    
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


def parse_kml_polygon_element(poly_el):
    """Parse a KML Polygon element (with outer + optional inner rings) into a shapely Polygon."""
    outer = poly_el.find(f'{{{NS}}}outerBoundaryIs/{{{NS}}}LinearRing/{{{NS}}}coordinates')
    if outer is None or not outer.text:
        return None
    outer_poly = parse_coordinates_to_polygon(outer.text.strip())
    if outer_poly is None:
        return None
    inner_rings = []
    for inner in poly_el.findall(f'{{{NS}}}innerBoundaryIs/{{{NS}}}LinearRing/{{{NS}}}coordinates'):
        if inner.text:
            inner_poly = parse_coordinates_to_polygon(inner.text.strip())
            if inner_poly is not None:
                inner_rings.append(inner_poly)
    if inner_rings:
        result = outer_poly
        for ring in inner_rings:
            result = result.difference(ring)
        return result
    return outer_poly


def parse_kml_coordinates_to_polygons(tree_root):
    """Extract all polygons from KML, respecting innerBoundaryIs holes."""
    polys = []
    for poly_el in tree_root.findall(f'.//{{{NS}}}Polygon'):
        p = parse_kml_polygon_element(poly_el)
        if p is not None:
            polys.append(p)
    return polys


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
    
    # Repair and collect valid geometries
    valid = []
    for g in geometries:
        if g is None:
            continue
        if not g.is_valid:
            repaired = g.buffer(0)
            if repaired is not None and not repaired.is_empty and repaired.is_valid:
                valid.append(repaired)
        else:
            valid.append(g)
    
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
    """Douglas-Peucker simplification at mild tolerance (~2.2km).
    Enough to remove redundant vertices from 1:10m Natural Earth data
    while preserving visual fidelity. Vertex count kept under GEP's
    250K limit by combining simplification with overlap removal."""
    if geom is None:
        return None
    try:
        return geom.simplify(tolerance, preserve_topology=True)
    except Exception as e:
        print(f"  Warning: simplification failed ({e}), using unsimplified geometry")
        return geom


def filter_interior_rings(geom, min_area=0.001):
    """
    Remove interior rings (holes) smaller than min_area (in sq degrees).
    For Polygons: drops holes below threshold.
    For MultiPolygons: applies to each sub-polygon individually.
    Returns modified geometry. If no holes to filter, returns original.
    """
    if geom is None or geom.is_empty:
        return geom
    
    if geom.geom_type == "Polygon":
        if not geom.interiors:
            return geom
        kept_rings = [
            ring for ring in geom.interiors
            if Polygon(ring).area >= min_area
        ]
        if len(kept_rings) == len(geom.interiors):
            return geom
        if not kept_rings:
            return Polygon(geom.exterior.coords)
        return Polygon(geom.exterior.coords, kept_rings)
    
    if geom.geom_type == "MultiPolygon":
        new_geoms = []
        for poly in geom.geoms:
            filtered = filter_interior_rings(poly, min_area)
            if filtered is not None and not filtered.is_empty:
                new_geoms.append(filtered)
        if len(new_geoms) == 1:
            return new_geoms[0]
        if new_geoms:
            return MultiPolygon(new_geoms)
        return geom
    
    return geom





def prepare_for_output(geom, entity_cfg):
    """Simplify and manage interior rings based on entity config. Call before geom_to_coords."""
    geom = simplify_polygon(geom, tolerance=0.02)
    if entity_cfg.get("preserve_holes"):
        min_area = entity_cfg.get("min_hole_area", 0.001)
        geom = filter_interior_rings(geom, min_area)
        geom = remove_z_spikes(geom)
    else:
        geom = strip_all_holes(geom)
    return geom


def remove_z_spikes(geom):
    """
    Remove Z-shaped spikes from polygon exterior rings only.
    Detects vertices where the path through the vertex is much longer
    than the direct path (detour ratio > 2.5 AND angle < 60°).
    Catches both short Z-spikes and long V-spikes like the Caswell dip.
    Only applies to Polygons/MultiPolygons. Preserves holes.
    Falls back to original if removal makes the geometry invalid.
    """
    if geom is None or geom.is_empty:
        return geom

    if geom.geom_type == "Polygon":
        orig = list(geom.exterior.coords)
        cleaned = _remove_z_vertices(orig)
        if len(cleaned) < 4:
            return geom
        if len(cleaned) == len(orig) and all(a == b for a, b in zip(cleaned, orig)):
            return geom

        ext_only = Polygon(cleaned)
        if not ext_only.is_valid or ext_only.geom_type != "Polygon":
            ext_only = ext_only.buffer(0)
        if ext_only.geom_type == "MultiPolygon":
            parts = sorted(ext_only.geoms, key=lambda p: p.area, reverse=True)
            ext_only = parts[0]
        if not ext_only.is_valid or ext_only.geom_type != "Polygon":
            return geom

        result = Polygon(list(ext_only.exterior.coords),
                         [list(r.coords) for r in geom.interiors])
        if result.is_valid and result.geom_type == "Polygon":
            return result

        repaired = result.buffer(0)
        if repaired.is_valid and repaired.geom_type == "Polygon":
            return repaired
        return geom

    if geom.geom_type == "MultiPolygon":
        parts = []
        for g in geom.geoms:
            p = remove_z_spikes(g)
            if p is not None and not p.is_empty:
                parts.append(p)
        if not parts:
            return geom
        if len(parts) == 1:
            return parts[0]
        return MultiPolygon(parts)

    return geom


def _remove_z_vertices(ring):
    """
    Remove Z/V-spike vertices — ones where passing through the vertex
    is a detour > 2.5x the direct path and the turn angle < 60°.
    Also removes degenerate zero-length segments left behind after spike removal.
    """
    if len(ring) < 4:
        return ring

    result = list(ring)
    changed = True
    passes = 0
    while changed and passes < 20:
        passes += 1
        changed = False
        new_ring = [result[0]]
        for i in range(1, len(result) - 1):
            prev = new_ring[-1]
            curr = result[i]
            nxt = result[i + 1]

            d1 = _rough_km(prev, curr)
            d2 = _rough_km(curr, nxt)
            dd = _rough_km(prev, nxt)
            angle = _interior_angle(prev, curr, nxt)

            path_ratio = (d1 + d2) / max(dd, 0.001)

            # Remove spike (detour ratio > 2.5, angle < 60°)
            if path_ratio > 2.5 and angle < 60:
                changed = True
                continue

            # Remove degenerate near-zero segment left by spike removal
            if d1 < 0.01 or d2 < 0.01:
                changed = True
                continue

            new_ring.append(curr)

        new_ring.append(result[-1])
        result = new_ring

    if result[0] != result[-1]:
        result.append(result[0])

    return result


def _rough_km(p1, p2):
    """Quick approximate km for short distances (lat in ~36° band)."""
    dlat = (p2[1] - p1[1]) * 111.0
    dlon = (p2[0] - p1[0]) * 111.0 * 0.8
    return (dlat * dlat + dlon * dlon) ** 0.5


def _interior_angle(p1, p2, p3):
    """Angle at p2 in degrees formed by p1-p2-p3."""
    import math
    v1 = (p1[0] - p2[0], p1[1] - p2[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    n1 = (v1[0]**2 + v1[1]**2) ** 0.5
    n2 = (v2[0]**2 + v2[1]**2) ** 0.5
    if n1 < 1e-10 or n2 < 1e-10:
        return 0
    cos_a = max(-1, min(1, dot / (n1 * n2)))
    return math.degrees(math.acos(cos_a))


def strip_all_holes(geom):
    """
    Remove ALL interior rings from a geometry.
    For Polygon: returns Polygon(geom.exterior.coords).
    For MultiPolygon: strips holes from all sub-polygons.
    """
    if geom is None or geom.is_empty:
        return geom
    
    if geom.geom_type == "Polygon":
        return Polygon(geom.exterior.coords)
    
    if geom.geom_type == "MultiPolygon":
        return unary_union([Polygon(p.exterior.coords) for p in geom.geoms])
    
    return geom


def remove_thin_slivers(geom, thinness_threshold=100, min_area=0.0005):
    """
    Remove thin sliver polygons from a MultiPolygon.
    A polygon is considered a sliver if:
      - perimeter^2 / area > thinness_threshold (very elongated)
      - area < min_area sq degrees (very small)
    Returns cleaned geometry, or original if no slivers found.
    """
    if geom is None or geom.is_empty:
        return geom
    if geom.geom_type == "Polygon":
        perim = geom.exterior.length
        ratio = perim * perim / geom.area if geom.area > 0 else 1e9
        if geom.area < min_area:
            return None
        if ratio > thinness_threshold:
            return None
        return geom
    if geom.geom_type == "MultiPolygon":
        kept = []
        for p in geom.geoms:
            if p.area < min_area:
                continue
            perim = p.exterior.length
            ratio = perim * perim / p.area if p.area > 0 else 1e9
            if ratio > thinness_threshold:
                continue
            kept.append(p)
        if not kept:
            return None
        if len(kept) == 1:
            return kept[0]
        return MultiPolygon(kept)
    return geom


def remove_slivers(geom, min_area_ratio=0.00001, min_abs_area=0.00002):
    """
    Remove sliver polygons from a MultiPolygon result (e.g. after difference).
    Keeps only polygons whose area is at least min_area_ratio of the largest polygon,
    and whose absolute area is at least min_abs_area (deg², ~2 km² at 45°N).
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
        keep = [p for p, a in zip(polys, areas) if a >= max_area * min_area_ratio and a >= min_abs_area]
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


def split_into_sides(geom, line):
    """
    Split a geometry along a line and return (sw_union, ne_union).
    Extends the line in both directions to ensure full bisection.
    """
    from shapely.ops import split
    geom = geom.buffer(0)

    # Extend the line in both directions to ensure it fully bisects the geometry
    coords = list(line.coords)
    first = coords[0]
    last = coords[-1]
    # Extend south and north (the Blue Ridge runs roughly N-S through PA)
    south_ext = (first[0], min(first[1] - 0.5, geom.bounds[1] - 0.1))
    north_ext = (last[0], max(last[1] + 0.5, geom.bounds[3] + 0.1))
    extended = LineString([south_ext] + coords + [north_ext])

    try:
        fragments = split(geom, extended)
    except Exception:
        try:
            fragments = split(geom, line.buffer(1e-7))
        except Exception:
            return geom, None

    if fragments.geom_type == 'GeometryCollection':
        pieces = list(fragments.geoms)
    else:
        pieces = [fragments]

    sw_pieces = []
    ne_pieces = []
    for piece in pieces:
        if piece.is_empty:
            continue
        centroid = piece.centroid
        proj_dist = line.project(centroid)
        proj_pt = line.interpolate(min(proj_dist, line.length - 0.00001))
        next_pt = line.interpolate(min(proj_dist + 0.00001, line.length))

        dx = next_pt.x - proj_pt.x
        dy = next_pt.y - proj_pt.y
        cx = centroid.x - proj_pt.x
        cy = centroid.y - proj_pt.y
        cross = dx * cy - dy * cx

        if cross >= -1e-10:
            sw_pieces.append(piece)
        else:
            ne_pieces.append(piece)

    sw_union = unary_union(sw_pieces) if sw_pieces else None
    ne_union = unary_union(ne_pieces) if ne_pieces else None
    return sw_union, ne_union


def geom_to_coords(geom):
    """
    Convert a shapely geometry to KML coordinates string.
    Returns list of dicts with exterior and optional interior rings:
    [{"exterior": str, "interiors": [str, ...]}, ...]
    """
    if geom is None:
        return []
    
    def ring_to_coords(ring):
        coords = []
        for x, y in ring.coords:
            coords.append(f"{x:.6f},{y:.6f},0")
        return " ".join(coords)
    
    result = []
    
    if geom.geom_type == "Polygon":
        exterior = ring_to_coords(geom.exterior)
        if exterior:
            interiors = [ring_to_coords(r) for r in geom.interiors]
            result.append({"exterior": exterior, "interiors": interiors})
    elif geom.geom_type == "MultiPolygon":
        for poly in geom.geoms:
            exterior = ring_to_coords(poly.exterior)
            if exterior:
                interiors = [ring_to_coords(r) for r in poly.interiors]
                result.append({"exterior": exterior, "interiors": interiors})
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


def make_polygon_element(coords_info):
    """
    Create a single KML Polygon element with optional interior rings (holes).
    coords_info: {"exterior": str, "interiors": [str, ...]}
    """
    polygon = etree.Element(f"{{{NS}}}Polygon")
    alt_mode = etree.SubElement(polygon, f"{{{NS}}}altitudeMode")
    alt_mode.text = "clampToGround"
    outer_boundary = etree.SubElement(polygon, f"{{{NS}}}outerBoundaryIs")
    linear_ring = etree.SubElement(outer_boundary, f"{{{NS}}}LinearRing")
    coords_el = etree.SubElement(linear_ring, f"{{{NS}}}coordinates")
    coords_el.text = coords_info["exterior"]
    for interior in coords_info.get("interiors", []):
        inner_boundary = etree.SubElement(polygon, f"{{{NS}}}innerBoundaryIs")
        inner_ring = etree.SubElement(inner_boundary, f"{{{NS}}}LinearRing")
        inner_coords = etree.SubElement(inner_ring, f"{{{NS}}}coordinates")
        inner_coords.text = interior
    return polygon


def make_placemark(name, coords_info, description=None, style_url=None):
    """
    Create a KML Placemark element with a single polygon.
    coords_info is {"exterior": str, "interiors": [str, ...]} or a plain str (backward compat).
    Pass {} or "" for placemarks without geometry (no_polygon type).
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
    
    if coords_info:
        if isinstance(coords_info, str):
            placemark.append(make_polygon_element({"exterior": coords_info, "interiors": []}))
        elif coords_info.get("exterior"):
            placemark.append(make_polygon_element(coords_info))
    
    return placemark


def make_placemark_multi(name, coords_info_list, description=None, style_url=None):
    """
    Create a KML Placemark with multiple polygons wrapped in MultiGeometry.
    Used by domain overlay KMLs where individual polygon styling isn't needed.
    coords_info_list is a list of {"exterior": str, "interiors": [str, ...]} or flat str (backward compat).
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
    
    def wrap(ct):
        if isinstance(ct, str):
            return {"exterior": ct, "interiors": []}
        return ct
    
    if len(coords_info_list) == 1:
        placemark.append(make_polygon_element(wrap(coords_info_list[0])))
    elif len(coords_info_list) > 1:
        multi = etree.SubElement(placemark, f"{{{NS}}}MultiGeometry")
        for ct in coords_info_list:
            multi.append(make_polygon_element(wrap(ct)))
    
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
    remainder_fragments = {}
    
    for entity_name, entity_cfg in config["entities"].items():
        source_type = entity_cfg.get("source", "none")
        
        if source_type == "county":
            clip_cfg = entity_cfg.get("clip_entity")
            
            matches, warnings = match_counties(
                county_data,
                entity_cfg.get("counties", [])
            )
            
            if warnings:
                for w in warnings:
                    entity_errors.append(f"  [{entity_name}] {w}")
            
            merged = merge_polygons(matches)
            if merged is not None:

                # clip_entity: split merged polygon along a border line
                if clip_cfg:
                    try:
                        border_line = load_border_line(os.path.join(script_dir, clip_cfg["line"]))
                        sw, ne = split_into_sides(merged, border_line)
                        if clip_cfg["keep_side"] == "southwest":
                            kept = sw if sw is not None else merged
                            discard = ne
                        else:
                            kept = ne if ne is not None else merged
                            discard = sw
                        kept = remove_slivers(kept)
                        merged = kept
                        # Store discard geometry for remainder donation
                        remainder_target = clip_cfg.get("remainder_entity")
                        if remainder_target and discard is not None and not discard.is_empty:
                            discard = remove_slivers(discard)
                            remainder_fragments.setdefault(remainder_target, []).append(discard)
                    except Exception as e:
                        entity_errors.append(f"  [{entity_name}] clip_entity failed: {e}")

                prepared = prepare_for_output(merged, entity_cfg)

                coords = geom_to_coords(prepared)

                if coords:
                    entity_polygons[entity_name] = {
                        "coords": coords,
                        "geom": merged,
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
                
                # Subtract manual KML geometries from country polygon (e.g., Canada fragmentation)
                subtract_manual_paths = entity_cfg.get("subtract_manual_paths", [])
                if subtract_manual_paths:
                    for manual_path in subtract_manual_paths:
                        full_path = os.path.join(os.path.dirname(__file__), manual_path)
                        if os.path.exists(full_path):
                            manual_tree = etree.parse(full_path)
                            polygons = []
                            for coords_el in manual_tree.findall(f".//{{{NS}}}coordinates"):
                                if coords_el.text:
                                    poly = parse_coordinates_to_polygon(coords_el.text.strip())
                                    if poly is not None:
                                        if not poly.is_valid:
                                            poly = poly.buffer(0)
                                        if poly is not None and not poly.is_empty and poly.is_valid:
                                            polygons.append(poly)
                            if polygons:
                                sub_geom = unary_union(polygons) if len(polygons) > 1 else polygons[0]
                                if not sub_geom.is_valid:
                                    sub_geom = sub_geom.buffer(0)
                                # Tiny buffer (~330m) to absorb minor boundary
                                # misalignment between manual KMLs and Natural
                                # Earth country polygons from different dataset scales
                                sub_buffered = sub_geom.buffer(0.003, join_style=2)
                                geom = geom.difference(sub_buffered)
                                geom = remove_slivers(geom)
                        else:
                            entity_errors.append(f"  [{entity_name}] Subtract manual path not found: {manual_path}")
                
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
                
                simplified = prepare_for_output(geom, entity_cfg)
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
                prepared = prepare_for_output(geom, entity_cfg)
                coords = geom_to_coords(prepared)
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
        
        elif source_type == "admin1_merge":
            country_code = entity_cfg.get("country_code", "CAN")
            provinces = entity_cfg.get("admin1_provinces", [])
            
            geoms = []
            for pname in provinces:
                g = admin1_data.get((country_code, pname))
                if g is not None:
                    geoms.append(g)
                else:
                    entity_errors.append(f"  [{entity_name}] Province '{pname}' in {country_code} not found")
            
            if geoms:
                merged = merge_polygons(geoms)
                
                # Add counties (e.g., Dena'ina Nenn' AK counties → Denendeh)
                add_counties = entity_cfg.get("add_counties", [])
                if add_counties and merged is not None:
                    cm, cw = match_counties(county_data, add_counties)
                    if cw:
                        for w in cw:
                            entity_errors.append(f"  [{entity_name}] add_counties: {w}")
                    if cm:
                        county_merged = merge_polygons(cm)
                        if county_merged is not None:
                            county_merged = remove_slivers(county_merged)
                            merged = merged.union(county_merged)
                
                # Add manual KMLs (e.g., Nunatsiavut/ISR → Inuit Nunangat)
                add_manual_paths = entity_cfg.get("add_manual_paths", [])
                clip_to_land = entity_cfg.get("clip_to_land", False)
                if add_manual_paths and merged is not None:
                    land_union = None
                    if clip_to_land:
                        land_geoms = []
                        for (cc, pname), g in admin1_data.items():
                            if cc == country_code:
                                land_geoms.append(g)
                        if land_geoms:
                            land_union = unary_union(land_geoms)
                            land_union = land_union.buffer(0)
                    for manual_path in add_manual_paths:
                        full_path = os.path.join(script_dir, manual_path)
                        if os.path.exists(full_path):
                            mt = etree.parse(full_path)
                            manual_polys = []
                            for coord_el in mt.findall(f".//{{{NS}}}coordinates"):
                                if coord_el.text:
                                    p = parse_coordinates_to_polygon(coord_el.text.strip())
                                    if p is not None:
                                        if not p.is_valid:
                                            p = p.buffer(0)
                                        if p is not None and not p.is_empty and p.is_valid:
                                            if land_union is not None:
                                                p = p.intersection(land_union)
                                                if p is None or p.is_empty:
                                                    continue
                                                if not p.is_valid:
                                                    p = p.buffer(0)
                                            manual_polys.append(p)
                            if manual_polys:
                                add_geom = unary_union(manual_polys) if len(manual_polys) > 1 else manual_polys[0]
                                merged = merged.union(add_geom)
                        else:
                            entity_errors.append(f"  [{entity_name}] add_manual_paths not found: {manual_path}")
                
                # Add country codes (e.g., Greenland → Inuit Nunangat)
                add_country_codes = entity_cfg.get("add_country_codes", [])
                if add_country_codes and merged is not None:
                    for cc in add_country_codes:
                        g = global_by_code.get(cc)
                        if g is not None:
                            merged = merged.union(g)
                        else:
                            entity_errors.append(f"  [{entity_name}] add_country_codes '{cc}' not found")
                
                # Merge additional admin1 provinces with clip options (e.g., Nunavik QC clip)
                merge_admin1 = entity_cfg.get("merge_admin1", [])
                if merge_admin1 and merged is not None:
                    for mref in merge_admin1:
                        mp = mref.get("province")
                        mclip_lat = mref.get("clip_lat")
                        mclip_side = mref.get("clip_side", "north")
                        mg = admin1_data.get((country_code, mp))
                        if mg is not None:
                            if mclip_lat is not None:
                                from shapely.ops import split as split_fn
                                line = LineString([(-180, mclip_lat), (180, mclip_lat)])
                                try:
                                    mfrags = split_fn(mg, line)
                                except Exception:
                                    mfrags = mg
                                if mfrags.geom_type == 'GeometryCollection':
                                    mpieces = list(mfrags.geoms)
                                else:
                                    mpieces = [mfrags]
                                mkept = [p for p in mpieces if not p.is_empty and (
                                    (mclip_side == "north" and p.centroid.y >= mclip_lat) or
                                    (mclip_side == "south" and p.centroid.y <= mclip_lat)
                                )]
                                if mkept:
                                    mg = unary_union(mkept)
                                else:
                                    mg = None
                            if mg is not None and not mg.is_empty:
                                merged = merged.union(mg)
                        else:
                            entity_errors.append(f"  [{entity_name}] merge_admin1 province '{mp}' not found")
                
                # Subtract manual KMLs (e.g., ISR from NT for Denendeh)
                subtract_manual_paths = entity_cfg.get("subtract_manual_paths", [])
                subtract_buffer = entity_cfg.get("subtract_buffer", 0.003)
                if subtract_manual_paths and merged is not None:
                    for manual_path in subtract_manual_paths:
                        full_path = os.path.join(script_dir, manual_path)
                        if os.path.exists(full_path):
                            mt = etree.parse(full_path)
                            for coord_el in mt.findall(f".//{{{NS}}}coordinates"):
                                if coord_el.text:
                                    p = parse_coordinates_to_polygon(coord_el.text.strip())
                                    if p is not None:
                                        if not p.is_valid:
                                            p = p.buffer(0)
                                        if p is not None and not p.is_empty and p.is_valid:
                                            sub_buffered = p.buffer(subtract_buffer, join_style=2)
                                            merged = merged.difference(sub_buffered)
                            merged = remove_slivers(merged)
                        else:
                            entity_errors.append(f"  [{entity_name}] subtract_manual_paths not found: {manual_path}")
                
                # Clip at latitude (e.g., Canada Rump = Ontario south of 46°N)
                clip_lat = entity_cfg.get("clip_lat")
                if clip_lat is not None and merged is not None:
                    clip_side = entity_cfg.get("clip_side", "south")
                    from shapely.ops import split as split_fn
                    line = LineString([(-180, clip_lat), (180, clip_lat)])
                    try:
                        fragments = split_fn(merged, line)
                    except Exception:
                        fragments = merged
                    if fragments.geom_type == 'GeometryCollection':
                        pieces = list(fragments.geoms)
                    else:
                        pieces = [fragments]
                    kept_pieces = []
                    remainder_pieces = []
                    for piece in pieces:
                        if piece.is_empty:
                            continue
                        centroid = piece.centroid
                        if clip_side == "south":
                            if centroid.y <= clip_lat:
                                kept_pieces.append(piece)
                            else:
                                remainder_pieces.append(piece)
                        else:
                            if centroid.y >= clip_lat:
                                kept_pieces.append(piece)
                            else:
                                remainder_pieces.append(piece)
                    merged = unary_union(kept_pieces) if kept_pieces else None
                    remainder_target = entity_cfg.get("remainder_entity")
                    if remainder_target and remainder_pieces:
                        remainder_geom = unary_union(remainder_pieces)
                        if remainder_geom is not None and not remainder_geom.is_empty:
                            remainder_geom = remove_slivers(remainder_geom)
                            remainder_fragments.setdefault(remainder_target, []).append(remainder_geom)
                
                # Clip along a line (e.g., New Caledonia = BC east of Coast Mountains crest)
                clip_line_path = entity_cfg.get("clip_line")
                if clip_line_path and merged is not None:
                    try:
                        border_line = load_border_line(os.path.join(script_dir, clip_line_path))
                        sw, ne = split_into_sides(merged, border_line)
                        clip_side = entity_cfg.get("clip_side", "east")
                        if clip_side in ("east", "northeast"):
                            kept = ne if ne is not None else merged
                            discard = sw
                        else:
                            kept = sw if sw is not None else merged
                            discard = ne
                        kept = remove_slivers(kept)
                        merged = kept
                        remainder_target = entity_cfg.get("remainder_entity")
                        if remainder_target and discard is not None and not discard.is_empty:
                            discard = remove_slivers(discard)
                            remainder_fragments.setdefault(remainder_target, []).append(discard)
                    except Exception as e:
                        entity_errors.append(f"  [{entity_name}] clip_line failed: {e}")
                
                # Filter by admin2 (e.g., Southern Ontario census divisions)
                admin2_filter = entity_cfg.get("admin2_filter")
                if admin2_filter and merged is not None:
                    try:
                        gadm_path = admin2_filter.get("gadm_path", "")
                        full_gadm_path = os.path.join(script_dir, gadm_path) if not os.path.isabs(gadm_path) else gadm_path
                        if not os.path.exists(full_gadm_path):
                            alt_path = os.path.join(script_dir, "source", os.path.basename(gadm_path))
                            if os.path.exists(alt_path):
                                full_gadm_path = alt_path
                        province = admin2_filter.get("province", "")
                        division_names = set(admin2_filter.get("division_names", []))
                        if os.path.exists(full_gadm_path) and province and division_names:
                            import fiona
                            from shapely.geometry import shape as shp_shape
                            div_geoms = []
                            with fiona.open(full_gadm_path, layer='ADM_ADM_2') as gadm_src:
                                for feat in gadm_src:
                                    props = feat['properties']
                                    if props.get('NAME_1') == province and props.get('NAME_2') in division_names:
                                        g = shp_shape(feat['geometry'])
                                        if g is not None and not g.is_empty and g.is_valid:
                                            div_geoms.append(g)
                            if div_geoms:
                                admin2_union = unary_union(div_geoms)
                                merged = merged.intersection(admin2_union)
                                merged = remove_slivers(merged)
                                remainder_target = entity_cfg.get("remainder_entity")
                                if remainder_target:
                                    non_match_geoms = []
                                    with fiona.open(full_gadm_path, layer='ADM_ADM_2') as gadm_src2:
                                        for feat in gadm_src2:
                                            props = feat['properties']
                                            if props.get('NAME_1') == province and props.get('NAME_2') not in division_names:
                                                # Skip Great Lakes water-body entries (Lake Erie, Hurron, Ontario, Superior)
                                                if props.get('NAME_2', '').startswith('Lake '):
                                                    continue
                                                g = shp_shape(feat['geometry'])
                                                if g is not None and not g.is_empty and g.is_valid:
                                                    non_match_geoms.append(g)
                                    if non_match_geoms:
                                        remainder = unary_union(non_match_geoms)
                                        # Keep lake water in remainder — GADM lake subtraction
                                        # is handled later via subtract_gadm_water in the remainder
                                        # merge section, which avoids double-subtraction slivers
                                        # from misaligned GADM boundaries.
                                        remainder = remove_slivers(remainder)
                                        if remainder is not None and not remainder.is_empty:
                                            remainder_fragments.setdefault(remainder_target, []).append(remainder)
                    except Exception as e:
                        entity_errors.append(f"  [{entity_name}] admin2_filter failed: {e}")
                
                # Subtract GADM water-body entries (e.g., GADM Lake Erie from Canada's Ontario divisions)
                subtract_gadm_water = entity_cfg.get("subtract_gadm_water", {})
                if subtract_gadm_water and merged is not None:
                    try:
                        sw_gadm_path = subtract_gadm_water.get("gadm_path", "")
                        sw_full_path = os.path.join(script_dir, sw_gadm_path) if not os.path.isabs(sw_gadm_path) else sw_gadm_path
                        if not os.path.exists(sw_full_path):
                            sw_alt = os.path.join(script_dir, "source", os.path.basename(sw_gadm_path))
                            if os.path.exists(sw_alt):
                                sw_full_path = sw_alt
                        sw_province = subtract_gadm_water.get("province", "")
                        sw_filters = subtract_gadm_water.get("name_filters", [])
                        if os.path.exists(sw_full_path) and sw_province and sw_filters:
                            import fiona
                            from shapely.geometry import shape as sw_shape
                            sw_water_geoms = []
                            with fiona.open(sw_full_path, layer='ADM_ADM_2') as sw_src:
                                for feat in sw_src:
                                    props = feat['properties']
                                    if props.get('NAME_1') == sw_province:
                                        n2 = props.get('NAME_2', '')
                                        if any(fn in n2 for fn in sw_filters):
                                            g = sw_shape(feat['geometry'])
                                            if g is not None and not g.is_empty and g.is_valid:
                                                sw_water_geoms.append(g)
                            if sw_water_geoms:
                                sw_water_union = unary_union(sw_water_geoms)
                                sw_water_union = sw_water_union.buffer(0.005, join_style=2)
                                merged = merged.difference(sw_water_union)
                                merged = remove_slivers(merged)
                    except Exception as e:
                        entity_errors.append(f"  [{entity_name}] subtract_gadm_water failed: {e}")

                # join_buffer: bridge sub-degree gaps between adjacent source polygons
                join_buffer = entity_cfg.get("join_buffer", 0)
                if join_buffer > 0 and merged is not None:
                    merged = merged.buffer(join_buffer).buffer(-join_buffer)
                    merged = remove_slivers(merged)

                if merged is not None:
                    merged = merged.buffer(0)
                    prepared = prepare_for_output(merged, entity_cfg)
                    coords = geom_to_coords(prepared)
                    if coords:
                        entity_polygons[entity_name] = {
                            "coords": coords,
                            "geom": merged,
                            "type": "admin1_merge",
                            "cfg": entity_cfg,
                        }
                        _, _, style_id = get_entity_style(entity_name)
                        entity_styles[entity_name] = style_id
                else:
                    entity_errors.append(f"  [{entity_name}] No polygon data after merge/clip operations")
            else:
                entity_errors.append(f"  [{entity_name}] No admin1 provinces found for merge")
        
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
                    prepared = prepare_for_output(merged, entity_cfg)
                    coords = geom_to_coords(prepared)
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
                        prepared = prepare_for_output(g, entity_cfg)
                        coords = geom_to_coords(prepared)
                        if coords:
                            entity_polygons[country_name] = {
                                "coords": coords,
                                "type": "country",
                                "cfg": {"source": "country", "country_code": code},
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
                        prepared = prepare_for_output(merged, entity_cfg)
                        coords = geom_to_coords(prepared)
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
                    full_geom_parts = parse_kml_coordinates_to_polygons(manual_root)
                    if full_geom_parts:
                        manual_geom = unary_union(full_geom_parts) if len(full_geom_parts) > 1 else full_geom_parts[0]
                        # Add additional manual KMLs via add_manual_paths (e.g., Tlingit Aaní → Pacifica)
                        add_manual_paths = entity_cfg.get("add_manual_paths", [])
                        if add_manual_paths:
                            for amp in add_manual_paths:
                                amp_full = os.path.join(os.path.dirname(__file__), amp)
                                if os.path.exists(amp_full):
                                    amp_tree = etree.parse(amp_full)
                                    amp_polys = []
                                    for coord_el in amp_tree.findall(f".//{{{NS}}}coordinates"):
                                        if coord_el.text:
                                            p = parse_coordinates_to_polygon(coord_el.text.strip())
                                            if p is not None:
                                                if not p.is_valid:
                                                    p = p.buffer(0)
                                                if p is not None and not p.is_empty and p.is_valid:
                                                    amp_polys.append(p)
                                    if amp_polys:
                                        amp_geom = unary_union(amp_polys) if len(amp_polys) > 1 else amp_polys[0]
                                        manual_geom = manual_geom.union(amp_geom)
                                else:
                                    entity_errors.append(f"  [{entity_name}] add_manual_paths not found: {amp}")
                        # Subtract manual KMLs (e.g., Akimiski Island from Great Lakes)
                        subtract_manual_paths = entity_cfg.get("subtract_manual_paths", [])
                        subtract_buffer = entity_cfg.get("subtract_buffer", 0.003)
                        if subtract_manual_paths:
                            for smp in subtract_manual_paths:
                                smp_full = os.path.join(os.path.dirname(__file__), smp)
                                if os.path.exists(smp_full):
                                    smp_tree = etree.parse(smp_full)
                                    for coord_el in smp_tree.findall(f".//{{{NS}}}coordinates"):
                                        if coord_el.text:
                                            p = parse_coordinates_to_polygon(coord_el.text.strip())
                                            if p is not None:
                                                if not p.is_valid:
                                                    p = p.buffer(0)
                                                if p is not None and not p.is_empty and p.is_valid:
                                                    sub_buffered = p.buffer(subtract_buffer, join_style=2)
                                                    manual_geom = manual_geom.difference(sub_buffered)
                                    manual_geom = remove_slivers(manual_geom)
                                else:
                                    entity_errors.append(f"  [{entity_name}] subtract_manual_paths not found: {smp}")
                        prepared = prepare_for_output(manual_geom, entity_cfg)
                        coords = geom_to_coords(prepared)
                        if coords:
                            entity_polygons[entity_name] = {
                                "coords": coords,
                                "geom": manual_geom,
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
    
    # Merge remainder fragments from clip_entity donations into target entities
    for ename, extra_geoms in remainder_fragments.items():
        if ename in entity_polygons:
            target_geom = entity_polygons[ename].get("geom")
            if target_geom is not None:
                merged_geom = unary_union([target_geom] + extra_geoms)
                # Subtract GADM water bodies from merged remainder (e.g., Great Lakes entity)
                entity_cfg = entity_polygons[ename]["cfg"]
                sw = entity_cfg.get("subtract_gadm_water", {})
                if sw and merged_geom is not None:
                    try:
                        sw_path = sw.get("gadm_path", "")
                        sw_full = os.path.join(script_dir, sw_path) if not os.path.isabs(sw_path) else sw_path
                        if not os.path.exists(sw_full):
                            sw_alt = os.path.join(script_dir, "source", os.path.basename(sw_path))
                            if os.path.exists(sw_alt):
                                sw_full = sw_alt
                        sw_prov = sw.get("province", "")
                        sw_filters = sw.get("name_filters", [])
                        if os.path.exists(sw_full) and sw_prov and sw_filters:
                            import fiona
                            from shapely.geometry import shape as _shp
                            sw_water = []
                            with fiona.open(sw_full, layer='ADM_ADM_2') as _src:
                                for feat in _src:
                                    props = feat['properties']
                                    if props.get('NAME_1') == sw_prov:
                                        n2 = props.get('NAME_2', '')
                                        if any(fn in n2 for fn in sw_filters):
                                            g = _shp(feat['geometry'])
                                            if g is not None and not g.is_empty and g.is_valid:
                                                sw_water.append(g)
                            if sw_water:
                                sw_union = unary_union(sw_water)
                                sw_union = sw_union.buffer(0.005, join_style=2)
                                merged_geom = merged_geom.difference(sw_union)
                                merged_geom = remove_slivers(merged_geom)
                    except Exception as e:
                        entity_errors.append(f"  [{ename}] remainder subtract_gadm_water failed: {e}")
                # Subtract manual KMLs from merged remainder (e.g., Akimiski Island from Great Lakes)
                smp_list = entity_cfg.get("subtract_manual_paths", [])
                subtract_buffer = entity_cfg.get("subtract_buffer", 0.003)
                if smp_list and merged_geom is not None:
                    for smp in smp_list:
                        smp_full = os.path.join(script_dir, smp)
                        if os.path.exists(smp_full):
                            smp_tree = etree.parse(smp_full)
                            for coord_el in smp_tree.findall(f".//{{{NS}}}coordinates"):
                                if coord_el.text:
                                    p = parse_coordinates_to_polygon(coord_el.text.strip())
                                    if p is not None:
                                        if not p.is_valid:
                                            p = p.buffer(0)
                                        if p is not None and not p.is_empty and p.is_valid:
                                            sub_buf = p.buffer(subtract_buffer, join_style=2)
                                            merged_geom = merged_geom.difference(sub_buf)
                            merged_geom = remove_slivers(merged_geom)
                        else:
                            entity_errors.append(f"  [{ename}] remainder subtract_manual_paths not found: {smp}")
                merged_prepared = prepare_for_output(merged_geom, entity_cfg)
                merged_coords = geom_to_coords(merged_prepared)
                if merged_coords:
                    entity_polygons[ename]["coords"] = merged_coords
                    entity_polygons[ename]["geom"] = merged_geom
                    print(f"  Merged donated fragment into {ename} ({len(extra_geoms)} geom(s))")
                else:
                    entity_errors.append(f"  Remainder merge for '{ename}' produced no output")
            else:
                entity_errors.append(f"  Remainder target '{ename}' has no stored geometry")
        else:
            entity_errors.append(f"  Remainder target '{ename}' not found")

    # Post-processing: if Mexico and Texas both specify clip_line to the same file,
    # combine their polygons, split along the border line, and reassign fragments.
    # Only processes dict-format clip_line (admin1_merge uses string path internally).
    clip_pairs = []
    for ename, ecfg in config["entities"].items():
        cl = ecfg.get("clip_line")
        if cl and isinstance(cl, dict):
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
                coord_str = ct["exterior"] if isinstance(ct, dict) else ct
                pts = [(float(p.split(",")[0]), float(p.split(",")[1])) for p in coord_str.strip().split() if "," in p]
                if len(pts) >= 3:
                    if pts[0] != pts[-1]: pts.append(pts[0])
                    try: a_geoms.append(Polygon(pts))
                    except: pass
            
            b_geoms = []
            for ct in poly_b["coords"]:
                coord_str = ct["exterior"] if isinstance(ct, dict) else ct
                pts = [(float(p.split(",")[0]), float(p.split(",")[1])) for p in coord_str.strip().split() if "," in p]
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
                sw_prepared = prepare_for_output(sw_merged, poly_sw.get("cfg", {}))
                sw_coords = geom_to_coords(sw_prepared)
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
                ne_prepared = prepare_for_output(ne_merged, poly_ne.get("cfg", {}))
                ne_coords = geom_to_coords(ne_prepared)
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
                # Count total vertices from all polygon coordinates elements
                total_vertices = 0
                for coords_el in tree.findall(".//kml:coordinates", NSMAP):
                    if coords_el.text:
                        # Count space-separated coordinate tuples; each is a vertex
                        total_vertices += len(coords_el.text.strip().split())
                status = "OK" if total_vertices < 250000 else "OVER LIMIT"
                print(f"  {domain}.kml: {len(placemarks)} placemarks, {total_vertices} vertices, {os.path.getsize(path)} bytes [{status}]")
                if total_vertices >= 250000:
                    all_ok = False
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
    fallback_path = os.path.join(script_dir, SOURCE_DIR, "us-counties.kml")
    low_res_counties = {
        "NC": ["Randolph", "Moore"],
    }
    county_data = read_county_kml(county_path, fallback_path, prefer_low_res=low_res_counties)
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
        print("SUCCESS: All 6 KML files generated (all within 250K vertex limit).")
    else:
        print()
        print("WARNING: Some output files exceeded 250K vertex limit or had errors.")
    
    print()
    print("Per D-19: Open generated KMLs in Google Earth Pro for refinement.")
    print("Douglas-Peucker simplification at 0.02 deg (~2.2km) + overlap removal.")
    print("Approximate overlay polygons will need manual adjustment in Google Earth Pro.")


if __name__ == "__main__":
    main()
