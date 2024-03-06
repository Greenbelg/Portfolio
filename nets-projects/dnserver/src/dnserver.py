import sys
import socket
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)

from src.data import Data
from src.dnsrequest import DNSRequest
from src.cach import Cach
import random


ROOT = ('198.41.0.4', 53)

class DNServer:
    def __init__(self, client_request):
        self.client_request = client_request

    def get_answer(self):
        client_request_data = DNSRequest(Data(self.client_request))
        if answer := self.__try_get_answer_from_cach(client_request_data): 
            print(f'Send caching answer')
            return answer

        return self.__get_answer_from_remote()

    def __try_get_answer_from_cach(self, data_from_client):
        if ans := Cach().try_get_record_by_domain_name(data_from_client.questions[0].name):
            data_ans = Data(ans)
            data_ans.read(2)
            data_ans = data_from_client.header.id.to_bytes(2, 'big') + data_ans.show()
            return data_ans

    def __has_request_answer(self, answer_data):
        if len(answer_data.answers) != 0:
                return True
        return False
    
    def __try_get_ip_for_next_remote(self, answer):
        next_addresses = [ipv4 for ipv4 in [additional.get_ipv4_address() for additional in answer.additionals] if ipv4 != None]
        if len(next_addresses) != 0:
            return next_addresses[random.randrange(0, len(next_addresses) - 1)]

    def __try_resolve_ip_for_domain(self, domain):
        subserver = DNServer(DNSRequest.create_simple_request(domain))
        answer_data = DNSRequest(Data(subserver.__get_answer_from_remote()))
        for answer in answer_data.answers:
            if ip := answer.get_ipv4_address():
                return ip

    def __proceed_authorities(self, answer_data: DNSRequest):
        for authority in answer_data.authorities:
            if ip := self.__try_resolve_ip_for_domain(authority.rsdata):
                return ip
        
        raise Exception('Something went wrong. IP could not be identified.')

    def __get_answer_from_remote(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        current_remote = ROOT
        while True:
            sock.sendto(self.client_request, current_remote)
            
            server_answer, _ = sock.recvfrom(1024)
            answer_data = DNSRequest(Data(server_answer))
            if self.__has_request_answer(answer_data):
                answer_data.answers[0].cach_address(server_answer)
                return server_answer

            if ip := self.__try_get_ip_for_next_remote(answer_data):
                pass
            else:
                ip = self.__proceed_authorities(answer_data)
            current_remote = (ip, 53)
