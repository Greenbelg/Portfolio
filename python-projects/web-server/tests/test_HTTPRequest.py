import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from src.HTTPRequest import HTTPRequest

class TestHTTPRequest(unittest.TestCase):
    def test_valid_request(self):
        valid_request = b'GET /path HTTP/1.1\r\nHost: example.com\r\n\r\n'
        http_request = HTTPRequest(valid_request)
        self.assertFalse(http_request.is_bad_request)
        self.assertEqual(http_request.method, 'GET')
        self.assertEqual(http_request.path, 'path')
        self.assertEqual(http_request.version, '1.1')

    def test_invalid_request(self):
        invalid_request = b'Invalid Request'
        http_request = HTTPRequest(invalid_request)
        self.assertTrue(http_request.is_bad_request)
        self.assertEqual(http_request.error, 400)

    def test_unicode_decode_error(self):
        unicode_request = b'\x80\x81\x82'
        http_request = HTTPRequest(unicode_request)
        self.assertTrue(http_request.is_bad_request)

    def test_get_header(self):
        valid_request = b'GET /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/json\r\n\r\n'
        http_request = HTTPRequest(valid_request)
        self.assertEqual(http_request.get_header('Host'), 'example.com')
        self.assertEqual(http_request.get_header('Content-Type'), 'application/json')

    def test_get_header_key_error(self):
        invalid_request = b'Invalid Request'
        http_request = HTTPRequest(invalid_request)
        http_request.get_header('Host')
        self.assertTrue(http_request.is_bad_request)

    def test_get_body(self):
        valid_request = b'GET /path HTTP/1.1\r\nHost: example.com\r\n\r\n{"key": "value"}'
        http_request = HTTPRequest(valid_request)
        self.assertEqual(http_request.get_body(), '{"key": "value"}')

    def test_get_body_no_body(self):
        valid_request = b'GET /path HTTP/1.1\r\nHost: example.com\r\n\r\n'
        http_request = HTTPRequest(valid_request)
        self.assertEqual(http_request.get_body(), '')

if __name__ == '__main__':
    unittest.main()
