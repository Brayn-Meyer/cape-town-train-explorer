import requests
from bs4 import BeautifulSoup

#Scraping all Southern line train stations
url = "https://cttrains.co.za/ss_route_select.php"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

depart_dropdown = soup.find("select", {"name": "departStation"})

stations = {}

for option in depart_dropdown.find_all("option"):
    name = option.text.strip()
    value = option.get("value")
    if value and name:
        stations[name] = value

print("Total stations found:", len(stations))
print(stations)

#Generating station pairs
station_items = list(stations.items())

route_pairs = []

for i in range(len(station_items)):
    for j in range(len(station_items)):
        if i !=j: #skips the same station
            depart_name, depart_id = station_items[i]
            arrive_name, arrive_id = station_items[j]

            route_pairs.append({
                "depart_name": depart_name,
                "depart_id": depart_id,
                "arrive_name": arrive_name,
                "arrive_id": arrive_id
            })

print("Total Route pairs:", len(route_pairs))

#Test scraping one Pair DYNAMICALLY

import time

url = "https://cttrains.co.za/ss_validate.php"

payload = {
    "departStation": test_route["depart_id"],
    "arriveStation": test_route["arrive_id"],
    "travel_day": "Mon-Fri",
    "search_time": "Departure",
    "HH": "00",
    "MM": "00"
}

response = requests.post(url, data=payload)
soup = BeautifulSoup(response.text, "html.parser")

if "Train No" in soup.text:
    print(f"Timetable found for {test_route['depart_name']} → {test_route['arrive_name']} ✅")
else:
    print(f"No timetable for {test_route['depart_name']} → {test_route['arrive_name']} ❌")