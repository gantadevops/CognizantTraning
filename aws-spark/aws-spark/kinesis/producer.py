import boto3

import json

from datetime import datetime

import calendar

import random

import time



my_stream_name = 'gs-data-stream'


kinesis_client = boto3.client('kinesis', region_name='us-east-2')



def put_to_stream(InvoiceNo,StocCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerId,Country):
    # countries=['US','IN','UK','CA','RS']
    payload = {
             'InvoiceNo' : str(InvoiceNo),
             'Stock_Code': StockCode,
              'Description': str(Description),
             'Quantity': Quantity,
              'invoice_Date':str(InvoiceDate),
              'Unitprice':UnitPrice,
              'Cust_id':CustomerId,
              'Coutry':Country


    }



    print(payload)



    put_response = kinesis_client.put_record(

                        StreamName=my_stream_name,

                        Data=json.dumps(payload),

                        PartitionKey=Country)



while True:

    InvoiceNo= '536365'
    StockCode= random.randint(60000,90000)
    Description= "All are mobiles"
    Quantity= random.randint(1,10)
    InvoiceDate=calendar.timegm(datetime.utcnow().timetuple())
    UnitPrice=random.randint(1,100)
    CustomerId ='1234'
    Country="USA"
        



    put_to_stream(InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerId,Country)



    # wait for 5 second

    time.sleep(5)