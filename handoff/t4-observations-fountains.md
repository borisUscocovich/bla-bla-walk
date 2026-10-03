# T4 — observations and fountains

## State

Status: in progress · Slot A · Branch: `feat/t4-observations-fountains`.
T1 and T0 are merged in main.

## Done

- Pull current main. Confirmed T1 PR #14 and T0 PR #16 merged.
- Added bounded Open Data Basel-Stadt temperature and fountain adapters.
- Confirmed the Explore API's 100-row page cap; adapters paginate within source limits.
- Switched temperature history to one bounded 5,000-row JSON export.
- Joined observations using station ID; points include reading age.
- Marked old readings and failed-refresh snapshots visibly stale.
- Preserved fountain drinking, operating and access status as unknown.
- Added minimal, dated, rights-labelled source fixtures.
- Kept API integration with T6 ownership.

## Next

1. Finish live query checks and review.
2. Run full checks and privacy guard.
3. Commit, push and open a T4 pull request.

## Limits

The observation export caps at 5,000 recent records. Stations absent from that window remain missing. Process caches do not survive restarts. The map-bound rectangle can include points outside the canton. Fountain metadata has no structured water or operational fields. Fixture timestamps are historical source samples.

The adapters are not yet called by `main.py`; T6 owns API integration. No model contract changed.

## Continue prompt

Continue T4 on `feat/t4-observations-fountains`. Read this handoff and T4 in `docs/plan.md`. Finish checks and source manifest updates, then commit and open the PR.
