#!/usr/bin/env python3
"""
Split climate.kml into files under Google Earth's 10,000 feature limit.

Produces:
  climate-koppen-A.kml  — Tropical (2,692 features)
  climate-koppen-B.kml  — Arid (2,787 features)
  climate-koppen-C.kml  — Temperate (3,871 features)
  climate-koppen-D.kml  — Continental (7,596 features)
  climate-koppen-E.kml  — Polar (2,291 features)
  climate-overlays.kml  — Biomes, SLR, refined placemarks (~100 features)
  climate.kml           — Master file with NetworkLinks to all above
"""
import sys
from lxml import etree
from lxml.etree import QName

KML_NS = "http://www.opengis.net/kml/2.2"
GX_NS = "http://www.google.com/kml/ext/2.2"
NS = f"{{{KML_NS}}}"
GX = f"{{{GX_NS}}}"

KOPPEN_GROUPS = [
    "A — Tropical Climates",
    "B — Arid Climates",
    "C — Temperate Climates",
    "D — Continental Climates",
    "E — Polar Climates",
]

GROUP_FILENAMES = {
    "A — Tropical Climates": "climate-koppen-A.kml",
    "B — Arid Climates": "climate-koppen-B.kml",
    "C — Temperate Climates": "climate-koppen-C.kml",
    "D — Continental Climates": "climate-koppen-D.kml",
    "E — Polar Climates": "climate-koppen-E.kml",
}


def make_kml_doc():
    doc = etree.Element(f"{NS}Document")
    name_el = etree.SubElement(doc, f"{NS}name")
    name_el.text = "2050 Climate"
    vis = etree.SubElement(doc, f"{NS}visibility")
    vis.text = "0"
    return doc


def write_kml(doc, path):
    kml = etree.Element(QName(KML_NS, "kml"), nsmap={
        None: KML_NS, "gx": GX_NS,
    })
    kml.append(doc)
    xml = etree.tostring(kml, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    with open(path, "wb") as f:
        f.write(xml)
    print(f"  {path}: {len(xml):,} bytes")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="climate.kml",
                        help="Input KML file (default: climate.kml)")
    args = parser.parse_args()
    tree = etree.parse(args.input)
    root = tree.getroot()
    old_doc = root.find(f"{NS}Document")

    # Extract all styles (recursively — styles can be nested inside Folders) and top-level folders/placemarks
    all_styles = old_doc.findall(f".//{NS}Style") + old_doc.findall(f".//{NS}StyleMap") + old_doc.findall(f".//{GX}CascadingStyle")
    folders = []
    placemarks = []

    for child in old_doc:
        tag = child.tag
        if tag == f"{NS}Folder":
            folders.append(child)
        elif tag == f"{NS}Placemark":
            placemarks.append(child)

    # Separate Köppen folder from others
    koppen_folder = None
    other_folders = []

    for f in folders:
        name_el = f.find(f"{NS}name")
        name = name_el.text if name_el is not None else ""
        if name == "Köppen-Geiger Climate Classification (2050)":
            koppen_folder = f
        else:
            other_folders.append(f)

    if koppen_folder is None:
        print("ERROR: Köppen folder not found!", file=sys.stderr)
        sys.exit(1)

    # Extract group subfolders from Köppen folder
    group_folders = {}
    for sub in koppen_folder.findall(f"{NS}Folder"):
        name_el = sub.find(f"{NS}name")
        name = name_el.text if name_el is not None else ""
        if name in KOPPEN_GROUPS:
            group_folders[name] = sub

    # Collect all style IDs referenced by placemarks in a folder
    def collect_ref_style_ids(folder):
        ids = set()
        for pm in folder.findall(f".//{NS}Placemark"):
            su = pm.find(f"{NS}styleUrl")
            if su is not None and su.text:
                sid = su.text.lstrip("#")
                if sid:
                    ids.add(sid)
        return ids

    all_style_by_id = {s.get("id", ""): s for s in all_styles}

    # Write one KML per Köppen group
    for group_name in KOPPEN_GROUPS:
        gf = group_folders.get(group_name)
        if gf is None:
            print(f"  WARNING: group folder not found: {group_name}")
            continue

        doc = make_kml_doc()
        needed_ids = collect_ref_style_ids(gf)
        for sid in needed_ids:
            if sid in all_style_by_id:
                doc.append(all_style_by_id[sid])
        doc.append(gf)
        write_kml(doc, GROUP_FILENAMES[group_name])

    # Write non-Köppen overlays file
    doc = make_kml_doc()
    # Only copy styles referenced by overlay placemarks
    overlay_refs = set()
    for f in other_folders:
        overlay_refs |= collect_ref_style_ids(f)
    for pm in placemarks:
        su = pm.find(f"{NS}styleUrl")
        if su is not None and su.text:
            overlay_refs.add(su.text.lstrip("#"))
    for sid in overlay_refs:
        if sid in all_style_by_id:
            doc.append(all_style_by_id[sid])
    for f in other_folders:
        doc.append(f)
    for pm in placemarks:
        doc.append(pm)
    write_kml(doc, "climate-overlays.kml")

    # Write master climate.kml with NetworkLinks
    doc = make_kml_doc()
    master_name = doc.find(f"{NS}name")
    master_name.text = "2050 Climate (Master)"

    kml_all_styles = ["climate-overlay", "climate-overlay-hi", "climate-overlay",
                      "climate-overlay-hi", "climate-basin", "climate-arctic"]

    for group_name in KOPPEN_GROUPS:
        fname = GROUP_FILENAMES[group_name]
        nl = etree.SubElement(doc, f"{NS}NetworkLink")
        nl_name = etree.SubElement(nl, f"{NS}name")
        nl_name.text = group_name
        nl_link = etree.SubElement(nl, f"{NS}Link")
        nl_href = etree.SubElement(nl_link, f"{NS}href")
        nl_href.text = fname

    nl = etree.SubElement(doc, f"{NS}NetworkLink")
    nl_name = etree.SubElement(nl, f"{NS}name")
    nl_name.text = "Climate Overlays (Biomes, SLR, Placemarks)"
    nl_link = etree.SubElement(nl, f"{NS}Link")
    nl_href = etree.SubElement(nl_link, f"{NS}href")
    nl_href.text = "climate-overlays.kml"

    write_kml(doc, "climate.kml")

    print("\nDone. Import each file separately into Google Earth.")


if __name__ == "__main__":
    main()
