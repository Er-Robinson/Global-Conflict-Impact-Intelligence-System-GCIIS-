import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analytics.casualty_analyzer import extract_casualties
from analytics.severity_score import compute_war_severity
from analytics.economic_impact import estimate_economic_impact
from analytics.refugee_detector import detect_refugee_crisis
from analytics.energy_risk import detect_energy_risk
from analytics.food_risk import detect_food_risk
from analytics.market_impact import detect_market_impact
from analytics.social_unrest import detect_unrest
from analytics.country_risk import compute_country_risk
from analytics.escalation_predictor import predict_escalation
from analytics.sentiment_model import get_sentiment
from analytics.conflict_classifier import classify_conflict
from analytics.weapon_detector import detect_weapon
from analytics.location_detector import detect_location

from database.mongo_writer import insert_news

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, lower, regexp_replace
from pyspark.sql.types import StructType, StringType

# -------------------------
# Spark Session
# -------------------------

spark = SparkSession.builder \
    .appName("ConflictNewsStream") \
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.1"
    ) \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# -------------------------
# Schema
# -------------------------

news_schema = StructType() \
    .add("title", StringType()) \
    .add("url", StringType()) \
    .add("sourceCountry", StringType()) \
    .add("language", StringType())

# -------------------------
# Read Kafka
# -------------------------

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "conflict-news") \
    .option("startingOffsets", "latest") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING) as json")

parsed_df = json_df.select(
    from_json(col("json"), news_schema).alias("data")
)

final_df = parsed_df.select("data.*")

# -------------------------
# Clean Title
# -------------------------

clean_df = final_df.withColumn(
    "clean_title",
    lower(regexp_replace(col("title"), "[^a-zA-Z ]", ""))
)

# -------------------------
# Mongo Writer
# -------------------------

def write_to_mongo(batch_df, batch_id):

    rows = batch_df.collect()

    for row in rows:

        text = row["clean_title"] if row["clean_title"] else ""

        casualties = extract_casualties(text)

        severity = compute_war_severity(casualties, text)

        economic = estimate_economic_impact(text)

        refugee = detect_refugee_crisis(text)

        energy = detect_energy_risk(text)

        food = detect_food_risk(text)

        market = detect_market_impact(text)

        unrest = detect_unrest(text)
        sentiment, sentiment_score = get_sentiment(text)

        conflict_type = classify_conflict(text)

        weapons = detect_weapon(text)

        location = detect_location(text)

        country_risk = compute_country_risk(severity, economic)

        escalation = predict_escalation(severity)

        data = {

            "title": row["title"],
            "url": row["url"],
            "sourceCountry": row["sourceCountry"],
            "language": row["language"],

            "clean_title": text,

            "casualties": casualties,
            "severity_score": severity,

            "economic_risk": economic,
            "refugee_crisis": refugee,
            "energy_risk": energy,
            "food_risk": food,
            "market_impact": market,
            "social_unrest": unrest,

            "country_risk_index": country_risk,
            "escalation_level": escalation
            data = {

            "title": row["title"],
            "url": row["url"],

            "severity_score": severity,
            "casualties": casualties,

            "sentiment": sentiment,
            "sentiment_score": sentiment_score,

            "conflict_type": conflict_type,

            "weapons_detected": weapons,

            "strategic_location": location,

            "economic_risk": economic,
            "energy_risk": energy,
            "food_risk": food,

            "refugee_crisis": refugee,

            "market_impact": market,
            "social_unrest": unrest,

            "country_risk_index": country_risk,

            "escalation_level": escalation

        }

        insert_news(data)

    print(f"Batch {batch_id} written to MongoDB")

query = clean_df.writeStream \
    .foreachBatch(write_to_mongo) \
    .start()

spark.streams.awaitAnyTermination()