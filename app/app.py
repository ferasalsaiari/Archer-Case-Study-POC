"""
EV Truck Route Planner - Streamlit Application
Interactive UI for planning electric semi-truck routes with charging stops.
"""

import streamlit as st
import time
from streamlit_folium import st_folium
from data import get_all_cities
from route_planner import build_graph, find_route, get_route_distance
from charging import compute_battery_usage, format_battery_level
from map_visualization import create_route_map
from trip_estimator import estimate_trip_time


def main():
    """Main application entry point."""
    
    # Page configuration
    st.set_page_config(
        page_title="EV Truck Route Planner",
        page_icon="🚛",
        layout="wide"
    )
    
    # Initialize session state for storing results
    if 'route_results' not in st.session_state:
        st.session_state.route_results = None
    
    # Title and description
    st.title("🚛 EV Truck Route Planner")
    st.markdown("""
    Plan optimal routes for electric semi-trucks with automatic charging stop identification.
    This tool ensures your trucks never run out of battery by intelligently routing through charging stations.
    """)
    
    st.divider()
    
    # Input section
    col1, col2, col3 = st.columns(3)
    
    cities = get_all_cities()
    
    with col1:
        start_city = st.selectbox(
            "🏁 Start City",
            cities,
            index=0
        )
    
    with col2:
        end_city = st.selectbox(
            "🎯 Destination City",
            cities,
            index=len(cities) - 1
        )
    
    with col3:
        battery_range = st.slider(
            "🔋 Truck Battery Range (miles)",
            min_value=100,
            max_value=400,
            value=250,
            step=10
        )
    
    st.divider()
    
    # Plan route button
    if st.button("🗺️ Plan Route", type="primary", use_container_width=True):
        
        try:
            # Validate inputs
            if start_city == end_city:
                st.error("⚠️ Start and destination cities must be different.")
                st.session_state.route_results = None
                return
            
            # Build range-constrained graph
            with st.spinner("🔧 Building route graph with battery constraints..."):
                graph = build_graph(battery_range)
            
            # Find shortest path
            with st.spinner("🧠 Running advanced pathfinding algorithms..."):
                route = find_route(graph, start_city, end_city)
            
            if route is None:
                st.error(f"❌ No route found from {start_city} to {end_city} with battery range of {battery_range} miles.")
                st.info("💡 Try increasing the battery range or selecting different cities.")
                st.session_state.route_results = None
                return
            
            # Simulate battery usage
            with st.spinner("⚡ Simulating battery consumption and charging requirements..."):
                battery_info = compute_battery_usage(route, battery_range)
            
            # Check if route is feasible
            if not battery_info['feasible']:
                st.error(f"❌ Route not feasible: {battery_info['error_message']}")
                st.info("💡 Try increasing the battery range.")
                st.session_state.route_results = None
                return
            
            # Calculate trip time
            trip_time = estimate_trip_time(route, battery_info['charging_stops'])
            
            # Store results in session state
            st.session_state.route_results = {
                'route': route,
                'battery_info': battery_info,
                'trip_time': trip_time
            }
                
        except Exception as e:
            st.error(f"❌ An error occurred during route planning: {str(e)}")
            st.info("Please check the console for more details and try again.")
            st.session_state.route_results = None
    
    # Display results if they exist in session state
    if st.session_state.route_results:
        results = st.session_state.route_results
        route = results['route']
        battery_info = results['battery_info']
        trip_time = results['trip_time']
        
        # Display results
        st.success("✅ Route successfully planned!")
        
        # Trip Summary
        st.subheader("📊 Trip Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Distance", f"{trip_time['total_distance']} miles")
        
        with col2:
            st.metric("Driving Time", trip_time['driving_time_formatted'])
        
        with col3:
            st.metric("Charging Time", trip_time['charging_time_formatted'])
        
        with col4:
            st.metric("Total Trip Time", trip_time['total_time_formatted'])
        
        # Interactive Map
        st.subheader("🗺️ Interactive Route Map")
        
        try:
            route_map = create_route_map(route, battery_info['charging_stops'])
            
            if route_map:
                st_folium(route_map, width=800, height=400, key="route_map")
            else:
                st.warning("⚠️ Could not generate map visualization")
        except Exception as map_error:
            st.error(f"⚠️ Map generation failed: {str(map_error)}")
            st.info("Route data is available below.")
        
        st.divider()
        
        # Route path
        st.subheader("🛣️ Route Path")
        route_str = " → ".join(route)
        st.markdown(f"**{route_str}**")
        
        # Charging stops
        if battery_info['charging_stops']:
            st.subheader("⚡ Charging Stops")
            for stop in battery_info['charging_stops']:
                st.markdown(f"- 🔌 **{stop}**")
        else:
            st.info("ℹ️ No charging stops needed for this route.")
        
        # Detailed segment breakdown
        st.subheader("📊 Segment-by-Segment Battery Analysis")
        
        for i, segment in enumerate(battery_info['segments'], 1):
            with st.expander(f"Segment {i}: {segment['from']} → {segment['to']}", expanded=True):
                
                # Check if charging occurred at the start of this segment
                charged_here = segment['from'] in battery_info['charging_stops']
                
                if charged_here:
                    st.success(f"🔌 Charged to 100% at {segment['from']}")
                
                st.markdown(f"**Distance:** {segment['distance']:.1f} miles")
                
                # Battery visualization with progress bars
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Battery Before:**")
                    st.progress(segment['battery_before'] / 100.0)
                    st.caption(f"{segment['battery_before']:.1f}%")
                
                with col2:
                    st.markdown("**Battery After:**")
                    battery_after = segment['battery_after']
                    st.progress(battery_after / 100.0)
                    st.caption(f"{battery_after:.1f}%")
                
                # Battery status indicator
                if battery_after >= 50:
                    st.success(f"✅ Battery healthy: {battery_after:.1f}%")
                elif battery_after >= 20:
                    st.warning(f"⚠️ Battery moderate: {battery_after:.1f}%")
                else:
                    st.error(f"🔴 Battery low: {battery_after:.1f}%")
        
        st.divider()
        
        # Additional information
        with st.expander("ℹ️ About This Tool"):
            st.markdown("""
            This EV Truck Route Planner uses graph-based algorithms to find optimal routes
            for electric semi-trucks while respecting battery range constraints.
            
            **How it works:**
            1. Builds a graph where cities are connected only if within battery range
            2. Finds the shortest path using Dijkstra's algorithm
            3. Simulates battery consumption along the route
            4. Automatically identifies necessary charging stops
            
            **Charging Stations Available:**
            - Bakersfield
            - Fresno
            - Modesto
            """)


if __name__ == "__main__":
    main()
