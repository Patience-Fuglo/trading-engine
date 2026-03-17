import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
	sys.path.insert(0, str(BASE_DIR))

from trading_engine.position_manager import PositionManager

pm = PositionManager()

# Buy 100 AAPL at 150
pm.update_position("AAPL", 100, 150)

# Buy 50 more AAPL at 155
pm.update_position("AAPL", 50, 155)

position = pm.get_position("AAPL")
print("After buys:")
print(position)

# Sell 75 AAPL at 160
pm.update_position("AAPL", -75, 160)

position = pm.get_position("AAPL")
print("\nAfter sell:")
print(position)

current_price = 160
print("\nUnrealized PnL:", round(position.unrealized_pnl(current_price), 2))
print("Total PnL:", round(pm.get_total_pnl({"AAPL": 160}), 2))