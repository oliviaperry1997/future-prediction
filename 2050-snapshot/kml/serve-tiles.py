#!/usr/bin/env python3
"""
CORS-enabled local tile server for Köppen-Geiger XYZ tiles.

Usage:
  python3 serve-tiles.py

Then add Tile Overlays in Google Earth Web with URLs:
  http://localhost:8080/tiles/climate-2050/{z}/{x}/{y}.png
  http://localhost:8080/tiles/biomes-current/{z}/{x}/{y}.png
  http://localhost:8080/tiles/biomes-2050/{z}/{x}/{y}.png
  http://localhost:8080/tiles/inundation-2050/{z}/{x}/{y}.png

Chrome allows HTTP requests to localhost from HTTPS pages (mixed-content exception),
so this works even though Google Earth Web is served over HTTPS.
"""

import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT      = 8080
TILES_DIR = os.path.join(os.path.dirname(__file__), "tiles")
SERVE_DIR = os.path.dirname(__file__)   # serve from kml/ so path is tiles/z/x/y.png


class CORSHandler(SimpleHTTPRequestHandler):
    """Serve files from the kml/ directory with permissive CORS headers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def log_message(self, fmt, *args):
        # Suppress per-request noise; show only errors
        if args and str(args[1]) not in ("200", "304", "404"):
            super().log_message(fmt, *args)


def main():
    if not os.path.isdir(TILES_DIR):
        print(f"WARNING: tiles/ directory not found at {TILES_DIR}")
        print("Run generate-koppen-tiles.py first.")

    server = HTTPServer(("localhost", PORT), CORSHandler)
    print(f"Tile server running at http://localhost:{PORT}/")
    print(f"Serving from: {SERVE_DIR}")
    print()
    print("Add this URL as a Tile Overlay in Google Earth Web:")
    print(f"  http://localhost:{PORT}/tiles/{{z}}/{{x}}/{{y}}.png")
    print()
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
