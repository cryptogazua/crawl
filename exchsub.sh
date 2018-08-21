#CLASSPATH=/usr/share/java/mysql.jar:$CLASSPATH
#export CLASSPATH
#echo $CLASSPATH
#$SPARK_HOME/bin/spark-submit --jars /usr/share/java/mysql.jar --packages mysql:mysql-connector-java --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.0 exchsub.py 2>/dev/null
$SPARK_HOME/bin/spark-submit --driver-class-path /usr/share/java/mysql.jar --jars /usr/share/java/mysql.jar --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.0 exchsub.py 2>/dev/null
