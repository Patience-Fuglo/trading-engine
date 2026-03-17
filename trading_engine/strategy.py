from src.order import Order


class Strategy:
    def on_market_data(self, symbol, price, timestamp):
        return None


class MovingAverageCrossover(Strategy):
    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window
        self.prices = []
        self.previous_signal = None
        self.order_count = 0

    def on_market_data(self, symbol, price, timestamp):
        self.prices.append(price)

        if len(self.prices) < self.long_window:
            return None

        short_ma = sum(self.prices[-self.short_window:]) / self.short_window
        long_ma = sum(self.prices[-self.long_window:]) / self.long_window

        current_signal = None
        if short_ma > long_ma:
            current_signal = "BUY"
        elif short_ma < long_ma:
            current_signal = "SELL"

        if self.previous_signal is None:
            self.previous_signal = current_signal
            return None

        if current_signal == "BUY" and self.previous_signal != "BUY":
            self.previous_signal = current_signal
            self.order_count += 1
            return Order(
                order_id=f"BT_ORDER_{self.order_count}",
                symbol=symbol,
                side="BUY",
                quantity=10,
                price=price,
                order_type="MARKET",
                timestamp=timestamp
            )

        if current_signal == "SELL" and self.previous_signal != "SELL":
            self.previous_signal = current_signal
            self.order_count += 1
            return Order(
                order_id=f"BT_ORDER_{self.order_count}",
                symbol=symbol,
                side="SELL",
                quantity=10,
                price=price,
                order_type="MARKET",
                timestamp=timestamp
            )

        self.previous_signal = current_signal
        return None