# Sources

Every dataset, API, notable library and AI tool used, with licence. Feeds the sources slide on Sunday.

| What | Source / URL | Licence or permission | Used for |
|---|---|---|---|
| Codex (OpenAI) | chatgpt.com/codex | Tool, AI-assisted development | Coding assistant |

## Licence-checked sources for shade modelling

Free to use for any purpose, including commercially, as long as attribution is given. Licences checked 2026-10-03; nothing is downloaded or integrated yet, so exact dataset URLs and retrieval dates are still to be recorded on first use.

| What | Source / URL | Licence or permission | Required attribution | Intended use |
|---|---|---|---|---|
| swisstopo geodata (swissSURFACE3D, swissBUILDINGS3D, terrain) | swisstopo.admin.ch/en/faq-free-geodata | Swiss open government data (free since 2021-03-01) | "© swisstopo" | Surface model with buildings and trees for computing cast shadows |
| Basel-Stadt open geodata | data.bs.ch, shop.geo.bs.ch | CC BY 4.0, only for datasets with open access and a download service; check each dataset | Kanton Basel-Stadt | Local surface model, trees, fountains |
| OpenStreetMap | openstreetmap.org/copyright | ODbL 1.0; a published derived database must also be ODbL, rendered maps and route results need not be | "© OpenStreetMap contributors" | Walking network, building footprints |
| suncalc | github.com/mourner/suncalc | BSD-2-Clause | Keep the licence notice | Sun position for a given date, time and location |

Not included: ShadeMap (shademap.app, `leaflet-shadow-simulator`) is a proprietary service with no open-source licence; a free API key exists, but usage limits and terms make it a demo-only dependency at best.

## Candidate data from the meeting

These are investigation targets, not integrated or verified sources. Provider names are transcribed from the meeting notes; exact dataset URLs and terms must be established before ingestion or redistribution.

| Candidate | Intended use | Checks still needed |
|---|---|---|
| Basel public data | Heat maps, sensors, fountains, trees, cooler public spaces | Exact datasets and endpoints, area coverage, opening hours or availability, refresh intervals, licence and attribution |
| swisstopo | Basemap and terrain context | Appropriate layers and coordinate systems; licence checked above |
| OpenStreetMap | Walking network, paths, crossings, and mapped amenities | Relevant tags and local completeness, snapshot date (licence checked above); do not assume tree locations provide measured shade |
| MeteoSwiss | Weather context | Suitable product, spatial and time resolution, update schedule, access terms, licence and attribution |
| Public transport providers (SBB; "OVA" in the notes, identity unconfirmed) | Stops and possible transit alternatives | Resolve the provider name, scope, timetable access, freshness, and reuse terms; deferred feature |
| Construction and closure information | Route obstacles | Identify an authoritative provider, spatial coverage, freshness, and licence; availability unknown |

Before using a source, record its exact URL, dataset identifier, licence or permission, required attribution, retrieval date, update time, geographic coverage, coordinate system, and transformation steps. Keep metadata with any exported sample.

Synthetic demo data must be labelled as synthetic and must not contain actual users' locations or health information. Aggregated population data and general health information were also discussed; their need for the initial demo is unconfirmed.
