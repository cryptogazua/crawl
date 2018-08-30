import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.streaming.ProcessingTime
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import java.io.FileInputStream
import java.util.Properties

object sub {
  def main(args: Array[String]): Unit = {
    val p = new Properties()
    p.load(new FileInputStream("gazua.ini"))
    val url = p.getProperty("url")
    val user = p.getProperty("user")
    val pwd  = p.getProperty("pwd")
    
    val writer = new JDBCSink(url, user, pwd)
    val spark = SparkSession
      .builder()
      .appName("Steemit Subscriber")
      .master("local[4]")
      .getOrCreate()

    import spark.implicits._

    val schema = StructType(
      StructField("author", StringType, true) ::
      StructField("permlink", StringType, true) ::
      StructField("last_update", StringType, true) ::
      StructField("keyword", StringType, true) ::
      StructField("id", StringType, true) ::
      StructField("category", StringType, true) ::
      StructField("title", StringType, true) :: 
      StructField("body", StringType, true) :: 
      StructField("created", StringType, true) :: 
      StructField("net_votes", IntegerType, true) :: Nil
    )

    val df = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("subscribe", "steemit")
      .load()

    val values = df.select($"key" cast "string", $"value" cast "string").select($"key", from_json($"value", schema) as "data").select("key", "data.*")

    values.writeStream
      .foreach(writer)
      .outputMode("append")
      .trigger(ProcessingTime("10 seconds"))
      .start()
      .awaitTermination()
  }
}
