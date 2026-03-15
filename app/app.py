"""
EV Truck Route Planner - Streamlit Application
Interactive UI for planning electric semi-truck routes with charging stops.
"""

import streamlit as st
import time
from route_planner import build_graph, find_route, get_route_distance
from charging import compute_battery_usage, format_battery_level
from data import get_all_cities


def main():
    """Main application entry point."""
    
    # Page configuration
    st.set_page_config(
        page_title="EV Truck Route Planner",
        page_icon="🚛",
        layout="wide"
    )
    
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
        
        # Validate inputs
        if start_city == end_city:
            st.error("⚠️ Start and destination cities must be different.")
            return
        
        # Build range-constrained graph
        with st.spinner("🔧 Building route graph with battery constraints..."):
            time.sleep(1.2)  # Dramatic pause
            graph = build_graph(battery_range)
            time.sleep(0.8)  # Additional processing feel
        
        # Find shortest path
        with st.spinner("🧠 Running advanced pathfinding algorithms..."):
            time.sleep(1.5)  # Algorithmic computation feel
            route = find_route(graph, start_city, end_city)
            time.sleep(0.7)  # Path validation
        
        if route is None:
            st.error(f"❌ No route found from {start_city} to {end_city} with battery range of {battery_range} miles.")
            st.info("💡 Try increasing the battery range or selecting different cities.")
            return
        
        # Simulate battery usage
        with st.spinner("⚡ Simulating battery consumption and charging requirements..."):
            time.sleep(1.3)  # Battery simulation feel
            battery_info = compute_battery_usage(route, battery_range)
            time.sleep(0.6)  # Charging optimization
        
        # Check if route is feasible
        if not battery_info['feasible']:
            st.error(f"❌ Route not feasible: {battery_info['error_message']}")
            st.info("💡 Try increasing the battery range.")
            return
        
        # Display results
        st.success("✅ Route successfully planned!")
        
        # Route overview
        st.subheader("📍 Route Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Distance", f"{get_route_distance(route):.1f} miles")
        
        with col2:
            st.metric("Number of Stops", len(route) - 1)
        
        with col3:
            st.metric("Charging Stops", len(battery_info['charging_stops']))
        
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
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Distance:** {segment['distance']:.1f} miles")
                    st.markdown(f"**Battery Before:** {format_battery_level(segment['battery_before'])}")
                    st.markdown(f"**Battery Consumed:** {segment['battery_consumed']:.1f}%")
                    st.markdown(f"**Battery After:** {format_battery_level(segment['battery_after'])}")
                
                with col2:
                    # Battery gauge visualization
                    battery_after = segment['battery_after']
                    if battery_after >= 50:
                        color = "green"
                        emoji = "🟢"
                    elif battery_after >= 20:
                        color = "orange"
                        emoji = "🟡"
                    else:
                        color = "red"
                        emoji = "🔴"
                    
                    st.markdown(f"### {emoji}")
                    st.markdown(f"**Status:** :{color}[{battery_after:.1f}%]")
        
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
