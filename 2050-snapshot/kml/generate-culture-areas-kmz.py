#!/usr/bin/env python3
"""
Generate culture areas KMZ for 2050: Cultural Areas, Ideologies, Lingua Franca.

Cultural Areas has two subfolders:
  - Continental Spheres (12 civilizational zones, zone-grouped from culture-zones-base.kml)
  - Regional Areas (88 cultural-geographic zones from culture-zones-base.kml, merged)
"""

import os, sys, json, zipfile, tempfile, shutil, xml.etree.ElementTree as ET
import numpy as np
import rasterio
from rasterio.features import rasterize, shapes as rio_shapes
from shapely.geometry import shape, mapping, MultiPolygon, Polygon, box, Point
from shapely.ops import unary_union
import fiona

SRC_DIR      = os.path.join(os.path.dirname(__file__) or ".", "source")
ETOPO_TIF    = os.path.join(SRC_DIR, "ETOPO_2022_v1_60s_N90W180_surface.tif")
BORDERS_KML  = os.path.join(os.path.dirname(__file__) or ".", "borders.kml")
NE_LAND_ZIP  = os.path.join(SRC_DIR, "ne_10m_land.zip")

OUTPUT_KMZ   = os.path.join(os.path.dirname(__file__) or ".", "culture-areas.kmz")
ZONES_BASE_KML = os.path.join(os.path.dirname(__file__) or ".", "culture-zones-base.kml")
ANT_ZONES_KML  = os.path.join(os.path.dirname(__file__) or ".", "antarctic-zones.kml")
SIMPLIFY     = 0.22
MIN_AREA     = 0.005
MIN_HOLE     = 0.01

# Holes to preserve after all-hole removal:
# continent_id -> [(centroid_lon, centroid_lat, radius_deg, min_area_sqdeg, name)]
HOLE_KEEP = {
    2: [
        (-86.5, 47.5, 1.8, 0.5, "Lake Superior"),
        (-85, 44.5, 2, 0.5, "Lake Michigan-Huron"),
        (-81.2, 42.2, 0.8, 0.5, "Lake Erie"),
        (-77.9, 43.6, 0.8, 0.5, "Lake Ontario"),
        (-98, 53, 1.8, 0.5, "Lake Winnipeg"),
        (-99.5, 52.5, 0.8, 0.5, "Lake Winnipegosis"),
        (-99, 51, 0.8, 0.5, "Lake Manitoba"),
    ],
    1: [
        (50, 41, 4, 1.0, "Caspian Sea"),
        (35, 44, 3, 1.0, "Black Sea"),
    ],
}
SLIVER_RATIO = 200  # P²/A max; higher = more permissive
ENTITY_CONFIG = os.path.join(os.path.dirname(__file__) or ".", "entity-config.json")
ANTARCTIC_DIR = os.path.join(SRC_DIR, "manual", "Antarctica")

KML_NS = "http://www.opengis.net/kml/2.2"

# ── KML helpers ──────────────────────────────────────────────────────────────────

def kml_color(rgb, alpha):
    r, g, b = rgb
    a = int(alpha * 255)
    return f"{a:02x}{b:02x}{g:02x}{r:02x}"

def fmt_coord(x, y):
    return f"{max(-180.0, min(180.0, x))},{y},0"

def coord_parts(geom):
    if geom["type"] == "Polygon":
        return [" ".join(fmt_coord(x, y) for x, y in ring) for ring in geom["coordinates"]]
    return []

def _collect(geom, min_area):
    if geom.is_empty: return []
    if geom.geom_type == "MultiPolygon":
        return [p for p in geom.geoms if p.area >= min_area]
    return [geom] if geom.area >= min_area else []

def _is_sliver(geom):
    """True if geom is a thin sliver (high P²/A, small area)."""
    if geom.area > 1.0:
        return False
    try:
        return geom.length ** 2 / geom.area > SLIVER_RATIO
    except (ZeroDivisionError, ValueError):
        return True

def _build_entity_zone_map(entities, zone_arr, tx):
    """Map entity names to zone IDs by sampling zone_arr at entity centroids."""
    zmap = {}
    if zone_arr is None:
        return zmap
    for en, g in entities.items():
        if g.is_empty or g.centroid.is_empty:
            continue
        c = g.centroid
        col = int((c.x - tx.c) / tx.a)
        row = int((c.y - tx.f) / tx.e)
        if 0 <= row < zone_arr.shape[0] and 0 <= col < zone_arr.shape[1]:
            zid = zone_arr[row, col]
            if zid > 0:
                zmap[en] = int(zid)
    return zmap

def _fill_zone_gaps(zone_arr, land_raster):
    """Fill unclaimed land pixels by dilating each zone into adjacent unclaimed areas."""
    from scipy import ndimage
    z = zone_arr.copy()
    unclaimed = land_raster & (z == 0)
    if not unclaimed.any():
        return z
    for zid in sorted(set(np.unique(z)) - {0}):
        mask = z == zid
        dilated = ndimage.binary_dilation(mask, iterations=2)
        new_pixels = dilated & unclaimed
        z[new_pixels] = zid
        unclaimed[new_pixels] = False
        if not unclaimed.any():
            break
    return z

def _remove_interior_pieces(geoms):
    """Remove polygon pieces entirely inside larger pieces of the same zone."""
    if len(geoms) <= 1:
        return geoms
    sorted_geoms = sorted(geoms, key=lambda g: g.area, reverse=True)
    result = [sorted_geoms[0]]
    for g in sorted_geoms[1:]:
        gb = g.bounds
        inside = False
        for r in result:
            rb = r.bounds
            if (rb[0] - 1e-8 <= gb[0] and rb[1] - 1e-8 <= gb[1] and
                rb[2] + 1e-8 >= gb[2] and rb[3] + 1e-8 >= gb[3]):
                if r.contains(g):
                    inside = True
                    break
        if not inside:
            result.append(g)
    return result

def _clean_holes(geom, min_hole_area, continent_id=None):
    """Remove interior holes. If continent_id is in HOLE_KEEP, preserve only
    holes whose centroid falls within the given radius of a keep-spec centre.
    Otherwise preserve holes larger than min_hole_area."""
    if geom.is_empty or not geom.interiors:
        return geom
    keep_specs = HOLE_KEEP.get(continent_id, [])
    if keep_specs:
        rings = []
        for r in geom.interiors:
            hole = Polygon(r)
            cx = hole.centroid.x
            cy = hole.centroid.y
            for kx, ky, kr, kmin_area, _ in keep_specs:
                if ((cx - kx) ** 2 + (cy - ky) ** 2) ** 0.5 <= kr and hole.area >= kmin_area:
                    rings.append(r)
                    break
    else:
        rings = [r for r in geom.interiors if Polygon(r).area >= min_hole_area]
    if len(rings) == len(geom.interiors):
        return geom
    if not rings:
        return Polygon(geom.exterior)
    return Polygon(geom.exterior, rings)

def vectorize_layered(layers, transform):
    if not layers: return {}
    comp = np.zeros(layers[0][1].shape, dtype=np.uint8)
    for val, mask in layers:
        comp[mask] = val
    out = {}
    for gd, val in rio_shapes(comp, mask=(comp > 0), transform=transform, connectivity=8):
        g = shape(gd)
        if g.is_empty: continue
        g = g.simplify(SIMPLIFY, preserve_topology=True)
        if g.is_empty: continue
        g = g.buffer(0)
        if g.is_empty: continue
        out.setdefault(val, []).extend(_collect(g, MIN_AREA))
    return out

def write_layer(document, parent_folder, name, style_id, geoms, rgb,
                fill_alpha=0.50, line_alpha=0.6, line_width=1):
    if not geoms: return
    style = ET.SubElement(document, "Style", {"id": style_id})
    ls = ET.SubElement(style, "LineStyle")
    ET.SubElement(ls, "color").text = kml_color(rgb, line_alpha)
    ET.SubElement(ls, "width").text = str(line_width)
    ps = ET.SubElement(style, "PolyStyle")
    ET.SubElement(ps, "color").text = kml_color(rgb, fill_alpha)
    ET.SubElement(ps, "fill").text = "1"
    ET.SubElement(ps, "outline").text = "1"
    folder = ET.SubElement(parent_folder, "Folder")
    ET.SubElement(folder, "name").text = name
    pm = ET.SubElement(folder, "Placemark")
    ET.SubElement(pm, "name").text = name
    ET.SubElement(pm, "styleUrl").text = f"#{style_id}"
    mg = ET.SubElement(pm, "MultiGeometry")
    for g in geoms:
        gd = mapping(g)
        parts = coord_parts(gd)
        if not parts: continue
        poly = ET.SubElement(mg, "Polygon")
        ET.SubElement(poly, "tessellate").text = "1"
        ET.SubElement(poly, "altitudeMode").text = "clampToGround"
        ob = ET.SubElement(poly, "outerBoundaryIs")
        ET.SubElement(ET.SubElement(ob, "LinearRing"), "coordinates").text = parts[0]
        for ring in parts[1:]:
            ib = ET.SubElement(poly, "innerBoundaryIs")
            ET.SubElement(ET.SubElement(ib, "LinearRing"), "coordinates").text = ring

# ── Data loading ─────────────────────────────────────────────────────────────────

def _load_shp(zip_path):
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(tmp)
    shp = next(os.path.join(r, f) for r, _, fs in os.walk(tmp)
               for f in fs if f.endswith(".shp"))
    return shp, tmp

def _parse_kml_coords(coords_text):
    pts = []
    for p in coords_text.strip().split():
        parts = p.split(",")
        if len(parts) >= 2:
            pts.append((float(parts[0]), float(parts[1])))
    return pts

def _extract_polygons_from_folder(folder, ns):
    polys = []
    for pm in folder.findall(f"{{{ns}}}Placemark"):
        for poly_el in pm.findall(f".//{{{ns}}}Polygon"):
            outer = poly_el.find(f"{{{ns}}}outerBoundaryIs/{{{ns}}}LinearRing/{{{ns}}}coordinates")
            if outer is None or not outer.text: continue
            rings = [_parse_kml_coords(outer.text)]
            for inner in poly_el.findall(f"{{{ns}}}innerBoundaryIs/{{{ns}}}LinearRing/{{{ns}}}coordinates"):
                if inner.text:
                    rings.append(_parse_kml_coords(inner.text))
            if rings:
                try:
                    polys.append(Polygon(rings[0], rings[1:] if len(rings) > 1 else None))
                except Exception:
                    pass
    for child in folder:
        if child.tag.split("}")[-1] == "Folder":
            polys.extend(_extract_polygons_from_folder(child, ns))
    return polys

