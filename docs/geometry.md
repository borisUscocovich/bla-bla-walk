# Native city geometry

T8 prepares the pinned [T0 inventory](../data/tile-inventory.json) using the
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
`data/geometry/`; `--root` selects another local output directory. One process
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
