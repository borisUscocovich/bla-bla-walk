"""Checksum-verified local acquisition for the pinned geometry inventory."""

import hashlib
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

DOWNLOAD_CHUNK_BYTES = 1024 * 1024
DOWNLOAD_TIMEOUT_SECONDS = 60


def verified_asset(path: Path, expected_bytes: int, sha256: str) -> bool:
    """Check size and full content before resuming from an existing local file."""
    if not path.is_file() or path.stat().st_size != expected_bytes:
        return False
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(DOWNLOAD_CHUNK_BYTES):
            digest.update(chunk)
    return digest.hexdigest() == sha256


def acquire_asset(asset: dict, directory: Path) -> Path:
    """Stream a pinned TIFF atomically, reusing only fully verified files.

    Network, truncation and checksum errors propagate to the batch caller.
    A failed acquisition never replaces a previously stored file.
    """
    url = urlsplit(asset["asset_url"])
    if url.scheme != "https" or url.hostname != "data.geo.admin.ch":
        raise ValueError("Geometry assets require the admitted official HTTPS host")
    name = Path(url.path).name
    if not name.endswith(".tif"):
        raise ValueError("Geometry asset must be a TIFF")
    checksum = asset["catalog_checksum"].lower()
    if len(checksum) != 68 or not checksum.startswith("1220"):
        raise ValueError("Geometry asset requires a SHA256 multihash")
    bytes.fromhex(checksum)
    expected_bytes = asset["header"]["asset_bytes"]
    if not isinstance(expected_bytes, int) or expected_bytes <= 0:
        raise ValueError("Geometry asset requires a positive pinned byte size")
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / name
    if verified_asset(target, expected_bytes, checksum[4:]):
        return target
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=directory, suffix=".part", delete=False
        ) as output:
            temporary = Path(output.name)
            digest = hashlib.sha256()
            received = 0
            request = urllib.request.Request(asset["asset_url"])
            with urllib.request.urlopen(
                request, timeout=DOWNLOAD_TIMEOUT_SECONDS
            ) as response:
                if response.status != 200:
                    raise ValueError(
                        f"Expected full asset response, got {response.status}"
                    )
                while chunk := response.read(DOWNLOAD_CHUNK_BYTES):
                    received += len(chunk)
                    if received > expected_bytes:
                        raise ValueError("Download exceeds pinned asset size")
                    digest.update(chunk)
                    output.write(chunk)
            if received != expected_bytes or digest.hexdigest() != checksum[4:]:
                raise ValueError("Geometry asset size or checksum mismatch")
        temporary.replace(target)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return target
