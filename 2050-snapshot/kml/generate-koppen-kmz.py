#!/usr/bin/env python3
"""
Generate climate-koppen.kmz — a GroundOverlay KMZ of Köppen-Geiger 2050 climate zones.

Reads the GloH2O V3 GeoTIFF, maps each pixel to its Köppen color, writes a
full-globe RGBA PNG, and packages it with a KML GroundOverlay into a KMZ.

No feature count limit.  Works in Google Earth Web, Pro, and mobile.
"""

import io
import os
import zipfile
import numpy as np
import rasterio
from PIL import Image

TIFF_PATH = "source/koppen_2041-2070_ssp370.tif"
OUTPUT_KMZ = "climate-koppen.kmz"

# Standard Köppen palette (Beck et al. 2023).  RRGGBB hex strings.
KOPPEN_COLORS = {
    "Af":  "#0000F5",  "Am":  "#3475F6",  "Aw":  "#61A7F7",
    "BWh": "#E83423",  "BWk": "#F19C98",  "BSh": "#E8A63A",  "BSk": "#F9DD77",
    "Csa": "#FFFF55",  "Csb": "#C5C740",  "Csc": "#96952E",
    "Cwa": "#B0FCA0",  "Cwb": "#7CC471",  "Cwc": "#509541",
    "Cfa": "#D1FD6E",  "Cfb": "#92F95B",  "Cfc": "#64C43A",
    "Dsa": "#E934F6",  "Dsb": "#B526BF",  "Dsc": "#88388E",  "Dsd": "#8E668F",
    "Dwa": "#ACB1F9",  "Dwb": "#6075D3",  "Dwc": "#4F52AF",  "Dwd": "#2C0381",
    "Dfa": "#75FBFC",  "Dfb": "#66C4F8",  "Dfc": "#367C7C",  "Dfd": "#1A445C",
    "ET":  "#B2B2B2",  "EF":  "#686868",
}

# Raster pixel value → Köppen code (GloH2O V3 numbering)
RASTER_LEGEND = {
    1:"Af", 2:"Am", 3:"Aw",
    4:"BWh", 5:"BWk", 6:"BSh", 7:"BSk",
    8:"Csa", 9:"Csb", 10:"Csc",
    11:"Cwa", 12:"Cwb", 13:"Cwc",
    14:"Cfa", 15:"Cfb", 16:"Cfc",
    17:"Dsa", 18:"Dsb", 19:"Dsc", 20:"Dsd",
    21:"Dwa", 22:"Dwb", 23:"Dwc", 24:"Dwd",
    25:"Dfa", 26:"Dfb", 27:"Dfc", 28:"Dfd",
    29:"ET", 30:"EF",
}

ALPHA = 180  # 0-255; 180 ≈ 70% opacity — adjust to taste
SCALE = 4    # nearest-neighbor upsample factor (1=native 0.1°, 4=0.025° ≈ 2.75km/px)


def hex_to_rgba(hex_color, alpha=ALPHA):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (r, g, b, alpha)


def build_color_lut():
    """Return a 256×4 uint8 LUT mapping pixel value → RGBA."""
    lut = np.zeros((256, 4), dtype=np.uint8)  # default: transparent
    for pixel_val, code in RASTER_LEGEND.items():
        hex_color = KOPPEN_COLORS.get(code)
        if hex_color:
            lut[pixel_val] = hex_to_rgba(hex_color)
    return lut


def generate_png(tiff_path):
    with rasterio.open(tiff_path) as src:
        band = src.read(1)
        nodata = src.nodata
        height, width = band.shape
        print(f"  Raster: {width}×{height} pixels")

    lut = build_color_lut()

    # Map each pixel value through the LUT
    rgba = lut[band]  # shape: (height, width, 4)

    # Zero out alpha for nodata pixels
    if nodata is not None:
        rgba[band == int(nodata), 3] = 0

    # Nearest-neighbor upsample for crisp zone edges (no color blending)
    if SCALE > 1:
        rgba = np.repeat(np.repeat(rgba, SCALE, axis=0), SCALE, axis=1)
        print(f"  Upsampled {SCALE}×: {rgba.shape[1]}×{rgba.shape[0]} pixels")

    img = Image.fromarray(rgba, mode="RGBA")
    out_w, out_h = img.size

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=False)
    buf.seek(0)
    png_bytes = buf.read()
    print(f"  PNG: {len(png_bytes):,} bytes ({out_w}×{out_h} RGBA)")
    return png_bytes


def build_kml():
    return """\
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Köppen-Geiger Climate Zones (2050)</name>
    <description>GloH2O V3 · SSP3-7.0 · 2041–2070 projection · Beck et al. 2023</description>
    <GroundOverlay>
      <name>Köppen Climate Zones 2050</name>
      <description>GloH2O V3 Köppen-Geiger classification, SSP3-7.0, 2041–2070.
Source: Beck et al. 2023 (https://doi.org/10.1038/s41597-023-02549-6)</description>
      <color>ffffffff</color>
      <drawOrder>0</drawOrder>
      <Icon>
        <href>files/koppen_2050.png</href>
        <viewBoundScale>1.0</viewBoundScale>
      </Icon>
      <LatLonBox>
        <north>90</north>
        <south>-90</south>
        <east>180</east>
        <west>-180</west>
      </LatLonBox>
    </GroundOverlay>
  </Document>
</kml>
"""


def main():
    if not os.path.exists(TIFF_PATH):
        print(f"ERROR: GeoTIFF not found at {TIFF_PATH}")
        return

    print("Generating Köppen GroundOverlay KMZ...")
    print("Building PNG from GeoTIFF...")
    png_bytes = generate_png(TIFF_PATH)

    kml_str = build_kml()

    print(f"Writing {OUTPUT_KMZ}...")
    with zipfile.ZipFile(OUTPUT_KMZ, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("doc.kml", kml_str.encode("utf-8"))
        zf.writestr("files/koppen_2050.png", png_bytes)

    kmz_size = os.path.getsize(OUTPUT_KMZ)
    print(f"Done: {OUTPUT_KMZ} ({kmz_size:,} bytes)")
    print()
    print("Import climate-koppen.kmz into Google Earth (Web or Pro).")
    print("No feature limit — renders as a raster image overlay.")


if __name__ == "__main__":
    main()
