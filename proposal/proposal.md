# Project Proposal: Emergency Response AI Command Centre

AINL3001 Knowledge-Driven AI · Group Project Proposal · Deliverable 1

> **Note for the team:** each person writes their own section(s) under the headings below and commits it themselves. Keep the whole proposal to about 500–800 words, so aim for roughly 80–120 words each. Delete this note before submitting.

## 1. Team Information

**Group name:** The A-Team

| Name | Student Number | GitHub Username |
|------|----------------|-----------------|
| Nada Abassi | C24317713 | Nadaaa72 |
| TODO | TODO | TODO |
| TODO | TODO | TODO |
| TODO | TODO | TODO |
| TODO | TODO | TODO |

## 2. Problem Description

## 3. Proposed AI Approach

## 4. System Design

## 5. Scope, Feasibility and Evaluation

**Minimum viable scope:** one small city graph (about 15–20 junctions), 3–5 responders, 5–8 synthetic incidents and a few road closures. This is small enough to finish and test before 30 November.

**Evaluation:** Most research on ambulance services measures performance using response time and coverage, which is the percentage of calls reached within a target time (Erkut et al., 2008). We'll use both, along with a few measures specific to our AI techniques:

| Metric | What it tells us |
|--------|------------------|
| Average travel cost | How quickly responders reach incidents overall |
| Critical incident response time | Whether the most urgent incidents are actually served first |
| Coverage | Percentage of incidents reached within a target time |
| Incidents assigned (%) | How many incidents got a suitable responder |
| Constraint violations | Wrong equipment, double-booked units or full hospitals (CSP vs. greedy) |
| Nodes expanded and runtime | How efficient each search algorithm is (A\* vs. BFS/UCS) |

We'll run each method on three test scenarios: a normal day (5 incidents, 5 responders), a busy day (8 incidents, 3 responders) and a road closure scenario where a road is closed partway through. The results will be shown in tables and charts.

**Demo plan:** run a normal scenario, then add a new critical incident and close a road. The system should reroute the affected responder and show the facts and rules behind its new decision.

**Stretch goal (dynamic replanning):** when a road closes, any responder using it gets a new route by running A\* again from where it currently is. Since our map is small this should be quick. On large real road networks, incremental algorithms like D\* Lite (Koenig and Likhachev, 2002) would be better because they only fix the part of the route that changed. We'll only attempt this once the core system passes its tests.

## 6. Planned Contributions

## References

- Erkut, E., Ingolfsson, A. and Erdoğan, G. (2008) 'Ambulance location for maximum survival', *Naval Research Logistics*, 55(1), pp. 42–58.
- Koenig, S. and Likhachev, M. (2002) 'D\* Lite', *Proceedings of AAAI-02*, pp. 476–483.

> [TODO – everyone: add any sources you use here, in the same style.]

## Acknowledgement of AI Use

Generative AI (Claude) was used to help draft and structure this proposal. The group reviewed and edited the content and is responsible for all design decisions.
