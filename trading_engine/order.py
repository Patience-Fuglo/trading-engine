from datetime import datetime


class Order:
    def __init__(
        self,
        order_id,
        symbol,
        side,
        quantity,
        price,
        order_type,
        timestamp=None,
        status="PENDING"
    ):
        self.order_id = order_id
        self.symbol = symbol
        self.side = side
        self.quantity = int(quantity)
        self.price = float(price)
        self.order_type = order_type
        self.timestamp = timestamp if timestamp else datetime.now()
        self.status = status

    def __repr__(self):
        return (
            f"Order(order_id={self.order_id}, symbol={self.symbol}, "
            f"side={self.side}, quantity={self.quantity}, price={self.price}, "
            f"order_type={self.order_type}, status={self.status})"
        )