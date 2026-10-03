# Decisions

One line per decision, newest at the bottom. Never edit an old line; add a new one that says what it replaces.

Format: `- <date> · <decision> · @<github-username> · Affects: <tasks or areas> · Why: <short> · Instead of: <alternative, why not>`

- 2026-10-03 · Transcribe the meeting's web-first, heat-aware walking concept into a design brief, with unresolved demo scope and integrations explicitly marked as proposals · @ltorrecilla · Affects: project documentation · Why: turn the notes into a reviewable starting point · Instead of: treating every discussed feature as an agreed implementation requirement.
- 2026-10-03 · Keep raw meeting notes local and publish only the project-relevant synthesis · @ltorrecilla · Affects: documentation and .gitignore · Why: retain the original while excluding participant logistics from shared project files · Instead of: committing the unedited meeting summary.

- 2026-10-03 · Publish the original meeting summary unchanged in notes/ at the user's explicit request, after the privacy check · @ltorrecilla · Affects: source notes, README, and .gitignore · Why: preserve the original alongside the synthesis · Replaces: the earlier decision to keep these meeting notes local; current proposals remain in the design and plan.

- 2026-10-03 · Document Basel-Stadt Geoportal daytime PET as the recommended first-demo heat indicator, conditional on T0 verifying data access and licence; defer arbitrary-time shadow modelling and avoid duplicate shade cooling adjustments · @Derriick · Affects: T0, T1, T2, T4, T5, T6 and design · Why: the official analysis already represents building and tree shade in its modelled 14:00 summer heat stress · Instead of: requiring a new shadow model for the first comparison or presenting scenario PET as live air temperature.
- 2026-10-03 · Prioritise the sources listed in the project resource page whenever they fulfil a project need, subject to checking dataset suitability and reuse terms · @Derriick · Affects: T0, T4 and source selection · Why: start from relevant official local and national resources already identified for the project · Instead of: choosing alternative providers before checking whether a listed source fits.

- 2026-10-03 · Include IWB fountain dataset 100008 for the explicitly noncommercial prototype, retaining IWB attribution and the commercial-use permission restriction; exclude photographs pending separate rights checks · @sergimos · Affects: T0, T4 and source selection · Why: the team confirmed noncommercial use, which the published terms permit · Instead of: excluding the dataset because it is not licensed for unrestricted commercial reuse.

- 2026-10-03 · Include two-route comparison with shade calculated for the current or selected time; retain a separately useful Basel layer-map foundation · @sergimos · Affects: design and build sequence · Why: the team selected route comparison and requested real-time shade · Replaces: the earlier proposal to defer arbitrary-time shadow modelling and use historical PET as the initial comparison basis; geometry extent, stack and computation approach still need agreement.

- 2026-10-03 · Target shade calculation across all Basel, with a full geometry inventory and city-wide performance checks; retain two routes for the first demonstration · @sergimos · Affects: T0, T8, T10, T6 and design · Why: the team selected full-city coverage · Instead of: restricting shade calculations to one neighbourhood; tiled on-demand calculation remains a proposed implementation approach.

- 2026-10-03 · Compare route tradeoffs side by side and let the user choose; show walking time/distance, shaded, exposed and unknown sections, and fountains without a combined score or automatic winner · @sergimos · Affects: T2, T5, T6 and UX · Why: the team selected an informative comparison · Instead of: ranking routes by shade or shortest distance.
