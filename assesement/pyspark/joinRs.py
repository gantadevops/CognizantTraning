from pyspark.sql  import SparkSession
from pyspark.sql.functions import avg,sum
spark=SparkSession \
       .builder \
       .appName("Python Spark SQL basic example") \
       .config("spark-jars", "postgresql-42.2.14.jar") \
       .getOrCreate()

# Create a data frame by reading data from SQL Server via JDBC
spark.sparkContext.setLogLevel("WARN")
movieDF = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://redshift-cluster-1.c1tni9kl9hys.us-east-2.redshift.amazonaws.com:5439/movies") \
    .option("dbtable", " movielens_rd.movies") \
    .option("user", "awsuser") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
    .load()
movieDF.show()
movieDF.createOrReplaceTempView('movies')

ratingDF = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://redshift-cluster-1.c1tni9kl9hys.us-east-2.redshift.amazonaws.com:5439/movies") \
    .option("dbtable", "movielens_rd.ratings") \
    .option("user", "awsuser") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
    .load()

ratingDF.show()
ratingDF.createOrReplaceTempView('ratings')

userDF = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://redshift-cluster-1.c1tni9kl9hys.us-east-2.redshift.amazonaws.com:5439/movies") \
    .option("dbtable", "users1") \
    .option("user", "awsuser") \
    .option("password", "Sirisha123!") \
    .option("driver", "org.postgresql.Driver") \
    .load()

userDF.show()
userDF.createOrReplaceTempView('users')


finaldf=spark.sql("select m.title, r.movieid, u.gender,u.c_id \
from ratings r join movies m on (m.movieid=r.movieid) \
join users u on (r.userid=u.c_id)")
    
finaldf.show()






