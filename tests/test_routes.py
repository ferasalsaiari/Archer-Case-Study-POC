"""
Unit tests for route planning logic.
Tests graph construction and shortest path algorithms.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from route_planner import build_graph, find_route, get_route_distance
from data import locations


def test_graph_respects_battery_range():
    """
    Test that graph construction only creates edges within battery range.
    
    With a 150-mile range, LA to Bakersfield (110 mi) should have an edge,
    but LA to Fresno (220 mi) should not.
    """
    battery_range = 150
    graph = build_graph(battery_range)
    
    # Should have edge from LA to Bakersfield (110 miles < 150)
    assert graph.has_edge("Los Angeles", "Bakersfield")
    
    # Should NOT have edge from LA to Fresno (220 miles > 150)
    assert not graph.has_edge("Los Angeles", "Fresno")
    
    # Should have edge from Bakersfield to Fresno (110 miles < 150)
    assert graph.has_edge("Bakersfield", "Fresno")


def test_graph_with_large_battery_range():
    """
    Test that with a large battery range, all cities are connected.
    """
    battery_range = 500  # Large enough to connect all cities
    graph = build_graph(battery_range)
    
    # All cities should be reachable from Los Angeles
    cities = list(locations.keys())
    for city in cities:
        if city != "Los Angeles":
            # Should be able to find a path
            route = find_route(graph, "Los Angeles", city)
            assert route is not None
            assert len(route) >= 2


def test_route_exists_la_to_sf():
    """
    Test that a route exists from Los Angeles to San Francisco with reasonable range.
    """
    battery_range = 250
    graph = build_graph(battery_range)
    
    route = find_route(graph, "Los Angeles", "San Francisco")
    
    # Route should exist
    assert route is not None
    
    # Route should start at LA and end at SF
    assert route[0] == "Los Angeles"
    assert route[-1] == "San Francisco"
    
    # Route should have multiple stops (not direct)
    assert len(route) > 2


def test_no_route_with_insufficient_range():
    """
    Test that no route is found when battery range is too small.
    """
    battery_range = 50  # Too small to connect any cities
    graph = build_graph(battery_range)
    
    route = find_route(graph, "Los Angeles", "San Francisco")
    
    # Should return None (no path exists)
    assert route is None


def test_route_distance_calculation():
    """
    Test that route distance is calculated correctly.
    """
    # Simple route: LA -> Bakersfield -> Fresno
    route = ["Los Angeles", "Bakersfield", "Fresno"]
    
    distance = get_route_distance(route)
    
    # LA to Bakersfield: 110 miles
    # Bakersfield to Fresno: 110 miles
    # Total: 220 miles
    assert distance == 220.0


def test_empty_route():
    """
    Test handling of empty route.
    """
    route = []
    distance = get_route_distance(route)
    assert distance == 0.0


def test_single_city_route():
    """
    Test handling of single city (no segments).
    """
    route = ["Los Angeles"]
    distance = get_route_distance(route)
    assert distance == 0.0


def test_graph_is_bidirectional():
    """
    Test that graph edges are bidirectional.
    """
    battery_range = 200
    graph = build_graph(battery_range)
    
    # If there's an edge from A to B, there should be one from B to A
    if graph.has_edge("Los Angeles", "Bakersfield"):
        assert graph.has_edge("Bakersfield", "Los Angeles")


def test_route_optimality():
    """
    Test that the shortest path algorithm finds the optimal route.
    
    With sufficient range, LA to SF should go through all intermediate cities
    in order (since they're on a straight line).
    """
    battery_range = 150
    graph = build_graph(battery_range)
    
    route = find_route(graph, "Los Angeles", "San Francisco")
    
    # Expected optimal route with 150-mile range
    expected_route = ["Los Angeles", "Bakersfield", "Fresno", "Modesto", "San Francisco"]
    
    assert route == expected_route
