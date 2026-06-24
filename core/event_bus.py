from typing import Dict, List, Callable, Any

class EventBus:

    def __init__(self):
        self.subcribers: Dict[str, List[Callable]] = {}
