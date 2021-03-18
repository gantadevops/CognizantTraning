from pyspark.sql  import SparkSession
spark=SparkSession \
       .builder \
       .appName("Python Spark SQL basic example") \
       .config("spark-jars", "postgresql-42.2.14.jar") \
       .getOrCreate()

# Create a data frame by reading data from SQL Server via JDBC
spark.sparkContext.setLogLevel("WARN")
jdbcDF = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://redshift-cluster-1.c1tni9kl9hys.us-east-2.redshift.amazonaws.com:5439/dev") \
    .option("dbtable", "Invoice") \
    .option("user", "awsuser") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
    .load()
jdbcDF.createOrReplaceTempView("sparkdata")

df1=spark.sql("select * from sparkdata where invoiceno = '536365'")
df1.show()

# writing back to db
spark.sql("set spark.sql.caseSensitive=false")
df1.write.format("jdbc") \
    .option("url", "jdbc:postgresql://redshift-cluster-1.c1tni9kl9hys.us-east-2.redshift.amazonaws.com:5439/dev") \
    .option("dbtable", "Invoice_536365") \
    .option("user", "awsuser") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
     .mode("overwrite") \
    .save()

