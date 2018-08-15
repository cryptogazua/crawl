import findspark
findspark.init()
from pyspark.sql.session import SparkSession
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pyspark
import time

sc = pyspark.SparkContext()

spark = SparkSession(sc)

schema = StructType() \
  .add("eventTime", TimestampType()) \
  .add("open", FloatType()) \
  .add("high", FloatType()) \
  .add("low", FloatType()) \
  .add("close", FloatType()) \
  .add("change", FloatType()) \
  .add("rate", FloatType())

# https://databricks.com/blog/2017/04/26/processing-data-in-apache-kafka-with-structured-streaming-in-apache-spark-2-2.html
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "bithumb") \
  .load() \
  .select(col("key").cast("string"), from_json(col("value").cast("string"), schema).alias("parsed_value"))

df_str = df.select(col("key"), col("parsed_value.*"))
#df_str.printSchema()
df_count = df_str.groupBy(window(df_str.eventTime, "1 minutes"), col("key")).agg(first("close").alias("open"), max("close").alias("high"), min("close").alias("low"), last("close").alias("close"))

#output = df_str.writeStream.outputMode("update").format("console").option("truncate", "false").trigger(processingTime='1 seconds').start()
output = df_count.writeStream.outputMode("complete").format("console").option("truncate", "false").start()


i = 0
while True:
    time.sleep(1)
    i += 1
