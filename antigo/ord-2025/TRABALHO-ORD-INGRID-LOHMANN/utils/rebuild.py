import struct
import re


def reconstruir_registros(raw_text):
    registros = []
    buffer = ""
    pipe_count = 0
    for char in raw_text:
        buffer += char
        if char == "|":
            pipe_count += 1
        if pipe_count == 7:
            buffer = buffer.strip()
            campos = buffer.split("|")
            campos[0] = re.sub(r"^\D+", "", campos[0])
            registros.append("|".join(campos))
            buffer = ""
            pipe_count = 0
    return registros


def rebuild_from_source(source_file, output_file):
    try:
        with open(source_file, "rb") as f:
            f.seek(4)
            tamanho_total_bytes = f.read(2)
            if not tamanho_total_bytes:
                print("Arquivo de entrada vazio ou inválido.")
                return False
            tamanho_total = struct.unpack("H", tamanho_total_bytes)[0]
            bloco = f.read(tamanho_total)
            texto = bloco.decode("utf-8", errors="ignore")
        registros = reconstruir_registros(texto)
        print(f"-> {len(registros)} registros extraídos para reconstrução.")
        with open(output_file, "wb") as f_out:
            f_out.write(struct.pack("i", -1))
            for registro in registros:
                dados = registro.encode("utf-8")
                f_out.write(struct.pack("H", len(dados)))
                f_out.write(dados)

        print(f"-> Arquivo corrigido salvo como '{output_file}'.")
        return True

    except FileNotFoundError:
        print(f"ERRO: Arquivo de entrada ('{source_file}') não encontrado.")
        return False
    except Exception as e:
        print(f"Ocorreu um erro durante a reconstrução: {e}")
        return False


if __name__ == "__main__":
    source_file = "original/filmes.dat"
    output_file = "filmes.dat"
    rebuild_from_source(source_file, output_file)
