# backend/scraping/route_scraper.py

import requests
from bs4 import BeautifulSoup
from config import BASE_RESULTS_URL, HEADERS


def scrape_route(from_station, to_station, travel_date):
    params = {
        "fromStation": from_station,
        "toStation": to_station,
        "travelDate": travel_date,
        "departureTime": "05:00"
    }

    response = requests.get(BASE_RESULTS_URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    options = soup.find_all(string=lambda t: "Option" in t)

    for block in options:
        parent = block.find_parent()
        if not parent:
            continue

        option_data = {
            "departure": None,
            "arrival": None,
            "duration": None,
            "train_number": None,
            "stops": []
        }

        text = parent.get_text(separator=" ").strip()

        # Duration extraction
        if "Total Duration" in text:
            parts = text.split("Total Duration:")
            if len(parts) > 1:
                option_data["duration"] = parts[1].split()[0]

        rows = parent.find_all_next("tr")

        for row in rows:
            cols = [c.get_text(strip=True) for c in row.find_all("td")]

            if len(cols) >= 2:
                station = cols[0]
                time = cols[1]

                if not option_data["departure"]:
                    option_data["departure"] = time

                option_data["arrival"] = time
                option_data["stops"].append(station)

            if "Option" in row.get_text():
                break

        results.append(option_data)

    return results
