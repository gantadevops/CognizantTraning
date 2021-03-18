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
#ds.createOrReplaceTempView("sparkdata")


final_df=ds.write.format("jdbc") \
    .option("url", "jdbc:postgresql://bigdata.ceves4tvnhxf.us-east-2.rds.amazonaws.com:5432/productdb") \
    .option("dbtable", "Invoice_RDS") \
    .option("user", "postgres") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()
