"""Native decoding, masks and resumability with controlled georeferenced rasters."""

from pathlib import Path

import numpy as np
import pytest
import rasterio
from bla_bla_walk.geometry_rasters import decode_native, pair_evidence
from rasterio.transform import from_origin


def write_raster(path: Path, values, *, origin=(2610000, 1266002), mask=None):
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        count=1,
        dtype="float32",
        width=values.shape[1],
        height=values.shape[0],
        crs="EPSG:2056",
        transform=from_origin(*origin, 0.5, 0.5),
        nodata=-9999,
    ) as out:
        out.write(values.astype("float32"), 1)
        if mask is not None:
            out.write_mask(mask)


def test_decode_preserves_negative_heights_and_invalid_mask(tmp_path):
    values = np.full((4, 4), 250, dtype="float32")
    values[0] = [-9999, np.nan, np.inf, 247]
    mask = np.full((4, 4), 255, dtype="uint8")
    mask[1, 0] = 0
    source, output = tmp_path / "input.tif", tmp_path / "surface.npy"
    write_raster(source, values, mask=mask)
    result = decode_native(source, output, [2610000, 1266000, 2610002, 1266002])
    prepared = np.load(output)
    assert result["invalid_cells"] == 4
    assert result["nonfinite_cells"] == 2
    assert prepared[0, 3] == 247
    assert np.all(prepared[0, :3] == -9999)
    assert prepared[1, 0] == -9999
    np.save(tmp_path / "terrain.npy", np.full((4, 4), 250, dtype="float32"))
    pair = pair_evidence(output, tmp_path / "terrain.npy")
    assert pair["valid_pair_cells"] == 12
    assert pair["surface_below_terrain_over_1m_cells"] == 1
    assert pair["relative_height_range_m"] == [-3, 0]


def test_grid_shift_rejected_without_replacing_previous_output(tmp_path):
    source, target = tmp_path / "shifted.tif", tmp_path / "surface.npy"
    target.write_bytes(b"previous verified output")
    write_raster(source, np.zeros((4, 4)), origin=(2610000.5, 1266002))
    with pytest.raises(ValueError, match="grid"):
        decode_native(source, target, [2610000, 1266000, 2610002, 1266002])
    assert target.read_bytes() == b"previous verified output"
    assert not list(tmp_path.glob("*.part"))


def test_interrupted_decoder_leaves_no_partial_output(tmp_path, monkeypatch):
    source, target = tmp_path / "input.tif", tmp_path / "surface.npy"
    write_raster(source, np.zeros((4, 4)))
    monkeypatch.setattr(
        np.lib.format,
        "write_array_header_2_0",
        lambda *a, **k: (_ for _ in ()).throw(OSError("disk failure")),
    )
    with pytest.raises(OSError, match="disk failure"):
        decode_native(source, target, [2610000, 1266000, 2610002, 1266002])
    assert not target.exists()
    assert not list(tmp_path.glob("*.part"))
