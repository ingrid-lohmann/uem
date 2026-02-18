import struct
from . import constants


def read_header(file):
    file.seek(0)
    header_data = file.read(constants.HEADER_SIZE)
    if len(header_data) < constants.HEADER_SIZE:
        return constants.NULL_POINTER
    return struct.unpack('i', header_data)[0]
