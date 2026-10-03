"""Check height encoding, caster preservation, missing cells and alignment."""

import numpy as np
import pytest
import rasterio
from bla_bla_walk.geometry import (
    compact_heights,
    geometry_settings,
    prepare_raster,
    read_heights,
)
from rasterio.transform import from_origin


def test_surface_max_preserves_narrow_caster_and_unknown_block():
    values = np.ma.array(
        [[250, 261, 250, 250], [250, 250, 250, 250]],
        mask=[[False, False, False, True], [False, False, False, False]],
    )
    codes = compact_heights(values, "surface", 0.5, geometry_settings())
    assert codes.tolist() == [[131, -32768]]


def test_terrain_upsampling_does_not_invent_detail_and_preserves_unknown():
    values = np.ma.array([[251.1, 0]], mask=[[False, True]])
    codes = compact_heights(values, "terrain", 2, geometry_settings())
    assert codes.tolist() == [[126, 126, -32768, -32768]] * 2


def test_height_steps_have_at_most_one_metre_rounding_error():
    values = np.ma.array(np.linspace(-100, 600, 701).reshape(1, -1))
    codes = compact_heights(values, "terrain", 1, geometry_settings())
    assert np.max(np.abs(codes * 2 - values)) <= 1
    assert codes[0, 101] * 2 == 2  # Half-step ties round toward positive infinity.


def test_nan_and_infinity_remain_unknown():
    values = np.ma.array([[250, np.nan, np.inf]])
    codes = compact_heights(values, "terrain", 1, geometry_settings())
    assert codes.tolist() == [[125, -32768, -32768]]


def test_height_overflow_is_rejected():
    with pytest.raises(ValueError, match="range"):
        compact_heights(np.ma.array([[100_000]]), "terrain", 1, geometry_settings())


def test_prepared_raster_round_trip_uses_scale_and_mask(tmp_path):
    tile = {"bounds_epsg2056": [2610000, 1266000, 2610004, 1266004]}
    source = tmp_path / "native.tif"
    target = tmp_path / "prepared.tif"
    with rasterio.open(
        source,
        "w",
        driver="GTiff",
        height=2,
        width=2,
        count=1,
        dtype="float32",
        crs="EPSG:2056",
        transform=from_origin(2610000, 1266004, 2, 2),
        nodata=-9999,
    ) as dataset:
        dataset.write(np.array([[251, 252], [253, -9999]], dtype="float32"), 1)
    result = prepare_raster(source, target, tile, "terrain")
    assert result["shape"] == [4, 4]
    assert result["unknown_cells"] == 4
    heights = read_heights(target)
    assert heights[0, 0] == 252
    assert heights.mask[3, 3]
    with rasterio.open(target) as dataset:
        assert dataset.res == (1, 1)
        assert dataset.scales == (2,)
        assert list(dataset.bounds) == tile["bounds_epsg2056"]
        assert dataset.tags()["vertical_reference"] == "LN02 / EPSG:5728"
    tile["bounds_epsg2056"][0] += 1
    with pytest.raises(ValueError, match="bounds"):
        prepare_raster(source, target, tile, "terrain")
