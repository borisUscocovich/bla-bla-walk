"""A real local raster batch resumes only verified prepared output."""

import json
from pathlib import Path

import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

from bla_bla_walk.geometry_prepare import prepare_batch
from bla_bla_walk.geometry_rasters import file_digest

ROOT = Path(__file__).resolve().parents[2]


def test_batch_resume_reuses_verified_arrays_and_repairs_corruption(
    tmp_path, monkeypatch
):
    inventory = json.loads((ROOT / "data/tile-inventory.json").read_text())
    manifest = json.loads((ROOT / "data/source-manifest.json").read_text())
    source = tmp_path / "synthetic.tif"
    with rasterio.open(
        source,
        "w",
        driver="GTiff",
        count=1,
        dtype="float32",
        width=2000,
        height=2000,
        crs="EPSG:2056",
        transform=from_origin(2610000, 1267000, 0.5, 0.5),
        nodata=-9999,
    ) as out:
        out.write(np.full((2000, 2000), 270, dtype="float32"), 1)
    monkeypatch.setattr(
        "bla_bla_walk.geometry_prepare.acquire_asset", lambda *_: source
    )
    root = tmp_path / "prepared"
    ledger = prepare_batch(inventory, manifest, root, "scenes", 1)
    assert ledger["tiles"]["2610-1266"]["pair"]["valid_pair_cells"] == 4000000
    target = root / "arrays/2610-1266-surface.npy"
    digest = file_digest(target)
    modified = target.stat().st_mtime_ns
    prepare_batch(inventory, manifest, root, "scenes", 1)
    assert target.stat().st_mtime_ns == modified
    with target.open("r+b") as out:
        out.seek(-4, 2)
        out.write(b"xxxx")
    prepare_batch(inventory, manifest, root, "scenes", 1)
    assert file_digest(target) == digest
    assert not list(root.rglob("*.part"))


def test_batch_failure_is_explicit_and_next_run_repairs_it(tmp_path, monkeypatch):
    inventory = json.loads((ROOT / "data/tile-inventory.json").read_text())
    manifest = json.loads((ROOT / "data/source-manifest.json").read_text())

    def unavailable(*_):
        raise OSError("synthetic source unavailable")

    monkeypatch.setattr("bla_bla_walk.geometry_prepare.acquire_asset", unavailable)
    ledger = prepare_batch(inventory, manifest, tmp_path, "scenes", 1)
    assert ledger["tiles"]["2610-1266"]["status"] == "preparation_failed"
    assert "source unavailable" in ledger["tiles"]["2610-1266"]["error"]
    assert json.loads((tmp_path / "manifest.json").read_text()) == ledger


def test_memory_budget_stops_batch_after_persisting_evidence(tmp_path, monkeypatch):
    inventory = json.loads((ROOT / "data/tile-inventory.json").read_text())
    manifest = json.loads((ROOT / "data/source-manifest.json").read_text())
    monkeypatch.setattr(
        "bla_bla_walk.geometry_prepare.process_peak_bytes", lambda: 800 * 1024**2
    )
    monkeypatch.setattr(
        "bla_bla_walk.geometry_prepare.acquire_asset",
        lambda *_: (_ for _ in ()).throw(OSError("synthetic")),
    )
    with pytest.raises(ValueError, match="memory"):
        prepare_batch(inventory, manifest, tmp_path, "scenes", 1)
    assert not json.loads((tmp_path / "manifest.json").read_text())["budget_pass"]
