"""Small foundation API; feature owners add their adapters after T1 merges."""

from fastapi import FastAPI

from .demo_fixture import fixture_snapshot
from .interfaces import MapSnapshot

app = FastAPI(title="Bla Bla Walk", version="0.1.0")


@app.get("/api/map", response_model=MapSnapshot)
def map_snapshot() -> MapSnapshot:
    """Serve labelled synthetic data; no live observation or shade claims."""
    return fixture_snapshot()
