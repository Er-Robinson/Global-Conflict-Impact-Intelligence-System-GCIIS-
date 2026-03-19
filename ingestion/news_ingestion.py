import requests
import pandas as pd
import time
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("data/raw/news")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_news():

    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": "conflict OR war",
        "mode": "ArtList",
        "maxrecords": 20,
        "format": "json"
    }

    for attempt in range(3):

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            articles = data.get("articles", [])

            df = pd.DataFrame(articles)

            filename = OUTPUT_DIR / f"news_{datetime.now().date()}.csv"

            df.to_csv(filename, index=False)

            print("Saved", len(df), "articles")

            return

        elif response.status_code == 429:
            print("Rate limited. Waiting 60 seconds...")
            time.sleep(60)

    print("Failed to fetch news")

if __name__ == "__main__":
    fetch_news()