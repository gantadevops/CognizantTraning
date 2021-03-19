package examples

import org.apache.kafka.clients.consumer.ConsumerRebalanceListener
import org.apache.kafka.common.TopicPartition

import java.util
import scala.collection.JavaConverters._

object OrderConsumer extends App {
  import org.apache.kafka.clients.consumer.KafkaConsumer
  import java.util.Properties

  val props = new Properties()
  props.put("bootstrap.servers", "localhost:9092")
  // deserializer
  // kafka broker has bytes
  // consumer should convert the bytes to string format
  props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
  props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
  props.put("group.id", "scala-order-consumer")

  //[String, String] means key is String type, Value also string type
  val consumer = new KafkaConsumer[String, String](props)

  val TOPIC = "orders"
  consumer.subscribe( util.Collections.singletonList(TOPIC), new ConsumerRebalanceListener {
    // is invoked when kafka revoke all the assigned partitions assigned to this instance
    override def onPartitionsRevoked(collection: util.Collection[TopicPartition]): Unit = {
      println("onPartitionsRevoked " + collection)
    }

    // called when kafka assign 0, 1 or more partitions
    override def onPartitionsAssigned(collection: util.Collection[TopicPartition]): Unit =  {
      println("onPartitionsAssigned " + collection)
    }
  })

  while (true) {
    // consumer poll data from broker
    //println("Waiting for records")
    val records = consumer.poll(500)
    //println("Got " + records.asScala.size + " records")
    // asScala convers Java collection to scala collection
    for (record <- records.asScala) {
      val partition = record.partition()
      val offset = record.offset()
      val key = record.key()
      val value = record.value()

      println("Got message Partition " + partition + ", offset  " + offset  + " " + key + ":" + value)
    }
  }
}