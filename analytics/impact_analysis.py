from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["gciis"]

def analyze_conflict_impact():

    pipeline = [
        {
            "$group": {
                "_id": "$sourceCountry",
                "newsCount": {"$sum": 1}
            }
        },
        {"$sort": {"newsCount": -1}}
    ]

    results = db.news_stream.aggregate(pipeline)

    print("\n🌍 Conflict Impact Analysis\n")

    for r in results:
        print(f"{r['_id']} -> {r['newsCount']} news events")