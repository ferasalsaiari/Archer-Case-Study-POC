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
        
        # Draw route polyline with modern styling
        route_coords = [geo_coordinates[city] for city in route]
        folium.PolyLine(
            locations=route_coords,
            color='#2563eb',
            weight=4,
            opacity=0.8
        ).add_to(route_map)
        
        # Add emoji-based markers for each city
        for i, city in enumerate(route):
            lat, lon = geo_coordinates[city]
            
            # Determine emoji and styling based on city type
            if i == 0:
                # Start city
                emoji = "&#128205;"  # 📍 Round Pushpin
                bg_color = "#10b981"
                popup_text = f"<b>START</b><br>{city}"
            elif i == len(route) - 1:
                # Destination city
                emoji = "&#127937;"  # 🏁 Checkered Flag
                bg_color = "#ef4444"
                popup_text = f"<b>DESTINATION</b><br>{city}"
            elif city in charging_stops:
                # Charging station
                emoji = "&#9889;"  # ⚡ Lightning Bolt
                bg_color = "#f59e0b"
                popup_text = f"<b>CHARGING</b><br>{city}"
            else:
                # Regular waypoint
                emoji = "&#128205;"  # 📍 Round Pushpin
                bg_color = "#6b7280"
                popup_text = city
            
            # Create custom HTML for emoji marker
            icon_html = f"""
                <div style="
                    font-size: 24px;
                    text-align: center;
                    line-height: 1;
                    background-color: {bg_color};
                    border-radius: 50%;
                    width: 36px;
                    height: 36px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                ">
                    {emoji}
                </div>
            """
            
            # Add marker with custom emoji icon
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_text, max_width=200),
                tooltip=city,
                icon=folium.DivIcon(html=icon_html)
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
