from pyspark.sql  import SparkSession,DataFrameWriter
spark=SparkSession \
       .builder \
       .appName("Python Spark SQL basic example") \
       .config("spark-jars", "postgresql-42.2.14.jar") \
       .getOrCreate()
ds=spark.read.format("csv").option("header",True).option("inferSchema",True) \
       .load("C:/Users/Administrator/Downloads/temp_zipcodes.csv")
ds.printSchema()
spark.sql("set spark.sql.caseSensitive=false")
columns_to_drop = ['area_code','lat','lon','county']
df = ds.drop(*columns_to_drop).collect()
columns=['code','city','state']
df2=spark.createDataFrame(data=df,schema=columns)

final_df=df2.write.format("jdbc") \
    .option("url", "jdbc:postgresql://bigdata.ceves4tvnhxf.us-east-2.rds.amazonaws.com:5432/productdb") \
    .option("dbtable", "Zipcodes") \
    .option("user", "postgres") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()
