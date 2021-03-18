from boto.kinesis.exceptions import ProvisionedThroughputExceededException

import datetime

import boto

import time

kinesis = boto.kinesis.connect_to_region("us-east-2")



class KinesisConsumer:

    """Generic Consumer for Amazon Kinesis Streams"""

    def __init__(self, stream_name, shard_id, iterator_type,

                 worker_time=30, sleep_interval=0.5):



        self.stream_name = stream_name

        self.shard_id = str(shard_id)

        self.iterator_type = iterator_type

        self.worker_time = worker_time

        self.sleep_interval = sleep_interval



    def process_records(self, records):

        """the main logic of the Consumer that needs to be implemented"""

        raise NotImplementedError



    @staticmethod

    def iter_records(records):

        for record in records:

            part_key = record['PartitionKey']

            data = record['Data']

            yield part_key, data



    def run(self):

        """poll stream for new records and pass them to process_records method"""

        response = kinesis.get_shard_iterator(self.stream_name,

            self.shard_id, self.iterator_type)



        next_iterator = response['ShardIterator']



        start = datetime.datetime.now()

        finish = start + datetime.timedelta(seconds=self.worker_time)



        while finish > datetime.datetime.now():

            try:

                response = kinesis.get_records(next_iterator, limit=25)



                records = response['Records']



                if records:

                    self.process_records(records)



                next_iterator = response['NextShardIterator']

                time.sleep(self.sleep_interval)

            except ProvisionedThroughputExceededException as ptee:

                time.sleep(1)



class EchoConsumer(KinesisConsumer):

    """Consumers that echos received data to standard output"""

    def process_records(self, records):

        """print the partion key and data of each incoming record"""

        for part_key, data in self.iter_records(records):

            print(part_key, ":", data)



shard_id = 'shardId-000000000000'

iterator_type = 'LATEST'

stream_name="gs-data-stream"

worker = EchoConsumer(stream_name, shard_id, iterator_type, worker_time=10)



worker.run()