"""Consumer contract: native windows, explicit gaps and unsupported receivers."""

import json

import numpy as np
import pytest
from bla_bla_walk.geometry_inventory import PIPELINE_VERSION
from bla_bla_walk.geometry_prepare import process_peak_bytes
from bla_bla_walk.geometry_rasters import file_digest
from bla_bla_walk.geometry_store import GeometryStore, halo_supported
from bla_bla_walk.interfaces import GeometryWindow


@pytest.fixture
def store(tmp_path):
    (tmp_path / "arrays").mkdir()
    assets = {}
    for product, height in (("surface", 275), ("terrain", 270)):
        values = np.full((2000, 2000), height, dtype="float32")
        if product == "surface":
            values[0, 0] = -9999
            values[0, 1] = 269
        path = tmp_path / "arrays" / f"2610-1266-{product}.npy"
        np.save(path, values)
        assets[product] = {
            "status": "prepared",
            "bytes": path.stat().st_size,
            "sha256": file_digest(path),
        }
    ledger = {
        "schema_version": 2,
        "geometry_version": PIPELINE_VERSION + ":synthetic",
        "tiles": {
            "2610-1266": {
                "status": "prepared",
                "nominal_year_mismatch": True,
                "assets": assets,
            }
        },
    }
    (tmp_path / "manifest.json").write_text(json.dumps(ledger))
    return GeometryStore(tmp_path, "synthetic")


def test_native_window_coordinates_masks_and_contract(store):
    window = store.read_window("2610-1266", (0, 2), (0, 4))
    assert isinstance(window, GeometryWindow)
    assert window.bounds_epsg2056 == (2610000, 1266999, 2610002, 1267000)
    assert window.nominal_year_mismatch is True
    assert not window.surface_valid[0, 0]
    assert window.surface[0, 1] == 269  # never clamp inconsistent surveys
    assert not window.receiver_valid[0, 1]
    assert window.receiver_valid[1].all()


@pytest.mark.parametrize("kind", ["bridge", "canopy", "tunnel"])
def test_unsupported_receivers_never_inherit_ground_elevation(store, kind):
    window = store.read_window("2610-1266", (0, 4), (0, 4), receiver_kind=kind)
    assert not window.receiver_valid.any()
    assert window.terrain_valid.all()  # terrain sample is valid, receiver isn't


def test_missing_border_geometry_is_unknown_and_window_bounded(store):
    window = store.read_window("2607-1270", (0, 4), (0, 4))
    assert not window.surface_valid.any()
    assert not window.receiver_valid.any()
    with pytest.raises(ValueError, match="inside"):
        store.read_window("2610-1266", (0, 2001))
    with pytest.raises(ValueError, match="version"):
        GeometryStore(store.root, "different_inventory")


def test_corrupt_prepared_geometry_never_reused_by_consumer(store):
    path = store.root / "arrays/2610-1266-surface.npy"
    with path.open("r+b") as out:
        out.seek(-4, 2)
        out.write(b"xxxx")
    with pytest.raises(ValueError, match="checksum"):
        store.read_window("2610-1266", (0, 4), (0, 4))


def test_ray_reach_handles_actual_relief_and_missing_halo():
    assert halo_supported(250, 0, 10, 1500, missing_geometry=False)
    assert not halo_supported(250, 50, 10, 1500, missing_geometry=False)
    assert not halo_supported(205, 0, 9, 1500, missing_geometry=False)
    assert not halo_supported(205, 0, 30, 1500, missing_geometry=True)
    assert not halo_supported(251, 0, 30, 1500, missing_geometry=False)
    assert not halo_supported(float("nan"), 0, 30, 1500, missing_geometry=False)


def test_linux_memory_measurement_uses_current_executable_peak(monkeypatch):
    from pathlib import Path

    monkeypatch.setattr("bla_bla_walk.geometry_prepare.sys.platform", "linux")
    monkeypatch.setattr(Path, "read_text", lambda _: "VmRSS: 100 kB\nVmHWM: 12345 kB\n")
    assert process_peak_bytes() == 12345 * 1024
