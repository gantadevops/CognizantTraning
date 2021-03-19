package examples

class Product(val name: String, val price:Double)  {
   // constructor
   println("new product created " + name )

   private var _discount = 0;
   // return _discount
   def getDiscount() = _discount
   def setDiscount(value: Int) = _discount = value

   def getTotal() = {
      val total = price - (price * _discount)/100.0

      total // return value, last executed value returned
   }
}

// App trait, java interface
// App trait already has main
object HelloWorld extends App {
   println("Hello World")
   val product = new Product("iPhone", 600)

   println("Discount " + product.getDiscount())
   product.setDiscount(20)

   println("Total is " + product.getTotal())
}