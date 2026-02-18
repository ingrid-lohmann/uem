import sys
import os
import struct

# Constantes do arquivo
HEADER_SIZE = 4
RECORD_SIZE_BYTES = 2
LED_POINTER_BYTES = 4
DELETION_MARKER = b'*'
NULL_POINTER = -1

def read_header(file):
    file.seek(0)
    header_data = file.read(HEADER_SIZE)
    if len(header_data) < HEADER_SIZE:
        return NULL_POINTER
    return struct.unpack('i', header_data)[0]

def write_header(file, head_offset):
    file.seek(0)
    file.write(struct.pack('i', head_offset))

def search_movie(filename, movie_id):
    print(f'Busca pelo registro de chave "{movie_id}"')
    with open(filename, 'rb') as file:
        file.seek(HEADER_SIZE)
        while True:
            record_size_data = file.read(RECORD_SIZE_BYTES)
            if not record_size_data:
                break
            record_size = struct.unpack('H', record_size_data)[0]
            record_data = file.read(record_size)
            if not record_data.startswith(DELETION_MARKER):
                try:
                    # CORREÇÃO APLICADA AQUI: Remove o BOM se existir
                    decoded_data = record_data.decode('utf-8', errors='ignore').lstrip('\ufeff')
                    current_id_str = decoded_data.split('|')[0]
                    if current_id_str.isdigit() and int(current_id_str) == movie_id:
                        print(f'{decoded_data} ({record_size} bytes)')
                        return
                except (IndexError, ValueError):
                    continue
    print("Erro: registro não encontrado!")

def insert_movie(filename, operation_line):
    with open(filename, 'r+b') as file:
        parts = operation_line.strip().split(' ', 2)
        movie_id, movie_data_string = parts[1], parts[2]
        record_str = f"{movie_id}|{movie_data_string}"
        record_bytes = record_str.encode('utf-8')
        required_size = len(record_bytes)
        print(f'Inserção do registro de chave "{movie_id}" ({required_size} bytes)')
        led_head = read_header(file)
        current_offset = led_head
        best_fit_offset, best_fit_prev_offset, best_fit_size = NULL_POINTER, NULL_POINTER, float('inf')
        prev_offset = NULL_POINTER
        while current_offset != NULL_POINTER:
            file.seek(current_offset)
            available_size = struct.unpack('H', file.read(RECORD_SIZE_BYTES))[0]
            file.read(1)
            next_offset = struct.unpack('i', file.read(LED_POINTER_BYTES))[0]
            if available_size >= required_size and available_size < best_fit_size:
                best_fit_size, best_fit_offset, best_fit_prev_offset = available_size, current_offset, prev_offset
            prev_offset, current_offset = current_offset, next_offset
        if best_fit_offset != NULL_POINTER:
            file.seek(best_fit_offset + RECORD_SIZE_BYTES + 1)
            next_node_ptr = struct.unpack('i', file.read(LED_POINTER_BYTES))[0]
            if best_fit_prev_offset == NULL_POINTER:
                write_header(file, next_node_ptr)
            else:
                file.seek(prev_offset + RECORD_SIZE_BYTES + 1)
                file.write(struct.pack('i', next_node_ptr))
            file.seek(best_fit_offset)
            file.write(struct.pack('H', required_size))
            file.write(record_bytes)
            print(f'Tamanho do espaço reutilizado: {best_fit_size} bytes')
            print(f'Local: offset = {best_fit_offset} bytes (0x{best_fit_offset:x})')
        else:
            file.seek(0, 2)
            file.write(struct.pack('H', required_size))
            file.write(record_bytes)
            print("Local: fim do arquivo")

