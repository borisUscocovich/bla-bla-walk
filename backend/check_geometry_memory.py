"""Measure two independent native-window consumers against T0 worker budgets."""

import concurrent.futures
import json
import multiprocessing
from pathlib import Path

from bla_bla_walk.geometry import MIB
from bla_bla_walk.geometry_prepare import process_peak_bytes, write_json
from bla_bla_walk.geometry_store import GeometryStore


def read_scenes(root: str, digest: str, tiles: list[str]) -> int:
    """Stream full native scene tiles; no full-city or halo allocation."""
    store = GeometryStore(Path(root), digest)
    for _ in range(3):
        for tile in tiles:
            window = store.read_window(tile)
            assert window.surface.shape == (2000, 2000)
            assert window.terrain_valid.any()
            del window
    return process_peak_bytes()


def main():
    manifest = json.loads(Path("data/source-manifest.json").read_text())
    budget = manifest["acceptance_budget"]
    root = Path("data/geometry")
    ledger = json.loads((root / "manifest.json").read_text())
    tiles = [scene["tile"] for scene in manifest["raster_samples"]["samples"]]
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=2, mp_context=multiprocessing.get_context("spawn")
    ) as pool:
        futures = [
            pool.submit(read_scenes, str(root), ledger["inventory_sha256"], tiles)
            for _ in range(2)
        ]
        peaks = [future.result() for future in futures]
    assert max(peaks) <= budget["maximum_worker_peak_mib"] * MIB
    assert sum(peaks) <= budget["total_worker_peak_mib"] * MIB
    evidence = {
        "method": (
            "Two independent spawned Python workers, each streaming four full "
            "native pairs three times; Linux VmHWM"
        ),
        "worker_peaks_bytes": peaks,
        "sum_independent_peaks_bytes": sum(peaks),
        "budget_pass": True,
        "scope": "Native geometry access only; T10 halo/shade/API memory not measured",
    }
    write_json(Path(".hack/t8/memory-check.json"), evidence)
    print(json.dumps(evidence))


if __name__ == "__main__":
    main()
