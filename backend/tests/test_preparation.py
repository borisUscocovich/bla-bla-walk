"""Interrupted/corrupt downloads must not be accepted as prepared source data."""

import hashlib
import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from prepare_geometry import (  # noqa: E402
    checksum_digest,
    download_verified,
    write_json,
)


def asset_for(data):
    return {
        "url": "https://example.com/source.tif",
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def test_interrupted_download_resumes_at_exact_offset(tmp_path):
    data = b"verified raster payload"
    path = tmp_path / "source.part"
    path.write_bytes(data[:8])

    def respond(request):
        assert request.headers["range"] == "bytes=8-"
        return httpx.Response(
            206,
            content=data[8:],
            headers={"Content-Range": f"bytes 8-{len(data) - 1}/{len(data)}"},
        )

    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        download_verified(asset_for(data), path, client)
    assert path.read_bytes() == data


def test_provider_ignoring_range_replaces_partial_instead_of_appending(tmp_path):
    data = b"complete raster payload"
    path = tmp_path / "source.part"
    path.write_bytes(data[:5])
    with httpx.Client(
        transport=httpx.MockTransport(lambda _: httpx.Response(200, content=data))
    ) as client:
        download_verified(asset_for(data), path, client)
    assert path.read_bytes() == data


def test_corruption_is_rejected_and_failed_temporary_file_removed(tmp_path):
    data = b"expected bytes"
    path = tmp_path / "source.part"
    with httpx.Client(
        transport=httpx.MockTransport(
            lambda _: httpx.Response(200, content=b"corrupt! bytes")
        )
    ) as client:
        with pytest.raises(ValueError, match="checksum"):
            download_verified(asset_for(data), path, client)
    assert not path.exists()


def test_incorrect_resume_offset_is_rejected_before_appending(tmp_path):
    data = b"source bytes"
    path = tmp_path / "source.part"
    path.write_bytes(data[:3])
    with httpx.Client(
        transport=httpx.MockTransport(
            lambda _: httpx.Response(
                206, content=data, headers={"Content-Range": "bytes 0-11/12"}
            )
        )
    ) as client:
        with pytest.raises(ValueError, match="Content-Range"):
            download_verified(asset_for(data), path, client)
    assert path.read_bytes() == data[:3]


def test_missing_or_other_checksum_algorithms_rejected():
    for value in (None, "abcd", "1320" + "0" * 64):
        with pytest.raises(ValueError, match="SHA-256"):
            checksum_digest(value)


def test_manifest_checkpoint_survives_transient_windows_file_lock(
    tmp_path, monkeypatch
):
    original = Path.replace
    calls = []

    def temporarily_locked(path, target):
        calls.append(path)
        if len(calls) < 3:
            raise PermissionError("Temporary file lock")
        return original(path, target)

    monkeypatch.setattr(Path, "replace", temporarily_locked)
    path = tmp_path / "manifest.json"
    write_json(path, {"complete": True})
    assert path.read_text() == '{\n  "complete": true\n}\n'
    assert len(calls) == 3


def test_native_reference_reuse_verifies_and_preserves_borrowed_source(
    tmp_path, monkeypatch
):
    import prepare_geometry

    data = b"synthetic borrowed source"
    reference = tmp_path / "reference"
    (reference / "raw").mkdir(parents=True)
    cached = reference / "raw/source.tif"
    cached.write_bytes(data)
    asset = {**asset_for(data), "item_id": "synthetic"}
    directory = tmp_path / "outputs"
    tile = {"tile": "2610-1266", "role": "receiver", "survey_year_mismatch": True}
    monkeypatch.setattr(prepare_geometry, "resolve_asset", lambda *_: asset)

    def no_download(*_):
        raise AssertionError("Verified native source must not redownload")

    monkeypatch.setattr(prepare_geometry, "download_verified", no_download)
    monkeypatch.setattr(
        prepare_geometry,
        "prepare_raster",
        lambda source, *_: {"used_source": str(source)},
    )
    _, record = prepare_geometry.prepare_one(
        tile, "surface", directory, {}, "v1", reference
    )
    assert record["used_source"] == str(cached)
    assert cached.read_bytes() == data
