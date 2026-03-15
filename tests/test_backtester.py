import csv
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.strategy import MovingAverageCrossover
from src.backtester import Backtester


price_data = []

with open(BASE_DIR / "data" / "sample_prices.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        symbol = row["symbol"]
        price = float(row["close"])
        timestamp = row["timestamp"]
        price_data.append((symbol, price, timestamp))


strategy = MovingAverageCrossover(short_window=2, long_window=4)
backtester = Backtester(strategy, starting_cash=100000, fee_per_trade=0.001)

backtester.run(price_data)
backtester.print_report()