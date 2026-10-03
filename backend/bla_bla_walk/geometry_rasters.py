"""Bounded native decoding; invalid samples never become plausible elevations."""

import hashlib
import tempfile
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.windows import Window

STRIPE_ROWS = 128
NODATA = -9999.0
GDAL_CACHE_BYTES = 32 * 1024**2


def file_digest(path: Path) -> str:
    """Hash outputs without loading them into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def valid_cells(values):
    """Nonfinite and source NoData are unknown, including in seam comparisons."""
    return np.isfinite(values) & (values != NODATA)


def decode_native(source: Path, target: Path, bounds: list) -> dict:
    """Validate the actual grid and atomically write native float32 NPY stripes.

    Masks are represented by -9999 in the prepared array; masked values and
    nonfinite input are counted separately. No resampling or height clamping.
    Vertical reference comes from pinned product provenance, not a TIFF claim.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    stats = {
        "valid_cells": 0,
        "invalid_cells": 0,
        "nonfinite_cells": 0,
        "minimum_m": None,
        "maximum_m": None,
    }
    try:
        with rasterio.Env(GDAL_CACHEMAX=GDAL_CACHE_BYTES), rasterio.open(source) as src:
            size = int((bounds[2] - bounds[0]) / 0.5)
            if (
                src.crs != rasterio.crs.CRS.from_epsg(2056)
                or src.transform != from_origin(bounds[0], bounds[3], 0.5, 0.5)
                or src.shape != (size, size)
                or src.count != 1
                or src.dtypes != ("float32",)
                or src.nodata != NODATA
            ):
                raise ValueError(
                    "Decoded raster grid/CRS/type/NoData differs from inventory"
                )
            with tempfile.NamedTemporaryFile(
                dir=target.parent, suffix=".part", delete=False
            ) as out:
                temporary = Path(out.name)
                np.lib.format.write_array_header_2_0(
                    out, {"descr": "<f4", "fortran_order": False, "shape": src.shape}
                )
                for row in range(0, size, STRIPE_ROWS):
                    window = Window(0, row, size, min(STRIPE_ROWS, size - row))
                    values = src.read(1, window=window)
                    finite = np.isfinite(values)
                    valid = (
                        finite
                        & (values != NODATA)
                        & (src.read_masks(1, window=window) != 0)
                    )
                    stats["nonfinite_cells"] += int((~finite).sum())
                    stats["valid_cells"] += int(valid.sum())
                    stats["invalid_cells"] += int((~valid).sum())
                    if valid.any():
                        low, high = (
                            float(values[valid].min()),
                            float(values[valid].max()),
                        )
                        stats["minimum_m"] = (
                            low
                            if stats["minimum_m"] is None
                            else min(low, stats["minimum_m"])
                        )
                        stats["maximum_m"] = (
                            high
                            if stats["maximum_m"] is None
                            else max(high, stats["maximum_m"])
                        )
                    values[~valid] = NODATA
                    out.write(values.astype("<f4", copy=False).tobytes())
            temporary.replace(target)
            temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return {**stats, "bytes": target.stat().st_size, "sha256": file_digest(target)}


def pair_evidence(surface_path: Path, terrain_path: Path) -> dict:
    """Preserve survey inconsistency and native height/terrain relief evidence."""
    surface = np.load(surface_path, mmap_mode="r", allow_pickle=False)
    terrain = np.load(terrain_path, mmap_mode="r", allow_pickle=False)
    try:
        if surface.shape != terrain.shape:
            raise ValueError("Prepared pair shapes differ")
        count = negative = 0
        low = high = None
        for row in range(0, surface.shape[0], STRIPE_ROWS):
            s, t = surface[row : row + STRIPE_ROWS], terrain[row : row + STRIPE_ROWS]
            valid = valid_cells(s) & valid_cells(t)
            differences = (s - t)[valid]
            count += differences.size
            negative += int((differences < -1).sum())
            if differences.size:
                minimum, maximum = float(differences.min()), float(differences.max())
                low = minimum if low is None else min(low, minimum)
                high = maximum if high is None else max(high, maximum)
        return {
            "valid_pair_cells": count,
            "invalid_pair_cells": surface.size - count,
            "relative_height_range_m": [low, high],
            "surface_below_terrain_over_1m_cells": negative,
            "scene_consistency": "unknown_mixed_surveys",
        }
    finally:
        surface._mmap.close()
        terrain._mmap.close()
