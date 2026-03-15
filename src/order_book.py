class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.side == "BUY":
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda x: x.price, reverse=True)

        elif order.side == "SELL":
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda x: x.price)

    def get_best_bid(self):
        if self.buy_orders:
            return self.buy_orders[0].price
        return None

    def get_best_ask(self):
        if self.sell_orders:
            return self.sell_orders[0].price
        return None

    def get_spread(self):
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()

        if best_bid is None or best_ask is None:
            return None

        return best_ask - best_bid

    def remove_order(self, order_id):
        for order in self.buy_orders:
            if order.order_id == order_id:
                self.buy_orders.remove(order)
                return

        for order in self.sell_orders:
            if order.order_id == order_id:
                self.sell_orders.remove(order)
                return

    def print_book(self):
        print("\nBUY ORDERS:")
        for order in self.buy_orders:
            print(order)

        print("\nSELL ORDERS:")
        for order in self.sell_orders:
            print(order)