def extract_entities(kml_path):
    tree = ET.parse(kml_path)
    doc = tree.getroot().find(f".//{{{KML_NS}}}Document")
    def is_leaf(folder):
        for child in folder:
            if child.tag.split("}")[-1] == "Folder":
                if child.find(f".//{{{KML_NS}}}Placemark") is not None:
                    return False
        return True
    def walk(parent):
        entities = {}
        for child in parent:
            if child.tag.split("}")[-1] != "Folder": continue
            name_el = child.find(f"{{{KML_NS}}}name")
            name = name_el.text if name_el is not None else "?"
            if is_leaf(child):
                polys = _extract_polygons_from_folder(child, KML_NS)
                if polys:
                    entities[name] = unary_union(polys)
            else:
                entities.update(walk(child))
        return entities
    return walk(doc)

def load_base_zones(kml_path):
    """Load zone polygons from the base KML. Returns {name_key: geometry} dict."""
    ns = 'http://www.opengis.net/kml/2.2'
    tree = ET.parse(kml_path)
    zones = {}
    for pm in tree.iter(f'{{{ns}}}Placemark'):
        name_el = pm.find(f'{{{ns}}}name')
        name = name_el.text if name_el is not None else "unknown"
        polys = []
        for poly_el in pm.findall(f'.//{{{ns}}}Polygon'):
            outer = poly_el.find(f'{{{ns}}}outerBoundaryIs/{{{ns}}}LinearRing/{{{ns}}}coordinates')
            if outer is None or not outer.text: continue
            rings = [_parse_kml_coords(outer.text)]
            for inner in poly_el.findall(f'{{{ns}}}innerBoundaryIs/{{{ns}}}LinearRing/{{{ns}}}coordinates'):
                if inner.text:
                    rings.append(_parse_kml_coords(inner.text))
            if rings and len(rings[0]) >= 3:
                try:
                    p = Polygon(rings[0], rings[1:] if len(rings) > 1 else None)
                    if not p.is_empty and p.area > 0:
                        polys.append(p)
                except Exception:
                    pass
        if polys:
            merged = unary_union(polys)
            if not merged.is_empty:
                merged = fix_antimeridian(merged)
                key = name.lower().replace(" ", "_")
                zones[key] = merged
    return zones

def fix_antimeridian(geom):
    """Split antimeridian-crossing polygons into valid -180/180 polygons.

    Zones like chukchi (lon 145-190), aotearoa (165-184), polynesia
    (-185 to -104) have coordinates outside the [-180, 180] grid.
    This shifts them to 0-360 space, clips at 180, and translates
    the east portion back by -360 so both halves are valid in the grid.
    """
    from shapely.affinity import translate
    from shapely.ops import unary_union
    if geom is None or geom.is_empty:
        return geom
    b = geom.bounds
    if b[0] >= -180 and b[2] <= 180:
        return geom
    if geom.geom_type == "MultiPolygon":
        parts = [fix_antimeridian(g) for g in geom.geoms]
        parts = [g for g in parts if not g.is_empty]
        return unary_union(parts) if parts else geom

    def to_360(g):
        if g.is_empty:
            return g
        ext = [(x + 360 if x < 0 else x, y) for x, y in g.exterior.coords]
        ints = []
        for r in g.interiors:
            ints.append([(x + 360 if x < 0 else x, y) for x, y in r.coords])
        p = Polygon(ext, ints)
        return p.buffer(0) if not p.is_valid else p
    poly_360 = to_360(geom)
    if poly_360.is_empty:
        return geom
    splitter_0_180 = box(0, -90, 180, 90)
    splitter_180_360 = box(180, -90, 360, 90)
    west = poly_360.intersection(splitter_0_180)
    east = poly_360.intersection(splitter_180_360)
    if not east.is_empty:
        east = translate(east, xoff=-360)
    parts = [g for g in [west, east] if not g.is_empty and g.geom_type
             in ("Polygon", "MultiPolygon")]
    if not parts:
        return geom
    result = unary_union(parts) if len(parts) > 1 else parts[0]
    return result if result.is_valid else geom


def load_land_geom(zip_path):
    """Load NE 10m land as a Shapely polygon (high-resolution coastline).

    Reads ALL features (11 total) and merges into a single MultiPolygon
    so that small islands are not lost.
    """
    shp_path, tmp_dir = _load_shp(zip_path)
    parts = []
    with fiona.open(shp_path) as lyr:
        for feat in lyr:
            g = shape(feat["geometry"])
            if g.is_empty: continue
            if g.geom_type == "MultiPolygon":
                parts.extend(p for p in g.geoms if not p.is_empty)
            elif g.geom_type == "Polygon":
                parts.append(g)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return MultiPolygon(parts) if parts else MultiPolygon()

def load_antarctic_sectors(config_path, antarctic_dir):
    """Load Antarctic ice-sheet sector KMLs.
    
    Returns dict of entity_name → merged ice-sheet MultiPolygon,
    and a combined MultiPolygon of all sectors.
    """
    with open(config_path) as f:
        cfg = json.load(f)
    entities_cfg = cfg.get("entities", {})
    sectors = {}
    all_parts = []
    for ename, eprops in entities_cfg.items():
        rel_path = eprops.get("antarctic_sector_path")
        if not rel_path:
            continue
        full_path = os.path.join(os.path.dirname(config_path), rel_path)
        if not os.path.exists(full_path):
            print(f"  [WARN] Antarctic sector not found: {full_path}", flush=True)
            continue
        tree = ET.parse(full_path)
        root = tree.getroot()
        parts = []
        for pm in root.findall(f".//{{{KML_NS}}}Placemark"):
            for poly_el in pm.findall(f".//{{{KML_NS}}}Polygon"):
                outer = poly_el.find(f"{{{KML_NS}}}outerBoundaryIs/{{{KML_NS}}}LinearRing/{{{KML_NS}}}coordinates")
                if outer is None or not outer.text:
                    continue
                rings = [_parse_kml_coords(outer.text)]
                for inner in poly_el.findall(f"{{{KML_NS}}}innerBoundaryIs/{{{KML_NS}}}LinearRing/{{{KML_NS}}}coordinates"):
                    if inner.text:
                        rings.append(_parse_kml_coords(inner.text))
                poly = Polygon(rings[0], rings[1:] if len(rings) > 1 else None)
                if not poly.is_empty:
                    parts.append(poly)
        if parts:
            merged = unary_union(parts)
            sectors[ename] = merged
            all_parts.extend(parts if hasattr(merged, 'geoms') else [merged])
    combined = unary_union(all_parts) if all_parts else MultiPolygon()
    return sectors, combined


# ── Zone processing ──────────────────────────────────────────────────────────────

def rasterize_zones(raster_shape, transform, zone_defs, entities, overrides=None, dtype="uint8"):
    pairs = []
    for zone_id, entity_names, *_ in zone_defs:
        polys = []
        for en in entity_names:
            g = entities.get(en)
            if g is not None and not g.is_empty:
                polys.append(g)
        if not polys: continue
        merged = unary_union(polys)
        if merged.is_empty: continue
        pairs.append((merged, zone_id))
    if overrides:
        for zone_id, override_geom in overrides:
            if override_geom.is_empty: continue
            pairs.append((override_geom, zone_id))
    if not pairs: return np.zeros(raster_shape, dtype=dtype)
    arr = rasterize(
        pairs, out_shape=raster_shape, transform=transform,
        fill=0, dtype=dtype, all_touched=True,
    )
    return arr

def zones_from_raster(arr, transform, land_mask):
    result = {}
    comp = np.where(land_mask, arr, 0).astype(arr.dtype)
    for gd, val in rio_shapes(comp, mask=(comp > 0), transform=transform, connectivity=8):
        if val == 0: continue
        g = shape(gd)
        if g.is_empty: continue
        g = g.simplify(SIMPLIFY, preserve_topology=True)
        if g.is_empty: continue
        g = g.buffer(0)
        if g.is_empty: continue
        result.setdefault(int(val), []).extend(_collect(g, MIN_AREA))
    return result

def inject_coastline_islands(polys_dict, zone_arr, tx, coastline, entities, map_dict, max_area=0.02):
    """
    Add small islands from the coastline to zones.
    First tries sampling the zone raster (fast). Falls back to nearest-entity distance.
    """
    if not hasattr(coastline, 'geoms'):
        return
    parts = list(coastline.geoms)
    total = 0
    by_dist = 0
    
    # Precompute entity centroids for distance fallback
    ent_items = [(en, g.centroid) for en, g in entities.items() if not g.is_empty and not g.centroid.is_empty]
    
    for part in parts:
        if part.is_empty or part.area >= max_area:
            continue
        c = part.centroid
        if c.is_empty: continue
        
        zid = 0
        col = int((c.x - tx.c) / tx.a)
        row = int((c.y - tx.f) / tx.e)
        if 0 <= row < zone_arr.shape[0] and 0 <= col < zone_arr.shape[1]:
            zid = zone_arr[row, col]
        
        used_dist = False
        if zid == 0:
            # Fallback: nearest entity by centroid distance (within 10°)
            best_d = float('inf')
            best_en = None
            for en, ec in ent_items:
                d = c.distance(ec)
                if d < best_d:
                    best_d = d
                    best_en = en
            if best_en is not None and best_d < 10:
                zid = map_dict.get(best_en, 0)
                used_dist = True
        
        if zid > 0:
            clipped = part.simplify(0.005, preserve_topology=True).buffer(0)
            if not clipped.is_empty and not _is_sliver(clipped) and clipped.area >= MIN_AREA:
                polys_dict.setdefault(int(zid), []).append(clipped)
                total += 1
                if used_dist:
                    by_dist += 1
    
    if total:
        print(f"    (injected {total} coastline islands, {by_dist} by distance)", flush=True)

def force_coastline_islands(polys_dict, coastline, zid_of, specs):
    """Forcibly assign coastline parts near given coordinates to target zones.
    specs: [(lon, lat, radius_deg, target_zone_name, label), ...]
    """
    if not hasattr(coastline, 'geoms'):
        return
    total = 0
    for cx, cy, radius, zname, label in specs:
        zid = zid_of.get(zname)
        if zid is None: continue
        for part in coastline.geoms:
            if part.is_empty or part.area > 3.0: continue
            c = part.centroid
            if c.is_empty: continue
            if ((c.x - cx) ** 2 + (c.y - cy) ** 2) ** 0.5 <= radius:
                clipped = part.simplify(0.005, preserve_topology=True).buffer(0)
                if not clipped.is_empty and not _is_sliver(clipped) and clipped.area >= MIN_AREA:
                    polys_dict.setdefault(zid, []).append(clipped)
                    total += 1
    if total:
        print(f"    (forced {total} coastline islands to specific zones)", flush=True)

