from lexer import lexer
from parser import parser, tabela_simbolos, erros_sintaticos, erros_semanticos

def compilar_codigo(codigo_fonte, nome_arquivo=""):
    """
    Função que executa o processo de compilação para um dado código-fonte.
    """
    print(f"--- Compilando o arquivo: {nome_arquivo} ---")

    erros_sintaticos.clear()
    erros_semanticos.clear()
    tabela_simbolos.clear()
    lexer.lineno = 1

    parser.parse(codigo_fonte, lexer=lexer)

    if not erros_sintaticos and not erros_semanticos:
        print("Programa compilado com sucesso.")
    else:
        print("A compilação falhou. Erros encontrados:")
        for erro in erros_sintaticos:
            print(erro)
        for erro in erros_semanticos:
            print(erro)
    print("-" * 35 + "\n")

if __name__ == '__main__':
    arquivos_para_testar = ['./exemplos/ok.calc', './exemplos/error.calc']

    for nome_arquivo in arquivos_para_testar:
        try:
            with open(nome_arquivo, 'r') as arquivo:
                codigo_fonte = arquivo.read()
                compilar_codigo(codigo_fonte, nome_arquivo)
        except FileNotFoundError:
            print(f"--- ERRO --- \nArquivo '{nome_arquivo}' não encontrado no diretório.\n")