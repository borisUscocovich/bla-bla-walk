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


def test_metadata_fixture_matches_pinned_inventory(inputs):
    fixture = json.loads((ROOT / "data/fixtures/geometry-metadata.json").read_text())
    assert fixture == plan_preparation(*inputs)
