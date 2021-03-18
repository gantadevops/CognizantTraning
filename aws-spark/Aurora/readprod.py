from pyspark.sql  import SparkSession,DataFrameWriter
spark=SparkSession \
       .builder \
       .appName("Python Spark SQL basic example") \
       .config("spark-jars", "postgresql-42.2.14.jar") \
       .getOrCreate()


spark.sparkContext.setLogLevel("WARN")


ds=[(2,"banana"),(3,"orange")]
columns=['id',"name"]
df2=spark.createDataFrame(data=ds,schema=columns)

   # writing data to JDBC
df3=df2.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://aurora1-instance-1.ceves4tvnhxf.us-east-2.rds.amazonaws.com:5432/bigdb") \
    .option("dbtable", "products") \
    .option("user", "postgres") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()  
jdbcDF = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://aurora1-instance-1.ceves4tvnhxf.us-east-2.rds.amazonaws.com:5432/bigdb") \
    .option("dbtable", "products") \
    .option("user", "postgres") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
    .load()
jdbcDF.show()

