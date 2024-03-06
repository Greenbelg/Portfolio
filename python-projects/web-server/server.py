import socket
import select
import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import src.config as config
from src.reactor import Reactor
from src.request_handler import BaseRequestHandler
from src.logger import configure_logger

logger = configure_logger(
    config.PATH_TO_LOGS,
    logging.INFO)


class EventHandler:
    def __call__(self, event_data):
        request_handler = BaseRequestHandler(event_data[0], event_data[1])
        request_handler(None)


class HTTPServer:
    def run(self):
        try:
            serv_sock = HTTPServer.create_serv_sock(self)
            cid = 0
            while True:
                client_sock = HTTPServer.accept_client_conn(self, 
                                                            serv_sock, cid)
                reactor.add_event(config.EVENT_TYPES.INCOMING, 
                                  (client_sock, cid))
                cid += 1
        except socket.gaierror as e:
            logger.exception(f'gaierror: {e}')
        except socket.timeout as e:
            logger.exception(f'timeout: {e}')

    def create_serv_sock(self):
        try:
            serv_socks = []
            for port in config.PORTS:
                serv_sock = socket.socket(socket.AF_INET, 
                                          socket.SOCK_STREAM, 
                                          proto=0)
                serv_sock.bind((config.SERVER_HOST, port))
                serv_sock.listen()
                serv_socks.append(serv_sock)
            return serv_socks
        except socket.error as e:
            logger.exception(f'socket.error: {e}')

    def accept_client_conn(self, serv_socks, cid):
        logger.info("Accept client connection")
        try:
            ready_sockets, _, _ = select.select(serv_socks, [], [])
            client_sock, client_addr = ready_sockets[0].accept()
            print(f'Client #{cid} connect {client_addr[0]}:{client_addr[1]}')
            return client_sock
        except socket.error as e:
            logger.exception(f'socket.error: {e}')


if __name__ == '__main__':
    reactor = Reactor()
    reactor.register_handler(config.EVENT_TYPES.INCOMING, EventHandler())
    reactor.start()

    server = HTTPServer()
    server.run()
