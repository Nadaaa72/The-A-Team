
import pytest

from src.graph import RoadGraph
from src.pathfinding import dijkstra


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
