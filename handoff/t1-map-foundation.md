# T1: Small map foundation

Status: done · Updated: 2026-10-03 · Branch: feat/t1-map-foundation · Owner: Slot D / @Derriick

## Goal
Meet T1's acceptance check in [the plan](../docs/plan.md): a runnable Basel basemap, two labelled fixture layers, provenance and missing/stale states, and a canonical Python contract with generated browser types.

## State
Branch: feat/t1-map-foundation; PR #14. T1's foundation acceptance check is complete, including setup in an isolated fresh copy. The app runs on one FastAPI server at port 8000 with a real Basel basemap and two labelled fixture layers. The user requested no JavaScript package manager: native .js modules replace the planned Vite/.ts runtime, and Python downloads/verifies pinned standalone browser distributions. Generated client declarations/schema are complete. All 15 API/model/browser checks passed both locally and in the fresh copy; real Chromium loaded nine provider tiles with no page errors. Publish this checkpoint for teammate review; merge requires explicit approval.

## Done
- Read shared launcher, profile, design, source audit and ownership paths.
- Verified executable privacy hooks and created the task branch.
- Checked the WMTS capabilities, VSBS CC-BY-4.0 collection metadata and one real tile (14/5725/8537).
- Wrote canonical models, fixture endpoint, generation script, client runtime validation and contract checks.
- Wrote layer toggles, keyboard feature inspection, provenance panel and explicit API/tile failures.
- Installed Python dependencies in a local .venv and pinned direct/transitive versions; browser assets and licence notices have a checksum manifest.
- Generated TypeScript declarations and validation schema from canonical Python models; no JavaScript build is required.
- Applied T3's civic palette, shared theme roles and touch-sized controls.
- Passed 15 checks covering contracts, generation drift, static serving, browser interactions, missing/stale states, API recovery and narrow-screen layout. Real browser loaded nine Basel tiles with no page errors.
- Python lint and browser formatting passed. README now documents the one-server setup.
- Fresh-copy setup passed with a new .venv and empty asset cache. Theme text/graphic contrast checks passed. Basel attribution is always visible.
- Integrated main at e547346: Git merged without manual conflicts, preserving T3's style guide, future-feature documentation and Windows hook fixes.
- Integrated main at a224011 with T0's source/geometry audit and T2's routing rules; resolved the design status conflict by keeping the completed T2 references and the runnable T1 foundation. Preserved the Python-only setup and all decision lines.

## Next
1. Review PR #14 and replace its WIP title/body with the completed implementation summary.
2. Merge only after teammate review and explicit approval for this PR.
3. Start downstream tasks from merged main using the owned paths below.

## PR summary
Suggested title: T1: runnable Basel map and fixture API without a JavaScript package manager.

FastAPI serves the browser map and fixture API from one origin. Two labelled fixture layers expose source attribution/times and stale/missing/unknown evidence. Includes generated client declarations/schema from canonical Python models, the T3 civic theme, checksum-pinned browser assets, Python requirements, verified startup instructions and 15 passing checks. Live observations, geometry/shade and route comparison remain downstream tasks.

## Limits
Browser checks require installed Chromium (or CHROMIUM_PATH); they explicitly skip without it. Verification used Python 3.14 and system Chromium on Linux. Basemap tiles require internet; the overlays are synthetic. The current Starlette TestClient emits a deprecation warning with httpx, but all checks pass. No geometry datasets, shade algorithm, routing scores or live adapters are implemented in T1.

## Ownership for consumers
Follow [ROADMAP.md](../ROADMAP.md) for owned adapter, geometry, route, evaluation and screen paths. Slot D owns foundation setup and the canonical contract during T1; after T1 merges, additive model changes belong to the feature task and must regenerate src/interfaces.ts and browser schemas and append a decision. Slot F owns API integration after foundation. T3's guide is applied. Plan .ts runtime paths now map to .js modules; replace planned client-runner tests with Python-driven browser checks. Do not reintroduce a JavaScript package manager. T1 introduces backend/bla_bla_walk/demo_fixture.py so Slot A's later fixture files stay disjoint.

## Resume prompt
Continue T1 on feat/t1-map-foundation. Read this handoff, TASK_START.md and T1 in docs/plan.md; start at Next and respect the roadmap ownership.
