# Revised build plan: layered map, shade, two routes

Based on [design](design.md). Draft: the team confirmed two-route comparison and current-time shade; city-wide Basel shade coverage is also confirmed; TypeScript/OpenLayers + Python API/worker is selected; exact boundary and rule assumptions remain pending. No application task has started. Owners are unassigned; agree them by GitHub username. Paths below are planned and will be created in the named tasks. Task state belongs in handoff files.

## M1: a map runs early; real layers replace fixtures independently

### Chunk A — parallel preparation (disjoint files)

#### T0 Finish layer admission and city-wide shade feasibility
Owner: unassigned
Needs: nothing
Files: docs/SOURCES.md, data/source-manifest.json, data/tile-inventory.json
Done when: one basemap request and representative licensed raster downloads succeed; a pinned Basel boundary and full surface/terrain tile inventory record versions, units, NoData, terms and surrounding occluder coverage. Include urban centre, vegetation, tall-building and border samples. Identify mismatched surveys, missing tiles, cross-border gaps and service constraints. Measure sample processing cost and estimate full-city storage/workload; define an acceptance latency and memory budget before building the full-city processing pipeline.
Notes: existing audit is a starting point, not completion. Accept IWB only within agreed noncommercial terms, omit photos. Tree licence notice is inspected; verify feature access. PET and forecasts are optional; they do not block the core map.

For construction obstacles, inspect dataset 100335 for usable geometry, dates, closure semantics, update frequency and coverage. A worksite is blocked only when authoritative data confirms it; otherwise display a caution or unknown.

#### T2 Agree one walk and comparison rules
Owner: unassigned
Needs: nothing
Files: docs/routing-rules.md, data/scenarios.json (proposed)
Done when: the team selects one demo area/start/destination, explains the current workaround and one domain pitfall, and approves examples for shade-vs-distance, water access, blocked segments, and unknown data. Specify walking-speed/stop assumptions, acceptable detours, metrics and denominator rules. Recommend an eligible route using adjustable preference weights while preserving side-by-side metrics and manual choice. Agree criteria, fixed normalization ranges, default weights and unknown/stale completeness rules; constraints stay outside weights. Include ties, all-zero weights and examples where changing weights changes the winner. Do not invent health thresholds or shade cooling degrees.

#### T3 Define the map and comparison screen
Owner: unassigned
Needs: nothing
Files: docs/style-guide.md (proposed)
Done when: a reviewable screen includes layer toggles, readable legends, provenance/times, Now/departure time, two route cards, coverage boundary and stale/unknown states; keyboard and non-colour-only explanations are specified.

### Chunk B — foundation (can begin alongside preparation)

#### T1 Build the smallest map foundation
Owner: unassigned
Needs: nothing (stack decision is recorded; verify the basemap endpoint within T1)
Files: README.md, docs/decisions.md, package.json, package-lock.json, vite.config.ts, index.html, src/main.ts, src/map.ts, src/theme.css, src/interfaces.ts (generated), backend/pyproject.toml, backend/requirements.txt, backend/bla_bla_walk/main.py, backend/bla_bla_walk/interfaces.py (canonical), backend/tests/test_contracts.py, src/contract.test.ts
Done when: a fresh checkout starts with documented commands, displays a real Basel basemap, toggles two labelled fixture layers, and shows feature provenance and missing/stale states. One shared contract supports later observations, shade and routes; consumers have explicit owned paths before parallel work begins.
Notes: chosen stack is TypeScript/OpenLayers with Vite and a Python FastAPI API/worker. Keep Python model definitions canonical and generate rather than separately author client types; actual model changes require a decision line. Use npm and a lockfile; propose pixi for reproducible Python setup or use a project virtual environment with pinned requirements. Do not install globally. Record actual interface decisions in the same commit. Fixtures must not masquerade as live data. Adopt T3 styling when available.

## M2: real layers, calculated shade and route alternatives

### Chunk C — parallel after T1 (T0/T2 inputs as listed)

