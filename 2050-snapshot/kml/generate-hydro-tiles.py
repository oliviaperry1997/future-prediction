#!/usr/bin/env python3
"""
Generate XYZ tiles for rivers and drainage basins.

Rivers: Natural Earth 10m, blue with line width proportional to scalerank.
Basins: HydroBASINS level 4, colored with 25% fill, no borders.

Output:
  tiles/rivers/{z}/{x}/{y}.png   — blue rivers with variable line width
  tiles/basins/{z}/{x}/{y}.png   — colored drainage basins, 25% fill

Data will be downloaded on first run (NE 10m rivers ~2 MB).
"""

import os, subprocess, tempfile, shutil, zipfile, glob, colorsys
import numpy as np
import fiona
import fiona.transform
import rasterio
import rasterio.features
from rasterio.crs import CRS
from PIL import Image, ImageDraw

TARGET_W = TARGET_H = 16384
ORIGIN = 20037508.342789244
MIN_ZOOM  = 0
MAX_ZOOM  = 6
TILE_SIZE = 256

TILES_DIR = "tiles"

WEB_MERCATOR = CRS.from_epsg(3857)

# ── River config ──────────────────────────────────────────────────────────────
NE_RIVERS_URL = "https://naciscdn.org/naturalearth/10m/physical/ne_10m_rivers_lake_centerlines.zip"
NE_RIVERS_ZIP = "source/ne_10m_rivers_lake_centerlines.zip"
RIVER_ALPHA   = 220
RIVER_WIDTH   = {1: 6, 2: 4, 3: 3, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1,
                 9: 1, 10: 1}
RIVER_COLOR   = (40, 100, 220)

# ── Drainage basin config ─────────────────────────────────────────────────────
HYBAS_GLOB = "source/hybas_*_lev04_v1c.zip"
BASIN_ALPHA = 64   # ~25%


# ── Coordinate helpers ────────────────────────────────────────────────────────
def mercator_to_pixel(x, y):
    """Convert EPSG:3857 (x, y) to pixel coords on the (W×H) grid."""
    px = (x + ORIGIN) / (2 * ORIGIN) * TARGET_W
    py = (ORIGIN - y) / (2 * ORIGIN) * TARGET_H
    return px, py


def geom_to_pixel_coords(geom):
    """Convert a geometry from EPSG:3857 to list of pixel coordinate tuples."""
    if geom["type"] == "LineString":
        return [tuple(mercator_to_pixel(x, y) for x, y in geom["coordinates"])]
    elif geom["type"] == "MultiLineString":
        return [tuple(mercator_to_pixel(x, y) for x, y in part)
                for part in geom["coordinates"]]
    elif geom["type"] == "Polygon":
        return [[tuple(mercator_to_pixel(x, y) for x, y in ring)]
                for ring in geom["coordinates"]]
    elif geom["type"] == "MultiPolygon":
        result = []
        for poly in geom["coordinates"]:
            result.append([tuple(mercator_to_pixel(x, y) for x, y in ring)
                          for ring in poly])
        return result
    return []


def pixel_bounds(z, x, y):
    n = 2 ** z
    px0 = round(x * TARGET_W / n);     py0 = round(y * TARGET_H / n)
    px1 = round((x + 1) * TARGET_W / n); py1 = round((y + 1) * TARGET_H / n)
    return px0, py0, px1, py1


# ── Download helpers ──────────────────────────────────────────────────────────
def download_if_missing(path, url):
    if not os.path.exists(path):
        print(f"  Downloading {url}…", flush=True)
        subprocess.run(["curl", "-L", url, "-o", path], check=True)


# ── Basin color helpers ───────────────────────────────────────────────────────
def basin_color(hid):
    """Deterministic, visually distinct RGB color for a basin."""
    h = (hash((hid, 0)) & 0xFFFF) / 65536.0
    s = 0.45 + ((hash((hid, 1)) & 0xFF) / 256.0) * 0.3
    v = 0.55 + ((hash((hid, 2)) & 0xFF) / 256.0) * 0.3
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255), BASIN_ALPHA)


# ── Tile writing ──────────────────────────────────────────────────────────────
def tile_rgba_array(rgba, out_dir, label):
    """Slice a (H, W, 4) RGBA uint8 array into XYZ tiles."""
    written = total = 0
    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        n = 2 ** z
        print(f"  Zoom {z} ({n}×{n})…", end=" ", flush=True)
        z_written = 0
        for x in range(n):
            x_dir = os.path.join(out_dir, str(z), str(x))
            for y in range(n):
                total += 1
                px0, py0, px1, py1 = pixel_bounds(z, x, y)
                patch = rgba[py0:py1, px0:px1]
                if patch[:, :, 3].max() == 0:
                    continue
                img = Image.fromarray(patch, mode="RGBA")
                if img.size != (TILE_SIZE, TILE_SIZE):
                    img = img.resize((TILE_SIZE, TILE_SIZE), Image.NEAREST)
                os.makedirs(x_dir, exist_ok=True)
                img.save(os.path.join(x_dir, f"{y}.png"), format="PNG", optimize=False)
                written += 1
                z_written += 1
        print(f"{z_written} tiles")
    print(f"  Done: {written}/{total} tiles → {out_dir}/")


