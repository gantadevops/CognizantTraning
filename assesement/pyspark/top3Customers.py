from pyspark.sql  import SparkSession
from pyspark.sql.functions import col,sum,rank
from pyspark.sql.window import Window
spark=SparkSession \
       .builder \
       .appName("Python Spark SQL basic example") \
       .config("spark-jars", "postgresql-42.2.14.jar") \
       .getOrCreate()

# Create a data frame by reading data from SQL Server via JDBC
spark.sparkContext.setLogLevel("WARN")
jdbcDF = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://bigdata.ceves4tvnhxf.us-east-2.rds.amazonaws.com:5432/productdb") \
    .option("dbtable", "Invoice_RDS") \
    .option("user", "postgres") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
    .load()
jdbcDF.show()
jdbcDF.createOrReplaceTempView("sparkdata")
invoice_df1=jdbcDF.withColumn("Amount-Spent",col("Quantity")*col("UnitPrice"))
filterdf=invoice_df1.filter("Quantity >0 and InvoiceNo not like '%C' and CustomerID is not null")
grouped_data=filterdf.groupBy("Country","CustomerID").sum("Amount-Spent").withColumnRenamed("sum(Amount-Spent)","Total_Amount_ByCountry")
grouped_data.show()

#selecting top 3 customers from each country
window=Window.partitionBy(grouped_data["Country"]).orderBy(grouped_data["Total_Amount_ByCountry"].desc())
final_data=grouped_data.select('*',rank().over(window).alias('rank')).filter(col('rank')<=3)
final_data.show()

# writing to RS

spark.sql("set spark.sql.caseSensitive=false")
   

final_data.write.format("jdbc") \
    .option("url", "jdbc:postgresql://redshift-cluster-1.c1tni9kl9hys.us-east-2.redshift.amazonaws.com:5439/dev") \
    .option("dbtable", "Top3Customers") \
    .option("user", "awsuser") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
     .mode("overwrite") \
    .save()


SELECT
 public.customer.name,
 public.customer.gender,
 public.customer.c_id,
 moviedb_schema.movies.id,
 moviedb_schema.movies.name,
 moviedb_schema.movies.year,
 moviedb_schema.ratings_datalake.rating
FROM  moviedb_schema.movies
JOIN moviedb_schema.ratings_datalake
  ON moviedb_schema.movies.id = moviedb_schema.ratings_datalake.id
JOIN public.customer
  ON moviedb_schema.ratings_datalake.userid = public.customer.c_id
