"""Latest-per-station temperature observations from Open Data Basel-Stadt."""

import math
from collections.abc import Callable
from datetime import UTC, datetime
from urllib.parse import urlencode

from ..interfaces import MapFeature, MapLayer, PointGeometry, Provenance
from .source import MAX_PAGE_RECORDS, LayerCache, SourceUnavailable, fetch_json

API = "https://data.bs.ch/api/explore/v2.1/catalog/datasets"
STATIONS_URL = f"{API}/100082/records"
OBSERVATIONS_URL = f"{API}/100009/records"
OBSERVATIONS_EXPORT_URL = f"{API}/100009/exports/json"
SOURCE_URL = "https://data.bs.ch/explore/dataset/100009/"
STATION_SOURCE_URL = "https://data.bs.ch/explore/dataset/100082/"
ATTRIBUTION = "meteoblue AG via Open Data Basel-Stadt"
LICENCE = "CC BY 4.0"
MAP_BOUNDS = (7.544814498, 47.508699688, 7.704595246, 47.607375471)
STATION_LIMIT = 250
PAGE_SIZE = MAX_PAGE_RECORDS
MAX_OBSERVATION_RECORDS = 5000
CURRENT_AGE_SECONDS = 90 * 60
REFRESH_SECONDS = 60 * 60


def parse_time(value: object) -> datetime | None:
    """Parse only timezone-aware provider timestamps."""
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone(UTC) if parsed.utcoffset() is not None else None


def _point(row: dict) -> tuple[float, float] | None:
    coords = row.get("coords")
    if not isinstance(coords, dict):
        return None
    try:
        lon, lat = float(coords["lon"]), float(coords["lat"])
    except (KeyError, TypeError, ValueError):
        return None
    west, south, east, north = MAP_BOUNDS
    if not math.isfinite(lon + lat) or not (
        west <= lon <= east and south <= lat <= north
    ):
        return None
    return lon, lat


def _records(
    url: str,
    params: dict[str, object],
    transport: Callable = fetch_json,
    max_records: int | None = None,
) -> list[dict]:
    payload = transport(f"{url}?{urlencode(params)}")
    if not isinstance(payload, dict):
        raise SourceUnavailable("The temperature source returned malformed records.")
    records = payload.get("results")
    if not isinstance(records, list) or any(
        not isinstance(row, dict) for row in records
    ):
        raise SourceUnavailable("The temperature source returned malformed records.")
    requested_limit = params.get("limit")
    if (
        not isinstance(requested_limit, int)
        or requested_limit < 0
        or requested_limit > MAX_PAGE_RECORDS
    ):
        raise SourceUnavailable("The temperature query exceeded the source page limit.")
    if isinstance(requested_limit, int) and len(records) > requested_limit:
        raise SourceUnavailable(
            "The temperature source exceeded the requested page size."
        )
    if max_records is not None and (
        not isinstance(payload.get("total_count"), int)
        or payload["total_count"] > max_records
    ):
        raise SourceUnavailable("The station catalogue exceeded its bounded page.")
    return records


