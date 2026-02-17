# backend/scraping/weekly_scraper.py

import os
import json
import time
import itertools
from datetime import datetime
from config import LINES
from route_scraper import scrape_route

DATA_FOLDER = "data"

# Example dates:
WEEKDAY_DATE = "17/02/2026"   # Tuesday
SATURDAY_DATE = "21/02/2026"
SUNDAY_DATE = "22/02/2026"


def load_existing_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def scrape_line(line_name, stations):
    print(f"Scraping {line_name}...")

    filepath = os.path.join(DATA_FOLDER, f"{line_name}.json")
    line_data = load_existing_data(filepath)

    station_pairs = [
        (a, b) for a, b in itertools.product(stations, stations)
        if a != b
    ]

    for from_station, to_station in station_pairs:

        if from_station not in line_data:
            line_data[from_station] = {}

        if to_station in line_data[from_station]:
            continue  # Skip already scraped

        print(f"  {from_station} → {to_station}")

        line_data[from_station][to_station] = {
            "weekday": scrape_route(from_station, to_station, WEEKDAY_DATE),
            "saturday": scrape_route(from_station, to_station, SATURDAY_DATE),
            "sunday": scrape_route(from_station, to_station, SUNDAY_DATE)
        }

        save_data(filepath, line_data)
        time.sleep(1)


def main():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    for line_name, stations in LINES.items():
        scrape_line(line_name, stations)


if __name__ == "__main__":
    main()
