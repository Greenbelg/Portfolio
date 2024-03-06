import struct
import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)

from src.decoder import decode_name


class Question:
    def __init__(self, data):
        self.name = decode_name(data)

        self.qtype = struct.unpack('!H', data.read(2))[0]
        self.qclass = struct.unpack('!H', data.read(2))[0]

    def create_simple_question(domain):
        name = domain
        qtype = struct.pack('!H', 1)
        qclass = struct.pack('!H', 1)
        return name + qtype + qclass
