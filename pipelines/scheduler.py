import schedule
import time
from ingestion.news_service import NewsIngestionService

service = NewsIngestionService()

def run_news_pipeline():
    service.fetch_news()

schedule.every(1).hours.do(run_news_pipeline)

while True:
    schedule.run_pending()
    time.sleep(60)