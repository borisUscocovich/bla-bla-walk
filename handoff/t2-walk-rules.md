# Handoff: T2 walk and comparison rules

Status: done · Updated: 2026-10-03 · Branch: feat/t2-walk-rules · Last owner: @danielbarmaimon (Slot B)

## Goal

Specify one real public-place demo walk and the comparison rules required by
T2 in the [build plan](../docs/plan.md#t2-agree-one-walk-and-comparison-rules).

## State

T2's domain specification and acceptance fixtures are complete on this branch.
The user delegated the remaining demo choices by instructing Codex to continue
until the task was finished. Defaults and scenarios are recorded under that
delegation; the current workaround is an explicit demo assumption, not an
interview finding. The completion PR needs review and an explicit merge yes.
Downstream tasks must still wait for T2 to merge into main.

## Done

- Selected Basel SBB/Centralbahnplatz → Marktplatz, with public-place references,
  a scenario workaround and the construction-versus-closure domain pitfall.
- Specified adjustable walking speed/stops, distance/time detour constraints,
  fixed shade/duration/water normalization and default preference weights.
- Specified full-length denominators, conservative unknown/stale evidence,
  access/coverage eligibility, water qualification and active-criterion checks.
- Added ties, zero/invalid weights, no eligible route, manual choice and
  cached-metric rescoring without repeating shadow calculations.
- Added 39 synthetic acceptance examples. Verified expected metrics,
  contributions, winners, completeness and detour boundaries, including
  independence from route order and the equal-distance reference stop plan.
- Updated design references and appended decisions without changing the plan,
  the shared interface, production scoring/config or other slots' owned files.
- Added a dependency-free Node acceptance checker and formatted its JSON.

## Next

1. Review the completion PR for feat/t2-walk-rules; merge only after an explicit
   yes for that PR. No application or live route calculation is claimed by T2.
2. T9: after T1/T2 merge, pin exact public endpoints and checked licensed walking
   geometry. Numerical route examples here are synthetic, not that geometry.
3. T5: after T10/T9/T2 merge, port the examples to production tests/config and
   implement the authored shared contract. Preserve active-criterion evidence
   gating, constraint reasons and route-order invariance.

## Files

- [Routing rules](../docs/routing-rules.md): domain specification and formulas.
- [Scenario fixture](../data/scenarios.json): one home for numeric defaults and cases.
- [Acceptance checker](../scripts/check-routing-scenarios.mjs): run with Node.
- [Design](../docs/design.md): points to the completed domain rules.
- [Decisions](../docs/decisions.md): appended selected walk and scoring policies.

## Validation

Run `node scripts/check-routing-scenarios.mjs` for all 39 examples, route-order
invariance and JSON format. Add `--format` to format the scenario file.
Run `node --check scripts/check-routing-scenarios.mjs` and the repository
documentation/privacy checks. T1 has not provided an application test suite
or formatter manifest on the merged foundation yet; no packages were installed.
The 39 examples, JSON format, Node syntax, staged whitespace and privacy check
passed. The strict documentation check reports one inherited T3 warning:
the style guide names src/theme.css, which T1 has not created yet. That warning
also exists in origin/main; this task introduces no missing documentation paths.

## Limits / decisions

Numeric defaults are editable demo choices, not health thresholds. The scenario
workaround is assumed. Source references identify public places/a construction
caution; no exact endpoint coordinates, walking geometry, actual shade, fountain
operation or participant habits were fabricated. T0 owns source admission;
T9 supplies geometry; T1 owns the shared interface; T5 owns production evaluation.

## Resume prompt

> Review completed T2 for Slot B on feat/t2-walk-rules. Read this handoff and
> docs/routing-rules.md; run node scripts/check-routing-scenarios.mjs. Check the
> completion PR, and ask for an explicit yes before merging it.
