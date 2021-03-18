from pyspark.sql  import SparkSession
spark=SparkSession \
       .builder \
       .appName("Python Spark SQL basic example") \
       .config("spark-jars", "postgresql-42.2.14.jar") \
       .getOrCreate()

# Create a data frame by reading data from SQL Server via JDBC
spark.sparkContext.setLogLevel("WARN")
jdbcDF = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://bigdata.ceves4tvnhxf.us-east-2.rds.amazonaws.com:5432/productdb") \
    .option("dbtable", "brands") \
    .option("user", "postgres") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
    .load()
jdbcDF.show()
