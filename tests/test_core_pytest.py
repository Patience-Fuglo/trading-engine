from trading_engine.event_bus import EventBus
from trading_engine.events import Event
from trading_engine.order import Order
from trading_engine.order_book import OrderBook
from trading_engine.position_manager import PositionManager
from trading_engine.risk_manager import RiskManager
from trading_engine.backtester import Backtester
from trading_engine.strategy import MovingAverageCrossover


def test_event_bus_publish_calls_subscriber():
    bus = EventBus()
    received = []

    def listener(evt):
        received.append(evt.event_type)

    bus.subscribe("Ping", listener)
    bus.publish(Event("Ping", {"ok": True}))

    assert received == ["Ping"]


def test_order_book_best_bid_ask_and_spread():
    book = OrderBook()
    book.add_order(Order("B1", "AAPL", "BUY", 10, 100.0, "LIMIT"))
    book.add_order(Order("B2", "AAPL", "BUY", 10, 101.0, "LIMIT"))
    book.add_order(Order("S1", "AAPL", "SELL", 10, 103.0, "LIMIT"))

    assert book.get_best_bid() == 101.0
    assert book.get_best_ask() == 103.0
    assert book.get_spread() == 2.0


def test_position_manager_total_pnl_positive_after_price_rise():
    pm = PositionManager()
    pm.update_position("AAPL", 10, 100.0)

    assert round(pm.get_total_pnl({"AAPL": 105.0}), 2) == 50.0


def test_risk_manager_rejects_position_limit():
    rm = RiskManager(max_position_size=100, max_total_exposure=1_000_000, max_daily_loss=5_000)
    pm = PositionManager()
    order = Order("R1", "AAPL", "BUY", 150, 100.0, "LIMIT")

    approved, reason = rm.check_order(order, pm, {"AAPL": 100.0}, daily_pnl=0)

    assert approved is False
    assert reason == "Position limit exceeded"


def test_backtester_runs_and_produces_metrics():
    strategy = MovingAverageCrossover(short_window=2, long_window=3)
    bt = Backtester(strategy, starting_cash=10_000, fee_per_trade=0.0)

    price_data = [
        ("AAPL", 100.0, "2024-01-01 09:30:00"),
        ("AAPL", 101.0, "2024-01-01 09:31:00"),
        ("AAPL", 102.0, "2024-01-01 09:32:00"),
        ("AAPL", 99.0, "2024-01-01 09:33:00"),
        ("AAPL", 98.0, "2024-01-01 09:34:00"),
        ("AAPL", 103.0, "2024-01-01 09:35:00"),
    ]

    bt.run(price_data)

    assert len(bt.portfolio_values) == len(price_data)
    assert bt.ending_value > 0
    assert -1.0 <= bt.total_return <= 10.0
    assert 0.0 <= bt.max_drawdown <= 1.0
