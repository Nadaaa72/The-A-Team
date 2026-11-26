import pytest

from src.graph import RoadGraph
from src.travel_matrix import calculate_travel_matrix


@pytest.fixture
def sample_network():
    graph = RoadGraph()

    graph.add_road("Hospital", "City Centre", 8)
    graph.add_road("Hospital", "Airport", 12)
    graph.add_road("City Centre", "Incident 1", 5)
    graph.add_road("Airport", "Incident 1", 7)

    responders = {
        "Ambulance 1": "Hospital",
        "Fire Engine 1": "Airport"
    }

    incidents = {
        "Incident 1": "Incident 1"
    }

    return graph, responders, incidents


def test_astar_travel_matrix(sample_network):
    graph, responders, incidents = sample_network

    result = calculate_travel_matrix(
        graph, responders, incidents, algorithm="astar"
    )

    assert result == {
        "Ambulance 1": {"Incident 1": 13},
        "Fire Engine 1": {"Incident 1": 7}
    }


def test_dijkstra_travel_matrix(sample_network):
    graph, responders, incidents = sample_network

    result = calculate_travel_matrix(
        graph, responders, incidents, algorithm="dijkstra"
    )

    assert result == {
        "Ambulance 1": {"Incident 1": 13},
        "Fire Engine 1": {"Incident 1": 7}
    }


def test_unreachable_incident():
    graph = RoadGraph()
    graph.add_location("Hospital")
    graph.add_location("Incident 1")

    responders = {"Ambulance 1": "Hospital"}
    incidents = {"Incident 1": "Incident 1"}

    result = calculate_travel_matrix(graph, responders, incidents)

    assert result["Ambulance 1"]["Incident 1"] == float("inf")


def test_invalid_algorithm(sample_network):
    graph, responders, incidents = sample_network

    with pytest.raises(ValueError):
        calculate_travel_matrix(
            graph, responders, incidents, algorithm="invalid"
        )


def test_multiple_incidents():
    graph = RoadGraph()
    graph.add_road("Hospital", "Incident 1", 5)
    graph.add_road("Hospital", "Incident 2", 10)

    responders = {"Ambulance 1": "Hospital"}
    incidents = {
        "Incident 1": "Incident 1",
        "Incident 2": "Incident 2"
    }

    result = calculate_travel_matrix(graph, responders, incidents)

    assert result == {
        "Ambulance 1": {
            "Incident 1": 5,
            "Incident 2": 10
        }
    }