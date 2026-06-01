#!/usr/bin/env python3
"""
Generate KMZ files for rivers and drainage basins as vector geometry.

Rivers: Natural Earth 10m, blue with line width proportional to scalerank.
Basins: HydroBASINS level 4, colored with 25% fill, borderless.

Output:
  rivers.kmz   — all river segments with per-style line widths
  basins.kmz   — all basin polygons with per-id fill colors
"""

import os, subprocess, tempfile, shutil, zipfile, glob, colorsys, xml.etree.ElementTree as ET
import fiona
import fiona.transform
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from shapely.strtree import STRtree

# ── River config ──────────────────────────────────────────────────────────────
NE_RIVERS_URL = "https://naciscdn.org/naturalearth/10m/physical/ne_10m_rivers_lake_centerlines.zip"
NE_RIVERS_ZIP = "source/ne_10m_rivers_lake_centerlines.zip"
RIVER_COLOR   = (40, 100, 220)   # RGB
RIVER_ALPHA   = 220
RIVER_WIDTH   = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 2, 7: 1, 8: 1,
                 9: 1, 10: 1}

# ── Drainage basin config ─────────────────────────────────────────────────────
HYBAS_GLOB       = "source/hybas_*_lev04_v1c.zip"
BASIN_ALPHA      = 128      # ~50%

# ── Output ────────────────────────────────────────────────────────────────────
RIVERS_KMZ = "rivers.kmz"
BASINS_KMZ = "basins.kmz"


# ── KML helpers ───────────────────────────────────────────────────────────────
def kml_color(rgb, alpha):
    """KML hex color = AABBGGRR."""
    r, g, b = rgb
    return f"{alpha:02x}{b:02x}{g:02x}{r:02x}"


def make_element(tag, text=None, attrib=None):
    e = ET.Element(tag, attrib or {})
    if text is not None:
        e.text = text
    return e


def coord_string(geom):
    """Build KML coordinate string from a geometry dict (EPSG:4326)."""
    parts = []
    if geom["type"] == "Polygon":
        for ring in geom["coordinates"]:
            parts.append(" ".join(f"{x},{y},0" for x, y in ring))
        return parts
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            for ring in poly:
                parts.append(" ".join(f"{x},{y},0" for x, y in ring))
        return parts
    return []


def coord_string_line(geom):
    """Build KML coordinate string from a LineString/MultiLineString."""
    coords = []
    if geom["type"] == "LineString":
        coords = geom["coordinates"]
    elif geom["type"] == "MultiLineString":
        for part in geom["coordinates"]:
            coords.extend(part)
    if coords:
        return " ".join(f"{x},{y},0" for x, y in coords)
    return ""


# ── River KMZ ─────────────────────────────────────────────────────────────────
def generate_rivers_kmz():
    os.environ.setdefault("OGR_ENABLE_PARTIAL_REPROJECTION", "TRUE")
    out_path = os.path.join(os.path.dirname(__file__) or ".", RIVERS_KMZ)

    if not os.path.exists(NE_RIVERS_ZIP):
        print("Downloading NE 10m rivers…", flush=True)
        subprocess.run(["curl", "-L", NE_RIVERS_URL, "-o", NE_RIVERS_ZIP], check=True)

    # ── Read features ─────────────────────────────────────────────────────────
    rivers = []  # (name, scalerank, shapely_geom, dict_geom)
    print("Reading river features…")
    with zipfile.ZipFile(NE_RIVERS_ZIP) as zf:
        tmpdir = tempfile.mkdtemp()
        try:
            zf.extractall(tmpdir)
            shp_path = next(
                os.path.join(root, f)
                for root, _, files in os.walk(tmpdir)
                for f in files if f.endswith(".shp")
            )
            with fiona.open(shp_path) as lyr:
                for feat in lyr:
                    g = feat["geometry"]
                    props = feat["properties"]
                    if g is None:
                        continue
                    fc = props.get("featurecla", "")
                    if fc not in ("River", "Lake Centerline", "Intermittent River",
                                  "Intermittent Stream", "Canals", "Canal"):
                        continue
                    sr = props.get("scalerank", 6) or 6
                    name = (props.get("name") or props.get("label") or "").strip()
                    geom = shape(g)
                    if sr <= 6:
                        rivers.append((name or f"River ({fc})", sr, geom, mapping(geom)))
                    else:
                        simplified = geom.simplify(0.001, preserve_topology=True)
                        rivers.append((name or f"River ({fc})", sr, simplified, mapping(simplified)))
        finally:
            shutil.rmtree(tmpdir)

    # Sort by scalerank so major rivers render first (larger width)
    rivers.sort(key=lambda r: r[1])

    # ── Build KML ─────────────────────────────────────────────────────────────
    doc = ET.Element("kml", {"xmlns": "http://www.opengis.net/kml/2.2"})
    document = ET.SubElement(doc, "Document")
    ET.SubElement(document, "name").text = "Rivers (NE 10m)"
    ET.SubElement(document, "description").text = "Natural Earth 10m rivers, styled by scalerank"

    # Define shared styles per river width
    color_str = kml_color(RIVER_COLOR, RIVER_ALPHA)
    style_ids = {}
    for sr, w in sorted(set(RIVER_WIDTH.items())):
        sid = f"river_w{w}"
        style_ids[sr] = sid
        style = ET.SubElement(document, "Style", {"id": sid})
        ls = ET.SubElement(style, "LineStyle")
        ET.SubElement(ls, "color").text = color_str
        ET.SubElement(ls, "width").text = str(w)

    # Add placemarks
    written = 0
    for name, sr, _, geom in rivers:
        w = RIVER_WIDTH.get(sr, 1)
        coords = coord_string_line(geom)
        if not coords or len(coords) < 20:
            continue

        pm = ET.SubElement(document, "Placemark")
        ET.SubElement(pm, "name").text = name
        ET.SubElement(pm, "styleUrl").text = f"#{style_ids.get(sr, 'river_w1')}"

        if geom["type"] in ("LineString", "MultiLineString"):
            ls_elem = ET.SubElement(pm, "LineString")
            ET.SubElement(ls_elem, "tessellate").text = "1"
            ET.SubElement(ls_elem, "altitudeMode").text = "clampToGround"
            ET.SubElement(ls_elem, "coordinates").text = coords
        written += 1

    print(f"  {written} river features")

    # ── Write KMZ ─────────────────────────────────────────────────────────────
    kml_xml = ET.tostring(doc, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("doc.kml", kml_xml)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"  Written: {out_path} ({size_kb:.0f} KB)")

    return rivers


