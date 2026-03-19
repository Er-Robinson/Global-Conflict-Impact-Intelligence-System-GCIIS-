from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["conflictDB"]
collection = db["news"]

print(collection.count_documents({}))