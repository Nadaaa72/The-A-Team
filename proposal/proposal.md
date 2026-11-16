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

### Figure 1: AI Dispatch Workflow

![AI Dispatch Workflow](Dublin%20Emergency%20Response%20AI%20Workflow.png)

*Figure 1: Overview of the proposed knowledge-driven emergency dispatch workflow, from simulated incidents to responder assignment and visualisation.*

The initial scope includes medical emergencies, building fires and road collisions, with approximately 5-10 incidents and 6-12 ambulance or fire and rescue vehicles. We will model the system state as S = (I, R, G, A), where I represents incidents and their requirements, R represents responder locations, capabilities and availability, G represents the weighted road network, and A represents current assignments.

Possible actions include assigning responders, updating availability, blocking roads and recalculating routes. Our goal is to find valid assignments that prioritise urgent incidents while keeping estimated response times low. Constraints will prevent double-booking, assigning unsuitable vehicles and selecting unreachable routes. The system will also account for situations where there are not enough available responders.
## 2. Proposed AI Approach

Our approach draws on established methods in search, knowledge representation and constraint satisfaction (Russell and Norvig).

**Knowledge Representation and Reasoning:**

A knowledge base containing incident facts and IF-THEN rules will use forward chaining to determine required resources and assign simulated priority levels: Critical, High, Medium or Low. For example, a building fire with trapped occupants may require rescue capabilities and receive Critical priority. The system will record the rules applied to explain its decisions. These simplified rules are for educational simulation and are not official emergency response protocols.

**Search Algorithms:**

Dublin's road network will be represented as a weighted graph, with edge weights estimating travel time. We will implement A* search to calculate routes between responders and incidents. Dijkstra's algorithm will be used as a baseline for comparison. We will use a straight-line distance heuristic divided by a justified upper-bound travel speed, ensuring it does not overestimate the remaining travel time.

**Constraint Satisfaction:**

Emergency responder allocation will be modelled as a Constraint Satisfaction Problem (CSP). Each required responder role will be a variable with a domain of suitable, available and reachable vehicles. Constraints will prevent double-booking and incompatible assignments. An unassigned option will represent resource shortages.

We will implement backtracking, Minimum Remaining Values (MRV) and forward checking. Feasible assignments will be compared using a priority-weighted cost function that combines estimated response times with penalties for unassigned incidents. The solver will select the lowest-cost assignment found within the scenario's search limits.

### Figure 2: Priority-Weighted Dispatch Scoring

![Priority-Weighted Dispatch Scoring](Priority%20Cost%20Selection%20Infographic.png)

*Figure 2: Illustrative priority-weighted cost model used to compare feasible responder assignments.*

## 3. System Architecture and Implementation

Simulated incidents will enter the knowledge base, which determines priorities and resource requirements. A* will calculate estimated travel times between available responders and incidents, providing a cost matrix for the CSP solver to evaluate assignments. The system will then display recommended responders, routes and explanations through a Streamlit dashboard with Folium maps.

### Figure 3: Routing Costs and Dynamic Replanning

![Routing Costs and Dynamic Replanning](Routing%20Costs%20to%20CSP%20Dispatch%20Feedback%20Loop.png)

*Figure 3: Proposed routing-to-CSP integration and recalculation of affected assignments when conditions change.*

Users can simulate road closures, congestion and vehicle unavailability. When conditions change, affected travel times and assignments will be recalculated, retaining existing assignments where possible.

Python, NetworkX and OSMnx will support road-network modelling using OpenStreetMap data, following Boeing (2025). Pytest will support automated testing. The AI components will be developed and tested before dashboard integration.

### Figure 4: System Architecture

![System Architecture](Dublin%20Emergency%20Dispatch%20Architecture.png)

*Figure 4: Proposed system components, simulated inputs and expected outputs.*

## 4. Individual Team Contributions

- **Lea Stanisavljevic:** CSP modelling, backtracking, MRV, forward checking and dispatch optimisation.
- **Hania Amear:** Streamlit dashboard, Folium maps and visualisation of dispatch decisions.
- **Nada Abassi:** Emergency simulation, dynamic replanning, testing and performance evaluation.
- **Monike Ozeias Santos:** A* and Dijkstra implementation, road network modelling and routing benchmarks.
- **Richard Taiwo:** Knowledge base, IF-THEN rules, forward chaining and explanation traces.

All members will contribute to integration, documentation and the final demonstration.

## 5. Evaluation and Expected Outcomes

Predefined scenarios will test whether forward chaining infers the expected priorities and resource requirements. A* and Dijkstra will be compared using route cost, execution time and nodes explored. CSP dispatch will be compared with greedy allocation using assignment validity, incidents served and priority-weighted response cost. Basic backtracking will be compared with MRV and forward checking using search effort.

Road closures, congestion and responder shortages will test replanning correctness and execution time. The expected outcome is a working simulation demonstrating explainable, priority-aware emergency dispatch.

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

Generative AI tools (Claude and ChatGPT, including OpenAI's image generation tool) were used to assist with drafting, structuring and formatting this proposal, and to generate the diagrams. All written content and diagrams were reviewed by the group, who remain responsible for the project's design decisions and final submission.
