# Bla Bla Walk

Track: Social impact · Updated: 2026-10-03
Status: revised design draft. The team selected two-route comparison with time-dependent shade and accepted IWB fountains for noncommercial use. City-wide shade coverage and a recommended route with user-adjustable weights are confirmed. The implementation stack is selected. Demo endpoints, domain rules and performance settings remain T0/T2 build prerequisites.

## Problem
People affected by heat, and caregivers planning on their behalf, need to understand shade, water and walking distance together. A short route can leave someone exposed; a longer shaded route may still be impractical. The current workaround and a concrete domain pitfall must be confirmed in T2; those examples set acceptable detours and recommendation defaults.

## What we build
A mobile-friendly Basel map with independently selectable data layers and two walking routes compared side by side. Show walking time/distance, shade at the time of the walk, exposed and unknown sections, and fountains; recommend a route using user-adjustable weights while keeping every underlying metric visible. The user may choose either eligible route.

### Demo flow (three minutes)
1. Open Basel, toggle temperature observations, fountains and computed shade; inspect a feature's source, age and uncertainty.
2. Select one agreed start/destination pair and see two real walking alternatives, with distance, estimated duration, nearby water, and shaded/unshaded/unknown metres.
3. Choose Now or change departure time. Recalculate shade and route comparison; change preference weights and see the winner and its explanation update. Explain the effective time, geometry and tradeoffs without promising a safest route.
4. Disconnect a source: retained data is visibly stale; a saved shade scenario is labelled with its original time.

Confirmed coverage: all Basel, rather than a single neighbourhood. Default interpretation is Basel city; the exact administrative boundary is to be pinned in the source manifest. Prepare a city-wide surface/terrain tile inventory plus surrounding shadow-casting geometry. Calculate visible tiles and route corridors on demand instead of recomputing the entire city on every time change. This execution approach is proposed and must pass performance checks. The initial demonstration still uses two checked walking alternatives; arbitrary endpoint route generation remains a separate decision.

## Data
The [source register](SOURCES.md) holds exact endpoints, verified licences, access status and remaining checks.

| Input | Source | Terms and meaning |
|---|---|---|
| Air-temperature observations and stations | Basel 100009 and 100082 | CC BY 4.0; raw timestamped points, not a continuous heat-risk map |
| Fountains | IWB via Basel 100008 | Noncommercial reuse with IWB attribution; commercial use requires permission; preserve drinking/type unknowns |
| Surface and terrain heights | swisstopo swissSURFACE3D Raster + swissALTI3D | OGD terms, © swisstopo; static surveyed geometry for calculated time-dependent shade |
| Tree context | Basel 100052 | CC BY 4.0 + OpenStreetMap notice pending review; points do not establish shade |
| Basemap and walking alternatives | Basel map service; checked OSM walking geometry candidate | Exact basemap mapping/access still to verify; OSM ODbL with attribution and applicable database obligations |
| Optional heat/weather context | Historical Basel PET; MeteoSwiss point forecasts | PET admission checks remain; MeteoSwiss CC BY 4.0. Keep scenario, prediction and observation separate |

## How it is built
Separate the map screen, source adapters, reusable data storage/cache, shadow calculation and route evaluation. The first foundation starts with a real basemap and small source-labelled fixtures; it does not wait for route scoring or a complete shadow engine. Then independently replace fixtures with checked data and attach calculations through one shared interface.

Proposed interface concepts: layer provenance and licence, geometry/coordinate system, units, observed time, forecast validity, scenario/effective calculation time, retrieval time, geometry version, coverage and unknown states; route geometry and per-segment arrival time. These are design concepts, not an implemented contract. Record any actual interface change in the same commit as its decision line.

Process geometry in LV95 metres; display geographic features with explicit conversion and checked alignment. A proposed shadow calculation tests direct sunlight from terrain-level receivers against surface heights. It must include off-screen occluders, mask missing coverage and account for solar-angle conventions. Sample routes at time of arrival along the walk; show unknown length separately. Test canopy, low sun and bridges/underpasses. Store geometry once and cache timestamped calculation outputs; five-minute buckets are a proposal to benchmark.

Chosen stack: TypeScript + OpenLayers for the browser UI and a Python API/worker for source ingestion and shade calculations. Use a small Vite app and FastAPI service; pin packages and check their licences in T1. Rasterio supplies chunked raster access, not the shadow algorithm. Process/cache geometry outside the browser; benchmark computation before promising latency. Deployment needs a running worker and persistent geometry cache.

Folder responsibilities: browser/map controls under src; server adapters, geometry, shade and evaluation under backend/bla_bla_walk; domain settings under config; versioned licensed data manifests under data. Keep large rasters and generated caches out of Git. The Python interface module is the single authored contract; generate the browser types and verify cross-language fixtures against it in T1. Detailed paths and file ownership live in the plan.

## Recommendation rules (draft)

Expose configurable preferences for shade/exposure, walking duration and water access. Define measurable criteria and fixed documented normalization ranges before selecting defaults; do not sum minutes and percentages directly or change normalization whenever a route candidate changes. Preserve raw metrics and each criterion's score contribution. Keep known blocking/access constraints outside preference weights. Do not reward missing shade or stale water status; define a completeness rule before issuing a winner. Handle ties, all-zero weights and insufficient evidence explicitly. Weight changes rescore existing route metrics without refetching geometry or rerunning shadows. Tests must include a deliberate winner change and a case with unknown coverage.

## Out of scope and approximations
No accounts, health profiles or stored location histories. No live geometry or observed cloud shadows. Canopy is an approximate occluding surface with uncertain foliage and gaps. No conversion from shade fraction to temperature/PET degrees. Historical PET stays a summer 14:00 scenario; no extra guessed shade cooling is applied. Arbitrary-endpoint route generation, alerts, volunteer matching and phone service remain extensions. City-wide shade coverage is in scope.

## Who does what
Owners remain unassigned until contributors choose tasks by GitHub username. Domain review owns walking constraints, acceptable detours, drinking-water interpretation and the concrete examples that route explanations must satisfy. Visual style can be explored together with hack-design before or after the first map works.

## Risks and fallback
Check complete city tile coverage, cross-border occluders, raster access, memory/calculate time, geometric alignment and current walking-network validity early. Keep a licensed bounded snapshot and computed masks for an explicitly dated scenario. If current calculations fail, show that saved scenario without a Now label. Unsupported geography stays unknown; map/source failure must not change unknown into low exposure.
