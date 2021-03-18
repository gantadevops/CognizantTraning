from pyspark.sql  import SparkSession,DataFrameWriter
spark=SparkSession \
       .builder \
       .appName("Python Spark SQL basic example") \
       .config("spark-jars", "postgresql-42.2.14.jar") \
       .getOrCreate()
ds=spark.read.format("csv").option("header",True).option("inferSchema",True) \
       .load("C:/Users/Administrator/Downloads/archive/data.csv")
ds.printSchema()
spark.sql("set spark.sql.caseSensitive=false")
ds.filter("InvoiceNo < 536400") \
     .write.format("jdbc") \
    .option("url", "jdbc:postgresql://redshift-cluster-1.c1tni9kl9hys.us-east-2.redshift.amazonaws.com:5439/dev") \
    .option("dbtable", "Invoice") \
    .option("user", "awsuser") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
     .mode("overwrite") \
    .save()