# backend/scraping/station_scraper.py
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://cttrains.co.za/train-form.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_stations():
    print("🔹 Fetching stations...")
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        print("❌ Failed to fetch stations")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    select_depart = soup.find("select", {"name": "fromStation"})
    select_arrive = soup.find("select", {"name": "toStation"})

    stations = {}
    if select_depart:
        for opt in select_depart.find_all("option"):
            value = opt.get("value")
            name = opt.text.strip()
            if value and name:
                stations[name] = value

    # Save stations JSON
    with open("stations.json", "w", encoding="utf-8") as f:
        json.dump(stations, f, indent=4, ensure_ascii=False)

    print(f"✅ Total stations found: {len(stations)}")
    return stations

if __name__ == "__main__":
    scrape_stations()