def force_coastline_islands_cont(cont_polys, coastline, specs):
    """Same as force_coastline_islands but specs use direct parent zone IDs.
    specs: [(lon, lat, radius_deg, parent_id, label), ...]
    """
    if not hasattr(coastline, 'geoms'):
        return
    total = 0
    for cx, cy, radius, pid, label in specs:
        for part in coastline.geoms:
            if part.is_empty or part.area > 3.0: continue
            c = part.centroid
            if c.is_empty: continue
            if ((c.x - cx) ** 2 + (c.y - cy) ** 2) ** 0.5 <= radius:
                clipped = part.simplify(0.005, preserve_topology=True).buffer(0)
                if not clipped.is_empty and not _is_sliver(clipped) and clipped.area >= MIN_AREA:
                    cont_polys.setdefault(pid, []).append(clipped)
                    total += 1
    if total:
        print(f"    (forced {total} coastline islands to continental spheres)", flush=True)

def clip_geoms_to_coastline(geoms, coastline):
    out = []
    for g in geoms:
        clipped = g.intersection(coastline)
        if clipped.is_empty: continue
        clipped = clipped.simplify(0.08, preserve_topology=True)
        clipped = clipped.buffer(0)
        if clipped.is_empty: continue
        pieces = _collect(clipped, MIN_AREA)
        # Re-merge touching fragments before sliver filtering
        if len(pieces) > 1:
            merged = unary_union(pieces)
            if merged.geom_type == "MultiPolygon":
                pieces = [p for p in merged.geoms if not p.is_empty]
            else:
                pieces = [merged]
        out.extend(p for p in pieces if not _is_sliver(p))
    return out

# ── Mapping tables ───────────────────────────────────────────────────────────────

CIV_MAP = {
    # 1 = European
    "European Federation": 1, "England": 1, "Russia": 1, "Belarus": 1,
    "Ukraine": 1, "Armenia": 1, "Georgia": 1, "Turkey": 1,
    "Azerbaijan": 1,
    # 2 = Anglo-American
    "Absaroka": 2, "Alaska": 2, "Alleghenia": 2, "Appalachia": 2,
    "Arkansas": 2, "Atlantica": 2, "Bermuda": 2, "Canada": 2,
    "Colorado": 2, "Columbia": 2, "Deseret": 2, "Florida": 2,
    "Front Range Socialist Republic": 2, "Great Lakes": 2, "Heartland": 2,
    "Kentucky": 2, "Manitoba": 2, "Maritimes": 2, "Montana-Wyoming": 2,
    "Neuse": 2, "New Afrika": 2, "New Caledonia": 2,
    "Newfoundland-Labrador": 2, "North Carolina": 2, "Oklahoma": 2,
    "Pacifica": 2, "Prairieland": 2, "Tennessee": 2, "Texas": 2,
    "Virginia": 2,
    # Indigenous entities → Anglo-American
    "Denendeh": 2, "Inuit Nunangat": 2, "Navajoland": 2,
    "Oceti Sakowin": 2, "Sequoyah": 2, "Yup'it-Alutiiq Confederacy": 2,
    # Former Franco-American → Anglo-American
    "Quebec": 2, "St. Pierre and Miquelon": 2,
    # 4 = Arabic
    "Arab Popular Republic": 4, "Ash-Sharqiyah": 4, "Bahrain": 4,
    "Kuwait": 4, "Morocco": 4, "Oman": 4, "Qatar": 4, "Saudi Arabia": 4,
    "United Arab Emirates": 4,
    # 5 = Persian
    "Afghanistan": 5, "Iran": 5, "Tajikistan": 5,
    # 6 = Central Asian
    "Kazakhstan": 6, "Kyrgyzstan": 6, "Turkmenistan": 6, "Uzbekistan": 6,
    # 7 = Hindustani
    "Bangladesh": 7, "Bhutan": 7, "India": 7, "Maldives": 7,
    "Nepal": 7, "Pakistan": 7, "Sri Lanka": 7,
    # 8 = Sinitic
    "China": 8, "Mongolia": 8,
    # 9 = Korean
    "DPRK": 9, "ROK": 9,
    # 10 = Japanese
    "Japan": 10,
    # 11 = Southeast Asian
    "Southeast Asian Federation": 11,
    # 12 = Latin American
    "Argentina": 12, "Belize": 12, "Bolivia": 12, "Brazil": 12,
    "Cayenne": 12, "Chile": 12, "Costa Rica": 12, "El Salvador": 12,
    "Gran Colombia": 12, "Guatemala": 12, "Honduras": 12,
    "Mexico": 12, "Nicaragua": 12, "Panama": 12, "Paraguay": 12,
    "Peru": 12,
    # Antarctic claim → Latin American
    "San Martin": 12,
    # 13 = Caribbean
    "Anguilla": 13, "Antigua and Barb.": 13, "Bahamas": 13,
    "Barbados": 13, "Bonaire": 13, "British Virgin Is.": 13,
    "Cayman Islands": 13, "Cuba": 13, "Curaçao": 13, "Dominica": 13,
    "Dominican Rep.": 13, "Grenada": 13, "Guadeloupe": 13, "Haiti": 13,
    "Jamaica": 13, "Martinique": 13, "Montserrat": 13, "Puerto Rico": 13,
    "Saba": 13, "Saint Lucia": 13, "Saint Martin": 13,
    "St. Barthélemy": 13, "St. Eustatius": 13, "St. Kitts and Nevis": 13,
    "St. Vin. and Gren.": 13, "Trinidad and Tobago": 13,
    "Turks and Caicos Is.": 13,
    "Guyana": 13, "Suriname": 13, "Cayenne": 13,
    # 14 = African
    "Ambazonia": 14, "Angola": 14, "Benin": 14, "Botswana": 14,
    "Cabo Verde": 14, "Cameroon": 14, "Chad": 14, "Côte d'Ivoire": 14,
    "Djibouti": 14, "East African Federation": 14, "Equatorial Guinea": 14,
    "Eritrea": 14, "Eswatini": 14, "Ethiopia": 14, "Gabon": 14,
    "Ghana": 14, "Guinea": 14, "Guinea-Bissau": 14, "Madagascar": 14,
    "Malawi": 14, "Mano River Union": 14, "Mauritius": 14,
    "Mozambique": 14, "Namibia": 14, "Nigeria": 14,
    "São Tomé and Príncipe": 14, "Senegambia": 14, "Seychelles": 14,
    "Federation of Sahel States": 14,
    "South Africa": 14, "Tigray": 14, "Zambia": 14, "Zimbabwe": 14,
    # 15 = Pacific
    "CNMI": 15, "Cook Is.": 15, "Fiji": 15, "Guam": 15, "Hawaii": 15,
    "Kanaky": 15, "Kiribati": 15, "Maohi Nui": 15, "Marshall Is.": 15,
    "Micronesia": 15, "Nauru": 15, "Niue": 15, "Palau": 15,
    "Papua New Guinea": 15, "Pitcairn": 15, "Samoa": 15,
    "Solomon Is.": 15, "Tokelau": 15, "Tonga": 15, "Tuvalu": 15,
    "Vanuatu": 15, "Wallis and Futuna": 15,
    # 17 = Anglo-Australasian
    "Australia": 17, "New Zealand": 17,
    # Indigenous entities → Anglo-American (2)
    "Denendeh": 2, "Inuit Nunangat": 2, "Navajoland": 2,
    "Oceti Sakowin": 2, "Sequoyah": 2, "Yup'it-Alutiiq Confederacy": 2,
}

