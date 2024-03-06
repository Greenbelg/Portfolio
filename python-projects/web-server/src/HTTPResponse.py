import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import src.config as config
from src.HTTPRequest import HTTPRequest
from src.logger import configure_logger

logger = configure_logger(
    config.PATH_TO_LOGS,
    logging.INFO)


class HTTPResponse:
    def get_response(request: HTTPRequest, headers=[], data=""):
        try:
            code_state = config.STATES_CODES.get(request.error, b"OK")
            title = b" ".join(
                [f"HTTP/{request.version if request.version else '1.1'}".encode(),
                 str(config.CODES.OK if request.error == 0 
                     else request.error).encode(),
                 code_state])
            
            response_headers = b"\r\n".join(
                [title,
                 *[b": ".join([header.encode(), config.HEADERS[header].encode()])
                   for header in headers if header in config.HEADERS]])
            
            body = bytes(data, encoding="utf-8")
            return b"\r\n\r\n".join([response_headers, body])
        except AttributeError as e:
            logger.exception(f'AttributeError getting response {e}')
        except KeyError as e:
            logger.exception(f'KeyError getting response {e}')
        except TypeError as e:
            logger.exception(f'TypeError getting response {e}')
