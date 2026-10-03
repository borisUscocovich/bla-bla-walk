# 10-02 Meeting: Heat- and Safety-Aware Routing Map App

> **Date & Time:** 2026-10-02 20:00:14 **Location:** \[Insert Location\] **Attendees:** Speaker 1, Speaker 2, Speaker 3, Speaker 4, Speaker 5, Speaker 6, Speaker 7

## 1\. Core App Concept: Heat- and Safety-Aware Routing Map

### Conclusion

The team converged on developing a map-based application that recommends the safest walking routes for vulnerable populations (elderly, children, pregnant women, people with chronic illnesses), particularly during extreme weather like heat waves and cold spells. The app will prioritize safety over speed, optimizing routes for factors like temperature, shade, water fountain access, and public transport alternatives, while avoiding hazards like construction closures. The solution will leverage public and open datasets from sources like Swiss Topo, OpenStreetMap, and MeteoSwiss. The primary access channel will be a website/web app, complemented by a phone-call bot to serve users without smartphones.

### Plan

- [ ] Review all available data sources to determine which app features are technically feasible \-- *Speaker 1* *Speaker 2*  
- [ ] Connect the app to MeteoSwiss for weather data integration \-- *Speaker 1* *Speaker 3*  
- [ ] Define core features vs. stretch features based on data availability and scope \-- *Speaker 1* *Speaker 2* *Speaker 3* *Speaker 4*  
- [ ] Build a base map/navigation tool that helps users reach cool rooms via the safest routes during heatwaves, leveraging Basel’s public data \-- *\[Insert Executor Names\]*  
- [ ] Aggregate Swiss Topo and OpenStreetMap layers (topography, hiking trails, shade/trees) and integrate LV95/WGS84 conversion in backend services \-- *\[Insert Executor Names\]*  
- [ ] Ingest Basel and Swiss public datasets (heat maps, sensors, fountains, trees, population by quarter, cantonal heat map, health info) \-- *\[Insert Executor Names\]*  
- [ ] Implement coordinate conversion from LV95 to WGS84 for web map layers \-- *\[Insert Executor Names\]*  
- [ ] Integrate public transport datasets (OVA/SBB timetables) to suggest nearest stations and routes \-- *\[Insert Executor Names\]*  
- [ ] Implement routing that optimizes for safety (shade, water access, avoid construction) with dynamic conditions \-- *\[Insert Executor Names\]*  
- [ ] Build a feedback/reporting feature for users to flag closures, construction sites, and fountain outages \-- *\[Insert Executor Names\]*  
- [ ] Develop a web app first, with mobile-friendly design and potential kiosk/screen mode for hospitals and elderly homes \-- *\[Insert Executor Names\]*  
- [ ] Create a phone-call bot interface for users without smartphones to request and receive route guidance \-- *\[Insert Executor Names\]*  
- [ ] Iteratively expand features to cover additional dangerous conditions (ice, heavy rain) after the base is working \-- *\[Insert Executor Names\]*

### Discussion Points

1. **Core Functionality:** The app's main purpose is to recommend safe routes, not necessarily the shortest ones, by accounting for shade, trees, water fountains, and cooler microclimates, especially during heat waves. It should also issue alerts for approaching storms.  
2. **Target Users & Accessibility:** The primary targets are vulnerable individuals and their caregivers. Since many at-risk users (elderly, children) lack smartphones, a phone-call interface is crucial. The app will use personalized, profile-based recommendations (e.g., shorter routes for the elderly) without collecting sensitive personal data like age, relying instead on self-declared risk categories (e.g., pregnant, high-risk). Accessibility barriers like roads without proper crossings must be factored into routing.  
3. **Weather Scope:** The primary focus is on heat waves, as specified in the challenge, but the app will also cover extreme cold to be useful year-round. It will be designed for future extensibility to other weather conditions.  
4. **Data Sources:** The app will integrate various datasets, including MeteoSwiss for weather, Swiss Topo and OpenStreetMap for base maps and features (trails, trees), and public transport data (OVA/SBB). Public data from Basel (heat maps, cool rooms, fountains) is also key. A critical step is to audit data availability to determine feature feasibility.  
5. **Dynamic Conditions:** The app must reflect dynamic local conditions, such as construction sites or out-of-service water fountains, to be reliable. A user feedback system will be included for reporting such issues.

---

## 2\. Social and Collaborative Features

### Conclusion

The team agreed that a social component is a valuable addition to the core safety features. Two main ideas were discussed: a "Waze-like" collaborative model for assistance and a feature for matching volunteers with vulnerable individuals for accompanied walks. This social aspect will be considered a secondary phase, to be built upon the foundational mapping tool, with strong emphasis on safety and vetting protocols.

### Plan

- [ ] Explore optional social feature to connect volunteers with elderly users for accompaniment, leveraging the same backend \-- *\[Insert Executor Names\]*  
- [ ] Explore integration of a voluntary social assistance component for pick-ups/groceries once privacy and vetting mechanisms are designed \-- *\[Insert Executor Names\]*  
- [ ] Design vetting mechanisms for volunteers (identity verification, background checks) to ensure safety \-- *\[Insert Executor Names\]*  
- [ ] Define operational workflows for requesting and delivering assistance (rides to appointments, grocery pickups) \-- *\[Insert Executor Names\]*  
- [ ] Assess legal and liability aspects of a community help model before any pilot \-- *\[Insert Executor Names\]*

### Discussion Points

