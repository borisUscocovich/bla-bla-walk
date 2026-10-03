# Sources

Every dataset, API, notable library and AI tool used, with licence. Feeds the sources slide on Sunday.

| What | Source / URL | Licence or permission | Used for |
|---|---|---|---|
| Codex (OpenAI) | chatgpt.com/codex | Tool, AI-assisted development | Coding assistant |

## Map-first source audit — 2026-10-03

Status: research verified where stated; design and stack still proposed. Checks used official metadata APIs, service capabilities, small JSON samples, and provider documentation. Nothing is integrated. Start from the resource list below, which the repository identifies as prioritised project resources. The public organiser site confirms Basel open-data resources but did not independently expose the heat challenge's exact resource list; do not label every repository link as organiser-verified.

Prefer sources permitting reuse for all purposes. The team explicitly allows IWB fountain dataset 100008 for this noncommercial prototype (2026-10-03); keep its commercial-use restriction visible and preserve attribution. Public visibility or free access alone is insufficient. Record provider, licence URL, attribution, modifications, observation/scenario time, publication time, retrieval time, coverage and units. Retain layer-specific licensing rather than treating a combined map as one freely relicensable database.

| Layer | Checked source and evidence | Licence / attribution | Freshness and readiness |
|---|---|---|---|
| Observed air temperature | [100009 metadata](https://data.bs.ch/api/explore/v2.1/catalog/datasets/100009); fields name_original, dates_max_date, meta_airtemp, coords. Latest-record query with order_by=dates_max_date desc and limit=3 succeeded. | CC BY 4.0; meteoblue AG via Open Data Basel-Stadt; link licence and indicate transformations. | Description says hourly; catalog frequency says daily. Sample observations were dated 2026-10-03 at 09:09 UTC. Use each reading's timestamp; raw and not corrected/plausibility checked. Ready for point-layer implementation; full coverage, browser access and latest-per-station query still need tests. |
| Sensor locations | [100082 metadata](https://data.bs.ch/api/explore/v2.1/catalog/datasets/100082); name_original, coords, lon, lat, dates_max_date. | CC BY 4.0; meteoblue AG via Open Data Basel-Stadt. | 198 catalog records at inspection, including the wider region, not necessarily 198 active Basel stations. Join by name_original; independently age each station. Metadata access verified; sample/join test remains. |
| Trees | [100052 metadata](https://data.bs.ch/api/explore/v2.1/catalog/datasets/100052); point geometry, species, planting/age fields. | Metadata explicitly says CC BY 4.0 + OpenStreetMap; attribution Geodaten Kanton Basel-Stadt; [linked exception notice](https://data-bs.ch/stata/dataspot/permalinks/20240822-osm-vektordaten.pdf) checked: canton permission for incorporation into OSM, with attribution waiver specific to OSM. | Daily catalog cadence; managed trees in Basel and Riehen, not all canopy. No height/crown radius fields in inspected schema. Notice reviewed; data access and map integration still to test; unsuitable by itself for physical shadow calculation. |
| IWB fountains | [100008 metadata](https://data.bs.ch/api/explore/v2.1/catalog/datasets/100008); name, desc, geometry and geo_point_2d. Metadata and a small record sample retrieved successfully. | Noncommercial use allowed with attribution: IWB Industrielle Werke Basel. Commercial reuse requires supplier permission. Accepted by the team for this noncommercial prototype; not unrestricted open data. | Irregular updates; no verified live operational-status feed. Includes drinking, bathing and decorative fountains. Preserve type evidence; unknown drinking status stays unknown. Photos require a separate rights check and are excluded initially. |
| Alternative drinking-water source | [OSM licence](https://www.openstreetmap.org/copyright) and [drinking-water tags](https://wiki.openstreetmap.org/wiki/Tag:amenity%3Ddrinking_water). Select amenity=drinking_water or explicit drinking_water=yes; preserve access, seasonal and lifecycle tags. | ODbL 1.0; © OpenStreetMap contributors; preserve licence and applicable share-alike obligations for redistributed/derived databases. | Optional alternative, local extract not yet checked. Mapped availability is not an operational live feed. No implied drinking status for generic fountains; avoid importing restricted IWB data into OSM. |
| Historical PET | Official climate model and WMS capabilities (details below). Baseline layer KL_HumanbioklimaSituation. | HOLD until specific public/download status and licence are verified; general canton terms alone are insufficient. | Fixed summer 14:00 scenario. Not today's thermometer temperature. Can be offered only once access/licence pass; it must remain separate from observations and predictions. |
| Basel basemap | [VSBS STAC metadata](https://api.geo.bs.ch/stac/v1/collections/VSBS) lists CC-BY-4.0; [3857 WMTS capabilities](https://wmts.geo.bs.ch/EPSG/3857/1.0.0/WMTSCapabilities.xml) advertises VS_Vektorstadtplan_grau and Stadtplan_grau. | Source: Geodaten Kanton Basel-Stadt; retain relevant dataset notices. | Capabilities verified. Exact tile-to-dataset mapping, successful tile request, scales, service policy and browser access must pass before adopting. [Swisstopo OGD](https://www.swisstopo.admin.ch/en/faq-free-geodata) is an unrestricted-use alternative with © swisstopo attribution; exact product/service still to select. |
| Forecast context | [MeteoSwiss local forecasts](https://opendatadocs.meteoswiss.ch/e-forecast-data/e4-local-forecast-data); collection ch.meteoschweiz.ogd-local-forecasting; hourly air temperature parameter tre200h0. | [CC BY 4.0 terms](https://opendatadocs.meteoswiss.ch/general/terms-of-use); Source: MeteoSwiss. Weather pictogram graphics are proprietary and excluded. | Hourly updates, nine-day point forecasts; hourly files can be up to 33 MB, so fetch/filter centrally. Verify Basel point, downloadable asset and timestamp semantics before integration. City-scale context, not street-scale PET. |

### IWB fountain terms and agreed noncommercial use

[100008 metadata](https://data.bs.ch/api/explore/v2.1/catalog/datasets/100008) states: free use with attribution, **commercial use only with the supplier's permission** (rights code terms_by_ask). This is not unrestricted open data. On 2026-10-03 the team confirmed the prototype is noncommercial and authorised including these fountains within the stated terms. Include the records with IWB attribution and the restriction in source metadata and exported fixtures. Recheck permission before any commercial reuse. Do not assume image rights follow the record licence; exclude photographs until checked. The investigation sample has not been added to the repository.

### Live observations and approximations

Proposed first release: timestamped sensor points, IWB fountain locations with verified type labels and noncommercial attribution, tree context once notices are checked, and separately labelled historical PET once admitted. Poll observations at a source-appropriate cadence, tentatively hourly; refreshing the map never makes an old reading current. Retain last good data on failure with an explicit stale/offline state and original timestamps.

Optional estimated air-temperature layer: use time-aligned nearby sensors and an explicit, bounded interpolation (for example inverse-distance weighting). Display station coverage and distance, mask unsupported areas, document assumptions, and check withheld-station error before displaying numbers. This is a proposed method, not a validated result. Never add a current air-temperature offset to historical PET and call it current PET. Never subtract guessed tree cooling from PET, which already models shade effects.

The team selected two-route comparison with time-dependent shade on 2026-10-03. A physical shade layer now belongs in the intended demo and needs a checked surface/terrain model, capture date, sun geometry, alignment and validation. Tree point buffers may show proximity but must not be called actual shade. Predictions, observed temperature, historical PET and calculated shade stay different variables and layers.

## Prioritized project resources

Use the sources in this list first whenever they fulfil the project's needs. Prefer these listed sources over alternatives for the same need, while checking that the specific data is suitable, current enough, accessible, and reusable for the intended use. For the map-first foundation, start with timestamped air-temperature observations. PET remains a separate historical scenario overlay, conditional on its own licence and access checks. A source being listed here does not by itself verify a dataset's licence, quality, or availability; record those details before using or redistributing data.

| Title | Description | URL | Licence or permission / notes |
|---|---|---|---|
| Heat and health Basel-Stadt | Cool public rooms, the heat hotline, first aid and heat advice in 14 languages. | [bs.ch — Heat and health](https://www.bs.ch/themen/gesundheit/gesundheitsfoerderung/praeventionsangebote/hitze) | Official public guidance; check content and service availability before presenting it. |
| Heat action plan Basel-Stadt | What the canton does before and during a heatwave, and what happens at each warning level. | [Basel-Stadt heat action plan (PDF)](https://media.bs.ch/original_file/cf38be8695e1cb3e0aefcaf832b4b89c65863658/hitzemassnahmenplan-basel-stadt.pdf) | Official publication; check reuse and attribution terms before reproducing content. |
| Climate maps on MapBS | Modelled heat, night cooling and felt temperature across the canton. | [MapBS Stadtklima](https://www.geo.bs.ch/stadtklima) | Map/catalogue reference; verify whether underlying data can be accessed and reused. |
| City temperature sensors | Hourly street-level air temperature from sensors across Basel, raw values. | [data.bs.ch dataset 100009](https://data.bs.ch/explore/dataset/100009/) | Verify dataset-specific licence, sensor coverage, units, quality and update frequency. |
| Public fountains | Locations of drinking, bathing and decorative fountains in Basel. | [data.bs.ch dataset 100008](https://data.bs.ch/explore/dataset/100008/) | Accepted for the noncommercial prototype with IWB attribution (team confirmation 2026-10-03); commercial reuse requires supplier permission. Verify drinking-water type and access; photographs need separate rights checks. |
| Tree register | Position and species of every city-maintained tree, a starting point for shade. | [data.bs.ch dataset 100052](https://data.bs.ch/explore/dataset/100052/) | Metadata: CC BY 4.0 + OpenStreetMap; the linked exception notice was checked: it permits incorporating canton CC BY data into OSM, rather than adding a general share-alike requirement to standalone canton data. Preserve CC BY attribution; ODbL applies when using OSM-derived data. Tree locations do not establish measured shade. |
| Population by age and quarter | Residents by age, sex and nationality for each quarter, updated yearly. | [data.bs.ch dataset 100128](https://data.bs.ch/explore/dataset/100128/) | Verify dataset-specific licence, aggregation, update date and relevance before use. |
| Quarter key figures | Selected social indicators for Basel's 19 quarters, Riehen and Bettingen. | [data.bs.ch dataset 100011](https://data.bs.ch/explore/dataset/100011/) | Verify dataset-specific licence, definitions and update date before use. |
| MeteoSwiss open data | Official measurements and forecasts, the basis for every heat warning. | [MeteoSwiss Open Data](https://opendatadocs.meteoswiss.ch) | Check the product's access, licence, attribution, coverage and update schedule. |
| Heat-related deaths in Switzerland | Yearly federal estimates of deaths caused by heat, with data to download. | [Federal indicators — KL077](https://www.indikatoren.admin.ch/public/v2/detail?ind=KL077&lng=de) | Check the dataset's terms, definitions, time range and attribution before reuse. |
| swissSURFACE3D Raster | Surface model at 0.5 m including buildings and trees, for calculating shade. | [swisstopo swissSURFACE3D Raster](https://www.swisstopo.admin.ch/de/hoehenmodell-swisssurface3d-raster) | Check current access, licence, attribution and dataset coverage before use. |
| OpenStreetMap via Overpass | Benches, pharmacies, public toilets and streets, queryable in the browser. | [Overpass Turbo](https://overpass-turbo.eu) | OpenStreetMap data is under ODbL 1.0; follow attribution and applicable share-alike requirements. |

## Historical heat scenario: Basel-Stadt Geoportal daytime PET

Documentation checked: 2026-10-03. PET is a candidate historical context layer, not the live-temperature foundation. Numeric access and dataset-specific open licensing still need verification; no application integration exists.

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
| API / download discovery | [Official geoservices](https://www.bs.ch/en/node/28694). GetCapabilities verified at https://wms.geo.bs.ch/?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0; exact baseline layer is KL_HumanbioklimaSituation, projection is KL_HumanbioklimaSituation_2030. GetMap rendering, numeric GetFeatureInfo/sampling, download and dataset-specific licence remain to be verified; advertised layers alone do not establish working numeric access |

Recommendation for the demo: compare routes using this documented 14:00 PET scenario, alongside distance, water, and known obstacles. Shade effects are already represented in PET, so do not apply an additional assumed shade cooling adjustment to those values. A separate shade overlay may explain conditions, but is not evidence for subtracting temperature or PET degrees.

Keep model/scenario time, dataset publication or update time, and retrieval time distinct. Missing cells or unavailable data must remain unknown; a synthetic fallback must be visibly labelled. Do not present this historical baseline or its 2030 projection as today's conditions.

Time-specific shadow modelling with surface/building data and SunCalc is a later option if arbitrary departure times become part of the scope. It would need its own validation and would not automatically produce updated PET values. The sources below remain candidates for that extension.

## Licence-checked sources for later shade modelling

These general provider terms do not replace dataset-specific checks. Metadata and small samples were inspected on 2026-10-03; no application integration exists. Keep attribution and applicable licence notices with derived outputs.

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

## Time-dependent shade: open geometry preflight — 2026-10-03

The team requested shade for the current time alongside two-route comparison. This changes the prior proposal that deferred shadow modelling. Real time here means recalculating solar geometry for the current timestamp; it does not imply live geometry, observed cloud shadows or live tree-canopy measurements.

- Recommended geometry: [swissSURFACE3D Raster](https://www.swisstopo.admin.ch/de/hoehenmodell-swisssurface3d-raster), a 0.5 m surface grid including terrain, buildings and vegetation; pair with swissALTI3D terrain for ground-level receiver heights. Use actual OGD download assets, not the product page's test-only sample data. [Swisstopo terms](https://www.swisstopo.admin.ch/en/faq-free-geodata) permit reuse for all purposes with © swisstopo attribution.
- [Surface catalog query](https://data.geo.admin.ch/api/stac/v1/collections/ch.swisstopo.swisssurface3d-raster/items?bbox=7.575,47.55,7.61,47.57&limit=4) and [terrain catalog query](https://data.geo.admin.ch/api/stac/v1/collections/ch.swisstopo.swissalti3d/items?bbox=7.575,47.55,7.61,47.57&limit=4) both returned Basel items and GeoTIFF asset URLs. This was a bounded discovery query, not a complete/current tile inventory. Example item swisssurface3d-raster_2023_2610-1266 offers a 0.5 m EPSG:2056 asset; example terrain item swissalti3d_2019_2610-1266 offers 0.5 m and 2 m assets. The year difference requires alignment and scene-consistency checks. Catalog datetime is not necessarily an exact survey date. No raster bytes or range requests have been tested yet.
- Coverage decision (2026-10-03): support shade across all Basel. Pin an administrative boundary and enumerate all intersecting surface/terrain tiles plus an occluder buffer; shadows from tall buildings outside the map crop can cross routes. Buffer size must reflect object height, solar elevation and the permitted time range. Where geometry or the buffer is incomplete, label shadow results unknown rather than sunlit. Show low-sun, night, and unsupported bridge/tunnel cases explicitly.
- Calculate direct-sun occlusion using surface heights, terrain receiver elevation and solar azimuth/elevation. Validate sun-angle conventions, raster NoData, units, map alignment and ground positions beneath canopies. A DSM treats canopy as a surface and cannot resolve gaps, seasonal foliage or all underpasses. Relief hillshade is not a walk-level shadow mask.
- Candidate sun-position utility (not yet selected): [SunCalc](https://github.com/mourner/suncalc), BSD-2-Clause; retain its notice. Sun position alone does not calculate building/tree shadows. Implementation library and stack remain unselected.
- [Basel MapBS 3D](https://www.bs.ch/news/2025-das-3d-geoportal-bietet-mit-projektabschluss-neue-perspektiven-auf-basel) documents time-dependent shadow visualisation. Use it as a cross-check; independently verify each 3D dataset's reuse terms before adopting it. A visual 3D rendering does not supply numeric route shade automatically.
- Proposed outputs: shaded route length, unshaded length and unknown length in metres; percentage denominators explicit. Compute along a walk using departure time plus travel time to each segment, not just departure-time shade everywhere. Walking speed, stop delays, receiver height and sampling resolution require explicit team-approved assumptions.
- Proposed serving approach for confirmed city-wide coverage: preprocess geometry once into reusable tiles; compute requested viewports and route corridors on demand rather than every city cell per request; calculate/cache shade for time buckets (tentatively five minutes, accuracy/latency to benchmark). Preserve requested time, effective calculation time, geometry version and resolution. Do not imply exact instantaneous results or measured cooling. Keep clouds as separately labelled weather context, never erase geometry shadows based on a coarse forecast.

City-wide discovery is not complete: the four-item bounding-box queries above only establish example asset availability. T0 must follow pagination, select appropriate versions and establish boundary/occluder coverage, including any surrounding areas outside Switzerland. Unsupported border geometry must remain unknown.

## Selected implementation tools — documentation checked 2026-10-03

TypeScript/OpenLayers with a Python worker selected by the team; not installed or integrated yet. [OpenLayers](https://openlayers.org/) supports raster/tiled OGC layers and vector formats; [licence](https://github.com/openlayers/openlayers/blob/main/LICENSE.md): BSD-2-Clause, retain notice. [Rasterio windowed reads](https://rasterio.readthedocs.io/en/stable/topics/windowed-rw.html) allow chunked raster processing; [licence](https://github.com/rasterio/rasterio/blob/main/LICENSE.txt): BSD-3-Clause, retain notice. A custom or separately verified shadow algorithm is still needed. [Leptos JavaScript integration](https://book.leptos.dev/web_sys.html) documents wasm-bindgen integration and DOM ownership considerations; [project](https://github.com/leptos-rs/leptos) offers MIT licensing. Check exact pinned versions and transitive notices at adoption. Open-source libraries do not determine the licences of displayed data.

Foundation tooling: [Vite](https://vite.dev/guide/) for the TypeScript browser build and [FastAPI](https://fastapi.tiangolo.com/) for the Python API; pin exact versions and preserve upstream licences/notices during T1. Shadow-library and deployment choices remain pending the preflight.
