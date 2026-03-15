# EV Truck Route Planner - Technical Architecture

## Problem Overview

Electric semi-trucks represent the future of freight transportation, but they introduce significant operational complexity compared to traditional diesel trucks. The core challenge is **range anxiety at scale**: fleet operators must ensure trucks can complete their routes without running out of battery charge.

### Key Challenges

1. **Limited Range**: Electric trucks typically have 150-400 mile ranges vs. 1000+ miles for diesel
2. **Sparse Infrastructure**: Charging stations for heavy-duty trucks are limited and unevenly distributed
3. **Route Constraints**: Not all routes are feasible with current battery technology
4. **Operational Planning**: Dispatchers need tools to plan routes that account for charging requirements
5. **Cost Optimization**: Charging stops add time and cost; routes must balance feasibility with efficiency

This application provides a computational solution to these challenges by modeling the route planning problem as a **constrained graph traversal** with battery capacity as the primary constraint.

## System Design

The application follows a clean **three-tier architecture**:

```
┌─────────────────────────────────────┐
│     Presentation Layer              │
│     (Streamlit UI)                  │
│  - User inputs                      │
│  - Route visualization              │
│  - Battery analysis display         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Business Logic Layer            │
│  ┌─────────────────────────────┐   │
│  │  Route Planner              │   │
│  │  - Graph construction       │   │
│  │  - Shortest path algorithm  │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │  Charging Simulator         │   │
│  │  - Battery tracking         │   │
│  │  - Charging stop detection  │   │
│  └─────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Data Layer                      │
│  - City locations                   │
│  - Charging station registry        │
│  - Distance calculations            │
└─────────────────────────────────────┘
```

### Component Responsibilities

#### 1. Streamlit UI (`app.py`)
- **Purpose**: User interaction and result visualization
- **Responsibilities**:
  - Collect user inputs (start, destination, battery range)
  - Orchestrate route planning workflow
  - Display route results with battery analysis
  - Handle error states and edge cases
- **Key Features**:
  - Interactive sliders and dropdowns
  - Real-time route computation
  - Segment-by-segment battery visualization
  - Color-coded battery status indicators

#### 2. Route Planner (`route_planner.py`)
- **Purpose**: Graph-based route computation
- **Responsibilities**:
  - Build range-constrained graphs
  - Compute shortest paths
  - Calculate total route distances
- **Algorithm**: Dijkstra's shortest path with battery range constraints

#### 3. Charging Simulator (`charging.py`)
- **Purpose**: Battery consumption modeling
- **Responsibilities**:
  - Simulate battery drain per segment
  - Identify when charging is required
  - Validate route feasibility
  - Track charging stop locations
- **Logic**: Sequential simulation with greedy charging strategy

#### 4. Data Layer (`data.py`)
- **Purpose**: Mock data and utility functions
- **Responsibilities**:
  - Provide city location data
  - Maintain charging station registry
  - Calculate inter-city distances
- **Data Model**: Simplified 2D coordinate system

## Tech Stack

### Python 3.10+
**Why Python?**
- Excellent libraries for graph algorithms (NetworkX)
- Rapid prototyping capabilities
- Strong data processing ecosystem
- Easy integration with web frameworks

### Streamlit
**Why Streamlit?**
- Zero-boilerplate web UI creation
- Perfect for data-driven applications
- Built-in widgets for common inputs
- Automatic reactivity and state management
- Ideal for prototypes and internal tools

**Alternatives Considered**:
- Flask/Django: Too heavy for a prototype
- Jupyter Notebook: Not suitable for end-user tools
- React/Vue: Requires separate backend and more development time

### NetworkX
**Why NetworkX?**
- Industry-standard graph library
- Optimized shortest path algorithms
- Clean, Pythonic API
- Well-documented and maintained

**Alternatives Considered**:
- Custom implementation: Unnecessary complexity
- igraph: Less Pythonic API
- graph-tool: Heavier dependency

## Graph Model

### Node Representation
Each city is represented as a **node** in the graph:

