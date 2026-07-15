from typing import Dict, List, Callable, Any

class EventBus:

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.state = {"is_speaking": False}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type: str, event_data: Any = None):
        if event_type in self.subscribers:
            for func in self.subscribers[event_type]:
                func(event_data)