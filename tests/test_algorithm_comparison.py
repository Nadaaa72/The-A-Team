import pytest

from src.sample_network import (
    create_sample_network,
    create_sample_responders,
    create_sample_incidents
)

from src.algorithm_comparison import (
    compare_algorithms,
    calculate_averages
)


@pytest.fixture
def comparison_results():
    graph = create_sample_network()
    responders = create_sample_responders()
    incidents = create_sample_incidents()

    return compare_algorithms(
        graph, responders, incidents, iterations=10
    )


def test_comparison_includes_both_algorithms(comparison_results):
    assert "astar" in comparison_results
    assert "dijkstra" in comparison_results


def test_comparison_includes_all_journeys(comparison_results):
    assert len(comparison_results["astar"]) == 12
    assert len(comparison_results["dijkstra"]) == 12


def test_both_algorithms_find_same_travel_times(comparison_results):
    for journey in comparison_results["astar"]:
        assert (
            comparison_results["astar"][journey]["travel_time"]
            == comparison_results["dijkstra"][journey]["travel_time"]
        )


def test_execution_times_are_non_negative(comparison_results):
    for algorithm in comparison_results.values():
        for journey in algorithm.values():
            assert journey["execution_time_ms"] >= 0


def test_calculate_averages(comparison_results):
    averages = calculate_averages(comparison_results)

    assert averages["astar"]["average_execution_time_ms"] >= 0
    assert averages["dijkstra"]["average_execution_time_ms"] >= 0

    assert averages["astar"]["average_nodes_explored"] > 0
    assert averages["dijkstra"]["average_nodes_explored"] > 0


def test_invalid_iterations():
    graph = create_sample_network()

    with pytest.raises(ValueError):
        compare_algorithms(
            graph,
            create_sample_responders(),
            create_sample_incidents(),
            iterations=0
        )
