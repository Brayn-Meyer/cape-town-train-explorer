import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from config import BASE_URL, HEADERS


def scrape_route(from_station, to_station, travel_date, departure_time):
    params = {
        "fromStation": from_station,
        "toStation": to_station,
        "travelDate": travel_date,
        "departureTime": departure_time
    }

    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    options = re.split(r"Option \d+ -", text)
    results = []

    for i, option in enumerate(options[1:], start=1):
        duration_match = re.search(r"Total Duration:\s*(\d+)", option)
        duration = int(duration_match.group(1)) if duration_match else None

        train_numbers = re.findall(r"Train number:\s*(\d+)", option)

        departures = re.findall(
            r"(\d{2}:\d{2})\s*([A-Za-z ]+)\s*-\s*Departure",
            option
        )

        arrivals = re.findall(
            r"(\d{2}:\d{2})\s*([A-Za-z ]+)\s*-\s*Arrival",
            option
        )

        results.append({
            "option": i,
            "duration_minutes": duration,
            "train_numbers": train_numbers,
            "departures": departures,
            "arrivals": arrivals
        })

    return results


def get_fastest_option(routes):
    return min(routes, key=lambda x: x["duration_minutes"])
