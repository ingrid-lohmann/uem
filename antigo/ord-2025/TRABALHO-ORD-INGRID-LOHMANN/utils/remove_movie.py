import re
import struct
from . import constants
from .read_header import read_header
from .write_header import write_header


def remove_movie(filename, movie_id):
    print(f'Remoção do registro de chave "{movie_id}"')
    try:
        with open(filename, 'r+b') as file:
            file.seek(constants.HEADER_SIZE)
            while True:
                current_offset = file.tell()
                record_size_data = file.read(constants.RECORD_SIZE_BYTES)
                if not record_size_data:
                    break

                record_size = struct.unpack('H', record_size_data)[0]
                record_data_pos = file.tell()
                record_data = file.read(record_size)

                if not record_data.startswith(constants.DELETION_MARKER):
                    try:
                        decoded_data = record_data.decode(
                            'utf-8', errors='ignore').lstrip('\ufeff')
                        id_field = decoded_data.split('|', 1)[0]
                        match = re.search(r'(\d+)', id_field)

                        if match and int(match.group(1)) == movie_id:
                            led_head = read_header(file)

                            file.seek(record_data_pos)
                            file.write(constants.DELETION_MARKER)
                            file.write(struct.pack('i', led_head))

                            write_header(file, current_offset)

                            print("Registro removido!")
                            print(f"({record_size} bytes)")
                            print(f"Local: offset = {current_offset} bytes "
                                  f"(0x{current_offset:x})")
                            return
                    except (IndexError, ValueError):
                        continue

        print("Erro: registro não encontrado!")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
