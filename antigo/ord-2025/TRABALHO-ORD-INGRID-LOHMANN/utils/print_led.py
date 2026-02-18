import struct

from . import constants
from .read_header import read_header


def print_led(filename):
    try:
        with open(filename, 'rb') as file:
            led_head = read_header(file)
            current_offset = led_head
            count = 0

            print("LED -> ", end="")

            while current_offset != constants.NULL_POINTER:
                file.seek(current_offset)
                size_data = file.read(constants.RECORD_SIZE_BYTES)
                if len(size_data) < constants.RECORD_SIZE_BYTES:
                    print(f"\nErro: espaço inválido na LED (offset: "
                          f"{current_offset}) — dados incompletos.")
                    break

                record_size = struct.unpack('H', size_data)[0]

                file.read(1)

                next_offset_data = file.read(constants.LED_POINTER_BYTES)
                if len(next_offset_data) < constants.LED_POINTER_BYTES:
                    print(f"\nErro: ponteiro da LED corrompido (offset: "
                          f"{current_offset}) — dados incompletos.")
                    break

                next_offset = struct.unpack('i', next_offset_data)[0]

                print(f"[offset: {current_offset}, tam: {record_size}] -> ",
                      end="")
                count += 1
                current_offset = next_offset

            print("[offset: -1]")
            print(f"Total: {count} espacos disponiveis")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
