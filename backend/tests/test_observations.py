"""T4 adapter joins, freshness states, bounded inputs and source provenance."""

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from bla_bla_walk.adapters.fountains import RECORDS_URL as FOUNTAIN_URL
from bla_bla_walk.adapters.fountains import FountainAdapter
from bla_bla_walk.adapters.source import SourceUnavailable
from bla_bla_walk.adapters.temperature import (
    CURRENT_AGE_SECONDS,
    OBSERVATIONS_EXPORT_URL,
    STATIONS_URL,
    TemperatureAdapter,
)

FIXTURES = Path(__file__).resolve().parents[2] / "data" / "fixtures"
NOW = datetime(2026, 10, 3, 11, 12, tzinfo=UTC)


def test_fixture_records_are_minimal_and_rights_limited():
    observations = json.loads((FIXTURES / "observations.json").read_text())
    fountains = json.loads((FIXTURES / "fountains.json").read_text())

    assert observations["fixture"] is True
    assert observations["features"][0]["air_temperature_celsius"] == 19.39
    assert observations["features"][0]["observed_at"] == "2026-10-03T11:00:01Z"
    assert fountains["fixture"] is True
    assert fountains["features"][0]["drinking_water"] == "unknown"
    assert "noncommercial" in fountains["license"].lower()
    assert not {"desc", "picture_link", "gx_media_links"} & set(
        fountains["features"][0]
    )


def test_temperature_joins_by_station_id_and_shows_each_reading_age():
    stations = [
        {
            "name_original": "S1",
            "name_custom": "Station One",
            "coords": {"lon": 7.6, "lat": 47.56},
        },
        {
            "name_original": "OUTSIDE",
            "name_custom": "Outside Map",
            "coords": {"lon": 8.0, "lat": 47.56},
        },
    ]
    observations = [
        {
            "name_original": "S1",
            "dates_max_date": "2026-10-03T10:00:00Z",
            "meta_airtemp": 18.0,
            "coords": {"lon": 7.6, "lat": 47.56},
        },
        {
            "name_original": "S1",
            "dates_max_date": "2026-10-03T11:05:00Z",
            "meta_airtemp": 20.5,
            "coords": {"lon": 7.6, "lat": 47.56},
        },
        {
            "name_original": "UNKNOWN",
            "dates_max_date": "2026-10-03T11:10:00Z",
            "meta_airtemp": 99,
            "coords": {"lon": 7.6, "lat": 47.56},
        },
    ]

    def transport(url):
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        if parsed.path == urlparse(STATIONS_URL).path:
            assert query["limit"] == ["100"]
            assert query["offset"] == ["0"]
            return {"total_count": 2, "results": stations}
        assert parsed.path == urlparse(OBSERVATIONS_EXPORT_URL).path
        assert query["limit"] == ["5000"]
        assert query["order_by"] == ["dates_max_date desc"]
        return observations

    adapter = TemperatureAdapter(transport=transport, now=lambda: NOW)
    layer = adapter.get_layer()
    assert len(layer.features) == 1
    feature = layer.features[0]
    assert feature.id == "temperature-S1"
    assert feature.label == "Station One"
    assert feature.value == 20.5
    assert feature.unit == "°C"
    assert feature.availability == "current"
    assert "7 minutes" in feature.explanation
    assert feature.provenance.observed_at == datetime(2026, 10, 3, 11, 5, tzinfo=UTC)
    assert feature.provenance.fixture is False
    assert feature.provenance.attribution == "meteoblue AG via Open Data Basel-Stadt"


def test_old_temperature_is_stale_and_missing_readings_keep_station_location():
    stations = [
        {
            "name_original": "OLD",
            "name_custom": "Old Station",
            "coords": {"lon": 7.6, "lat": 47.56},
        },
        {
            "name_original": "EMPTY",
            "name_custom": "No Reading",
            "coords": {"lon": 7.61, "lat": 47.57},
        },
    ]
    observation = {
        "name_original": "OLD",
        "dates_max_date": (
            NOW - timedelta(seconds=CURRENT_AGE_SECONDS + 1)
        ).isoformat(),
        "meta_airtemp": 17.0,
        "coords": {"lon": 7.6, "lat": 47.56},
    }

    def transport(url):
        path = urlparse(url).path
        return (
            {"total_count": 2, "results": stations}
            if path == urlparse(STATIONS_URL).path
            else [observation]
        )

    layer = TemperatureAdapter(transport=transport, now=lambda: NOW).get_layer()
    by_id = {feature.id: feature for feature in layer.features}
    assert by_id["temperature-OLD"].availability == "stale"
    assert by_id["temperature-EMPTY"].availability == "missing"
    assert by_id["temperature-EMPTY"].value is None
    assert by_id["temperature-EMPTY"].provenance.observed_at is None


