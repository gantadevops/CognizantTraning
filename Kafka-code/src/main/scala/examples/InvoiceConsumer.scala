
package examples

import org.apache.kafka.clients.consumer.ConsumerRebalanceListener
import org.apache.kafka.common.TopicPartition

import java.util
import scala.collection.JavaConverters._

object InvoiceConsumer extends App {
  import org.apache.kafka.clients.consumer.KafkaConsumer

  import java.util.Properties

  val props = new Properties()
  props.put("bootstrap.servers", "localhost:9092")
  // deserializer
  // kafka broker has bytes
  // consumer should convert the bytes to string format
  props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
  // custom deserializer converting json bytes to Invoice object
  props.put("value.deserializer", "examples.InvoiceDeserializer")
  props.put("group.id", "scala-invoice-consumer")

  //[String, Invoice] means key is String type, Value is Invoice  type
  val consumer = new KafkaConsumer[String, Invoice](props)

  val TOPIC = "invoices"
  consumer.subscribe( util.Collections.singletonList(TOPIC))

  while (true) {
    // consumer poll data from broker
    // poll function internally calls deserialize function
    // that converts bytes to invoice
    val records = consumer.poll(500)

    for (record <- records.asScala) {
      val partition = record.partition()
      val offset = record.offset()
      val key = record.key()

      // object type, by deserializer
      val value: Invoice = record.value()

      println("Invoice Obj " + value)
      println("Got message Partition " + partition + ", offset  " + offset  + " " + key + ":" + value)
    }
  }
}