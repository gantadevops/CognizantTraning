package assignment

case class order(val order_id: Integer,
                 val item_id: String,
                 val price: Integer,
                 val qty: Integer,
                 val state: String)
