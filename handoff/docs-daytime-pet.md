# Daytime PET source recommendation

State: documentation complete; data integration not started.

## Goal
Document Basel-Stadt Geoportal daytime PET findings and align the demo plan.

## Done
- Added official method, layer-model, catalogue, licence, and service-discovery references to docs/SOURCES.md.
- Recorded shade effects already included in PET, the 14:00 summer scenario, model resolution, and pending API/data-access checks.
- Updated docs/plan.md, docs/design.md, and docs/decisions.md to recommend PET for the first demo and defer arbitrary-time shadows.
- Kept route weighting and aggregation undecided; prevented duplicate shade cooling adjustments in the proposed rules.

## Next
- T0: verify the exact endpoint/download, licence, numeric PET or class access, missing-data encoding, and geographic coverage.
- T2: agree the demo scenario and route aggregation rules using inspected data or labelled synthetic examples.

## Limits
No dataset was downloaded or integrated. The service endpoint is not yet verified. This work does not validate real-world routes or live heat estimates.

## Resume prompt
Continue T0 using docs/SOURCES.md: verify access to Basel-Stadt daytime PET and record the exact dataset, endpoint, licence, format, values/classes, and missing-data behaviour before implementation.
