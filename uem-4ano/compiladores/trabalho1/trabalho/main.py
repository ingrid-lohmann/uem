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
        print("✅ Programa compilado com sucesso.")
    else:
        print("❌ A compilação falhou. \nErros encontrados:")
        for erro in erros_lexicos:
            print(erro)
        for erro in erros_sintaticos:
            print(erro)
        for erro in erros_semanticos:
            print(erro)
    print("-" * 35 + "\n")


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        nome_arquivo = sys.argv[1]
        try:
            with open(nome_arquivo, 'r') as arquivo:
                codigo_fonte = arquivo.read()
                compilar_codigo(codigo_fonte, nome_arquivo)
        except FileNotFoundError:
            print(
                f"--- ERRO --- \nArquivo '{nome_arquivo}' não encontrado no diretório.\n"
            )
        except Exception as e:
            print(
                f"--- ERRO INESPERADO ao processar {nome_arquivo} --- \n{e}\n")

    else:
        print(
            "Nenhum arquivo especificado. Rodando a suíte de testes padrão...\n"
        )
        arquivos_para_testar = [
            './tascal_testes/P1.tascal', './tascal_testes/P2.tascal',
            './tascal_testes/P3.tascal', './tascal_testes/P4.tascal',
            './tascal_testes/P5.tascal', './tascal_testes/P6.tascal',
            './tascal_testes/P7.tascal', './tascal_testes/P8.tascal',
            './tascal_testes/P9.tascal', './tascal_testes/P10.tascal',
            './tascal_testes/PErr01.tascal', './tascal_testes/PErr02.tascal',
            './tascal_testes/PErr03.tascal', './tascal_testes/PErr04.tascal',
            './tascal_testes/PErr05.tascal', './tascal_testes/PErr06.tascal',
            './tascal_testes/PErr07.tascal', './tascal_testes/PErr08.tascal',
            './tascal_testes/PErr09.tascal', './tascal_testes/PErr10.tascal',
            './tascal_testes/PErr11.tascal', './tascal_testes/PErr12.tascal',
            './tascal_testes/PErr13.tascal', './tascal_testes/PErr14.tascal',
            './tascal_testes/PErr15.tascal', './tascal_testes/PErr16.tascal',
            './tascal_testes/PErr17.tascal', './tascal_testes/PErr18.tascal'
        ]

        for nome_arquivo in arquivos_para_testar:
            try:
                with open(nome_arquivo, 'r') as arquivo:
                    codigo_fonte = arquivo.read()
                    compilar_codigo(codigo_fonte, nome_arquivo)
            except FileNotFoundError:
                print(
                    f"--- ERRO --- \nArquivo de teste '{nome_arquivo}' não encontrado no diretório.\n"
                )
            except Exception as e:
                print(
                    f"--- ERRO INESPERADO ao processar {nome_arquivo} --- \n{e}\n"
                )
