# Sources

Every dataset, API, notable library and AI tool used, with licence. Feeds the sources slide on Sunday.

| What | Source / URL | Licence or permission | Used for |
|---|---|---|---|
| Codex (OpenAI) | chatgpt.com/codex | Tool, AI-assisted development | Coding assistant |

## Recommended heat source: Basel-Stadt Geoportal daytime PET

Documentation checked: 2026-10-03. Recommend the Basel-Stadt Geoportal's daytime PET layer as the first demo's heat indicator, subject to verifying data access in T0. Nothing has been downloaded or integrated yet.

PET (Physiological Equivalent Temperature) estimates thermal conditions for a modelled person from air temperature, humidity, wind, and short- and long-wave radiation. Although expressed in °C, PET is not thermometer air temperature or a personalised health-risk estimate.

| Item | Finding / reference |
|---|---|
| Dataset to investigate | Stadtklima: `HumanbioklimSituation`, the daytime PET layer; keep the separate `HumanbioklimSituation_2030` projection out of the initial baseline |
| Map and catalogue | [MapBS Stadtklima](https://www.geo.bs.ch/stadtklima), [Basel-Stadt geodata catalogue](https://shop.geo.bs.ch/geodaten-katalog/) |
| Layer description | [Official Stadtklima data model, sections 6.1.12–6.1.13](https://models.geo.bs.ch/Modellbeschreibungen/KL_Stadtklima_KGDM_V1_0.pdf) |
| Method and shade evidence | [2019 climate analysis, sections 4 and 4.4](https://map.geo.bs.ch/file_proxy/KL_Stadtklima_Windstroemungsfeld/Endbericht_Basel_Klimaanalyse_Rev09_ohne_Anhang.pdf): reduced heat stress under tree canopies and from building shade in the old town |
| Scenario | Modelled clear summer weather at 14:00, not live weather or a forecast for a chosen departure time |
| Model resolution | 10 × 10 m cells, evaluated at 2 m above ground; verify the delivered layer's resolution and whether values are numeric PET or classified ranges |
| Licence and attribution | Verify the selected dataset's access and download terms. Basel-Stadt applies CC BY 4.0 to public-access geodata with a download service; attribute Kanton Basel-Stadt and retain dataset-specific notices. [Official terms](https://www.bs.ch/en/node/29871) |
| API / download discovery | [Official geoservices](https://www.bs.ch/en/node/28694). Exact service endpoint, layer identifier, downloadable format, and a numeric query or sampling method remain to be verified in T0; a rendered map alone does not establish access to PET values |

Recommendation for the demo: compare routes using this documented 14:00 PET scenario, alongside distance, water, and known obstacles. Shade effects are already represented in PET, so do not apply an additional assumed shade cooling adjustment to those values. A separate shade overlay may explain conditions, but is not evidence for subtracting temperature or PET degrees.

Keep model/scenario time, dataset publication or update time, and retrieval time distinct. Missing cells or unavailable data must remain unknown; a synthetic fallback must be visibly labelled. Do not present this historical baseline or its 2030 projection as today's conditions.

Time-specific shadow modelling with surface/building data and SunCalc is a later option if arbitrary departure times become part of the scope. It would need its own validation and would not automatically produce updated PET values. The sources below remain candidates for that extension.

## Licence-checked sources for later shade modelling

These sources allow reuse under their respective terms, including attribution and any applicable share-alike or licence-notice requirements. Licences checked 2026-10-03; nothing is downloaded or integrated yet, so exact dataset URLs and retrieval dates are still to be recorded on first use.

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
| Basel public data | Daytime PET as recommended above; fountains, cooler public spaces, and possible later sensors/tree layers | Exact datasets and endpoints, area coverage, opening hours or availability, refresh intervals, licence and attribution |
| swisstopo | Basemap and terrain context | Appropriate layers and coordinate systems; licence checked above |
| OpenStreetMap | Walking network, paths, crossings, and mapped amenities | Relevant tags and local completeness, snapshot date (licence checked above); do not assume tree locations provide measured shade |
| MeteoSwiss | Weather context | Suitable product, spatial and time resolution, update schedule, access terms, licence and attribution |
| Public transport providers (SBB; "OVA" in the notes, identity unconfirmed) | Stops and possible transit alternatives | Resolve the provider name, scope, timetable access, freshness, and reuse terms; deferred feature |
| Construction and closure information | Route obstacles | Identify an authoritative provider, spatial coverage, freshness, and licence; availability unknown |

Before using a source, record its exact URL, dataset identifier, licence or permission, required attribution, retrieval date, update time, geographic coverage, coordinate system, and transformation steps. Keep metadata with any exported sample.

Synthetic demo data must be labelled as synthetic and must not contain actual users' locations or health information. Aggregated population data and general health information were also discussed; their need for the initial demo is unconfirmed.
