# Sources

Every dataset, API, notable library and AI tool used, with licence. Feeds the sources slide on Sunday.

| What | Source / URL | Licence or permission | Used for |
|---|---|---|---|
| Codex (OpenAI) | chatgpt.com/codex | Tool, AI-assisted development | Coding assistant |

## Candidate data from the meeting

These are investigation targets, not integrated or verified sources. Provider names are transcribed from the meeting notes; exact dataset URLs and terms must be established before ingestion or redistribution.

| Candidate | Intended use | Checks still needed |
|---|---|---|
| Basel public data | Heat maps, sensors, fountains, trees, cooler public spaces | Exact datasets and endpoints, area coverage, opening hours or availability, refresh intervals, licence and attribution |
| swisstopo | Basemap and terrain context | Appropriate layers, coordinate systems, access terms, licence and attribution |
| OpenStreetMap | Walking network, paths, crossings, and mapped amenities | Relevant tags and local completeness, snapshot date, permitted use and attribution; do not assume tree locations provide measured shade |
| MeteoSwiss | Weather context | Suitable product, spatial and time resolution, update schedule, access terms, licence and attribution |
| Public transport providers (SBB; "OVA" in the notes, identity unconfirmed) | Stops and possible transit alternatives | Resolve the provider name, scope, timetable access, freshness, and reuse terms; deferred feature |
| Construction and closure information | Route obstacles | Identify an authoritative provider, spatial coverage, freshness, and licence; availability unknown |

Before using a source, record its exact URL, dataset identifier, licence or permission, required attribution, retrieval date, update time, geographic coverage, coordinate system, and transformation steps. Keep metadata with any exported sample.

Synthetic demo data must be labelled as synthetic and must not contain actual users' locations or health information. Aggregated population data and general health information were also discussed; their need for the initial demo is unconfirmed.
