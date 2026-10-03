# City geometry acceptance and native references

Production uses the merged compact configuration in `config/geometry.json`:
1m horizontal cells, 2m height steps, native 0.5m surface max aggregation and
native 2m terrain nearest repetition. `geometry.py` retains that preparation
and scaled reader. `geometry_inventory.py` contains the native inventory planner;
the native pipeline supplies independent aggregation/alignment diagnostics.

```sh
.venv/bin/python scripts/prepare_geometry.py --workers 2
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_compact_audit
```

The audit needs prepared native references as described below. If they already
exist, add `--native-reference data/geometry/native-reference` to the compact
preparation command to borrow matching full-checksum-verified surface TIFFs.
Borrowed files remain intact. Native 2m terrain is resolved and checksum-pinned
separately; native 0.5m terrain is not substituted. Compact and native manifests
occupy different directories. Production deployments need the compact files;
the larger reference cache is optional diagnostic evidence.

All 225 configured compact assets and all 65 receiver pairs were verified in
this clone. Five compact surface cells remain unknown, with the same 53 catalogue
gaps. Every surface tile retains native 2×2 block maxima within 1m rounding error;
all terrain 2×2 repeated cells match. Scaling is applied before subtraction.
397 product seams were measured; 105 seam gaps remain unknown. Mixed surveys,
negative differences and a 388m maximum relative-height anomaly remain explicit.
Quantization can hide small negative differences or move shadow edges; neither
native nor compact data certifies scene consistency or walking shade. T10 must
validate these effects before using them as known route evidence.

Compact rasters occupy 35.36 MiB (compression bytes can differ across runtimes).
This clone, including native references and metadata, occupies 6.47 GiB, below
8 GiB. The full compact/native audit peaked around 155 MiB. Two independent
compact-window workers peaked at 126.57/126.64 MiB (sum about 253.21 MiB), below
768 MiB each and 1536 MiB combined. Full halo/shade/API performance is T10 work.
Compact centre/boundary reference offsets are 0.484m/0.105m and
0.600px/0.131px. Live-basemap screenshots were inspected; bridge walking
elevation remains unknown despite valid scaled raster samples.

T10 uses `CompactGeometryStore` and the canonical `GeometryWindow`, whose
resolution and height step identify the representation. `GeometryStore` reads
native diagnostic windows only. Missing/corrupt files and unsupported receiver
types retain explicit masks, never inferred ground height on bridges.

## Native diagnostic evidence

T8 retains full-resolution validation references for the pinned [T0 inventory](../data/tile-inventory.json) using the
sources, attribution and engineering envelope in [SOURCES.md](SOURCES.md).
The [recorded acceptance metadata](../data/fixtures/geometry-metadata.json)
describes verified local output; it does not distribute rasters or certify live
shade coverage. A fresh installation must prepare its own local files.
Published diagnostic measurements use four decimal places; exact arrays,
checksums and full-precision local manifest evidence remain available locally.

## Preparation and resume

Install the pinned Python requirements using the [project setup](../README.md).
From the repository root, on Linux/macOS:

```sh
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_prepare --batch scenes
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_prepare --batch receivers
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_prepare --batch buffer
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_audit
```

The first batch checks the four T0 examples. Subsequent batches prepare receivers
and buffered occluders. `--batch all` runs all three sequentially; `--limit N`
selects the first N batch tiles. Repeat any batch to resume. Preparation rechecks
the entire raw-file checksum and the prepared array checksum before reuse.
Corruption is repaired; inventory or pipeline version changes invalidate resume.
Each failed tile is recorded explicitly, while verified neighbours survive.

Generated raw TIFFs, native arrays and the versioned manifest live under ignored
`data/geometry/native-reference/`; `--root` selects another local output directory. One process
holds a POSIX writer lock. Normal failures remove temporary files. A killed
process can leave an abandoned `.part` file; remove it only after the writer
has stopped. Temporary output never becomes a prepared array. Preparation and
audit require POSIX locking/resource support; the consumer store does not.

Native arrays retain EPSG:2056 horizontal coordinates, north-first row order,
0.5m resolution, LN02/EPSG:5728 product provenance and float32 heights in metres.
NoData, nonfinite or masked samples become -9999. Negative surface–terrain
differences remain unchanged. Vertical CRS is product evidence, not a claim that
the TIFF embeds it. The pipeline version and inventory digest identify outputs.

