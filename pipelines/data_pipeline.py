
import schedule
import time
from ingestion.news_ingestion import fetch_news

schedule.every(1).hours.do(fetch_news)

while True:
    schedule.run_pending()
    time.sleep(60)