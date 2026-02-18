import sys
from lexer import lexer, erros_lexicos
from parser import parser, erros_sintaticos
from analise_semantica import tabela_simbolos, erros_semanticos

def compilar_codigo(codigo_fonte, nome_arquivo=""):
    print(f"--- Compilando o arquivo: {nome_arquivo} ---")

    erros_lexicos.clear()
    erros_sintaticos.clear()
    erros_semanticos.clear()
    tabela_simbolos.clear()
    lexer.lineno = 1

    parser.parse(codigo_fonte, lexer=lexer)

    if not erros_lexicos and not erros_sintaticos and not erros_semanticos:
        print("Programa compilado com sucesso.")
    else:
        print("A compilação falhou. \nErros encontrados:")
        for erro in erros_lexicos:
            print(erro)
        for erro in erros_sintaticos:
            print(erro)
        for erro in erros_semanticos:
            print(erro)
    print("-" * 35 + "\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_para_o_arquivo.tascal>")
        sys.exit(1) 

    nome_arquivo = sys.argv[1]

    try:
        with open(nome_arquivo, 'r') as arquivo:
            codigo_fonte = arquivo.read()
            compilar_codigo(codigo_fonte, nome_arquivo)
    except FileNotFoundError:
        print(
            f"--- ERRO --- \nArquivo '{nome_arquivo}' não encontrado no diretório.\n"
        )