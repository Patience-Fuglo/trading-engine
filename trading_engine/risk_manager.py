from datetime import datetime


class RiskManager:
    def __init__(self, max_position_size, max_total_exposure, max_daily_loss):
        self.max_position_size = max_position_size
        self.max_total_exposure = max_total_exposure
        self.max_daily_loss = max_daily_loss
        self.log = []

    def check_position_limit(self, current_quantity, order_quantity, max_size):
        new_position = current_quantity + order_quantity
        return abs(new_position) <= max_size

    def check_exposure_limit(self, positions, current_prices):
        total_exposure = 0.0

        for symbol, position in positions.items():
            current_price = current_prices.get(symbol, 0)
            total_exposure += abs(position.quantity) * current_price

        return total_exposure <= self.max_total_exposure

    def check_daily_loss(self, current_daily_pnl):
        return current_daily_pnl >= -self.max_daily_loss

    def check_order(self, order, position_manager, current_prices, daily_pnl):
        position = position_manager.get_position(order.symbol)

        current_quantity = 0
        if position is not None:
            current_quantity = position.quantity

        order_quantity = order.quantity if order.side == "BUY" else -order.quantity

        if not self.check_position_limit(current_quantity, order_quantity, self.max_position_size):
            self.log.append({
                "timestamp": datetime.now(),
                "order_id": order.order_id,
                "approved": False,
                "reason": "Position limit exceeded"
            })
            return (False, "Position limit exceeded")

        if not self.check_exposure_limit(position_manager.positions, current_prices):
            self.log.append({
                "timestamp": datetime.now(),
                "order_id": order.order_id,
                "approved": False,
                "reason": "Exposure limit exceeded"
            })
            return (False, "Exposure limit exceeded")

        if not self.check_daily_loss(daily_pnl):
            self.log.append({
                "timestamp": datetime.now(),
                "order_id": order.order_id,
                "approved": False,
                "reason": "Daily loss limit exceeded"
            })
            return (False, "Daily loss limit exceeded")

        self.log.append({
            "timestamp": datetime.now(),
            "order_id": order.order_id,
            "approved": True,
            "reason": None
        })
        return (True, None)