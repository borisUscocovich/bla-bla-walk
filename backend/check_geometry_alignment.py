"""Check the local T8 review page with actual OpenLayers and live Basel tiles."""

import functools
import http.server
import json
import os
import shutil
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

from bla_bla_walk.geometry_store import GeometryStore


def main():
    """Save browser alignment measurements and screenshots for human inspection."""
    directory = Path(".hack/t8/alignment").resolve()
    executable = os.environ.get("CHROMIUM_PATH") or shutil.which("chromium")
    if not executable:
        raise SystemExit("Geometry alignment requires installed Chromium")
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=directory
    )
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=executable)
            page = browser.new_page(viewport={"width": 1500, "height": 900})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(f"http://127.0.0.1:{server.server_port}")
            page.wait_for_function("window.maps?.length === 2")
            page.wait_for_function(
                "window.overlayLayers.every(l=>l.getSource().getImage("
                "l.getSource().getImageExtent(),2,1,"
                "ol.proj.get('EPSG:3857'))?.getState()===2)"
            )
            page.wait_for_function("window.loadedBasemapTiles > 0", timeout=30_000)
            page.screenshot(path=str(directory / "overlay.png"), full_page=True)
            measurements = page.evaluate("""() => evidence.references.map((ref,i)=>{
                const map=window.maps[i];
                const a=map.getPixelFromCoordinate(ref.point_3857);
                const b=map.getPixelFromCoordinate(ref.pixel_centre_3857);
                const roundTrip=map.getCoordinateFromPixel(a);
                return {id:ref.id, reference_pixel:a, native_centre_pixel:b,
                    separation_screen_px:Math.hypot(a[0]-b[0],a[1]-b[1]),
                    round_trip_error_3857_m:Math.hypot(
                        roundTrip[0]-ref.point_3857[0],
                        roundTrip[1]-ref.point_3857[1])};
            })""")
            page.locator("#toggle").click()
            page.screenshot(path=str(directory / "basemap.png"), full_page=True)
            for measurement in measurements:
                assert measurement["separation_screen_px"] < 1
                assert measurement["round_trip_error_3857_m"] < 1e-6
            assert not errors, errors
            report = {
                "renderer": "Chromium/OpenLayers",
                "live_basemap_tiles_loaded": page.evaluate("window.loadedBasemapTiles"),
                "references": measurements,
                "browser_errors": errors,
            }
            # Manual diagnostic location on the span displayed on the admitted
            # Basel basemap, northeast of the centre reference (Mittlere Brücke).
            # This identifies a test location, never a verified deck elevation.
            root = Path("data/geometry")
            ledger = json.loads((root / "manifest.json").read_text())
            store = GeometryStore(root, ledger["inventory_sha256"])
            bridge = store.read_window(
                "2611-1267", (589, 591), (709, 711), receiver_kind="bridge"
            )
            assert not bridge.receiver_valid.any()
            report["bridge_check"] = {
                "reference_epsg2056": [2611355, 1267705],
                "location_evidence": (
                    "Manual span diagnostic from rendered official Basel basemap"
                ),
                "surface_samples_m": bridge.surface.tolist(),
                "bare_terrain_samples_m": bridge.terrain.tolist(),
                "walking_deck_elevation": "unknown",
                "receiver_valid_cells": int(bridge.receiver_valid.sum()),
            }
            (directory / "browser-check.json").write_text(
                json.dumps(report, indent=2) + "\n"
            )
            browser.close()
            print(json.dumps(report))
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
