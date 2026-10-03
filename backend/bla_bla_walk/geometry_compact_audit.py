"""T8 acceptance for configured compact geometry, retaining native references."""

import argparse
import json
from pathlib import Path

import numpy as np
import rasterio

from bla_bla_walk.geometry import geometry_settings, read_heights, sha256_file
from bla_bla_walk.geometry_inventory import GIB, MIB
from bla_bla_walk.geometry_prepare import process_peak_bytes, storage_bytes, write_json
from bla_bla_walk.geometry_rasters import GDAL_CACHE_BYTES, valid_cells


def scaled_pair(surface, terrain):
    """Mixed-survey values and negative differences are evidence, never clamped."""
    valid = valid_cells(surface) & valid_cells(terrain)
    relative = (surface - terrain)[valid]
    return {
        "valid_pair_cells": int(valid.sum()),
        "invalid_pair_cells": int((~valid).sum()),
        "relative_height_range_m": [float(relative.min()), float(relative.max())]
        if relative.size
        else [None, None],
        "negative_relative_height_cells": int((relative < 0).sum()),
    }


def scaled_seam(a, b, direction):
    """Compare touching north-first compact edges without smoothing or infill."""
    first, second = (a[:, -1], b[:, 0]) if direction == "east" else (a[0, :], b[-1, :])
    valid = valid_cells(first) & valid_cells(second)
    jumps = np.abs(first[valid] - second[valid])
    return {
        "paired_samples": int(valid.sum()),
        "unknown_samples": int((~valid).sum()),
        "absolute_jump_p50_p95_max_m": [
            float(x) for x in np.percentile(jumps, [50, 95, 100])
        ]
        if jumps.size
        else None,
    }


