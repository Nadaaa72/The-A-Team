import time

from src.pathfinding import astar, dijkstra


def compare_algorithms(graph, responders, incidents, iterations=100):
    """
    Compare A* and Dijkstra across all responder-to-incident journeys.

    Each journey is repeated to obtain a more reliable average
    execution time.
    """

    if iterations < 1:
        raise ValueError("Iterations must be at least 1")

    results = {
        "astar": {},
        "dijkstra": {}
    }

    algorithms = {
        "astar": astar,
        "dijkstra": dijkstra
    }

    for responder, start_location in responders.items():
        for incident, destination in incidents.items():

            journey_results = {}

            for algorithm_name, search_function in algorithms.items():

                # Warm-up run (excluded from measurements)
                search_function(graph, start_location, destination)

                total_execution_time = 0
                final_result = None

                # Repeat the search to measure average execution time
                for _ in range(iterations):
                    start_time = time.perf_counter()

                    final_result = search_function(
                        graph,
                        start_location,
                        destination
                    )

                    end_time = time.perf_counter()

                    total_execution_time += (
                        end_time - start_time
                    ) * 1000

                average_execution_time = (
                    total_execution_time / iterations
                )

                journey_results[algorithm_name] = {
                    "travel_time": final_result["total_time"],
                    "nodes_explored": final_result["nodes_explored"],
                    "execution_time_ms": average_execution_time
                }

            # Check that both algorithms find the same travel time
            astar_time = journey_results["astar"]["travel_time"]
            dijkstra_time = journey_results["dijkstra"]["travel_time"]

            if astar_time != dijkstra_time:
                raise AssertionError(
                    f"Different travel times for {responder} "
                    f"to {incident}"
                )

            for algorithm_name in algorithms:
                results[algorithm_name][(responder, incident)] = (
                    journey_results[algorithm_name]
                )

    return results


def calculate_averages(results):
    """
    Calculate average execution time and nodes explored
    for each pathfinding algorithm.
    """

    averages = {}

    for algorithm, journeys in results.items():

        if not journeys:
            averages[algorithm] = {
                "average_execution_time_ms": 0,
                "average_nodes_explored": 0
            }
            continue

        averages[algorithm] = {
            "average_execution_time_ms": sum(
                journey["execution_time_ms"]
                for journey in journeys.values()
            ) / len(journeys),

            "average_nodes_explored": sum(
                journey["nodes_explored"]
                for journey in journeys.values()
            ) / len(journeys)
        }

    return averages
