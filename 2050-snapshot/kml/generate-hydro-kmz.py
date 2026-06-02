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
from shapely.geometry import shape, mapping, Polygon, MultiPolygon, Point
from shapely.ops import unary_union
from shapely.strtree import STRtree
from shapely.validation import make_valid

# ── River config ──────────────────────────────────────────────────────────────
NE_RIVERS_URL = "https://naciscdn.org/naturalearth/10m/physical/ne_10m_rivers_lake_centerlines.zip"
NE_RIVERS_ZIP = "source/ne_10m_rivers_lake_centerlines.zip"
NE_LAKES_URL  = "https://naciscdn.org/naturalearth/10m/physical/ne_10m_lakes.zip"
NE_LAKES_ZIP  = "source/ne_10m_lakes.zip"
RIVER_COLOR   = (40, 100, 220)   # RGB
RIVER_ALPHA   = 220
RIVER_WIDTH   = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 2, 7: 1, 8: 1}

# ── Drainage basin config ─────────────────────────────────────────────────────
HYBAS_GLOB       = "source/hybas_*_lev04_v1c.zip"
BASIN_ALPHA      = 128      # ~50%

# ── Endorheic water body name lookup (by terminal MAIN_BAS group) ────────────
ENDORHEIC_NAMES = {
    1040040190: "Lake Chad",
    1040040200: "Okavango Basin",
    4040050210: "Tarim Basin",
    4040050220: "Aral Sea Basin",
    4040050230: "Lake Balkhash",
    5040087590: "Lake Eyre",
}

# NE 10m uses multiple names for the same river at the same scalerank.
# Map segment names to a single canonical name so basins don't get split.
NAME_CANONICAL = {
    "Bahr el Jebel": "Nile",
    "Albert Nile": "Nile",
    "Victoria Nile": "Nile",
    "El Bahr el Abyad": "Nile",
    "El Bahr el Azraq": "Nile",
    "Damietta Branch": "Nile",
    "Rosetta Branch": "Nile",
    "Bahr el  Zeraf": "Nile",
    "Bahr Aouk": "Nile",
    "Jinsha": "Yangtze",
    "Chang Jiang": "Yangtze",
    "Tongtian": "Yangtze",
    "Tuotuo": "Yangtze",
    "Qumar": "Yangtze",
    "Amazonas": "Amazon",
}

# ── Output ────────────────────────────────────────────────────────────────────
RIVERS_KMZ = "rivers.kmz"
BASINS_KMZ = "basins.kmz"


# ── KML helpers ───────────────────────────────────────────────────────────────
def kml_color(rgb, alpha):
    r, g, b = rgb
    return f"{alpha:02x}{b:02x}{g:02x}{r:02x}"

def make_element(tag, text=None, attrib=None):
    e = ET.Element(tag, attrib or {})
    if text is not None:
        e.text = text
    return e

def fmt_coord(x, y):
    return f"{max(-180.0, min(180.0, x))},{y},0"

def coord_string(geom):
    parts = []
    if geom["type"] == "Polygon":
        for ring in geom["coordinates"]:
            parts.append(" ".join(fmt_coord(x, y) for x, y in ring))
        return parts
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            for ring in poly:
                parts.append(" ".join(fmt_coord(x, y) for x, y in ring))
        return parts
    return []

def coord_parts(geom):
    if geom["type"] == "LineString":
        coords = " ".join(fmt_coord(x, y) for x, y in geom["coordinates"])
        return [coords] if len(geom["coordinates"]) >= 3 else []
    elif geom["type"] == "MultiLineString":
        parts = []
        for part in geom["coordinates"]:
            if len(part) >= 3:
                parts.append(" ".join(fmt_coord(x, y) for x, y in part))
        return parts
    return []

# ── Data loading ──────────────────────────────────────────────────────────────
def load_shapefile_zip(zip_path):
    """Extract a shapefile zip to temp dir and return the path to the .shp file."""
    tmpdir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(tmpdir)
    shp = next(os.path.join(root, f) for root, _, files in os.walk(tmpdir) for f in files if f.endswith(".shp"))
    return shp, tmpdir


