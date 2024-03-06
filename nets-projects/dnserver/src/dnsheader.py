import struct
import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)

from src.data import Data
from src.flags import Flags
import random


class Header:
    def __init__(self, data: Data):
        self.id = struct.unpack("!H", data.read(2))[0]
        self.flags = Flags(data)
        self.qdcount = struct.unpack("!H", data.read(2))[0]
        self.ancount = struct.unpack("!H", data.read(2))[0]
        self.nscount = struct.unpack("!H", data.read(2))[0]
        self.arcount = struct.unpack("!H", data.read(2))[0]
        self.check_rcode()
    
    def check_rcode(self):
        if self.flags.flags['RCODE'] == '' or int(self.flags.flags['RCODE'], 2) == 0:
            return
        
        if int(self.flags.flags['RCODE'], 2) == 1:
            raise Exception('Format error')
        if int(self.flags.flags['RCODE'], 2) == 2:
            raise Exception('Server failure')
        if int(self.flags.flags['RCODE'], 2) == 3:
            raise Exception('Name Error')
        if int(self.flags.flags['RCODE'], 2) == 4:
            raise Exception('Not Implemented')
        if int(self.flags.flags['RCODE'], 2) == 5:
            raise Exception('Refused')


    def create_simple_header():
        id = struct.pack('!H', random.randrange(0, 2**16-1))
        flags = struct.pack('!H', int('0000000100000000', 2))
        qdcount = struct.pack("!H", 1)
        ancount = struct.pack("!H", 0)
        nscount = struct.pack("!H", 0)
        arcount = struct.pack("!H", 0)
        return id + flags + qdcount + ancount + nscount + arcount
