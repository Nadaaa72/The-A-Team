# Project Proposal: Emergency Response AI Command Centre
## Dublin Emergency Response AI System: Knowledge-Driven Dispatch and Routing

**Module:** AINL3001 - Knowledge-Driven Artificial Intelligence

**GitHub Repository:** https://github.com/Nadaaa72/The-A-Team

## Group Information

**Name:** The A-Team

| Name | Student Number | GitHub Username | Role | 
|------|----------------|-----------------|-----------------|
| Lea Stanisavljevic | A00046044 | [@bytelea](https://github.com/bytelea) | CSP & Dispatch Optimisation |
| Hania Amear | C24405892 | [@HaniaAmear25](https://github.com/HaniaAmear25) | Dashboard & Visualisation |
| Nada Abassi | C24317713 | [@Nadaaa72](https://github.com/Nadaaa72) | Simulation, Dynamic Replanning & Evaluation |
| Monike Ozeias Santos | C24300243 | [@monikeoz](https://github.com/monikeoz) | Pathfinding & Search Algorithms |
| Richard Taiwo | C24375003 | [@richytaiwo](https://github.com/richytaiwo) | Knowledge Representation & Reasoning |

## 1. Problem Description and Motivation

Emergency dispatch involves making decisions about incident urgency, suitable resources and routes while vehicle availability and road conditions change. Our project proposes a Python-based educational simulation for a selected area of Dublin, combining symbolic reasoning, graph search and constraint satisfaction. The system will use OpenStreetMap road data and simulated incidents, vehicles and traffic conditions. It will not process real patient information or provide operational emergency advice. Research into emergency resource allocation and ambulance demand forecasting demonstrates the importance of efficient resource planning (Kalogiannidis et al., 2026; Butsingkorn et al., 2026).

The initial scope includes medical emergencies, building fires and road collisions, with approximately 5-10 incidents and 6-12 ambulance or fire and rescue vehicles. We will model the system state as S = (I, R, G, A), where I represents incidents and their requirements, R represents responder locations, capabilities and availability, G represents the weighted road network, and A represents current assignments.

Possible actions include assigning responders, updating availability, blocking roads and recalculating routes. Our goal is to find valid assignments that prioritise urgent incidents while keeping estimated response times low. Constraints will prevent double-booking, assigning unsuitable vehicles and selecting unreachable routes. The system will also account for situations where there are not enough available responders.
## 2. Proposed AI Approach

Our approach draws on established methods in search, knowledge representation and constraint satisfaction (Russell and Norvig).

**Knowledge Representation and Reasoning:**

We will use a knowledge base containing incident facts and IF-THEN rules, with forward chaining to infer emergency priorities and resource requirements. For example, a building fire involving trapped occupants could trigger a rule requiring rescue capabilities. The system will record which rules were applied so users can understand how decisions were reached. These rules are simplified for simulation purposes and are not official emergency response protocols.

**Search Algorithms:**

Dublin's road network will be represented as a weighted graph, with edge weights estimating travel time. We will implement A* search to calculate routes between responders and incidents. Dijkstra's algorithm will be used as a baseline for comparison. We will use a straight-line distance heuristic divided by a justified upper-bound travel speed, ensuring it does not overestimate the remaining travel time.

**Constraint Satisfaction:**

Emergency responder allocation will be modelled as a Constraint Satisfaction Problem (CSP). Each required responder role for an incident will be represented as a variable, with a domain of available, suitable and reachable vehicles. Constraints will ensure that responders have the required capabilities and cannot be assigned to multiple simultaneous incidents. An unassigned option will allow the system to handle resource shortages, with higher penalties for leaving urgent incidents unattended.

We will implement backtracking search, Minimum Remaining Values (MRV) and forward checking to improve search efficiency. We will also compare valid assignments using incident priority and estimated response time, while accounting for emergencies that cannot be assigned a responder.


### Figure 1: AI Dispatch Workflow

![AI Dispatch Workflow](Dublin%20Emergency%20Response%20AI%20Workflow.png)

*Figure 1: Proposed workflow showing simulated incidents, knowledge-based reasoning, A* and Dijkstra routing, CSP responder assignment and dashboard visualisation.*

## 3. System Architecture and Implementation

The system will begin with simulated emergency incidents, which will be processed by the knowledge base to determine their priority and required resources. The routing algorithms will calculate travel times, and the CSP solver will assign suitable responders.

A Streamlit dashboard with Folium maps will display incidents, responder locations, routes and dispatch decisions. Users will be able to simulate changes such as road closures, congestion and unavailable vehicles, allowing the system to recalculate affected routes and assignments.

The project will use Python, NetworkX and OSMnx to model Dublin's road network using OpenStreetMap data, following the network modelling approach described by Boeing (2025). Streamlit and Folium will be used for visualisation, while Pytest will support automated testing. We will develop the main AI components first, then integrate them into the dashboard and test the complete system.


### Figure 2: System Architecture

![System Architecture](Dublin%20Emergency%20Dispatch%20Architecture.png)

*Figure 2: Proposed system architecture showing simulated inputs, AI processing components and expected outputs.*

## 4. Individual Team Contributions

- **Lea Stanisavljevic:** CSP modelling, backtracking, MRV, forward checking and dispatch optimisation.
- **Hania Amear:** Streamlit dashboard, Folium maps and visualisation of dispatch decisions.
- **Nada Abassi:** Emergency simulation, dynamic replanning, testing and performance evaluation.
- **Monike Ozeias Santos:** A* and Dijkstra implementation, road network modelling and routing benchmarks.
- **Richard Taiwo:** Knowledge base, IF-THEN rules, forward chaining and explanation traces.

All members will contribute to integration, documentation and the final demonstration.

## 5. Evaluation and Expected Outcomes

We will evaluate the system using simulated scenarios with known expected results. We will also test the knowledge base using predefined incidents to verify that the correct priorities and resource requirements are inferred. A* and Dijkstra will be compared based on route cost, execution time and nodes explored. CSP-based dispatch will be compared with greedy allocation using assignment validity, estimated response times and the number of incidents served.

We will also compare basic backtracking with MRV and forward checking to measure search efficiency. Scenarios involving road closures, increased emergency demand and limited responders will be used to test how the system adapts to changing conditions.

Our expected outcome is a working prototype that demonstrates how knowledge-driven AI techniques can be combined to make explainable emergency dispatch decisions.


## References

1. Russell, S. J. and Norvig, P. *Artificial Intelligence: A Modern Approach*.

2. Kalogiannidis, S. et al. (2026). [Machine Learning Applications in Emergency](https://www.mdpi.com/2504-4990/8/7/182). *Machine Learning and Knowledge Extraction*, 8, 182.

3. Butsingkorn, T., Apichottanakul, A. and Arunyanart, S. (2026). [An Integrated Machine Learning Method for Enhancing Emergency Response Planning](https://www.sciencedirect.com/science/article/pii/S2772662226000421). *Decision Analytics Journal*, 19, 100714.

4. Boeing, G. (2025). Modeling and Analyzing Urban Networks and Amenities with OSMnx. [*Geographical Analysis*](https://arxiv.org/html/2505.00736v1), 57(4), 567-577.

### AI Algorithms and Knowledge Representation

5. AIMA Python. [GitHub Repository](https://github.com/aimacode/aima-python)

6. GeeksforGeeks. [Constraint Satisfaction Problems (CSP) in Artificial Intelligence](https://www.geeksforgeeks.org/artificial-intelligence/constraint-satisfaction-problems-csp-in-artificial-intelligence/)

7. GeeksforGeeks. [Dijkstra's Shortest Path Algorithm](https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/)

8. Inference Systems. [Minimum Remaining Values (MRV) Heuristic](https://inferensys.com/glossary/agentic-cognitive-architectures/constraint-satisfaction-problem-solving/minimum-remaining-values-mrv-heuristic)

9. GeeksforGeeks. [Rule-Based Classifier](https://www.geeksforgeeks.org/machine-learning/rule-based-classifier-machine-learning/)

### Related GitHub Projects

10. [Intelligent Emergency Resource Scheduling and Simulation Platform](https://github.com/just1n9877/Intelligent-Emergency-Resource-Scheduling-Simulation-Platform)

11. [Ambulance Dispatch Route Optimiser](https://github.com/Maxencejules/ambulance-dispatch-systems)

12. [EMS Simulator](https://github.com/EMSTrack/EMS-Simulator)

### Software and Framework Documentation

13. Streamlit. [Official Documentation](https://docs.streamlit.io/)

14. Streamlit. [GitHub Repository](https://github.com/streamlit/streamlit)

15. OSMnx. [Official Documentation](https://osmnx.readthedocs.io/en/stable/)

16. NetworkX. [Official Documentation](https://networkx.org/documentation/stable/)

17. Folium. [Official Documentation](https://folium.readthedocs.io/en/latest/)

### Mapping Data and Tutorials

18. OpenStreetMap Contributors. [OpenStreetMap and Data Licensing](https://www.openstreetmap.org/copyright)

19. Breuss, M. (2025). [Python Folium: Create Web Maps From Your Data](https://realpython.com/python-folium-web-maps-from-data/). *Real Python*.

### Declaration of Generative AI Use:

Generative AI tools (Claude and ChatGPT, including OpenAI's image generation tool) were used to assist with drafting, structuring and formatting this proposal, and to generate the two system diagrams. All written content and diagrams were reviewed by the group, who remain responsible for the project's design decisions and final submission.
