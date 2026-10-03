"""Offline serving must never fall back to a remote provider."""

from bla_bla_walk import basemap
from bla_bla_walk.main import app
from fastapi.testclient import TestClient


def test_tile_ranges_and_invalid_requests():
    columns, rows = basemap.tile_ranges(basemap.basemap_settings()["bounds_wgs84"], 12)
    assert len(columns) * len(rows) == 9
    assert basemap.tile_path(11, 0, 0) is None
    assert basemap.tile_path(18, 0, 0) is None
    assert basemap.tile_path(14, -1, -1) is None


def test_saved_tile_served_and_missing_tile_explicit(tmp_path, monkeypatch):
    monkeypatch.setattr(basemap, "TILE_DIRECTORY", tmp_path)
    columns, rows = basemap.tile_ranges(basemap.basemap_settings()["bounds_wgs84"], 14)
    x, y = columns.start, rows.start
    client = TestClient(app)
    path = basemap.tile_path(14, x, y)
    assert client.get(f"/tiles/14/{x}/{y}.png").status_code == 404
    path.parent.mkdir(parents=True)
    path.write_bytes(b"saved image")
    response = client.get(f"/tiles/14/{x}/{y}.png")
    assert response.status_code == 200
    assert response.content == b"saved image"
    assert response.headers["content-type"] == "image/png"
    assert client.get("/tiles/14/-1/-1.png").status_code == 404
    assert client.get("/config/basemap.json").json() == basemap.basemap_settings()
