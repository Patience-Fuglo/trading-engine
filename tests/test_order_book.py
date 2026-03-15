import csv
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.order import Order
from src.order_book import OrderBook

book = OrderBook()

with open(BASE_DIR / "data" / "sample_orders.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        order = Order(
            order_id=row["order_id"],
            symbol=row["symbol"],
            side=row["side"],
            quantity=row["quantity"],
            price=row["price"],
            order_type=row["order_type"],
            timestamp=row["