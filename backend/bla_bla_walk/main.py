"""Small foundation API; feature owners add their adapters after T1 merges."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .demo_fixture import fixture_snapshot
from .interfaces import MapSnapshot

app = FastAPI(title="Bla Bla Walk", version="0.1.0")
ROOT = Path(__file__).resolve().parents[2]
app.mount("/src", StaticFiles(directory=ROOT / "src"), name="browser")
app.mount(
    "/vendor",
    StaticFiles(directory=ROOT / ".cache/browser-assets", check_dir=False),
    name="browser-assets",
)


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    """Serve the map and API from one origin, without a JavaScript build step."""
    return FileResponse(ROOT / "index.html")


@app.get("/api/map", response_model=MapSnapshot)
def map_snapshot() -> MapSnapshot:
    """Serve labelled synthetic data; no live observation or shade claims."""
    return fixture_snapshot()