# ── River rendering ───────────────────────────────────────────────────────────
def render_rivers():
    """Return RGBA array (H, W, 4) with river lines drawn."""
    download_if_missing(NE_RIVERS_ZIP, NE_RIVERS_URL)

    print("Reading river features…")
    lines = []  # list of (pixel_coords_list, width)
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
                    sr = props.get("scalerank", 6) or 6
                    fc = props.get("featurecla", "")
                    if fc not in ("River", "Lake Centerline", "Intermittent River",
                                  "Intermittent Stream", "Canals", "Canal"):
                        continue
                    width = RIVER_WIDTH.get(sr, 1)
                    # reproject to EPSG:3857
                    g3857 = fiona.transform.transform_geom(
                        "EPSG:4326", "EPSG:3857", g
                    )
                    pixel_lines = geom_to_pixel_coords(g3857)
                    for pl in pixel_lines:
                        if len(pl) >= 2:
                            lines.append((pl, width))
        finally:
            shutil.rmtree(tmpdir)

    print(f"  {len(lines)} line segments loaded")

    # Filter to visible extent
    clipped = []
    margin = 100
    for pl, w in lines:
        xs = [p[0] for p in pl]
        ys = [p[1] for p in pl]
        if max(xs) < -margin or min(xs) > TARGET_W + margin:
            continue
        if max(ys) < -margin or min(ys) > TARGET_H + margin:
            continue
        clipped.append((pl, w))
    print(f"  {len(clipped)} segments in tile bounds")

    print("Rendering rivers at 16384×16384…")
    img = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for pl, w in clipped:
        draw.line(pl, fill=(*RIVER_COLOR, RIVER_ALPHA), width=w, joint="curve")

    return np.asarray(img, dtype=np.uint8)


# ── Basin rendering ───────────────────────────────────────────────────────────
def render_basins():
    """Return RGBA array (H, W, 4) with colored basin fills."""
    os.environ.setdefault("OGR_ENABLE_PARTIAL_REPROJECTION", "TRUE")

    zips = sorted(glob.glob(HYBAS_GLOB))
    if not zips:
        print("  No HydroBASINS zip files found — skipping basins.")
        return None

    # Collect all basin geometries with HYBAS_ID
    shapes = []  # list of (geom_3857, hid)
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
                        g3857 = fiona.transform.transform_geom(
                            "EPSG:4326", "EPSG:3857", g
                        )
                        shapes.append((g3857, hid))
            finally:
                shutil.rmtree(tmpdir)

    print(f"  {len(shapes)} basin polygons collected")

    # Assign palette indices
    hid_to_pidx = {}
    palette_list = [(0, 0, 0, 0)]  # index 0 = transparent
    for _, hid in shapes:
        if hid not in hid_to_pidx:
            hid_to_pidx[hid] = len(palette_list)
            palette_list.append(basin_color(hid))

    palette = np.array(palette_list, dtype=np.uint8)

    # Rasterize palette indices at 16384×16384
    raster_shapes = [(g, hid_to_pidx[hid]) for g, hid in shapes]
    print("  Rasterizing at 16384×16384…")
    transform = rasterio.transform.from_bounds(
        -ORIGIN, -ORIGIN, ORIGIN, ORIGIN, TARGET_W, TARGET_H
    )
    idx_raster = rasterio.features.rasterize(
        raster_shapes, out_shape=(TARGET_H, TARGET_W),
        transform=transform, fill=0, dtype="uint32"
    )

    # Build RGBA tile-by-tile using palette lookup
    print("  Applying palette and tiling…")
    out_dir = os.path.join(TILES_DIR, "basins")
    written = total = 0
    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        n = 2 ** z
        print(f"  Zoom {z} ({n}×{n})…", end=" ", flush=True)
        z_written = 0
        for x in range(n):
            x_dir = os.path.join(out_dir, str(z), str(x))
            for y in range(n):
                total += 1
                px0, py0, px1, py1 = pixel_bounds(z, x, y)
                idx_patch = idx_raster[py0:py1, px0:px1]
                if (idx_patch > 0).sum() == 0:
                    continue
                rgba_patch = palette[idx_patch]
                img = Image.fromarray(rgba_patch, mode="RGBA")
                if img.size != (TILE_SIZE, TILE_SIZE):
                    img = img.resize((TILE_SIZE, TILE_SIZE), Image.NEAREST)
                os.makedirs(x_dir, exist_ok=True)
                img.save(os.path.join(x_dir, f"{y}.png"), format="PNG", optimize=False)
                written += 1
                z_written += 1
        print(f"{z_written} tiles")
    print(f"  Done: {written}/{total} tiles → {out_dir}/")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    # Rivers
    print("=== Rivers ===")
    rgba = render_rivers()
    tile_rgba_array(rgba, os.path.join(TILES_DIR, "rivers"), label="Rivers")
    del rgba

    # Basins
    print("\n=== Drainage Basins ===")
    render_basins()

    print("\nTile overlay URLs:")
    BASE = "https://oliviaperry1997.github.io/future-prediction/2050-snapshot/kml/tiles"
    print(f"  Rivers:  {BASE}/rivers/{{z}}/{{x}}/{{y}}.png")
    print(f"  Basins:  {BASE}/basins/{{z}}/{{x}}/{{y}}.png")


if __name__ == "__main__":
    main()
