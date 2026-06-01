#!/usr/bin/env python3
"""
Add proper Document-level styles to climate.kml.

KML color format: AABBGGRR (alpha, blue, green, red)
"""
import lxml.etree as ET
import shutil
import os

NS_KML = "http://www.opengis.net/kml/2.2"
NS_GX = "http://www.google.com/kml/ext/2.2"
ns = {"kml": NS_KML, "gx": NS_GX}

KML_PATH = "2050-snapshot/kml/climate.kml"

def c(hex_color, alpha="80"):
    """Convert #RRGGBB to KML AABBGGRR."""
    h = hex_color.lstrip("#")
    rr, gg, bb = h[0:2], h[2:4], h[4:6]
    return f"{alpha}{bb}{gg}{rr}"

def make_style(elem_id, poly_color, line_color=None, line_width=0.5):
    style = ET.Element(f"{{{NS_KML}}}Style", id=elem_id)
    ls = ET.SubElement(style, f"{{{NS_KML}}}LineStyle")
    ET.SubElement(ls, f"{{{NS_KML}}}color").text = line_color or "ff55b0b0"
    ET.SubElement(ls, f"{{{NS_KML}}}width").text = str(line_width)
    ps = ET.SubElement(style, f"{{{NS_KML}}}PolyStyle")
    ET.SubElement(ps, f"{{{NS_KML}}}color").text = poly_color
    return style

def make_icon_style(elem_id, color="ff55b0b0"):
    style = ET.Element(f"{{{NS_KML}}}Style", id=elem_id)
    icons = ET.SubElement(style, f"{{{NS_KML}}}IconStyle")
    ET.SubElement(icons, f"{{{NS_KML}}}color").text = color
    ET.SubElement(icons, f"{{{NS_KML}}}scale").text = "0.8"
    return style

# Standard Köppen colors (from Beck et al. 2023)
KOPPEN_COLORS = {
    "Af": "#0000FF", "Am": "#0078FF", "Aw": "#46AAFA",
    "BWh": "#FE0000", "BWk": "#FE9695", "BSh": "#F5A505", "BSk": "#FFDC7C",
    "Csa": "#FFCC00", "Csb": "#C9C800", "Cwa": "#C6C76A", "Cwb": "#6C9A5E",
    "Cwc": "#7EAA7D", "Cfa": "#96FF96", "Cfb": "#6DB46D", "Cfc": "#40A040",
    "Dsa": "#5EBDC9", "Dsb": "#4DA6B8", "Dsc": "#2F8FA5",
    "Dwa": "#5DF0F0", "Dwb": "#41C8C8", "Dwc": "#2CAAAA",
    "Dfa": "#00FFFF", "Dfb": "#46D2D2", "Dfc": "#64C8E4", "Dfd": "#5EE0F0",
    "ET": "#964696", "EF": "#FFFFFF",
}

# Biome colors
BIOME_COLORS = {
    "Tundra": "#A0A0A0",
    "Boreal Forest/Taiga": "#3A7D3A",
    "Temperate Forest": "#5CA65C",
    "Grassland/Savanna": "#E8D44D",
    "Desert": "#EDC58E",
    "Tropical Rainforest": "#1A5C1A",
}

