import org.apache.spark.sql._
import java.sql._

class JDBCSink(url:String, user:String, pwd:String) extends ForeachWriter[Row] {
    val driver = "org.mariadb.jdbc.Driver"
    var connection:Connection = _
    var statement:Statement = _
    val sql = "INSERT INTO Steemit_MT VALUES(?,?,?,?,?,?,?,?,?,?) ON DUPLICATE KEY UPDATE keyword=?, ID=?, CATEGORY=?, TITLE=?, BODY=?, CREATED=?, NET_VOTES=?"

    def open(partitionId: Long, version: Long): Boolean = {
        Class.forName(driver)
        connection = DriverManager.getConnection(url, user, pwd)
        statement = connection.createStatement
        true
    }

    def process(value: Row): Unit = {
        if(value(1) == null) return
        val pstmt = connection.prepareStatement(sql)
        pstmt.setString(1, value(1).toString)
        pstmt.setString(2, value(2).toString)
        pstmt.setString(3, value(3).toString)
        pstmt.setString(4, value(4).toString)
        pstmt.setString(5, value(5).toString)
        pstmt.setString(6, value(6).toString)
        pstmt.setString(7, value(7).toString)
        pstmt.setString(8, value(8).toString)
        pstmt.setString(9, value(9).toString)
        pstmt.setInt(10, value(10).toString.toInt)
        pstmt.setString(11, value(4).toString)
        pstmt.setString(12, value(5).toString)
        pstmt.setString(13, value(6).toString)
        pstmt.setString(14, value(7).toString)
        pstmt.setString(15, value(8).toString)
        pstmt.setString(16, value(9).toString)
        pstmt.setInt(17, value(10).toString.toInt)
        try {
            pstmt.executeUpdate()
        } catch {
            case e: SQLException => { println("Exception ", e); }
        }
    }

    def close(errorOrNull:Throwable): Unit = {
        connection.close
    }
}
