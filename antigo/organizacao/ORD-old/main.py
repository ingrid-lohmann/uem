import struct
import sys
import os

HEADER_SIZE = 4
RECORD_SIZE_FIELD = 2
MIN_UNUSED_SPACE = 10


def read_header(file):
    file.seek(0)
    header = file.read(HEADER_SIZE)
    return struct.unpack('I', header)[0]


def write_header(file, value):
    file.seek(0)
    file.write(struct.pack('I', value))


def read_record(file):
    size_data = file.read(RECORD_SIZE_FIELD)
    if not size_data or len(size_data) < RECORD_SIZE_FIELD:
        return None, None
    record_size = struct.unpack('H', size_data)[0]
    record_data = file.read(record_size)
    return record_size, record_data


def write_record(file, record_data):
    record_size = len(record_data)
    file.write(struct.pack('H', record_size))
    file.write(record_data)


def search_by_id(file, search_id):
    file.seek(HEADER_SIZE)  # Skip the header
    search_id_encoded = search_id.encode('utf-8')
    while True:
        pos = file.tell()
        record_size, record_data = read_record(file)
        if not record_data:
            return None, None
        try:
            if record_data[:len(search_id_encoded)] == search_id_encoded:
                return pos, record_data
        except UnicodeDecodeError:
            pass
    return None, None


def insert_game(file, game_data):
    header = read_header(file)
    game_data_encoded = game_data.encode('utf-8')
    game_size = len(game_data_encoded)

    # Search for space in LED
    if header != 0:
        led = header
        prev_led = None
        while led != -1:
            file.seek(led)
            size_data = file.read(4)
            next_led_data = file.read(4)
            if len(size_data) < 4 or len(next_led_data) < 4:
                break
            size = struct.unpack('I', size_data)[0]
            next_led = struct.unpack('I', next_led_data)[0]
            if size >= game_size + RECORD_SIZE_FIELD:
                if prev_led is None:
                    write_header(file, next_led)
                else:
                    file.seek(prev_led + 4)
                    file.write(struct.pack('I', next_led))
                file.seek(led)
                write_record(file, game_data_encoded)
                remaining_space = size - game_size - RECORD_SIZE_FIELD
                if remaining_space > MIN_UNUSED_SPACE:
                    file.write(struct.pack('I', remaining_space))
                    file.write(struct.pack('I', next_led))
                return (
                    f"{game_size} bytes\nTamanho do espaço reutilizado: {
                        size} bytes (sobra {remaining_space} bytes)\n"
                    f"Local: offset = {led} bytes (0x{led:x})")
            prev_led = led
            led = next_led
        file.seek(0, 2)  # Move to end of file
        pos = file.tell()
        write_record(file, game_data_encoded)
        return f"{game_size} bytes\nLocal: fim do arquivo"
    else:
        file.seek(0, 2)  # Move to end of file
        pos = file.tell()
        write_record(file, game_data_encoded)
        return f"{game_size} bytes\nLocal: fim do arquivo"


def remove_game(file, remove_id):
    pos, record_data = search_by_id(file, remove_id)
    if not record_data:
        return False, None
    file.seek(pos)
    size = struct.unpack('H', file.read(2))[0]
    header = read_header(file)
    file.seek(pos)
    file.write(struct.pack('I', header))  # Write next LED pointer
    file.write(struct.pack('I', size))  # Write size of the removed space
    write_header(file, pos)
    return True, f"Registro removido! ({size} bytes) Local: offset = {pos} bytes (0x{pos:x})"


def print_led(file):
    header = read_header(file)
    if header == 0:
        print("LED -> [offset: -1] Total: 0 espacos disponiveis")
        return
    led = header
    total_spaces = 0
    print("LED -> ", end="")
    while led != -1:
        file.seek(led)
        # problema está aqui
        size_data = file.read(4)
        next_led_data = file.read(4)
        if len(size_data) < 4 or len(next_led_data) < 4:
            print(f"len size {file.seek(led)}")
            print(f"len next {len(next_led_data)}")
            break
        print('oooo')
        size = struct.unpack('I', size_data)[0]
        next_led = struct.unpack('I', next_led_data)[0]
        print(f"[offset: {led}, tam: {size}] -> ", end="")
        led = next_led
        total_spaces += 1
        print(f">>> {total_spaces}")
    print(f"[offset: -1] Total: {total_spaces} espacos disponiveis")


def execute_operations(data_file, operations_file):
    with open(data_file, 'r+b') as file:
        if os.path.getsize(data_file) == 0:
            write_header(file, 0)
        with open(operations_file, 'r') as operations:
            for line in operations:
                operation = line.strip().split()
                if operation[0] == 'b':
                    search_id = operation[1]
                    _, result = search_by_id(file, search_id)
                    if result:
                        print(
                            f'Busca pelo registro de chave "{
                                search_id}" {result.decode("utf-8")}'
                        )
                    else:
                        print(f'Erro: registro não encontrado!')
                elif operation[0] == 'i':
                    game_data = ' '.join(operation[1:])
                    result = insert_game(file, game_data)
                    print(
                        f'Inserção do registro de chave "{operation[1].split("|")[0]}" {
                            result}'
                    )
                elif operation[0] == 'r':
                    remove_id = operation[1]
                    success, result = remove_game(file, remove_id)
                    if success:
                        print(
                            f'Remoção do registro de chave "{
                                remove_id}"\n{result}'
                        )
                    else:
                        print(f'Erro: registro não encontrado!')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python script.py -e <operations_file> or python script.py -p"
        )
    elif sys.argv[1] == '-e':
        execute_operations('dados.dat', sys.argv[2])
    elif sys.argv[1] == '-p':
        with open('dados.dat', 'r+b') as file:
            print_led(file)
