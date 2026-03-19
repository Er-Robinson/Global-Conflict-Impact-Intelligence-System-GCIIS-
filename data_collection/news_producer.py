import requests
import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

API_KEY = "9dd243c696ac42f384e704c2652817f2"

url = f"https://newsapi.org/v2/everything?q=war OR conflict OR military&apiKey={API_KEY}"

while True:

    response = requests.get(url)
    articles = response.json()["articles"]

    for a in articles:

        data = {
            "title": a["title"],
            "url": a["url"],
            "sourceCountry": a["source"]["name"],
            "language": "en"
        }

        producer.send("conflict-news", data)

    print("News pushed to Kafka")

    time.sleep(60)