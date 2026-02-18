import struct


def write_header(file, head_offset):
    file.seek(0)
    file.write(struct.pack('i', head_offset))
