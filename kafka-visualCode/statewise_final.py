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

import pyspark.sql.functions as F
df_added_time=df.withColumn("time_stamp", F.current_timestamp())
df_grouped=df_added_time.groupBy("state",window(col("time_stamp"),"5 minutes")).agg(F.sum("totals").alias("TotalAmount"))
df_selected=df_grouped.select(col("state"),col("TotalAmount"))


# publishing the grouped data to statewise_earnings



query= df_selected\
    .selectExpr("CAST(state AS STRING) AS key","to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .outputMode("update") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "statewise_earnings") \
    .option("checkpointLocation", "/home/ubuntu/test3") \
    .start().awaitTermination()