## Acceptance evidence and limits

All 65 receiver pairs and 225 available assets were checksum-verified and decoded.
All 139 selected tile squares have a prepared or explicit catalogue-gap record.
The four representative pairs exactly reproduce T0's full-cell statistics.
Eleven invalid surface cells remain unknown. Every one of the 96 available pairs
has different nominal survey years (surface 2023, terrain 2025); the catalogue's
January dates are not precise acquisition dates. Preparation does not establish
scene consistency or physical shade accuracy.

The audit covers 502 adjacent product seams: 397 measured, 105 unknown because
of catalogue gaps. Native grid origins and pixel centres are contiguous. The
largest adjacent surface jump is 47.78m, terrain jump 9.47m. These are jumps
between separate neighbouring cell centres, not differences at a duplicate
sample. Real building/terrain edges and survey artefacts cannot be separated
from this statistic alone; values are retained without smoothing or infill.

Actual maximum surface–terrain difference is 387.90m in `2610-1267`, beyond the
250m planning envelope; its physical cause is unverified. Whole-inventory terrain
relief is 280.82m. Combining those conservative maxima at 10° requires about
3,792.51m reach. Therefore the selected 1,500m buffer is not a blanket guarantee.
T10 must check actual sunward height, relief, ray reach and missing geometry for
each request; envelope violations and unavailable rays stay unknown/unsupported.
No 2m resampling accuracy, shade kernel, API latency or full native halo allocation
has been accepted by T8.

`GeometryStore` returns the canonical `GeometryWindow` contract from
[interfaces.py](../backend/bla_bla_walk/interfaces.py). Each read is bounded to
one native tile or a smaller window; stream neighbouring halo tiles rather than
allocating a full-city/halo mosaic. Sample masks are distinct from receiver
eligibility, and the mismatch flag remains available to T10. Ground receiver
eligibility requires valid paired samples without negative relative height;
T10 must additionally mask the canton and resolve scene uncertainty. Bridge,
canopy and tunnel receivers are always unknown until separate walking-elevation
evidence is supplied. A real Mittlere Brücke diagnostic preserved different
surface/bare-terrain values and zero eligible bridge receivers; neither raster
was treated as a verified walking-deck height.

## Rendering and measured budgets

```sh
PYTHONPATH=backend .venv/bin/python -m bla_bla_walk.geometry_preview
.venv/bin/python backend/check_geometry_alignment.py
.venv/bin/python backend/check_geometry_memory.py
```

The default preview/memory commands above now check compact production geometry.
For native display, add `--native --root data/geometry/native-reference` to the
preview command. The remaining figures below describe the earlier native run.
Preview requires the existing pinned OpenLayers assets; the browser check needs
installed Chromium and access to the admitted Basel basemap. Local PNGs, review
page and screenshots are written under `.hack/t8/alignment/`. Display reprojection
and colour bins are diagnostic visualisation only. Actual OpenLayers rendering
loaded 25 live basemap tiles without browser errors. The centre and pinned western
boundary reference are 0.130m and 0.260m from their native pixel centres (0.162 and
0.323 screen pixels). Browser coordinate round trips are within 1e-6m. Visual
inspection agrees at the Rhine/bridge/building edges and western boundary.
These checks establish grid/display alignment, not independent elevation accuracy.

Verified raw files, arrays and local metadata occupy approximately 6.44 GiB,
below 8 GiB. Preflight reserves 128 MiB for atomic replacement and metadata;
measured disk use is checked after every tile. Peak memory during original
ingestion was about 125 MiB; the acceptance/resume run measured about 120 MiB.
Two independently spawned readers, each streaming the four full native pairs
three times, peaked at 123.70 and 123.63 MiB; the conservative sum is 247.34 MiB.
Each is below 768 MiB, and the sum below the two-worker 1,536 MiB budget.
These measurements concern geometry access, not T10 processing performance.

Linux measurements use `/proc/self/status` VmHWM for the current Python image.
The initial apparent 859 MiB failure came from `getrusage` retaining a launcher
peak across exec; both counters were recorded during diagnosis. The budget was
unchanged. On macOS the tool converts `getrusage`'s byte units directly.
