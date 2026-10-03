# Revised build plan: layered map, shade, two routes

Based on [design](design.md). Draft: the team confirmed two-route comparison and current-time shade; city-wide Basel shade coverage is also confirmed; TypeScript/OpenLayers + Python API/worker is selected; exact boundary and rule assumptions remain pending. T0, T1, T2 and T9 are complete and merged. Their original task labels remain and are crossed out below. Owners for remaining tasks are unassigned; agree them by GitHub username. Paths below are planned and will be created in the named tasks. Task state belongs in handoff files.

## M1: a map runs early; real layers replace fixtures independently

### Chunk A — parallel preparation (disjoint files)

#### ~~T0 Finish layer admission and city-wide shade feasibility~~
Owner: unassigned
Needs: nothing
Files: docs/SOURCES.md, data/source-manifest.json, data/tile-inventory.json
Done when: one basemap request and representative licensed raster downloads succeed; a pinned Basel boundary and full surface/terrain tile inventory record versions, units, NoData, terms and surrounding occluder coverage. Include urban centre, vegetation, tall-building and border samples. Identify mismatched surveys, missing tiles, cross-border gaps and service constraints. Measure sample processing cost and estimate full-city storage/workload; define an acceptance latency and memory budget before building the full-city processing pipeline.
Notes: existing audit is a starting point, not completion. Accept IWB only within agreed noncommercial terms, omit photos. Tree licence notice is inspected; verify feature access. PET and forecasts are optional; they do not block the core map.

For construction obstacles, inspect dataset 100335 for usable geometry, dates, closure semantics, update frequency and coverage. A worksite is blocked only when authoritative data confirms it; otherwise display a caution or unknown.
For optional bus and tram alternatives, check the 2026 GTFS timetable for BVB/BLT coverage, stops, access terms and usable trip times. Verify operator coverage in GTFS-RT Service Alerts; use alerts as service warnings unless they provide enough detail to route the detour. API access requires a key. Keep scheduled timetable evidence separate from live service status. Transit remains unavailable in the app until this admission succeeds.

For broader emergency notices, check Alertswiss separately from MeteoSwiss weather data. MeteoSwiss relays Alertswiss alarm-level messages through its app, but this does not confirm that its open-data feed carries the full Alertswiss stream. Verify whether a machine-readable Alertswiss feed is currently available and reusable before integration.

For rest stops, use Basel-Stadt's official cool-room list as a curated starting point. Verify current opening hours, visitor access, accessibility and any conditions; do not infer that churches or shops are open, cool or air-conditioned. Check whether the page has a reusable machine-readable feed. For outdoor stops, inspect tree-canopy coverage dataset 100357 and OpenStreetMap parks (`leisure=park`) and benches (`amenity=bench`). Verify dataset terms, freshness and local completeness; tree canopy is not a guarantee of shade at a given time, and mapped benches may lack details such as covering or accessibility. Label evidence and unknowns separately; don't call a location safe based on its category alone.



#### ~~T2 Agree one walk and comparison rules~~
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

#### ~~T1 Build the smallest map foundation~~
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

#### ~~T9 Provide two checked walking alternatives~~
Owner: unassigned
Needs: T1, T2
Files: backend/bla_bla_walk/adapters/routes.py, backend/tests/test_routes.py, data/routes/demo.geojson
Done when: two routes connect the agreed endpoints using licensed, checked walking geometry, with distance/duration and available access restrictions. Store provenance and snapshot date. Routes outside calculation coverage are marked unsupported.

#### T14 Review route modes and verify transit feasibility (proposed)
Owner: unassigned
Needs: T0 source admission follow-up; T2 routing proposal
Files: docs/routing-rules.md, docs/style-guide.md, docs/SOURCES.md, data/source-manifest.json, docs/decisions.md
Done when: the team reviews Fastest overall, More shade, manual choice and the optional five-minute detour limit. Agree mode ranking and evidence labels. Verify BVB/BLT timetable access, coverage, terms, stop and transfer data, and usable journey times. Separately verify GTFS-RT alert access, key handling, operator coverage and freshness. Decide whether evidence supports scheduled trips, live disruption status, both or neither. Record gaps explicitly. Do not start transit integration unless its required inputs are admitted.

