"""Save a finite licensed Basel basemap for use without internet."""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime

import httpx
from prepare_geometry import ROOT, sha256_file, write_json

sys.path.insert(0, str(ROOT / "backend"))
from bla_bla_walk.basemap import (  # noqa: E402
    TILE_DIRECTORY,
    basemap_settings,
    tile_ranges,
)
from bla_bla_walk.snapshots import save_provider_snapshot  # noqa: E402

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_TILE_BYTES = 2_000_000


def save_tile(config, zoom, x, y, previous, client):
    """Reuse verified images; reject errors disguised as tiles and bound responses."""
    key = f"{zoom}/{x}/{y}.png"
    target = TILE_DIRECTORY / key
    old = previous.get(key)
    if old and target.exists() and sha256_file(target) == old["sha256"]:
        return key, old
    url = config["url"].format(z=zoom, x=x, y=y)
    for attempt in range(3):
        try:
            with client.stream("GET", url) as response:
                response.raise_for_status()
                data = bytearray()
                for block in response.iter_bytes():
                    data.extend(block)
                    if len(data) > MAX_TILE_BYTES:
                        raise ValueError("Basemap tile exceeds response limit")
            if not data.startswith(PNG_SIGNATURE) or data[12:16] != b"IHDR":
                raise ValueError("Basemap response is not a PNG")
            if int.from_bytes(data[16:20], "big") != 256 or (
                int.from_bytes(data[20:24], "big") != 256
            ):
                raise ValueError("Basemap tile has unexpected dimensions")
            target.parent.mkdir(parents=True, exist_ok=True)
            partial = target.with_suffix(".tmp")
            partial.write_bytes(data)
            partial.replace(target)
            return key, {
                "bytes": len(data),
                "sha256": sha256_file(target),
                "retrieved_at": datetime.now(UTC).isoformat(),
            }
        except (httpx.HTTPError, OSError, ValueError):
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def prepare_offline(workers=4):
    """Download every configured zoom/coverage tile with resumable checkpoints."""
    config = basemap_settings()
    path = TILE_DIRECTORY / "manifest.json"
    previous = json.loads(path.read_text()) if path.exists() else {}
    images = previous.get("tiles", {}) if previous.get("config") == config else {}
    jobs = [
        (z, x, y)
        for z in range(config["min_zoom"], config["max_zoom"] + 1)
        for columns, rows in [tile_ranges(config["bounds_wgs84"], z)]
        for x in columns
        for y in rows
    ]
    manifest = {
        "config": config,
        "tiles": images,
        "errors": [],
        "expected_tiles": len(jobs),
        "complete": False,
        "downloaded_at": previous.get("downloaded_at"),
    }
    with (
        httpx.Client(timeout=30, follow_redirects=True) as client,
        ThreadPoolExecutor(max_workers=workers) as executor,
    ):
        futures = [
            executor.submit(save_tile, config, *job, images, client) for job in jobs
        ]
        for index, future in enumerate(as_completed(futures), 1):
            try:
                key, record = future.result()
                images[key] = record
                if record.get("retrieved_at"):
                    manifest["downloaded_at"] = max(
                        manifest["downloaded_at"] or "", record["retrieved_at"]
                    )
            except (httpx.HTTPError, OSError, ValueError) as error:
                manifest["errors"].append(str(error))
            if index % 50 == 0 or index == len(jobs):
                manifest["verified_at"] = datetime.now(UTC).isoformat()
                write_json(path, manifest)
                print(
                    f"Basemap {index}/{len(jobs)}; errors {len(manifest['errors'])}",
                    flush=True,
                )
    manifest["complete"] = len(images) == len(jobs) and not manifest["errors"]
    manifest["bytes"] = sum(image["bytes"] for image in images.values())
    write_json(path, manifest)
    print(json.dumps({k: manifest[k] for k in ("complete", "bytes", "errors")}))
    return manifest["complete"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, choices=range(1, 5), default=4)
    args = parser.parse_args()
    try:
        snapshot = save_provider_snapshot()
        print(
            f"Provider snapshot saved: {snapshot.generated_at.isoformat()}", flush=True
        )
    except (OSError, ValueError) as error:
        sys.exit(f"Offline provider snapshot preparation failed: {error}")
    raise SystemExit(0 if prepare_offline(args.workers) else 1)
