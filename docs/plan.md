# Proposed build plan

Based on [the design brief](design.md). Scope and ownership need team review before implementation. No implementation task has started. Owners are unassigned until contributors choose them; use GitHub usernames when assigning work.

Task state belongs in the relevant handoff file. File paths below are proposed, not existing application files. The foundation task must settle the stack and adjust these paths before parallel code work starts.

## M1: a small, reproducible map demo

### Chunk A: parallel preparation

#### T0 Verify candidate data

Owner: unassigned
Needs: nothing
Files: docs/SOURCES.md
Done when: the team can identify one usable source for each required demo layer, or an explicitly synthetic fallback, with exact dataset URLs, licences, coverage, coordinate systems, timestamps, and attribution requirements recorded.
Notes: use the prioritized sources in [the source register](SOURCES.md) first wherever they fulfil a need, and prioritise Basel-Stadt Geoportal daytime PET (`HumanbioklimSituation`) for the heat layer. Verify the actual endpoint/download, dataset licence, delivered resolution, units or class ranges, missing-data encoding, and a usable numeric sampling/query method. Distinguish the 2019 analysis baseline from the 2030 projection and record model scenario time separately from publication and retrieval times. If only a rendered map or no usable values are available, record that limitation and use a labelled synthetic fallback.

#### T2 Agree the example and route rules

Owner: unassigned
Needs: nothing
Files: docs/routing-rules.md, data/scenarios.json
Done when: the team approves a demo area and at least three synthetic cases: contrasting PET/water/distance tradeoffs, a known blocked segment, and missing or stale information. Expected outputs, units, and route aggregation rules are explicit, and no unvalidated health thresholds are introduced.
Notes: use the documented 14:00 summer PET scenario for the initial heat comparison. Agree how route length or walking duration affects exposure and how classified values, if supplied, can be compared without inventing precise temperatures. Do not count shade twice by applying an extra cooling adjustment to PET; arbitrary-time shadow modelling is deferred.

#### T3 Define accessible visual design

Owner: unassigned
Needs: nothing
Files: docs/style-guide.md
Done when: the team can review the mobile route-comparison screen, including readable labels, keyboard navigation, non-colour-only explanations, and the unknown-data state.

### Chunk B: in order after preparation

#### T1 Build the foundation

Owner: unassigned
Needs: T0, T2, T3
Files: README.md, docs/decisions.md, docs/plan.md, package manifest and lock file, application entry point, shared interface file, theme file, initial tests
Done when: a fresh checkout starts using verified README commands and shows the full sample journey from start/destination selection to two labelled route alternatives. The stack, layout, shared contracts, and test command are documented; one theme file applies the agreed style.
Notes: include PET values or class ranges, units, scenario time, dataset timestamps, and unknown-data states in contracts, following the source register. Record interface decisions in the same commit. Resolve the proposed file paths in this plan before later tasks begin.

## M2: compare routes with inspected inputs

### Chunk C: parallel after the foundation

#### T4 Connect the selected data layers

Owner: unassigned
Needs: T1
Files: data adapters, data fixtures, adapter tests, docs/SOURCES.md
Done when: at least one verified dataset appears in the demo with source and freshness labels; failed requests fall back visibly to sample data. Coordinate conversions, when needed, pass a known reference example.
Notes: attempt the verified Basel daytime PET integration first and use the prioritized sources in [the source register](SOURCES.md) for other layers whenever they meet the need. Sampling must preserve numeric values or documented class ranges and distinguish missing cells from low heat stress. Display the model scenario and data provenance; use a labelled synthetic PET fallback if access cannot be verified.

#### T5 Implement route comparison rules

Owner: unassigned
Needs: T1
Files: route evaluation module, config/routing-rules.json, rule tests
Done when: the approved scenarios produce their expected comparisons, blocked routes are excluded according to the agreed rules, and missing information is shown without being interpreted as safe. Each suggestion includes an explanation.
Notes: apply T2's agreed PET aggregation rules alongside distance, water, and obstacles. Verify that no additional shade cooling adjustment is applied to PET and that the 2030 projection is not mixed into the baseline.

### Chunk D: in order

#### T6 Connect and check the complete journey

Owner: unassigned
Needs: T4, T5
Files: map and comparison UI, application wiring, integration tests, README.md
Done when: a user completes the approved journey on a narrow screen and with keyboard controls, sees evidence and limits for each route, and can still view the labelled fallback when a source fails.
Notes: explain PET as modelled heat stress and show the 14:00 summer scenario. Do not label PET as current air temperature or imply support for arbitrary departure times.

## M3: a repeatable demonstration

### Chunk E: after the complete journey

#### T7 Prepare the story and fallback

Owner: unassigned
Needs: T6
Files: docs/demo.md; screenshots or recordings kept locally
Done when: the presenter can demonstrate the problem, route comparison, and sources/limits in three minutes, and can show the same story from saved material without live services. Explain the planned non-smartphone journey and which features remain future work.
