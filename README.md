# EV Truck Route + Charging Planner

A proof-of-concept route planning application for electric semi-truck fleet operators. This tool helps dispatchers plan optimal routes while ensuring trucks never exceed their battery range by automatically identifying necessary charging stops.

## Project Overview

Electric semi-trucks face a unique operational challenge: limited battery range compared to diesel trucks. Fleet operators must carefully plan routes to ensure trucks can reach their destinations without running out of charge. This becomes especially complex when:

- Battery range varies by truck model and load
- Charging infrastructure is limited to specific locations
- Route efficiency directly impacts operational costs

This application solves these challenges by:
1. Computing feasible routes based on truck battery capacity
2. Automatically identifying when and where charging is needed
3. Providing detailed battery consumption analysis per route segment
4. Offering an interactive UI for route experimentation

## Features

### 🗺️ Range-Aware Route Planning
- Builds route graphs constrained by battery range
- Only considers routes that are physically achievable
- Uses Dijkstra's algorithm for optimal path finding

### ⚡ Charging Stop Identification
- Automatically detects when battery will be depleted
- Inserts charging stops at available stations
- Validates route feasibility with current infrastructure

### 📊 Battery Consumption Analysis
- Segment-by-segment battery tracking
- Visual progress bars for battery levels
- Color-coded battery status indicators
- Clear warnings for low battery situations

### 🗺️ Interactive Map Visualization
- Folium-powered interactive maps
- Visual route display with polylines
- Color-coded markers (green=start, red=destination, orange=charging)
- Clickable city markers with details
- Pan and zoom controls

### ⏱️ Trip Time Estimation
- Calculates total driving time (60 mph average)
- Estimates charging time (30 min per stop)
- Displays total trip duration
- Formatted time breakdowns

### 🎯 Interactive UI
- Easy-to-use Streamlit interface
- Adjustable battery range slider (100-400 miles)
- Real-time route computation
- Comprehensive trip summary metrics

## Tech Stack

- **Python 3.10+**: Core language
- **Streamlit**: Web UI framework
- **NetworkX**: Graph algorithms and shortest path computation
- **Folium**: Interactive map visualization
- **Pytest**: Unit testing framework
- **Mock Data**: Hardcoded city locations and charging stations (no external APIs)

## How to Run

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Archer\ Case\ Study\ POC
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app/app.py
```

The application will open in your default web browser at `http://localhost:8501`

### 5. Run Tests (Optional)
```bash
pytest tests/ -v
```

## Example Usage

### Scenario 1: Long-Distance Route
**Input:**
- Start: Los Angeles
- Destination: San Francisco
- Battery Range: 250 miles

**Output:**
```
Route: Los Angeles → Bakersfield → Fresno → Modesto → San Francisco

Charging Stops:
- Bakersfield
- Fresno

Total Distance: 380.0 miles
```

### Scenario 2: Short Battery Range
**Input:**
- Start: Los Angeles
- Destination: San Francisco
- Battery Range: 150 miles

**Output:**
```
Route: Los Angeles → Bakersfield → Fresno → Modesto → San Francisco

Charging Stops:
- Bakersfield
- Fresno
- Modesto

Total Distance: 380.0 miles
```

### Scenario 3: Insufficient Range
**Input:**
- Start: Los Angeles
- Destination: Bakersfield
- Battery Range: 100 miles

**Output:**
```
❌ No route found from Los Angeles to Bakersfield with battery range of 100 miles.
💡 Try increasing the battery range or selecting different cities.
```

## Project Structure

```
ev-truck-route-planner/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── app/
│   ├── app.py               # Streamlit UI application
│   ├── route_planner.py     # Graph construction and pathfinding
│   ├── charging.py          # Battery simulation logic
│   ├── data.py              # Mock city and charging station data
│   ├── map_visualization.py # Folium map generation
│   └── trip_estimator.py    # Trip time calculations
├── tests/
│   ├── test_routes.py       # Route planning tests
│   └── test_charging.py     # Battery simulation tests
└── docs/
    └── architecture.md      # Technical architecture documentation
```

## Available Cities

The prototype includes five cities along a California corridor:

- **Los Angeles** (0, 0)
- **Bakersfield** (110, 0) - ⚡ Charging Available
- **Fresno** (220, 0) - ⚡ Charging Available
- **Modesto** (300, 0) - ⚡ Charging Available
- **San Francisco** (380, 0)

## Testing

The project includes comprehensive unit tests for core functionality.

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Files
```bash
# Test route planning
pytest tests/test_routes.py -v

# Test battery simulation
pytest tests/test_charging.py -v
```

### Example Test Output
```
tests/test_routes.py::test_graph_respects_battery_range PASSED
tests/test_routes.py::test_route_exists_la_to_sf PASSED
tests/test_charging.py::test_charging_stops_detected PASSED
tests/test_charging.py::test_battery_consumption_calculation PASSED

==================== 15 passed in 0.23s ====================
```

### Test Coverage
- **Route Planning**: Graph construction, pathfinding, distance calculations
- **Battery Simulation**: Charging detection, consumption tracking, feasibility validation
- **Edge Cases**: Empty routes, insufficient range, single segments

## Development

### Code Style
The codebase follows:
- PEP 8 style guidelines
- Modular architecture with clear separation of concerns
- Comprehensive docstrings for all functions
- Type hints where appropriate

### Adding New Features
1. Implement feature in appropriate module
2. Add unit tests in `tests/`
3. Update documentation
4. Run test suite to ensure no regressions

## Future Enhancements

This prototype demonstrates core concepts. Production-ready enhancements could include:

### Data & Integration
- Real road network data (OpenStreetMap, Google Maps API)
- Live charging station availability (ChargePoint, Electrify America APIs)
- Real-time traffic and weather data integration

### Advanced Routing
- Terrain-aware energy modeling (hills, elevation changes)
- Payload weight impact on battery consumption
- Multi-stop route optimization
- Alternative route suggestions

### Charging Optimization
- Charging time estimation and scheduling
- Electricity price-aware charging (charge during off-peak hours)
- Battery degradation modeling
- Partial charging strategies

### Fleet Management
- Multi-truck dispatch optimization
- Fleet-wide battery health monitoring
- Driver assignment and scheduling
- Cost analysis and reporting

### UI/UX Improvements
- Map visualization with route overlay
- Historical route analytics
- Mobile-responsive design
- Export routes to GPS devices