def test_station_catalogue_pages_at_the_source_limit():
    stations = [
        {
            "name_original": f"S{index}",
            "name_custom": f"Station {index}",
            "coords": {"lon": 7.6, "lat": 47.56},
        }
        for index in range(101)
    ]
    station_offsets = []

    def transport(url):
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        if parsed.path == urlparse(STATIONS_URL).path:
            station_offsets.append(int(query["offset"][0]))
            assert int(query["limit"][0]) <= 100
            offset = int(query["offset"][0])
            return {
                "total_count": len(stations),
                "results": stations[offset : offset + 100],
            }
        return []

    layer = TemperatureAdapter(transport=transport, now=lambda: NOW).get_layer()
    assert station_offsets == [0, 100]
    assert len(layer.features) == len(stations)


def test_fountain_catalogue_pages_at_the_source_limit():
    records = [
        {
            "name": f"Fountain {index}",
            "geo_point_2d": {"lon": 7.588, "lat": 47.558},
        }
        for index in range(305)
    ]
    offsets = []

    def transport(url):
        query = parse_qs(urlparse(url).query)
        limit, offset = int(query["limit"][0]), int(query["offset"][0])
        assert limit <= 100
        offsets.append(offset)
        return {
            "total_count": len(records),
            "results": records[offset : offset + limit],
        }

    layer = FountainAdapter(transport=transport, now=lambda: NOW).get_layer()
    assert offsets == [0, 100, 200, 300]
    assert len(layer.features) == len(records)


def test_failed_temperature_refresh_retains_last_good_as_stale():
    station = {
        "name_original": "S1",
        "name_custom": "Station One",
        "coords": {"lon": 7.6, "lat": 47.56},
    }
    monotonic = [0.0]
    now = [NOW]
    fail = [False]

    def transport(url):
        if fail[0]:
            raise SourceUnavailable("offline")
        path = urlparse(url).path
        if path == urlparse(STATIONS_URL).path:
            return {"total_count": 1, "results": [station]}
        return [
            {
                "name_original": "S1",
                "dates_max_date": NOW.isoformat(),
                "meta_airtemp": 21.0,
                "coords": station["coords"],
            }
        ]

    adapter = TemperatureAdapter(
        transport=transport,
        now=lambda: now[0],
        monotonic=lambda: monotonic[0],
    )
    good = adapter.get_layer()
    fail[0] = True
    monotonic[0] = 3601
    stale = adapter.get_layer()
    assert good.features[0].value == 21
    assert stale.availability == "stale"
    assert stale.features[0].availability == "stale"
    assert stale.features[0].value == 21
    assert stale.features[0].provenance.observed_at == NOW
    assert "last good" in stale.explanation.lower()


def test_fountain_locations_keep_unknown_type_access_and_attribution():
    def transport(url):
        parsed = urlparse(url)
        assert parsed.path == urlparse(FOUNTAIN_URL).path
        assert parse_qs(parsed.query)["select"] == ["name,geo_point_2d"]
        return {
            "total_count": 1,
            "results": [
                {
                    "name": "Sevogel-Brunnen",
                    "geo_point_2d": {"lon": 7.5887686, "lat": 47.5587034},
                    "desc": "Ignored unstructured text",
                }
            ],
        }

    layer = FountainAdapter(transport=transport, now=lambda: NOW).get_layer()
    feature = layer.features[0]
    assert feature.label == "Sevogel-Brunnen"
    assert feature.geometry.coordinates == (7.5887686, 47.5587034)
    assert feature.drinking_water == "unknown"
    assert feature.availability == "unknown"
    assert "not provided" in feature.explanation.lower()
    assert feature.provenance.attribution == "IWB Industrielle Werke Basel"
    assert "Noncommercial" in feature.provenance.licence
    assert feature.provenance.fixture is False
    assert feature.provenance.retrieved_at == NOW


def test_fountain_refresh_failure_retains_last_good_location_as_stale():
    monotonic = [0.0]
    fail = [False]

    def transport(_url):
        if fail[0]:
            raise SourceUnavailable("offline")
        return {
            "total_count": 1,
            "results": [
                {
                    "name": "Sevogel-Brunnen",
                    "geo_point_2d": {"lon": 7.5887686, "lat": 47.5587034},
                }
            ],
        }

    adapter = FountainAdapter(transport=transport, monotonic=lambda: monotonic[0])
    first = adapter.get_layer()
    fail[0] = True
    monotonic[0] = 24 * 60 * 60 + 1
    stale = adapter.get_layer()
    assert first.features[0].id == stale.features[0].id
    assert stale.features[0].availability == "stale"
    assert stale.features[0].drinking_water == "unknown"
    assert stale.features[0].provenance.attribution == "IWB Industrielle Werke Basel"


def test_source_failure_without_cache_returns_explicit_missing_layers():
    def offline(_url):
        raise SourceUnavailable("offline")

    assert TemperatureAdapter(transport=offline).get_layer().availability == "missing"
    assert FountainAdapter(transport=offline).get_layer().availability == "missing"
