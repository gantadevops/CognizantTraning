
package assignment

import org.apache.kafka.common.serialization.Deserializer
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.scala.{DefaultScalaModule, ScalaObjectMapper}


class orderDeserializer extends  Deserializer[ordergrouped] {
  val objectMapper = new ObjectMapper() with ScalaObjectMapper
  objectMapper.registerModule(DefaultScalaModule)

  // convert bytes to  Invoice object
  // when consumer calls poll method, this method is invoked automatically

  override def deserialize(topic: String, bytes: Array[Byte]): ordergrouped = {

    val order: ordergrouped = objectMapper.readValue[ordergrouped] (bytes)
    order// return the object to consumer
  }
}