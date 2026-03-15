class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    # Backward-compatible alias for older misspelled calls
    def subcribe(self, event_type, callback):
        self.subscribe(event_type, callback)

    def publish(self, event):
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                callback(event)

                