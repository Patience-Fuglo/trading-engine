from src.events import OrderSubmittedEvent, OrderFilledEvent, OrderCancelledEvent


class ExecutionEngine:
    def __init__(self, order_book, position_manager, risk_manager, event_bus):
        self.order_book = order_book
        self.position_manager = position_manager
        self.risk_manager = risk_manager
        self.event_bus = event_bus

    def submit_order(self, order):
        current_prices = {order.symbol: order.price}
        daily_pnl = 0

        approved, reason = self.risk_manager.check_order(
            order,
            self.position_manager,
            current_prices,
            daily_pnl
        )

        if not approved:
            order.status = "REJECTED"
            self.event_bus.publish(OrderCancelledEvent({
                "order_id": order.order_id,
                "reason": reason,
                "timestamp": str(order.timestamp)
            }))
            return

        # MARKET order
        if order.order_type == "MARKET":
            opposite_orders = (
                self.order_book.sell_orders if order.side == "BUY"
                else self.order_book.buy_orders
            )

            symbol_orders = [o for o in opposite_orders if o.symbol == order.symbol]

            if not symbol_orders:
                order.status = "REJECTED"
                self.event_bus.publish(OrderCancelledEvent({
                    "order_id": order.order_id,
                    "reason": "No liquidity for market order",
                    "timestamp": str(order.timestamp)
                }))
                return

            order.status = "ACTIVE"
            self.event_bus.publish(OrderSubmittedEvent({
                "order_id": order.order_id,
                "symbol": order.symbol,
                "side": order.side,
                "quantity": order.quantity,
                "price": order.price,
                "order_type": order.order_type,
                "timestamp": str(order.timestamp)
            }))

            self.match_market_order(order)
            return

        # LIMIT order
        order.status = "ACTIVE"
        self.order_book.add_order(order)

        self.event_bus.publish(OrderSubmittedEvent({
            "order_id": order.order_id,
            "symbol": order.symbol,
            "side": order.side,
            "quantity": order.quantity,
            "price": order.price,
            "order_type": order.order_type,
            "timestamp": str(order.timestamp)
        }))

        self.match_orders(order.symbol)

    def match_orders(self, symbol):
        while True:
            buy_orders = [o for o in self.order_book.buy_orders if o.symbol == symbol]
            sell_orders = [o for o in self.order_book.sell_orders if o.symbol == symbol]

            if not buy_orders or not sell_orders:
                break

            buy_order = buy_orders[0]
            sell_order = sell_orders[0]

            best_bid_price = buy_order.price
            best_ask_price = sell_order.price

            if best_bid_price < best_ask_price:
                break

            fill_price = best_ask_price
            fill_quantity = min(buy_order.quantity, sell_order.quantity)

            buy_order.quantity -= fill_quantity
            sell_order.quantity -= fill_quantity

            self.position_manager.update_position(symbol, fill_quantity, fill_price)
            self.position_manager.update_position(symbol, -fill_quantity, fill_price)

            self.event_bus.publish(OrderFilledEvent({
                "buyer_order_id": buy_order.order_id,
                "seller_order_id": sell_order.order_id,
                "fill_price": fill_price,
                "fill_quantity": fill_quantity,
                "timestamp": str(buy_order.timestamp)
            }))

            if buy_order.quantity == 0:
                buy_order.status = "FILLED"
                self.order_book.remove_order(buy_order.order_id)
            else:
                buy_order.status = "PARTIALLY_FILLED"

            if sell_order.quantity == 0:
                sell_order.status = "FILLED"
                self.order_book.remove_order(sell_order.order_id)
            else:
                sell_order.status = "PARTIALLY_FILLED"

    def match_market_order(self, market_order):
        if market_order.side == "BUY":
            opposite_orders = [o for o in self.order_book.sell_orders if o.symbol == market_order.symbol]
            if not opposite_orders:
                return

            sell_order = opposite_orders[0]
            fill_price = sell_order.price
            fill_quantity = min(market_order.quantity, sell_order.quantity)

            market_order.quantity -= fill_quantity
            sell_order.quantity -= fill_quantity

            self.position_manager.update_position(market_order.symbol, fill_quantity, fill_price)
            self.position_manager.update_position(market_order.symbol, -fill_quantity, fill_price)

            self.event_bus.publish(OrderFilledEvent({
                "buyer_order_id": market_order.order_id,
                "seller_order_id": sell_order.order_id,
                "fill_price": fill_price,
                "fill_quantity": fill_quantity,
                "timestamp": str(market_order.timestamp)
            }))

            if market_order.quantity == 0:
                market_order.status = "FILLED"
            else:
                market_order.status = "PARTIALLY_FILLED"

            if sell_order.quantity == 0:
                sell_order.status = "FILLED"
                self.order_book.remove_order(sell_order.order_id)
            else:
                sell_order.status = "PARTIALLY_FILLED"

        elif market_order.side == "SELL":
            opposite_orders = [o for o in self.order_book.buy_orders if o.symbol == market_order.symbol]
            if not opposite_orders:
                return

            buy_order = opposite_orders[0]
            fill_price = buy_order.price
            fill_quantity = min(market_order.quantity, buy_order.quantity)

            market_order.quantity -= fill_quantity
            buy_order.quantity -= fill_quantity

            self.position_manager.update_position(market_order.symbol, -fill_quantity, fill_price)
            self.position_manager.update_position(market_order.symbol, fill_quantity, fill_price)

            self.event_bus.publish(OrderFilledEvent({
                "buyer_order_id": buy_order.order_id,
                "seller_order_id": market_order.order_id,
                "fill_price": fill_price,
                "fill_quantity": fill_quantity,
                "timestamp": str(market_order.timestamp)
            }))

            if market_order.quantity == 0:
                market_order.status = "FILLED"
            else:
                market_order.status = "PARTIALLY_FILLED"

            if buy_order.quantity == 0:
                buy_order.status = "FILLED"
                self.order_book.remove_order(buy_order.order_id)
            else:
                buy_order.status = "PARTIALLY_FILLED"