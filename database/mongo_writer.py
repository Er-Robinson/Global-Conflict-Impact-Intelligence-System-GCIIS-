from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["gciis"]
collection = db["news_stream"]

def insert_news(data):
    try:
        collection.insert_one(data)
        print("Inserted:", data["title"])
    except Exception as e:
        print("Mongo Error:", e)