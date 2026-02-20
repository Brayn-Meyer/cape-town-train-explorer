import json
import os
import osmnx as ox
import networkx as nx

# =========================
# CONFIG
# =========================

STATIONS_FILE = "stations.json"
GRAPH_FILE = "stations_graph.json"
OUTPUT_FILE = "railway_route_nodes.json"

SEARCH_RADIUS_METERS = 10000  # Increased radius
RAIL_FILTER = '["railway"]'   # Broader filter


# =========================
# LOAD DATA
# =========================

with open(STATIONS_FILE, "r", encoding="utf-8") as f:
    stations_data = json.load(f)

with open(GRAPH_FILE, "r", encoding="utf-8") as f:
    graph_data = json.load(f)

# Create quick lookup for station coordinates
station_lookup = {
    station["id"]: (station["lat"], station["lon"])
    for station in stations_data
}


# =========================
# FUNCTION: GET RAIL SEGMENT
# =========================

def get_rail_segment(start_id, end_id):
    if start_id not in station_lookup or end_id not in station_lookup:
        print(f"⚠️ Missing station: {start_id} or {end_id}")
        return []

    start_lat, start_lon = station_lookup[start_id]
    end_lat, end_lon = station_lookup[end_id]

    # Midpoint
    center_lat = (start_lat + end_lat) / 2
    center_lon = (start_lon + end_lon) / 2

    print(f"\n🔍 Fetching segment: {start_id} → {end_id}")
    print(f"Center: {center_lat}, {center_lon}")

    try:
        G = ox.graph_from_point(
            (center_lat, center_lon),
            dist=SEARCH_RADIUS_METERS,
            custom_filter=RAIL_FILTER,
            simplify=True
        )

        if len(G.nodes) == 0:
            print("⚠️ No railway nodes found in this area.")
            return []

        # Find nearest graph nodes
        start_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
        end_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

        # Shortest path
        route = nx.shortest_path(G, start_node, end_node, weight="length")

        # Extract coordinates
        coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route]

        return coords

    except Exception as e:
        print(f"❌ Failed segment {start_id} → {end_id}: {e}")
        return []


# =========================
# BUILD ROUTES
# =========================

routes_output = {}

for station in graph_data:
    current_id = station["id"]

    for next_id in station.get("front", []):
        route_name = f"{current_id}_to_{next_id}"

        coords = get_rail_segment(current_id, next_id)

        if coords:
            routes_output[route_name] = coords
        else:
            print(f"⚠️ Empty route: {route_name}")


# =========================
# SAVE OUTPUT
# =========================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(routes_output, f, indent=2)

print("\n✅ Done. Routes saved to:", OUTPUT_FILE)
