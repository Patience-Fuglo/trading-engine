import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.event_bus import EventBus
from src.order import Order
from src.order_book import OrderBook
from src.position_manager import PositionManager
from src.risk_manager import RiskManager
from src.execution_engine import ExecutionEngine


def event_listener(event):
    print(f"Event: {event.event_type} | Data: {event.data}")


event_bus = EventBus()
event_bus.subscribe("OrderSubmitted", event_listener)
event_bus.subscribe("OrderFilled", event_listener)
event_bus.subscribe("OrderCancelled", event_listener)

order_book = OrderBook()
position_manager = PositionManager()
risk_manager = RiskManager(
    max_position_size=1000,
    max_total_exposure=100000,
    max_daily_loss=5000
)

engine = ExecutionEngine(order_book, position_manager, risk_manager, event_bus)

# Submit SELL LIMIT 100 AAPL at 150
sell_order = Order("SELL001", "AAPL", "SELL", 100, 150, "LIMIT")
engine.submit_order(sell_order)

# Submit BUY LIMIT 50 AAPL at 150
buy_order = Order("BUY001", "AAPL", "BUY", 50, 150, "LIMIT")
engine.submit_order(buy_order)

print("\nFinal Order Status:")
print("Sell Order:", sell_order.status, "| Remaining Qty:", sell_order.quantity)
print("Buy Order:", buy_order.status, "| Remaining Qty:", buy_order.quantity)

print("\nOrder Book:")
order_book.print_book()

print("\nPosition:")
position = position_manager.get_position("AAPL")
print(position)