def audit_compact(root: Path, native: Path) -> dict:
    """Verify all local compact hashes, scaled grids, native aggregation and seams."""
    inventory_path = Path("data/tile-inventory.json")
    inventory = json.loads(inventory_path.read_text())
    settings = geometry_settings()
    ledger = json.loads((root / "manifest.json").read_text())
    if (
        not ledger.get("complete_available_inventory")
        or ledger.get("errors")
        or ledger["settings"] != settings
        or ledger["inventory_sha256"] != sha256_file(inventory_path)
    ):
        raise ValueError("Compact inventory/settings/preparation incomplete or stale")
    expected = {
        f"{t['tile']}-{p}"
        for t in inventory["tiles"]
        for p in ("surface", "terrain")
        if t[p]["status"] == "catalog_available"
    }
    if set(ledger["assets"]) != expected:
        raise ValueError("Compact assets differ from full selected inventory")
    expected_gaps = {
        (t["tile"], p)
        for t in inventory["tiles"]
        for p in ("surface", "terrain")
        if t[p]["status"] == "missing_from_catalog"
    }
    if {(g["tile"], g["kind"]) for g in ledger["gaps"]} != expected_gaps:
        raise ValueError("Compact catalogue gaps changed")
    tiles, seams, unknown = {}, [], 0
    with rasterio.Env(GDAL_CACHEMAX=GDAL_CACHE_BYTES):
        for tile in inventory["tiles"]:
            name = tile["tile"]
            arrays = {}
            record = {
                "role": tile["role"],
                "nominal_year_mismatch": tile["survey_year_mismatch"],
                "assets": {},
            }
            for product in ("surface", "terrain"):
                key = f"{name}-{product}"
                if key not in expected:
                    record["assets"][product] = {"status": "catalog_gap"}
                    continue
                asset = ledger["assets"][key]
                path = root / f"{key}.tif"
                source_url = tile[product]["asset_url"]
                if product == "terrain":
                    source_url = source_url.replace("_0.5_2056_", "_2_2056_")
                if (
                    asset["source"]["url"] != source_url
                    or asset["preparation_version"] != ledger["preparation_version"]
                    or sha256_file(path) != asset["sha256"]
                ):
                    raise ValueError(f"Compact source/version/checksum drift: {key}")
                with rasterio.open(path) as src:
                    if (
                        src.shape != (1000, 1000)
                        or src.res != (1, 1)
                        or src.scales != (2,)
                        or src.offsets != (0,)
                        or src.nodata != -32768
                        or src.dtypes != ("int16",)
                        or src.crs.to_epsg() != 2056
                        or list(src.bounds) != tile["bounds_epsg2056"]
                        or src.tags()["vertical_reference"]
                        != settings["vertical_reference"]
                    ):
                        raise ValueError(f"Compact grid/vertical/scale drift: {key}")
                values = read_heights(path).filled(-9999)
                invalid = int((~valid_cells(values)).sum())
                if invalid != asset["unknown_cells"]:
                    raise ValueError(f"Compact mask drift: {key}")
                unknown += invalid
                arrays[product] = values
                stats = {
                    "status": "prepared",
                    "unknown_cells": invalid,
                    "bytes": asset["bytes"],
                    "sha256": asset["sha256"],
                    "source": asset["source"],
                    "source_resolution_m": asset["source_cell_size_metres"],
                    "minimum_m": float(values[valid_cells(values)].min()),
                    "maximum_m": float(values[valid_cells(values)].max()),
                }
                if product == "surface":
                    mapped = np.load(
                        native / "arrays" / f"{name}-surface.npy",
                        mmap_mode="r",
                        allow_pickle=False,
                    )
                    try:
                        blocks = mapped.reshape(1000, 2, 1000, 2)
                        native_valid = valid_cells(blocks).all(axis=(1, 3))
                        if not np.array_equal(native_valid, valid_cells(values)):
                            raise ValueError(
                                "Compact surface aggregation changed missingness"
                            )
                        maximum = blocks.max(axis=(1, 3))
                        error = float(
                            np.abs(values[native_valid] - maximum[native_valid]).max()
                        )
                        if error > settings["height_step_metres"] / 2:
                            raise ValueError(
                                "Compact surface error exceeds half a height step"
                            )
                        stats["max_error_from_native_block_max_m"] = error
                    finally:
                        mapped._mmap.close()
                record["assets"][product] = stats
                if product == "terrain":
                    coarse = values[::2, ::2]
                    if not (
                        np.array_equal(coarse, values[1::2, ::2])
                        and np.array_equal(coarse, values[::2, 1::2])
                        and np.array_equal(coarse, values[1::2, 1::2])
                    ):
                        raise ValueError("Compact terrain invented sub-2m detail")
                    stats["native_2m_nearest_repetition_verified"] = True
            if len(arrays) == 2:
                record["pair"] = scaled_pair(arrays["surface"], arrays["terrain"])
                record["status"] = "prepared"
            else:
                record["status"] = "documented_catalog_gap"
            tiles[name] = record
        for name, record in sorted(tiles.items()):
            east, north = map(int, name.split("-"))
            for direction, neighbour in (
                ("east", f"{east + 1}-{north}"),
                ("north", f"{east}-{north + 1}"),
            ):
                if neighbour not in tiles:
                    continue
                for product in ("surface", "terrain"):
                    seam = {
                        "tile": name,
                        "neighbour": neighbour,
                        "product": product,
                        "direction": direction,
                    }
                    if (
                        record["assets"][product]["status"]
                        == tiles[neighbour]["assets"][product]["status"]
                        == "prepared"
                    ):
                        seam.update(
                            scaled_seam(
                                read_heights(root / f"{name}-{product}.tif").filled(
                                    -9999
                                ),
                                read_heights(
                                    root / f"{neighbour}-{product}.tif"
                                ).filled(-9999),
                                direction,
                            )
                        )
                        seam["grid_alignment"] = "contiguous_1m_centres"
                    else:
                        seam["status"] = "unknown_catalog_gap"
                    seams.append(seam)
    budget = json.loads(Path("data/source-manifest.json").read_text())[
        "acceptance_budget"
    ]
    peak, disk = process_peak_bytes(), storage_bytes(root)
    if (
        peak > budget["maximum_worker_peak_mib"] * MIB
        or disk > budget["geometry_disk_gib"] * GIB
    ):
        raise ValueError("Compact audit plus native reference exceeds geometry budget")
    receivers = sum(
        r["role"] == "receiver" and r["status"] == "prepared" for r in tiles.values()
    )
    if receivers != inventory["summary"]["receiver_tiles"]:
        raise ValueError("Compact receiver pair coverage incomplete")
    return {
        "schema_version": 1,
        "status": "compact_prepared_with_explicit_limitations",
        "settings": settings,
        "geometry_version": ledger["preparation_version"],
        "receiver_tiles_prepared": receivers,
        "prepared_assets": len(expected),
        "unknown_source_cells": unknown,
        "gaps": ledger["gaps"],
        "prepared_bytes": ledger["prepared_bytes"],
        "combined_storage_bytes": disk,
        "peak_process_bytes": peak,
        "budget_pass": True,
        "tiles": tiles,
        "seams": seams,
        "accuracy_scope": (
            "Native surface max aggregation verified within 1m height rounding; "
            "native 2m terrain nearest repetition adds no detail. Independent "
            "scene/sun/shade accuracy remains unknown"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/geometry"))
    parser.add_argument(
        "--native", type=Path, default=Path("data/geometry/native-reference")
    )
    args = parser.parse_args()
    try:
        report = audit_compact(args.root, args.native)
        write_json(Path(".hack/t8/compact-acceptance.json"), report)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Compact T8 acceptance failed: {error}\n")
    print(
        f"Verified {report['prepared_assets']} compact assets, "
        f"{report['receiver_tiles_prepared']} receiver pairs; "
        f"{report['prepared_bytes']} raster bytes"
    )


if __name__ == "__main__":
    main()
