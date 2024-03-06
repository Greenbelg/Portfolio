import unittest
import socket
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import src.config as config
from server import EventHandler, HTTPServer


class EventHandlerTestCase(unittest.TestCase):
    def test_event_handler(self):
        client_sock = MagicMock()
        cid = 1
        event_data = (client_sock, cid)
        with patch('src.server.BaseRequestHandler', autospec=True) as mock_base_request_handler:
            event_handler = EventHandler()
            event_handler(event_data)
            mock_base_request_handler.assert_called_once_with(client_sock, cid)
            mock_base_request_handler.return_value.assert_called_once_with(None)


class HTTPServerTestCase(unittest.TestCase):
    def setUp(self):
        self.server = HTTPServer()

    def test_create_serv_sock(self):
        with patch('socket.socket') as mock_socket:
            with patch('socket.socket.bind'):
                with patch('socket.socket.listen'):
                    serv_socks = self.server.create_serv_sock()
                    self.assertEqual(len(serv_socks), len(config.PORTS))
                    for serv_sock in serv_socks:
                        self.assertIsInstance(serv_sock, MagicMock)
                        mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM, proto=0)


if __name__ == '__main__':
    unittest.main()
