"""Acceptance evidence for prepared native geometry, independent of shade."""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from bla_bla_walk.geometry import GIB, MIB, PIPELINE_VERSION, PRODUCTS, plan_preparation
from bla_bla_walk.geometry_assets import verified_asset
from bla_bla_walk.geometry_prepare import process_peak_bytes, storage_bytes, write_json
from bla_bla_walk.geometry_rasters import pair_evidence, valid_cells


def seam_evidence(first: Path, second: Path, direction: str) -> dict:
    """Measure neighbouring half-metre cell jumps, without flattening real edges.

    Adjacent cell centres differ by 0.5m, not coincident duplicate samples.
    A height jump is retained as evidence; it does not establish a registration
    error or a real cliff on its own. NoData remains an unknown seam segment.
    """
    a = np.load(first, mmap_mode="r", allow_pickle=False)
    b = np.load(second, mmap_mode="r", allow_pickle=False)
    try:
        if direction == "east":
            edge_a, edge_b = a[:, -1], b[:, 0]
        elif direction == "north":
            edge_a, edge_b = a[0, :], b[-1, :]
        else:
            raise ValueError("Unknown seam direction")
        valid = valid_cells(edge_a) & valid_cells(edge_b)
        differences = np.abs(edge_a[valid] - edge_b[valid])
        return {
            "paired_samples": int(valid.sum()),
            "unknown_samples": int((~valid).sum()),
            "absolute_jump_p50_p95_max_m": [
                float(x) for x in np.percentile(differences, [50, 95, 100])
            ]
            if differences.size
            else None,
        }
    finally:
        a._mmap.close()
        b._mmap.close()


