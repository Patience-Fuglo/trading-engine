import json
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.event_bus import EventBus
from src.events import Event

def event_listener(event):
    print(f"Received event: {event.event_type}")
    print(f'Timestamp: {event.timestamp}')
    print(f'Data: {event.data}')
    print('--' * 40)


#Create a event Bus
bus = EventBus()

#Load event types from JSON file
with open(BASE_DIR / 'reference.json', 'r') as file:
    config = json.load(file)

#subcribe the listener to all event type in theJSON file
for event_info in config['event_types']:
    event_name = event_info['name']
    bus.subscribe(event_name, event_listener)

#Publish one sample event for each type in the JSON file
for event_info in config['event_types']:
    event_name = event_info['name']
    fields = event_info['fields']

# Create fake sample data from the fields list
    sample_data = {}
    for field in fields:
        sample_data[field] = f'sample_{field}'

# Create a generic Event using the JSON event name
    event = Event(event_name, sample_data)
    bus.publish(event)
    