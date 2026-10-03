"""Load the checked Basel walking alternatives as a canonical map layer."""

import json
import math
from pathlib import Path

from ..interfaces import LineGeometry, MapFeature, MapLayer, Provenance, RouteMetrics

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ROUTES_PATH = PROJECT_ROOT / "data" / "routes" / "demo.geojson"
DEFAULT_SCENARIOS_PATH = PROJECT_ROOT / "data" / "scenarios.json"


def load_demo_routes(
    routes_path: Path = DEFAULT_ROUTES_PATH,
    scenarios_path: Path = DEFAULT_SCENARIOS_PATH,
) -> MapLayer:
    """Return the two sourced alternatives, using T2's walking-time rule."""
    collection = json.loads(routes_path.read_text(encoding="utf-8"))
    metadata = collection["metadata"]
    features = collection["features"]
    if len(features) != 2:
        raise ValueError(
            "The checked Basel snapshot must contain exactly two alternatives"
        )

    scenario = json.loads(scenarios_path.read_text(encoding="utf-8"))
    speed = float(scenario["rules"]["walking_speed_m_per_s"])
    if not math.isfinite(speed) or speed <= 0:
        raise ValueError("walking_speed_m_per_s must be a positive finite number")

    provenance = Provenance(
        provider=metadata["provider"],
        source_url=metadata["osm_copyright_url"],
        attribution=metadata["attribution"],
        licence=metadata["licence"],
        fixture=False,
        retrieved_at=metadata["retrieved_at"],
    )
    mapped = []
    for item in features:
        properties = item["properties"]
        coords = item["geometry"]["coordinates"]
        distance = float(properties["distance_m"])
        path = ", ".join(properties["path_names"])
        explanation = (
            f"Walking path via {path}. "
            f"Geometry snapshot retrieved {metadata['snapshot_date']}. "
            f"Walking duration uses T2's {speed:g} m/s assumption. "
            f"{properties['access_note']} {properties['coverage_note']}"
        )
        mapped.append(
            MapFeature(
                id=properties["route_id"],
                label=properties["label"],
                kind="route",
                geometry=LineGeometry(type="LineString", coordinates=coords),
                # Route geometry is available, but local access has not been audited.
                availability="unknown",
                explanation=explanation,
                provenance=provenance,
                route=RouteMetrics(distance_m=distance, duration_s=distance / speed),
            )
        )

    return MapLayer(
        id="demo-walking-routes",
        label="Walking alternatives",
        kind="route",
        availability="unknown",
        explanation=(
            "Two FOSSGIS foot-profile alternatives from "
            f"{metadata['start']['name']} to {metadata['end']['name']}; "
            f"OSM network snapshot retrieved {metadata['snapshot_date']}. "
            "The exact routing-graph build timestamp is not exposed, "
            "and the service has no temporary-closure feed "
            "or per-segment access audit. "
            "Treat access as unverified; outside shade-calculation coverage, "
            "route support must be marked unsupported."
        ),
        features=mapped,
    )
