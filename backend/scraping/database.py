from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# ==========================
# Database information needed
# =============================
client = MongoClient(MONGO_URI)
db = client[DB_NAME] #database name needed
collection = db[COLLECTION_NAME]


def save_weekly_data(data):
    collection.delete_many({})  # clear old week
    collection.insert_many(data)


def get_cached_route(from_station, to_station, date):
    return collection.find_one({
        "from": from_station,
        "to": to_station,
        "date": date
    })
