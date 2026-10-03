"""T8 inventory checks: prevent incorrect grids or coverage claims."""

import copy
import json
from pathlib import Path

import pytest

from bla_bla_walk.geometry import plan_preparation

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def inputs():
    inventory = json.loads((ROOT / "data/tile-inventory.json").read_text())
    manifest = json.loads((ROOT / "data/source-manifest.json").read_text())
    return inventory, manifest["acceptance_budget"]


def test_full_inventory_preserves_unknown_cells_and_buffer_gaps(inputs):
    ledger = plan_preparation(*inputs)
    assert ledger["counts"]["receiver_tiles"] == 65
    assert ledger["counts"]["available_assets"] == 225
    assert ledger["prepared_tiles"] == 0
    assert ledger["status"] == "planned_not_prepared"
    assert len(ledger["counts"]["missing_tiles"]["surface"]) == 10
    assert len(ledger["counts"]["missing_tiles"]["terrain"]) == 43
    assert ledger["counts"]["paired_nominal_year_mismatches"] == 96
    assert all(row["cell_validation"] == "pending" for row in ledger["tiles"])
    assert ledger["storage_estimate"]["remaining_budget_bytes"] > 0
    assert ledger == plan_preparation(*inputs)


@pytest.mark.parametrize(
    "field,value",
    [
        ("tiepoint", [0, 0, 0, 0, 0, 0]),
        ("crs_epsg", 4326),
        ("nodata", "0"),
        ("shape", [1000, 1000]),
        ("pixel_scale", [1, 1, 0]),
        ("vertical_crs", "unknown"),
    ],
)
def test_misaligned_or_unknown_grid_rejected(inputs, field, value):
    inventory, budget = inputs
    asset = next(
        tile["surface"]
        for tile in inventory["tiles"]
        if tile["surface"]["status"] == "catalog_available"
    )
    asset["header"][field] = value
    with pytest.raises(ValueError):
        plan_preparation(inventory, budget)


def test_receiver_gap_rejected_before_claiming_coverage(inputs):
    inventory, budget = inputs
    receiver = next(tile for tile in inventory["tiles"] if tile["role"] == "receiver")
    receiver["terrain"] = {"status": "missing_from_catalog"}
    with pytest.raises(ValueError, match="Receiver asset missing"):
        plan_preparation(inventory, budget)


def test_duplicate_tile_rejected(inputs):
    inventory, budget = inputs
    inventory["tiles"].append(copy.deepcopy(inventory["tiles"][0]))
    with pytest.raises(ValueError, match="Duplicate tile"):
        plan_preparation(inventory, budget)


def test_summary_and_survey_flags_cannot_drift(inputs):
    inventory, budget = inputs
    inventory["summary"]["available_assets"] -= 1
    with pytest.raises(ValueError, match="summary mismatch"):
        plan_preparation(inventory, budget)
    inventory["summary"]["available_assets"] += 1
    paired = next(
        tile for tile in inventory["tiles"] if tile["survey_year_mismatch"] is True
    )
    paired["survey_year_mismatch"] = False
    with pytest.raises(ValueError, match="Survey mismatch"):
        plan_preparation(inventory, budget)


def test_budget_rejected(inputs):
    inventory, budget = inputs
    budget["geometry_disk_gib"] = 1
    with pytest.raises(ValueError, match="disk budget"):
        plan_preparation(inventory, budget)


def test_verified_metadata_fixture_preserves_pinned_inventory(inputs):
    fixture = json.loads((ROOT / "data/fixtures/geometry-metadata.json").read_text())
    plan = plan_preparation(*inputs)
    assert fixture["inventory_sha256"] == plan["inventory_sha256"]
    assert fixture["counts"] == plan["counts"]
    assert fixture["status"] == "prepared_with_explicit_limitations"
    assert fixture["receiver_tiles_prepared"] == 65
    assert fixture["prepared_assets"] == 225
    assert len(fixture["tiles"]) == 139
    assert all(
        row["status"] in ("prepared", "documented_catalog_gap")
        for row in fixture["tiles"].values()
    )
    assert fixture["resolution_metres"] == 0.5
    assert fixture["budget_pass"]
    assert not fixture["reach_evidence"]["blanket_1500m_halo_supported"]


def test_asset_resume_verifies_content_and_replaces_corruption(tmp_path, monkeypatch):
    import hashlib
    import io

    from bla_bla_walk.geometry_assets import acquire_asset

    content = b"synthetic raster download"
    asset = {
        "asset_url": "https://data.geo.admin.ch/synthetic.tif",
        "catalog_checksum": "1220" + hashlib.sha256(content).hexdigest(),
        "header": {"asset_bytes": len(content)},
    }
    calls = []

    def download(*args, **kwargs):
        calls.append(True)
        response = io.BytesIO(content)
        response.status = 200
        return response

    monkeypatch.setattr("urllib.request.urlopen", download)
    target = acquire_asset(asset, tmp_path)
    assert target.read_bytes() == content
    assert acquire_asset(asset, tmp_path) == target
    assert len(calls) == 1
    target.write_bytes(b"x" * len(content))
    acquire_asset(asset, tmp_path)
    assert len(calls) == 2
    assert target.read_bytes() == content
    assert not list(tmp_path.glob("*.part"))


def test_failed_download_preserves_existing_file(tmp_path, monkeypatch):
    import hashlib
    import io

    from bla_bla_walk.geometry_assets import acquire_asset

    content = b"expected raster"
    asset = {
        "asset_url": "https://data.geo.admin.ch/synthetic.tif",
        "catalog_checksum": "1220" + hashlib.sha256(content).hexdigest(),
        "header": {"asset_bytes": len(content)},
    }
    target = tmp_path / "synthetic.tif"
    target.write_bytes(b"previous file")

    def download(*args, **kwargs):
        response = io.BytesIO(b"truncated")
        response.status = 200
        return response

    monkeypatch.setattr("urllib.request.urlopen", download)
    with pytest.raises(ValueError, match="checksum mismatch"):
        acquire_asset(asset, tmp_path)
    assert target.read_bytes() == b"previous file"
    assert not list(tmp_path.glob("*.part"))
