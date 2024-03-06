import struct
import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)

from src.data import Data


def decode_name(data: Data):
    parts = []
    while (length := struct.unpack('!b', data.read(1))[0]) != 0:
        if length & 0b1100_0000:
            parts.append(decode_compressed_name(data, length))
            break
        else:
            parts.append(data.read(length))
    return b".".join(parts)


def decode_compressed_name(data: Data, length):
    pointer_bytes = bytes([length & 0b0011_1111]) + data.read(1)
    pointer = struct.unpack("!H", pointer_bytes)[0]
    current_pos = data.cursor
    data.move_cursor(pointer)
    result = decode_name(data)
    data.move_cursor(current_pos)
    return result
