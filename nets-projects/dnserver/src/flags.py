import struct


class Flags:
    def __init__(self, data):
        self.flags = {}
        self._parse_flags(struct.unpack("!H", data.read(2))[0])

    def _parse_flags(self, flags_as_int):
        flags_string = bin(flags_as_int)[2:]
        if flags_string == '0':
            flags_string = '0'*16
        self.flags = {
            'QR': flags_string[0],
            'Opcode': flags_string[1:5],
            'AA': flags_string[5],
            'TC': flags_string[6],
            'RD': flags_string[7],
            'RA': flags_string[8],
            'Z': flags_string[9:12],
            'RCODE': flags_string[12:]
        }
