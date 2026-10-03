"""Finite Basel basemap coverage and local offline image storage."""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TILE_DIRECTORY = ROOT / ".cache/basemap"


def basemap_settings() -> dict:
    """Use one source definition for the browser and offline preparation."""
    return json.loads((ROOT / "config/basemap.json").read_text())


def tile_ranges(bounds, zoom):
    """Return the XYZ rectangles covering a WGS84 bounding box."""
    west, south, east, north = bounds
    size = 2**zoom

    def x(longitude):
        return int((longitude + 180) / 360 * size)

    def y(latitude):
        angle = math.radians(latitude)
        return int((1 - math.asinh(math.tan(angle)) / math.pi) / 2 * size)

    return range(x(west), x(east) + 1), range(y(north), y(south) + 1)


def tile_path(zoom, x, y):
    """Return a path only for valid finite provider coverage; no proxy requests."""
    config = basemap_settings()
    if not config["min_zoom"] <= zoom <= config["max_zoom"]:
        return None
    columns, rows = tile_ranges(config["bounds_wgs84"], zoom)
    if x not in columns or y not in rows:
        return None
    return TILE_DIRECTORY / str(zoom) / str(x) / f"{y}.png"