```python
Node = {
    "name": str,           # City name
    "location": (x, y),    # 2D coordinates
    "has_charging": bool   # Charging station availability
}
```

### Edge Representation
Edges represent **feasible routes** between cities:

```python
Edge = {
    "source": str,      # Starting city
    "target": str,      # Destination city
    "weight": float     # Distance in miles
}
```

**Critical Constraint**: An edge only exists if `distance <= battery_range`

This constraint ensures the graph only contains routes the truck can physically traverse on a single charge.

### Graph Construction

The graph is **dynamically constructed** based on battery range:

```
For battery_range = 150 miles:

LA ──110mi── Bakersfield ──110mi── Fresno
(No edge from LA to Fresno because 220mi > 150mi)

For battery_range = 250 miles:

LA ──110mi── Bakersfield ──110mi── Fresno
 └────────220mi────────────┘
(Edge exists because 220mi ≤ 250mi)
```

This approach naturally encodes the range constraint into the graph structure.

## Algorithm

### High-Level Workflow

```
1. Input: start_city, end_city, battery_range
2. Build range-constrained graph G(V, E)
3. Find shortest path P using Dijkstra's algorithm
4. Simulate battery consumption along P
5. Insert charging stops where needed
6. Validate feasibility
7. Return route with charging plan
```

### Detailed Steps

#### Step 1: Graph Construction
```python
def build_graph(battery_range):
    G = DirectedGraph()
    
    for each pair of cities (A, B):
        distance = calculate_distance(A, B)
        
        if distance <= battery_range:
            G.add_edge(A, B, weight=distance)
            G.add_edge(B, A, weight=distance)
    
    return G
```

**Time Complexity**: O(n²) where n = number of cities
- Must check all city pairs
- For this prototype: 5 cities → 10 pairs (negligible)

#### Step 2: Shortest Path Computation
```python
def find_route(graph, start, end):
    return dijkstra_shortest_path(graph, start, end)
```

**Time Complexity**: O(E log V) using binary heap
- E = number of edges
- V = number of vertices
- For dense graphs: O(V² log V)
- For this prototype: ~20 edges, 5 vertices (negligible)

#### Step 3: Battery Simulation
```python
def compute_battery_usage(route, battery_range):
    battery = 100.0  # Start full
    charging_stops = []
    
    for each segment (A → B) in route:
        distance = get_distance(A, B)
        consumption = (distance / battery_range) * 100
        
        if battery - consumption < 0:
            # Need to charge at A
            if has_charging_station(A):
                charging_stops.append(A)
                battery = 100.0
            else:
                return INFEASIBLE
        
        battery -= consumption
    
    return charging_stops
```

**Time Complexity**: O(k) where k = number of segments in route
- Linear scan through route
- Constant time per segment

### Overall Complexity

**Total Time Complexity**: O(n² + E log V + k)
- Dominated by graph construction for small graphs
- For this prototype: All operations complete in milliseconds

**Space Complexity**: O(n² + k)
- Graph storage: O(n²) for dense graphs
- Route storage: O(k)

## Charging Strategy

The current implementation uses a **greedy charging strategy**:

1. Drive until battery would drop below 0%
2. Charge to 100% at the previous city (if it has a station)
3. Continue to next segment

### Assumptions

- **Instant Charging**: Charging time is not modeled
- **Full Charge**: Always charge to 100%
- **No Degradation**: Battery capacity doesn't degrade
- **Deterministic Consumption**: Energy use is purely distance-based

### Limitations

This greedy approach is **not globally optimal**. Consider:

```
Route: A → B → C → D
Charging at: B, C

Better strategy might be:
Route: A → B → C → D
Charging at: B only (with partial charge)
```

For a production system, this would require:
- Charging time optimization
- Partial charging strategies
- Dynamic programming for optimal charging schedule

## Data Model

### City Locations

Cities are represented in a simplified 2D coordinate system:

```python
locations = {
    "Los Angeles": (0, 0),
    "Bakersfield": (110, 0),
    "Fresno": (220, 0),
    "Modesto": (300, 0),
    "San Francisco": (380, 0)
}
```

