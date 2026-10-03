# Bla Bla Walk

> Built at [HackAmRhein 2026](https://hackamrhein.dev) with Codex. First time in this repository? The setup guide is [HACKAMRHEIN.md](HACKAMRHEIN.md).

Bla Bla Walk is a proposed heat-aware walking route planner for Basel. It aims to help people who are more affected by heat, and their caregivers, compare routes using shade, drinking water, cooler places, and known obstacles.

## The problem

The shortest walk may involve exposed streets, few places to rest, or inaccessible crossings. The project explores how public environmental and map data could make those tradeoffs visible when planning a walk.

## Project status

The T1 foundation runs a real Basel basemap with two labelled synthetic layers. Toggle temperature and fountain samples, inspect provenance and timestamps, and see stale, missing and unknown states. FastAPI serves both the browser modules and API; no JavaScript package manager or build step is required. T8 prepares the checksum-pinned city geometry locally for the shade worker; calculated shade and route comparison remain later tasks. See [T1's handoff](handoff/t1-map-foundation.md) and [T8's handoff](handoff/t8.md) for validation and review state.

- [Design and demo proposal](docs/design.md)
- [Build tasks and acceptance checks](docs/plan.md)
- [Pick a task and start](TASK_START.md)
- [Recorded decisions](docs/decisions.md)
- [Future features](docs/future-features.md)
- [Proposed six-person work split](ROADMAP.md)
- [Team roles and shared-repository rules](TEAM.md)
- [Team collaboration guide](TEAMWORK.md)
- [Original meeting notes](notes/261002-001_Meeting_Heat-_and_Safety-Aware_Routing_Map_App-Summary.md) (historical source; see the design and plan for current proposals)

## Run locally

Use Python 3.12 or newer. From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
python scripts/fetch_browser_assets.py
python backend/export_contract.py
python -m uvicorn bla_bla_walk.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Open [the local map](http://127.0.0.1:8000). On Windows, use `python -m venv .venv` and run the Activate.ps1 script inside the environment's Scripts folder in PowerShell instead of the first two commands.

The browser assets are pinned by URL and SHA-256 in [config/browser-assets.json](config/browser-assets.json). The setup script downloads them into an ignored local cache, verifies their bytes and retains licence notices. Subsequent setup runs reuse matching files. An internet connection is needed for initial setup and real basemap tiles; fixture data and browser libraries are served locally.

## Prepare city geometry

T8 keeps the native 0.5 m Float32 surface and terrain grids outside Git under `data/geometry/`. The committed [geometry metadata](data/fixtures/geometry-metadata.json) records every selected tile, explicit source gaps, checksums, alignment and cell-flag policy. Preparation is safe to rerun: verified artifacts are reused and incomplete downloads resume.

```sh
python backend/prepare_geometry.py plan
python backend/prepare_geometry.py prepare --tiles 2613-1269 2614-1269 --workers 2 --batch-name vegetation-audit
python backend/prepare_geometry.py prepare --all --batch-size 8 --workers 2
python backend/prepare_geometry.py verify
```

Keep preparation at two workers or fewer. The full local output is about 3.7 GiB; a missing buffer source remains an explicit unknown rather than being filled or assumed clear. T10 consumes this prepared geometry and its flags but owns shade wire output.

## Development checks

Activate the environment and run from the repository root:

```sh
python backend/export_contract.py
python -m pytest -c backend/pyproject.toml backend/tests
python -m ruff check backend scripts/fetch_browser_assets.py scripts/format_browser.py
python -m ruff format --check backend scripts/fetch_browser_assets.py scripts/format_browser.py
python scripts/format_browser.py --check
bash scripts/doc-check.sh --strict
```

Browser checks use an installed Chromium; set `CHROMIUM_PATH` to its executable if it is not on PATH. These checks skip with a visible reason when no browser is available. Run only the API/model checks with `python -m pytest -c backend/pyproject.toml backend/tests -m 'not browser'`. No Node.js installation is required.

Format Python with `python -m ruff format backend scripts/fetch_browser_assets.py scripts/format_browser.py` and browser code with `python scripts/format_browser.py`. [backend/bla_bla_walk/interfaces.py](backend/bla_bla_walk/interfaces.py) is canonical; regeneration writes [src/interfaces.ts](src/interfaces.ts) for editor/JSDoc use and the browser validation schema. Include a decision line with model changes and never edit generated files by hand. Consumer ownership is listed in [ROADMAP.md](ROADMAP.md); the map modules now use .js filenames.

## Data sources

See [docs/SOURCES.md](docs/SOURCES.md).

## Limits

Only the basemap is provider data in this foundation. Overlay locations and values are invented, visibly labelled fixtures. No safety claims, route validation or shade accuracy/performance have been established. This prototype is not a navigation or emergency service. Scope, unknowns, and demo fallback are documented in the [design brief](docs/design.md).

## Team

The six-person work split is proposed in [ROADMAP.md](ROADMAP.md). Contributors still need to choose role slots and add their GitHub usernames in [TEAM.md](TEAM.md).
