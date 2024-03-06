import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import src.config as config
from src.HTTPResponse import HTTPResponse
from src.HTTPRequest import HTTPRequest


class TestHTTPResponse(unittest.TestCase):
    def test_get_response_ok(self):
        valid_request = HTTPRequest(b'GET /path HTTP/1.1\r\nHost: example.com\r\n\r\n')
        config.HEADERS['Content-Type'] = 'application/json'
        config.HEADERS['Server'] = 'MyServer'

        headers = ['Content-Type', 'Server']
        data = '{"key": "value"}'
        expected_response = b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nServer: MyServer\r\n\r\n{"key": "value"}'

        response = HTTPResponse.get_response(valid_request, headers, data)
        self.assertEqual(response, expected_response)

        config.HEADERS.clear()

    def test_get_response_bad_request(self):
        invalid_request = HTTPRequest(b'Invalid Request')
        config.HEADERS['Content-Type'] = 'text/plain'
        print(config.HEADERS)
        headers = ['Content-Type']
        data = 'Error: Bad Request'
        expected_response = b'HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nError: Bad Request'

        response = HTTPResponse.get_response(invalid_request, headers, data)
        self.assertEqual(response, expected_response)

        config.HEADERS.clear()

    def test_get_response_attribute_error(self):
        invalid_request = HTTPRequest(b'GET /path HTTP/1.1\r\nHost: example.com\r\n\r\n')
        invalid_request.error = 500
        config.STATES_CODES[500] = b'Internal Server Error'
        config.HEADERS['Content-Type'] = 'text/plain'
        
        headers = ['Content-Type']
        data = 'Internal Server Error'
        expected_response = b'HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nInternal Server Error'
        response = HTTPResponse.get_response(invalid_request, headers, data)
        self.assertEqual(response, expected_response)

        config.HEADERS.clear()
        config.STATES_CODES.pop(500)


if __name__ == '__main__':
    unittest.main()
