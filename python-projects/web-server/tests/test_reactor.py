import unittest
import threading
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from src.reactor import Reactor

class ReactorTestCase(unittest.TestCase):
    def test_register_handler(self):
        reactor = Reactor()
        event_type = "example_event"
        handler_func = lambda x: print(x)
        reactor.register_handler(event_type, handler_func)
        self.assertEqual(reactor._handlers[event_type], handler_func)

    def test_register_handler_which_registered(self):
        reactor = Reactor()
        event_type = "example_event"
        handler_func1 = lambda x: print(x)
        handler_func2 = lambda x: print(x)
        reactor.register_handler(event_type, handler_func1)
        with self.assertRaises(ValueError):
            reactor.register_handler(event_type, handler_func2)

    def test_remove_handler(self):
        reactor = Reactor()
        event_type = "example_event"
        handler_func = lambda x: print(x)
        reactor._handlers[event_type] = handler_func
        reactor.remove_handler(event_type)
        self.assertNotIn(event_type, reactor._handlers)

    def test_add_event(self):
        reactor = Reactor()
        event_type = "example_event"
        event_data = {"key": "value"}
        reactor.add_event(event_type, event_data)
        queued_event = reactor._event_queue.get()
        self.assertEqual(queued_event, (event_type, event_data))

    def test_start(self):
        reactor = Reactor()
        num_threads = 3
        reactor.start(num_threads)
        self.assertEqual(threading.active_count(), num_threads + 1)


if __name__ == '__main__':
    unittest.main()
