# T8 — reusable city geometry

Status: in progress · Slot E / @Derriick · Branch: feat/t8-city-geometry

## State

Inventory checkpoint pushed as 08114c9. Continued with checksum-verified, atomic
asset acquisition; raster decoding awaits dependency approval.
T1 and T0 are merged into the starting main (9fa2a35). No existing T8 ownership
was found in handoff/. No raster is prepared yet; T8's acceptance check is pending.

## Done

- Validate all 139 pinned tile squares: 65 receivers, 74 buffer-only squares and
  225 available assets. Check origin, shape, EPSG:2056, LN02/EPSG:5728,
  0.5m resolution, NoData, checksum format, official asset host and summary totals.
- Preserve the 10 surface / 43 terrain catalogue gaps and all 96 paired nominal
  year mismatches. Every cell and scene validation remains pending.
- Generate `data/fixtures/geometry-metadata.json` as a **planning fixture**, with
  zero prepared tiles and inventory digest. It is not an API coverage response.
- Estimate compressed assets plus native float32 arrays against the existing
  8 GiB budget. Remaining space excludes derived grids, metadata and temporary
  files; one pair uses 32,000,000 array bytes before masks/decoder overhead.
- Added geometry_assets.py: bounded streaming, full checksum/size verification,
  verified-file reuse, atomic replacement and cleanup on failure. Synthetic
  download tests cover corrupted local files and truncated remote responses.
- Generated data/geometry/ outputs are ignored before any raster download.
- No new packages installed or shared wire contracts changed. Rasterio, NumPy,
  Pillow and PyProj are all absent. Approval question for Rasterio/NumPy is pending.

## Reproduce this checkpoint

From repository root:

```sh
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry
.venv/bin/ruff format backend/bla_bla_walk/geometry.py backend/tests/test_geometry.py
.venv/bin/ruff check backend/bla_bla_walk/geometry.py backend/tests/test_geometry.py
.venv/bin/python -m pytest -c backend/pyproject.toml backend/tests/test_geometry.py -q
```

The first command writes a local plan under `.hack/t8/`. To regenerate the
committed planning fixture, add `--output data/fixtures/geometry-metadata.json`.
The planner validates metadata only and does not download anything or implement
resume; its resume field specifies the requirement for the next checkpoint.

## Checks

14 geometry tests pass, including incorrect origin/grid/CRS/NoData, receiver gaps,
duplicate tiles, summary drift, survey flags, budget overflow and fixture drift.
Python formatting and lint pass; all 36 non-browser backend tests pass (3 browser
checks deselected). doc-check and diff whitespace checks pass. The sandboxed
regression run stalled and was interrupted; the approved run outside the sandbox
passed in 0.32s, with the existing Starlette/httpx deprecation warning.
Privacy guard must pass before this checkpoint is committed and pushed.

## Next

1. Await the pending Rasterio/NumPy dependency approval before installation. Rasterio
   is a candidate for georeferenced window reads; NumPy arrays are another new
   dependency. Declare and pin approved packages in the project manifests.
2. Wire the checked asset downloader into the batch CLI and add atomic prepared
   outputs with a versioned resumable manifest. Generated rasters stay local under
   ignored `data/geometry/`. No local T0 sample
   assets were present in this clone; the inventory contains their pinned URLs.
3. Decode the four T0 scenes first: urban centre, vegetation, tall building,
   border (see source manifest). Measure memory and disk against T0 budgets.
   Preserve masks and negative surface-minus-terrain differences as evidence.
4. Validate seams, survey mismatch, border gaps and bridges; render alignment
   at centre and boundary reference points. Ground-only terrain is insufficient
   to claim bridge walking elevations; bridge/canopy receiver evidence remains
   unknown until addressed. The buffer's height/relief/ray-reach policy must hold.
5. Prepare remaining receivers and buffer assets in separately verified batches.
   Missing buffers and NoData never become known shade. Candidate 2m geometry
   requires accuracy validation before adoption. Define reusable consumer data
   in the canonical interface through hack-interface with a decision line.
6. Complete literal T8 acceptance, open a PR, then ask before merging. T10 remains
   blocked on completed, merged T8. Do not mark T8 done for this planning step.

## Continue prompt

Continue T8 for Slot E on feat/t8-city-geometry. Use hack-build and read this
handoff, TASK_START.md, T8 in docs/plan.md and the T0 inventory/source manifest.
Start at Next with decoder/dependency selection, then one measured raster batch.
