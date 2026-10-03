"""Canonical wire and worker models. Generate browser types; never edit copies.

Coordinates are WGS84 longitude/latitude (GeoJSON), not LV95 processing metres.
Unknown values stay null. Source times are distinct from calculation times.
Feature tasks extend these models with a decision line before regeneration.
Worker GeometryWindow uses LV95 metres and native raster arrays, not GeoJSON.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Annotated, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray


@dataclass(frozen=True)
class GeometryWindow:
    """A bounded native tile window for T10, never a shade coverage promise.

    Arrays are north-first at 0.5m in EPSG:2056; heights are LN02/EPSG:5728
    metres. Missing elevations are -9999. Valid masks describe samples only.
    Mixed survey years and negative relative heights retain scene uncertainty.
    Receiver elevations on bridges, under canopy or in tunnels are unknown.
    Halo/ray reach must be checked separately; stream neighbouring tiles.
    """

    geometry_version: str
    bounds_epsg2056: tuple[float, float, float, float]
    surface: "NDArray[np.float32]"
    terrain: "NDArray[np.float32]"
    surface_valid: "NDArray[np.bool_]"
    terrain_valid: "NDArray[np.bool_]"
    receiver_valid: "NDArray[np.bool_]"
    nominal_year_mismatch: bool | None
    resolution_m: float = 0.5
    vertical_reference: str = "LN02 / EPSG:5728"


Longitude = Annotated[float, Field(ge=-180, le=180)]
Latitude = Annotated[float, Field(ge=-90, le=90)]
Position = tuple[Longitude, Latitude]
Availability = Literal["current", "stale", "missing", "unknown", "unsupported"]
LayerKind = Literal["observation", "fountain", "shade", "route"]


class ContractModel(BaseModel):
    """Reject undeclared fields so producers cannot silently drift."""

    model_config = ConfigDict(extra="forbid")


class PointGeometry(ContractModel):
    """A known point location, even when its measured value is missing."""

    type: Literal["Point"]
    coordinates: Position


class LineGeometry(ContractModel):
    """A walking line in display coordinates; does not imply eligibility."""

    type: Literal["LineString"]
    coordinates: Annotated[list[Position], Field(min_length=2)]


class PolygonGeometry(ContractModel):
    """GeoJSON rings for later calculated shade coverage."""

    type: Literal["Polygon"]
    coordinates: list[Annotated[list[Position], Field(min_length=4)]]


class Provenance(ContractModel):
    """Provider, reuse terms and distinct observation/retrieval timestamps."""

    provider: str
    source_url: str | None = None
    attribution: str
    licence: str
    fixture: bool
    observed_at: AwareDatetime | None = None
    retrieved_at: AwareDatetime | None = None


class ShadeMetadata(ContractModel):
    """Calculation context, independent of sensor observations."""

    requested_time: AwareDatetime
    effective_time: AwareDatetime
    geometry_version: str
    resolution_m: Annotated[float, Field(gt=0)]


class RouteMetrics(ContractModel):
    """Basic walking effort; comparison rules and scoring come from T2/T5."""

    distance_m: Annotated[float, Field(ge=0)]
    duration_s: Annotated[float, Field(ge=0)]


class MapFeature(ContractModel):
    """One display feature, with explicit evidence and unknown values."""

    id: str
    label: str
    kind: LayerKind
    geometry: Annotated[
        PointGeometry | LineGeometry | PolygonGeometry, Field(discriminator="type")
    ]
    availability: Availability
    explanation: str
    provenance: Provenance
    value: float | None = None
    unit: str | None = None
    drinking_water: Literal["yes", "no", "unknown"] | None = None
    shade: ShadeMetadata | None = None
    route: RouteMetrics | None = None


class MapLayer(ContractModel):
    """Independently toggleable layer; empty is distinct from a failed layer."""

    id: str
    label: str
    kind: LayerKind
    availability: Availability
    explanation: str
    features: list[MapFeature]


class MapSnapshot(ContractModel):
    """API envelope shared by observations, fountains, shade and route layers."""

    generated_at: AwareDatetime
    layers: list[MapLayer]
