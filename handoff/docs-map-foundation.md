# Map-first foundation and source audit

Status: in progress

## Goal
Improve the design and plan around a Basel map with prioritised data layers, current observations and defensible approximations, before application code.

## State
Branch: docs/design. Source audit saved in docs/SOURCES.md; design and plan are revised drafts with a map foundation followed by geometry, time-dependent shade and route metrics. No implementation or PR yet. Documentation checkpoint is being saved; scope/stack remain draft where marked. The team chose two-route comparison and requested current-time shade. The team confirmed shade across all Basel; administrative boundary and implementation approach remain pending.

## Done
- Official metadata and current small samples checked for temperature 100009; station metadata 100082 also checked (both CC BY 4.0).
- IWB fountains 100008 restrict commercial use. The team explicitly authorised their inclusion for this noncommercial prototype on 2026-10-03. Preserve IWB attribution and restriction; exclude photos until rights checked. OSM water remains an optional alternative, not yet fetched.
- Found trees 100052 explicitly list CC BY 4.0 + OpenStreetMap, with a linked notice still to inspect.
- WMS advertises KL_HumanbioklimaSituation and separate 2030 projection; numeric access, render and dataset-specific licence remain unverified.
- WMTS advertises Basel basemaps; VSBS STAC lists CC-BY-4.0, exact tile mapping/test remains.
- MeteoSwiss CC BY 4.0 and hourly local forecasts documented; downloadable Basel subset remains to verify.

## Next
- City-wide coverage is agreed. Pin the exact boundary and confirm one concrete domain pitfall and the walking example.
- Present two or three approaches, agree map-first scope and stack (Leptos is a participant suggestion, not yet a team decision).
- Review the revised design/plan with the team and settle stack. Source STAC queries returned 2023 surface and 2019 terrain examples; exact tile selection and raster tests remain.
- Complete layer admission checks, then record decisions, run doc and privacy checks, commit and open a PR. Ask before merging.

## Resume prompt
Continue hack-brainstorm on docs/design. Read docs/SOURCES.md and this handoff; finish agreed map-first design and task plan without application code. Keep live temperature, historical PET, forecasts and approximations distinct. Prefer unrestricted open data; dataset 100008 is explicitly accepted for noncommercial use with attribution and its restriction preserved.
