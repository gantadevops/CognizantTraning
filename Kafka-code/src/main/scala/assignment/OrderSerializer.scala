package assignment


import org.apache.kafka.common.serialization.Serializer
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.scala.DefaultScalaModule
import java.io.StringWriter
import java.nio.charset.StandardCharsets


class OrderSerializer [T] extends  Serializer[T] {
  val objectMapper = new ObjectMapper()
  objectMapper.registerModule(DefaultScalaModule)

  // this code shall convert Order object data into bytes
  // serialize function called automatically by producer during producer.send
  override def serialize(topic: String, ord: T): Array[Byte] = {

    val bytes: Array[Byte] = objectMapper.writeValueAsBytes(ord)
    //println(bytes)
    println()
    for (k <- bytes) print(k + " ")
    println()

    println("Serialized content " + new String(bytes, StandardCharsets.UTF_8))
    bytes //return bytes, this will send to kafka
  }
}


