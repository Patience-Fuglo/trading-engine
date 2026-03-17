from datetime import datetime

class Event:
	def __init__(self, event_type, data=None):
		self.event_type = event_type
		self.timestamp = datetime.now()
		self.data = data or {}

	def __repr__(self):
		return f'Event(type={self.event_type}, time={self.timestamp}, data={self.data})'
	

class MarketDataEvent(Event):
	def __init__(self, data):
		super().__init__("MarketDataUpdate", data)

class OrderSubmittedEvent(Event):
	def __init__(self, data):
		super().__init__('OrderSubmitted', data)

class OrderFilledEvent(Event):
	def __init__(self, data):
		super().__init__('OrderFilled', data)

class OrderCancelledEvent(Event):
	def __init__(self, data):
		super().__init__('OrderCancelled', data)