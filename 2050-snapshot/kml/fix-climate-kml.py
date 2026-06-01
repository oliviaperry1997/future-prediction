#!/usr/bin/env python3
"""
Fix climate.kml:
1. Reorganize thematic placemarks into sub-category folders
2. Fix Köppen fallback descriptions to note approximate status
3. Ensure all styles work correctly via gx:CascadingStyle
"""
import shutil
import os
import lxml.etree as ET

NS_KML = "http://www.opengis.net/kml/2.2"
NS_GX = "http://www.google.com/kml/ext/2.2"
NSMAP = {"kml": NS_KML, "gx": NS_GX}

KML_PATH = "2050-snapshot/kml/climate.kml"
BACKUP_PATH = KML_PATH + ".bak.prefix_fix"

# --- Category mapping for placemarks ---
# (placemark_name_pattern, category_folder_name)
# Each placemark is matched by substring against its name
PLACEMARK_CATEGORIES = [
    # Glacial Systems & Risk Areas
    ("Arctic Permafrost", "Glacial Systems & Risk Areas"),
    ("Greenland Ice Sheet", "Glacial Systems & Risk Areas"),
    ("Glacier Mass Loss", "Glacial Systems & Risk Areas"),
    # Climate Systems
    ("Extreme Heat Zones", "Climate Systems"),
    ("Extreme Heat — Persian Gulf", "Climate Systems"),
    ("Fire Regime Shift", "Climate Systems"),
    # Drainage Basins
    ("Transboundary Water Conflict Basins", "Drainage Basins"),
    # Inundation Zones
    ("Sea Level Impact Zones", "Inundation Zones"),
    # Ecoregions
    ("Sahel Degradation Zone", "Ecoregions"),
    # Resources & Infrastructure
    ("Arctic Resource Zones", "Resources & Infrastructure"),
    ("Desalination and Adaptation Infrastructure", "Resources & Infrastructure"),
]

# Category ordering
CATEGORY_ORDER = [
    "Climate Systems",
    "Drainage Basins",
    "Ecoregions",
    "Inundation Zones",
    "Glacial Systems & Risk Areas",
    "Resources & Infrastructure",
]


def get_category(placemark_name):
    for pattern, cat in PLACEMARK_CATEGORIES:
        if pattern in placemark_name:
            return cat
    return None


def make_cascading_style(color, line_color=None, line_width=0.5):
    elem = ET.Element(f"{{{NS_GX}}}CascadingStyle")
    style = ET.SubElement(elem, f"{{{NS_KML}}}Style")
    ls = ET.SubElement(style, f"{{{NS_KML}}}LineStyle")
    lc = ET.SubElement(ls, f"{{{NS_KML}}}color")
    lc.text = line_color or "ff55b0b0"
    lw = ET.SubElement(ls, f"{{{NS_KML}}}width")
    lw.text = str(line_width)
    ps = ET.SubElement(style, f"{{{NS_KML}}}PolyStyle")
    pc = ET.SubElement(ps, f"{{{NS_KML}}}color")
    pc.text = color
    return elem


