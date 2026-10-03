"""Resumable sequential preparation of T0's pinned receiver and buffer tiles."""

import argparse
import fcntl
import json
import resource
import shutil
import sys
import tempfile
from pathlib import Path

from rasterio.errors import RasterioError

from bla_bla_walk.geometry import GIB, MIB, PIPELINE_VERSION, PRODUCTS, plan_preparation
from bla_bla_walk.geometry_assets import acquire_asset, verified_asset
from bla_bla_walk.geometry_rasters import decode_native, pair_evidence


def process_peak_bytes() -> int:
    """Measure this executable's high-water RSS, excluding pre-exec launcher peaks.

    Linux getrusage can retain a launcher high-water mark across exec; /proc
    VmHWM describes the current process image. Other systems use getrusage.
    """
    if sys.platform == "linux":
        status = Path("/proc/self/status").read_text()
        return int(status.split("VmHWM:", 1)[1].split()[0]) * 1024
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return peak if sys.platform == "darwin" else peak * 1024


def write_json(path: Path, value: dict) -> None:
    """Atomically replace a ledger only after the complete JSON is written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=path.parent, suffix=".part", delete=False
        ) as out:
            temporary = Path(out.name)
            json.dump(value, out, indent=2, allow_nan=False)
            out.write("\n")
        temporary.replace(path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def storage_bytes(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def prepare_batch(
    inventory: dict, manifest: dict, root: Path, batch: str, limit: int | None = None
) -> dict:
    """Acquire/decode one product at a time and checkpoint each validated tile.

    A single writer lock prevents overlapping preparation. Local corruption,
    changed inventory or decoder versions invalidate resume. Failures retain
    previous files but mark this tile unavailable; successful neighbours survive.
    """
    plan = plan_preparation(inventory, manifest["acceptance_budget"])
    root.mkdir(parents=True, exist_ok=True)
    with (root / "preparation.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return _prepare_locked(inventory, manifest, root, batch, limit, plan)


def _prepare_locked(inventory, manifest, root, batch, limit, plan):
    path = root / "manifest.json"
    version = PIPELINE_VERSION + ":" + plan["inventory_sha256"]
    ledger = json.loads(path.read_text()) if path.exists() else {}
    if ledger.get("geometry_version") != version:
        ledger = {
            "schema_version": 2,
            "geometry_version": version,
            "inventory_sha256": plan["inventory_sha256"],
            "tiles": {},
        }
    budget = manifest["acceptance_budget"]
    # All native arrays, raw files, plus one atomic replacement and metadata margin.
    required = (
        plan["storage_estimate"]["compressed_and_native_float32_bytes"] + 128 * MIB
    )
    if required > budget["geometry_disk_gib"] * GIB:
        raise ValueError("Preparation plus temporary reserve exceeds disk budget")
    if shutil.disk_usage(root).free < required - min(required, storage_bytes(root)):
        raise ValueError("Insufficient local free space for preparation")
    scenes = [scene["tile"] for scene in manifest["raster_samples"]["samples"]]
    selected = [
        tile
        for tile in inventory["tiles"]
        if batch == "all"
        or (batch == "scenes" and tile["tile"] in scenes)
        or (batch == "receivers" and tile["role"] == "receiver")
        or (batch == "buffer" and tile["role"] == "occluder_buffer")
    ]
    selected.sort(key=lambda tile: (tile["tile"] not in scenes, tile["tile"]))
    if limit is not None:
        selected = selected[:limit]
    for tile in selected:
        name = tile["tile"]
        record = {
            "role": tile["role"],
            "bounds_epsg2056": tile["bounds_epsg2056"],
            "nominal_year_mismatch": tile["survey_year_mismatch"],
            "assets": {},
        }
        previous = ledger["tiles"].get(name, {})
        try:
            for product in PRODUCTS:
                asset = tile[product]
                if asset["status"] == "missing_from_catalog":
                    record["assets"][product] = {"status": "catalog_gap"}
                    continue
                source = acquire_asset(asset, root / "raw")
                target = root / "arrays" / f"{name}-{product}.npy"
                old = previous.get("assets", {}).get(product, {})
                if (
                    old.get("status") == "prepared"
                    and old.get("source_checksum") == asset["catalog_checksum"]
                    and verified_asset(target, old["bytes"], old["sha256"])
                ):
                    prepared = old
                else:
                    prepared = {
                        **decode_native(source, target, tile["bounds_epsg2056"]),
                        "status": "prepared",
                        "source_checksum": asset["catalog_checksum"],
                        "path": str(target.relative_to(root)),
                        "nominal_datetime": asset["nominal_datetime"],
                    }
                record["assets"][product] = prepared
            if all(record["assets"][p]["status"] == "prepared" for p in PRODUCTS):
                record["pair"] = pair_evidence(
                    root / "arrays" / f"{name}-surface.npy",
                    root / "arrays" / f"{name}-terrain.npy",
                )
            record["status"] = (
                "prepared"
                if all(record["assets"][p]["status"] == "prepared" for p in PRODUCTS)
                else "documented_catalog_gap"
            )
        except (OSError, ValueError, RasterioError) as error:
            record["status"] = "preparation_failed"
            record["error"] = str(error)
        ledger["tiles"][name] = record
        ledger["storage_bytes"] = storage_bytes(root)
        ledger["peak_process_bytes"] = process_peak_bytes()
        ledger["getrusage_peak_raw"] = resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss
        ledger["memory_measurement"] = (
            "VmHWM KiB converted to bytes"
            if sys.platform == "linux"
            else "getrusage platform units converted to bytes"
        )
        ledger["budget_pass"] = (
            ledger["storage_bytes"] <= budget["geometry_disk_gib"] * GIB
            and ledger["peak_process_bytes"] <= budget["maximum_worker_peak_mib"] * MIB
        )
        write_json(path, ledger)
        print(
            f"{name}: {record['status']}; {ledger['storage_bytes']} disk bytes; "
            f"{ledger['peak_process_bytes']} peak bytes",
            flush=True,
        )
        if not ledger["budget_pass"]:
            raise ValueError("Measured storage or memory exceeds geometry budget")
    return ledger


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory", type=Path, default=Path("data/tile-inventory.json")
    )
    parser.add_argument(
        "--manifest", type=Path, default=Path("data/source-manifest.json")
    )
    parser.add_argument("--root", type=Path, default=Path("data/geometry"))
    parser.add_argument(
        "--batch", choices=("scenes", "receivers", "buffer", "all"), default="scenes"
    )
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be positive")
    try:
        ledger = prepare_batch(
            json.loads(args.inventory.read_text()),
            json.loads(args.manifest.read_text()),
            args.root,
            args.batch,
            args.limit,
        )
        if any(
            row["status"] == "preparation_failed" for row in ledger["tiles"].values()
        ):
            parser.exit(
                1,
                "One or more tiles failed; see local manifest and resume this batch.\n",
            )
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Cannot prepare geometry: {error}\n")


if __name__ == "__main__":
    main()
