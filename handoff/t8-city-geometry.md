# T8 — reusable city geometry

Status: in progress (upstream compact integration) · Slot E / @Derriick · PR: #25

## State

Original native geometry acceptance passed: all 65 receiver pairs and all 225
available assets prepared; every selected tile has a prepared or documented gap
record. Checkpoints 08114c9 and 4848aaf were checked before changes. Bounded
pipeline checkpoint 14b31b3 is pushed; full acceptance is saved as e6c1ec0.
Updated from main 1e043f5 in merge checkpoint 489925d; all 56 tests pass again.
The upload hook blocked the main-merge ancestry because existing upstream author
names fail local push checks. Shared history was left intact: the exact verified
T8 diff is carried on feat/t8-city-geometry-complete, based on main 1e043f5.
Original feat/t8-city-geometry and pushed checkpoint 14b31b3 remain available.
Completed branch is committed/pushed as 80bf175; both privacy hooks passed.
Completed PR #25 is open: https://github.com/danielbarmaimon/bla-bla-walk/pull/25.
Head 1facda2; GitHub guard passed. Main advanced to d8393eb via compact/offline
PR #24 while this work was being verified. PR #25 now conflicts. Main's T8
acceptance now specifies 1m horizontal / 2m height steps and native 2m terrain.
Do not mark revised T8 complete or ask to merge until compact integration and
acceptance pass. Native reference preparation/evidence remains useful.
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

1. Integrate current main d8393eb without rewriting shared history. A squash
   update from main can avoid bringing existing upstream author-name violations
   into the old-branch push range; retain both pipelines, do not weaken hooks.
2. Keep main's compact geometry.py and test_geometry.py. Move our inventory
   planner/tests to geometry_inventory.py and test_geometry_inventory.py; update
   imports. Move local native raw/arrays/manifest into data/geometry/native-reference
   before running main's compact script: both currently use manifest.json!
3. Keep compact config/production default; native data is validation evidence,
   not a replacement for main's agreed reduced-resource representation. Add
   compact scaled-window consumer and scene/seam/border/bridge alignment checks.
4. Reuse checksum-verified native surface TIFFs when preparing compact outputs;
   resolve/download the pinned 2m terrain as main does. Verify revised acceptance,
   update docs/evidence/handoff, check all new offline/browser tests, commit/push.
5. PR creation required the authenticated browser because CLI/token absent.
   Update PR #25's description in browser if needed; ask before merging only
   when conflicts and acceptance are resolved. T10 starts after T8 merges.

## Continue prompt

Continue T8 on feat/t8-city-geometry-complete and PR #25. Read this handoff,
TASK_START.md and main's new compact geometry/offline changes from PR #24.
Finish integrating and validating the configured compact representation while
retaining native references; commit/push and ask before merging. Dependencies
are approved; no extra install is needed. Keep critical T10 unknowns explicit.
