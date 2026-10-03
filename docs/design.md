# Bla Bla Walk: design brief

Updated: 2026-10-03. Synthesized from the team's 2026-10-02 meeting notes.
The meeting established the direction; the demo scope below is a proposal for review, not a completed product or a final scope decision.

## Problem and users

People who are more affected by heat, including older adults, children, pregnant people, and people with chronic illnesses, may need help planning a walk. Caregivers may plan on their behalf. A useful route needs to account for exposure, water, places to cool down, and barriers, rather than distance alone.

## Direction recorded in the meeting

- Start with a mobile-friendly web map focused on heat in Basel.
- Explore routes to cooler destinations using shade, fountains, and known closures or accessibility barriers.
- Investigate public and aggregated data before committing to live integrations.
- Preserve access for people without smartphones as a design concern; a phone interface needs further scoping.
- Treat volunteer accompaniment and community assistance as a later phase, with operating and vetting arrangements still unresolved.

## Proposed first demo

Use one small Basel demonstration area and a fixed pair of route alternatives, with clearly labelled sample data where sources have not been verified.

1. Choose a sample start and a cooler destination.
2. See two walking alternatives on a map, with distance, modelled daytime heat stress (PET), water, and obstacle information; use labelled synthetic PET if data access is not verified.
3. Compare the tradeoffs and see why one route is suggested under the demonstrated rules.
4. Inspect source labels, update times, missing information, and the demo's limitations.

The proposal demonstrates route comparison before attempting city-wide route generation. Whether to use precomputed alternatives or a routing service remains a technical decision for the foundation task.

## Data and components

The [source register](SOURCES.md) is the home for candidate providers, availability checks, licences, and attribution. No dataset has been downloaded or validated as part of this documentation update.

Recommend Basel-Stadt Geoportal daytime PET for the initial heat comparison, pending T0's endpoint, licence, and data-access checks. The source register documents the evidence that PET includes shade effects, its 14:00 summer scenario, and its limitations. Compare routes within that scenario; do not apply another assumed shade cooling adjustment to PET. Time-specific shadow modelling is deferred, and PET aggregation rules still need team agreement in T2.

Expected components are a map and route-comparison screen, data adapters, and route evaluation rules. The foundation task will choose the stack and define a single shared interface for locations, route segments, observations, timestamps, and missing-data states. Data adapters must handle coordinate systems explicitly, including LV95 to WGS84 conversion when required by a source.

No application stack, deployment platform, routing weights, or medical thresholds have been selected. Domain rules need concrete examples reviewed by the team. Shade and tree data must not be presented as a validated temperature or health-risk measurement.

## Privacy and accessibility

Use public or synthetic demonstration data. Do not require an account, personal health details, or a stored location history for the proposed demo. The meeting's idea of risk-category profiles remains unresolved because categories can disclose health information; the initial proposal uses route preferences instead.

Readable text, touch-friendly controls, non-colour-only explanations, and keyboard access are part of the web demo proposal. A road crossing or step-free route must not be described as accessible unless the relevant data has been checked. Unknown conditions should be visible.

## Deferred ideas

These remain in the backlog for scope review: live weather alerts, public transport alternatives, community reports of closures or fountain outages, phone-call guidance, kiosk mode, cold/ice/heavy-rain routing, volunteer matching, errands or rides, smartwatch monitoring, and on-device language models.

Arbitrary departure-time shade simulation also remains deferred; the proposed initial PET comparison does not support live or time-specific heat estimates.

The phone channel is an important accessibility goal from the meeting, but its service flow, operations, and technical approach are not decided. Volunteer features likewise require a separate operational design before a pilot.

## Open decisions

- Confirm the demo area, destination, and first user journey with the team.
- Agree the smallest demo scope and how the non-smartphone journey will be represented.
- Verify source coverage, licences, freshness, and accessible crossing information.
- Choose the stack and route-generation approach after the first data audit.
- Agree route-comparison rules and how stale or missing observations affect recommendations.
- Confirm the public project/team name: this draft uses the existing repository name; the meeting mentioned a different team name.
- Assign task owners by GitHub username; meeting speaker labels are not identities.

## Risks and fallback

Incomplete or stale data can produce misleading routes. Display unknowns and source timestamps, avoid promising a "safest" route, and distinguish a demonstrated comparison from validated real-world guidance.

If live sources or map services are unavailable, show a labelled local sample scenario and saved screenshots of the same flow. Keep any recording local and prepare a short explanation of what was simulated.