class TemperatureAdapter:
    """Join each bounded-map station to its latest bounded observation."""

    def __init__(
        self,
        transport: Callable = fetch_json,
        now: Callable[[], datetime] = lambda: datetime.now(UTC),
        monotonic: Callable[[], float] | None = None,
    ):
        self._transport = transport
        self._now = now
        self._cache = LayerCache(
            REFRESH_SECONDS, **({"clock": monotonic} if monotonic else {})
        )

    def get_layer(self) -> MapLayer:
        """Return age-aware readings, or the last-good layer marked stale."""
        layer = self._cache.get(self._fetch_layer, self._empty_layer)
        return self._with_current_ages(layer, self._now())

    def _fetch_layer(self) -> MapLayer:
        station_rows = []
        for offset in range(0, STATION_LIMIT, PAGE_SIZE):
            limit = min(PAGE_SIZE, STATION_LIMIT - offset)
            rows = _records(
                STATIONS_URL,
                {
                    "select": "name_original,name_custom,coords",
                    "limit": limit,
                    "offset": offset,
                },
                self._transport,
                max_records=STATION_LIMIT,
            )
            station_rows.extend(rows)
            if len(rows) < limit:
                break
        stations = {
            row["name_original"]: row
            for row in station_rows
            if isinstance(row.get("name_original"), str) and _point(row) is not None
        }
        if not stations:
            raise SourceUnavailable("No map-area stations were returned.")

        observations: dict[str, dict] = {}
        selected = "name_original,name_custom,dates_max_date,meta_airtemp,coords"
        query = urlencode(
            {
                "select": selected,
                "order_by": "dates_max_date desc",
                "limit": MAX_OBSERVATION_RECORDS,
            }
        )
        rows = self._transport(f"{OBSERVATIONS_EXPORT_URL}?{query}")
        if (
            not isinstance(rows, list)
            or len(rows) > MAX_OBSERVATION_RECORDS
            or any(not isinstance(row, dict) for row in rows)
        ):
            raise SourceUnavailable("The temperature export exceeded its record limit.")
        for row in rows:
            station_id = row.get("name_original")
            observed_at = parse_time(row.get("dates_max_date"))
            if station_id not in stations or observed_at is None:
                continue
            try:
                value = float(row["meta_airtemp"])
            except (KeyError, TypeError, ValueError):
                continue
            if not math.isfinite(value):
                continue
            prior = observations.get(station_id)
            if prior is None or observed_at > prior["observed_at"]:
                observations[station_id] = {
                    "row": row,
                    "observed_at": observed_at,
                    "value": value,
                }

        retrieved_at = self._now().astimezone(UTC)
        features = []
        for station_id, station in sorted(stations.items()):
            item = observations.get(station_id)
            row = item["row"] if item else station
            coordinates = _point(row) or _point(station)
            if coordinates is None:
                continue
            observed_at = item["observed_at"] if item else None
            value = item["value"] if item else None
            age = retrieved_at - observed_at if observed_at else None
            availability = (
                "missing"
                if item is None
                else "current"
                if age.total_seconds() <= CURRENT_AGE_SECONDS
                else "stale"
            )
            label = station.get("name_custom") or station_id
            if availability == "missing":
                explanation = (
                    "No temperature reading appeared in the bounded recent-record "
                    "window."
                )
            else:
                explanation = (
                    f"Observation age: {self._age_text(age.total_seconds())}. "
                    "Raw, uncorrected sensor value."
                )
            features.append(
                MapFeature(
                    id=f"temperature-{station_id}",
                    label=str(label),
                    kind="observation",
                    geometry=PointGeometry(type="Point", coordinates=coordinates),
                    availability=availability,
                    explanation=explanation,
                    provenance=Provenance(
                        provider="meteoblue AG via Open Data Basel-Stadt",
                        source_url=SOURCE_URL,
                        attribution=ATTRIBUTION,
                        licence=LICENCE,
                        fixture=False,
                        observed_at=observed_at,
                        retrieved_at=retrieved_at,
                    ),
                    value=value,
                    unit="°C" if value is not None else None,
                )
            )

        readings = sum(feature.value is not None for feature in features)
        state = self._layer_state(features)
        layer_explanation = (
            f"{readings} readings joined to {len(features)} station locations. "
            "Records are raw and uncorrected; ages appear when a point is selected."
        )
        return MapLayer(
            id="observations-meteoblue",
            label="Air temperature · meteoblue",
            kind="observation",
            availability=state,
            explanation=layer_explanation,
            features=features,
        )

    def _empty_layer(self) -> MapLayer:
        return MapLayer(
            id="observations-meteoblue",
            label="Air temperature · meteoblue",
            kind="observation",
            availability="missing",
            explanation="Temperature source unavailable; no last-good snapshot exists.",
            features=[],
        )

    def _with_current_ages(self, layer: MapLayer, now: datetime) -> MapLayer:
        if layer.availability == "stale":
            return layer
        features = []
        for feature in layer.features:
            observed_at = feature.provenance.observed_at
            if observed_at is None or feature.value is None:
                features.append(feature)
                continue
            seconds = max(0.0, (now.astimezone(UTC) - observed_at).total_seconds())
            availability = "current" if seconds <= CURRENT_AGE_SECONDS else "stale"
            explanation = (
                f"Observation age: {self._age_text(seconds)}. "
                "Raw, uncorrected sensor value."
            )
            features.append(
                feature.model_copy(
                    update={"availability": availability, "explanation": explanation}
                )
            )
        return layer.model_copy(
            update={"availability": self._layer_state(features), "features": features}
        )

    @staticmethod
    def _layer_state(features: list[MapFeature]) -> str:
        if not features or all(
            feature.availability == "missing" for feature in features
        ):
            return "missing"
        if any(feature.availability == "stale" for feature in features):
            return "stale"
        return "current"

    @staticmethod
    def _age_text(seconds: float) -> str:
        minutes = max(0, int(seconds // 60))
        if minutes < 60:
            return f"{minutes} minutes"
        hours, remainder = divmod(minutes, 60)
        return f"{hours} hours and {remainder} minutes"
