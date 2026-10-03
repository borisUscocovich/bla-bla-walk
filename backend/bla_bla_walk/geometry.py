"""Validate T0's pinned inventory and plan bounded geometry preparation.

This checkpoint does not download, decode, resample or certify raster coverage.
Preparation states must only advance after subsequent cell and scene validation.
"""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

PRODUCTS = ("surface", "terrain")
FLOAT32_BYTES = 4
MIB = 1024**2
GIB = 1024**3


def _validate_asset(asset: dict, bounds: list, resolution: float) -> int:
    if asset["status"] == "missing_from_catalog":
        return 0
    if asset["status"] != "catalog_available":
        raise ValueError("Unexpected inventory asset status")
    url = urlsplit(asset["asset_url"])
    if url.scheme != "https" or url.hostname != "data.geo.admin.ch":
        raise ValueError("Asset must use the admitted official HTTPS host")
    checksum = asset["catalog_checksum"]
    if len(checksum) != 68 or not checksum.lower().startswith("1220"):
        raise ValueError("Asset must carry a SHA256 multihash")
    try:
        bytes.fromhex(checksum)
    except ValueError as error:
        raise ValueError("Invalid asset checksum") from error
    header = asset["header"]
    size = int((bounds[2] - bounds[0]) / resolution)
    expected = {
        "status": "header_verified",
        "crs_epsg": 2056,
        "shape": [size, size],
        "pixel_scale": [resolution, resolution, 0.0],
        "tiepoint": [0.0, 0.0, 0.0, bounds[0], bounds[3], 0.0],
        "bits_per_sample": [32],
        "nodata": "-9999",
    }
    for name, value in expected.items():
        if header.get(name) != value:
            raise ValueError(f"Unexpected asset {name}: {header.get(name)!r}")
    if "EPSG:5728" not in header["vertical_crs"]:
        raise ValueError("Asset vertical reference is not LN02 / EPSG:5728")
    if not isinstance(header["asset_bytes"], int) or header["asset_bytes"] <= 0:
        raise ValueError("Invalid asset byte size")
    return header["asset_bytes"]


def plan_preparation(inventory: dict, budget: dict) -> dict:
    """Return a deterministic pending/gap ledger after checking all pinned grids.

    The digest identifies the input inventory, not prepared geometry.
    No catalogue/header evidence is promoted to validated cell coverage.
    """
    if (
        inventory["schema_version"] != 1
        or inventory["horizontal_crs"] != "EPSG:2056"
        or not inventory["vertical_reference"].startswith("LN02 / EPSG:5728")
        or inventory["resolution_metres"] != 0.5
        or inventory["boundary"]["crs"] != "EPSG:2056"
    ):
        raise ValueError("Unsupported inventory coordinate system or resolution")
    rows = []
    seen = set()
    totals = dict.fromkeys(PRODUCTS, 0)
    missing = {product: [] for product in PRODUCTS}
    asset_count = receiver_count = paired_count = mismatch_count = 0
    for tile in sorted(inventory["tiles"], key=lambda tile: tile["tile"]):
        name = tile["tile"]
        if name in seen:
            raise ValueError(f"Duplicate tile: {name}")
        seen.add(name)
        east, north = map(int, name.split("-"))
        bounds = [east * 1000, north * 1000, (east + 1) * 1000, (north + 1) * 1000]
        if tile["bounds_epsg2056"] != bounds:
            raise ValueError(f"Tile bounds do not match identifier: {name}")
        if tile["role"] not in ("receiver", "occluder_buffer"):
            raise ValueError(f"Unexpected tile role: {name}")
        receiver_count += tile["role"] == "receiver"
        states = {}
        for product in PRODUCTS:
            byte_size = _validate_asset(tile[product], bounds, 0.5)
            totals[product] += byte_size
            asset_count += bool(byte_size)
            states[product] = "pending" if byte_size else "catalog_gap"
            if not byte_size:
                missing[product].append(name)
                if tile["role"] == "receiver":
                    raise ValueError(f"Receiver asset missing: {name}/{product}")
        paired = all(state == "pending" for state in states.values())
        mismatch = (
            tile["surface"]["nominal_datetime"][:4]
            != tile["terrain"]["nominal_datetime"][:4]
            if paired
            else None
        )
        if tile["survey_year_mismatch"] != mismatch:
            raise ValueError(f"Survey mismatch flag inconsistent: {name}")
        paired_count += paired
        mismatch_count += mismatch is True
        rows.append(
            {
                "tile": name,
                "role": tile["role"],
                "bounds_epsg2056": bounds,
                "assets": states,
                "nominal_year_mismatch": mismatch,
                "cell_validation": "pending",
                "scene_validation": "pending",
            }
        )
    counts = {
        "required_tile_squares": len(rows),
        "receiver_tiles": receiver_count,
        "buffer_only_tiles": len(rows) - receiver_count,
        "paired_tiles": paired_count,
        "paired_nominal_year_mismatches": mismatch_count,
        "available_assets": asset_count,
        "missing_receiver_assets": 0,
        "missing_tiles": missing,
        "compressed_bytes": totals,
    }
    for name, value in counts.items():
        if inventory["summary"].get(name) != value:
            raise ValueError(f"Inventory summary mismatch: {name}")
    decoded_bytes = asset_count * 2000**2 * FLOAT32_BYTES
    planned_disk_bytes = sum(totals.values()) + decoded_bytes
    if planned_disk_bytes > budget["geometry_disk_gib"] * GIB:
        raise ValueError("Raw assets plus native arrays exceed geometry disk budget")
    encoded = json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode()
    return {
        "schema_version": 1,
        "inventory_sha256": hashlib.sha256(encoded).hexdigest(),
        "status": "planned_not_prepared",
        "prepared_tiles": 0,
        "horizontal_crs": inventory["horizontal_crs"],
        "vertical_reference": inventory["vertical_reference"],
        "resolution_metres": inventory["resolution_metres"],
        "nodata": -9999,
        "boundary_release": inventory["boundary"]["release"],
        "buffer_policy": inventory["buffer"],
        "counts": counts,
        "storage_estimate": {
            "compressed_and_native_float32_bytes": planned_disk_bytes,
            "remaining_budget_bytes": budget["geometry_disk_gib"] * GIB
            - planned_disk_bytes,
            "scope": "Excludes metadata, temporary files and derived grids",
        },
        "batch_policy": {
            "max_tiles_in_memory": 1,
            "native_pair_float32_bytes": 2 * 2000**2 * FLOAT32_BYTES,
            "worker_budget_bytes": budget["maximum_worker_peak_mib"] * MIB,
            "order": "Representative scenes, remaining receivers, then buffer assets",
            "resume": "Skip only checksum-verified and cell-validated local outputs",
        },
        "tiles": rows,
    }


def main() -> None:
    """Write a planning ledger; raster preparation is a later checkpoint."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory", type=Path, default=Path("data/tile-inventory.json")
    )
    parser.add_argument(
        "--manifest", type=Path, default=Path("data/source-manifest.json")
    )
    parser.add_argument(
        "--output", type=Path, default=Path(".hack/t8/preparation-plan.json")
    )
    args = parser.parse_args()
    try:
        inventory = json.loads(args.inventory.read_text())
        budget = json.loads(args.manifest.read_text())["acceptance_budget"]
        ledger = plan_preparation(inventory, budget)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_suffix(".tmp")
        temporary.write_text(json.dumps(ledger, indent=2) + "\n")
        temporary.replace(args.output)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Cannot plan geometry preparation: {error}\n")
    print(f"Validated inventory; 0 tiles prepared. Plan: {args.output}")


if __name__ == "__main__":
    main()
