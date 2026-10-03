"""Bounded native windows and conservative support checks for T10 consumers."""

import json
import math
from pathlib import Path
from typing import Literal

import numpy as np
from rasterio.windows import Window

from bla_bla_walk.geometry import geometry_settings, read_heights
from bla_bla_walk.geometry_assets import verified_asset
from bla_bla_walk.geometry_inventory import PIPELINE_VERSION
from bla_bla_walk.geometry_rasters import NODATA, valid_cells
from bla_bla_walk.interfaces import GeometryWindow


def halo_supported(
    height_m: float,
    relief_m: float,
    elevation_degrees: float,
    available_distance_m: float,
    *,
    missing_geometry: bool,
) -> bool:
    """The T0 250m/10° envelope never authorises missing or insufficient rays."""
    if (
        missing_geometry
        or not all(
            math.isfinite(value)
            for value in (height_m, relief_m, elevation_degrees, available_distance_m)
        )
        or not 10 <= elevation_degrees <= 90
        or not 0 <= height_m <= 250
        or relief_m < 0
        or available_distance_m < 0
    ):
        return False
    reach = (height_m + relief_m) / math.tan(math.radians(elevation_degrees))
    return reach <= available_distance_m


class GeometryStore:
    """Consume a version-matched ledger, verifying each asset before copying it.

    Each call reads at most one native 1km tile (two 16MB arrays plus masks).
    Callers must stream halo tiles rather than building a full native halo.
    """

    def __init__(self, root: Path, inventory_sha256: str):
        self.root = root
        self.ledger = json.loads((root / "manifest.json").read_text())
        expected = PIPELINE_VERSION + ":" + inventory_sha256
        if (
            self.ledger.get("schema_version") != 2
            or self.ledger.get("geometry_version") != expected
        ):
            raise ValueError(
                "Geometry version does not match expected inventory/pipeline"
            )
        self.version = expected

    def read_window(
        self,
        tile: str,
        rows: tuple[int, int] = (0, 2000),
        columns: tuple[int, int] = (0, 2000),
        *,
        receiver_kind: Literal["ground", "bridge", "canopy", "tunnel"] = "ground",
    ) -> GeometryWindow:
        """Copy elevations/masks; unsupported receiver kinds never use bare terrain."""
        if receiver_kind not in ("ground", "bridge", "canopy", "tunnel"):
            raise ValueError("Unknown receiver kind")
        if not all(0 <= start < stop <= 2000 for start, stop in (rows, columns)):
            raise ValueError("Window must lie inside one native tile")
        east, north = map(int, tile.split("-"))
        if tile != f"{east}-{north}":
            raise ValueError("Invalid tile identifier")
        record = self.ledger["tiles"].get(tile, {})
        arrays = {}
        for product in ("surface", "terrain"):
            asset = record.get("assets", {}).get(product, {})
            path = self.root / "arrays" / f"{tile}-{product}.npy"
            if asset.get("status") != "prepared":
                values = np.full(
                    (rows[1] - rows[0], columns[1] - columns[0]),
                    NODATA,
                    dtype="float32",
                )
            else:
                if not verified_asset(path, asset["bytes"], asset["sha256"]):
                    raise ValueError(
                        "Prepared geometry checksum failed; resume preparation"
                    )
                mapped = np.load(path, mmap_mode="r", allow_pickle=False)
                try:
                    if mapped.shape != (2000, 2000) or mapped.dtype != np.dtype("<f4"):
                        raise ValueError(
                            "Prepared geometry array differs from native grid"
                        )
                    values = mapped[rows[0] : rows[1], columns[0] : columns[1]].copy()
                finally:
                    mapped._mmap.close()
            arrays[product] = values
        surface_valid, terrain_valid = (
            valid_cells(arrays[p]) for p in ("surface", "terrain")
        )
        receiver_valid = (
            surface_valid & terrain_valid & (arrays["surface"] >= arrays["terrain"])
        )
        if receiver_kind != "ground" or record.get("status") == "preparation_failed":
            receiver_valid[:] = False
        bounds = (
            east * 1000 + columns[0] * 0.5,
            (north + 1) * 1000 - rows[1] * 0.5,
            east * 1000 + columns[1] * 0.5,
            (north + 1) * 1000 - rows[0] * 0.5,
        )
        return GeometryWindow(
            self.version,
            bounds,
            arrays["surface"],
            arrays["terrain"],
            surface_valid,
            terrain_valid,
            receiver_valid,
            record.get("nominal_year_mismatch"),
        )


class CompactGeometryStore:
    """Read configured compact production tiles in metres, never raw int16 codes."""

    def __init__(self, root: Path):
        self.root = root
        self.ledger = json.loads((root / "manifest.json").read_text())
        self.settings = geometry_settings()
        if self.ledger.get("settings") != self.settings:
            raise ValueError("Compact geometry settings differ from configuration")
        self.version = self.ledger["preparation_version"]

    def read_window(
        self,
        tile: str,
        rows: tuple[int, int] = (0, 1000),
        columns: tuple[int, int] = (0, 1000),
        *,
        receiver_kind: Literal["ground", "bridge", "canopy", "tunnel"] = "ground",
    ) -> GeometryWindow:
        """Bound reads to one configured tile; preserve masks and receiver unknowns."""
        if receiver_kind not in ("ground", "bridge", "canopy", "tunnel"):
            raise ValueError("Unknown receiver kind")
        cell = self.settings["cell_size_metres"]
        size = int(1000 / cell)
        if not all(0 <= start < stop <= size for start, stop in (rows, columns)):
            raise ValueError("Window must lie inside one compact tile")
        east, north = map(int, tile.split("-"))
        if tile != f"{east}-{north}":
            raise ValueError("Invalid tile identifier")
        arrays, mismatch = {}, None
        for product in ("surface", "terrain"):
            record = self.ledger["assets"].get(f"{tile}-{product}")
            if record is None:
                values = np.full(
                    (rows[1] - rows[0], columns[1] - columns[0]),
                    NODATA,
                    dtype="float32",
                )
            else:
                path = self.root / f"{tile}-{product}.tif"
                if record["preparation_version"] != self.version or not verified_asset(
                    path, record["bytes"], record["sha256"]
                ):
                    raise ValueError(
                        "Compact geometry checksum/version failed; resume preparation"
                    )
                values = read_heights(
                    path,
                    Window(
                        columns[0], rows[0], columns[1] - columns[0], rows[1] - rows[0]
                    ),
                ).filled(NODATA)
                mismatch = record["survey_year_mismatch"]
            arrays[product] = values
        surface_valid, terrain_valid = (
            valid_cells(arrays[p]) for p in ("surface", "terrain")
        )
        receiver_valid = (
            surface_valid & terrain_valid & (arrays["surface"] >= arrays["terrain"])
        )
        if receiver_kind != "ground":
            receiver_valid[:] = False
        bounds = (
            east * 1000 + columns[0] * cell,
            (north + 1) * 1000 - rows[1] * cell,
            east * 1000 + columns[1] * cell,
            (north + 1) * 1000 - rows[0] * cell,
        )
        return GeometryWindow(
            self.version,
            bounds,
            arrays["surface"],
            arrays["terrain"],
            surface_valid,
            terrain_valid,
            receiver_valid,
            mismatch,
            resolution_m=cell,
            height_step_m=self.settings["height_step_metres"],
        )
