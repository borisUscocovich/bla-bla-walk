# Sources

Every dataset, API, notable library and AI tool used, with licence. Feeds the sources slide on Sunday.

| What | Source / URL | Licence or permission | Used for |
|---|---|---|---|
| Codex (OpenAI) | chatgpt.com/codex | Tool, AI-assisted development | Coding assistant |

## Prioritized project resources

Use the sources in this list first whenever they fulfil the project's needs. Prefer these listed sources over alternatives for the same need, while checking that the specific data is suitable, current enough, accessible, and reusable for the intended use. For the first-demo heat indicator, Basel-Stadt Geoportal daytime PET remains the recommended source, subject to the checks in the section below. A source being listed here does not by itself verify a dataset's licence, quality, or availability; record those details before using or redistributing data.

| Title | Description | URL | Licence or permission / notes |
|---|---|---|---|
| Heat and health Basel-Stadt | Cool public rooms, the heat hotline, first aid and heat advice in 14 languages. | [bs.ch — Heat and health](https://www.bs.ch/themen/gesundheit/gesundheitsfoerderung/praeventionsangebote/hitze) | Official public guidance; check content and service availability before presenting it. |
| Heat action plan Basel-Stadt | What the canton does before and during a heatwave, and what happens at each warning level. | [Basel-Stadt heat action plan (PDF)](https://media.bs.ch/original_file/cf38be8695e1cb3e0aefcaf832b4b89c65863658/hitzemassnahmenplan-basel-stadt.pdf) | Official publication; check reuse and attribution terms before reproducing content. |
| Climate maps on MapBS | Modelled heat, night cooling and felt temperature across the canton. | [MapBS Stadtklima](https://www.geo.bs.ch/stadtklima) | Map/catalogue reference; verify whether underlying data can be accessed and reused. |
| City temperature sensors | Hourly street-level air temperature from sensors across Basel, raw values. | [data.bs.ch dataset 100009](https://data.bs.ch/explore/dataset/100009/) | Verify dataset-specific licence, sensor coverage, units, quality and update frequency. |
| Public fountains | Locations of drinking, bathing and decorative fountains in Basel. | [data.bs.ch dataset 100008](https://data.bs.ch/explore/dataset/100008/) | Verify dataset-specific licence, fountain type, access and availability information. |
| Construction sites | Current and upcoming construction works on public land, published by the Basel-Stadt Civil Engineering Office. | [data.bs.ch dataset 100335 — Baustellen](https://data.bs.ch/explore/dataset/100335/) · [Tiefbauamt construction map](https://www.bs.ch/bvd/tiefbauamt/baustellen) | Machine-readable candidate for identifying route obstacles. Verify geometry, active dates, closure status, update frequency, coverage and reuse terms; the listing alone does not confirm that a road is impassable. |
| Basel public transport | Swiss GTFS timetable data includes BVB and BLT routes, stops and schedules; GTFS-RT Service Alerts can report disruptions and detours for connected operators. | [Timetable 2026 (GTFS)](https://data.opentransportdata.swiss/en/dataset/timetable-2026-gtfs2020) · [GTFS-RT Service Alerts](https://data.opentransportdata.swiss/en/dataset/gtfs-sa) · [BVB traffic information](https://www.bvb.ch/de/aktuelle-informationen/verkehrsinformationen/) | Candidate for nearby stop and service alternatives. The timetable is static. Alerts require an API key, allow up to two requests per minute, and cover connected operators only. Verify BVB/BLT alert coverage and whether detour details include usable geometry; alerts may provide text only. Check reuse terms. |
| Tree register | Position and species of every city-maintained tree, a starting point for shade. | [data.bs.ch dataset 100052](https://data.bs.ch/explore/dataset/100052/) | Verify dataset-specific licence and coverage; tree locations do not establish measured shade. |
| Population by age and quarter | Residents by age, sex and nationality for each quarter, updated yearly. | [data.bs.ch dataset 100128](https://data.bs.ch/explore/dataset/100128/) | Verify dataset-specific licence, aggregation, update date and relevance before use. |
| Quarter key figures | Selected social indicators for Basel's 19 quarters, Riehen and Bettingen. | [data.bs.ch dataset 100011](https://data.bs.ch/explore/dataset/100011/) | Verify dataset-specific licence, definitions and update date before use. |
| MeteoSwiss open data | Official weather measurements, forecasts and meteorological warnings. | [MeteoSwiss Open Data](https://opendatadocs.meteoswiss.ch) | Check the product's access, licence, attribution, coverage and update schedule. The MeteoSwiss app relays Alertswiss messages at alarm level; this does not establish that the MeteoSwiss data feed contains all Alertswiss messages. |
| Alertswiss alerts | Federal and cantonal emergency information, warnings and alerts, including affected areas and public instructions. | [Alertswiss](https://www.alert.swiss/en/home.html) · [Alertswiss FAQ](https://www.alert.swiss/en/faq.html) · [BABS multi-channel strategy](https://www.babs.admin.ch/dam/de/sd-web/yqZESGSo8RVq/20241001-Multikanastrategie-de.pdf) | Useful for broader hazards beyond weather. The BABS strategy describes a machine-readable API as planned work; verify a current feed, access and reuse terms before integration. Alertswiss content has separate reuse conditions; review its [legal terms](https://www.alert.swiss/en/home/meta/legal-issues.html). |
| Heat-related deaths in Switzerland | Yearly federal estimates of deaths caused by heat, with data to download. | [Federal indicators — KL077](https://www.indikatoren.admin.ch/public/v2/detail?ind=KL077&lng=de) | Check the dataset's terms, definitions, time range and attribution before reuse. |
| swissSURFACE3D Raster | Surface model at 0.5 m including buildings and trees, for calculating shade. | [swisstopo swissSURFACE3D Raster](https://www.swisstopo.admin.ch/de/hoehenmodell-swisssurface3d-raster) | Check current access, licence, attribution and dataset coverage before use. |
| OpenStreetMap via Overpass | Benches, pharmacies, public toilets and streets, queryable in the browser. | [Overpass Turbo](https://overpass-turbo.eu) | OpenStreetMap data is under ODbL 1.0; follow attribution and applicable share-alike requirements. |

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
