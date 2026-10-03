"""Noncommercial IWB fountain locations with unknown drinking status."""

import math
from collections.abc import Callable
from datetime import UTC, datetime
from hashlib import sha256
from urllib.parse import urlencode

from ..interfaces import MapFeature, MapLayer, PointGeometry, Provenance
from .source import MAX_PAGE_RECORDS, LayerCache, SourceUnavailable, fetch_json
from .temperature import MAP_BOUNDS

RECORDS_URL = "https://data.bs.ch/api/explore/v2.1/catalog/datasets/100008/records"
SOURCE_URL = "https://data.bs.ch/explore/dataset/100008/"
ATTRIBUTION = "IWB Industrielle Werke Basel"
LICENCE = (
    "Noncommercial use with attribution; commercial use requires supplier permission"
)
RECORD_LIMIT = 350
PAGE_SIZE = MAX_PAGE_RECORDS
REFRESH_SECONDS = 24 * 60 * 60


class FountainAdapter:
    """Fetch a bounded fountain list without inferring operational status."""

    def __init__(
        self,
        transport: Callable = fetch_json,
        now: Callable[[], datetime] = lambda: datetime.now(UTC),
        monotonic: Callable | None = None,
    ):
        self._transport = transport
        self._now = now
        self._cache = LayerCache(
            REFRESH_SECONDS, **({"clock": monotonic} if monotonic else {})
        )

    def get_layer(self) -> MapLayer:
        """Return the latest catalog locations, or a stale cached layer."""
        return self._cache.get(self._fetch_layer, self._empty_layer)

    def _fetch_layer(self) -> MapLayer:
        records = []
        for offset in range(0, RECORD_LIMIT, PAGE_SIZE):
            limit = min(PAGE_SIZE, RECORD_LIMIT - offset)
            query = urlencode(
                {
                    "select": "name,geo_point_2d",
                    "limit": limit,
                    "offset": offset,
                }
            )
            payload = self._transport(f"{RECORDS_URL}?{query}")
            if not isinstance(payload, dict):
                raise SourceUnavailable(
                    "The fountain source returned an unexpected response."
                )
            if (
                not isinstance(payload.get("total_count"), int)
                or payload["total_count"] > RECORD_LIMIT
            ):
                raise SourceUnavailable(
                    "The fountain catalogue exceeded its bounded record limit."
                )
            page = payload.get("results")
            if not isinstance(page, list) or any(
                not isinstance(row, dict) for row in page
            ):
                raise SourceUnavailable(
                    "The fountain source returned malformed records."
                )
            if len(page) > limit:
                raise SourceUnavailable(
                    "The fountain source exceeded the requested page size."
                )
            records.extend(page)
            if len(page) < limit:
                break

        west, south, east, north = MAP_BOUNDS
        features = []
        seen: set[str] = set()
        retrieved_at = self._now().astimezone(UTC)
        for row in records:
            point = row.get("geo_point_2d")
            if not isinstance(point, dict):
                continue
            try:
                lon, lat = float(point["lon"]), float(point["lat"])
            except (KeyError, TypeError, ValueError):
                continue
            if not math.isfinite(lon + lat) or not (
                west <= lon <= east and south <= lat <= north
            ):
                continue
            name = row.get("name")
            label = (
                name.strip()
                if isinstance(name, str) and name.strip()
                else "Unlabelled IWB fountain"
            )
            source_key = f"{label.casefold()}|{lon:.7f}|{lat:.7f}"
            feature_id = "iwb-fountain-" + sha256(source_key.encode()).hexdigest()[:16]
            if feature_id in seen:
                continue
            seen.add(feature_id)
            features.append(
                MapFeature(
                    id=feature_id,
                    label=label,
                    kind="fountain",
                    geometry=PointGeometry(type="Point", coordinates=(lon, lat)),
                    availability="unknown",
                    explanation=(
                        "IWB lists this fountain location. Drinking-water type, "
                        "operating condition, and access are not provided."
                    ),
                    provenance=Provenance(
                        provider="Industrielle Werke Basel (IWB)",
                        source_url=SOURCE_URL,
                        attribution=ATTRIBUTION,
                        licence=LICENCE,
                        fixture=False,
                        retrieved_at=retrieved_at,
                    ),
                    drinking_water="unknown",
                )
            )
        if not records:
            raise SourceUnavailable("The fountain source returned no records.")
        return MapLayer(
            id="fountains-iwb",
            label="Fountains · IWB",
            kind="fountain",
            availability="current",
            explanation=(
                f"{len(features)} mapped locations. Drinking status, operation, "
                "and access remain unknown."
            ),
            features=features,
        )

    @staticmethod
    def _empty_layer() -> MapLayer:
        return MapLayer(
            id="fountains-iwb",
            label="Fountains · IWB",
            kind="fountain",
            availability="missing",
            explanation="IWB source unavailable; no last-good fountain list exists.",
            features=[],
        )
