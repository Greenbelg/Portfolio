import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from unittest.mock import MagicMock
from src.request_handler import BaseRequestHandler


class BaseRequestHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.client_sock_kate = MagicMock()
        self.client_sock_kate.getsockname.return_value = ('localhost', 12346)
        self.handler_kate = BaseRequestHandler(self.client_sock_kate, 1)

        self.client_sock_strange = MagicMock()
        self.client_sock_strange.getsockname.return_value = ('localhost', 12347)
        self.handler_strange = BaseRequestHandler(self.client_sock_strange, 1)

    def test_handle_request_valid_request(self):
        raw_request = b'GET /kotik.html HTTP/1.1\r\nHost: kate.com\r\n\r\n'
        response = self.handler_kate.handle_request(raw_request)
        self.assertTrue(self.handler_kate.request)
        self.assertFalse(self.handler_kate.request.is_bad_request)
        self.assertEqual(response[:15], b'HTTP/1.1 200 OK')

    def test_handle_request_bad_request(self):
        raw_request = b'Invalid Request'
        response = self.handler_kate.handle_request(raw_request)
        self.assertTrue(self.handler_kate.request)
        self.assertTrue(self.handler_kate.request.is_bad_request)
        self.assertEqual(response[:24], b'HTTP/1.1 400 Bad Request')

    def test_handle_request_not_found(self):
        raw_request = b'GET /ejik.html HTTP/1.1\r\nHost: kate.com\r\n\r\n'
        response = self.handler_kate.handle_request(raw_request)
        self.assertTrue(self.handler_kate.request)
        self.assertTrue(self.handler_kate.request.is_bad_request)
        self.assertEqual(response[:22], b'HTTP/1.1 404 Not Found')

    def test_write_response(self):
        response = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, World!'
        self.handler_kate.write_response(response)
        self.client_sock_kate.close.assert_called_once()

    def test_handle_request_valid_request_with_invalid_port(self):
        raw_request = b'GET /kotik.html HTTP/1.1\r\nHost: strange.com\r\n\r\n'
        response = self.handler_strange.handle_request(raw_request)
        self.assertTrue(self.handler_strange.request)
        self.assertTrue(self.handler_strange.request.is_bad_request)
        self.assertEqual(response[:22], b'HTTP/1.1 404 Not Found')

    # Добавьте дополнительные тесты для покрытия других случаев использования

if __name__ == '__main__':
    unittest.main()