# ── River KMZ ─────────────────────────────────────────────────────────────────
def generate_rivers_kmz():
    os.environ.setdefault("OGR_ENABLE_PARTIAL_REPROJECTION", "TRUE")
    out_path = os.path.join(os.path.dirname(__file__) or ".", RIVERS_KMZ)

    if not os.path.exists(NE_RIVERS_ZIP):
        print("Downloading NE 10m rivers…", flush=True)
        subprocess.run(["curl", "-L", NE_RIVERS_URL, "-o", NE_RIVERS_ZIP], check=True)

    rivers = []
    print("Reading river features…")
    with zipfile.ZipFile(NE_RIVERS_ZIP) as zf:
        tmpdir = tempfile.mkdtemp()
        try:
            zf.extractall(tmpdir)
            shp_path = next(os.path.join(root, f) for root, _, files in os.walk(tmpdir) for f in files if f.endswith(".shp"))
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
                    if sr >= 9:
                        continue
                    name = (props.get("name") or props.get("label") or "").strip()
                    geom = shape(g)
                    rivers.append((name or f"River ({fc})", sr, geom, mapping(geom)))
        finally:
            shutil.rmtree(tmpdir)

    rivers.sort(key=lambda r: r[1])

    doc = ET.Element("kml", {"xmlns": "http://www.opengis.net/kml/2.2"})
    document = ET.SubElement(doc, "Document")
    ET.SubElement(document, "name").text = "Rivers (NE 10m)"
    ET.SubElement(document, "description").text = "Natural Earth 10m rivers, styled by scalerank"

    color_str = kml_color(RIVER_COLOR, RIVER_ALPHA)
    style_ids = {}
    for sr, w in sorted(set(RIVER_WIDTH.items())):
        sid = f"river_w{w}"
        style_ids[sr] = sid
        style = ET.SubElement(document, "Style", {"id": sid})
        ls = ET.SubElement(style, "LineStyle")
        ET.SubElement(ls, "color").text = color_str
        ET.SubElement(ls, "width").text = str(w)

    written = 0
    for name, sr, _, geom in rivers:
        parts = coord_parts(geom)
        if not parts:
            continue
        pm = ET.SubElement(document, "Placemark")
        ET.SubElement(pm, "name").text = name
        ET.SubElement(pm, "styleUrl").text = f"#{style_ids.get(sr, 'river_w1')}"
        if len(parts) == 1:
            ls_elem = ET.SubElement(pm, "LineString")
            ET.SubElement(ls_elem, "tessellate").text = "1"
            ET.SubElement(ls_elem, "altitudeMode").text = "clampToGround"
            ET.SubElement(ls_elem, "coordinates").text = parts[0]
        else:
            mg = ET.SubElement(pm, "MultiGeometry")
            for part_coords in parts:
                ls_elem = ET.SubElement(mg, "LineString")
                ET.SubElement(ls_elem, "tessellate").text = "1"
                ET.SubElement(ls_elem, "altitudeMode").text = "clampToGround"
                ET.SubElement(ls_elem, "coordinates").text = part_coords
        written += 1

    print(f"  {written} river features")

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

    SIMPLIFY_TOLERANCE = 0.03
    MIN_AREA = 0.001

    # ── Load NE 10m lakes for endorheic naming ─────────────────────────────
    lake_names = []
    lake_geoms = []
    if os.path.exists(NE_LAKES_ZIP):
        print("Loading NE 10m lakes…")
        shp, tmp_lakes = load_shapefile_zip(NE_LAKES_ZIP)
        try:
            with fiona.open(shp) as lyr:
                for feat in lyr:
                    g = feat["geometry"]
                    if g is None:
                        continue
                    n = (feat["properties"].get("name") or "").strip()
                    if not n:
                        continue
                    geom = shape(g)
                    if not geom.is_empty:
                        lake_names.append(n)
                        lake_geoms.append(geom)
            lake_tree = STRtree(lake_geoms)
        finally:
            shutil.rmtree(tmp_lakes)
    else:
        lake_tree = STRtree([])

    # ── Read and clean HydroBASINS sub-basins ──────────────────────────────
    def clean_geom(geom):
        if not geom.is_valid:
            geom = make_valid(geom)
        if geom.is_empty or geom.area < MIN_AREA:
            return None
        if geom.geom_type not in ("Polygon", "MultiPolygon"):
            return None
        if geom.geom_type == "Polygon":
            return None if geom.area < MIN_AREA else Polygon(geom.exterior)
        parts = [Polygon(p.exterior) for p in geom.geoms if p.area >= MIN_AREA]
        if not parts:
            return None
        return MultiPolygon(parts) if len(parts) > 1 else parts[0]

    basin_data = []   # (HYBAS_ID, MAIN_BAS, geometry, is_coastal)
    all_geoms_by_mb = {}   # mb -> [(hid, area, geom, is_coastal)]
    invalid_orig = 0
    for zp in zips:
        cont = os.path.basename(zp).split("_")[1]
        print(f"  Reading {cont} basins…")
        with zipfile.ZipFile(zp) as zf:
            tmpdir = tempfile.mkdtemp()
            try:
                zf.extractall(tmpdir)
                shp_path = next(os.path.join(root, f) for root, _, files in os.walk(tmpdir) for f in files if f.endswith(".shp"))
                with fiona.open(shp_path) as lyr:
                    for feat in lyr:
                        g = feat["geometry"]
                        if g is None:
                            continue
                        props = feat["properties"]
                        hid = props["HYBAS_ID"]
                        mb = props["MAIN_BAS"]
                        coast = props["COAST"]
                        endo = props["ENDO"]
                        geom = shape(g)
                        if not geom.is_valid:
                            invalid_orig += 1
                        geom = clean_geom(geom)
                        if geom is not None:
                            basin_data.append((hid, mb, geom, coast == 1, endo == 1))
                            all_geoms_by_mb.setdefault(mb, []).append((hid, geom.area, geom, coast == 1))
            finally:
                shutil.rmtree(tmpdir)

    # Only used to flag endorheic groups for naming
    endo_mb = set()
    for _, mb, _, _, endo in basin_data:
        if endo:
            endo_mb.add(mb)

    print(f"  {len(basin_data)} cleaned sub-basins ({invalid_orig} invalid original)")

    # ── Group and merge ────────────────────────────────────────────────────
    groups = {}
    coastal_geoms_by_group = {}
    for hid, mb, geom, is_coastal, _ in basin_data:
        groups.setdefault(mb, []).append(geom)
        if is_coastal:
            coastal_geoms_by_group.setdefault(mb, []).append(geom)

    merged = []
    for mb, geoms in groups.items():
        if len(geoms) == 1:
            merged_geom = geoms[0]
        else:
            merged_geom = unary_union(geoms)
        if not merged_geom.is_valid:
            merged_geom = make_valid(merged_geom)
        if merged_geom.is_empty or merged_geom.area < MIN_AREA:
            continue
        if merged_geom.geom_type not in ("Polygon", "MultiPolygon"):
            continue
        merged_geom = merged_geom.simplify(SIMPLIFY_TOLERANCE, preserve_topology=True)
        if merged_geom.is_empty or merged_geom.area < MIN_AREA:
            continue
        if merged_geom.geom_type == "Polygon":
            merged_geom = Polygon(merged_geom.exterior)
        else:
            parts = [Polygon(p.exterior) for p in merged_geom.geoms if p.area >= MIN_AREA]
            if not parts:
                continue
            merged_geom = MultiPolygon(parts) if len(parts) > 1 else parts[0]
        merged.append((mb, merged_geom))

    print(f"  Merged into {len(merged)} watersheds by MAIN_BAS")

    # ── Build river spatial index ──────────────────────────────────────────
    river_geoms = [r[2] for r in river_features]
    river_names = [r[0] for r in river_features]
    river_srs = [r[1] for r in river_features]
    river_tree = STRtree(river_geoms)

    def best_river_name(search_geom):
        candidates = river_tree.query(search_geom)
        name_data = {}
        for i in candidates:
            if not search_geom.intersects(river_geoms[i]):
                continue
            n = river_names[i]
            if not n or n.startswith("River ("):
                continue
            n = NAME_CANONICAL.get(n, n)
            sr = river_srs[i]
            inter_len = search_geom.intersection(river_geoms[i]).length
            if n in name_data:
                curr_sr, curr_len = name_data[n]
                if sr < curr_sr:
                    name_data[n] = (sr, inter_len)
                elif sr == curr_sr:
                    name_data[n] = (curr_sr, curr_len + inter_len)
            else:
                name_data[n] = (sr, inter_len)
        if name_data:
            best = min(name_data.items(), key=lambda x: (x[1][0], -x[1][1]))
            return best[0]
        return ""

    def watershed_name(mb, merged_geom):
        # Endorheic groups: prefer lake / endorheic water-body name over rivers
        if mb in endo_mb:
            if mb in ENDORHEIC_NAMES:
                return ENDORHEIC_NAMES[mb]
            if lake_geoms:
                lakes = [i for i in lake_tree.query(merged_geom)
                         if merged_geom.intersects(lake_geoms[i])]
                if lakes:
                    return lake_names[lakes[0]]
        # 2 — try coastal sub-basin(s) for river name at the ocean outlet
        if mb in coastal_geoms_by_group:
            for coastal_geom in coastal_geoms_by_group[mb]:
                name = best_river_name(coastal_geom)
                if name:
                    return name
        # 3 — no coastal flag set; try smallest sub-basin (= most coastal)
        #     (handles deltaic systems where COAST=1 is not set)
        if mb in all_geoms_by_mb:
            members = sorted(all_geoms_by_mb[mb], key=lambda x: x[1])  # by area asc
            for hid, area, member_geom, is_coastal in members[:3]:
                name = best_river_name(member_geom)
                if name:
                    return name
        # 4 — fall back to merged geometry
        name = best_river_name(merged_geom)
        if name:
            return name
        # 5 — try lake name (non-endorheic groups)
        if lake_geoms:
            lakes = [i for i in lake_tree.query(merged_geom)
                     if merged_geom.intersects(lake_geoms[i])]
            if lakes:
                return lake_names[lakes[0]]
        # 6 — endorheic fallback
        if mb in endo_mb:
            return f"Endorheic Basin ({mb})"
        # 7 — numeric fallback
        return ""

    # ── Deterministic color per MAIN_BAS ──────────────────────────────────────
    def group_color(mb):
        h = (hash((mb, 0)) & 0xFFFF) / 65536.0
        s = 0.45 + ((hash((mb, 1)) & 0xFF) / 256.0) * 0.3
        v = 0.55 + ((hash((mb, 2)) & 0xFF) / 256.0) * 0.3
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))

    # ── Build KML ─────────────────────────────────────────────────────────────
    doc = ET.Element("kml", {"xmlns": "http://www.opengis.net/kml/2.2"})
    document = ET.SubElement(doc, "Document")
    ET.SubElement(document, "name").text = "Drainage Basins (HydroBASINS L4)"
    ET.SubElement(document, "description").text = "HydroBASINS L4 merged by MAIN_BAS"

    for mb, _ in merged:
        rgb = group_color(mb)
        fill_hex = kml_color(rgb, BASIN_ALPHA)
        sid = f"b{mb}"
        style = ET.SubElement(document, "Style", {"id": sid})
        ls = ET.SubElement(style, "LineStyle")
        ET.SubElement(ls, "color").text = "00000000"
        ET.SubElement(ls, "width").text = "1"
        ps = ET.SubElement(style, "PolyStyle")
        ET.SubElement(ps, "color").text = fill_hex
        ET.SubElement(ps, "fill").text = "1"
        ET.SubElement(ps, "outline").text = "1"

    written = 0
    total_vertices = 0
    for mb, merged_geom in merged:
        sid = f"b{mb}"
        coord_parts_list = coord_string(mapping(merged_geom))
        if not coord_parts_list:
            continue

        label = watershed_name(mb, merged_geom)
        if not label:
            label = f"Watershed {mb}"

        pm = ET.SubElement(document, "Placemark")
        ET.SubElement(pm, "name").text = label
        ET.SubElement(pm, "styleUrl").text = f"#{sid}"

        if merged_geom.geom_type == "Polygon":
            poly = ET.SubElement(pm, "Polygon")
            ET.SubElement(poly, "tessellate").text = "1"
            ET.SubElement(poly, "altitudeMode").text = "clampToGround"
            ob = ET.SubElement(poly, "outerBoundaryIs")
            lr = ET.SubElement(ob, "LinearRing")
            ET.SubElement(lr, "coordinates").text = coord_parts_list[0]
            total_vertices += len(coord_parts_list[0].split())
        elif merged_geom.geom_type == "MultiPolygon":
            mg_elem = ET.SubElement(pm, "MultiGeometry")
            for ring_list in mapping(merged_geom)["coordinates"]:
                poly = ET.SubElement(mg_elem, "Polygon")
                ET.SubElement(poly, "tessellate").text = "1"
                ET.SubElement(poly, "altitudeMode").text = "clampToGround"
                ob = ET.SubElement(poly, "outerBoundaryIs")
                coords = " ".join(fmt_coord(x, y) for x, y in ring_list[0])
                lr = ET.SubElement(ob, "LinearRing")
                ET.SubElement(lr, "coordinates").text = coords
                total_vertices += len(ring_list[0])
        written += 1

    print(f"  {written} watershed placemarks, {total_vertices} vertices ({'PASS' if total_vertices <= 250000 else 'FAIL'} — limit 250k)")

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
