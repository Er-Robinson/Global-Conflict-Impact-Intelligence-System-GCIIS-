from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "conflict-news",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

for message in consumer:

    try:
        value = message.value.decode("utf-8")

        if not value:
            continue

        data = json.loads(value)

        print(data)

    except Exception as e:
        print("Skipping bad message:", e)