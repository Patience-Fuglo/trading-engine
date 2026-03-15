import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.order import Order
from src.position_manager import PositionManager
from src.risk_manager import RiskManager


pm = PositionManager()
rm = RiskManager(
    max_position_size=1000,
    max_total_exposure=100000,
    max_daily_loss=5000
)

current_prices = {"AAPL": 150.0}
daily_pnl = 0

# Test A: buy 500 shares -> should pass
order1 = Order("ORD001", "AAPL", "BUY", 500, 150.0, "LIMIT")
result1 = rm.check_order(order1, pm, current_prices, daily_pnl)
print("Test A:", result1)

# Test B: buy 1500 shares -> should fail position limit
order2 = Order("ORD002", "AAPL", "BUY", 1500, 150.0, "LIMIT")
result2 = rm.check_order(order2, pm, current_prices, daily_pnl)
print("Test B:", result2)

# Test C: daily pnl = -6000 -> should fail daily loss limit
order3 = Order("ORD003", "AAPL", "