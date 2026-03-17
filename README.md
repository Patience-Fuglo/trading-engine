
# Event-Driven Trading Engine in Python

### Quantitative Trading System Architecture Project

![Python](https://img.shields.io/badge/python-3.x-blue)
![Architecture](https://img.shields.io/badge/architecture-event--driven-green)
![Project](https://img.shields.io/badge/status-complete-brightgreen)

---

# Overview

This project implements a **simplified event-driven trading engine from scratch** to demonstrate the core architecture used in many quantitative trading systems.

The goal of this project is **not strategy profitability**, but understanding **how trading infrastructure is designed and connected**.

The engine simulates the key components of a trading system:

* Market data feed
* Event-driven communication
* Order submission and execution
* Order book matching
* Risk management checks
* Position and P&L tracking
* Strategy backtesting
* Terminal monitoring dashboard

The design emphasizes **modularity**, allowing each component to operate independently while interacting through an event system.

This structure mirrors the architecture used in many **quantitative research and algorithmic trading platforms**.

---

# System Architecture

The system follows an **event-driven architecture** where each component communicates through events rather than direct coupling.

```
Market Data Feed
       ↓
     Event Bus
       ↓
     Strategy
       ↓
  Execution Engine
       ↓
    Order Book
       ↓
   Risk Manager
       ↓
 Position Manager
       ↓
 Dashboard / Backtester
```

Each module can be extended or replaced without changing the entire system.

---

# Features

* Event-driven trading system architecture
* Simulated order book with price priority matching
* Risk management guardrails
* Execution engine connecting all system components
* Position tracking with realized and unrealized P&L
* Historical strategy backtesting framework
* Terminal-based monitoring dashboard
* Modular design suitable for extension

---

# Project Modules

## 1. Event System

Provides communication between independent components.

Files:

```
events.py
event_bus.py
```

Core pattern:

```
publish(event)
subscribe(event)
```

Events allow different parts of the system to react to updates such as market data or order fills.

---

## 2. Order Book

Stores buy and sell orders waiting to be matched.

Files:

```
order.py
order_book.py
```

Order priority:

```
BUY orders  → highest price first
SELL orders → lowest price first
```

Matching occurs when:

```
best_bid >= best_ask
```

---

## 3. Position & PnL Tracking

Tracks portfolio holdings and profit/loss.

Files:

```
position.py
position_manager.py
```

Tracks:

* quantity
* average entry price
* realized P&L
* unrealized P&L

Portfolio value:

```
cash + position_quantity × current_price
```

---

## 4. Risk Manager

Applies safety checks before orders are executed.

File:

```
risk_manager.py
```

Risk controls implemented:

* Maximum position size
* Maximum portfolio exposure
* Maximum daily loss

Orders that fail these checks are rejected before execution.

---

## 5. Execution Engine

Central component that connects the system.

File:

```
execution_engine.py
```

Execution workflow:

```
Submit Order
      ↓
Risk Check
      ↓
Add to Order Book
      ↓
Match Orders
      ↓
Update Positions
      ↓
Publish Events
```

Order states include:

```
ACTIVE
PARTIALLY_FILLED
FILLED
REJECTED
```

---

## 6. Market Data Feed

Simulates a live data feed using historical CSV data.

File:

```
market_data.py
```

CSV format:

```
symbol,timestamp,open,high,low,close,volume
```

Data flow:

```
Load CSV
    ↓
Publish MarketDataEvent
    ↓
Update latest prices
    ↓
Store price history
```

---

## 7. Strategy & Backtester

Provides a framework for testing trading strategies on historical data.

Files:

```
strategy.py
backtester.py
```

Example strategy implemented:

```
Moving Average Crossover
```

Logic:

```
Short MA > Long MA → BUY
Short MA < Long MA → SELL
```

Backtester tracks:

* portfolio value
* number of trades
* total return
* transaction fees
* maximum drawdown

---

## 8. Monitoring Dashboard

Provides a terminal-based interface to monitor the system.

File:

```
dashboard.py
```

Built using the **Rich** library.

Displays:

* current positions
* recent orders
* realized and unrealized P&L
* risk exposure indicators

---

# Project Structure

```
trading_engine/
    events.py
    event_bus.py
    order.py
    order_book.py
    position.py
    position_manager.py
    risk_manager.py
    execution_engine.py
    market_data.py
    strategy.py
    backtester.py
    dashboard.py
    __init__.py

tests/
    test_event.py
    test_order_book.py
    test_position.py
    test_positions.py
    test_risk_manager.py
    test_execution_engine.py
    test_market_data.py
    test_backtester.py
    test_dashboard.py

data/
    sample_orders.csv
    sample_prices.csv

README.md
```


# Requirements

Python 3.9+

Required library:

pip install rich
---

# Running the Project

Install dependencies:

```
pip install rich
```

Run component tests:

```
python tests/test_event.py
python tests/test_order_book.py
python tests/test_position.py
python tests/test_risk_manager.py
python tests/test_execution_engine.py
python tests/test_market_data.py
python tests/test_backtester.py
python tests/test_dashboard.py
```

Each test demonstrates a different part of the trading system.

---

# Example Output

Running the backtester produces performance metrics:

```
Backtest Report
------------------------------
Starting Cash: $100,000.00
Ending Value: $102,450.75
Total Return: 2.45%
Number of Trades: 8
Total Fees Paid: $127.50
Max Drawdown: 3.20%
```

The dashboard displays real-time system state during backtesting or live execution, showing:

* Active positions and their P&L
* Recent order executions with fills
* Risk manager status and exposure metrics
* Event log of system activity

---

# Technologies

* Python
* Event-driven architecture
* CSV data feeds
* Rich (terminal UI library)

---

# Key Concepts Demonstrated

* Event-driven system design
* Order book mechanics
* Risk management frameworks
* Position accounting
* Strategy signal generation
* Historical backtesting
* Trading system monitoring

---

# How This Architecture Can Be Extended

Possible extensions include:

* multi-symbol strategy support
* asynchronous event processing
* database storage
* exchange API integration
* slippage and transaction cost modeling
* portfolio optimization
* real-time dashboards

---

# Disclaimer

This project is a **simplified educational implementation** of a trading engine designed to demonstrate quantitative trading system architecture.

It is **not intended for live trading without significant additional development and testing**.

---
