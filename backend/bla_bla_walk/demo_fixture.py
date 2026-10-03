"""Synthetic foundation data; live adapters belong to later owned tasks."""

from datetime import UTC, datetime

from .interfaces import MapFeature, MapLayer, MapSnapshot, PointGeometry, Provenance


def fixture_snapshot() -> MapSnapshot:
    """Return two labelled fixture layers, including stale and missing examples."""
    provenance = Provenance(
        provider="Bla Bla Walk synthetic demo",
        attribution="Bla Bla Walk team; invented values and locations",
        licence="Project-authored synthetic fixture; no provider data",
        fixture=True,
        observed_at=datetime(2026, 10, 1, 12, tzinfo=UTC),
        retrieved_at=datetime(2026, 10, 1, 13, tzinfo=UTC),
    )
    observations = [
        MapFeature(
            id="fixture-temperature-stale",
            label="Sample sensor A",
            kind="observation",
            geometry=PointGeometry(type="Point", coordinates=(7.5886, 47.5596)),
            availability="stale",
            explanation="Invented saved reading. It is not today's temperature.",
            provenance=provenance,
            value=28,
            unit="°C",
        ),
        MapFeature(
            id="fixture-temperature-missing",
            label="Sample sensor B",
            kind="observation",
            geometry=PointGeometry(type="Point", coordinates=(7.5944, 47.5621)),
            availability="missing",
            explanation="No reading. Missing values are not treated as cooler.",
            provenance=provenance.model_copy(update={"observed_at": None}),
        ),
    ]
    fountains = [
        MapFeature(
            id="fixture-fountain-unknown",
            label="Sample fountain A",
            kind="fountain",
            geometry=PointGeometry(type="Point", coordinates=(7.5857, 47.5574)),
            availability="unknown",
            explanation="Invented location. Drinking water and operation unverified.",
            provenance=provenance.model_copy(update={"observed_at": None}),
            drinking_water="unknown",
        )
    ]
    return MapSnapshot(
        generated_at=datetime.now(UTC),
        layers=[
            MapLayer(
                id="fixture-observations",
                label="Temperature · fixture",
                kind="observation",
                availability="stale",
                explanation="Squares: synthetic readings; stale or missing.",
                features=observations,
            ),
            MapLayer(
                id="fixture-fountains",
                label="Fountains · fixture",
                kind="fountain",
                availability="unknown",
                explanation="Circles: synthetic locations; drinking status unknown.",
                features=fountains,
            ),
        ],
    )