IDEO_MAP = {
    # ═══════════════════════════════════════════════════════════════════════════
    # Revolutionary III (3) — bright red   →  Stage 4-5 (mature/developed socialism)
    # ═══════════════════════════════════════════════════════════════════════════
    # North America
    "Pacifica": 3,       # Revolutionary Stage 3-4
    "Atlantica": 3,      # Revolutionary Stage 3-4
    "Great Lakes": 3,    # Revolutionary Stage 3-4
    "Mexico": 3,         # Revolutionary Stage 3-4
    # South America
    "Brazil": 3,         # Revolutionary Stage 3-4
    "Gran Colombia": 3,  # Revolutionary Stage 4-5
    # Europe
    "European Federation": 3,  # Revolutionary Stage 5
    "New Zealand": 3,    # Revolutionary Stage 4
    # East Africa
    "East African Federation": 3,  # Revolutionary Stage 3-4
    # East Asia
    "China": 3,          # Revolutionary state-directed model, largest economy
    "DPRK": 3,           # Revolutionary ascendancy
    # Caribbean revolutionary anchor
    "Cuba": 3,           # Anchor of Caribbean revolutionary socialism
    # Pacific
    "Hawaii": 3,         # Revolutionary Stage 3
    "Fiji": 3,           # Revolutionary Stage 3-4
    "Kanaky": 3,         # Revolutionary Stage 3-4
    # Africa stable democracies
    "Cabo Verde": 3,     # Revolutionary Stage 3
    "Botswana": 3,       # Stage 3-4 — stable democratic success story
    "Namibia": 3,        # Stage 3-4 — stable democratic success story
    # Australia
    "Australia": 3,      # Revolutionary Stage 3 — structural pivot complete
    # Iran
    "Iran": 3,           # Stage 4 — entrenched revolutionary institutional hybrid
    # ═══════════════════════════════════════════════════════════════════════════
    # Revolutionary II (2) — medium red  →  Stage 2-3 (established socialism)
    # ═══════════════════════════════════════════════════════════════════════════
    # North America — revolutionary successor states
    "Front Range Socialist Republic": 2,   # Revolutionary Stage 3
    "New Afrika": 2,       # Revolutionary Stage 2-3
    "Alleghenia": 2,       # Revolutionary Stage 2-3
    "Appalachia": 2,       # Revolutionary Stage 2-3
    "Maritimes": 2,        # Revolutionary Stage 2-3
    "Newfoundland-Labrador": 2,  # Revolutionary Stage 2-3
    "Manitoba": 2,         # Revolutionary Stage 2-3
    # Indigenous revolutionary (sovereign socialist / communal)
    "Denendeh": 2,         # Indigenous Sovereign Stage 2-3
    "Inuit Nunangat": 2,   # Indigenous Sovereign Stage 2-3
    "Navajoland": 2,       # Indigenous Sovereign Stage 2-3
    "Oceti Sakowin": 2,    # Indigenous Sovereign Stage 2-3
    "Sequoyah": 2,         # Indigenous Sovereign Stage 2-3
    "Yup'it-Alutiiq Confederacy": 2,  # Indigenous revolutionary
    "Maohi Nui": 2,        # Revolutionary Stage 1-2 — decolonization complete
    # South America
    "Argentina": 2,        # Revolutionary Stage 2-3
    "Bolivia": 2,          # Revolutionary Stage 2-3 (Lithium Triangle)
    "Chile": 2,            # Revolutionary Stage 2-3 (Lithium Triangle)
    "Paraguay": 2,         # Stage 2-3 — buffer between revolutionary blocs
    "Cayenne": 2,          # Stage 2-3 — independent former French department
    "Suriname": 2,         # Stage 2-3 (Guianas Cooperation Council)
    "Guyana": 2,           # Stage 2-3 (Guianas Cooperation Council)
    # Central America
    "Guatemala": 2,        # Revolutionary Stage 2-3 (CAF core)
    "El Salvador": 2,      # Revolutionary Stage 2-3 (CAF core)
    "Honduras": 2,         # Revolutionary Stage 2-3 (CAF)
    "Costa Rica": 2,       # Stage 2-3 — stable democratic outlier
    "Belize": 2,           # Stage 2-3 — CARICOM-CAF bridge
    # Caribbean — Revolutionary and Center-Revolutionary (CARICOM core)
    "Barbados": 2, "Jamaica": 2, "Dominica": 2, "Grenada": 2,
    "St. Vin. and Gren.": 2, "Antigua and Barb.": 2,
    "Saint Lucia": 2, "St. Kitts and Nevis": 2,
    "Martinique": 2, "Guadeloupe": 2,
    "Puerto Rico": 2,      # De facto independent CARICOM member
    # Europe
    "Armenia": 2,          # Early revolutionary — EU associate + Iran security partner
    "Georgia": 2,          # Revolutionary flip ~2029-2031
    # West Africa — Revolutionary
    "Federation of Sahel States": 2,  # Revolutionary Stage 2-3
    "Nigeria": 2,          # Revolutionary Stage 2-3
    "Ghana": 2,            # Revolutionary Stage 2-3
    "Côte d'Ivoire": 2,    # Revolutionary Stage 2-3
    "Mano River Union": 2, # Revolutionary Stage 2-3
    "Senegambia": 2,       # Revolutionary Stage 2-3
    "Benin": 2,            # Revolutionary Stage 2-3
    # East & Southern Africa — Revolutionary
    "Ethiopia": 2,         # Revolutionary Stage 2-3
    "Tigray": 2,           # Revolutionary Stage 2-3
    "Mozambique": 2,       # Stage 2-3 — EAF expansion candidate
    "Malawi": 2,           # Stage 2-3 — EAF accession trajectory
    "Zambia": 2,           # Stage 2-3 — EAF-integrated
    "Angola": 2,           # Stage 3-4 — post-MPLA weak confederal
    "Mauritius": 2,        # Stage 2-3 — BRICS+ financial node
    # Central Africa — Revolutionary
    "Ambazonia": 2,        # Stage 2-3 — independent Anglophone state
    "Gabon": 2,            # Stage 2-3 — EAF-associate
    "Equatorial Guinea": 2, # Stage 2-3 — post-collapse, absorbed by EAF/Gabon
    "São Tomé and Príncipe": 2,  # Stage 2-3 — EAF observer
    "Djibouti": 2,         # Stage 2-3 — EAF absorption trajectory
    # Southern Africa
    "South Africa": 2,     # Stage 3 — dual identity, BRICS+ anchor
    # Asia — SEAF (single federation entity in borders.kml)
    "Southeast Asian Federation": 2,  # Revolutionary Stage 2-4 (encompasses 11 members)
    # South Asia — Revolutionary
    "Bangladesh": 2,       # Stage 2-3 Revolutionary (climate-stressed)
    "Nepal": 2,            # Stage 2 Revolutionary
    "Sri Lanka": 2,        # Stage 2 Revolutionary
    # North Africa / APR — Revolutionary
    "Arab Popular Republic": 2,  # Unified revolutionary nation (encompasses Algeria, Egypt, Libya, Sudan, Tunisia, Yemen, Syria, Iraq, Hejaz/Ash-Sharqiyah, Levant Republic)
    "Ash-Sharqiyah": 2,    # Hejaz separated from Saudi, APR member
    # Pacific Islands — Revolutionary
    "Solomon Is.": 2,      # Revolutionary Stage 2-3
    "Vanuatu": 2,          # Revolutionary Stage 2-3
    "Kiribati": 2,         # Revolutionary Stage 2-3
    "Tuvalu": 2,           # Revolutionary Stage 2-3
    "Samoa": 2,            # Revolutionary Stage 2-3
    # ═══════════════════════════════════════════════════════════════════════════
    # Revolutionary I (1) — dark red  →  Stage 1 (recent/struggling / pre-revolutionary)
    # ═══════════════════════════════════════════════════════════════════════════
    "Columbia": 1,         # Stage 2-3 Flipping — reactionary-origin flipping rev
    "Neuse": 1,            # Research Triangle Area — besieged revolutionary city-state
    "England": 1,          # Late revolutionary flip ~2045-2048, early-stage
    "Peru": 1,             # Stage 1-2 — chronically unstable
    "Panama": 1,           # Stage 2 — pragmatic, transactional
    "Nicaragua": 1,        # Centrist in Central America spectrum
    "Guinea": 1,           # Revolutionary Stage 1-2
    "Guinea-Bissau": 1,    # Revolutionary Stage 1
    "Madagascar": 1,       # Stage 1-2 — long-term EAF alignment prospect
    "Seychelles": 1,       # Stage 1 — tiny archipelago microstate
    "Cameroon": 1,         # Stage 1-2 — fragmented rump, EAF-aligned
    "Chad": 1,             # Stage 1-2 — contested between AES and EAF
    "Eswatini": 1,         # Stage 1-2 — absolute monarchy in reactionary stasis
    # Caribbean — Centrist (CARICOM least ideologically committed)
    "Bahamas": 1,
    "Bonaire": 1, "Curaçao": 1,
    "Saint Martin": 1,
    "Saba": 1, "St. Barthélemy": 1, "St. Eustatius": 1,
    "Turks and Caicos Is.": 1,
    "Dominican Rep.": 1,   # Tends conservative but CARICOM-integrated
    # South Asia — small states
    "Bhutan": 1,           # Stage 1-2 — GNH model, climate-stressed
    "Maldives": 1,         # Stage 1 — climate-existential displacement
    "Mongolia": 1,         # Independent buffer state, revolutionary-adjacent
    # Pacific Islands — Stage 1-2 revolutionary / reorientation
    "Guam": 1, "CNMI": 1,
    "Marshall Is.": 1, "Micronesia": 1,
    "Nauru": 1, "Palau": 1,
    "Cook Is.": 1, "Niue": 1,
    "Tonga": 1, "Tokelau": 1,
    "Wallis and Futuna": 1,
    "Pitcairn": 1,
    "Papua New Guinea": 1, # Stage 1-2 Bifurcation — rev potential unrealised
    "New Caledonia": 1,    # Post-French Pacific territory, early independent
    # Central Asian CAC (revolutionary framework, integration-as-revolution)
    "Kazakhstan": 1,
    "Kyrgyzstan": 1,
    "Tajikistan": 1,
    "Turkmenistan": 1,
    "Uzbekistan": 1,
    # ═══════════════════════════════════════════════════════════════════════════
    # Reactionary III (6) — dark blue  →  Stage 4-5 (crisis/failed capitalism)
    # ═══════════════════════════════════════════════════════════════════════════
    # North America — reactionary rumps
    "Texas": 6,            # Reactionary Stage 4-5
    "Florida": 6,          # Reactionary Stage 5
    "North Carolina": 6,   # Reactionary Stage 5
    "Virginia": 6,         # Reactionary Stage 5
    "Tennessee": 6,        # Reactionary Stage 5
    "Kentucky": 6,         # Reactionary Stage 5
    "Heartland": 6,        # Reactionary Stage 5
    "Arkansas": 6,         # Reactionary Stage 5
    "Oklahoma": 6,         # Reactionary Stage 5
    "Deseret": 6,          # Reactionary Stage 4-5
    "Montana-Wyoming": 6,  # Reactionary Stage 4-5
    "Alaska": 6,           # Stage 5 — shrunken impoverished rump
    "Canada": 6,           # Reactionary Stage 4-5
    "Prairieland": 6,      # Reactionary Stage 5
    "Absaroka": 6,         # Reactionary Stage 4
    "Colorado": 6,         # Reactionary Stage 4
    "Quebec": 6,           # Reactionary Stage 4
    # Asia — reactionary degradation / crisis
    "Japan": 6,            # Slow-motion strategic erosion
    "ROK": 6,              # Reactionary degradation — US scaffolding removed
    "India": 6,            # Stage 3 Reactionary Degradation
    "Pakistan": 6,         # Stage 4-5 Reactionary Degradation
    # Middle East — reactionary crisis
    "Saudi Arabia": 6,     # Stage 4-5 Reactionary — fragmentation trajectory
    "Afghanistan": 6,      # Stage 1 Reactionary — Taliban regime
    "Zimbabwe": 6,         # Stage 4-5 Reactionary Degradation
    # Caribbean — Reactionary (CARICOM spectrum)
    "Haiti": 6,            # Deepest crisis — CARICOM stabilization
    "Trinidad and Tobago": 6,  # Swing state, most resistant to rev trajectory
    # Gulf states — crisis/fragmentation
    "Bahrain": 6,          # Most vulnerable Gulf micro-state
    # Gulf states likely C2 or C3 depending on depth of crisis
    "United Arab Emirates": 6,  # Stage 3 Reactionary — gilded fortress
    "Kuwait": 6,           # Rentier model terminal crisis
    "Qatar": 6,            # Strategic ambiguity, long LNG runway but terminal
    "Oman": 6,             # Neutral intermediary, declining oil
    # South Caucasus — reactionary
    "Azerbaijan": 6,       # Stage 3-4 Reactionary Degradation
    # ═══════════════════════════════════════════════════════════════════════════
    # Reactionary II (5) — medium blue  →  Stage 3 (deteriorating capitalism)
    # ═══════════════════════════════════════════════════════════════════════════
    # Post-Soviet reactionary
    "Russia": 5,           # Declining peripheral power
    "Belarus": 5,          # Reactionary satellite
    "Ukraine": 5,          # Union State republic, reactionary
    # Turkey
    "Turkey": 5,           # Stage 3 Reactionary — neo-Ottoman overextension
    # North African reactionary
    "Morocco": 5,          # Stage 2 — sole non-APR Arab state
    "Eritrea": 5,          # Stage 1-2 Reactionary Stasis
    # Caribbean Center-Reactionary
    "Cayman Islands": 5,
    "British Virgin Is.": 5,
    "Anguilla": 5,
    "Montserrat": 5,
    # Atlantic microstates
    "Bermuda": 5,
    "St. Pierre and Miquelon": 5,
    # Antarctica sector
    "San Martin": 5,
    # ═══════════════════════════════════════════════════════════════════════════
    # Reactionary I (4) — bright blue  →  Stage 1 (stable capitalism)
    # ═══════════════════════════════════════════════════════════════════════════
    # None — no stable capitalist states in 2050
    # (All capitalist states are in some stage of degradation or crisis)
}

