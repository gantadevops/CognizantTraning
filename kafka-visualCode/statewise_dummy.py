from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructField, StructType, IntegerType, StringType, DoubleType
import time
from pyspark import SparkContext
from pyspark.sql import SparkSession
import pyspark.sql.functions 
spark=SparkSession.builder.appName('statewise').getOrCreate()
df = spark.readStream.format("kafka")\
  .option("kafka.bootstrap.servers", "localhost:9092")\
  .option("subscribe", "orders")\
  .load()   
spark.sparkContext.setLogLevel("WARN")
dfDeserialized = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
#dfDeserialized.writeStream.outputMode("append").format("console").start()
schema = StructType(
        [
                StructField("order_id", IntegerType()),
                StructField("item_id", StringType()),
                StructField("price", IntegerType()),
                StructField("qty", IntegerType()),
                StructField("state", StringType()),
        ]
)
jsonDf = dfDeserialized.withColumn("value", from_json("value", schema))\
    .select(col('value.*'))
    
df=jsonDf.withColumn("totals",col("price") * col("qty"))

df.printSchema()
# NOTE: sum should be from spark.
import pyspark.sql.functions as F
#df_added_time=df.withColumn("time_stamp", F.current_timestamp())
df_grouped=df.groupBy("state").agg(F.sum("totals").alias("TotalAmount"))
df_grouped.printSchema()
#df_grouped=df_added_time.groupBy("state",window(col("time_stamp"),"5 minutes")).agg(F.sum("totals").alias("Total Amount"))
#df_grouped.writeStream.outputMode("update").format("console").start().awaitTermination()

# publishing the grouped data to statewise_earnings

dff= df_grouped.withColumn("json_col",F.to_json(F.struct([df_grouped[k] for k in df_grouped.columns]))) \
     .withColumnRenamed("state","key") \
      .withColumnRenamed("json_col","value") \
      .drop("TotalAmount") \
      .selectExpr('CAST(key AS STRING)','CAST(value AS STRING)')


query= dff \
    .writeStream \
    .format("kafka") \
    .outputMode("update") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "statewise_earnings") \
    .option("checkpointLocation", "/home/ubuntu/test3") \
    .start().awaitTermination()

# writing to RDS

#final_df=df2.write.format("jdbc") 
 #   .option("url", "jdbc:postgresql://bigdata.ceves4tvnhxf.us-east-2.rds.amazonaws.com:5432/productdb") 
  #  .option("dbtable", "ordergrouped") 
  # .option("user", "postgres") 
  #  .option("password", "Sirisha123!") 
   # .option("driver", "org.postgresql.Driver") 
   # .mode("append") 
   # .save()


