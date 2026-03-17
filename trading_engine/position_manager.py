from src.position import Position


class PositionManager:
    def __init__(self):
        self.positions = {}

    def update_position(self, symbol, fill_quantity, fill_price):
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol)

        self.positions[symbol].update(fill_quantity, fill_price)

    def get_position(self, symbol):
        return self.positions.get(symbol, None)

    def get_total_pnl(self, current_prices):
        total_pnl = 0.0

        for symbol, position in self.positions.items():
            current_price = current_prices[symbol]
            total_pnl += position.realized_pnl + position.unrealized_pnl(current_price)

        return total_pnl