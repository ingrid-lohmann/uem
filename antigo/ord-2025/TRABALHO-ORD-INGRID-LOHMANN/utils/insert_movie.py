import struct

from . import constants
from .read_header import read_header
from .write_header import write_header


def insert_movie(filename, operation_line):
    try:
        with open(filename, 'r+b') as file:
            operation_line = operation_line.strip()
            record_str = operation_line[2:]
            record_bytes = record_str.encode("utf-8")
            required_size = len(record_bytes)
            movie_id = record_str.split('|', 1)[0]
            print(f"Inserção do registro de chave'{movie_id}' "
                  f"({required_size} bytes)")

            led_head = read_header(file)
            current_offset = led_head
            best_fit_offset = constants.NULL_POINTER
            best_fit_prev_offset = constants.NULL_POINTER
            best_fit_size = float('inf')
            prev_offset = constants.NULL_POINTER

            while current_offset != constants.NULL_POINTER:
                file.seek(current_offset)
                size_data = file.read(constants.RECORD_SIZE_BYTES)
                if len(size_data) < constants.RECORD_SIZE_BYTES:
                    break

                available_size = struct.unpack('H', size_data)[0]
                file.read(1)

                next_offset_data = file.read(constants.LED_POINTER_BYTES)
                if len(next_offset_data) < constants.LED_POINTER_BYTES:
                    break

                next_offset = struct.unpack('i', next_offset_data)[0]

                if available_size >= required_size and available_size < best_fit_size:
                    best_fit_size = available_size
                    best_fit_offset = current_offset
                    best_fit_prev_offset = prev_offset

                prev_offset = current_offset
                current_offset = next_offset

            if best_fit_offset != constants.NULL_POINTER:
                file.seek(best_fit_offset + constants.RECORD_SIZE_BYTES + 1)
                next_node_ptr = struct.unpack(
                    'i', file.read(constants.LED_POINTER_BYTES))[0]

                if best_fit_prev_offset == constants.NULL_POINTER:
                    write_header(file, next_node_ptr)
                else:
                    file.seek(best_fit_prev_offset +
                              constants.RECORD_SIZE_BYTES + 1)
                    file.write(struct.pack('i', next_node_ptr))

                file.seek(best_fit_offset)
                file.write(struct.pack('H', required_size))
                file.write(record_bytes)
                print(f'Tamanho do espaço reutilizado: {best_fit_size} bytes')
                print(f'Local: offset = {best_fit_offset} bytes'
                      f"(0x{best_fit_offset:x})")
            else:
                file.seek(0, 2)
                file.write(struct.pack('H', required_size))
                file.write(record_bytes)
                print("Local: fim do arquivo")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
