package assignment


import assignment.order
import scala.math.random
import scala.util.Random

object OrderProducer extends  App {
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
  props.put("value.serializer", "assignment.OrderSerializer")

  val producer = new KafkaProducer[String, order](props)

  val TOPIC = "orders";
  val random: Random = new Random()

  val state_code=List("AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                      "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                      "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX",
                       "UT", "VT", "VA", "WA", "WV", "WI", "WY")
  for (i <- 1 to 1000) {
    val key="Order" +i
    val order_id=100+random.nextInt(1000)
    val item_id=random.nextInt(100).toString
    val price= 1+random.nextInt(50)
    val qty=1+random.nextInt(10)
    val state= state_code(random.nextInt(state_code.size))

    val order_record = order(order_id,item_id,price,qty,state)
    val record = new ProducerRecord(TOPIC, key, order_record)
    println("Writing " + key + ":" + order_record)
    // this will call serialize to serialize invoice into json bytes
    producer.send(record)
    Thread.sleep(5000)
  }

  producer.close()
}
