
package examples

import scala.math.random
import scala.util.Random

object InvoiceProducer extends  App {
  // comments
  import java.util.Properties // producer settings
  // _ means import all
  import org.apache.kafka.clients.producer._

  val props = new Properties()
  props.put("bootstrap.servers", "localhost:9092")
  // kafka only knows bytes
  // producer to convert key to bytes, values to bytes
  // producer will have serializer
  // the key which is string type to bytes
  props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
  props.put("value.serializer", "examples.InvoiceSerializer")

  //[String, Invoice] means key is String type, Value  is Invoice type
  // value is converted to bytes by InvoiceSerializer
  val producer = new KafkaProducer[String, Invoice](props)

  val TOPIC = "invoices";
  val random: Random = new Random()

  val stock_codes= List("laptop", "mobile", "tablet", "monitor")
  for (i <- 1 to 10) {
    val key = "Order" + i // Order1, Order2...
    val stock_code = stock_codes(random.nextInt(stock_codes.size))
    val qty =1 + random.nextInt(20)
    //val invoice = Invoice(key, "laptop1", qty, 400) // value
    val invoice = Invoice(key, stock_code, qty, 400)
    val record = new ProducerRecord(TOPIC, key, invoice)
    println("Writing " + key + ":" + invoice)
    // this will call serialize to serialize invoice into json bytes
    producer.send(record)
    Thread.sleep(5000)
  }

  producer.close()
}