# ── Basin KMZ ─────────────────────────────────────────────────────────────────
def generate_basins_kmz(river_features):
    os.environ.setdefault("OGR_ENABLE_PARTIAL_REPROJECTION", "TRUE")
    out_path = os.path.join(os.path.dirname(__file__) or ".", BASINS_KMZ)
    zips = sorted(glob.glob(HYBAS_GLOB))
    if not zips:
        print("No HydroBASINS zip files found — skipping."); return

    # ── Collect features, simplify geometry ──────────────────────────────────
    SIMPLIFY_TOLERANCE = 0.065  # degrees (~7 km at equator)
    basin_data = []  # (hybas_id, next_down, geometry)
    for zp in zips:
        cont = os.path.basename(zp).split("_")[1]
        print(f"  Reading {cont} basins…")
        with zipfile.ZipFile(zp) as zf:
            tmpdir = tempfile.mkdtemp()
            try:
                zf.extractall(tmpdir)
                shp_path = next(
                    os.path.join(root, f)
                    for root, _, files in os.walk(tmpdir)
                    for f in files if f.endswith(".shp")
                )
                with fiona.open(shp_path) as lyr:
                    for feat in lyr:
                        g = feat["geometry"]
                        if g is None:
                            continue
                        hid = feat["properties"]["HYBAS_ID"]
                        nd = feat["properties"].get("NEXT_DOWN", 0) or 0
                        geom = shape(g)
                        geom_simple = geom.simplify(SIMPLIFY_TOLERANCE,
                                                     preserve_topology=True)
                        basin_data.append((hid, nd, geom_simple))
            finally:
                shutil.rmtree(tmpdir)

    # ── Trace each basin to its ultimate outlet via NEXT_DOWN ───────────────
    next_down = {hid: nd for hid, nd, _ in basin_data}

    def ultimate_outlet(start_hid):
        seen = set()
        hid = start_hid
        while hid in next_down and next_down[hid] not in (0, hid):
            if hid in seen:
                break
            seen.add(hid)
            hid = next_down[hid]
        return hid

    groups = {}
    for hid, nd, geom in basin_data:
        term = ultimate_outlet(hid)
        groups.setdefault(term, []).append(geom)

    # ── Merge geometries per watershed group ────────────────────────────────
    merged_basins = []  # (terminal_id, merged_shapely_geom)
    for term, geoms in groups.items():
        if len(geoms) == 1:
            merged_basins.append((term, geoms[0]))
        else:
            merged_basins.append((term, unary_union(geoms)))
    merged_basins.sort(key=lambda x: x[0])

    print(f"  {len(basin_data)} sub-basins merged into {len(merged_basins)} watersheds")

    # ── Build river name lookup via spatial index ────────────────────────────
    river_geoms = [r[2] for r in river_features]
    river_names = [r[0] for r in river_features]
    river_srs = [r[1] for r in river_features]
    name_tree = STRtree(river_geoms)

    def watershed_name(term, merged_geom):
        candidates = name_tree.query(merged_geom)
        scored = [(i, river_srs[i]) for i in candidates
                  if merged_geom.intersects(river_geoms[i])]
        if not scored:
            return ""
        best = min(scored, key=lambda x: x[1])[0]
        n = river_names[best]
        # Skip generic "River (River)" names
        if n and not n.startswith("River ("):
            return n
        if scored:
            return river_names[min(scored, key=lambda x: x[1])[0]]
        return ""

    # ── Deterministic color per terminal ──────────────────────────────────────
    def terminal_color(hid):
        h = (hash((hid, 0)) & 0xFFFF) / 65536.0
        s = 0.45 + ((hash((hid, 1)) & 0xFF) / 256.0) * 0.3
        v = 0.55 + ((hash((hid, 2)) & 0xFF) / 256.0) * 0.3
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))

    # ── Build KML ─────────────────────────────────────────────────────────────
    doc = ET.Element("kml", {"xmlns": "http://www.opengis.net/kml/2.2"})
    document = ET.SubElement(doc, "Document")
    ET.SubElement(document, "name").text = "Drainage Basins (merged watersheds)"
    ET.SubElement(document, "description").text = "HydroBASINS L4 merged by NEXT_DOWN watershed, colored, borderless"

    # One style per terminal (no outline via PolyStyle only)
    style_map = {}
    for term, _ in merged_basins:
        rgb = terminal_color(term)
        fill_hex = kml_color(rgb, BASIN_ALPHA)
        sid = f"b{term}"
        style_map[term] = (sid, fill_hex)
        style = ET.SubElement(document, "Style", {"id": sid})
        ps = ET.SubElement(style, "PolyStyle")
        ET.SubElement(ps, "color").text = fill_hex
        ET.SubElement(ps, "fill").text = "1"
        ET.SubElement(ps, "outline").text = "0"

    # Add placemarks
    written = 0
    for term, merged_geom in merged_basins:
        sid, fill_hex = style_map[term]
        geom_dict = mapping(merged_geom)
        coord_parts = coord_string(geom_dict)
        if not coord_parts:
            continue

        label = watershed_name(term, merged_geom)
        if not label:
            label = f"Watershed {term}"

        pm = ET.SubElement(document, "Placemark")
        ET.SubElement(pm, "name").text = label
        ET.SubElement(pm, "styleUrl").text = f"#{sid}"

        if geom_dict["type"] == "Polygon":
            poly = ET.SubElement(pm, "Polygon")
            ET.SubElement(poly, "tessellate").text = "1"
            ET.SubElement(poly, "altitudeMode").text = "clampToGround"
            ob = ET.SubElement(poly, "outerBoundaryIs")
            lr = ET.SubElement(ob, "LinearRing")
            ET.SubElement(lr, "coordinates").text = coord_parts[0]
            for inner_coords in coord_parts[1:]:
                ib = ET.SubElement(poly, "innerBoundaryIs")
                lr2 = ET.SubElement(ib, "LinearRing")
                ET.SubElement(lr2, "coordinates").text = inner_coords
        elif geom_dict["type"] == "MultiPolygon":
            for ring_list in geom_dict["coordinates"]:
                poly = ET.SubElement(pm, "Polygon")
                ET.SubElement(poly, "tessellate").text = "1"
                ET.SubElement(poly, "altitudeMode").text = "clampToGround"
                for i, ring in enumerate(ring_list):
                    coords = " ".join(f"{x},{y},0" for x, y in ring)
                    if i == 0:
                        ob = ET.SubElement(poly, "outerBoundaryIs")
                    else:
                        ib = ET.SubElement(poly, "innerBoundaryIs")
                    lr = ET.SubElement(ob if i == 0 else ib, "LinearRing")
                    ET.SubElement(lr, "coordinates").text = coords
        written += 1

    print(f"  {written} merged watershed placemarks")

    # ── Write KMZ ─────────────────────────────────────────────────────────────
    kml_xml = ET.tostring(doc, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("doc.kml", kml_xml)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"  Written: {out_path} ({size_kb:.0f} KB)")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=== Rivers ===")
    river_features = generate_rivers_kmz()

    print("\n=== Drainage Basins ===")
    generate_basins_kmz(river_features)

    print("\nKMZ files written to current directory:")
    for f in [RIVERS_KMZ, BASINS_KMZ]:
        if os.path.exists(f):
            sz = os.path.getsize(f) / 1024
            print(f"  {f} ({sz:.0f} KB)")


if __name__ == "__main__":
    main()