1. **Accompanied Walks:** Healthy volunteers could use the app to find and accompany vulnerable users (e.g., elderly in care homes) on safe walks, with the app guiding the route. This promotes both safety and social interaction.  
2. **Community Assistance ("Uber for Elderly"):** The app could facilitate community-driven assistance, where volunteers help with errands like grocery runs or provide rides to appointments during extreme weather.  
3. **Safety and Vetting:** For any social feature, robust safety and vetting mechanisms are essential to prevent abuse and ensure user trust. This was a primary concern.  
4. **Focus on Assistance, Not Gamification:** The core value of the social feature is helping vulnerable people, not motivating them through gamification. The focus remains on safety and assistance.

---

## 3\. Technical Strategy, Data, and Compliance

### Conclusion

The team will use the provided technical harness and tools (like Codex) to streamline development. The initial scope will be kept small and focused on a working prototype, with more complex features like on-device LLMs planned for a later phase. All code will be managed in a shared Git repository. The project will use public and aggregated data, avoiding personal health data to comply with GDPR, and all data sources will be clearly licensed and cited within the app.

### Plan

- [ ] All team members should read the `hackandrhyme.md` file and review the repository to understand the project setup. \-- *All*  
- [ ] Clearly state licenses and data source origins within the app for all datasets used. \-- *\[Insert Executor Names\]*  
- [ ] Validate data freshness and real-time integration for routing decisions \-- *\[Insert Executor Names\]*

### Discussion Points

1. **Technology Stack:** The team will leverage the provided project harness to simplify model interaction and setup. While provided tools are primary, personal cloud subscriptions (e.g., for Claude) can be used for brainstorming. Deployment could use free VPS options or a local computer for the prototype.  
2. **Data & Privacy:** The solution will strictly use public and aggregated data to respect privacy and GDPR. Risk profiling will be non-identifying and consent-based. The Swiss data coordinate system (LV95) will need to be converted to WGS84 for web map compatibility, a task for the backend.  
3. **Scope Management:** The team agreed to keep the initial scope small and focused to ensure a deliverable prototype. Advanced features, such as deploying a small LLM on an edge device for privacy, are considered good ideas for a second phase.  
4. **Smartwatch Integration:** Connecting to smartwatches for real-time health monitoring (heart rate, O2 levels) was discussed but identified as a non-priority "stretch" feature.

---

## 4\. Team Organization and Logistics

### Conclusion

The team has a diverse and relevant skillset, including architecture, robotics, software development, and cybersecurity/AI. The group agreed on the team name **"blablabook"** and will prioritize collaboration and fun over strict competition rules. A private Discord channel will be used for communication. The next work session is scheduled to narrow the project scope and divide tasks. Speaker 3 will lead the final presentation, with support from Speaker 1\.

### Plan

- [ ] Create the team repository under the name "blablabook" \-- *Speaker 5*  
- [ ] Create a private Discord channel for team communication. \-- *Speaker 1* *Speaker 3*  
- [ ] Meet at Markthalle to continue working on the project. \-- *All* 2026-10-03 at 9 AM  
- [ ] Upload the meeting recording to a shared document to feed to an LLM for summary. \-- *Speaker 3*  
- [ ] Bring a 2 terabyte SSD with fast data processing capabilities. \-- *Speaker 7* 2026-10-03  
- [ ] Bring a Wi-Fi router. \-- *Speaker 3* 2026-10-03  
- [ ] Bring any missing items like multi-plugs or coffee. \-- *Speaker 1* 2026-10-03  
- [ ] Speaker 3 will take the lead on the final presentation, with support from Speaker 1\. \-- *Speaker 3* *Speaker 1*

### Discussion Points

1. **Team Skills:** The team includes a "real" architect (focused on people), a robotics/software specialist, a software architect, and a cybersecurity/AI specialist, providing a strong foundation for the project.  
2. **Working Style:** The team values a collaborative and flexible approach, with a focus on creating something useful and having fun.  
3. **Next Steps:** The immediate next step is a meeting at Markthalle at 9 AM on Oct 3 to finalize the MVP scope and assign specific tasks.  
4. **Communication:** A private Discord channel is needed to coordinate work effectively. The final presentation is a key deliverable, and time will be allocated for its creation.

---

> **AI Suggestions** AI has identified the following issues that were not concluded in the meeting or lack clear action items; please pay attention:

> 1. **Execution Ownership and Timelines are Missing:** Many crucial tasks (building the base map, data ingestion, coordinate conversion, phone-bot design) lack assigned executors and deadlines. Defining responsible individuals and target dates is critical to ensure progress.  
> 2. **MVP Feature Set is Undefined:** While many ideas were discussed, the team did not decide on a concrete Minimum Viable Product (MVP) feature set. A prioritization session is needed to lock in the core vs. stretch features to focus development efforts.  
> 3. **Data Strategy and Availability is Unverified:** The project's success hinges on external datasets (MeteoSwiss, real-time heat maps, construction closures, etc.). A plan to audit, source, and integrate these specific datasets is needed, including handling of dynamic/real-time feeds.  
> 4. **Accessibility for Non-Smartphone Users Needs a Concrete Plan:** The phone-call bot and integration with existing hotlines were mentioned as key for accessibility, but the technical approach, UX design, and escalation protocols were not defined.  
> 5. **Volunteer Vetting and Safety Protocols are Undefined:** For the social assistance features, the group acknowledged safety concerns but did not define specific vetting methods (background checks, ID verification), liability handling, or incident response protocols. These must be established before any pilot.