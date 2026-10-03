"""Production compact windows apply scales and keep receiver uncertainty."""

import json

import numpy as np
import pytest
import rasterio
from bla_bla_walk.geometry import geometry_settings, sha256_file
from bla_bla_walk.geometry_compact_audit import scaled_pair, scaled_seam
from bla_bla_walk.geometry_store import CompactGeometryStore
from rasterio.transform import from_origin


def test_compact_window_scales_mask_and_bridge_contract(tmp_path):
    assets = {}
    for product, code in (("surface", 135), ("terrain", 134)):
        path = tmp_path / f"2610-1266-{product}.tif"
        codes = np.full((1000, 1000), code, dtype="int16")
        if product == "surface":
            codes[0, :2] = [-32768, 133]
        with rasterio.open(
            path,
            "w",
            driver="GTiff",
            width=1000,
            height=1000,
            count=1,
            dtype="int16",
            crs="EPSG:2056",
            nodata=-32768,
            transform=from_origin(2610000, 1267000, 1, 1),
        ) as out:
            out.write(codes, 1)
            out.scales = (2,)
        assets[f"2610-1266-{product}"] = {
            "preparation_version": "synthetic",
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
            "survey_year_mismatch": True,
        }
    (tmp_path / "manifest.json").write_text(
        json.dumps(
            {
                "settings": geometry_settings(),
                "preparation_version": "synthetic",
                "assets": assets,
            }
        )
    )
    store = CompactGeometryStore(tmp_path)
    window = store.read_window("2610-1266", (0, 4), (0, 4))
    assert window.surface[1, 0] == 270  # band scale, never raw code 135
    assert window.terrain[0, 0] == 268
    assert not window.surface_valid[0, 0]
    assert not window.receiver_valid[0, 1]  # negative difference retained
    assert window.resolution_m == 1 and window.height_step_m == 2
    assert window.bounds_epsg2056 == (2610000, 1266996, 2610004, 1267000)
    assert not store.read_window(
        "2610-1266", (0, 4), (0, 4), receiver_kind="bridge"
    ).receiver_valid.any()
    assert not store.read_window("2607-1270", (0, 4), (0, 4)).receiver_valid.any()
    with pytest.raises(ValueError, match="inside"):
        store.read_window("2610-1266", (0, 1001))
    path = tmp_path / "2610-1266-surface.tif"
    with path.open("r+b") as out:
        out.seek(-1, 2)
        out.write(b"x")
    with pytest.raises(ValueError, match="checksum"):
        store.read_window("2610-1266", (0, 4), (0, 4))


def test_compact_pair_and_seam_keep_negatives_and_unknown():
    surface = np.array([[270, -9999], [266, 270]], dtype="float32")
    terrain = np.full((2, 2), 268, dtype="float32")
    pair = scaled_pair(surface, terrain)
    assert pair["invalid_pair_cells"] == 1
    assert pair["negative_relative_height_cells"] == 1
    assert pair["relative_height_range_m"] == [-2, 2]
    seam = scaled_seam(surface, terrain, "east")
    assert seam["unknown_samples"] == 1
    assert seam["absolute_jump_p50_p95_max_m"] == [2, 2, 2]
