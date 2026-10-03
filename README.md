# Bla Bla Walk

> Built at [HackAmRhein 2026](https://hackamrhein.dev) with Codex. First time in this repository? The setup guide is [HACKAMRHEIN.md](HACKAMRHEIN.md).

Bla Bla Walk is a proposed heat-aware walking route planner for Basel. It aims to help people who are more affected by heat, and their caregivers, compare routes using shade, drinking water, cooler places, and known obstacles.

## The problem

The shortest walk may involve exposed streets, few places to rest, or inaccessible crossings. The project explores how public environmental and map data could make those tradeoffs visible when planning a walk.

## Project status

This repository contains the source audit, revised design and build plan. The agreed direction is a layered Basel map, city-wide calculated shade and two-route comparison with adjustable recommendation weights. The selected stack is TypeScript/OpenLayers plus a Python API/worker. There is no runnable application yet.

- [Design and demo proposal](docs/design.md)
- [Build tasks and acceptance checks](docs/plan.md)
- [Recorded decisions](docs/decisions.md)
- [Team collaboration guide](TEAMWORK.md)
- [Original meeting notes](notes/261002-001_Meeting_Heat-_and_Safety-Aware_Routing_Map_App-Summary.md) (historical source; see the design and plan for current proposals)

## How to run it

Run and test commands will be added and verified when the foundation task creates the application. For participant setup, use [HACKAMRHEIN.md](HACKAMRHEIN.md).

## Data sources

See [docs/SOURCES.md](docs/SOURCES.md).

## Limits

Official metadata, licences and small data samples have been inspected; integration, route validation and shade accuracy/performance remain untested. No safety claims have been validated. This is a planning-stage prototype, not a navigation or emergency service. Proposed scope, unknowns, and demo fallback are documented in the [design brief](docs/design.md).

## Team

Project roles are not assigned yet. Assign contributors by GitHub username in the [build plan](docs/plan.md).
