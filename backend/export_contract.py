"""Export schemas and a fixture from the same canonical Python models."""

import json
from pathlib import Path

from bla_bla_walk.demo_fixture import fixture_snapshot
from bla_bla_walk.interfaces import MapSnapshot
from bla_bla_walk.main import app

ROOT = Path(__file__).resolve().parents[1]


def write_json(path: Path, value: object) -> None:
    """Write deterministic JSON for generation and cross-language checks."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write_json(ROOT / ".cache/openapi.json", app.openapi())
    write_json(ROOT / "src/snapshot.schema.json", MapSnapshot.model_json_schema())
    write_json(
        ROOT / ".cache/fixture-snapshot.json",
        fixture_snapshot().model_dump(mode="json"),
    )
