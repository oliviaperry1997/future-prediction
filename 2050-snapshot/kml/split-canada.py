#!/usr/bin/env python3
"""
Extract Canada's country polygon and split by admin1 (province/territory)
boundaries. Writes each province as a separate manual KML file for use
in entity-config.json entity definitions.
"""

import os
import sys
from lxml import etree
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

SCRIPT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(SCRIPT_DIR, "source")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "source", "manual")

NS = "http://www.opengis.net/kml/2.2"
TAG = lambda tag: f"{{{NS}}}{tag}"


def parse_geom(pm):
    multi_geom = pm.find(f".//{TAG('MultiGeometry')}")
    if multi_geom is not None:
        polygons = []
        for poly_el in multi_geom.findall(TAG("Polygon")):
            g = _parse_polygon(poly_el)
            if g is not None:
                polygons.append(g)
        if polygons:
            return MultiPolygon(polygons) if len(polygons) > 1 else polygons[0]
    polygon_el = pm.find(TAG("Polygon"))
    if polygon_el is not None:
        return _parse_polygon(polygon_el)
    return None


def _parse_polygon(polygon_el):
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


def get_simple_data(pm, field_name):
    ext = pm.find(TAG("ExtendedData"))
    if ext is not None:
        sd = ext.find(TAG("SchemaData"))
        if sd is not None:
            for s in sd.findall(TAG("SimpleData")):
                if s.get("name", "") == field_name and s.text:
                    return s.text.strip()
    return None


def geom_to_kml_coords(ring):
    coords = []
    for x, y in ring.coords:
        coords.append(f"{x:.6f},{y:.6f},0")
    return " ".join(coords)


