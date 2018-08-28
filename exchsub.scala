import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.streaming.ProcessingTime
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import java.io.FileInputStream
import java.util.Properties

object exchsub {
  def main(args: Array[String]): Unit = {
    val p = new Properties()
    p.load(new FileInputStream("gazua.ini"))
    val url = p.getProperty("url")
    val user = p.getProperty("user")
    val pwd  = p.getProperty("pwd")
    
    val writer = new ExchJDBCSink(url, user, pwd)
    val spark = SparkSession
      .builder()
      .appName("Spark Structured Streaming Example")
      .master("local[4]")
      .getOrCreate()

    import spark.implicits._

    val schema = StructType(
      StructField("eventTime", TimestampType, true) ::
      StructField("open", FloatType, true) ::
      StructField("high", FloatType, true) ::
      StructField("low", FloatType, true) ::
      StructField("close", FloatType, true) ::
      StructField("change", FloatType, true) ::
      StructField("rate", FloatType, true) :: Nil
    )

    val df = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("subscribe", "bithumb")
      .load()

    val values = df.select($"key" cast "string", $"value" cast "string").select($"key", from_json($"value", schema) as "data").select("key", "data.*")
    val df_count = values.groupBy($"key", window($"eventTime", "1 minutes")).agg(first("close").alias("open"), max("close").alias("high"), min("close").alias("low"), last("close").alias("close"))
    val df_res = df_count.select("key", "window.start", "open","high","low","close")

    /*df_count.writeStream
      //.trigger(ProcessingTime("1 seconds"))
      .outputMode("complete")
      .format("console")
      .start()
      .awaitTermination()*/
    df_res.writeStream
      .foreach(writer)
      .outputMode("complete")
      .trigger(ProcessingTime("30 seconds"))
      .start()
      .awaitTermination()
  }
}
