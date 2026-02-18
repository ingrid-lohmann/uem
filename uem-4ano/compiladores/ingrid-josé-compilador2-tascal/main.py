import sys
import os
import glob
from lexer import lexer, erros_lexicos
from parser import parser
from semantica import VerificadorSemantico
from codegen import GeradorCodigo

def compilar_arquivo(caminho_arquivo):
    nome_arquivo = os.path.basename(caminho_arquivo)
    print(f"🔹 Processando: {nome_arquivo} ...", end=" ")

    try:
        with open(caminho_arquivo, 'r') as f:
            codigo_fonte = f.read()
    except FileNotFoundError:
        print(f"\n❌ Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return

    lexer.lineno = 1
    erros_lexicos.clear()

    ast = parser.parse(codigo_fonte, lexer=lexer)

    if erros_lexicos or ast is None:
        print("❌ Falha na Análise Léxica/Sintática.")
        for erro in erros_lexicos:
            print(f"   -> {erro}")
        print("-" * 40)
        return

    verificador = VerificadorSemantico()
    verificador.visita(ast)

    if verificador.erros:
        print("❌ Falha na Análise Semântica.")
        for erro in verificador.erros:
            print(f"   -> {erro}")
        print("-" * 40)
        return

    gerador = GeradorCodigo()
    try:
        gerador.visita(ast)
        codigo_mepa = gerador.obter_codigo()

        nome_saida = os.path.splitext(caminho_arquivo)[0] + ".mep"

        with open(nome_saida, 'w') as f_out:
            f_out.write(codigo_mepa)

        print(f"✅ Sucesso! Gerado: {os.path.basename(nome_saida)}")

    except Exception as e:
        print(f"\n❌ Erro Interno na Geração de Código: {e}")
        import traceback
        traceback.print_exc()

    print("-" * 40)

def main():
    if len(sys.argv) >= 2:
        arquivo_alvo = sys.argv[1]
        compilar_arquivo(arquivo_alvo)

    else:
        print("Nenhum arquivo especificado. Rodando bateria de testes em './tascal_testes/'...\n")
        
        padrao_busca = os.path.join('.', 'testes', '*.tascal')
        arquivos = sorted(glob.glob(padrao_busca))

        if not arquivos:
            print(f"⚠️  Nenhum arquivo .tascal encontrado em '{padrao_busca}'")
            return

        for arquivo in arquivos:
            compilar_arquivo(arquivo)

if __name__ == '__main__':
    main()