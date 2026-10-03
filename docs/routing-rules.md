# Walk and comparison rules

Status: draft for T2. The team walk, current workaround, domain pitfall and
recommendation defaults still need agreement. This checkpoint does not complete
T2 or unblock T9/T5. See [the task handoff](../handoff/t2-walk-rules.md).

## First walk example

Candidate public endpoints: **Basel SBB (Centralbahnplatz) to Marktplatz**,
with a proposed purpose of reaching the city market. This is a concrete place
pair for discussion, not a team-confirmed trip or checked walking geometry.
The [SBB station plan](https://company.sbb.ch/content/dam/infrastruktur/trafimage/bahnhofplaene/plan-basel-sbb-a4.pdf)
identifies the station and Centralbahnplatz; the
[cantonal city-market page](https://www.bs.ch/en/verwaltung/prasidialdepartement/amter-und-bereiche/external-affairs-and-marketing/fairs-and-markets/basel-markets/basel-city-market)
identifies the market at Marktplatz. Both references were inspected on 2026-10-03.
T9 must resolve exact public endpoint coordinates and check two licensed routes
after the team selects its walk.

The team must supply or confirm:

- The walk's purpose and endpoints.
- How the person plans this walk today.
- One domain pitfall that the comparison must handle.

A sourced pitfall to discuss: the city-market page describes construction at
the Marktplatz tram stop and a reduced market area from June 2026. This notice
alone does not establish that a particular walking segment is closed. T0 owns
source admission; T9 must check access rather than infer a closure from a
worksite or assume that silence proves access.

## One worked comparison

[The scenario fixture](../data/scenarios.json) is the home for the example's
numbers, assumptions and expected results. All route distances, shade lengths,
fountain states and scores there are **synthetic**. They are not measurements
of the candidate Basel walk, verified water access or live shade calculations.

The fixture asks whether a longer route with more shade should win when shade
has more weight, and whether the shorter route should win when walking time has
more weight. Its walking speed, normalization and two preference sets are
illustrative proposals, not approved defaults or health thresholds.

For that calculation:

- Walking minutes = total route metres / walking metres per second / 60.
  The fixture includes no stops. A planned water/rest detour or stop must add its
  distance and time before evaluation; later shade samples use departure plus
  cumulative walking and stop time.
- Total metres = shaded + unshaded + unknown metres. Each displayed percentage
  divides its metres by the full route length. Unknown metres stay visible;
  excluding them from the denominator can exaggerate apparent shade coverage.
- Shade benefit = shaded metres / total metres. Unknown metres earn no shade
  credit and must never be relabelled as sunlit or cooler.
- Duration benefit = clamp(1 - walking minutes / 40, 0, 1) in this fixture.
  The fixed 0-40 minute range does not change with the competing routes and is
  not a maximum acceptable walking time.
- Water benefit = 1 for the fixture's fresh, accessible drinking-water
  opportunity, otherwise 0. Unknown drinking type, access, operation or stale
  evidence earns no water credit; an unknown is displayed separately from a
  verified absence. The team still needs to define proximity, evidence age,
  access checks and whether water should be binary or continuous.
- Normalize nonnegative preference weights by their sum. A contribution is
  normalized weight times benefit; sum contributions for the comparison score.
  Show the underlying metrics and allow manual selection of an eligible route.

No route recommendation is approved by this checkpoint. In particular, the
fixture's synthetic eligibility and completeness cannot be applied to real
routes until the constraints and evidence requirements are agreed.

## Constraints and missing evidence

The [agreed design](design.md#recommendation-rules) already keeps eligibility
outside preference weights. Known blocked segments cannot be outweighed by
shade, distance or water. Construction cautions, unknown access, unsupported
shade coverage and stale snapshots must remain explicit states.

T2 still needs concrete examples and agreement for water access, blocked
segments, unknown/stale evidence, ties, all-zero weights and insufficient
evidence. Zero total weights must not cause division by zero or an arbitrary
winner. Agree a tie tolerance and show both eligible routes on a tie.

## Remaining decisions before T2 is done

- Select the real walk and confirm its workaround and domain pitfall.
- Agree walking speed, planned stops, acceptable detours and access constraints.
- Agree criteria, fixed normalization ranges and default weights.
- Specify water opportunity checks and freshness/completeness requirements.
- Approve the worked comparison and the remaining edge-case examples.
- Record accepted team choices in the decision log; keep live status in the
  handoff. T1 owns the shared interface, and T5 owns production scoring/config.
