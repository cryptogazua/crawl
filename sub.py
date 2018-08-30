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
  .add("author", StringType()) \
  .add("permlink", StringType()) \
  .add("last_update", StringType()) \
  .add("keyword", StringType()) \
  .add("id", StringType()) \
  .add("category", StringType()) \
  .add("title", StringType()) \
  .add("body", StringType()) \
  .add("created", StringType()) \
  .add("net_votes", IntegerType())

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "steemit") \
  .load() \
  .select(col("key").cast("string"), from_json(col("value").cast("string"), schema).alias("parsed_value"))

df_str = df.select(col("key"), col("parsed_value.*"))
output = df_str.writeStream.format("console").option("truncate", "false").trigger(processingTime='1 seconds').start()

i = 0
while True:
    time.sleep(1)
    i += 1
