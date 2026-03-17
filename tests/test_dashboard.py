import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from trading_engine.event_bus import EventBus
from trading_engine.order import Order
from trading_engine.order_book import OrderBook
from trading_engine.position_manager import PositionManager
from trading_engine.risk_manager import RiskManager
from trading_engine.execution_engine import ExecutionEngine
from trading_engine.dashboard import Dashboard

# Set up core components
event_bus = EventBus()
order_book = OrderBook()
position_manager = PositionManager()
risk_manager = RiskManager(
    max_position_size=1000,
    max_total_exposure=100000,
    max_daily_loss=5000
)
execution_engine = ExecutionEngine(order_book, position_manager, risk_manager, event_bus)

# Create some sample positions
position_manager.update_position("AAPL", 100, 150)
position_manager.update_position("MSFT", 50, 340)
position_manager.update_position("GOOGL", 30, 130)

# Sell some AAPL to create realized pnl
position_manager.update_position("AAPL", -20, 160)

# Current prices
current_prices = {
    "AAPL": 155.0,
    "MSFT": 350.0,
    "GOOGL": 135.0
}

# Sample orders
orders = [
    Order("ORD001", "AAPL", "BUY", 100, 150.0, "LIMIT"),
    Order("ORD002", "MSFT", "SELL", 50, 350.0, "LIMIT"),
    Order("ORD003", "GOOGL", "BUY", 30, 130.0, "MARKET"),
    Order("ORD004", "AAPL", "SELL", 20, 160.0, "LIMIT"),
]

orders[0].status = "FILLED"
orders[1].status = "PARTIALLY_FILLED"
orders[2].status = "ACTIVE"
orders[3].status = "FILLED"

daily_pnl = -1200

dashboard = Dashboard(position_manager, execution_engine, risk_manager)
dashboard.refresh(current_prices, orders, daily_pnl)