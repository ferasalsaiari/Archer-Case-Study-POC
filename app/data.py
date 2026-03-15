"""
Mock data for EV truck route planner.
Provides city locations and charging station information.
"""

# City locations with (x, y) coordinates in miles
# Using simplified 1D coordinates along a highway corridor for this prototype
locations = {
    "Los Angeles": (0, 0),
    "Bakersfield": (110, 0),
    "Fresno": (220, 0),
    "Modesto": (300, 0),
    "San Francisco": (380, 0)
}

# Cities with charging stations available
charging_stations = [
    "Bakersfield",
    "Fresno",
    "Modesto"
]


def get_distance(city1, city2):
    """
    Calculate Euclidean distance between two cities.
    
    Args:
        city1 (str): Name of first city
        city2 (str): Name of second city
    
    Returns:
        float: Distance in miles
    """
    x1, y1 = locations[city1]
    x2, y2 = locations[city2]
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def has_charging_station(city):
    """
    Check if a city has a charging station.
    
    Args:
        city (str): Name of city
    
    Returns:
        bool: True if city has charging station
    """
    return city in charging_stations


def get_all_cities():
    """
    Get list of all cities.
    
    Returns:
        list: List of city names
    """
    return list(locations.keys())
