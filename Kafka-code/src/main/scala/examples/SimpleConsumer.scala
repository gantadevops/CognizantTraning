
package examples
import java.util

import scala.collection.JavaConverters._

// Right click and Run SimpleConsumer

// Then goto SimpleProduct.scala, and run that too

object SimpleConsumer extends  App {
  import org.apache.kafka.clients.consumer.KafkaConsumer
  import java.util.Properties

  val props = new Properties()
  props.put("bootstrap.servers", "localhost:9092")
  // deserializer
  // kafka broker has bytes
  // consumer should convert the bytes to string format
  props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
  props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
  props.put("group.id", "scala-consumer-greetings")

  //[String, String] means key is String type, Value also string type
  val consumer = new KafkaConsumer[String, String](props)

  val TOPIC = "greetings"
  consumer.subscribe( util.Collections.singletonList(TOPIC))

  while (true) {
    // consumer poll data from broker
    val records = consumer.poll(500)
    for (record <- records.asScala) {
      val key = record.key()
      val value = record.value()

      println("Got message " + key + ":" + value)
    }
  }
}
