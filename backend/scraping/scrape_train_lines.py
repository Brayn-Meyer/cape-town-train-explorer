import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

# Config values inline
BASE_URL = "https://cttrains.co.za"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0 Safari/537.36"
}

# Map each cttrains URL to its line name
LINE_URLS = {
    f"{BASE_URL}/ss_route_select.php": "Southern Line",
    f"{BASE_URL}/ns_bell_route_select.php": "Northern Line",
    f"{BASE_URL}/CT_KYL_route_select.php": "Central Line",
    f"{BASE_URL}/cf_route_select.php": "Cape Flats Line"
    # f"{BASE_URL}/malmesbury_route_select.php": "Malmesbury Line"  # if available
}

def scrape_line(url, line_name):
    """Scrape all stations from a cttrains line page and tag them with the line."""
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    stations = []
    for option in soup.select("select#departStation option"):
        name = option.text.strip()
        if name and not re.search(r"select", name, re.I):
            stations.append({"name": name, "lines": [line_name]})
    return stations

def scrape_all_lines():
    all_stations = []
    for url, line_name in LINE_URLS.items():
        print(f"Scraping {line_name} from {url}...")
        try:
            stations = scrape_line(url, line_name)
            all_stations.extend(stations)
        except Exception as e:
            print(f"⚠️ Failed to scrape {line_name}: {e}")

    # Deduplicate: merge lines for stations appearing on multiple routes
    merged = {}
    for s in all_stations:
        if s["name"] not in merged:
            merged[s["name"]] = {"name": s["name"], "lines": set()}
        merged[s["name"]]["lines"].update(s["lines"])

    # Convert sets to lists
    final_list = [{"name": v["name"], "lines": sorted(list(v["lines"]))} for v in merged.values()]
    return final_list

if __name__ == "__main__":
    stations = scrape_all_lines()
    print(f"\n✓ Found {len(stations)} unique stations at {datetime.now().isoformat()}")

    # Save to JSON
    with open("stations_by_line.json", "w", encoding="utf-8") as f:
        json.dump(stations, f, indent=2, ensure_ascii=False)

    # Preview
    for s in stations[:10]:
        print(f" - {s['name']}: {', '.join(s['lines'])}")