def main():
    if not os.path.exists(KML_PATH):
        print(f"ERROR: {KML_PATH} not found")
        return False

    shutil.copy2(KML_PATH, BACKUP_PATH)
    print(f"Backup saved: {BACKUP_PATH}")

    tree = ET.parse(KML_PATH)
    root = tree.getroot()
    doc = root.find(f"{{{NS_KML}}}Document")
    if doc is None:
        print("ERROR: No Document element found")
        return False

    # Find all top-level folders
    top_folders = []
    for child in list(doc):
        if child.tag == f"{{{NS_KML}}}Folder":
            name_el = child.find(f"{{{NS_KML}}}name")
            fname = name_el.text if name_el is not None else ""
            top_folders.append((child, fname))

    # Find the "Climate" folder (the one with 11 thematic sub-folders)
    climate_folder = None
    climate_idx = None
    for i, (folder, fname) in enumerate(top_folders):
        if fname == "Climate":
            climate_folder = folder
            climate_idx = i
            break

    if climate_folder is None:
        print("ERROR: No 'Climate' folder found")
        return False

    print(f"Found Climate folder at index {climate_idx}")

    # Find all sub-folders in Climate folder
    sub_folders = []
    for child in list(climate_folder):
        if child.tag == f"{{{NS_KML}}}Folder":
            name_el = child.find(f"{{{NS_KML}}}name")
            fname = name_el.text if name_el is not None else ""
            sub_folders.append((child, fname))

    print(f"Found {len(sub_folders)} sub-folders in Climate folder")
    for _, fname in sub_folders:
        cat = get_category(fname)
        print(f"  {fname} -> {cat or 'NO CATEGORY'}")

    # Build category folders
    cat_folders = {}
    for cat_name in CATEGORY_ORDER:
        cat_folder = ET.Element(f"{{{NS_KML}}}Folder")
        cat_name_el = ET.SubElement(cat_folder, f"{{{NS_KML}}}name")
        cat_name_el.text = cat_name
        cat_folders[cat_name] = cat_folder

    # Move each sub-folder into its category
    moved = set()
    for sub_folder, fname in sub_folders:
        cat = get_category(fname)
        if cat:
            cat_folders[cat].append(sub_folder)
            moved.add(id(sub_folder))

    # Remove unmoved sub-folders from Climate folder
    for child in list(climate_folder):
        if child.tag == f"{{{NS_KML}}}Folder" and id(child) in moved:
            climate_folder.remove(child)

    # Insert category folders after the SLR folder but before Climate
    # Find SLR folder position
    slr_idx = None
    sea_level_folder = None
    for i, (folder, fname) in enumerate(top_folders):
        if "Sea Level Rise" in fname:
            slr_idx = i
            sea_level_folder = folder
            break

    # Insert category folders
    insert_pos = None
    for i, child in enumerate(list(doc)):
        if child.tag == f"{{{NS_KML}}}Folder":
            name_el = child.find(f"{{{NS_KML}}}name")
            if name_el is not None and name_el.text == "Climate":
                insert_pos = i
                break

    # Insert categories in reverse order before Climate
    if insert_pos is not None:
        for cat_name in reversed(CATEGORY_ORDER):
            cf = cat_folders[cat_name]
            if len(cf) > 1 or (len(cf) == 1 and list(cf)[0].tag == f"{{{NS_KML}}}Folder"):
                doc.insert(insert_pos, cf)

    # --- Fix Köppen layer descriptions ---
    for folder, fname in top_folders + sub_folders:
        if fname and "Köppen" in fname:
            descs = folder.findall(f".//{{{NS_KML}}}description", NSMAP)
            for desc in descs:
                if desc.text and "approximate" not in desc.text.lower():
                    desc.text = desc.text.rstrip(".") + ". [NOTE: Approximate — derived from climate narrative; replace with GloH2O V3 GeoTIFF when available.]"

    # --- Fix styles: replace styleUrl refs with gx:CascadingStyle ---
    # Collect all defined styles in Document
    defined_styles = {}
    for child in list(doc):
        if child.tag == f"{{{NS_KML}}}Style":
            sid = child.get("id")
            if sid:
                defined_styles[sid] = child
        elif child.tag == f"{{{NS_GX}}}CascadingStyle":
            sid = child.get("id")
            if sid:
                defined_styles[sid] = child

    # Check all placemarks for broken styleUrl refs
    all_pms = doc.findall(f".//{{{NS_KML}}}Placemark")
    fixed_count = 0
    for pm in all_pms:
        style_url = pm.find(f"{{{NS_KML}}}styleUrl")
        if style_url is not None and style_url.text:
            sid = style_url.text.lstrip("#")
            if sid not in defined_styles:
                name_el = pm.find(f"{{{NS_KML}}}name")
                pm_name = name_el.text if name_el is not None else "unknown"
                poly = pm.find(f".//{{{NS_KML}}}Polygon")
                line = pm.find(f".//{{{NS_KML}}}LineString")
                point = pm.find(f".//{{{NS_KML}}}Point")
                if poly is not None or line is not None:
                    cs = make_cascading_style("4055b0b0", "ff55b0b0", 0.5)
                    parent = style_url.getparent()
                    idx = list(parent).index(style_url)
                    parent.insert(idx, cs)
                    parent.remove(style_url)
                    fixed_count += 1
                elif point is not None:
                    cs = ET.Element(f"{{{NS_GX}}}CascadingStyle")
                    style = ET.SubElement(cs, f"{{{NS_KML}}}Style")
                    icons = ET.SubElement(style, f"{{{NS_KML}}}IconStyle")
                    icolor = ET.SubElement(icons, f"{{{NS_KML}}}color")
                    icolor.text = "ff55b0b0"
                    iscale = ET.SubElement(icons, f"{{{NS_KML}}}scale")
                    iscale.text = "0.8"
                    parent = style_url.getparent()
                    idx = list(parent).index(style_url)
                    parent.insert(idx, cs)
                    parent.remove(style_url)
                    fixed_count += 1

    print(f"Fixed {fixed_count} broken style references")

    # Write output
    tree.write(KML_PATH, xml_declaration=True, encoding="UTF-8")
    print(f"Written: {KML_PATH}")

    # --- Verify ---
    verify = ET.parse(KML_PATH)
    verify_root = verify.getroot()
    verify_doc = verify_root.find(f"{{{NS_KML}}}Document")

    # Count top-level folders
    vfolders = []
    for child in list(verify_doc):
        if child.tag == f"{{{NS_KML}}}Folder":
            name_el = child.find(f"{{{NS_KML}}}name")
            vfolders.append(name_el.text if name_el is not None else "")

    print(f"\nUpdated top-level folders ({len(vfolders)}):")
    for vf in vfolders:
        print(f"  - {vf}")

    # Verify style refs
    vpms = verify_root.findall(f".//{{{NS_KML}}}Placemark")
    vstyles = {}
    for child in list(verify_doc):
        sid = child.get("id")
        if sid:
            vstyles[sid] = True
        if child.tag == f"{{{NS_GX}}}CascadingStyle" and child.get("id"):
            vstyles[child.get("id")] = True

    bad = 0
    for pm in vpms:
        su = pm.find(f"{{{NS_KML}}}styleUrl")
        if su is not None and su.text:
            sid = su.text.lstrip("#")
            if sid not in vstyles:
                bad += 1
                ne = pm.find(f"{{{NS_KML}}}name")
                print(f"  MISSING STYLE #{sid}: {ne.text if ne is not None else '?'}")

    print(f"Style references: {len(vstyles)} defined, {bad} broken")

    # Check no global bounding boxes
    coords = verify_root.findall(f".//{{{NS_KML}}}coordinates")
    coord_text = " ".join(c.text or "" for c in coords)
    global_boxes = 0
    if "-180.000000,65.000000" in coord_text:
        global_boxes += 1
    if "-180.000000,-90.000000" in coord_text:
        global_boxes += 1
    print(f"Global bounding boxes: {global_boxes} {'PASS' if global_boxes == 0 else 'FAIL'}")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
