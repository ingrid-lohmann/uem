#Ingrid Lohmann
# RA: 117698
import sys
import os

from utils.constants import NULL_POINTER
from utils.write_header import write_header
from utils.rebuild import rebuild_from_source
from utils.search_movie import search_movie
from utils.insert_movie import insert_movie
from utils.remove_movie import remove_movie
from utils.print_led import print_led
from utils.compact_file import compact_file


def main():
    if len(sys.argv) < 2:
        print("Uso: python programa.py [-e <ops> | -p | -c | -a]")
        return

    mode = sys.argv[1]
    data_filename = "filmes.dat"

    if mode == '-a':
        arquivo_origem = "original/filmes.dat"
        print(f"Modo de Ajuste: Reconstruindo '{data_filename}' "
              f"a partir de '{arquivo_origem}'...")
        rebuild_from_source(arquivo_origem, data_filename)

    elif mode == '-e':
        if len(sys.argv) < 3:
            print("Uso: python programa.py -e <arquivo_operacoes>")
            return

        if not os.path.exists(data_filename):
            with open(data_filename, 'wb') as f:
                write_header(f, NULL_POINTER)

        ops_filename = sys.argv[2]
        try:
            with open(ops_filename, 'r', encoding='utf-8-sig') as ops_file:
                for line in ops_file:
                    line = line.strip()
                    if not line:
                        continue

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
        except FileNotFoundError:
            print(
                f"Erro: Arquivo de operações '{ops_filename}' não encontrado.")

    elif mode == '-p':
        if not os.path.exists(data_filename):
            print(f"Erro: O arquivo  '{data_filename}' "
                  f"não existe. Use a flag -a para criá-lo.")
            return
        print_led(data_filename)

    elif mode == '-c':
        if not os.path.exists(data_filename):
            print(f"Erro: O arquivo  '{data_filename}' "
                  f"não existe. Use a flag -a para criá-lo.")
            return
        compact_file(data_filename)

    else:
        print(f"Erro: modo '{mode}' desconhecido. Use -e, -p, -c ou -a.")


if __name__ == "__main__":
    main()
