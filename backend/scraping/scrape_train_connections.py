import requests
import json
import time
import random

# Cycle through multiple Overpass servers for resilience
OVERPASS_SERVERS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.fr/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.nchc.org.tw/api/interpreter"
]

def generate_id(name):
    return name.lower().replace(" ", "_").replace("'", "").replace("-", "_")

def run_query(query, max_retries=3):
    for attempt in range(max_retries):
        for server in OVERPASS_SERVERS:
            try:
                response = requests.post(server, data={'data': query}, timeout=90)
                if response.status_code == 200 and response.text.strip():
                    return response.json()
                else:
                    print(f"Server {server} returned status {response.status_code}")
            except Exception as e:
                print(f"Error on {server}: {e}")
        wait = 5 * (attempt + 1) + random.randint(0, 5)
        print(f"Retrying in {wait}s...")
        time.sleep(wait)
    return None

def fetch_stations(relation_id):
    # Step 1: Get relation members
    query_relation = f"""
    [out:json][timeout:25];
    relation({relation_id});
    out body;
    """
    data = run_query(query_relation)
    if not data or not data.get("elements"):
        print(f"No relation data for {relation_id}")
        return []

    members = data["elements"][0].get("members", [])
    stop_ids = [m["ref"] for m in members if m["type"] == "node" and m.get("role") == "stop"]

    if not stop_ids:
        print(f"No stop nodes for relation {relation_id}")
        return []

    # Step 2: Fetch node details
    ids_str = ",".join(map(str, stop_ids))
    query_nodes = f"""
    [out:json][timeout:25];
    node({ids_str});
    out body;
    """
    data_nodes = run_query(query_nodes)
    if not data_nodes or not data_nodes.get("elements"):
        print(f"No node data for relation {relation_id}")
        return []

    id_to_name = {}
    for element in data_nodes.get("elements", []):
        name = element.get("tags", {}).get("name")
        if name:
            id_to_name[element["id"]] = name

    stations = [id_to_name[i] for i in stop_ids if i in id_to_name]
    return stations

def build_graph(lines):
    graph = {}
    for line in lines:
        for i, station in enumerate(line):
            sid = generate_id(station)
            if sid not in graph:
                graph[sid] = {"id": sid, "front": [], "rear": []}
            if i < len(line) - 1:
                graph[sid]["front"].append(generate_id(line[i+1]))
            if i > 0:
                graph[sid]["rear"].append(generate_id(line[i-1]))
    return graph

def main():
    # Relation IDs for Cape Town commuter corridors
    relation_ids = [948941, 952458, 952469, 952470, 952471, 956847, 956849, 956850, 957035]

    lines = []
    for rid in relation_ids:
        stations = fetch_stations(rid)
        print(f"Relation {rid}: {len(stations)} stations -> {stations}")
        lines.append(stations)
        time.sleep(10)  # throttle requests

    graph = build_graph(lines)

    with open("stations_graph.json", "w", encoding="utf-8") as f:
        json.dump(list(graph.values()), f, indent=2)

    print("Graph saved to stations_graph.json")

if __name__ == "__main__":
    main()