LANG_MAP = {
    # 1 = English
    "Pacifica": 1, "Atlantica": 1, "Great Lakes": 1,
    "Front Range Socialist Republic": 1, "New Afrika": 1,
    "Appalachia": 1, "Alleghenia": 1, "Absaroka": 1, "Alaska": 1,
    "Arkansas": 1, "Bermuda": 1, "Canada": 1, "Colorado": 1,
    "Columbia": 1, "Deseret": 1, "England": 1, "Florida": 1,
    "Heartland": 1, "Kentucky": 1, "Manitoba": 1, "Maritimes": 1,
    "Montana-Wyoming": 1, "Neuse": 1, "New Caledonia": 1,
    "Newfoundland-Labrador": 1, "North Carolina": 1, "Oklahoma": 1,
    "Prairieland": 1, "Tennessee": 1, "Texas": 1, "Virginia": 1,
    "Australia": 1, "New Zealand": 1,
    "Papua New Guinea": 1, "Solomon Is.": 1, "Vanuatu": 1,
    "Fiji": 1, "Kiribati": 1, "Marshall Is.": 1, "Micronesia": 1,
    "Nauru": 1, "Samoa": 1, "Tonga": 1, "Tuvalu": 1,
    "Cook Is.": 1, "Niue": 1, "Tokelau": 1, "Pitcairn": 1,
    # Caribbean English
    "Anguilla": 1, "Antigua and Barb.": 1, "Bahamas": 1,
    "Barbados": 1, "British Virgin Is.": 1, "Cayman Islands": 1,
    "Dominica": 1, "Grenada": 1, "Jamaica": 1, "Montserrat": 1,
    "Saba": 1, "Saint Lucia": 1, "St. Eustatius": 1,
    "St. Kitts and Nevis": 1, "St. Vin. and Gren.": 1,
    "Trinidad and Tobago": 1, "Turks and Caicos Is.": 1,
    "Guyana": 1, "Suriname": 1, "Belize": 1,
    "Bonaire": 1, "Curaçao": 1,
    # Pacific
    "Hawaii": 1,
    # Indigenous → English (absorbed into Anglo-American)
    "Denendeh": 1, "Inuit Nunangat": 1, "Navajoland": 1,
    "Oceti Sakowin": 1, "Sequoyah": 1, "Yup'it-Alutiiq Confederacy": 1,
    # East Asia / global lingua franca
    # (Japan, Korea moved to Mandarin; Western Pacific moving to Mandarin)
    # Anglophone Africa
    "Ambazonia": 1, "Botswana": 1, "Eswatini": 1,
    "Ghana": 1,
    "Namibia": 1, "Nigeria": 1, "Mano River Union": 1,
    "South Africa": 1,
    # 2 = Mandarin
    "China": 2, "Mongolia": 2, "Southeast Asian Federation": 2,
    "DPRK": 2, "ROK": 2, "Japan": 2,
    "CNMI": 2, "Guam": 2, "Palau": 2,
    # 3 = Spanish
    "Mexico": 3, "Argentina": 3, "Bolivia": 3, "Chile": 3,
    "Costa Rica": 3, "Cuba": 3, "Dominican Rep.": 3,
    "El Salvador": 3, "Gran Colombia": 3, "Guatemala": 3,
    "Honduras": 3, "Nicaragua": 3, "Panama": 3, "Paraguay": 3,
    "Peru": 3, "Puerto Rico": 3,
    "Saint Martin": 3, "San Martin": 3,
    # 4 = French
    "European Federation": 4, "Quebec": 4, "St. Pierre and Miquelon": 4,
    "Cayenne": 4, "Guadeloupe": 4, "Martinique": 4,
    "St. Barthélemy": 4, "Haiti": 4,
    "Gabon": 4, "Cameroon": 4, "Equatorial Guinea": 4,
    "Benin": 4, "Côte d'Ivoire": 4, "Guinea": 4,
    "Kanaky": 4,
    "Maohi Nui": 4, "Senegambia": 4,
    "Wallis and Futuna": 4,
    # 5 = Portuguese
    "Brazil": 5, "Angola": 5,
    "São Tomé and Príncipe": 5, "Cabo Verde": 5,
    "Guinea-Bissau": 5,
    # 6 = Arabic
    "Arab Popular Republic": 6, "Saudi Arabia": 6,
    "United Arab Emirates": 6, "Bahrain": 6, "Kuwait": 6,
    "Oman": 6, "Qatar": 6, "Ash-Sharqiyah": 6, "Morocco": 6,
    "Djibouti": 6, "Eritrea": 6,
    "Chad": 6, "Federation of Sahel States": 6,
    # 7 = Swahili
    "East African Federation": 7,
    "Malawi": 7, "Zambia": 7,
    "Ethiopia": 7, "Tigray": 7,
    "Mozambique": 7, "Zimbabwe": 7,
    "Madagascar": 7, "Mauritius": 7, "Seychelles": 7,
    # 8 = Russian
    "Russia": 8, "Belarus": 8, "Ukraine": 8,
    "Kazakhstan": 8, "Kyrgyzstan": 8, "Tajikistan": 8,
    "Turkmenistan": 8, "Uzbekistan": 8,
    "Armenia": 8, "Georgia": 8,
    # 9 = Hindustani
    "India": 9, "Pakistan": 9, "Bangladesh": 9,
    "Nepal": 9, "Bhutan": 9, "Sri Lanka": 9, "Maldives": 9,
    "Afghanistan": 9, "Iran": 9,
    # 10 = Turkish
    "Turkey": 10, "Azerbaijan": 10,
}

# ── Layer configs ────────────────────────────────────────────────────────────────

CIV_ZONES = [
    (1, "Hesperia"), (2, "North America"),
    (4, "Arabia"),
    (7, "Hindustan"), (8, "East Asia"),
    (11, "Southeast Asia"), (12, "Latin America"),
    (13, "Caribbean"), (14, "Africa"), (15, "Pacific"),
    (17, "Australasia"),
]

CIV_COLORS = {
    1: (147, 112, 219), 2: (29, 78, 216),
    4: (34, 197, 94),
    7: (249, 115, 22), 8: (239, 68, 68),
    11: (240, 100, 170), 12: (234, 179, 8),
    13: (20, 184, 166), 14: (161, 98, 7), 15: (13, 148, 136),
    17: (6, 182, 212),
}

IDEO_ZONES = [
    (1, "Revolutionary I"), (2, "Revolutionary II"), (3, "Revolutionary III"),
    (5, "Reactionary II"), (6, "Reactionary III"),
]

IDEO_COLORS = {
    1: (160, 25, 25),     # R1 - dark red, recent/struggling revolution
    2: (200, 50, 50),     # R2 - medium red, established socialism
    3: (240, 80, 80),     # R3 - bright red, mature/developed socialism
    5: (30, 80, 200),     # C2 - medium blue, deteriorating capitalism
    6: (10, 40, 120),     # C3 - dark blue, crisis/failed capitalism
}

LANG_ZONES = [
    (1, "English"), (2, "Mandarin"), (3, "Spanish"),
    (4, "French"), (5, "Portuguese"), (6, "Arabic"),
    (7, "Swahili"), (8, "Russian"), (9, "Hindustani"),
    (10, "Turkish"),
]

LANG_COLORS = {
    1: (0, 150, 150),     # English → teal (was Turkish's; avoids red clash with Mandarin)
    2: (169, 34, 22),     # Mandarin → red (original, distinct from Spanish yellow)
    3: (234, 179, 8),     # Spanish ← reverted to original yellow
    4: (1, 47, 154),      # French → European Federation (#012F9A)
    5: (34, 197, 94),     # Portuguese ← reverted to original green
    6: (35, 159, 64),     # Arabic → Arab Popular Republic (#239F40)
    7: (66, 165, 245),    # Swahili → East African Federation (#42a5f5)
    8: (85, 151, 49),     # Russian → Russia (#559731)
    9: (238, 126, 59),    # Hindustani → India (#ee7e3b)
    10: (120, 15, 15),    # Turkish → dark wine red (was teal, given to English)
}

# ── Regional Areas ────────────────────────────────────────────────────────────────

REGIONS_MAP = {
    # European
    "European Federation": 101,
    "England": 102,
    "Russia": 103, "Belarus": 103, "Ukraine": 103,
    "Armenia": 104, "Georgia": 104, "Azerbaijan": 104, "Turkey": 104,
    # Anglo-American
    "Pacifica": 201,
    "Front Range Socialist Republic": 202, "Columbia": 202, "Deseret": 202,
    "Absaroka": 202, "Colorado": 202, "Montana-Wyoming": 202, "Navajoland": 202,
    "Heartland": 203, "Prairieland": 203, "Oceti Sakowin": 203, "Sequoyah": 203,
    "Great Lakes": 204, "Manitoba": 204, "Alleghenia": 204,
    "Atlantica": 205, "Maritimes": 205, "Newfoundland-Labrador": 205, "Appalachia": 205,
    "New Afrika": 206, "Neuse": 206, "North Carolina": 206, "Virginia": 206,
    "Tennessee": 206, "Kentucky": 206, "Arkansas": 206, "Oklahoma": 206,
    "Texas": 207, "Florida": 207,
    "Canada": 208, "Quebec": 208, "Alaska": 208,
    "Denendeh": 208, "Inuit Nunangat": 208, "Yup'it-Alutiiq Confederacy": 208,
    "Bermuda": 209, "St. Pierre and Miquelon": 209,
    "New Caledonia": 210,
    # Arabic
    "Arab Popular Republic": 301,
    "Saudi Arabia": 302, "United Arab Emirates": 302, "Bahrain": 302,
    "Kuwait": 302, "Oman": 302, "Qatar": 302, "Ash-Sharqiyah": 302,
    "Morocco": 303,
    # Persian
    "Iran": 401, "Afghanistan": 401, "Tajikistan": 401,
    # Central Asian
    "Kazakhstan": 501, "Kyrgyzstan": 501, "Uzbekistan": 501, "Turkmenistan": 501,
    # Hindustani
    "Pakistan": 601, "India": 601, "Bangladesh": 601, "Nepal": 601, "Bhutan": 601,
    "Sri Lanka": 602, "Maldives": 602,
    # Sinitic
    "China": 701, "Mongolia": 702,
    # Korean
    "DPRK": 801, "ROK": 801,
    # Japanese
    "Japan": 901,
    # SE Asian
    "Southeast Asian Federation": 1001,
    # Latin American
    "Mexico": 1101, "Guatemala": 1101, "Belize": 1101, "El Salvador": 1101,
    "Honduras": 1101, "Nicaragua": 1101, "Costa Rica": 1101, "Panama": 1101,
    "Gran Colombia": 1102,
    "Brazil": 1103,
    "Peru": 1104, "Bolivia": 1104,
    "Argentina": 1105, "Chile": 1105, "Paraguay": 1105,
    "San Martin": 1106,
    # Caribbean
    "Cuba": 1201, "Jamaica": 1201, "Haiti": 1201, "Dominican Rep.": 1201,
    "Puerto Rico": 1201, "Cayman Islands": 1201, "Bahamas": 1201,
    "Turks and Caicos Is.": 1201,
    "Anguilla": 1202, "Antigua and Barb.": 1202, "Barbados": 1202,
    "Bonaire": 1202, "British Virgin Is.": 1202, "Curaçao": 1202,
    "Dominica": 1202, "Grenada": 1202, "Guadeloupe": 1202,
    "Martinique": 1202, "Montserrat": 1202, "Saba": 1202,
    "Saint Lucia": 1202, "Saint Martin": 1202, "St. Barthélemy": 1202,
    "St. Eustatius": 1202, "St. Kitts and Nevis": 1202,
    "St. Vin. and Gren.": 1202, "Trinidad and Tobago": 1202,
    "Guyana": 1203, "Suriname": 1203, "Cayenne": 1203,
    # African
    "Federation of Sahel States": 1301, "Nigeria": 1301, "Ghana": 1301,
    "Côte d'Ivoire": 1301, "Mano River Union": 1301, "Senegambia": 1301,
    "Benin": 1301, "Guinea": 1301, "Guinea-Bissau": 1301, "Cabo Verde": 1301,
    "Chad": 1301,
    "Cameroon": 1302, "Ambazonia": 1302, "Gabon": 1302,
    "Equatorial Guinea": 1302, "São Tomé and Príncipe": 1302,
    "East African Federation": 1303, "Ethiopia": 1303, "Tigray": 1303,
    "Eritrea": 1303, "Djibouti": 1303,
    "Angola": 1304, "Namibia": 1304, "Botswana": 1304, "South Africa": 1304,
    "Zimbabwe": 1304, "Zambia": 1304, "Malawi": 1304, "Mozambique": 1304,
    "Madagascar": 1304, "Mauritius": 1304, "Seychelles": 1304, "Eswatini": 1304,
    # Pacific
    "Papua New Guinea": 1401, "Solomon Is.": 1401, "Vanuatu": 1401,
    "Fiji": 1401, "Kanaky": 1401,
    "Guam": 1402, "CNMI": 1402, "Marshall Is.": 1402, "Micronesia": 1402,
    "Nauru": 1402, "Palau": 1402, "Kiribati": 1402,
    "Hawaii": 1403, "Maohi Nui": 1403, "Cook Is.": 1403, "Niue": 1403,
    "Samoa": 1403, "Tonga": 1403, "Tuvalu": 1403, "Tokelau": 1403,
    "Pitcairn": 1403, "Wallis and Futuna": 1403,
    # Anglo-Australasian
    "Australia": 1501,
    "New Zealand": 1502,
}

