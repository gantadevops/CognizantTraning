import psycopg2
conn=psycopg2.connect(host="redshift-cluster-1.c1tni9kl9hys.us-east-2.redshift.amazonaws.com",
                      dbname="dev",
                      user="awsuser",
                      port='5439',
                      password="Sirisha123!")
cur=conn.cursor()
#cur.execute("insert into brands (id,name) values(1,'banana')")
cur.execute("SELECT * from brands1")
records=cur.fetchall()
print("Total rows", cur.rowcount)
for row in records:
    print(row)