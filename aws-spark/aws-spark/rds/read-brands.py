import psycopg2
conn=psycopg2.connect("host=bigdata.ceves4tvnhxf.us-east-2.rds.amazonaws.com",
                      dbname="productdb",
                      user="postgres",
                      password="Sirisha123!")
cur=conn.cursor()
cur.execute("insert into brands (id,name) values(1,'banana')")
cur.execute("SELECT * from brands")
records=cur.fetchall()
print("Total rows", cur.rowcount)
for row in records:
    print(row)