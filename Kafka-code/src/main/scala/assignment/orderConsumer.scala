package assignment


import assignment.ordergrouped

import java.util
import scala.collection.JavaConverters._

object orderConsumer extends App {

  import org.apache.kafka.clients.consumer.KafkaConsumer

  import java.util.Properties

  val props = new Properties()
  props.put("bootstrap.servers", "localhost:9092")
  // deserializer
  // kafka broker has bytes
  // consumer should convert the bytes to string format
  props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
  // custom deserializer converting json bytes to Invoice object
  props.put("value.deserializer", "assignment.orderDeserializer")
  props.put("group.id", "scala-order-consumer3")


  val consumer = new KafkaConsumer[String, ordergrouped](props)
  val TOPIC = "statewise_earnings"
  consumer.subscribe(util.Collections.singletonList(TOPIC))

  while (true) {
    val records = consumer.poll(500)
    for (record <- records.asScala) {
      val partition = record.partition()
      val offset = record.offset()
      val key = record.key()
      val value: ordergrouped = record.value()
      println("Order Obj " + value)
      println("Got message Partition " + partition + ", offset  " + offset + " " + key + ":" + value)
      consumer.commitSync()
    }
  }
}
