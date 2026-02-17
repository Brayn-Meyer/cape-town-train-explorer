# backend/scraping/config.py

BASE_FORM_URL = "https://cttrains.co.za/train-form.php"
BASE_RESULTS_URL = "https://cttrains.co.za/train-schedule.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# -------------------------
# LINE DEFINITIONS
# -------------------------

LINES = {
    "southern_line": [
        "Cape Town", "Woodstock", "Salt River", "Observatory",
        "Mowbray", "Rondebosch", "Newlands", "Claremont",
        "Kenilworth", "Harfield Road", "Wynberg", "Plumstead",
        "Steenberg", "Retreat", "Lakeside", "False Bay",
        "Muizenberg", "St James", "Kalk Bay", "Fish Hoek",
        "Sunny Cove", "Glencairn", "Simon's Town"
    ],

    "northern_line": [
        "Cape Town", "Woodstock", "Salt River",
        "Bellville", "Brackenfell", "Kraaifontein",
        "Eerste River", "Strand", "Wellington"
    ],

    "central_line": [
        "Cape Town", "Woodstock", "Salt River",
        "Langa", "Bonteheuwel", "Netreg",
        "Heideveld", "Nyanga", "Philippi",
        "Mitchells Plain", "Kapteinsklip"
    ],

    "cape_flats_line": [
        "Athlone", "Heideveld", "Lavistown",
        "Belhar", "Pentech"
    ]
}

# -------------------------
# TRANSFER HUB RULES
# -------------------------

TRANSFER_HUBS = {
    ("southern_line", "northern_line"): "Cape Town",
    ("southern_line", "central_line"): "Cape Town",
    ("northern_line", "central_line"): "Bellville"
}
