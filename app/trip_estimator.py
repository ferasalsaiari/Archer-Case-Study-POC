"""
Trip time estimation for EV truck routes.
Calculates driving time, charging time, and total trip duration.
"""

from data import get_distance


# Constants for trip estimation
AVERAGE_SPEED_MPH = 60  # Average highway speed for trucks
CHARGING_TIME_MINUTES = 30  # Time per charging stop


def estimate_trip_time(route, charging_stops):
    """
    Estimate total trip time including driving and charging.
    
    Assumptions:
    - Average speed: 60 mph
    - Charging time: 30 minutes per stop
    - No traffic delays or rest stops
    
    Args:
        route (list): Ordered list of cities in the route
        charging_stops (list): List of cities where charging occurs
    
    Returns:
        dict: Trip time breakdown with:
            - total_distance (float): Total miles
            - driving_time_hours (float): Hours spent driving
            - charging_time_hours (float): Hours spent charging
            - total_time_hours (float): Total trip time
            - driving_time_formatted (str): Formatted driving time
            - charging_time_formatted (str): Formatted charging time
            - total_time_formatted (str): Formatted total time
    """
    if not route or len(route) < 2:
        return {
            'total_distance': 0.0,
            'driving_time_hours': 0.0,
            'charging_time_hours': 0.0,
            'total_time_hours': 0.0,
            'driving_time_formatted': '0h 0m',
            'charging_time_formatted': '0h 0m',
            'total_time_formatted': '0h 0m'
        }
    
    # Calculate total distance
    total_distance = 0.0
    for i in range(len(route) - 1):
        distance = get_distance(route[i], route[i + 1])
        total_distance += distance
    
    # Calculate driving time (distance / speed)
    driving_time_hours = total_distance / AVERAGE_SPEED_MPH
    
    # Calculate charging time
    num_charging_stops = len(charging_stops)
    charging_time_hours = (num_charging_stops * CHARGING_TIME_MINUTES) / 60.0
    
    # Calculate total time
    total_time_hours = driving_time_hours + charging_time_hours
    
    # Format times as "Xh Ym"
    driving_time_formatted = format_time(driving_time_hours)
    charging_time_formatted = format_time(charging_time_hours)
    total_time_formatted = format_time(total_time_hours)
    
    return {
        'total_distance': round(total_distance, 1),
        'driving_time_hours': round(driving_time_hours, 2),
        'charging_time_hours': round(charging_time_hours, 2),
        'total_time_hours': round(total_time_hours, 2),
        'driving_time_formatted': driving_time_formatted,
        'charging_time_formatted': charging_time_formatted,
        'total_time_formatted': total_time_formatted
    }


def format_time(hours):
    """
    Format hours as "Xh Ym" string.
    
    Args:
        hours (float): Time in hours
    
    Returns:
        str: Formatted time string
    """
    total_minutes = int(hours * 60)
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h}h {m}m"


def get_segment_time(city1, city2):
    """
    Calculate driving time for a single segment.
    
    Args:
        city1 (str): Starting city
        city2 (str): Ending city
    
    Returns:
        float: Time in hours
    """
    distance = get_distance(city1, city2)
    return distance / AVERAGE_SPEED_MPH


def estimate_arrival_times(route, charging_stops, start_time_hours=0):
    """
    Estimate arrival time at each city in the route.
    
    Args:
        route (list): Ordered list of cities
        charging_stops (list): Cities where charging occurs
        start_time_hours (float): Starting time in hours (default 0)
    
    Returns:
        list: List of dicts with city name and arrival time
    """
    if not route:
        return []
    
    arrivals = []
    current_time = start_time_hours
    
    # First city (starting point)
    arrivals.append({
        'city': route[0],
        'arrival_time_hours': current_time,
        'arrival_time_formatted': format_time(current_time)
    })
    
    # Subsequent cities
    for i in range(1, len(route)):
        # Add driving time
        segment_time = get_segment_time(route[i-1], route[i])
        current_time += segment_time
        
        # Add charging time if previous city had charging
        if route[i-1] in charging_stops:
            current_time += CHARGING_TIME_MINUTES / 60.0
        
        arrivals.append({
            'city': route[i],
            'arrival_time_hours': round(current_time, 2),
            'arrival_time_formatted': format_time(current_time)
        })
    
    return arrivals