def remove_movie(filename, movie_id):
    print(f'Remoção do registro de chave "{movie_id}"')
    with open(filename, 'r+b') as file:
        file.seek(HEADER_SIZE)
        while True:
            current_offset = file.tell()
            record_size_data = file.read(RECORD_SIZE_BYTES)
            if not record_size_data: break
            record_size = struct.unpack('H', record_size_data)[0]
            record_data_pos = file.tell()
            record_data = file.read(record_size)
            if not record_data.startswith(DELETION_MARKER):
                try:
                    # CORREÇÃO APLICADA AQUI: Remove o BOM se existir
                    decoded_data = record_data.decode('utf-8', errors='ignore').lstrip('\ufeff')
                    current_id_str = decoded_data.split('|')[0]
                    if current_id_str.isdigit() and int(current_id_str) == movie_id:
                        led_head = read_header(file)
                        file.seek(record_data_pos)
                        file.write(DELETION_MARKER)
                        file.write(struct.pack('i', led_head))
                        write_header(file, current_offset)
                        print("Registro removido!")
                        print(f"({record_size} bytes)")
                        print(f"Local: offset = {current_offset} bytes (0x{current_offset:x})")
                        return
                except (IndexError, ValueError): continue
    print("Erro: registro não encontrado!")

def print_led(filename):
    with open(filename, 'rb') as file:
        led_head = read_header(file)
        current_offset = led_head
        count = 0
        print("LED -> ", end="")
        while current_offset != NULL_POINTER:
            count += 1
            file.seek(current_offset)
            record_size = struct.unpack('H', file.read(RECORD_SIZE_BYTES))[0]
            file.read(1)
            next_offset = struct.unpack('i', file.read(LED_POINTER_BYTES))[0]
            print(f"[offset: {current_offset}, tam: {record_size}] -> ", end="")
            current_offset = next_offset
        print(f"[offset: -1]")
        print(f"Total: {count} espacos disponiveis")

def compact_file(filename):
    print(f"Iniciando a compactação do arquivo '{filename}'...")
    temp_filename = filename + ".tmp"
    try:
        with open(filename, 'rb') as old_file, open(temp_filename, 'wb') as new_file:
            new_file.write(struct.pack('i', NULL_POINTER))
            old_file.seek(HEADER_SIZE)
            while True:
                record_size_data = old_file.read(RECORD_SIZE_BYTES)
                if not record_size_data: break
                record_size = struct.unpack('H', record_size_data)[0]
                record_data = old_file.read(record_size)
                if not record_data.startswith(DELETION_MARKER):
                    new_file.write(record_size_data)
                    new_file.write(record_data)
        os.replace(temp_filename, filename)
        print("Arquivo compactado com sucesso. A LED foi resetada.")
    except Exception as e:
        print(f"Ocorreu um erro durante a compactação: {e}")
        if os.path.exists(temp_filename): os.remove(temp_filename)

def main():
    if len(sys.argv) < 2:
        print("Uso: python programa.py [-e <arquivo_ops> | -p | -c]")
        return
    mode = sys.argv[1]
    data_filename = "filmes.dat"
    if not os.path.exists(data_filename) and mode in ['-p', '-c']:
        print(f"Erro: O arquivo '{data_filename}' não existe.")
        return
    if not os.path.exists(data_filename) and mode == '-e':
        with open(data_filename, 'wb') as f:
            write_header(f, NULL_POINTER)
    if mode == '-e':
        if len(sys.argv) < 3:
            print("Uso: python programa.py -e <arquivo_operacoes>")
            return
        ops_filename = sys.argv[2]
        # CORREÇÃO APLICADA AQUI: utf-8-sig lida com o BOM automaticamente
        with open(ops_filename, 'r', encoding='utf-8-sig') as ops_file:
            for line in ops_file:
                line = line.strip()
                if not line: continue
                op_code = line.split(' ')[0]
                if op_code == 'b':
                    movie_id = int(line.split(' ')[1])
                    search_movie(data_filename, movie_id)
                elif op_code == 'i':
                    insert_movie(data_filename, line)
                elif op_code == 'r':
                    movie_id = int(line.split(' ')[1])
                    remove_movie(data_filename, movie_id)
                print("-" * 20)
    elif mode == '-p': print_led(data_filename)
    elif mode == '-c': compact_file(data_filename)
    else: print(f"Erro: modo '{mode}' desconhecido. Use -e, -p ou -c.")

if __name__ == "__main__":
    main()