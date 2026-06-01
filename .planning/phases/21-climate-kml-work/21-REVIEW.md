---
phase: 21-climate-kml-work
reviewed: 2026-06-01T18:00:00Z
depth: standard
files_reviewed: 5
files_reviewed_list:
  - 2050-snapshot/kml/generate-climate-layers.py
  - 2050-snapshot/kml/climate.kml
  - 2050-snapshot/domains/climate.md
  - 2050-snapshot/index.md
  - 2050-snapshot/kml/source/download-data.py
findings:
  critical: 4
  warning: 6
  info: 5
  total: 15
status: issues_found
---

# Phase 21: Code Review Report — Climate KML Work

**Reviewed:** 2026-06-01T18:00:00Z
**Depth:** standard
**Files Reviewed:** 5
**Status:** issues_found

## Summary

Reviewed 5 files changed during Phase 21: two new Python scripts (2,481 and 789 lines), one modified KML (3,096 lines), one modified domain document, and one modified index. Found 4 critical defects, 6 warnings, and 5 info items.

The most severe issues are: (1) a KML color byte-order bug that makes all Köppen climate zones and biome overlays display with wrong colors, (2) a runtime crash in the GeoTIFF polygonization histogram code, (3) broken Markdown cross-reference links in climate.md, and (4) a cascading-style override in climate.kml that paints all 30 Köppen zones with the same default teal color instead of their assigned scheme colors.

---

## Critical Issues

### CR-01: `hex_to_kml_color` produces wrong KML color byte order (swapped RGB → BGR)

**File:** `2050-snapshot/kml/generate-climate-layers.py:1528`
**Issue:** The `hex_to_kml_color` function converts HTML `#RRGGBB` to `AARRGGBB`, but the KML/Google Earth color format requires `AABBGGRR` (alpha, blue, green, red). The function preserves RGB order, producing colors like `800000FF` (opaque red) from `#0000FF` (blue). This affects **all 30 Köppen zones** and **all 6 biome types** rendered through `build_koppen_kml` and `_generate_biomes_from_wwf` / `_generate_biomes_fallback`.

Affected code paths:
- `build_koppen_kml` (line 1814-1816) — all Köppen polygon fill (`poly_color`) and outline (`line_color`) colors
- `_generate_biomes_from_wwf` (lines 2025-2026)
- `_generate_biomes_fallback` (lines 2152-2154)

Example: `Af` zone receives `KOPPEN_COLORS["Af"] = "#0000FF"` (blue). `hex_to_kml_color("#0000FF", "80")` returns `"800000FF"` which KML interprets as Alpha=80, Blue=00, Green=00, Red=FF = **bright red**, not blue.

Gray tones (`#A0A0A0` → `80A0A0A0`) are symmetric and appear correct by coincidence.

**Fix:**
```python
def hex_to_kml_color(hex_color, alpha="80"):
    """
    Convert #RRGGBB to AABBGGRR KML color format.
    KML byte order is Alpha, Blue, Green, Red.
    """
    hex_color = hex_color.lstrip("#")
    rr = hex_color[0:2]
    gg = hex_color[2:4]
    bb = hex_color[4:6]
    return f"{alpha}{bb}{gg}{rr}"
```

---

### CR-02: Histogram destructuring crash in `generate_from_geotiff`

**File:** `2050-snapshot/kml/generate-climate-layers.py:1679`
**Issue:** Line 1679 performs `unique, counts = Counter(band[band != src.nodata]).most_common()`. `Counter.most_common()` returns a **list of tuples** `[(value1, count1), (value2, count2), ...]`. Python tuple unpacking `unique, counts = list_of_tuples` tries to unpack the list into exactly two variables. This crashes for any GeoTIFF with:

- **0 unique values** → `ValueError: not enough values to unpack (expected 2, got 0)`
- **1 unique value** → `ValueError: not enough values to unpack (expected 2, got 1)`
- **2 unique values** → assigns `unique = (v1, c1)`, `counts = (v2, c2)`, then line 1684 tries `for val, cnt in unique[:35]` which iterates over the individual tuple elements `v1` and `c1` — a bare integer cannot be unpacked → `TypeError: cannot unpack non-iterable int object`
- **3+ unique values** → `ValueError: too many values to unpack (expected 2)`

This means **any real GeoTIFF with more than zero valid pixel values will crash** when printing the value histogram. The script would fall through to the exception handler at line 1917 and attempt fallback, but the GeoTIFF workflow is broken.

**Fix:**
```python
hist = Counter(band[band != src.nodata]).most_common()
if not hist:
    hist = Counter(band.flatten()).most_common()
log.info(f"  Unique pixel values found: {len(hist)}")
for val, cnt in hist[:35]:
    code = RASTER_LEGEND.get(val, "UNKNOWN")
    log.info(f"    Value {val:3d} ({code:>4s}): {cnt:>10,d} pixels")
```

---

### CR-03: All KML cross-reference links in climate.md resolve to wrong paths

