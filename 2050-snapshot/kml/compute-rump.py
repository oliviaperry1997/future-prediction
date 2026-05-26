#!/usr/bin/env python3
"""
Compute Canadian Rump geometry by subtracting all carved-out entities
from the full Canada country polygon.

Output: source/manual/Canada.rump.kml
"""

import os
from lxml import etree
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

NS = "http://www.opengis.net/kml/2.2"
TAG = lambda tag: f"{{{NS}}}{tag}"

SCRIPT_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "source", "manual")


def parse_kml_geometry(kml_path):
    """Load all geometries from a KML file into a single merged geometry."""
    tree = etree.parse(kml_path)
    root = tree.getroot()
    parts = []
    for pm in root.findall(f".//{TAG('Placemark')}"):
        multi = pm.find(f".//{TAG('MultiGeometry')}")
        if multi is not None:
            for poly_el in multi.findall(TAG("Polygon")):
                g = parse_polygon(poly_el)
                if g is not None:
                    parts.append(g)
        else:
            poly_el = pm.find(TAG("Polygon"))
            if poly_el is not None:
                g = parse_polygon(poly_el)
                if g is not None:
                    parts.append(g)
    if not parts:
        return None
    merged = unary_union(parts)
    return merged


def parse_polygon(polygon_el):
    outer = polygon_el.find(f".//{TAG('outerBoundaryIs')}/{TAG('LinearRing')}/{TAG('coordinates')}")
    if outer is None or not outer.text:
        return None
    points = []
    for line in outer.text.strip().split():
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) >= 2:
            try:
                points.append((float(parts[0]), float(parts[1])))
            except (ValueError, IndexError):
                continue
    if len(points) < 3:
        return None
    if points[0] != points[-1]:
        points.append(points[0])
    return Polygon(points)


def clean_geometry(geom, min_area=0.001):
    """Remove slivers from a geometry."""
    if geom is None or geom.is_empty:
        return None
    if geom.geom_type == "MultiPolygon":
        polys = [p for p in geom.geoms if p.area >= min_area]
        if not polys:
            return None
        if len(polys) == 1:
            return polys[0]
        return MultiPolygon(polys)
    if geom.geom_type == "Polygon":
        return geom if geom.area >= min_area else None
    return geom


def write_manual_kml(name, geometry, output_path):
    if geometry is None or geometry.is_empty:
        print(f"  WARNING: Empty geometry for {name}, skipping")
        return False
    if geometry.geom_type == "MultiPolygon":
        polys = list(geometry.geoms)
    elif geometry.geom_type == "Polygon":
        polys = [geometry]
    else:
        print(f"  WARNING: Unexpected type {geometry.geom_type} for {name}")
        return False

    kml = etree.Element(TAG("kml"), nsmap={None: NS})
    doc = etree.SubElement(kml, TAG("Document"))
    name_el = etree.SubElement(doc, TAG("name"))
    name_el.text = name

    for poly in polys:
        pm = etree.SubElement(doc, TAG("Placemark"))
        pm_name = etree.SubElement(pm, TAG("name"))
        pm_name.text = name
        polygon_el = etree.SubElement(pm, TAG("Polygon"))
        outer = etree.SubElement(polygon_el, TAG("outerBoundaryIs"))
        ring = etree.SubElement(outer, TAG("LinearRing"))
        coords_el = etree.SubElement(ring, TAG("coordinates"))
        ring_coords = []
        for x, y in poly.exterior.coords:
            ring_coords.append(f"{x:.6f},{y:.6f},0")
        coords_el.text = " ".join(ring_coords)
        for interior in poly.interiors:
            inner = etree.SubElement(polygon_el, TAG("innerBoundaryIs"))
            inner_ring = etree.SubElement(inner, TAG("LinearRing"))
            inner_coords = etree.SubElement(inner_ring, TAG("coordinates"))
            icoords = []
            for x, y in interior.coords:
                icoords.append(f"{x:.6f},{y:.6f},0")
            inner_coords.text = " ".join(icoords)

    xml_bytes = etree.tostring(kml, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    with open(output_path, "wb") as f:
        f.write(xml_bytes)
    print(f"  Written: {output_path} ({len(xml_bytes)} bytes, {len(polys)} polygons)")
    return True


def main():
    # Load full Canada
    print("Loading full Canada polygon...")
    canada = parse_kml_geometry(os.path.join(OUTPUT_DIR, "Canada (full reference).kml"))
    if canada is None:
        print("ERROR: Could not load Canada")
        return
    print(f"  Canada area: {canada.area:.2f}")

    # Load all carved-out entities
    subtract_entities = [
        "Quebec Republic.kml",
        "Maritime Republic.kml",
        "Newfoundland.kml",
        "Manitoba.kml",
        "Denendeh.kml",
        "Inuit Nunangat.kml",
    ]

    subtract_geom = None
    for entity_file in subtract_entities:
        path = os.path.join(OUTPUT_DIR, entity_file)
        if not os.path.exists(path):
            print(f"  WARNING: {entity_file} not found, skipping")
            continue
        g = parse_kml_geometry(path)
        if g is not None:
            print(f"  Loaded {entity_file}: area {g.area:.2f}")
            if subtract_geom is None:
                subtract_geom = g
            else:
                subtract_geom = unary_union([subtract_geom, g])

    if subtract_geom is None:
        print("ERROR: No entities to subtract")
        return

    print(f"\nTotal subtract area: {subtract_geom.area:.2f}")

    # Also subtract Great Lakes (takes islands in the Great Lakes)
    gl_path = os.path.join(OUTPUT_DIR, "Great Lakes.kml")
    if os.path.exists(gl_path):
        gl = parse_kml_geometry(gl_path)
        if gl is not None:
            print(f"  Also subtracting Great Lakes: area {gl.area:.2f}")
            subtract_geom = unary_union([subtract_geom, gl])
            print(f"  Total subtract now: {subtract_geom.area:.2f}")

    # Also subtract Pacifica BC coast (approximate: BC south of 55°N, west of -122°)
    pacifica_path = os.path.join(OUTPUT_DIR, "Pacifica.kml")
    if os.path.exists(pacifica_path):
        pacifica = parse_kml_geometry(pacifica_path)
        if pacifica is not None:
            print(f"  Also subtracting Pacifica: area {pacifica.area:.2f}")
            subtract_geom = unary_union([subtract_geom, pacifica])

    # Compute rump = Canada - all carved entities
    print("\nComputing Canadian Rump (Canada - carved entities)...")
    rump = canada.difference(subtract_geom)
    rump = clean_geometry(rump)
    if rump is None:
        print("ERROR: Rump is empty!")
        return

    print(f"  Rump area: {rump.area:.2f}")
    print(f"  Rump type: {rump.geom_type}")

    # Write rump KML
    rump_path = os.path.join(OUTPUT_DIR, "Canada.rump.kml")
    write_manual_kml("Canada", rump, rump_path)

    # Also write a "Canada" entity that keeps the original name for display
    canada_path = os.path.join(OUTPUT_DIR, "Canada.kml")
    write_manual_kml("Canada", rump, canada_path)

    print("\nDone!")


if __name__ == "__main__":
    main()
