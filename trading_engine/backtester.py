class Backtester:
    def __init__(self, strategy, starting_cash=100000, fee_per_trade=0.001):
        self.strategy = strategy
        self.starting_cash = starting_cash
        self.cash = starting_cash
        self.fee_per_trade = fee_per_trade
        self.position_quantity = 0
        self.portfolio_values = []
        self.trade_count = 0
        self.total_fees_paid = 0.0
        self.ending_value = starting_cash
        self.total_return = 0.0
        self.max_drawdown = 0.0

    def run(self, price_data):
        for symbol, price, timestamp in price_data:
            order = self.strategy.on_market_data(symbol, price, timestamp)

            if order is not None:
                trade_value = price * order.quantity
                fee = trade_value * self.fee_per_trade

                if order.side == "BUY":
                    total_cost = trade_value + fee
                    if self.cash >= total_cost:
                        self.cash -= total_cost
                        self.position_quantity += order.quantity
                        self.trade_count += 1
                        self.total_fees_paid += fee

                elif order.side == "SELL":
                    if self.position_quantity >= order.quantity:
                        proceeds = trade_value - fee
                        self.cash += proceeds
                        self.position_quantity -= order.quantity
                        self.trade_count += 1
                        self.total_fees_paid += fee

            portfolio_value = self.cash + (self.position_quantity * price)
            self.portfolio_values.append((timestamp, portfolio_value))

        if self.portfolio_values:
            self.ending_value = self.portfolio_values[-1][1]
            self.total_return = (self.ending_value / self.starting_cash) - 1
            self.max_drawdown = self.calculate_max_drawdown()

    def calculate_max_drawdown(self):
        peak = float("-inf")
        max_drawdown = 0.0

        for _, value in self.portfolio_values:
            if value > peak:
                peak = value

            drawdown = (peak - value) / peak if peak > 0 else 0.0
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return max_drawdown

    def print_report(self):
        print("Backtest Report")
        print("-" * 30)
        print(f"Starting Cash: ${self.starting_cash:,.2f}")
        print(f"Ending Value: ${self.ending_value:,.2f}")
        print(f"Total Return: {self.total_return * 100:.2f}%")
        print(f"Number of Trades: {self.trade_count}")
        print(f"Total Fees Paid: ${self.total_fees_paid:,.2f}")
        print(f"Max Drawdown: {self.max_drawdown * 100:.2f}%")