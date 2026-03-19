try:
    from rich.table import Table
    from rich.console import Console
except ModuleNotFoundError:
    class Table:
        def __init__(self, title=""):
            self.title = title
            self.columns = []
            self.rows = []

        def add_column(self, name):
            self.columns.append(name)

        def add_row(self, *values):
            self.rows.append(values)

        def __str__(self):
            lines = []
            if self.title:
                lines.append(self.title)
            if self.columns:
                lines.append(" | ".join(self.columns))
                lines.append("-" * max(10, len(" | ".join(self.columns))))
            for row in self.rows:
                lines.append(" | ".join(str(v) for v in row))
            return "\n".join(lines)

    class Console:
        def print(self, value=""):
            print(value)

        def clear(self):
            print("\n" * 2)

from datetime import datetime

console = Console()


class Dashboard:
    def __init__(self, position_manager, execution_engine, risk_manager):
        self.position_manager = position_manager
        self.execution_engine = execution_engine
        self.risk_manager = risk_manager

    def display_positions(self, current_prices):
        table = Table(title="Positions")

        table.add_column("Symbol")
        table.add_column("Quantity")
        table.add_column("Avg Price")
        table.add_column("Current Price")
        table.add_column("Unrealized P&L")
        table.add_column("Realized P&L")

        for symbol, position in self.position_manager.positions.items():
            current_price = current_prices.get(symbol, 0.0)
            unrealized = position.unrealized_pnl(current_price)
            realized = position.realized_pnl

            unrealized_text = f"{unrealized:.2f}"
            realized_text = f"{realized:.2f}"

            unrealized_style = "green" if unrealized >= 0 else "red"
            realized_style = "green" if realized >= 0 else "red"

            table.add_row(
                symbol,
                str(position.quantity),
                f"{position.average_entry_price:.2f}",
                f"{current_price:.2f}",
                f"[{unrealized_style}]{unrealized_text}[/{unrealized_style}]",
                f"[{realized_style}]{realized_text}[/{realized_style}]"
            )

        console.print(table)

    def display_recent_orders(self, orders, limit=10):
        table = Table(title="Recent Orders")

        table.add_column("Order ID")
        table.add_column("Symbol")
        table.add_column("Side")
        table.add_column("Qty")
        table.add_column("Price")
        table.add_column("Status")

        recent_orders = orders[-limit:]

        for order in recent_orders:
            side_style = "green" if order.side == "BUY" else "red"

            table.add_row(
                order.order_id,
                order.symbol,
                f"[{side_style}]{order.side}[/{side_style}]",
                str(order.quantity),
                f"{order.price:.2f}",
                order.status
            )

        console.print(table)

    def display_pnl_summary(self, current_prices):
        total_realized = 0.0
        total_unrealized = 0.0

        for symbol, position in self.position_manager.positions.items():
            current_price = current_prices.get(symbol, 0.0)
            total_realized += position.realized_pnl
            total_unrealized += position.unrealized_pnl(current_price)

        net_pnl = total_realized + total_unrealized

        realized_style = "green" if total_realized >= 0 else "red"
        unrealized_style = "green" if total_unrealized >= 0 else "red"
        net_style = "green" if net_pnl >= 0 else "red"

        console.print(f"Total Realized P&L: [{realized_style}]{total_realized:.2f}[/{realized_style}]")
        console.print(f"Total Unrealized P&L: [{unrealized_style}]{total_unrealized:.2f}[/{unrealized_style}]")
        console.print(f"Net P&L: [{net_style}]{net_pnl:.2f}[/{net_style}]")

    def _usage_style(self, ratio):
        if ratio >= 0.9:
            return "red"
        elif ratio >= 0.75:
            return "yellow"
        return "green"

    def _bar(self, ratio, width=20):
        ratio = max(0.0, min(ratio, 1.0))
        filled = int(ratio * width)
        empty = width - filled
        return "█" * filled + "-" * empty

    def display_risk_status(self, daily_pnl, current_prices):
        largest_position = 0
        total_exposure = 0.0

        for symbol, position in self.position_manager.positions.items():
            largest_position = max(largest_position, abs(position.quantity))
            current_price = current_prices.get(symbol, 0.0)
            total_exposure += abs(position.quantity) * current_price

        position_ratio = (
            largest_position / self.risk_manager.max_position_size
            if self.risk_manager.max_position_size > 0 else 0
        )

        exposure_ratio = (
            total_exposure / self.risk_manager.max_total_exposure
            if self.risk_manager.max_total_exposure > 0 else 0
        )

        daily_loss_used = max(0.0, -daily_pnl)
        daily_loss_ratio = (
            daily_loss_used / self.risk_manager.max_daily_loss
            if self.risk_manager.max_daily_loss > 0 else 0
        )

        position_style = self._usage_style(position_ratio)
        exposure_style = self._usage_style(exposure_ratio)
        loss_style = self._usage_style(daily_loss_ratio)

        console.print("\nRisk Status")
        console.print(
            f"Position Usage : [{position_style}]{self._bar(position_ratio)} {position_ratio * 100:.1f}%[/{position_style}]"
        )
        console.print(
            f"Exposure Usage : [{exposure_style}]{self._bar(exposure_ratio)} {exposure_ratio * 100:.1f}%[/{exposure_style}]"
        )
        console.print(
            f"Daily Loss Use : [{loss_style}]{self._bar(daily_loss_ratio)} {daily_loss_ratio * 100:.1f}%[/{loss_style}]"
        )

    def refresh(self, current_prices, orders, daily_pnl):
        console.clear()
        console.print(f"[bold cyan]Trading Engine Dashboard[/bold cyan] - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.display_positions(current_prices)
        self.display_recent_orders(orders)
        self.display_pnl_summary(current_prices)
        self.display_risk_status(daily_pnl, current_prices)