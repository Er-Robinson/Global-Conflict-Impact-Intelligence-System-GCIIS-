from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType

# Create Spark session
spark = SparkSession.builder \
    .appName("ConflictNewsStream") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Schema of incoming Kafka data
schema = StructType() \
    .add("title", StringType()) \
    .add("url", StringType()) \
    .add("sourceCountry", StringType())

# Read Kafka stream
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "conflict-news") \
    .load()

# Convert binary value to string
json_df = df.selectExpr("CAST(value AS STRING)")

# Parse JSON
parsed_df = json_df.select(from_json(col("value"), schema).alias("data"))

final_df = parsed_df.select("data.*")

# Write to console
query = final_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()