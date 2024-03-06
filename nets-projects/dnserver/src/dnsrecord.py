import struct
import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)

from src.cach import Cach
from src.data import Data
from src.decoder import decode_name


class Record:
    def __init__(self, data):
        self.name = decode_name(data)
        self.qtype = struct.unpack('!H', data.read(2))[0]
        self.qclass = struct.unpack('!H', data.read(2))[0]
        self.ttl =  struct.unpack('!l', data.read(4))[0]
        self.rdlength = struct.unpack('!H', data.read(2))[0]
        self.rsdata = data.read(self.rdlength)

    def get_ipv4_address(self):
        if self.qtype != 1 or self.qclass != 1:
            return None
        return ".".join([str(x) for i, x in enumerate(self.rsdata) if i < 4])

    def get_name_authority(self):
        try:
            return decode_name(Data(self.rsdata))
        except struct.error:
            return None
        
    def cach_address(self, answer):
        record = Cach()
        record.record_data(self.name, answer, self.ttl)