REGION_ZONES = [
    (101, "European Federation"), (102, "British Isles"),
    (103, "Eastern Europe"), (104, "Caucasus & Anatolia"),
    (201, "Pacific Coast"), (202, "Interior Mountain West"),
    (203, "Great Plains"), (204, "Great Lakes Basin"),
    (205, "Atlantic Seaboard"), (206, "Southeast Interior"),
    (207, "Gulf Coast"), (208, "Canada & Arctic"),
    (209, "Atlantic Outposts"), (210, "Pacific Outpost"),
    (301, "Arab Popular Republic"), (302, "Arabian Peninsula"),
    (303, "Maghreb"),
    (401, "Iranian Plateau"),
    (501, "Central Asian Steppe"),
    (601, "Northern Subcontinent"), (602, "Southern Islands"),
    (701, "China Proper"), (702, "Mongolian Plateau"),
    (801, "Korean Peninsula"),
    (901, "Japanese Archipelago"),
    (1001, "Southeast Asian Archipelago"),
    (1101, "Mexico & Central America"), (1102, "Gran Colombia"),
    (1103, "Brazil"), (1104, "Andes"),
    (1105, "Southern Cone"), (1106, "Antarctic Claim"),
    (1201, "Greater Antilles & Bahamas"), (1202, "Lesser Antilles"),
    (1203, "Mainland Guianas"),
    (1301, "West Africa & Sahel"), (1302, "Central Africa & Gulf"),
    (1303, "East Africa & Horn"), (1304, "Southern Africa"),
    (1401, "Melanesia"), (1402, "Micronesia"), (1403, "Polynesia"),
    (1501, "Australia"), (1502, "New Zealand"),
]

# ── Base KML zone parent mapping (for grouping) ────────────────────────────────

ZONE_PARENT = {
    # Anglo-American (2)
    "new_afrika": 2, "california": 2, "atlantica": 2, "columbia_plateau": 2,
    "appalachia": 2, "great_basin": 2, "new_england": 2, "aridoamerica": 12,
    "texas": 2, "great_lakes": 2, "great_plains": 2, "maritimes": 2,
    "ontario": 2, "quebec": 2, "newfoundland": 2, "subarctic": 2,
    "arctic": 2, "arctic_quebec": 2,
    "cascadia": 2,
    # Latin American (12)
    "mesoamerica": 12, "centroamerica": 12, "colombia": 12, "andes": 12,
    "amazon": 12, "brasil_norte": 12, "gran_chaco": 12, "brasil_sur": 12,
    "argentina": 12, "patagonia": 12, "chile": 12, "san_martin": 12,
    # Caribbean (13)
    "carribean_florida": 13,
    # Eurasian (1)
    "western_europe": 1, "central_europe": 1, "southern_europe": 1,
    "scandanavia": 1, "balkans": 1, "russia": 1, "transcaucasia": 1,
    "siberia": 1, "novosibirsk": 1, "vladivostok": 1,
    # Arabic (4)
    "maghreb": 4, "egypt": 4, "levant": 4, "mesopotamia": 4, "arabia": 4,
    "sahara": 4,
    # African (14)
    "sahel": 14, "west_africa": 14, "congo": 14,
    "abyssinia": 14, "swahili": 14, "southern_bantu": 14, "south_africa": 14,
    "kalahari": 14, "madagascar": 14,
    # Persian / Central Asian → Eurasian (1)
    "iranian_plateau": 1, "central_asia": 1,
    # Hindustani (7)
    "indus": 7, "maratha": 7, "hindustan": 7, "bengal": 7, "dravidia": 7,
    # East Asian (8)
    "xinjiang": 8, "manchuria": 8, "northwestern_china": 8, "central_china": 8,
    "tibet": 8, "southwestern_china": 8, "south_china": 8, "mongolia": 8,
    "korea": 8, "japan": 8,
    # Paleosiberian → reintegrated into Hesperia (1)
    "yakutia": 1, "chukchi": 1,
    # SE Asian (11)
    "southeast_asia": 11, "vietnam": 11, "malaya": 11, "philippines": 11,
    # Pacific (15)
    "melanesia": 15, "polynesia": 15, "micronesia": 15,
    # Anglo-Australasian (17)
    "east_australia": 17, "north_australia": 17, "west_australia": 17,
    "desert_australia": 17, "aotearoa": 17,
}

ZONE_DISPLAY = {
    "new_afrika": "New Afrika", "california": "California",
    "atlantica": "Atlantica", "columbia_plateau": "Columbia Plateau",
    "appalachia": "Appalachia", "great_basin": "Great Basin",
    "new_england": "New England", "aridoamerica": "Aridoamerica",
    "texas": "Texas", "great_lakes": "Great Lakes",
    "great_plains": "Great Plains", "maritimes": "Maritimes",
    "ontario": "Ontario", "quebec": "Quebec",
    "newfoundland": "Newfoundland", "subarctic": "Subarctic",
    "arctic": "Arctic", "arctic_islands": "Arctic Islands",
    "arctic_greenland": "Arctic Greenland", "arctic_quebec": "Arctic Quebec",
    "cascadia": "Cascadia",
    "mesoamerica": "Mesoamerica", "centroamerica": "Centroamerica",
    "colombia": "Colombia", "andes": "Andes",
    "amazon": "Amazon", "brasil_norte": "Brasil Norte",
    "gran_chaco": "Gran Chaco", "brasil_sur": "Brasil Sur",
    "argentina": "Argentina", "patagonia": "Patagonia",
    "chile": "Chile", "san_martin": "San Martin",
    "carribean_florida": "Caribbean",
    "western_europe": "Western Europe", "central_europe": "Central Europe",
    "southern_europe": "Southern Europe", "scandanavia": "Scandinavia",
    "balkans": "Balkans",
    "russia": "Russia", "transcaucasia": "Transcaucasia",
    "siberia": "Siberia", "novosibirsk": "Novosibirsk",
    "vladivostok": "Vladivostok", "yakutia": "Yakutia",
    "chukchi": "Chukchi",
    "maghreb": "Maghreb", "egypt": "Egypt",
    "levant": "Levant", "mesopotamia": "Mesopotamia",
    "arabia": "Arabia",
    "sahel": "Sahel", "west_africa": "West Africa",
    "sahara": "Sahara", "congo": "Congo",
    "abyssinia": "Abyssinia", "swahili": "Swahili",
    "southern_bantu": "Southern Bantu", "south_africa": "South Africa",
    "kalahari": "Kalahari", "madagascar": "Madagascar",
    "iranian_plateau": "Iranian Plateau", "central_asia": "Central Asia",
    "indus": "Indus", "maratha": "Maratha",
    "hindustan": "Hindustan", "bengal": "Bengal",
    "dravidia": "Dravidia",
    "xinjiang": "Xinjiang", "manchuria": "Manchuria",
    "northwestern_china": "Hetao", "central_china": "Zhongyuan",
    "tibet": "Tibet", "southwestern_china": "Bashu",
    "south_china": "Lingnan", "mongolia": "Mongolia",
    "korea": "Korea", "japan": "Japan",
    "southeast_asia": "Southeast Asia", "vietnam": "Vietnam",
    "malaya": "Malaya", "philippines": "Philippines",
    "melanesia": "Melanesia", "polynesia": "Polynesia",
    "micronesia": "Micronesia",
    "east_australia": "East Australia", "north_australia": "North Australia",
    "west_australia": "West Australia", "desert_australia": "Desert Australia",
    "aotearoa": "Aotearoa",
}

