import re
import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import src.config as config
from src.logger import configure_logger

logger = configure_logger(
    config.PATH_TO_LOGS,
    logging.INFO)


class HTTPRequest:
    def __init__(self, request: bytes):
        try:
            self.request = request.decode()
        except UnicodeDecodeError as e:
            self.request = ''
            logger.error(f'UnicodeDecodeError decoding request: {e}')
        self._headers = {}
        self._body = ""
        self.is_bad_request = False
        self.error = 0
        self.method, self.path, self.version = '', '', ''
        self._define_request_line()

    def _define_request_line(self):
        match = re.match(r'(\w+) (\S+) HTTP/(\d\.\d)', self.request)
        if match:
            self.method, self.path, self.version = match.groups()
            if self.method and self.path and self.version:
                self.path = self.path[1:] if self.path[0] == '/'\
                    else self.path
            else:
                self.error = config.CODES.BAD_REQUEST
                self.is_bad_request = True
        else:
            self.error = config.CODES.BAD_REQUEST
            self.is_bad_request = True

    def get_header(self, header):
        if len(self._headers) != 0 and header in self._headers:
            return self._headers[header]
        elif len(self._headers) != 0 and header not in self._headers:
            raise KeyError(f"{header} doesn't define")

        try:
            request_lines = self.request\
                .split(config.CRLF * 2)[0]\
                .split(config.CRLF)[1:]
            self._headers = {header.split(':')[0].strip():
                             header.split(':')[1].strip()
                             for header in request_lines}
            return self._headers[header]
        except IndexError:
            logger.exception('IndexError getting headers')
            self.is_bad_request = True
        except KeyError:
            logger.exception(f"{header} doesn't define")
            self.is_bad_request = True

    def get_body(self):
        if self._body != "":
            return self._body
        try:
            self._body = self.request.split(config.CRLF * 2)[1]
        except IndexError:
            logger.exception('No body found in the request')
        finally:
            return self._body
