# T1: Small map foundation

Status: in progress · Updated: 2026-10-03 · Branch: feat/t1-map-foundation · Owner: Slot D / @Derriick

## Goal
Meet T1's acceptance check in [the plan](../docs/plan.md): a runnable Basel basemap, two labelled fixture layers, provenance and missing/stale states, and a canonical Python contract with generated browser types.

## State
Branch: feat/t1-map-foundation. The user requested committing and pushing all task changes and opening a prefilled PR creation page. This is a WIP checkpoint, not completed T1. The API, neutral theme and map screen are written, but have not been run. Dependency manifests are incomplete; generated client files are absent. The official VS_Vektorstadtplan_grau WMTS returned a valid Basel PNG with Access-Control-Allow-Origin: *. Software installation approval and Python package-manager choice remain pending.

## Done
- Read shared launcher, profile, design, source audit and ownership paths.
- Verified executable privacy hooks and created the task branch.
- Checked the WMTS capabilities, VSBS CC-BY-4.0 collection metadata and one real tile (14/5725/8537).
- Wrote canonical models, fixture endpoint, generation script, client runtime validation and contract checks.
- Wrote layer toggles, keyboard feature inspection, provenance panel and explicit API/tile failures. Generated files and dependency pins are still pending.
- All authored Python files passed syntax parsing. Application startup, formatting, lint and contract tests have not run because project dependencies are not installed.
- README describes the incomplete startup state; recorded the initial canonical-contract decision.

## Next
1. Obtain the pending installation answer, install project dependencies and pin backend/requirements.txt; use npm's package manager to record exact versions and generate its lockfile.
2. Generate client types/schema and fix any compiler or contract failures.
3. Verify documented startup, contracts, browser toggles, provenance and failure states.
4. Record the actual package-manager decision, update README with verified commands, and publish a completed checkpoint to this branch. Create the WIP PR from the prepared browser page if it has not been submitted. Merge requires explicit approval and completion of T1's acceptance check.

## Ownership for consumers
Follow [ROADMAP.md](../ROADMAP.md) for owned adapter, geometry, route, evaluation and screen paths. Slot D owns foundation setup and the canonical contract during T1; after T1 merges, additive model changes belong to the feature task and must regenerate src/interfaces.ts and append a decision. Slot F owns API integration after foundation. T3's style guide is not available yet; foundation uses neutral theme defaults.

## Resume prompt
Continue T1 on feat/t1-map-foundation. Read this handoff, TASK_START.md and T1 in docs/plan.md; start at Next and respect the roadmap ownership.