**File:** `2050-snapshot/domains/climate.md:25,37,39,47,51,57,66,74,82,100,211`
**Issue:** Every KML reference link in `climate.md` uses the form `[label](2050-snapshot/kml/climate.kml)`. Because `climate.md` is located at `2050-snapshot/domains/climate.md`, the relative path `2050-snapshot/kml/climate.kml` resolves to `2050-snapshot/domains/2050-snapshot/kml/climate.kml` — which does not exist. All 11+ links are broken.

Affected lines: 25, 37, 39, 47, 51, 57, 66 (two links), 74, 82, 100, 211.

**Fix:** Change every instance of `2050-snapshot/kml/climate.kml` to `../kml/climate.kml`. For example:
```markdown
- [climate.kml](../kml/climate.kml)
- [Köppen-Geiger Climate Classification (2050)](../kml/climate.kml)
- [Arctic Permafrost Degradation Zone](../kml/climate.kml)
```

---

### CR-04: `gx:CascadingStyle` on each Placemark overrides Köppen-zone-specific colors in climate.kml

**File:** `2050-snapshot/kml/climate.kml:78,106,134,164,192,220...` (every Placemark in Climate Zones section)
**Issue:** Each Köppen Placemark has an inline `gx:CascadingStyle` that sets `<color>ff55b0b0</color>` (default teal). These are defined at the **Placemark level** and take rendering priority over the parent Folder's `<Style>` element (which has the correct Köppen-specific color like `FF0000FF` for Af). The cascading style override means **all 30 Köppen zones render with the same teal color** regardless of their assigned Köppen color scheme.

Example — Af zone:
```xml
<Folder id="8">
    <Style><LineStyle><color>FF0000FF</color></LineStyle></Style>   <!-- Correct: Red line for Af -->
    ...
    <Placemark>
        <gx:CascadingStyle>
            <Style>
                <LineStyle><color>ff55b0b0</color></LineStyle>   <!-- OVERRIDES: Default teal -->
            </Style>
        </gx:CascadingStyle>
        ...
    </Placemark>
</Folder>
```

This affects the entire Climate Zones section (~30 folders with ~30 Placemarks).

**Fix:** This is a regeneration issue. The `gx:CascadingStyle` elements should either be removed (so the Folder style applies) or should carry the correct Köppen-specific color. The fix depends on the generation toolchain. If `simplekml` is producing these cascading overrides, the placemark-level styles should be set with the correct Köppen colors, or the folder-level styles should be used instead of the cascading overrides.

---

## Warnings

### WR-01: `crs` variable assigned but never used in `generate_from_geotiff`

**File:** `2050-snapshot/kml/generate-climate-layers.py:1674`
**Issue:** Line 1674 assigns `crs = src.crs` but `crs` is never referenced again in the function. This dead variable suggests the CRS was intended for coordinate transformation but was not used, meaning the function assumes CRS compatibility without verification.

**Fix:** Either remove the line or add a CRS check:
```python
crs = src.crs
if crs and not crs.is_geographic:
    log.warning(f"  GeoTIFF CRS is not geographic: {crs} — window-based operations may be incorrect")
```

---

### WR-02: Double simplification in polygonization pipeline

**File:** `2050-snapshot/kml/generate-climate-layers.py:1691,1708`
**Issue:** The polygonization generator expression (line 1691) calls `.simplify(0.02, preserve_topology=True)` on each geometry, then the loop body (line 1708) calls `.simplify(0.02, preserve_topology=True)` again on the already-simplified result. This is redundant and wastes computation. While simplify is idempotent, it adds CPU overhead for each polygon.

**Fix:** Remove the `.simplify()` call from the generator expression and keep only the one in the loop body:
```python
results = (
    (shp_shape(geom), value)
    for geom, value in shapes(band, mask=band != src.nodata, transform=transform)
)
```

---

### WR-03: `_generate_slr_from_dem` assumes DEM CRS is geographic without checking

**File:** `2050-snapshot/kml/generate-climate-layers.py:2262-2269`
**Issue:** The function passes raw geographic coordinates `(min_lon, min_lat, max_lon, max_lat)` to `src.window()` without verifying that the DEM tile's CRS is EPSG:4326 (geographic). If DEM tiles use a projected CRS (e.g., UTM, Mercator), the window calculation and elevation mask (`band <= 0.35`) would produce incorrect results or raise an error. The function also reads `src.crs` but stores it in an unused variable.

**Fix:**
```python
with rasterio.open(dem_path) as src:
    if src.crs and not src.crs.is_geographic:
        log.warning(f"  DEM CRS is not geographic: {src.crs} — window may be incorrect")
    window = src.window(min_lon, min_lat, max_lon, max_lat)
```

---

### WR-04: `climate.kml` descriptions contain typo "T errestrial" (extra space)

**File:** `2050-snapshot/kml/climate.kml:1233,1274,1286,1366,1378...` (every biomes Placemark)
**Issue:** The text "WWF T errestrial Ecoregions source" appears throughout the Ecoregions & Biomes section with an erroneous space between "T" and "errestrial".

