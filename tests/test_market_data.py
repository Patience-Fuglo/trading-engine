import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from trading_engine.event_bus import EventBus
from trading_engine.market_data import MarketDataFeed


def print_market_event(event):
    print(f"Market Event: {event.event_type} | Data: {event.data}")


event_bus = EventBus()
event_bus.subscribe("MarketDataUpdate", print_market_event)

feed = MarketDataFeed(event_bus)
feed.load_csv(BASE_DIR / "data" / "sample_prices.csv")

feed.simulate_feed()

print("\nLatest Prices:")
print(feed.latest_prices)

print("\nLast 5 AAPL Prices:")
print(feed.get_price_history("AAPL", 5))