def audit_prepared(inventory: dict, manifest: dict, root: Path) -> dict:
    """Reverify complete receiver/buffer coverage and gather reproducible checks."""
    plan = plan_preparation(inventory, manifest["acceptance_budget"])
    ledger = json.loads((root / "manifest.json").read_text())
    if (
        ledger.get("geometry_version")
        != PIPELINE_VERSION + ":" + plan["inventory_sha256"]
    ):
        raise ValueError("Prepared geometry version is stale")
    if set(ledger["tiles"]) != {tile["tile"] for tile in inventory["tiles"]}:
        raise ValueError("Every selected tile must have a prepared/gap record")
    prepared_assets = receiver_pairs = 0
    for tile in inventory["tiles"]:
        record = ledger["tiles"][tile["tile"]]
        if record["status"] not in ("prepared", "documented_catalog_gap"):
            raise ValueError(f"Unresolved tile: {tile['tile']}")
        if (
            record["bounds_epsg2056"] != tile["bounds_epsg2056"]
            or record["nominal_year_mismatch"] != tile["survey_year_mismatch"]
        ):
            raise ValueError("Prepared grid/survey evidence drift")
        for product in PRODUCTS:
            asset = tile[product]
            prepared = record["assets"][product]
            if asset["status"] == "missing_from_catalog":
                if prepared != {"status": "catalog_gap"}:
                    raise ValueError("Catalogue gap was filled without provenance")
                continue
            source = root / "raw" / Path(asset["asset_url"]).name
            array = root / "arrays" / f"{tile['tile']}-{product}.npy"
            if (
                prepared["status"] != "prepared"
                or prepared["source_checksum"] != asset["catalog_checksum"]
                or not verified_asset(
                    source,
                    asset["header"]["asset_bytes"],
                    asset["catalog_checksum"][4:].lower(),
                )
                or not verified_asset(array, prepared["bytes"], prepared["sha256"])
            ):
                raise ValueError(
                    f"Cannot verify prepared asset: {tile['tile']}/{product}"
                )
            if prepared["valid_cells"] + prepared["invalid_cells"] != 2000**2:
                raise ValueError("Incomplete native cell validation")
            prepared_assets += 1
        if record["status"] == "prepared":
            pair = pair_evidence(
                root / "arrays" / f"{tile['tile']}-surface.npy",
                root / "arrays" / f"{tile['tile']}-terrain.npy",
            )
            if pair != record["pair"]:
                raise ValueError("Prepared pair evidence drift")
            receiver_pairs += tile["role"] == "receiver"
    scenes = []
    for scene in manifest["raster_samples"]["samples"]:
        record = ledger["tiles"][scene["tile"]]
        pair = record["pair"]
        if (
            pair["valid_pair_cells"] != scene["valid_pair_cells"]
            or pair["relative_height_range_m"] != scene["relative_height_range_metres"]
            or pair["surface_below_terrain_over_1m_cells"]
            != scene["surface_below_terrain_over_1m_cells"]
        ):
            raise ValueError(f"T0 representative evidence differs: {scene['tile']}")
        scenes.append(
            {
                "environment": scene["environment"],
                "tile": scene["tile"],
                "matches_T0": True,
            }
        )
    seams = []
    for name, record in sorted(ledger["tiles"].items()):
        east, north = map(int, name.split("-"))
        for direction, neighbour in (
            ("east", f"{east + 1}-{north}"),
            ("north", f"{east}-{north + 1}"),
        ):
            if neighbour not in ledger["tiles"]:
                continue
            for product in PRODUCTS:
                a, b = (
                    record["assets"][product],
                    ledger["tiles"][neighbour]["assets"][product],
                )
                evidence = {
                    "tile": name,
                    "neighbour": neighbour,
                    "direction": direction,
                    "product": product,
                }
                if a["status"] == b["status"] == "prepared":
                    evidence.update(
                        seam_evidence(
                            root / "arrays" / f"{name}-{product}.npy",
                            root / "arrays" / f"{neighbour}-{product}.npy",
                            direction,
                        )
                    )
                    evidence["grid_alignment"] = "contiguous_native_half_metre_centres"
                else:
                    evidence["status"] = "unknown_catalog_gap"
                seams.append(evidence)
    heights = [
        r["pair"]["relative_height_range_m"][1]
        for r in ledger["tiles"].values()
        if "pair" in r and r["pair"]["valid_pair_cells"]
    ]
    terrain = [
        r["assets"]["terrain"]
        for r in ledger["tiles"].values()
        if r["assets"]["terrain"]["status"] == "prepared"
        and r["assets"]["terrain"]["valid_cells"]
    ]
    relief = max(a["maximum_m"] for a in terrain) - min(a["minimum_m"] for a in terrain)
    reach = (max(heights) + relief) / math.tan(math.radians(10))
    measured_storage = storage_bytes(root)
    peak = max(process_peak_bytes(), ledger["peak_process_bytes"])
    budget = manifest["acceptance_budget"]
    if (
        measured_storage > budget["geometry_disk_gib"] * GIB
        or peak > budget["maximum_worker_peak_mib"] * MIB
    ):
        raise ValueError("Measured acceptance budget exceeded")
    return {
        "schema_version": 2,
        "status": "prepared_with_explicit_limitations",
        "geometry_version": ledger["geometry_version"],
        "inventory_sha256": plan["inventory_sha256"],
        "horizontal_crs": "EPSG:2056",
        "vertical_reference": "LN02 / EPSG:5728 (product provenance)",
        "resolution_metres": 0.5,
        "nodata": -9999,
        "attribution": "© swisstopo",
        "receiver_tiles_prepared": receiver_pairs,
        "prepared_assets": prepared_assets,
        "counts": plan["counts"],
        "buffer_policy": plan["buffer_policy"],
        "storage_bytes": measured_storage,
        "peak_single_process_bytes": peak,
        "budget_pass": True,
        "representative_scenes": scenes,
        "seams": seams,
        "reach_evidence": {
            "maximum_relative_height_m": max(heights),
            "whole_inventory_terrain_relief_m": relief,
            "conservative_reach_at_10_degrees_m": reach,
            "blanket_1500m_halo_supported": False,
            "policy": (
                "Check actual sunward height/relief/reach and gaps; "
                "unsupported rays stay unknown"
            ),
        },
        "receiver_policy": (
            "Ground eligibility requires valid nonnegative paired geometry; "
            "bridge/canopy/tunnel elevations remain unknown; T10 must mask city "
            "boundary and handle mixed surveys explicitly"
        ),
        "scene_policy": (
            "All 96 pairs have mixed nominal surveys; negative heights and seam "
            "jumps retained, no infill/clamping or shade accuracy claim"
        ),
        "tiles": ledger["tiles"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/geometry"))
    parser.add_argument("--output", type=Path, default=Path(".hack/t8/acceptance.json"))
    args = parser.parse_args()
    try:
        report = audit_prepared(
            json.loads(Path("data/tile-inventory.json").read_text()),
            json.loads(Path("data/source-manifest.json").read_text()),
            args.root,
        )
        write_json(args.output, report)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Geometry acceptance failed: {error}\n")
    print(
        f"Accepted {report['receiver_tiles_prepared']} receiver pairs and "
        f"{report['prepared_assets']} assets; {args.output}"
    )


if __name__ == "__main__":
    main()
