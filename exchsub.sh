#CLASSPATH=/usr/share/java/mysql.jar:$CLASSPATH
$SPARK_HOME/bin/spark-submit --master local[*] --class exchsub --driver-class-path mariadb-java-client-2.2.6.jar --jars mariadb-java-client-2.2.6.jar --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.0 target/scala-2.11/simple-project_2.11-1.0.jar 2>/dev/null
