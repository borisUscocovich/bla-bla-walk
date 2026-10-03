# Bla Bla Walk

Track: Social impact · Updated: 2026-10-03
Status: agreed direction and stack; domain defaults, demo endpoints and performance settings remain implementation prerequisites. No application exists yet.

## Problem
People affected by heat, and caregivers planning on their behalf, need to understand shade, drinking water and walking effort together. A short route can leave someone exposed; a shaded detour may be impractical. T2 must confirm the current workaround and one concrete domain pitfall with the team before setting recommendation defaults.

## What we build
A mobile-friendly Basel map with independent data layers, city-wide calculated shade, and two walking alternatives. Recommend a route using adjustable weights, explain the tradeoffs, and allow the user to choose either eligible route.

### Demo flow (three minutes)
1. Open Basel, toggle sensor temperatures, fountains and calculated shade. Inspect a feature's source, timestamp and uncertainty.
2. Select the agreed start/destination pair. Compare two checked routes: walking time/distance, shaded, exposed and unknown lengths, and nearby drinking-water opportunities.
3. Choose Now or another departure time. Recalculate shade along the walk; adjust preference weights and see the recommendation and explanation change.
4. Disconnect a source: show retained observations as stale and saved shade results with their original effective time.

Coverage includes all Basel, rather than one neighbourhood. Pin the administrative boundary in T0; default interpretation is Basel city. Inventory city-wide geometry plus surrounding shadow-casting objects. Calculate requested map tiles and route corridors on demand. The first demo uses two checked walking alternatives; arbitrary-endpoint route generation is a later decision.

## Data
The [source register](SOURCES.md) is authoritative for endpoints, licensing, attribution, evidence and admission checks.

| Input | Source | Meaning / admission |
|---|---|---|
| Air temperature and stations | Basel 100009 / 100082 | CC BY 4.0; timestamped raw observations |
| Fountains | IWB / Basel 100008 | Noncommercial reuse with attribution; preserve drinking-type unknowns |
| Surface and terrain heights | swissSURFACE3D Raster / swissALTI3D | Swisstopo OGD terms; surveyed geometry for calculated shadows |
| Tree context | Basel 100052 | Canton CC BY terms and OSM incorporation notice; locations alone do not establish shade |
| Basemap and walking alternatives | Basel map service / OSM candidate | Verify basemap mapping/access; OSM attribution and database obligations apply |
| Optional context | Historical PET, MeteoSwiss forecasts, construction feed | Separate scenario, forecast and caution states; source admission remains required |

## How it is built
Chosen stack: TypeScript + OpenLayers browser UI and a Python API/worker. Use Vite, FastAPI and Rasterio as foundation tools, with versions/licences pinned in T1. Rasterio provides chunked raster access; the shadow algorithm still needs validation. Keep geometry processing and versioned caches outside the browser. Hosting must support a worker and persistent geometry storage.

Browser code lives under src; adapters, geometry, shade and evaluation under backend/bla_bla_walk; domain values under config; licensed manifests under data. Large rasters and caches stay outside Git. T1 defines one authored Python interface, generates browser types, and checks cross-language fixtures. Actual interface edits include decision lines in the same commit. File ownership lives in the [plan](plan.md).

Build the basemap and a fixture API round trip first; add verified observations, geometry and routes independently. Use LV95 metres for geometry, checked coordinate conversion for display, terrain-level receivers and buffered surface heights for shadows. Preserve unknown cells and off-screen occluders. Evaluate shade at departure plus cumulative walking time. Cache versioned results; five-minute buckets require benchmarking. Validate canopy receivers, low sun, tile seams, bridges and borders.

## Recommendation rules
Expose preferences for shade/exposure, walking duration and water access. T2 defines measurable criteria, fixed normalization ranges and defaults; raw minutes and percentages cannot simply be added. Show raw metrics and each criterion's score contribution. Known access/blocking constraints remain outside weights. Define evidence-completeness rules; missing shade or stale fountain status must not improve a score. Handle ties, all-zero weights and insufficient evidence. Weight changes rescore existing metrics without repeating shadow calculations.

## Out of scope and approximations
No accounts, health profiles or stored location histories. Current-time shade is calculated from surveyed geometry, not observed cloud shadows or live canopy measurements. Foliage and gaps are approximate; unsupported areas stay unknown. Do not turn shade fraction into temperature/PET degrees. Historical PET remains a summer 14:00 scenario. City-wide shade is in scope; alerts, volunteer matching and phone service remain extensions.

## Team and domain input
Owners remain unassigned until contributors choose tasks by GitHub username. Domain examples determine walking constraints, acceptable detours and water interpretation. Explore the look together with hack-design before or after the first map works.

## Risks and fallback
Preflight city-wide tile coverage, border occluders, survey alignment, memory and latency before promising current-time performance. Keep licensed geometry snapshots and dated calculation outputs. If a source/calculation fails, show a labelled saved scenario without a Now claim. Missing data must not become sunlit, cool or passable by default.
