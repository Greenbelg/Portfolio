import socket
import sys
from pathlib import Path

sys.path.append(Path(__file__).parent)
sys.path.append(Path(__file__).parent.joinpath('src'))

from src.dnserver import DNServer


def main():
    dns_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_server_socket.bind(('127.0.0.1', 53))
    while True:
        client_request, client_address = dns_server_socket.recvfrom(1024)
        dns_server = DNServer(client_request)
        dns_server_socket.sendto(dns_server.get_answer(), client_address)


if __name__ == '__main__':
    main()