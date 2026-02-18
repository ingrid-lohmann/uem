import os
import struct
from . import constants


def compact_file(filename):
    print(f"Iniciando a compactação do arquivo '{filename}'...")
    temp_filename = filename + ".tmp"
    try:
        with (open(filename, 'rb') as old_file, open(temp_filename, 'wb') as
              new_file):
            new_file.write(struct.pack('i', constants.NULL_POINTER))

            old_file.seek(constants.HEADER_SIZE)
            while True:
                record_size_data = old_file.read(constants.RECORD_SIZE_BYTES)
                if not record_size_data:
                    break

                record_size = struct.unpack('H', record_size_data)[0]
                record_data = old_file.read(record_size)

                if record_data[0:1] != constants.DELETION_MARKER:
                    new_file.write(record_size_data)
                    new_file.write(record_data)

        os.replace(temp_filename, filename)
        print("Arquivo compactado com sucesso. A LED foi resetada.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' "
              f"não foi encontrado para compactação.")
    except Exception as e:
        print(f"Ocorreu um erro durante a compactação: {e}")
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
