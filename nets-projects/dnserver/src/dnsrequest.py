import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)

from src.dnsheader import Header
from src.dnsquestion import Question
from src.dnsrecord import Record
from src.data import Data


class DNSRequest:
    def __init__(self, data: Data):
        self.header = Header(data)
        self.questions = [Question(data) for _ in range(self.header.qdcount)]
        self.answers = [Record(data) for _ in range(self.header.ancount)]
        self.authorities = [Record(data) for _ in range(self.header.nscount)]
        self.additionals = [Record(data) for _ in range(self.header.arcount)]

    def create_simple_request(domain):
        header = Header.create_simple_header()
        question = Question.create_simple_question(domain)
        return header + question
    