**Simplification**: Uses straight-line distances along x-axis
**Reality**: Actual roads follow complex paths with elevation changes

### Distance Calculation

```python
distance = sqrt((x2 - x1)² + (y2 - y1)²)
```

For this prototype, all cities are on y=0, so:
```python
distance = abs(x2 - x1)
```

## Error Handling

The system handles several error conditions:

### 1. No Path Exists
**Cause**: Battery range too small to connect start and end
**Response**: Display error message, suggest increasing range

### 2. Infeasible Segment
**Cause**: Single segment exceeds battery range
**Response**: Identify problematic segment, explain constraint violation

### 3. Missing Charging Station
**Cause**: Battery depleted at city without charging
**Response**: Explain which city needs charging infrastructure

### 4. Invalid Inputs
**Cause**: Same start and destination
**Response**: Validation error with clear message

## Future Improvements

### 1. Real Road Network Data
**Current**: Simplified 2D coordinates
**Enhancement**: Integration with OpenStreetMap or Google Maps
**Benefit**: Realistic distances and actual road networks

### 2. Charging Station APIs
**Current**: Hardcoded station list
**Enhancement**: Live data from ChargePoint, Electrify America
**Benefit**: Real-time availability and station details

### 3. Terrain & Payload Modeling
**Current**: Distance-only energy consumption
**Enhancement**: 
- Elevation gain/loss impact
- Payload weight effects
- Weather conditions (wind, temperature)
**Benefit**: More accurate battery predictions

### 4. Charging Time Optimization
**Current**: Instant, full charging
**Enhancement**:
- Charging curve modeling (fast initially, slower near full)
- Partial charging strategies
- Time-optimal vs. distance-optimal routes
**Benefit**: Minimize total trip time

### 5. Electricity Price Awareness
**Current**: No cost modeling
**Enhancement**:
- Time-of-use electricity pricing
- Charge during off-peak hours when possible
- Cost-optimal charging schedules
**Benefit**: Reduce operational costs

### 6. Fleet-Level Optimization
**Current**: Single truck routing
**Enhancement**:
- Multi-truck dispatch optimization
- Shared charging infrastructure management
- Load balancing across fleet
**Benefit**: System-wide efficiency gains

### 7. Machine Learning Integration
**Current**: Deterministic energy model
**Enhancement**:
- Learn actual energy consumption patterns
- Driver behavior modeling
- Predictive maintenance for batteries
**Benefit**: Improved accuracy over time

### 8. Advanced Algorithms
**Current**: Greedy charging strategy
**Enhancement**:
- Dynamic programming for optimal charging
- A* search with better heuristics
- Multi-objective optimization (time, cost, battery health)
**Benefit**: Provably optimal solutions

## Testing Strategy

For production deployment, implement:

### Unit Tests
- Graph construction with various battery ranges
- Distance calculations
- Battery simulation edge cases
- Charging stop detection

### Integration Tests
- End-to-end route planning workflows
- Error handling scenarios
- UI interaction flows

### Performance Tests
- Large-scale graphs (1000+ cities)
- Complex route scenarios
- Concurrent user requests

### Validation Tests
- Compare against known optimal solutions
- Verify battery calculations
- Ensure charging stops are necessary and sufficient

## Deployment Considerations

### Scalability
- Current: Single-user Streamlit app
- Production: Multi-user web service with caching
- Database: Store historical routes and battery performance data

### Monitoring
- Route computation latency
- Error rates by scenario
- User interaction patterns

### Security
- Input validation (prevent injection attacks)
- Rate limiting for API calls
- Authentication for fleet management features

## Conclusion

This prototype demonstrates a **clean, modular approach** to EV truck route planning. The architecture separates concerns effectively, uses appropriate algorithms, and provides a foundation for future enhancements.

The key insight is modeling the problem as a **constrained graph traversal**, where battery range naturally limits the graph structure. This approach is both computationally efficient and conceptually clear.

While simplified for prototype purposes, the system architecture and algorithm choices are production-ready and can scale to real-world complexity with the enhancements outlined above.