#### T15 Provide a transit-assisted candidate (conditional)
Owner: unassigned
Needs: T1, T2, T14 admitted data; T9 for checked walking legs
Files: backend/bla_bla_walk/adapters/transit.py, backend/tests/test_transit.py, data/fixtures/transit.json
Done when: a candidate includes checked access/egress walking legs, ride/wait/transfer durations, stop access state, source provenance and a clear scheduled or live label. Waiting shade stays unknown without stop evidence. Confirmed closures and unavailable service cannot appear as usable legs. If T14 does not admit a source, record the unavailable state and leave walking comparison usable.

### Chunk D — shade after prepared geometry

#### T10 Calculate and serve time-dependent shade
Owner: unassigned
Needs: T8
Files: backend/bla_bla_walk/shade.py, backend/bla_bla_walk/shade_cache.py, backend/tests/test_shade.py
Done when: current/selected timestamps produce direct-sun shadow masks for requested viewports and route corridors anywhere within Basel with requested/effective time and geometry version. Simple known-object cases verify direction/length, and spot checks compare with an independent reference. Measure cold/warm-cache latency, concurrency and tile-seam consistency across representative city views; test low sun/night, missing cells, occluder boundaries and canopy receivers. Unsupported cells stay unknown.
Notes: sun geometry changes with time; surveyed geometry does not. Benchmark five-minute buckets and lazy tile/corridor calculation before adopting them; version cache keys by geometry, resolution and effective time. New requests must not wait for a full-city recomputation. Do not use relief hillshade or tree buffers as actual walking shade.

### Chunk E — route metrics after shade and routes

#### T5 Compare eligible trip options
Owner: unassigned
Needs: T10, T9, T2; T14/T15 only if transit sources pass admission
Files: backend/bla_bla_walk/evaluation.py, config/routing-rules.json, backend/tests/test_evaluation.py
Done when: walking candidates show shaded/unshaded/unknown metres and percentages at departure plus cumulative walking time. Where T15 is admitted, compare complete door-to-door time across walking and transit candidates, keeping walking, waiting, ride, transfer and stop time separate. Provide Fastest overall and More shade choices, preserve manual choice, and explain every recommendation. Do not score transit ride duration as walking time or infer shade for indoor/onboard segments. Unknown coverage cannot gain credit; known blocked paths cannot become eligible. Handle ties and insufficient evidence. Weight changes rescore cached metrics without repeating shade calculations.

## M3: complete journey and repeatable demonstration

### Chunk F — in order

#### T6 Connect and verify the journey
Owner: unassigned
Needs: T4, T5, T3; T15 only if transit sources pass admission
Files: src/map.ts, src/main.ts, src/comparison.ts, src/theme.css, backend/bla_bla_walk/main.py, src/journey.test.ts, README.md
Done when: narrow-screen and keyboard users toggle layers, inspect freshness, choose Fastest overall or More shade, compare eligible trip options, and change departure time. If transit is admitted, show door-to-door duration and each trip leg with scheduled/live status. Keep the five-minute detour option clear. Test source failure, calculation failure, tile seams, city-edge unknowns and outside-coverage behaviour; show effective time without implying measured cooling or overall safety.

#### T7 Prepare the three-minute demo and fallback
Owner: unassigned
Needs: T6
Files: docs/demo.md; media kept locally
Done when: the presenter shows map layers, two routes and changing shade, explains source licences/approximations, and repeats the story with a dated saved scenario offline. Saved output never appears as a successful live calculation.

## M4: people without smartphones can follow a prepared route in a transparent phone simulation

