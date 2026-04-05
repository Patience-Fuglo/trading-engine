"""
Event-Driven Trading Engine

A modular quantitative trading system demonstrating:
- Event-driven architecture
- Order book mechanics  
- Risk management
- Position tracking
- Strategy backtesting
"""

from trading_engine.events import (
    Event,
    MarketDataEvent,
    OrderSubmittedEvent,
    OrderFilledEvent,
    OrderCancelledEvent,
)
from trading_engine.event_bus import EventBus
from trading_engine.order import Order
from trading_engine.order_book import OrderBook
from trading_engine.position import Position
from trading_engine.position_manager import PositionManager
from trading_engine.risk_manager import RiskManager
from trading_engine.execution_engine import ExecutionEngine
from trading_engine.market_data import MarketDataFeed
from trading_engine.strategy import Strategy, MovingAverageCrossover
from trading_engine.backtester import Backtester
from trading_engine.dashboard import Dashboard

__version__ = "0.1.0"

__all__ = [
    "Event",
    "MarketDataEvent",
    "OrderSubmittedEvent",
    "OrderFilledEvent",
    "OrderCancelledEvent",
    "EventBus",
    "Order",
    "OrderBook",
    "Position",
    "PositionManager",
    "RiskManager",
    "ExecutionEngine",
    "MarketDataFeed",
    "Strategy",
    "MovingAverageCrossover",
    "Backtester",
    "Dashboard",
]