#### T4 Connect current observations and fountains
Owner: unassigned
Needs: T1, relevant T0 source admission
Files: backend/bla_bla_walk/adapters/temperature.py, backend/bla_bla_walk/adapters/fountains.py, backend/tests/test_observations.py, data/fixtures/observations.json, data/fixtures/fountains.json
Done when: recent values join stations by ID, each point displays observation age, IWB fountains retain type/unknown and attribution, and failed requests retain a visibly stale last-good snapshot. Fetch latest per station, bound responses and follow source cadence.

#### T8 Prepare reusable surface/terrain geometry
Owner: unassigned
Needs: T1, T0 city boundary and inventory
Files: backend/bla_bla_walk/geometry.py, backend/tests/test_geometry.py, data/geometry/ (local generated rasters), data/fixtures/geometry-metadata.json
Done when: every tile intersecting the city boundary is prepared or has an explicitly documented data gap; geometry renders aligned at centre and boundary reference points. Include buffered occluders, versioned geometry, coordinate/vertical system, resolution and NoData. Test seams, survey mismatch, border gaps and bridges. Document resumable tile preparation and storage/memory budgets; subdivide ingestion into separately verified batches if needed.

#### T9 Provide two checked walking alternatives
Owner: unassigned
Needs: T1, T2
Files: backend/bla_bla_walk/adapters/routes.py, backend/tests/test_routes.py, data/routes/demo.geojson
Done when: two routes connect the agreed endpoints using licensed, checked walking geometry, with distance/duration and available access restrictions. Store provenance and snapshot date. Routes outside calculation coverage are marked unsupported.

### Chunk D — shade after prepared geometry

#### T10 Calculate and serve time-dependent shade
Owner: unassigned
Needs: T8
Files: backend/bla_bla_walk/shade.py, backend/bla_bla_walk/shade_cache.py, backend/tests/test_shade.py
Done when: current/selected timestamps produce direct-sun shadow masks for requested viewports and route corridors anywhere within Basel with requested/effective time and geometry version. Simple known-object cases verify direction/length, and spot checks compare with an independent reference. Measure cold/warm-cache latency, concurrency and tile-seam consistency across representative city views; test low sun/night, missing cells, occluder boundaries and canopy receivers. Unsupported cells stay unknown.
Notes: sun geometry changes with time; surveyed geometry does not. Benchmark five-minute buckets and lazy tile/corridor calculation before adopting them; version cache keys by geometry, resolution and effective time. New requests must not wait for a full-city recomputation. Do not use relief hillshade or tree buffers as actual walking shade.

### Chunk E — route metrics after shade and routes

#### T5 Compare routes over the walk
Owner: unassigned
Needs: T10, T9, T2
Files: backend/bla_bla_walk/evaluation.py, config/routing-rules.json, backend/tests/test_evaluation.py
Done when: approved examples give shaded/unshaded/unknown metres and explicit percentages, evaluating at departure plus cumulative walking time. Present distance, estimated duration, shade, exposed/unknown sections and fountains side by side; show a recommended winner with editable weights and explain each score contribution; allow manual choice. Unknown coverage cannot gain score by appearing cooler, and known blocked segments cannot be made eligible by weights. Handle ties, all-zero weights and insufficient evidence. Weight changes rescore cached metrics without repeating shade calculations. Keep unknown/blocked handling explicit. A change in departure time can change shade results without altering recorded sensor observations.

## M3: complete journey and repeatable demonstration

### Chunk F — in order

#### T6 Connect and verify the journey
Owner: unassigned
Needs: T4, T5, T3
Files: src/map.ts, src/main.ts, src/comparison.ts, src/theme.css, backend/bla_bla_walk/main.py, src/journey.test.ts, README.md
Done when: narrow-screen and keyboard users toggle layers, inspect freshness, compare two routes and change time. Pan and compare across the city; test source failure, calculation failure, tile seams, city-edge unknowns and outside-coverage behaviour; show effective time and route explanation without implying measured cooling.

#### T7 Prepare the three-minute demo and fallback
Owner: unassigned
Needs: T6
Files: docs/demo.md; media kept locally
Done when: the presenter shows map layers, two routes and changing shade, explains source licences/approximations, and repeats the story with a dated saved scenario offline. Saved output never appears as a successful live calculation.
