import re
import struct
from . import constants


def search_movie(filename, movie_id):
    print(f'Busca pelo registro de chave "{movie_id}"')
    try:
        with open(filename, 'rb') as file:
            file.seek(constants.HEADER_SIZE)
            while True:
                record_size_data = file.read(constants.RECORD_SIZE_BYTES)
                if not record_size_data:
                    break

                record_size = struct.unpack('H', record_size_data)[0]
                record_data = file.read(record_size)

                if not record_data.startswith(constants.DELETION_MARKER):
                    try:
                        decoded_data = record_data.decode(
                            'utf-8', errors='ignore').lstrip('\ufeff')
                        id_field = decoded_data.split('|', 1)[0]
                        match = re.search(r'(\d+)', id_field)

                        if match and int(match.group(1)) == movie_id:
                            print(f'{decoded_data} ({record_size} bytes)')
                            return
                    except (IndexError, ValueError):
                        continue

        print("Erro: registro não encontrado!")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
