import pytest
import os
import sys
import struct
import programa

from utils.insert_movie import insert_movie
from utils.search_movie import search_movie
from utils.remove_movie import remove_movie
from utils.print_led import print_led
from utils.compact_file import compact_file
from utils.rebuild import rebuild_from_source


@pytest.fixture
def arquivo_dat_temporario(tmp_path):
    # Prepara um arquivo .dat limpo para cada teste
    data_filename = tmp_path / "filmes.dat"
    with open(data_filename, 'wb') as f:
        f.write(struct.pack('i', -1))
    return str(data_filename)


def test_insercao_e_busca(arquivo_dat_temporario, capsys):
    # deve inserir e buscar um registro com sucesso
    path = arquivo_dat_temporario
    insert_movie(
        path,
        "i 101|O Grande Hotel Budapeste|Wes Anderson|2014|Aventura|99|Ralph Fiennes"
    )
    search_movie(path, 101)
    captured = capsys.readouterr()
    assert "O Grande Hotel Budapeste" in captured.out
    assert "Erro: registro não encontrado!" not in captured.out


def test_remocao_e_led(arquivo_dat_temporario, capsys):
    # deve remover um registro e verificar se ele aparece na LED
    path = arquivo_dat_temporario
    insert_movie(
        path,
        "i 42|Guia do Mochileiro das Galáxias|Garth Jennings|2005|Aventura|109|Martin Freeman"
    )
    remove_movie(path, 42)
    search_movie(path, 42)
    captured_search = capsys.readouterr()
    assert "Erro: registro não encontrado!" in captured_search.out
    print_led(path)
    captured_led = capsys.readouterr()
    assert "[offset: 4, tam: 83]" in captured_led.out
    assert "Total: 1 espacos disponiveis" in captured_led.out


def test_compactacao(arquivo_dat_temporario):
    # deve reduzir o tamanho do arquivo após a compactação
    path = arquivo_dat_temporario
    insert_movie(path, "i 1|Filme A|...|...")
    insert_movie(path, "i 2|Filme B|...|...")
    remove_movie(path, 1)
    tamanho_antes = os.path.getsize(path)
    compact_file(path)
    tamanho_depois = os.path.getsize(path)
    assert tamanho_depois < tamanho_antes


def test_reconstrucao(tmp_path):
    # deve reconstruir um arquivo a partir de uma fonte corrompida
    original_dir = tmp_path / "original"
    original_dir.mkdir()
    arquivo_origem = original_dir / "filmes.dat"
    texto_corrompido = "x34|O Labirinto do Fauno|Guillermo del Toro|2006|Drama|Fantasia|Guerra|"
    bloco = texto_corrompido.encode('utf-8')
    with open(arquivo_origem, 'wb') as f:
        f.write(struct.pack('i', -1))
        f.write(struct.pack('H', len(bloco)))
        f.write(bloco)
    arquivo_saida = tmp_path / "filmes.dat"
    rebuild_from_source(str(arquivo_origem), str(arquivo_saida))
    assert os.path.exists(arquivo_saida)
    with open(arquivo_saida, 'rb') as f:
        f.seek(4)
        tamanho = struct.unpack('H', f.read(2))[0]
        dados = f.read(tamanho).decode('utf-8')
        assert dados.startswith("34|O Labirinto do Fauno")


def test_main_com_flag_invalida(monkeypatch, capsys):
    # deve lidar com uma flag de modo inválida
    monkeypatch.setattr(sys, 'argv', ['programa.py', '-x'])
    programa.main()
    captured = capsys.readouterr()
    assert "modo '-x' desconhecido" in captured.out


def test_main_execucao_sem_arquivo(tmp_path, monkeypatch):
    # deve criar um arquivo de dados automaticamente ao usar -e se ele não existir
    monkeypatch.chdir(tmp_path)
    ops_file = tmp_path / "ops.txt"
    ops_file.write_text("i 1|Teste")
    monkeypatch.setattr(sys, 'argv', ['programa.py', '-e', 'ops.txt'])
    assert not os.path.exists("filmes.dat")
    programa.main()
    assert os.path.exists("filmes.dat")