def write_manual_kml(name, geometry, output_path):
    if geometry is None or geometry.is_empty:
        print(f"  WARNING: Empty geometry for {name}, skipping")
        return False

    kml = etree.Element(TAG("kml"), nsmap={None: NS})
    doc = etree.SubElement(kml, TAG("Document"))
    name_el = etree.SubElement(doc, TAG("name"))
    name_el.text = name

    if geometry.geom_type == "MultiPolygon":
        polys = list(geometry.geoms)
    elif geometry.geom_type == "Polygon":
        polys = [geometry]
    else:
        print(f"  WARNING: Unexpected type {geometry.geom_type} for {name}")
        return False

    for poly in polys:
        if poly.is_empty:
            continue
        pm = etree.SubElement(doc, TAG("Placemark"))
        pm_name = etree.SubElement(pm, TAG("name"))
        pm_name.text = name

        polygon_el = etree.SubElement(pm, TAG("Polygon"))
        outer = etree.SubElement(polygon_el, TAG("outerBoundaryIs"))
        ring = etree.SubElement(outer, TAG("LinearRing"))
        coords_el = etree.SubElement(ring, TAG("coordinates"))
        coords_el.text = geom_to_kml_coords(poly.exterior)

        for interior in poly.interiors:
            inner = etree.SubElement(polygon_el, TAG("innerBoundaryIs"))
            inner_ring = etree.SubElement(inner, TAG("LinearRing"))
            inner_coords = etree.SubElement(inner_ring, TAG("coordinates"))
            inner_coords.text = geom_to_kml_coords(interior)

    xml_bytes = etree.tostring(kml, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(xml_bytes)
    print(f"  Written: {output_path} ({len(xml_bytes)} bytes)")
    return True


def main():
    print("Loading Canada country polygon...")
    global_kml = os.path.join(SOURCE_DIR, "global-countries.kml")
    tree = etree.parse(global_kml)
    root = tree.getroot()

    canada_geom = None
    for pm in root.findall(f".//{TAG('Placemark')}"):
        name = pm.find(TAG("name"))
        if name is not None and name.text and name.text.strip() == "Canada":
            canada_geom = parse_geom(pm)
            break

    if canada_geom is None:
        print("ERROR: Could not find Canada in global-countries.kml")
        sys.exit(1)
    print(f"  Canada: {canada_geom.geom_type}, area: {canada_geom.area:.2f}")

    ref_path = os.path.join(OUTPUT_DIR, "Canada (full reference).kml")
    write_manual_kml("Canada", canada_geom, ref_path)

    print("\nLoading Canadian admin1 boundaries...")
    admin1_kml = os.path.join(SOURCE_DIR, "ne-admin1-10m.kml")
    tree = etree.parse(admin1_kml)
    root = tree.getroot()

    provinces = {}
    for pm in root.findall(f".//{TAG('Placemark')}"):
        adm0 = get_simple_data(pm, "adm0_a3")
        if adm0 != "CAN":
            continue
        name = pm.find(TAG("name"))
        if name is None or not name.text:
            continue
        prov_name = name.text.strip()
        geom = parse_geom(pm)
        if geom is not None and not geom.is_empty:
            provinces[prov_name] = geom
            print(f"  {prov_name}: {geom.geom_type}, area: {geom.area:.2f}")

    # Individual province KMLs
    print("\nWriting individual province KMLs...")
    province_dir = os.path.join(OUTPUT_DIR, "provinces")
    for name, geom in provinces.items():
        safe_name = name.replace(" ", "_").replace("é", "e")
        path = os.path.join(province_dir, f"{safe_name}.kml")
        write_manual_kml(name, geom, path)

    # Inuit Nunangat: Nunavut + N Quebec (Nunavik) + N Labrador (Nunatsiavut) + Greenland
    print("\nCreating Inuit Nunangat KML...")
    inuit_parts = []

    if "Nunavut" in provinces:
        inuit_parts.append(provinces["Nunavut"])
        print("  Added Nunavut")

    if "Québec" in provinces:
        qc = provinces["Québec"]
        north_clip = Polygon([(-80, 55), (-50, 55), (-50, 65), (-80, 65), (-80, 55)])
        qc_north = qc.intersection(north_clip)
        if not qc_north.is_empty:
            if qc_north.geom_type == "MultiPolygon":
                polys = [p for p in qc_north.geoms if p.area > 0.001]
                qc_north = MultiPolygon(polys) if len(polys) > 1 else polys[0]
            inuit_parts.append(qc_north)
            print(f"  Added Nunavik ({qc_north.area:.2f})")

    if "Newfoundland and Labrador" in provinces:
        nl = provinces["Newfoundland and Labrador"]
        lab_clip = Polygon([(-68, 54), (-55, 54), (-55, 62), (-68, 62), (-68, 54)])
        lab_north = nl.intersection(lab_clip)
        if not lab_north.is_empty:
            if lab_north.geom_type == "MultiPolygon":
                polys = [p for p in lab_north.geoms if p.area > 0.001]
                lab_north = MultiPolygon(polys) if len(polys) > 1 else polys[0]
            inuit_parts.append(lab_north)
            print(f"  Added Nunatsiavut ({lab_north.area:.2f})")

    print("  Loading Greenland...")
    global_kml2 = os.path.join(SOURCE_DIR, "global-countries.kml")
    tree2 = etree.parse(global_kml2)
    root2 = tree2.getroot()
    for pm in root2.findall(f".//{TAG('Placemark')}"):
        name = pm.find(TAG("name"))
        if name is not None and name.text and name.text.strip() == "Greenland":
            grl_geom = parse_geom(pm)
            if grl_geom is not None:
                inuit_parts.append(grl_geom)
                print(f"  Added Greenland ({grl_geom.area:.2f})")
            break

    if inuit_parts:
        inuit_geom = unary_union(inuit_parts)
        inuit_path = os.path.join(OUTPUT_DIR, "Inuit Nunangat.kml")
        write_manual_kml("Inuit Nunangat", inuit_geom, inuit_path)

    # Maritime Republic: NS + NB + PEI
    print("\nCreating Maritime Republic KML...")
    maritime_parts = []
    for prov_name in ["Nova Scotia", "New Brunswick", "Prince Edward Island"]:
        if prov_name in provinces:
            maritime_parts.append(provinces[prov_name])
            print(f"  Added {prov_name}")
    if maritime_parts:
        maritime_geom = unary_union(maritime_parts)
        maritime_path = os.path.join(OUTPUT_DIR, "Maritime Republic.kml")
        write_manual_kml("Maritime Republic", maritime_geom, maritime_path)

    # Quebec (Quebec minus Nunavik)
    print("\nCreating Quebec KML...")
    if "Québec" in provinces:
        qc = provinces["Québec"]
        south_clip = Polygon([(-80, 44), (-50, 44), (-50, 55), (-80, 55), (-80, 44)])
        qc_south = qc.intersection(south_clip)
        if qc_south.is_empty:
            qc_south = qc
        if qc_south.geom_type == "MultiPolygon":
            polys = [p for p in qc_south.geoms if p.area > 0.001]
            qc_south = MultiPolygon(polys) if len(polys) > 1 else polys[0]
        qc_path = os.path.join(OUTPUT_DIR, "Quebec.kml")
        write_manual_kml("Quebec", qc_south, qc_path)

    # Newfoundland (minus Nunatsiavut)
    print("\nCreating Newfoundland KML...")
    if "Newfoundland and Labrador" in provinces:
        nl = provinces["Newfoundland and Labrador"]
        nl_clip = Polygon([(-68, 46), (-52, 46), (-52, 54), (-68, 54), (-68, 46)])
        nl_south = nl.intersection(nl_clip)
        if nl_south.is_empty:
            nl_south = nl
        if nl_south.geom_type == "MultiPolygon":
            polys = [p for p in nl_south.geoms if p.area > 0.001]
            nl_south = MultiPolygon(polys) if len(polys) > 1 else polys[0]
        nl_path = os.path.join(OUTPUT_DIR, "Newfoundland.kml")
        write_manual_kml("Newfoundland", nl_south, nl_path)

    # Denendeh (NWT)
    print("\nCreating Denendeh KML...")
    if "Northwest Territories" in provinces:
        nwt_path = os.path.join(OUTPUT_DIR, "Denendeh.kml")
        write_manual_kml("Denendeh", provinces["Northwest Territories"], nwt_path)

    # Manitoba
    print("\nCreating Manitoba KML...")
    if "Manitoba" in provinces:
        mb_path = os.path.join(OUTPUT_DIR, "Manitoba.kml")
        write_manual_kml("Manitoba", provinces["Manitoba"], mb_path)

    print("\nDone!")


if __name__ == "__main__":
    main()
