# T8 — reusable city geometry

Status: done (acceptance) · Slot E / @Derriick · PR branch: feat/t8-city-geometry-complete

## State

T8's literal geometry acceptance passed: all 65 receiver pairs and all 225
available assets prepared; every selected tile has a prepared or documented gap
record. Checkpoints 08114c9 and 4848aaf were checked before changes. Bounded
pipeline checkpoint 14b31b3 is pushed; full acceptance is saved as e6c1ec0.
Updated from main 1e043f5 in merge checkpoint 489925d; all 56 tests pass again.
The upload hook blocked the main-merge ancestry because existing upstream author
names fail local push checks. Shared history was left intact: the exact verified
T8 diff is carried on feat/t8-city-geometry-complete, based on main 1e043f5.
Original feat/t8-city-geometry and pushed checkpoint 14b31b3 remain available.
Completed branch is committed/pushed as 80bf175; both privacy hooks passed.
The filled browser PR form was opened successfully. Browser-authenticated
creation remains pending; ask before merging once the PR exists.
Never merge without the user's explicit yes.

## Done

- User-approved Rasterio 1.5.2/NumPy 2.5.3 plus required transitive packages are
  pinned in backend/requirements.txt and installed only in project .venv.
- Atomic checksum-verified downloads and native stripe decoding, versioned local
  manifest, single-writer lock and verified resume. One timed-out download was
  repaired by rerunning the batch; all other outputs were reused.
- Preserve native 0.5m float32 heights, EPSG:2056 and LN02/EPSG:5728 provenance,
  explicit masks/NoData, negative differences and all nominal survey mismatches.
  Four representative scenes exactly reproduce T0 full-cell statistics.
- Canonical GeometryWindow plus bounded GeometryStore reads, separate sample and
  receiver masks, unknown bridge/canopy/tunnel receivers and conservative reach
  policy. Shared-interface decision is recorded.
- Full asset/output checksum audit: 139 tile records, 96 pairs, 43 catalogue-gap
  tile records. All 65 receivers paired. Ten surface / 43 terrain buffer gaps
  and 11 invalid source cells remain explicit, with no infill.
- 502 adjacent product seams: 397 measured, 105 unknown gaps; retain jumps.
  All grids contiguous at 0.5m. All 96 pairs mix nominal 2023/2025 surveys.
- Centre/boundary OpenLayers rendering against 25 loaded live Basel tiles;
  browser errors zero, reference-to-cell-centre distances 0.130m/0.260m,
  screen offsets 0.162px/0.323px. Screenshots visually inspected. Real bridge
  diagnostic uses zero eligible bridge receivers; deck elevation stays unknown.
- Storage 6.44 GiB / 8 GiB. Original ingestion peak about 125 MiB; audited resume
  about 120 MiB. Two spawned native readers peak 123.70/123.63 MiB (sum 247.34),
  below 768 MiB each / 1536 MiB total. T10 halo/shade/API memory not measured.
- 56 regression tests passed including three Chromium checks. Focused T8
  lint/format, contract generation, doc-check and whitespace checks passed.
  Full-repo lint/format has pre-existing T9 routes.py long lines; not changed
  across file ownership. Existing Starlette/httpx deprecation warning remains.

## Critical T10 limits

Maximum relative height 387.90m (2610-1267) exceeds the 250m planning envelope;
physical cause unverified. Whole-inventory terrain relief 280.82m. Conservative
combined reach at 10 degrees is 3792.51m: 1500m is not blanket coverage. Check
sunward reach/relief/gaps per request and retain unsupported/unknown results.
Survey scene consistency, seam causes, bridge/canopy/tunnel walking elevations,
2m accuracy, shade accuracy and API performance remain unresolved T10 evidence.
Native sample validity is not scene acceptance or known sunlight/shade.

## Memory finding

Initial apparent 859 MiB failure was a measurement artefact: Linux getrusage
retained a pre-exec launcher peak. In the same resumed process it reported
879332 KiB while current-image VmHWM was 125947904 bytes (120 MiB). Use VmHWM
on Linux; budget unchanged. Regression protects the measurement source.

## Reproduce and consume

Commands and resumable preparation: docs/geometry.md. Source provenance/budgets:
docs/SOURCES.md. Recorded evidence: data/fixtures/geometry-metadata.json. It is
not live coverage and contains no distributed rasters. Each clone prepares its
own ignored data/geometry/ files. Local preview/screenshots and detailed runtime
checks live in .hack/t8/. Preparation/audit use POSIX locking/resource; store is
platform-neutral. No background preparation writer remains running.

## Next

1. Open the completed PR using the prepared browser form. GitHub CLI/hub and
   API tokens are absent in this clone;
   authenticated SSH permits pushes but cannot create GitHub PRs by itself.
   the exact body is saved locally in .hack/t8/pull-request.md. The form targets
   main...feat/t8-city-geometry-complete. Select Create pull request in an authenticated
   browser, or obtain approval to install/authenticate GitHub CLI. Public API
   confirmed there is no open T8 PR yet. Never claim creation until confirmed.
2. Ask before merging the specific created PR. T10 starts only after T8 merges.

## Continue prompt

T8 acceptance is done on feat/t8-city-geometry-complete. Read this handoff and
TASK_START.md. Verify final branch upload, finish creating the completed PR and
ask before merging. Dependencies are approved. Keep critical T10 limits.