Priority: after the core web demo (M3). This milestone reuses the same checked routes and evidence as the map. It does not include live phone service, collecting real addresses or emails, or actually sending printed maps.

### Chunk G — validate human wayfinding

#### T11 Validate landmarks and barriers on a demo route
Owner: unassigned
Needs: T7, T9
Files: docs/future-features.md, data/fixtures/call-scenarios.json
Done when: a short walk-along or sketch-map check on a prepared route records which global and local landmarks people recognize, confusing decision points, and reported barriers. Each cue/barrier has evidence, a check date and a known/unknown state. Findings consider different levels of route familiarity and omit participant names and contact details.

### Chunk H — agree and build the spoken directions (in order)

#### T12 Agree the spoken instruction format
Owner: unassigned
Needs: T11
Files: docs/future-features.md
Done when: the team agrees a short spoken step format with one maneuver at a time, a broad orientation cue when verified, a nearby landmark, a street-name fallback when available, and plain wording for missing or uncertain information. Examples cover a known landmark, an unfamiliar landmark and an unknown barrier. Do not promise safety or passability without evidence.

#### T13 Generate route-backed spoken steps in the Python backend
Owner: unassigned
Needs: T12, T5, T9
Files: backend/bla_bla_walk/interfaces.py, backend/bla_bla_walk/instructions.py, backend/tests/test_instructions.py, backend/export_contract.py, src/interfaces.ts, src/snapshot.schema.json, docs/decisions.md
Done when: the backend produces one structured spoken step per maneuver from the same route and evidence used by the map, carrying cue/source freshness and explicit unknowns. Use the agreed format and validated landmarks only. Define the shared contract through hack-interface; regenerate browser types/schema and add its decision line in the same change.

#### T14 Build the simulated call and map-request flow
Owner: unassigned
Needs: T13, T6, T7
Files: src/call-demo.js, src/main.js, src/theme.css, backend/tests/test_browser.py, docs/demo.md
Done when: a person chooses a prepared Basel trip, hears one instruction at a time, can repeat or slow it down, and can follow an accessible transcript. If browser speech is unavailable, the simulation still shows the scripted spoken lines. The caller can choose postal delivery or a neighbour's email and sees a generic simulated confirmation; the demo never asks for real contact details or sends anything. Missing and unverified route information remains explicit.

## M5: people can share timely map reports

This remains after the phone-access prototype in the team's priority order. `Needs` below lists actual technical dependencies.

### Chunk I — define the report rules

#### T15 Define shared-report rules and storage
Owner: unassigned
Needs: T1, T2
Files: docs/reporting-rules.md, docs/decisions.md
Done when: the team approves report categories, optional note limits, anonymous-by-default handling, confirmation/resolution and flagging behaviour, expiry, moderation, rate limits, and a persistent-storage approach. Examples cover a broken fountain, a closed place and a blocked path. Rules show report age and uncertainty without calling places safe.

### Chunk J — build the API and map experience (in order)

#### T16 Store and serve shared reports
Owner: unassigned
Needs: T15, T1
Files: backend/bla_bla_walk/reporting.py, backend/bla_bla_walk/main.py, backend/tests/test_reporting.py
Done when: reports persist across reloads, validate their category and location, receive server timestamps, expire by the agreed rule, and support confirmation, resolution and flagging. Apply the agreed rate limits; reporter identity is not collected by default.

#### T17 Add reports to the map
Owner: unassigned
Needs: T16, T6
Files: src/map.js, src/main.js, src/reporting.js, backend/tests/test_browser.py
Done when: a person can submit a map report, see current reports with age and status, confirm or resolve one, and flag a questionable report. Closed or broken items are visibly reports, not verified safe-stop data.
## Not scheduled yet

Live phone numbers/calls, actual postal or email map delivery, and volunteer accompaniment stay outside this plan. Re-plan them after the scripted call has been tried with users and the team has agreed on cost, privacy, reliability, safeguarding, and operating responsibilities.
