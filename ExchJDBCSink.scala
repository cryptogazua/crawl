import org.apache.spark.sql._
import java.sql._

class ExchJDBCSink(url:String, user:String, pwd:String) extends ForeachWriter[Row] {
    val driver = "org.mariadb.jdbc.Driver"
    var connection:Connection = _
    var statement:Statement = _
    val sql = "INSERT INTO quote VALUES(?,?,?,?,?,?)"

    def open(partitionId: Long, version: Long): Boolean = {
        Class.forName(driver)
        connection = DriverManager.getConnection(url, user, pwd)
        statement = connection.createStatement
        //println(sql)
        true
    }

    def process(value: Row): Unit = {
        //println(value)
        val pstmt = connection.prepareStatement(sql)
        pstmt.setString(1, value(0).toString)
        pstmt.setString(2, value(1).toString)
        pstmt.setDouble(3, value(2).toString.toDouble)
        pstmt.setDouble(4, value(3).toString.toDouble)
        pstmt.setDouble(5, value(4).toString.toDouble)
        pstmt.setDouble(6, value(5).toString.toDouble)
        pstmt.executeUpdate()
    }

    def close(errorOrNull:Throwable): Unit = {
        //connection.commit()
        connection.close
    }
}