def main():
    if not os.path.exists(KML_PATH):
        print(f"ERROR: {KML_PATH} not found")
        return False

    shutil.copy2(KML_PATH, KML_PATH + ".bak.style")

    tree = ET.parse(KML_PATH)
    root = tree.getroot()
    doc = root.find(f"{{{NS_KML}}}Document")

    # --- Build style elements ---
    new_styles = []

    # Climate overlay style (default for thematic placemarks)
    s = make_style("climate-overlay", "4055b0b0", "ff55b0b0", 0.5)
    new_styles.append(s)

    # Climate overlay highlighted
    s = make_style("climate-overlay-hi", "6055b0b0", "ff55b0b0", 1.0)
    new_styles.append(s)

    # Water basins (blue-teal shift)
    s = make_style("climate-basin", "405555b0", "ff5555b0", 0.5)
    new_styles.append(s)

    # Arctic resources (green-teal shift)
    s = make_style("climate-arctic", "40b0b055", "ffb0b055", 0.5)
    new_styles.append(s)

    # Köppen sub-type styles
    for code, hex_color in KOPPEN_COLORS.items():
        poly = c(hex_color, "80")
        line = c(hex_color, "FF")
        s = make_style(f"koppen-{code}", poly, line, 0.5)
        new_styles.append(s)

    # Biome styles
    for name, hex_color in BIOME_COLORS.items():
        safe_id = name.lower().replace("/", "-").replace(" ", "-")
        poly = c(hex_color, "60")
        line = c(hex_color, "FF")
        s = make_style(f"biome-{safe_id}", poly, line, 0.5)
        new_styles.append(s)

    # Icon style for point placemarks
    s = make_icon_style("climate-icon", "ff55b0b0")
    new_styles.append(s)

    # === Determine which style each placemark should use ===
    # Strategy: match by name pattern against parent folder name or placemark name

    # Collect all placemarks with their names and context
    all_pms = tree.findall(f".//{{{NS_KML}}}Placemark")

    for pm in all_pms:
        ne = pm.find(f"{{{NS_KML}}}name")
        pname = ne.text if ne is not None else ""

        # Determine parent folder context
        parent = pm.getparent()
        parent_name = ""
        while parent is not None:
            pne = parent.find(f"{{{NS_KML}}}name")
            if pne is not None:
                parent_name = pne.text or ""
                break
            parent = parent.getparent()

        # Check if existing styleUrl
        existing_su = pm.find(f"{{{NS_KML}}}styleUrl")
        if existing_su is not None:
            continue  # keep existing style if defined

        # Determine style based on name and context
        style_id = None

        # Köppen sub-types (codes like "Af", "BWh", etc.)
        for code in KOPPEN_COLORS:
            if pname == code or pname.startswith(code + " "):
                style_id = f"koppen-{code}"
                break

        if style_id:
            pass
        elif parent_name in BIOME_COLORS:
            safe = parent_name.lower().replace("/", "-").replace(" ", "-")
            style_id = f"biome-{safe}"
        elif "Transboundary Water Conflict" in parent_name or "Transboundary Water Conflict" in pname:
            style_id = "climate-basin"
        elif "Arctic Resource" in parent_name or "Arctic Resource" in pname:
            style_id = "climate-arctic"
        elif "Desalination" in parent_name or "Desalination" in pname or "Coastal Defenses" in pname or "Thames Barrier" in pname:
            style_id = "climate-icon"
        else:
            style_id = "climate-overlay"

        # Add styleUrl
        su = ET.SubElement(pm, f"{{{NS_KML}}}styleUrl")
        su.text = f"#{style_id}"

    # Insert styles at beginning of Document (after name element)
    insert_pos = 0
    for i, child in enumerate(list(doc)):
        if child.tag == f"{{{NS_KML}}}name":
            insert_pos = i + 1
            break

    for i, style in enumerate(reversed(new_styles)):
        doc.insert(insert_pos, style)

    tree.write(KML_PATH, xml_declaration=True, encoding="UTF-8")
    print(f"Added {len(new_styles)} Document-level styles ({len(KOPPEN_COLORS)} Köppen + {len(BIOME_COLORS)} biome + 4 thematic)")

    # Verify
    tree2 = ET.parse(KML_PATH)
    doc2 = tree2.find(f"{{{NS_KML}}}Document")
    all_pms2 = tree2.findall(f".//{{{NS_KML}}}Placemark")

    defined = {}
    for child in list(doc2):
        sid = child.get("id")
        if sid: defined[sid] = True

    bad = 0
    styled = 0
    for pm in all_pms2:
        su = pm.find(f"{{{NS_KML}}}styleUrl")
        if su is not None and su.text:
            styled += 1
            sid = su.text.lstrip("#")
            if sid not in defined:
                bad += 1
                ne = pm.find(f"{{{NS_KML}}}name")
                print(f"  MISSING #{sid}: {ne.text if ne is not None else '?'}")

    print(f"Placemarks: {len(all_pms2)}, Styled: {styled}, Broken: {bad} ({'PASS' if bad == 0 else 'FAIL'})")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
