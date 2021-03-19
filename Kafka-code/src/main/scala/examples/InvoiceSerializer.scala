package examples

import org.apache.kafka.common.serialization.Serializer
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.scala.DefaultScalaModule
import java.io.StringWriter
import java.nio.charset.StandardCharsets

class InvoiceSerializer[T] extends  Serializer[T] {
  val objectMapper = new ObjectMapper()
  objectMapper.registerModule(DefaultScalaModule)

  // this code shall convert Invoice object data into bytes
  // serialize function called automatically by producer during producer.send
  override def serialize(topic: String, invoice: T): Array[Byte] = {
    println("Serialize called")

    val bytes: Array[Byte] = objectMapper.writeValueAsBytes(invoice)
    //println(bytes)
    println()
    for (k <- bytes) print(k + " ")
    println()
    //    val out = new StringWriter()
    //    objectMapper.writeValue(out, invoice)
    //    val json = out.toString()
    //    println(json)

    println("Serialized content " + new String(bytes, StandardCharsets.UTF_8))
    bytes //return bytes, this will send to kafka
  }
}