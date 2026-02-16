import overpy
import json
from pathlib import Path

def load_line_map(json_file="stations_by_line.json"):
    json_path = Path(__file__).resolve().parent / json_file
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            stations = json.load(f)
        return {
            station.get("name", "").strip(): station.get("lines", ["Unknown"])
            for station in stations
            if station.get("name")
        }
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Dictionary mapping station names to their line(s), sourced from stations_by_line.json
LINE_MAP = load_line_map()

def clean_stations(stations):
    cleaned = []
    seen = set()
    MIN_LAT, MAX_LAT = -34.4, -33.6
    MIN_LON, MAX_LON = 18.2, 19.0
    
    for station in stations:
        name = station.get("name", "").strip()
        lat = station.get("lat")
        lon = station.get("lon")
        
        if not name or name == "Unnamed Stop":
            continue
        if not (MIN_LAT <= lat <= MAX_LAT and MIN_LON <= lon <= MAX_LON):
            continue
        
        key = (name.lower(), round(lat, 4), round(lon, 4))
        if key in seen:
            continue
        
        seen.add(key)
        cleaned.append({
            "name": name,
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "lines": LINE_MAP.get(name, ["Unknown"])  # attach line info
        })
    
    cleaned.sort(key=lambda x: x["name"].lower())
    return cleaned

def export_to_json(stations, output_file="stations.json"):
    with open(output_file, "w") as f:
        json.dump(stations, f, indent=2, ensure_ascii=False)
    print(f"✓ Exported {len(stations)} stations to {output_file}")

# Main script
api = overpy.Overpass()

query = """
(
  node["railway"="station"]( -34.4, 18.2, -33.6, 19.0 );
  node["railway"="halt"]( -34.4, 18.2, -33.6, 19.0 );
);
out;
"""

print("Querying Overpass API for train stations...")
result = api.query(query)

stations = []
for node in result.nodes:
    name = node.tags.get("name", "Unnamed Stop")
    stations.append({
        "name": name,
        "lat": float(node.lat),
        "lon": float(node.lon)
    })

print(f"Found {len(stations)} raw stops")

cleaned_stations = clean_stations(stations)
print(f"Cleaned to {len(cleaned_stations)} unique, named stops")

export_to_json(cleaned_stations)

print("\nSample of cleaned data:")
for s in cleaned_stations[:5]:
    print(f"  - {s['name']}: ({s['lat']}, {s['lon']}) on {', '.join(s['lines'])}")
