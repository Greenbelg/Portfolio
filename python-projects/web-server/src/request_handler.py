from pathlib import Path
import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import src.config as config
from src.HTTPRequest import HTTPRequest
from src.HTTPResponse import HTTPResponse
from src.logger import configure_logger

logger = configure_logger(
    config.PATH_TO_LOGS,
    logging.INFO)


class BaseRequestHandler:
    def __init__(self, client_sock, cid):
        self.client_sock = client_sock
        self.port = client_sock.getsockname()[1]
        self.cid = cid
        self.request = None

    def handle_request(self, raw_request):
        logger.info(f"Handling request {raw_request}")
        self.request = HTTPRequest(raw_request)
        if self.request.is_bad_request:
            return HTTPResponse.get_response(self.request)
        
        if self.port in config.HOSTS:
            return self._get_response()
        else:
            self.request.is_bad_request = True
            self.request.error = config.CODES.NOT_FOUND
            return HTTPResponse.get_response(self.request)

    def _get_response(self):
        path_to_page = Path(__file__).parent.parent\
            .joinpath("www")\
            .joinpath(config.HOSTS[self.port])\
            .joinpath(self.request.path)
        
        if not(Path.exists(path_to_page)):
            self.request.is_bad_request = True
            self.request.error = config.CODES.NOT_FOUND
            return HTTPResponse.get_response(self.request)
        
        return HTTPResponse.get_response(self.request, 
                                         data=path_to_page.open().read())

    def write_response(self, response):
        logger.info(f"Sending response: {response} for client")
        try:
            self.client_sock.sendall(response)
            self.client_sock.close()
            print(f'Client #{self.cid} has been served')
        except ConnectionError as e:
            logger.exception(f'ConnectionError writing response {e}')

    def __call__(self, event_data):
        try:
            request = self.client_sock.recv(config.ACCEPT_DATA_IN_BYTES)
            if isinstance(request, bytes):
                if request:
                    response = self.handle_request(request)
                    self.write_response(response)
                else:
                    print(f'Client #{self.cid} unexpectedly disconnected')
            else:
                logger.exception(f'''TypeError handling request: 
                                 a bytes-like object is required, 
                                 not {type(request)}''')
        except TypeError as e:
            logger.exception(f'TypeError handling request {e}')
