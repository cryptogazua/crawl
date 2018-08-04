import findspark
findspark.init()
from pyspark.sql.session import SparkSession
from pyspark.sql import *
from pyspark.sql.functions import *
import pyspark
import time
sc = pyspark.SparkContext()

spark = SparkSession(sc)

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "steemit") \
  .load()

df_str = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
output = df_str.writeStream.outputMode("update").format("console").option("truncate", "false").trigger(processingTime='5 seconds').start()

i = 0
while True:
    time.sleep(1)
    i += 1