Source of typo: `2050-snapshot/kml/generate-climate-layers.py:2143` — the `fallback_note` string in `_generate_biomes_fallback`.

**Fix:** In `generate-climate-layers.py`, line 2143:
```python
fallback_note = (
    "APPROXIMATE — Replace with data-driven polygons when WWF "
    "Terrestrial Ecoregions source becomes available."
)
```
And regenerate `climate.kml`.

---

### WR-05: `download-data.py` KML magic-byte check is too strict (ignores BOM and whitespace)

**File:** `2050-snapshot/kml/source/download-data.py:115`
**Issue:** The KML format check at line 115 requires the first 16 bytes to start with either `b"<?xml"` or `b"<kml"`. Valid KML files may begin with a UTF-8 BOM (`\xef\xbb\xbf`), leading whitespace, or other XML declarations with encoding attributes. This could produce false negatives for valid KML files.

**Fix:** Strip whitespace and BOM before checking:
```python
header_clean = header.lstrip(b"\xef\xbb\xbf").lstrip()
if not header_clean.startswith(b"<?xml") and not header_clean.startswith(b"<kml"):
    log.error("  Not a valid KML (missing XML/KML header): %s", path)
    return False
```

---

### WR-06: Ocean-to-land vertex in Arctic resource sectors at 90°N causes rendering artifacts

**File:** `2050-snapshot/kml/generate-climate-layers.py:1132-1134,1154-1156,1175-1176,...`
**Issue:** Arctic sector polygons (Russian, Canadian, US, Norwegian, Greenlandic) include vertices at 90°N across all longitudes. When these polygons are rendered in Google Earth, the 90°N vertices converge at the North Pole, causing these sector boundaries to overlap at the pole. The polygon extends to the pole but then traces the 90° circle, producing a complex degenerate edge at the pole. While not strictly invalid KML, this can cause rendering glitches in some KML viewers.

**Fix:** Consider trimming sectors to stop at 85-87°N instead of 90°N, or use a pole-cap polygon for the region above the highest sector boundary, to avoid degenerate polar vertices.

---

## Info

### IN-01: `_make_coords_box` function defined but never called

**File:** `2050-snapshot/kml/generate-climate-layers.py:174`
**Issue:** The `_make_coords_box` helper function is defined but never invoked anywhere in the script. The `_generate_slr_fallback` function (line 2380) uses `box()` from shapely directly instead.

**Fix:** Either remove the unused function or use it in `_generate_slr_fallback` for consistency.

---

### IN-02: `_sha256` function defined but never called in `download-data.py`

**File:** `2050-snapshot/kml/source/download-data.py:205`
**Issue:** The `_sha256` function computes SHA-256 hashes but is never called. If file integrity verification was intended to include hash checking (beyond the size + magic-byte checks), this function should be wired in. Otherwise, it should be removed.

**Fix:** Either remove or integrate into `_check_file_integrity`.

---

### IN-03: Mixed coordinate precision across KML (float vs integer)

**File:** `2050-snapshot/kml/climate.kml` and `2050-snapshot/kml/generate-climate-layers.py`
**Issue:** Köppen zones and SLR zones use full-precision floating-point coordinates (e.g., `-180.0,65.0,0`), while refined placemarks in the thematic sections use integer coordinates (e.g., `68,22,0`). This is visually acceptable for KML but inconsistent. The integer coordinates in the refined zones (e.g., `75,28,0` for Himalayas) are acceptable for approximate/narrative polygons.

**Fix:** Consider passing coordinates through a consistent formatter e.g., `f"{x:.1f},{y:.1f},0"` for narrative-derived polygons.

---

### IN-04: Progress logging at 0% in download-data.py

**File:** `2050-snapshot/kml/source/download-data.py:177-179`
**Issue:** The progress check `if pct % 10 == 0` triggers at `pct == 0` (immediately after download starts), producing a "Progress: 0%" log line that is noise. It also triggers at 100% (since `100 % 10 == 0`), which is useful.

**Fix:** Add a `downloaded > 0` guard:
```python
if total > 0 and downloaded > 0:
    pct = downloaded * 100 // total
    if pct % 10 == 0:
        log.info(...)
```

---

### IN-05: Redundant `from shapely.geometry import Polygon` import in two nested functions

**File:** `2050-snapshot/kml/generate-climate-layers.py:1568,1626`
**Issue:** Both `create_fallback_polygons` (line 1568) and `generate_fallback_koppen_kml` (line 1626) import `Polygon` from `shapely.geometry` independently. These are function-level imports (perhaps to defer the import cost or handle missing dependency), which is a valid pattern for optional dependencies, but the duplication could be consolidated. Not a bug, but worth noting for cleanup.

---

_Reviewed: 2026-06-01T18:00:00Z_
_Reviewer: gsd-code-reviewer agent_
_Depth: standard_
