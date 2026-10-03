# Handoff: T2 walk and comparison rules

Status: in progress · Updated: 2026-10-03 · Branch: feat/t2-walk-rules · Last owner: @danielbarmaimon (Slot B)

## Goal

Agree one real demo walk and the comparison rules required by T2 in the
[build plan](../docs/plan.md#t2-agree-one-walk-and-comparison-rules).

## State

Started from fetched origin/main at 8af65ba; T2 has no task prerequisites and no
existing active T2 ownership was found. This checkpoint is a discussion draft,
not completed T2. Team input on the real walk, workaround and domain pitfall is
pending. No application, shared interface or production configuration changed.

## Done

- Read the shared metaprompt, plan, design, decisions and team file ownership.
- Confirmed privacy hooks are configured and executable.
- Prepared a public endpoint candidate with official place references.
- Added a synthetic shade/time/water comparison with two preference sets that
  change the winner. Real endpoint coordinates and route geometry remain unset.
- Formatted and parsed the JSON with Node; checked length partitions,
  percentages, walking times, detours and every score contribution. Shade-focused
  scores are A=0.325, B=0.55; time-focused scores are A=0.475, B=0.3975.
- Ran the repository documentation check: passed. There is no application test
  suite or formatter setup yet; T1 owns that foundation.

## Next (in order, concrete)

1. Get the team's real public start/destination, purpose, current workaround and
   one domain pitfall; replace or confirm the candidate.
2. Agree speed/stops, acceptable detours, access constraints, scoring criteria,
   fixed ranges/default weights and unknown/stale completeness rules.
3. Add and approve water, blocked, unknown, tie, all-zero and insufficient-evidence
   cases. Record accepted choices in the decision log in the same checkpoint.
4. Verify the fixture arithmetic, JSON formatting, documentation and privacy;
   commit/push checkpoints. Open the completion PR only when T2's literal
   acceptance check passes; ask before merging that PR.

## Files

- [Routing rules](../docs/routing-rules.md): discussion example and open decisions.
- [Scenario fixture](../data/scenarios.json): synthetic metrics and expected results.
- This handoff: task ownership and current progress.

## Decisions made

No new domain defaults or demo endpoints have been approved. Follow the existing
weighted-recommendation design; constraints stay outside weights. T0 owns source
admission, T1 owns interfaces, T9 owns walking geometry, T5 owns production
scoring/configuration. Do not edit their files or the build plan for this task.

## Open questions / problems

- Real team walk, workaround and domain pitfall are awaiting user input.
- Illustrative assumptions are proposals, not health thresholds or observations.
- Remaining acceptance examples and defaults are not yet agreed; T9/T5 stay gated.

## Resume prompt

> Continue T2 for Slot B using $hack-build. Read handoff/t2-walk-rules.md on
> feat/t2-walk-rules. Start with the team's real walk example and Next step 1.
