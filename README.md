# Bla Bla Walk

> Built at [HackAmRhein 2026](https://hackamrhein.dev) with Codex. First time in this repository? The setup guide is [HACKAMRHEIN.md](HACKAMRHEIN.md).

Bla Bla Walk is a proposed heat-aware walking route planner for Basel. It aims to help people who are more affected by heat, and their caregivers, compare routes using shade, drinking water, cooler places, and known obstacles.

## The problem

The shortest walk may involve exposed streets, few places to rest, or inaccessible crossings. The project explores how public environmental and map data could make those tradeoffs visible when planning a walk.

## Project status

T1 is an incomplete implementation checkpoint for a TypeScript/OpenLayers map and Python FastAPI API. The screen and API code are written, but dependency installation, version pins, generated client files and application checks are pending. A real Basel basemap tile request succeeded independently. Live observations, calculated shade and route comparison are later tasks. See [T1's handoff](handoff/t1-map-foundation.md) for current validation and publishing state.

- [Design and demo proposal](docs/design.md)
- [Build tasks and acceptance checks](docs/plan.md)
- [Pick a task and start](TASK_START.md)
- [Recorded decisions](docs/decisions.md)
- [Proposed six-person work split](ROADMAP.md)
- [Team roles and shared-repository rules](TEAM.md)
- [Team collaboration guide](TEAMWORK.md)
- [Original meeting notes](notes/261002-001_Meeting_Heat-_and_Safety-Aware_Routing_Map_App-Summary.md) (historical source; see the design and plan for current proposals)

## Startup status

A fresh checkout is not runnable yet. T1 still needs project dependencies, npm's lockfile, pinned Python requirements and generated browser files. Installation approval and the Python package-manager choice are pending. Verified setup and run instructions will be added when those steps are complete.

The intended development setup uses Python 3.12 or newer and Node.js 22.12 or newer, with Vite at port 5173 forwarding `/api` requests to FastAPI at port 8000. The basemap requires an internet connection; fixture data is synthetic and served locally.

## Pending development checks

The scripts and contract checks are authored but cannot run until dependencies and generated files are available. Planned checks from the repository root are:

```sh
npm run contracts:generate
npm test
npm run lint
npm run build
npm run fmt:check
python -m pytest -c backend/pyproject.toml backend/tests
python -m ruff check backend
python -m ruff format --check backend
```

Formatting scripts are `npm run fmt` and `python -m ruff format backend`. [backend/bla_bla_walk/interfaces.py](backend/bla_bla_walk/interfaces.py) is the canonical wire contract. The generation script will write client types and the browser validation schema after setup. Include a decision line with model changes. Never edit generated files by hand. Owned consumer paths are listed in [ROADMAP.md](ROADMAP.md).

## Data sources

See [docs/SOURCES.md](docs/SOURCES.md).

## Limits

Only the basemap is provider data in this foundation. Overlay locations and values are invented, visibly labelled fixtures. No safety claims, route validation or shade accuracy/performance have been established. This prototype is not a navigation or emergency service. Scope, unknowns, and demo fallback are documented in the [design brief](docs/design.md).

## Team

The six-person work split is proposed in [ROADMAP.md](ROADMAP.md). Contributors still need to choose role slots and add their GitHub usernames in [TEAM.md](TEAM.md).
