"""
Battery simulation and charging stop logic.
Tracks battery consumption and determines when charging is needed.
"""

from data import get_distance, has_charging_station


def compute_battery_usage(route, battery_range):
    """
    Simulate battery consumption along a route and identify charging stops.
    
    The truck starts with 100% battery. For each segment, we calculate battery
    consumption. If battery would drop below 0%, the truck must charge at the
    previous city (if it has a charging station).
    
    Args:
        route (list): Ordered list of cities in the route
        battery_range (int): Maximum range of truck in miles
    
    Returns:
        dict: Contains:
            - segments (list): List of segment info with battery levels
            - charging_stops (list): Cities where charging occurred
            - feasible (bool): Whether route is feasible with given range
            - error_message (str): Error message if route is not feasible
    """
    if not route or len(route) < 2:
        return {
            'segments': [],
            'charging_stops': [],
            'feasible': True,
            'error_message': None
        }
    
    segments = []
    charging_stops = []
    current_battery = 100.0  # Start with full battery
    
    for i in range(len(route) - 1):
        city_from = route[i]
        city_to = route[i + 1]
        distance = get_distance(city_from, city_to)
        
        # Calculate battery consumption for this segment
        battery_consumed = (distance / battery_range) * 100
        battery_after = current_battery - battery_consumed
        
        # Check if we need to charge before this segment
        if battery_after < 0:
            # Need to charge at current city
            if has_charging_station(city_from):
                # Charge to 100%
                charging_stops.append(city_from)
                current_battery = 100.0
                battery_after = current_battery - battery_consumed
                
                # Double check if segment is still too long even with full charge
                if battery_after < 0:
                    return {
                        'segments': segments,
                        'charging_stops': charging_stops,
                        'feasible': False,
                        'error_message': f"Segment {city_from} → {city_to} ({distance:.1f} mi) exceeds battery range ({battery_range} mi)"
                    }
            else:
                # No charging station available, route not feasible
                return {
                    'segments': segments,
                    'charging_stops': charging_stops,
                    'feasible': False,
                    'error_message': f"Battery depleted before {city_to}, but {city_from} has no charging station"
                }
        
        # Record segment information
        segments.append({
            'from': city_from,
            'to': city_to,
            'distance': distance,
            'battery_before': current_battery,
            'battery_consumed': battery_consumed,
            'battery_after': battery_after
        })
        
        # Update current battery for next segment
        current_battery = battery_after
    
    return {
        'segments': segments,
        'charging_stops': charging_stops,
        'feasible': True,
        'error_message': None
    }


def format_battery_level(battery_percentage):
    """
    Format battery level as a visual bar.
    
    Args:
        battery_percentage (float): Battery level (0-100)
    
    Returns:
        str: Visual representation of battery level
    """
    # Create a simple text-based battery bar
    filled = int(battery_percentage / 5)  # 20 segments for 100%
    empty = 20 - filled
    bar = '█' * filled + '░' * empty
    return f"{bar} {battery_percentage:.1f}%"
