# Future features

## Phone access for people without a smartphone or internet

**Status:** Deferred until the core web-app demo is ready.

### Goal

Let people using a basic phone or landline access the same route-planning help as the map: routes that consider shade, confirmed construction closures, and other known risks. The service must never claim that a route is safe when that has not been verified. It must state clearly when route information is missing or uncertain.

### Agreed demo direction

Use a scripted call simulation, not a live phone number. The caller chooses from prepared Basel locations, receives a route recommendation and directions, and can request a map for later. Map delivery is the priority extension: the caller can choose postal delivery to their home or an email to a neighbour who can print it. For the demo, show a confirmation only. Do not ask for or store a real home address or email, and do not actually send a map.

Use the same route scenario and evidence as the web demo. Label simulated or unverified data. The call must explain missing information and avoid presenting the recommendation as a guarantee of safety.

### Infrastructure notes for a later implementation

A call simulation can be demonstrated inside the web app without buying a phone number. Open-source [Asterisk](https://www.asterisk.org/products/software/) is free phone-server software, but reaching ordinary phone networks still requires a provider, number, and call service. As checked on 2026-10-03, [Twilio's Switzerland pricing](https://www.twilio.com/en-us/voice/pricing/ch) lists a local number at $1.15/month and incoming calls at $0.01/minute; its [free trial restrictions](https://help.twilio.com/hc/en-us/articles/360036052753-Twilio-Free-Trial-Limitations) limit calls to verified numbers, so a trial is for testing rather than a public service. Recheck costs and availability before a pilot. Postal delivery also has per-item costs and operational work.

### Before building a live service

- Verify that the web demo's route data and missing-data behavior can be reused by the phone flow.
- Check Swiss phone-number availability, provider costs, and call reliability.
- Decide supported languages and how callers can repeat or slow down directions.
- Define a privacy-conscious process for handling a postal address or a neighbour's email, including consent, retention, and deletion.
- Confirm who would prepare and send printed maps and how delivery timing is represented.

The first demo only shows the scripted interaction and simulated map-request confirmation. Live calls and actual map delivery remain future work.
