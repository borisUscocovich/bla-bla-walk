"""Acceptance checks for the checked walking-route snapshot and adapter."""

import json
import math
from pathlib import Path

from bla_bla_walk.adapters.routes import load_demo_routes

ROOT = Path(__file__).resolve().parents[2]
ROUTES_PATH = ROOT / "data" / "routes" / "demo.geojson"


def test_snapshot_has_two_distinct_routes_and_pinned_endpoints():
    snapshot = json.loads(ROUTES_PATH.read_text(encoding="utf-8"))
    metadata = snapshot["metadata"]
    routes = snapshot["features"]

    assert len(routes) == 2
    assert [route["properties"]["route_id"] for route in routes] == [
        "demo-route-a",
        "demo-route-b",
    ]
    assert routes[0]["geometry"]["coordinates"] != routes[1]["geometry"]["coordinates"]
    assert metadata["start"]["osm_feature"] == "way/659612290"
    assert metadata["end"]["osm_feature"] == "way/193681195"
    assert metadata["start"]["snap_distance_m"] < 10
    assert metadata["end"]["snap_distance_m"] < 10
    for route in routes:
        coords = route["geometry"]["coordinates"]
        assert math.dist(coords[0], metadata["start"]["snapped_coordinates"]) < 1e-6
        assert math.dist(coords[-1], metadata["end"]["snapped_coordinates"]) < 1e-6
        assert route["properties"]["distance_m"] > 0


def test_adapter_preserves_provenance_and_uses_t2_duration_rule():
    layer = load_demo_routes()
    assert len(layer.features) == 2
    assert layer.availability == "unknown"
    for feature in layer.features:
        assert feature.provenance.fixture is False
        assert "OpenStreetMap" in feature.provenance.attribution
        assert feature.provenance.retrieved_at is not None
        assert feature.route is not None
        assert feature.route.duration_s == feature.route.distance_m
        assert "temporary closure feed" in feature.explanation
        assert "unverified" in feature.explanation
    assert "graph build timestamp is not exposed" in layer.explanation


def test_snapshot_records_route_source_and_snapshot_limits():
    metadata = json.loads(ROUTES_PATH.read_text(encoding="utf-8"))["metadata"]
    assert metadata["route_profile"] == "foot"
    assert metadata["route_engine"] == "OSRM"
    assert metadata["snapshot_date"] == "2026-10-03"
    assert "not exposed" in metadata["snapshot_date_basis"]
    assert "ODbL" in metadata["licence"]
