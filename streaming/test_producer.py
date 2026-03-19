from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data = {
    "title": "War Update",
    "url": "cnn.com/news",
    "sourceCountry": "Ukraine",
    "language": "en"
}

producer.send("conflict-news", value=data)
producer.flush()