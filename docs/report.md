# Project Report

To be completed for Deliverable 2.

This report documents the design, implementation, and evaluation of the Emergency Response AI Command Centre. It describes the system components developed by the team, the AI techniques used, testing, and evaluation results.

## 1. Pathfinding and Search

### 1.1 Overview
The Pathfinding and Search component is responsible for calculating efficient routes between emergency responders and incident locations. It uses a weighted road graph to represent the simulated road network, where locations are represented as nodes and roads are represented as edges. Each edge has an estimated travel time in minutes.

Two shortest-path algorithms were implemented: Dijkstra's algorithm and A* search. Dijkstra's algorithm provides a baseline for finding the shortest route, while A* uses a heuristic to guide the search towards the destination. Both algorithms return the selected route, total estimated travel time, number of nodes explored, and execution time.

### 1.2 Road Network Representation

The road network was implemented in `src/graph.py` using a weighted graph data structure. The `RoadGraph` class stores locations in an adjacency dictionary, with each location connected to its neighbouring locations and the corresponding travel time.

Each location can also store geographical coordinates (latitude and longitude). These coordinates are used by the A* algorithm to calculate the estimated straight-line distance between locations.

The graph supports bidirectional roads, meaning that a connection can be travelled in both directions. Travel times are stored as edge weights, allowing the pathfinding algorithms to compare alternative routes and identify the route with the lowest total estimated travel time.

A sample network was created in `src/sample_network.py` to test the system. It contains seven locations, including emergency service bases, hospitals and incident locations, connected by ten bidirectional roads. The network uses simulated locations and estimated travel times rather than live road or traffic data.

### 1.3 Dijkstra's Algorithm

Dijkstra's algorithm was implemented in `src/pathfinding.py`. It calculates the shortest path between a starting location and a destination by repeatedly selecting the unvisited node with the lowest known travel cost.

The algorithm maintains the shortest known distance to each node and updates these distances when a cheaper route is discovered through a neighbouring node. Once the destination is reached, the route is reconstructed using the recorded predecessor nodes.

Dijkstra's algorithm was used as the baseline for evaluating the performance of A*. It guarantees an optimal shortest path when all edge weights are non-negative, which is the case in the implemented road network.

### 1.4 A* Search Algorithm

A* search was also implemented in `src/pathfinding.py`. It uses the same weighted road graph as Dijkstra's algorithm but introduces a heuristic to guide the search towards the destination.

The heuristic estimates the remaining travel time using the Haversine formula, which calculates the straight-line geographical distance between two coordinates on the Earth's surface. This distance is converted into an estimated travel time using an assumed maximum speed of 60 km/h.

The algorithm combines the known travel cost from the starting location with the estimated remaining cost to prioritise which node to explore next. This helps guide the search towards promising routes rather than exploring every possible direction.

The heuristic assumes that 60 km/h is an upper bound on the average speed represented by the simulated road connections. This assumption is important for maintaining the optimality of the search.

### 1.5 Travel Time Matrix

The travel time matrix was implemented in `src/travel_matrix.py`. Its purpose is to calculate the estimated travel time from each emergency responder to each incident.

The function `calculate_travel_matrix()` accepts a road graph, a dictionary of responders, a dictionary of incidents, and the selected pathfinding algorithm. It supports both A* and Dijkstra's algorithms.

The output is a nested dictionary containing the estimated travel time for every responder and incident combination. This allows the system to compare how quickly different emergency responders can reach different incidents.

If a destination cannot be reached, its travel time is represented as infinity. This makes unreachable routes distinguishable from valid routes.

### 1.6 Algorithm Comparison and Evaluation

To evaluate the two pathfinding algorithms, a comparison module was developed in `src/algorithm_comparison.py`.

The comparison measures three main metrics:

- **Execution time:** the average time taken by each algorithm to calculate a route.
- **Nodes explored:** the average number of nodes visited during the search.
- **Travel time:** the total estimated travel time of the selected route.

The benchmark was performed across all responder and incident combinations in the sample network. Each algorithm was executed 100 times per journey, with an initial warm-up execution excluded from the measurements. Average execution times were then calculated to reduce the impact of individual timing variations.

Both algorithms returned identical shortest travel times for all 12 responder and incident combinations.

The results were as follows:

| Metric | A* Search | Dijkstra's Algorithm |
|---|---:|---:|
| Average execution time (ms) | 0.01125 | 0.00467 |
| Average nodes explored | 3.42 | 3.92 |

A* explored approximately 12.8% fewer nodes than Dijkstra's algorithm. However, Dijkstra's algorithm was faster in terms of average execution time in this particular test.

This result demonstrates that exploring fewer nodes does not necessarily mean an algorithm will execute faster, particularly when using a small graph where processing overhead can have a significant impact. The sample network is relatively small, so these results should not be treated as evidence that one algorithm will always outperform the other on larger road networks.

### 1.7 Testing

Unit tests were created to verify the correctness of the pathfinding and travel matrix implementations.

The tests cover:

- Finding valid shortest paths.
- Calculating the correct total travel time.
- Handling unreachable destinations.
- Handling unknown starting locations and destinations.
- Handling a starting location that is already the destination.
- Validating the A* heuristic and maximum speed parameter.
- Calculating travel times for multiple responders and incidents.
- Supporting both A* and Dijkstra's algorithms.
- Rejecting invalid algorithm selections.
- Comparing the results of both algorithms.

The project currently contains 20 passing tests across the pathfinding, travel matrix and algorithm comparison test files.

The full test suite was executed using `pytest`, with all 20 tests passing successfully.

### 1.8 Limitations and Future Improvements

The current implementation uses a small simulated road network with estimated travel times. It does not currently use live traffic information, real road data or changing traffic conditions.

Future improvements could include integrating real road network data, incorporating live traffic conditions into edge weights, and expanding the network to include more locations and emergency responders.

The pathfinding component is also intended to work alongside the team's responder allocation component. Further integration will allow the calculated travel time matrix to support the allocation of emergency responders to incidents.