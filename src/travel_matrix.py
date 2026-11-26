from src.pathfinding import astar, dijkstra


def calculate_travel_matrix(graph, responders, incidents, algorithm="astar"):
    """
    Calculate the travel time from each responder to each incident.

    Returns a dictionary containing the shortest travel time
    between every responder and incident.
    """

    # Select which pathfinding algorithm to use
    if algorithm == "astar":
        search = astar
    elif algorithm == "dijkstra":
        search = dijkstra
    else:
        raise ValueError("Algorithm must be 'astar' or 'dijkstra'")

    travel_times = {}

    # Calculate travel time for each responder and incident
    for responder, start_location in responders.items():
        travel_times[responder] = {}

        for incident, destination in incidents.items():
            result = search(graph, start_location, destination)

            travel_times[responder][incident] = result["total_time"]

    return travel_times 

