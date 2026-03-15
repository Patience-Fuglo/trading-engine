class Position:
    def __init__(self, symbol):
        self.symbol = symbol
        self.quantity = 0
        self.average_entry_price = 0.0
        self.realized_pnl = 0.0

    def update(self, fill_quantity, fill_price):
        # BUY
        if fill_quantity > 0:
            total_cost = (self.quantity * self.average_entry_price) + (fill_quantity * fill_price)
            self.quantity += fill_quantity
            self.average_entry_price = total_cost / self.quantity

        # SELL
        elif fill_quantity < 0:
            shares_sold = abs(fill_quantity)
            profit = (fill_price - self.average_entry_price) * shares_sold
            self.realized_pnl += profit
            self.quantity += fill_quantity

    def unrealized_pnl(self, current_price):
        return (current_price - self.average_entry_price) * self.quantity

    def market_value(self, current_price):
        return abs(self.quantity) * current_price

    def __repr__(self):
        return (
            f"Position(symbol={self.symbol}, quantity={self.quantity}, "
            f"average_entry_price={self.average_entry_price:.2f}, "
            f"realized_pnl={self.realized_pnl:.2f})"
        )