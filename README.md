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
- Visual battery level indicators
- Clear warnings for low battery situations

### 🎯 Interactive UI
- Easy-to-use Streamlit interface
- Adjustable battery range slider (100-400 miles)
- Real-time route computation
- Detailed route visualization

## Tech Stack

- **Python 3.10+**: Core language
- **Streamlit**: Web UI framework
- **NetworkX**: Graph algorithms and shortest path computation
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
├── app/
│   ├── app.py               # Streamlit UI application
│   ├── route_planner.py     # Graph construction and pathfinding
│   ├── charging.py          # Battery simulation logic
│   └── data.py              # Mock city and charging station data
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

## Development

### Running Tests
Currently, this is a prototype without formal test coverage. For production use, add:
- Unit tests for route planning logic
- Integration tests for battery simulation
- UI tests with Streamlit testing framework

### Code Style
The codebase follows:
- PEP 8 style guidelines
- Modular architecture with clear separation of concerns
- Comprehensive docstrings for all functions
- Type hints where appropriate

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

