"""
Map visualization using Folium for interactive route display.
Renders cities, charging stations, and computed routes on an interactive map.
"""

import folium
from data import geo_coordinates, charging_stations


def create_route_map(route, charging_stops):
    """
    Create a modern, sleek Folium map showing the route with cities and charging stations.
    
    Args:
        route (list): Ordered list of city names in the route
        charging_stops (list): List of cities where charging occurs
    
    Returns:
        folium.Map: Interactive map object
    """
    if not route or len(route) == 0:
        return None
    
    try:
        # Calculate map center (midpoint of all cities in route)
        lats = [geo_coordinates[city][0] for city in route]
        lons = [geo_coordinates[city][1] for city in route]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        
        # Create base map with modern CartoDB Positron tiles (clean, minimal style)
        route_map = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='CartoDB positron'
        )
        
        # Draw route polyline with modern styling (darker, thicker)
        route_coords = [geo_coordinates[city] for city in route]
        folium.PolyLine(
            locations=route_coords,
            color='#2563eb',  # Modern blue
            weight=4,
            opacity=0.8
        ).add_to(route_map)
        
        # Add modern circle markers for each city
        for i, city in enumerate(route):
            lat, lon = geo_coordinates[city]
            
            # Modern color scheme and styling
            if i == 0:
                # Start city - green with larger radius
                color = '#10b981'  # Modern green
                fill_color = '#10b981'
                radius = 12
                popup_text = f"<b>🚀 START</b><br>{city}"
            elif i == len(route) - 1:
                # Destination city - red with larger radius
                color = '#ef4444'  # Modern red
                fill_color = '#ef4444'
                radius = 12
                popup_text = f"<b>🎯 DESTINATION</b><br>{city}"
            elif city in charging_stops:
                # Charging station - electric blue
                color = '#f59e0b'  # Modern amber/orange
                fill_color = '#f59e0b'
                radius = 10
                popup_text = f"<b>⚡ CHARGING</b><br>{city}"
            else:
                # Regular waypoint - subtle gray
                color = '#6b7280'  # Modern gray
                fill_color = '#9ca3af'
                radius = 8
                popup_text = f"<b>📍</b> {city}"
            
            # Add modern circle marker
            folium.CircleMarker(
                location=[lat, lon],
                radius=radius,
                popup=folium.Popup(popup_text, max_width=200),
                tooltip=city,
                color=color,
                fill=True,
                fillColor=fill_color,
                fillOpacity=0.9,
                weight=2
            ).add_to(route_map)
        
        return route_map
        
    except Exception as e:
        print(f"Map creation error: {e}")
        return None


def create_all_cities_map():
    """
    Create a map showing all available cities and charging stations.
    Useful for overview display before route planning.
    
    Returns:
        folium.Map: Interactive map object
    """
    # Calculate center of all cities
    all_lats = [coord[0] for coord in geo_coordinates.values()]
    all_lons = [coord[1] for coord in geo_coordinates.values()]
    center_lat = sum(all_lats) / len(all_lats)
    center_lon = sum(all_lons) / len(all_lons)
    
    # Create base map
    overview_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Add markers for all cities
    for city, (lat, lon) in geo_coordinates.items():
        if city in charging_stations:
            # Charging station available
            folium.Marker(
                location=[lat, lon],
                popup=f"<b>{city}</b><br>⚡ Charging Available",
                tooltip=city,
                icon=folium.Icon(color='orange', icon='bolt', prefix='glyphicon')
            ).add_to(overview_map)
        else:
            # Regular city
            folium.Marker(
                location=[lat, lon],
                popup=f"<b>{city}</b>",
                tooltip=city,
                icon=folium.Icon(color='blue', icon='info-sign', prefix='glyphicon')
            ).add_to(overview_map)
    
    return overview_map
