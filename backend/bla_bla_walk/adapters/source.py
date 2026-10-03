"""Bounded HTTP and last-good layer caching for public-data adapters."""

import json
import time
from collections.abc import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ..interfaces import MapLayer

MAX_RESPONSE_BYTES = 2_000_000
REQUEST_TIMEOUT_SECONDS = 8
RETRY_DELAY_SECONDS = 60
MAX_PAGE_RECORDS = 100


class SourceUnavailable(RuntimeError):
    """The source failed, or its response exceeded adapter limits."""


def fetch_json(url: str) -> dict | list:
    """Fetch a small JSON response with fixed timeout and byte bounds."""
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except (HTTPError, URLError, TimeoutError) as error:
        raise SourceUnavailable("The public source could not be reached.") from error

    if len(body) > MAX_RESPONSE_BYTES:
        raise SourceUnavailable("The public source response exceeded the size limit.")
    try:
        payload = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SourceUnavailable("The public source returned invalid JSON.") from error
    if not isinstance(payload, (dict, list)):
        raise SourceUnavailable("The public source returned an unexpected response.")
    return payload


class LayerCache:
    """Keep a bounded refresh cadence and visibly retain last-good data."""

    def __init__(self, ttl_seconds: int, clock: Callable[[], float] = time.monotonic):
        self._ttl_seconds = ttl_seconds
        self._clock = clock
        self._layer: MapLayer | None = None
        self._refresh_at = 0.0

    def get(
        self, refresh: Callable[[], MapLayer], empty_layer: Callable[[], MapLayer]
    ) -> MapLayer:
        """Refresh when due; retain an old layer as stale after failure."""
        now = self._clock()
        if self._layer is not None and now < self._refresh_at:
            return self._layer

        try:
            layer = refresh()
        except SourceUnavailable:
            self._refresh_at = now + RETRY_DELAY_SECONDS
            if self._layer is None:
                return empty_layer()
            already_stale = self._layer.availability == "stale"
            stale_features = [
                feature.model_copy(
                    update={
                        "availability": "stale",
                        "explanation": feature.explanation
                        if already_stale
                        else (
                            f"{feature.explanation} Last good source snapshot retained."
                        ),
                    }
                )
                for feature in self._layer.features
            ]
            self._layer = self._layer.model_copy(
                update={
                    "availability": "stale",
                    "explanation": (
                        "Source refresh failed; retained the last good snapshot."
                    ),
                    "features": stale_features,
                }
            )
            return self._layer

        self._layer = layer
        self._refresh_at = now + self._ttl_seconds
        return layer
