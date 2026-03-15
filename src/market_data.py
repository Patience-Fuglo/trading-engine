import csv
import time
from src.events import MarketDataEvent


class MarketDataFeed:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.latest_prices = {}
        self.price_history = {}
        self.data = []

    def load_csv(self, filepath):
        self.data = []

        with open(filepath, "r") as file:
            reader = csv.DictReader(file)

            for i, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                try:
                    parsed_row = {
                        "symbol": row["symbol"],
                        "timestamp": row["timestamp"],
                        "open": float(row["open"]),
                        "high": float(row["high"]),
                        "low": float(row["low"]),
                        "close": float(row["close"]),
                        "volume": int(row["volume"])
                    }
                    self.data.append(parsed_row)

                except (ValueError, KeyError, TypeError):
                    print(f"Skipping invalid row {i}")
                    continue

    def simulate_feed(self):
        for row in self.data:
            event = MarketDataEvent(row)
            self.event_bus.publish(event)

            symbol = row["symbol"]
            close_price = row["close"]

            self.latest_prices[symbol] = close_price

            if symbol not in self.price_history:
                self.price_history[symbol] = []

            self.price_history[symbol].append(close_price)

            time.sleep(0.1)

    def get_latest_price(self, symbol):
        return self.latest_prices.get(symbol, None)

    def get_price_history(self, symbol, n_periods=10):
        if symbol not in self.price_history:
            return []
        return self.price_history[symbol][-n_periods:]