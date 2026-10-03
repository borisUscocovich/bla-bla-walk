"""Canonical wire models. Generate browser types; never edit client copies.

Coordinates are WGS84 longitude/latitude (GeoJSON), not LV95 processing metres.
Unknown values stay null. Source times are distinct from calculation times.
Feature tasks extend these models with a decision line before regeneration.
"""

from typing import Annotated, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

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
    mode: Literal["fixture", "online", "offline"] = "fixture"
