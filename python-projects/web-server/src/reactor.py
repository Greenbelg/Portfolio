import queue
import threading


class Reactor:
    def __init__(self):
        self._event_queue = queue.Queue()
        self._handlers = {}

    def register_handler(self, event_type, handler):
        if event_type not in self._handlers:
            self._handlers[event_type] = handler
        else:
            raise ValueError(
                f"Handler for {event_type} is already registered")

    def remove_handler(self, event_type):
        if event_type in self._handlers:
            del self._handlers[event_type]

    def add_event(self, event_type, event_data):
        self._event_queue.put((event_type, event_data))

    def start(self, num_threads=5):
        for _ in range(num_threads):
            worker = threading.Thread(target=self._handle_events)
            worker.daemon = True
            worker.start()

    def _handle_events(self):
        while True:
            event_type, event_data = self._event_queue.get()
            if event_type in self._handlers:
                handler = self._handlers[event_type]
                handler(event_data)