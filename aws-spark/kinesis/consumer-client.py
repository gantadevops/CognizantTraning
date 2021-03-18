
from boto.kinesis.exceptions import ProvisionedThroughputExceededException
import datetime
import boto
import time
import json

kinesis = boto.kinesis.connect_to_region("us-east-2")
shard_id = 'shardId-000000000000'
iterator_type = 'LATEST'
stream_name="gk-data-stream"

# get kinesis to get iterator / shared to read the data
response = kinesis.get_shard_iterator( stream_name, shard_id, iterator_type)
next_iterator = response['ShardIterator']

while True:
    response = kinesis.get_records(next_iterator, limit=25)
    records = response['Records']

    for record in records:
        part_key = record['PartitionKey']
        data = json.loads(record['Data'])

        print(part_key, ":", data[Quantity]*data[UnitPrice]
       # print("total price :", data.Quantity*data.UnitPrice)

    # in case, if we have more shared, this will help us to move to next shard, read data
    next_iterator = response['NextShardIterator']
    time.sleep(1) # debug purpose