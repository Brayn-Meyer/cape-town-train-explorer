import json
from datetime import datetime, timedelta
from scraper import scrape_route

STATIONS = [
    "Langa",
    "Fish Hoek"
]


def scrape_week():
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())

    all_data = []

    for i in range(7):
        travel_date = (monday + timedelta(days=i)).strftime("%d/%m/%Y")

        for from_station in STATIONS:
            for to_station in STATIONS:
                if from_station != to_station:
                    print(f"Scraping {from_station} → {to_station} for {travel_date}")

                    routes = scrape_route(
                        from_station,
                        to_station,
                        travel_date,
                        "05:00"
                    )

                    all_data.append({
                        "from": from_station,
                        "to": to_station,
                        "date": travel_date,
                        "routes": routes
                    })

    # Save to JSON instead of MongoDB
    with open("weekly_routes.json", "w") as f:
        json.dump(all_data, f, indent=4)

    print("\n✅ Weekly data saved to weekly_routes.json")


if __name__ == "__main__":
    scrape_week()
