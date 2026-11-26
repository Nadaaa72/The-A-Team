
import pytest

from src.graph import RoadGraph
from src.pathfinding import dijkstra, astar, haversine_distance


def test_dijkstra_finds_shortest_route():
    graph = RoadGraph()

    graph.add_road("Hospital", "City Centre", 8)
    graph.add_road("Hospital", "Airport", 12)
    graph.add_road("City Centre", "Incident", 5)
    graph.add_road("Airport", "Incident", 7)

    result = dijkstra(graph, "Hospital", "Incident")

    assert result["path"] == [
        "Hospital",
        "City Centre",
        "Incident"
    ]
    assert result["total_time"] == 13


def test_dijkstra_returns_empty_path_when_unreachable():
    graph = RoadGraph()

    graph.add_road("Hospital", "City Centre", 8)
    graph.add_location("Incident")

    result = dijkstra(graph, "Hospital", "Incident")

    assert result["path"] == []
    assert result["total_time"] == float("inf")


def test_dijkstra_when_start_equals_goal():
    graph = RoadGraph()
    graph.add_location("Hospital")

    result = dijkstra(graph, "Hospital", "Hospital")

    assert result["path"] == ["Hospital"]
    assert result["total_time"] == 0


def test_dijkstra_rejects_unknown_start():
    graph = RoadGraph()
    graph.add_location("Hospital")

    with pytest.raises(ValueError):
        dijkstra(graph, "Unknown", "Hospital")


def test_dijkstra_rejects_unknown_destination():
    graph = RoadGraph()
    graph.add_location("Hospital")

    with pytest.raises(ValueError):
        dijkstra(graph, "Hospital", "Unknown")

def test_astar_finds_shortest_route():
    graph = RoadGraph()

    graph.add_location("Hospital", (53.3438, -6.2546))
    graph.add_location("City Centre", (53.3500, -6.2600))
    graph.add_location("Airport", (53.4264, -6.2499))
    graph.add_location("Incident", (53.4265, -6.2500))

    graph.add_road("Hospital", "City Centre", 8)
    graph.add_road("Hospital", "Airport", 12)
    graph.add_road("City Centre", "Incident", 10)
    graph.add_road("Airport", "Incident", 7)

    result = astar(graph, "Hospital", "Incident")

    assert result["path"] == [
        "Hospital",
        "City Centre",
        "Incident"
    ]
    assert result["total_time"] == 18


def test_astar_matches_dijkstra():
    graph = RoadGraph()

    graph.add_road("Hospital", "City Centre", 8)
    graph.add_road("Hospital", "Airport", 12)
    graph.add_road("City Centre", "Incident", 10)
    graph.add_road("Airport", "Incident", 7)

    dijkstra_result = dijkstra(graph, "Hospital", "Incident")
    astar_result = astar(graph, "Hospital", "Incident")

    assert astar_result["total_time"] == dijkstra_result["total_time"]


def test_astar_handles_missing_coordinates():
    graph = RoadGraph()

    graph.add_road("Hospital", "City Centre", 8)
    graph.add_road("City Centre", "Incident", 5)

    result = astar(graph, "Hospital", "Incident")

    assert result["path"] == [
        "Hospital",
        "City Centre",
        "Incident"
    ]
    assert result["total_time"] == 13


def test_astar_rejects_invalid_max_speed():
    graph = RoadGraph()
    graph.add_location("Hospital")

    with pytest.raises(ValueError):
        astar(graph, "Hospital", "Hospital", max_speed_kmh=0)
