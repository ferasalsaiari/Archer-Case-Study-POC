"""
Route planning logic using NetworkX graph algorithms.
Builds range-constrained graphs and computes shortest paths.
"""

import networkx as nx
from data import locations, get_distance


def build_graph(battery_range):
    """
    Build a directed graph where edges exist only if distance <= battery_range.
    
    This creates a range-constrained graph where trucks can only travel between
    cities if the distance is within their battery capacity.
    
    Args:
        battery_range (int): Maximum range of truck in miles
    
    Returns:
        nx.DiGraph: Directed graph with cities as nodes and feasible routes as edges
    """
    G = nx.DiGraph()
    
    # Add all cities as nodes
    cities = list(locations.keys())
    G.add_nodes_from(cities)
    
    # Add edges only if distance is within battery range
    for i, city1 in enumerate(cities):
        for city2 in cities[i+1:]:  # Avoid duplicate pairs
            distance = get_distance(city1, city2)
            
            # Only add edge if within battery range
            if distance <= battery_range:
                # Add bidirectional edges with distance as weight
                G.add_edge(city1, city2, weight=distance)
                G.add_edge(city2, city1, weight=distance)
    
    return G


def find_route(graph, start, end):
    """
    Find shortest path between start and end cities using Dijkstra's algorithm.
    
    Args:
        graph (nx.DiGraph): Range-constrained graph
        start (str): Starting city
        end (str): Destination city
    
    Returns:
        list: Ordered list of cities in the route, or None if no path exists
    
    Raises:
        nx.NetworkXNoPath: If no path exists between start and end
    """
    try:
        # Use Dijkstra's algorithm to find shortest path
        path = nx.shortest_path(graph, start, end, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None


def get_route_distance(route):
    """
    Calculate total distance of a route.
    
    Args:
        route (list): Ordered list of cities
    
    Returns:
        float: Total distance in miles
    """
    if not route or len(route) < 2:
        return 0.0
    
    total_distance = 0.0
    for i in range(len(route) - 1):
        total_distance += get_distance(route[i], route[i + 1])
    
    return total_distance