ZONE_COLORS = {
    # North American (2)
    "new_afrika": (176, 52, 26), "california": (251, 192, 45),
    "atlantica": (73, 123, 124), "columbia_plateau": (168, 117, 86),
    "appalachia": (66, 66, 66), "great_basin": (213, 164, 181),
    "new_england": (45, 105, 56), "texas": (35, 2, 195),
    "great_lakes": (83, 46, 144), "great_plains": (211, 200, 96),
    "maritimes": (53, 69, 129), "ontario": (57, 125, 49),
    "quebec": (47, 88, 231), "newfoundland": (189, 65, 59),
    "subarctic": (99, 18, 41), "cascadia": (56, 142, 60),
    "arctic": (126, 109, 165), "arctic_quebec": (126, 109, 165),
    # Merged arctic zones (same base color)
    "arctic_islands": (126, 109, 165), "arctic_greenland": (126, 109, 165),
    # Latin American (12)
    "mesoamerica": (162, 215, 129), "centroamerica": (73, 158, 230),
    "colombia": (236, 209, 80), "andes": (215, 140, 49),
    "amazon": (40, 89, 55), "brasil_norte": (235, 119, 50),
    "gran_chaco": (203, 105, 79), "brasil_sur": (69, 154, 71),
    "argentina": (128, 171, 234), "patagonia": (82, 173, 110),
    "chile": (159, 54, 39), "san_martin": (119, 183, 239),
    "aridoamerica": (188, 132, 71),
    # Caribbean (13)
    "carribean_florida": (135, 211, 207),
    "carribean_bahamas": (135, 211, 207),
    "carribean_greater_antilles": (135, 211, 207),
    "carribean_lesser_antilles": (135, 211, 207),
    # Eurasian (1)
    "western_europe": (41, 3, 103), "central_europe": (99, 99, 99),
    "southern_europe": (208, 171, 68), "scandanavia": (78, 161, 247),
    "balkans": (112, 19, 11), "russia": (74, 123, 51),
    "transcaucasia": (213, 133, 69), "siberia": (164, 101, 81),
    "novosibirsk": (77, 182, 225), "vladivostok": (173, 228, 28),
    "iranian_plateau": (103, 236, 226), "central_asia": (239, 239, 70),
    # Arabic (4)
    "maghreb": (162, 45, 251), "egypt": (118, 251, 106),
    "levant": (76, 107, 54), "mesopotamia": (179, 149, 118),
    "arabia": (231, 213, 101), "sahara": (101, 99, 95),
    # African (14)
    "sahel": (225, 223, 73), "west_africa": (175, 173, 101),
    "congo": (196, 92, 84), "abyssinia": (174, 135, 79),
    "swahili": (66, 165, 245), "southern_bantu": (255, 83, 177),
    "south_africa": (225, 138, 70), "kalahari": (174, 209, 66),
    "madagascar": (178, 117, 114),
    # Hindustani (7)
    "indus": (51, 95, 53), "maratha": (137, 35, 17),
    "hindustan": (237, 110, 45), "bengal": (58, 107, 188),
    "dravidia": (240, 199, 72),
    # East Asian (8)
    "xinjiang": (112, 146, 164), "manchuria": (155, 98, 50),
    "northwestern_china": (110, 81, 83), "central_china": (42, 96, 151),
    "tibet": (187, 205, 205), "southwestern_china": (80, 112, 97),
    "south_china": (246, 200, 68), "mongolia": (123, 163, 104),
    "korea": (101, 16, 9), "japan": (237, 205, 190),
    # Paleosiberian (18)
    "yakutia": (245, 201, 73), "chukchi": (61, 118, 147),
    # SE Asian (11)
    "southeast_asia": (112, 150, 114), "vietnam": (223, 65, 59),
    "malaya": (235, 88, 122), "philippines": (41, 31, 190),
    # Pacific (15)
    "melanesia": (130, 132, 70), "polynesia": (255, 238, 88),
    "micronesia": (108, 254, 156),
    # Anglo-Australasian (17)
    "east_australia": (145, 252, 107), "north_australia": (98, 168, 244),
    "west_australia": (255, 255, 84), "desert_australia": (233, 168, 58),
    "aotearoa": (125, 55, 167),
}

ANT_DISPLAY = {
    "ant_san_martin": "San Martin",
    "ant_maudland": "Maudland",
    "ant_indian": "Dakshin",
    "ant_rossland": "Victorialand",
    "ant_marie_byrd_land": "Nandi",
}

ANT_COLORS = {
    "ant_san_martin": (50, 150, 200),
    "ant_maudland": (100, 180, 220),
    "ant_indian": (200, 180, 100),
    "ant_rossland": (150, 200, 200),
    "ant_marie_byrd_land": (180, 180, 220),
}

# Antarctic zone → continental sphere parent ID
ANT_CONT = {
    "ant_san_martin": 12,           # Latin America
    "ant_maudland": 1,              # Hesperia
    "ant_indian": 7,                # Hindustan
    "ant_rossland": 17,             # Australasia
    "ant_marie_byrd_land": 8,       # East Asia (Chinese settlement)
}

# Island fix specs: (centroid_lon, centroid_lat, radius_deg, target_zone_name, label)
ISLAND_FIXES = [
    (-77.3, 18.1, 1.5, "carribean_florida", "Jamaica → Caribbean"),
    (-66.5, 18.2, 1.0, "carribean_florida", "Puerto Rico → Caribbean"),
    (-90.5, -0.5, 1.5, "colombia", "Galapagos → Colombia"),
    (-59.0, -51.7, 1.5, "patagonia", "Malvinas → Patagonia"),
    (-36.5, -54.5, 2.0, "patagonia", "San Pedro → Patagonia"),
]

# Same islands but for continental spheres (uses parent zone IDs)
CONT_ISLAND_FIXES = [
    (-77.3, 18.1, 1.5, 13, "Jamaica → Caribbean"),
    (-66.5, 18.2, 1.0, 13, "Puerto Rico → Caribbean"),
    (-90.5, -0.5, 1.5, 12, "Galapagos → Latin America"),
    (-59.0, -51.7, 1.5, 12, "Malvinas → Latin America"),
    (-36.5, -54.5, 2.0, 12, "San Pedro → Latin America"),
]

MERGE_MAP = {
    "arctic_islands": "arctic",
    "arctic_greenland": "arctic",
    "carribean_bahamas": "carribean_florida",
    "carribean_greater_antilles": "carribean_florida",
    "carribean_lesser_antilles": "carribean_florida",
}

ZONE_DELETE = {"san_martin"}

def build_zone_defs(map_dict, zone_list):
    reverse = {}
    for en, zid in map_dict.items():
        reverse.setdefault(zid, []).append(en)
    return [(zid, reverse[zid]) for zid, _ in zone_list]

