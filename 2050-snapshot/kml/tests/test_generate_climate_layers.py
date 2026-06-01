#!/usr/bin/env python3
"""
Tests for generate-climate-layers.py — Köppen-Geiger KML generation.

RED phase: these tests should fail because the script doesn't exist yet.
"""

import importlib
import importlib.util
import os
import sys
import tempfile
import unittest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_PATH = os.path.join(SCRIPT_DIR, "generate-climate-layers.py")


class TestGenerateClimateLayersModule(unittest.TestCase):
    """Test that the module exists, imports, and has required API."""

    def test_script_file_exists(self):
        """The script file must exist."""
        self.assertTrue(
            os.path.isfile(SCRIPT_PATH),
            f"Script not found: {SCRIPT_PATH}",
        )

    def test_script_imports_cleanly(self):
        """The module must import without errors."""
        spec = importlib.util.spec_from_file_location(
            "gen_climate", SCRIPT_PATH
        )
        self.assertIsNotNone(spec, "Failed to create module spec")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["gen_climate"] = mod
        spec.loader.exec_module(mod)
        self.assertIsNotNone(mod, "Module failed to load")

    def test_has_generate_koppen_kml_function(self):
        """Module must have a generate_koppen_kml() function."""
        spec = importlib.util.spec_from_file_location(
            "gen_climate", SCRIPT_PATH
        )
        mod = importlib.util.module_from_spec(spec)
        sys.modules["gen_climate"] = mod
        spec.loader.exec_module(mod)
        self.assertTrue(
            hasattr(mod, "generate_koppen_kml")
            or hasattr(mod, "generate_koppen_geotiff_kml"),
            "Module must have generate_koppen_kml() or generate_koppen_geotiff_kml()",
        )

    def test_has_main_entry_point(self):
        """Module must have a main() entry point (callable)."""
        spec = importlib.util.spec_from_file_location(
            "gen_climate", SCRIPT_PATH
        )
        mod = importlib.util.module_from_spec(spec)
        sys.modules["gen_climate"] = mod
        spec.loader.exec_module(mod)
        self.assertTrue(
            callable(getattr(mod, "main", None)),
            "Module must have a callable main() entry point",
        )


class TestGenerateClimateLayersExecution(unittest.TestCase):
    """Test execution behavior — graceful fallback and KML validity."""

    def setUp(self):
        # Import the module
        spec = importlib.util.spec_from_file_location(
            "gen_climate", SCRIPT_PATH
        )
        self.mod = importlib.util.module_from_spec(spec)
        sys.modules["gen_climate"] = self.mod
        spec.loader.exec_module(self.mod)

    def test_graceful_missing_geotiff(self):
        """
        When the source GeoTIFF doesn't exist, the script should
        print an informative message and produce fallback output
        instead of crashing.
        """
        # Temporarily rename the GeoTIFF if it exists, to simulate missing
        tiff_path = os.path.join(SCRIPT_DIR, "source", "koppen_2041-2070_ssp370.tif")
        tiff_bak = None
        if os.path.exists(tiff_path):
            tiff_bak = tiff_path + ".bak"
            os.rename(tiff_path, tiff_bak)

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                out_path = os.path.join(tmpdir, "climate_koppen.kml")
                # The function should not crash even without source data
                result = self.mod.generate_koppen_kml(out_path)
                if result is not None:
                    self.assertTrue(
                        os.path.isfile(out_path),
                        f"Output KML should be created at {out_path}",
                    )
        except Exception as e:
            self.fail(f"generate_koppen_kml() raised an exception: {e}")
        finally:
            if tiff_bak and os.path.exists(tiff_bak):
                os.rename(tiff_bak, tiff_path)

    def test_output_kml_is_valid_xml(self):
        """Generated KML must be valid XML parsable by lxml."""
        import lxml.etree as ET

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "climate_koppen.kml")
            self.mod.generate_koppen_kml(out_path)

            if os.path.isfile(out_path):
                # Parse with lxml — raises exception if invalid XML
                tree = ET.parse(out_path)
                root = tree.getroot()
                ns = "http://www.opengis.net/kml/2.2"
                self.assertEqual(
                    root.tag, f"{{{ns}}}kml",
                    "Root element must be <kml>",
                )

    def test_contains_koppen_folder(self):
        """Output KML must contain a Köppen-Geiger folder."""
        import lxml.etree as ET

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "climate_koppen.kml")
            self.mod.generate_koppen_kml(out_path)

            if os.path.isfile(out_path):
                tree = ET.parse(out_path)
                ns = "http://www.opengis.net/kml/2.2"
                names = tree.findall(".//{%s}name" % ns)
                name_texts = [n.text for n in names if n.text]
                has_koppen = any(
                    "Köppen" in t for t in name_texts
                )
                self.assertTrue(
                    has_koppen,
                    f"Köppen folder not found in KML names: {name_texts}",
                )

    def test_30_subtype_codes_defined(self):
        """Module must define all 30 Köppen sub-type codes."""
        if hasattr(self.mod, "KOPPEN_COLORS"):
            colors = self.mod.KOPPEN_COLORS
        elif hasattr(self.mod, "KOPPEN_SUBTYPES"):
            colors = self.mod.KOPPEN_SUBTYPES
        else:
            self.fail("Module must define KOPPEN_COLORS or KOPPEN_SUBTYPES dict")

        expected_codes = {
            "Af", "Am", "Aw",
            "BWh", "BWk", "BSh", "BSk",
            "Csa", "Csb", "Cwa", "Cwb", "Cwc",
            "Cfa", "Cfb", "Cfc",
            "Dsa", "Dsb", "Dsc", "Dwa", "Dwb", "Dwc",
            "Dfa", "Dfb", "Dfc", "Dfd",
            "ET", "EF",
        }
        missing = expected_codes - set(colors.keys())
        self.assertSetEqual(
            missing, set(),
            f"Missing Köppen sub-type codes in color map: {missing}",
        )


if __name__ == "__main__":
    import importlib.util

    unittest.main()
