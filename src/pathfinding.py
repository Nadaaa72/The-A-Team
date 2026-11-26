
import heapq
import time


def dijkstra(graph, start, goal):
    """
    Find the shortest travel-time route between two locations
    using Dijkstra's algorithm.
    """

    # Check that both locations exist in the graph
    if start not in graph.adjacency:
        raise ValueError(f"Unknown starting location: {start}")

    if goal not in graph.adjacency:
        raise ValueError(f"Unknown destination: {goal}")

    # The starting location has a travel time of zero
    distances = {location: float("inf") for location in graph.get_locations()}
    distances[start] = 0

    # Store the previous location to reconstruct the route
    previous = {}

    # Priority queue stores (travel time, location)
    priority_queue = [(0, start)]

    # Track locations already processed
    visited = set()

    # Count how many locations are explored
    nodes_explored = 0

    # Start measuring execution time
    start_time = time.perf_counter()

    while priority_queue:

        # Get the location with the lowest known travel time
        current_distance, current_location = heapq.heappop(priority_queue)

        # Skip locations already processed
        if current_location in visited:
            continue

        visited.add(current_location)
        nodes_explored += 1

        # Stop when the destination is reached
        if current_location == goal:
            break

        # Explore all neighbouring locations
        for neighbour, travel_time in graph.get_neighbours(current_location).items():

            if neighbour in visited:
                continue

            new_distance = current_distance + travel_time

            # Update the shortest distance if a better route is found
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current_location

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbour)
                )

    # Calculate execution time
    execution_time = (time.perf_counter() - start_time) * 1000

    # Return an empty route if the destination cannot be reached
    if distances[goal] == float("inf"):
        return {
            "path": [],
            "total_time": float("inf"),
            "nodes_explored": nodes_explored,
            "execution_time_ms": execution_time
        }

    # Reconstruct the shortest route
    path = []
    current = goal

    while current != start:
        path.append(current)
        current = previous[current]

    path.append(start)
    path.reverse()

    return {
        "path": path,
        "total_time": distances[goal],
        "nodes_explored": nodes_explored,
        "execution_time_ms": execution_time
    }