# ── Main ─────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Culture Areas KMZ Generator (2050) v2")
    print("=" * 60)
    
    # 1. Load reference grid
    print("\nLoading ETOPO 2022 reference grid…", flush=True)
    src = rasterio.open(ETOPO_TIF)
    H0, W0 = src.shape
    tx0 = src.transform
    src.close()
    print(f"  Full grid: {W0}x{H0}", flush=True)
    
    # Resolution for working grid — native 60s for best island capture
    STRIDE = 1
    H = H0 // STRIDE
    W = W0 // STRIDE
    tx = tx0 * tx0.scale(STRIDE, STRIDE)
    print(f"  Working grid: {W}x{H}", flush=True)
    
    # 2. Load high-resolution coastline and simplify to stay under Google Earth's 250K vertex limit
    print("\nLoading NE 10m land mask…", flush=True)
    coastline = load_land_geom(NE_LAND_ZIP)
    print(f"  Coastline loaded: {coastline.geom_type}", flush=True)
    print(f"    Original vertices: ~{sum(len(g.exterior.coords) for g in (coastline.geoms if hasattr(coastline, 'geoms') else [coastline])):,}", flush=True)
    # Split coastline: simplify large landmasses (≥0.1 sq deg), keep small islands at full resolution
    if hasattr(coastline, 'geoms'):
        parts = list(coastline.geoms)
        large = [p for p in parts if p.area >= 0.1]
        small = [p for p in parts if p.area < 0.1]
        large_simple = [p.simplify(0.011, preserve_topology=True) for p in large if not p.is_empty]
        coastline = unary_union(large_simple + small)
    else:
        coastline = coastline.simplify(0.011, preserve_topology=True)
    print(f"    Simplified vertices: ~{sum(len(g.exterior.coords) for g in (coastline.geoms if hasattr(coastline, 'geoms') else [coastline])):,}", flush=True)
    
    # 3. Extract entities
    print("\nExtracting entities from borders.kml…", flush=True)
    entities = extract_entities(BORDERS_KML)
    print(f"  {len(entities)} entities loaded", flush=True)
    
    # 4b. Load Antarctic ice-sheet sectors and merge into entities
    print("\nLoading Antarctic ice-sheet sectors…", flush=True)
    antarctic_sectors, antarctic_ice = load_antarctic_sectors(ENTITY_CONFIG, ANTARCTIC_DIR)
    if antarctic_sectors:
        for ename, sector_geom in antarctic_sectors.items():
            if ename in entities:
                entities[ename] = unary_union([entities[ename], sector_geom])
            else:
                entities[ename] = sector_geom
        print(f"  {len(antarctic_sectors)} entity sectors merged", flush=True)
        print(f"  Combined ice area: {antarctic_ice.area:.0f} sq.deg", flush=True)
        # Add Antarctic ice to coastline for land mask
        coastline = unary_union([coastline, antarctic_ice])
        print(f"  Ice-sheet added to coastline, new area: {coastline.area:.0f} sq.deg", flush=True)
    
    # Raster land mask for clipping
    land_raster = rasterize(
        [(coastline, 1)], out_shape=(H, W), transform=tx,
        fill=0, dtype="uint8", all_touched=False,
    ).astype(bool)
    print(f"  {land_raster.sum():,} land cells", flush=True)
    
    # 5. Process layers
    layers = []
    
    # ── Cultural Areas ────────────────────────────────────────────────────────
    print("\n─ Cultural Areas ─", flush=True)
    
    # Load base KML zones and merge absorbed zones
    base_zones = load_base_zones(ZONES_BASE_KML)
    # Fix self-intersections (common in hand-drawn KML) and merge
    for key, geom in base_zones.items():
        if not geom.is_valid:
            base_zones[key] = geom.buffer(0)
    for src, dst in MERGE_MAP.items():
        if src not in base_zones: continue
        if dst not in base_zones: continue
        merged = unary_union([base_zones[dst], base_zones[src]])
        if not merged.is_empty and merged.is_valid:
            base_zones[dst] = fix_antimeridian(merged)
        del base_zones[src]
    for name in ZONE_DELETE:
        base_zones.pop(name, None)
    zone_names = sorted(base_zones.keys())
    zid_of = {n: i+1 for i, n in enumerate(zone_names)}
    
    # Build zone colors from base KML zone colors
    zone_colors = {}
    for zname in zone_names:
        rgb = ZONE_COLORS.get(zname, (180, 180, 180))
        zone_colors[zid_of[zname]] = rgb
    
    # Rasterize base zones (geometry → zone_id pairs)
    zone_pairs = [(base_zones[n], zid_of[n]) for n in zone_names]
    zone_arr = rasterio.features.rasterize(
        zone_pairs, out_shape=(H, W), transform=tx,
        fill=0, dtype="uint16", all_touched=True,
    )
    zone_arr[~land_raster] = 0
    zone_arr = _fill_zone_gaps(zone_arr, land_raster)
    zone_polys_raw = zones_from_raster(zone_arr, tx, land_raster)
    
    # Clip to high-res coastline
    zone_polys = {}
    for zid, geoms in zone_polys_raw.items():
        zone_polys[zid] = clip_geoms_to_coastline(geoms, coastline)
    
    # Inject coastline islands with entity-to-zone distance fallback
    entity_zone_map = _build_entity_zone_map(entities, zone_arr, tx)
    inject_coastline_islands(zone_polys, zone_arr, tx, coastline, entities, entity_zone_map, max_area=0.05)
    # Force specific islands into correct zones
    force_coastline_islands(zone_polys, coastline, zid_of, ISLAND_FIXES)
    for polys in zone_polys.values():
        for i, g in enumerate(polys):
            polys[i] = _clean_holes(g, MIN_HOLE)
    for zid in list(zone_polys.keys()):
        zone_polys[zid] = _remove_interior_pieces(zone_polys[zid])
    
    # ── Continental Spheres (grouped from zones by parent continent) ──
    print("\n─ Continental Spheres ─", flush=True)
    cont_geoms = {}
    for zname in zone_names:
        pid = ZONE_PARENT.get(zname)
        if pid is None: continue
        cont_geoms.setdefault(pid, []).append(zname)
    
    cont_arr = np.zeros((H, W), dtype=np.uint8)
    for pid, zn in cont_geoms.items():
        mask = np.isin(zone_arr, [zid_of[z] for z in zn])
        cont_arr[mask] = pid
    cont_arr[~land_raster] = 0
    
    cont_polys_raw = zones_from_raster(cont_arr, tx, land_raster)
    cont_polys = {}
    for zid, geoms in cont_polys_raw.items():
        pieces = []
        for g in geoms:
            pieces.extend(_collect(g.simplify(0.08, preserve_topology=True).buffer(0), MIN_AREA))
        if len(pieces) > 1:
            merged = unary_union(pieces)
            if merged.geom_type == "MultiPolygon":
                pieces = [p for p in merged.geoms if not p.is_empty]
            else:
                pieces = [merged]
        cont_polys[zid] = [p for p in pieces if not _is_sliver(p)]
    
    print(f"  Continents: {len(cont_polys)}", flush=True)
    for zid, name in CIV_ZONES:
        polys = cont_polys.get(zid, [])
        print(f"    {name}: {len(polys)} polygons", flush=True)
    
    # Inject islands — use zone_arr raster sampling + CIV_MAP distance fallback
    inject_coastline_islands(cont_polys, cont_arr, tx, coastline, entities, CIV_MAP)
    # Force specific islands into correct continental spheres
    force_coastline_islands_cont(cont_polys, coastline, CONT_ISLAND_FIXES)
    
    # ── Antarctic Settlement Zones ──
    print("\n─ Antarctic Settlement Zones ─", flush=True)
    ant_ns = '{http://www.opengis.net/kml/2.2}'
    ant_tree = ET.parse(ANT_ZONES_KML)
    ant_root = ant_tree.getroot()
    ant_polys_raw = {}
    for pm in ant_root.iter(f'{ant_ns}Placemark'):
        name_el = pm.find(f'{ant_ns}name')
        name = name_el.text if name_el is not None else "unknown"
        for poly_el in pm.findall(f'.//{ant_ns}Polygon'):
            outer = poly_el.find(f'{ant_ns}outerBoundaryIs/{ant_ns}LinearRing/{ant_ns}coordinates')
            if outer is None or not outer.text: continue
            rings = [_parse_kml_coords(outer.text)]
            for inner in poly_el.findall(f'{ant_ns}innerBoundaryIs/{ant_ns}LinearRing/{ant_ns}coordinates'):
                if inner.text:
                    rings.append(_parse_kml_coords(inner.text))
            if rings and len(rings[0]) >= 3:
                try:
                    p = Polygon(rings[0], rings[1:] if len(rings) > 1 else None)
                    if not p.is_empty and p.area > 0:
                        clipped = p.intersection(coastline)
                        if not clipped.is_empty:
                            for piece in _collect(clipped, MIN_AREA):
                                key = "ant_" + name.lower().replace(" ", "_")
                                ant_polys_raw.setdefault(key, []).append(piece)
                except Exception:
                    pass
    ant_zones = {}
    for aname, geoms in ant_polys_raw.items():
        merged = unary_union([fix_antimeridian(g) for g in geoms])
        pieces = _collect(merged, MIN_AREA)
        pieces = [p for p in pieces if not _is_sliver(p)]
        if pieces:
            ant_zones[aname] = pieces
    ant_used = 0
    if ant_zones:
        next_zid = max(zid_of.values()) + 1
        for aname, pieces in ant_zones.items():
            zid = next_zid
            next_zid += 1
            display = ANT_DISPLAY.get(aname, aname.replace("_", " ").title())
            ZONE_DISPLAY[aname] = display
            zone_names.append(aname)
            zid_of[aname] = zid
            zone_colors[zid] = ANT_COLORS.get(aname, (180, 180, 200))
            zone_polys[zid] = pieces
            # Assign to continental sphere
            pid = ANT_CONT.get(aname)
            if pid is not None:
                cont_polys.setdefault(pid, []).extend(pieces)
            ant_used += 1
        print(f"  {ant_used} antarctic zones added", flush=True)
        for aname, pieces in ant_zones.items():
            print(f"    {ANT_DISPLAY.get(aname, aname)}: {len(pieces)} polygons", flush=True)
    else:
        print("  No antarctic zones loaded", flush=True)
    
    # Clean holes and interior pieces from all continental spheres (incl. antarctic)
    for zid, polys in cont_polys.items():
        for i, g in enumerate(polys):
            polys[i] = _clean_holes(g, MIN_HOLE, continent_id=zid)
    for zid in list(cont_polys.keys()):
        cont_polys[zid] = _remove_interior_pieces(cont_polys[zid])


    # ── Regional Areas (from the same zone data) ──
    print("\n─ Regional Areas ─", flush=True)
    reg_polys = dict(zone_polys)
    print(f"  Zones: {len(reg_polys)}", flush=True)
    for zname in zone_names:
        polys = reg_polys.get(zid_of[zname], [])
        print(f"    {ZONE_DISPLAY.get(zname, zname)}: {len(polys)} polygons", flush=True)
    
    # ── Ideologies ────────────────────────────────────────────────────────────
    print("\n─ Ideologies ─", flush=True)
    ideo_defs = build_zone_defs(IDEO_MAP, IDEO_ZONES)
    ideo_arr = rasterize_zones((H, W), tx, ideo_defs, entities)
    ideo_arr[~land_raster] = 0
    ideo_polys_raw = zones_from_raster(ideo_arr, tx, land_raster)
    ideo_polys = {zid: clip_geoms_to_coastline(g, coastline) for zid, g in ideo_polys_raw.items()}
    print(f"  Zones found: {len(ideo_polys)}", flush=True)
    for zid, name in IDEO_ZONES:
        polys = ideo_polys.get(zid, [])
        print(f"    {name}: {len(polys)} polygons", flush=True)
    for polys in ideo_polys.values():
        for i, g in enumerate(polys):
            polys[i] = _clean_holes(g, MIN_HOLE)
    
    inject_coastline_islands(ideo_polys, ideo_arr, tx, coastline, entities, IDEO_MAP)
    
    layers.append(("Ideologies", IDEO_ZONES, ideo_polys, IDEO_COLORS))
    
    # ── Lingua Franca ────────────────────────────────────────────────────────
    print("\n─ Lingua Franca ─", flush=True)
    lang_defs = build_zone_defs(LANG_MAP, LANG_ZONES)
    lang_arr = rasterize_zones((H, W), tx, lang_defs, entities)
    lang_arr[~land_raster] = 0
    lang_polys_raw = zones_from_raster(lang_arr, tx, land_raster)
    lang_polys = {zid: clip_geoms_to_coastline(g, coastline) for zid, g in lang_polys_raw.items()}
    print(f"  Zones found: {len(lang_polys)}", flush=True)
    for zid, name in LANG_ZONES:
        polys = lang_polys.get(zid, [])
        print(f"    {name}: {len(polys)} polygons", flush=True)
    for polys in lang_polys.values():
        for i, g in enumerate(polys):
            polys[i] = _clean_holes(g, MIN_HOLE)
    
    inject_coastline_islands(lang_polys, lang_arr, tx, coastline, entities, LANG_MAP)
    
    layers.append(("Lingua Franca", LANG_ZONES, lang_polys, LANG_COLORS))
    
    # ── Build KMZ ─────────────────────────────────────────────────────────────
    print("\nBuilding KMZ…", flush=True)
    doc = ET.Element("kml", {"xmlns": "http://www.opengis.net/kml/2.2"})
    document = ET.SubElement(doc, "Document")
    ET.SubElement(document, "name").text = "Culture Areas 2050"
    
    # ── Cultural Areas (parent folder with two subfolders) ──
    cultural = ET.SubElement(document, "Folder")
    ET.SubElement(cultural, "name").text = "Cultural Areas"
    
    # Continental Spheres subfolder
    cont = ET.SubElement(cultural, "Folder")
    ET.SubElement(cont, "name").text = "Continental Spheres"
    for zid, zname in CIV_ZONES:
        geoms = cont_polys.get(zid, [])
        if not geoms: continue
        rgb = CIV_COLORS.get(zid, (180, 180, 180))
        sid = f"cont_{zid}"
        write_layer(document, cont, zname, sid, geoms, rgb)
    
    # Regional Areas subfolder
    reg = ET.SubElement(cultural, "Folder")
    ET.SubElement(reg, "name").text = "Regional Areas"
    for zname in zone_names:
        zid = zid_of[zname]
        geoms = reg_polys.get(zid, [])
        if not geoms: continue
        rgb = zone_colors.get(zid, (180, 180, 180))
        sid = f"reg_{zid}"
        write_layer(document, reg, ZONE_DISPLAY.get(zname, zname), sid, geoms, rgb)
    
    # Other layers (Ideologies, Lingua Franca)
    for layer_name, zone_list, polys_dict, colors in layers:
        folder = ET.SubElement(document, "Folder")
        ET.SubElement(folder, "name").text = layer_name
        for zid, zname in zone_list:
            geoms = polys_dict.get(zid, [])
            if not geoms: continue
            rgb = colors.get(zid, (180, 180, 180))
            sid = f"{layer_name.lower().replace(' ', '_')}_{zid}"
            write_layer(document, folder, zname, sid, geoms, rgb)
    
    kml_xml = ET.tostring(doc, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(OUTPUT_KMZ, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("doc.kml", kml_xml)
    size_kb = os.path.getsize(OUTPUT_KMZ) / 1024
    print(f"\nWritten: {OUTPUT_KMZ} ({size_kb:.0f} KB)", flush=True)


if __name__ == "__main__":
    main()
