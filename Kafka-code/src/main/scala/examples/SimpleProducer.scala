package examples

// in linux terminal, run
// kafka-console-consumer --bootstrap-server localhost:9092 --topic greetings --group greetings-consumer-group --property print.key=true


// Right Click and Run SimpleProducer in Intellji


object SimpleProducer extends  App {
  // comments
  import java.util.Properties // producer settings
  // _ means import all
  import org.apache.kafka.clients.producer._

  val props = new Properties()
  props.put("bootstrap.servers", "localhost:9092")
  // kafka only knows bytes
  // convert key to bytes, values to bytes
  // producer will have serializer
  // the key which is string type to bytes
  props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
  props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")

  //[String, String] means key is String type, Value also string type
  val producer = new KafkaProducer[String, String](props)

  val TOPIC = "greetings";

  for (i <- 1 to 100) {
    val key = "Message" + i // KEY1, KEY2, KEY3....KEY100
    val value = "MESSAGE" + i // MESSAGE1, MESSAGE2,......
    val record = new ProducerRecord(TOPIC, key, value)
    println("Writing " + key + ":" + value)
    producer.send(record)
    Thread.sleep(5000)
  }

  producer.close()

}