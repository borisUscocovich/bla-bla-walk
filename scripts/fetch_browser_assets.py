"""Fetch pinned standalone browser assets; no JavaScript package manager."""

import hashlib
import io
import json
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / ".cache/browser-assets"


def fetch_assets() -> None:
    """Reuse matching local bytes, otherwise download and verify before writing."""
    manifest = json.loads((ROOT / "config/browser-assets.json").read_text())
    downloads = {}
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for asset in manifest["assets"]:
        target = ASSET_DIR / asset["file"]
        if target.exists():
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if digest == asset["sha256"]:
                continue
        url = asset["url"]
        if url not in downloads:
            with urllib.request.urlopen(url, timeout=40) as response:
                downloads[url] = response.read()
        data = downloads[url]
        if "archive_path" in asset:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                data = archive.read(asset["archive_path"])
        if hashlib.sha256(data).hexdigest() != asset["sha256"]:
            raise ValueError(f"Asset checksum mismatch: {asset['file']}")
        target.write_bytes(data)
    print("Pinned browser assets ready.")


if __name__ == "__main__":
    try:
        fetch_assets()
    except (OSError, ValueError, urllib.error.URLError, zipfile.BadZipFile) as error:
        sys.exit(f"Browser asset setup failed: {error}")
