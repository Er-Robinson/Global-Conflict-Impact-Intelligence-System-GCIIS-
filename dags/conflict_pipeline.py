from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "gciis",
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    "global_conflict_pipeline",
    default_args=default_args,
    start_date=datetime(2024,1,1),
    schedule_interval="*/5 * * * *",
    catchup=False
) as dag:

    fetch_news = BashOperator(
        task_id="fetch_news",
        bash_command="python producers/news_producer.py"
    )

    spark_processing = BashOperator(
        task_id="spark_processing",
        bash_command="spark-submit spark/stream_processor.py"
    )

    store_mongo = BashOperator(
        task_id="store_mongo",
        bash_command="python pipelines/store_mongo.py"
    )

    retrain_model = BashOperator(
        task_id="retrain_model",
        bash_command="python ai/train_model.py"
    )

    fetch_news >> spark_processing >> store_mongo >> retrain_model