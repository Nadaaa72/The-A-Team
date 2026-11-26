
import heapq
import time
import math

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

def haversine_distance(coord1, coord2):
    """
    Calculate the straight line distance between two geographical coordinates in km
    Coordinates use latitude and longitude
    """

    # Convert lat and long from degrees to radians
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)

    # Calculate differences between coords
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = (
    math.sin(dlat / 2) ** 2 +
    math.cos(lat1) * math.cos(lat2) *
    math.sin(dlon / 2) ** 2
    )

    # Calculate distance using earth's radius
    earth_radius = 6371

    distance = 2 * earth_radius * math.asin(math.sqrt(a))

    return distance 


def astar(graph, start, goal, max_speed_kmh=60):
    """
    Find the shortest travel-time route using A* search.

    The heuristic estimates remaining travel time using
    straight line geographical distance.
    """

    if start not in graph.adjacency:
        raise ValueError(f"Unknown starting location: {start}")

    if goal not in graph.adjacency:
        raise ValueError(f"Unknown destination: {goal}")

    if max_speed_kmh <= 0:
        raise ValueError("Maximum speed must be positive")

    # Get geographical coords
    start_coords = graph.get_coordinates(start)
    goal_coords = graph.get_coordinates(goal)

    # Use zero heuristic if coords are unavailable
    def heuristic(location):
        location_coords = graph.get_coordinates(location)

        if location_coords is None or goal_coords is None:
            return 0

        distance = haversine_distance(location_coords, goal_coords)

        # Convert estimated distance into travel time in mins
        return (distance / max_speed_kmh) * 60

    # Store the shortest known travel time
    distances = {
        location: float("inf")
        for location in graph.get_locations()
    }
    distances[start] = 0

    # Store previous locations to reconstruct the route
    previous = {}

    # Priority queue stores (estimated total cost, actual cost, location)
    priority_queue = [(heuristic(start), 0, start)]

    visited = set()
    nodes_explored = 0

    start_time = time.perf_counter()

    while priority_queue:

        estimated_cost, current_distance, current = heapq.heappop(
            priority_queue
        )

        if current in visited:
            continue

        visited.add(current)
        nodes_explored += 1

        if current == goal:
            break

        for neighbour, travel_time in graph.get_neighbours(current).items():

            if neighbour in visited:
                continue

            new_distance = current_distance + travel_time

            if new_distance < distances[neighbour]:

                distances[neighbour] = new_distance
                previous[neighbour] = current

                estimated_total = new_distance + heuristic(neighbour)

                heapq.heappush(
                    priority_queue,
                    (estimated_total, new_distance, neighbour)
                )

    execution_time = (time.perf_counter() - start_time) * 1000

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
