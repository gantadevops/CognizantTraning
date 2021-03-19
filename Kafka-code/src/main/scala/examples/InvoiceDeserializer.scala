
package examples

import org.apache.kafka.common.serialization.Deserializer
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.scala.{DefaultScalaModule, ScalaObjectMapper}

class InvoiceDeserializer extends  Deserializer[Invoice] {
  val objectMapper = new ObjectMapper() with ScalaObjectMapper
  objectMapper.registerModule(DefaultScalaModule)

  // convert bytes to  Invoice object
  // when consumer calls poll method, this method is invoked automatically

  override def deserialize(topic: String, bytes: Array[Byte]): Invoice = {

    val invoice: Invoice = objectMapper.readValue[Invoice] (bytes)
    invoice // return the object to consumer
  }
}