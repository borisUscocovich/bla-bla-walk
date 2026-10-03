# T8 — reusable city geometry

Status: in progress · Slot E / @Derriick · Branch: feat/t8-city-geometry

## State

Checked pushed checkpoints 08114c9 (inventory) and 4848aaf (acquisition).
T0/T1 are merged into starting main 9fa2a35; origin/main remains at that base.
Native preparation is running against all 225 assets. Generated files stay local
under ignored data/geometry/. Full acceptance and PR remain pending.

## Done

- Approved Rasterio 1.5.2 and NumPy 2.5.3 installed in .venv. Dependencies and
  required transitive packages are pinned in backend/requirements.txt.
- Validate all 139 pinned tile squares, grids, CRS, vertical provenance and totals.
  Planning fixture still has zero prepared tiles; replace only after full audit.
- Checksum-verified downloads; atomic stripe-written native float32 NPY outputs;
  versioned manifest, single-writer lock, explicit failures/gaps and verified resume.
  No resampling, gap filling or height clamping; invalid masks become -9999.
- Four real scenes exactly reproduce T0 ranges, valid cells and negative counts.
  Preserve the nominal 2023/2025 survey mismatch and all buffer catalogue gaps.
- GeometryWindow worker contract plus bounded GeometryStore reads; separate
  sample/receiver masks; bridge/canopy/tunnel receivers stay unknown. Conservative
  height/relief/sunward-reach checks and interface decision line added.
- Full-checksum acceptance audit, seam statistics and local OpenLayers preview
  implemented; full-data/browser verification still pending.
- 29 focused geometry tests and 53 non-browser backend tests pass. Lint/format pass.

## Memory finding

First elevated batch stopped at apparent 900,435,968-byte (859 MiB) peak against
768 MiB. Linux getrusage retained a pre-exec launcher peak: the resumed process
reported 879,332 KiB while its current-image VmHWM was 125,947,904 bytes (120 MiB).
Use VmHWM on Linux and retain the old counter as diagnostics. The budget has not
changed. Isolated decoders peak around 100 MiB. Regression protects measurement.

## Reproduce

From repository root with .venv installed (Linux/macOS preparation tools):

```sh
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_prepare --batch scenes
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_prepare --batch receivers
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_prepare --batch buffer
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_audit
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_preview
.venv/bin/python -m pytest -c backend/pyproject.toml backend/tests
```

`--batch all` prepares everything sequentially; `--limit N` selects the first N
batch tiles. Repeat the same batch to resume or repair corruption. Single-writer
lock releases on exit. Hard interruptions may leave abandoned .part files, never
prepared arrays; clean these only when no writer holds the lock. Separate output
roots allow independent workers. Preparation/audit use POSIX locking/resource;
GeometryStore is platform-neutral. Preview needs existing pinned browser assets.
No generated raster is committed. Planning CLI remains metadata-only.

## Next

1. Finish running all-assets batch; inspect failures and receiver/buffer counts.
2. Run full audit, centre/boundary OpenLayers rendering and two simultaneous
   bounded consumer memory checks. Inspect images and seam evidence.
3. Replace planning fixture with actual verified metadata. Document measured
   budgets and explicit survey/seam/border/bridge/ray-reach limitations.
4. Run relevant checks, privacy guard, commit/push; update from main and open
   completed PR. Ask before merging. T10 waits for merged T8; shade/API targets
   and 2m accuracy remain T10 work.

## Continue prompt

Continue T8 for Slot E on feat/t8-city-geometry with hack-build and TASK_START.md.
Read this handoff and T0 inventory/manifest. Check active batch before starting
another writer. Finish literal acceptance, commit/push and open PR; ask before
merging. Rasterio/NumPy approval is already given.
