import subprocess
import os
import sys

PASTA_MEPA = "mepa"
SCRIPT_MEPA = os.path.join(PASTA_MEPA, "mepa_pt.py")
PASTA_TESTES = "testes"

CASOS_TESTE = {
    "P01.mep": {
        "entrada": "70\n170\n",
        "saida_esperada": "24",
        "desc": "Calculo IMC"
    },
    "P02.mep": {
        "entrada": "5\n",
        "saida_esperada": "9",
        "desc": "Expressao Aritmetica"
    },
    "P03.mep": {
        "entrada": "11\n",
        "saida_esperada": "1",
        "desc": "Numero Primo (11)"
    },
    "P04.mep": {
        "entrada": "72\n24\n",
        "saida_esperada": "3",
        "desc": "Divisao Inteira"
    },
    "P05.mep": {
        "entrada": "9\n",
        "saida_esperada": "1",
        "desc": "Maior que 5"
    },
    "P06.mep": {
        "entrada": "",
        "saida_esperada": "0",
        "desc": "Logica Booleana"
    },
    "P07.mep": {
        "entrada": "",
        "saida_esperada": "10",
        "desc": "Soma Inteiros < 5"
    },
    "P08.mep": {
        "entrada": "3\n",
        "saida_esperada": "0",
        "desc": "Verifica Par"
    },
    "P09.mep": {
        "entrada": "5\n8\n",
        "saida_esperada": "13\n40\n1",
        "desc": "Expressoes Mistas"
    },
    "P10.mep": {
        "entrada": "10\n",
        "saida_esperada": "0\n1\n1\n2\n3\n5\n8",
        "desc": "Fibonacci"
    }
}

def rodar_teste(arquivo_mep, dados, modo_detalhado):
    caminho_mep = os.path.join(PASTA_TESTES, arquivo_mep)

    if not os.path.exists(caminho_mep):
        print(f"⚠️  Arquivo {arquivo_mep} não encontrado.")
        return False

    cmd = ["python", SCRIPT_MEPA, "--progfile", caminho_mep]

    if not modo_detalhado:
        cmd.insert(2, "--silent")

    try:
        processo = subprocess.run(
            cmd,
            input=dados["entrada"],
            capture_output=True,
            text=True,
            timeout=5
        )

        stderr_output = processo.stderr
        stdout_output = processo.stdout

        saida_limpa = "\n".join([l for l in stdout_output.split('\n') if l.strip() != ''])
        esperado = dados["saida_esperada"].strip()
        passou = (saida_limpa == esperado)


        if modo_detalhado:
            print(f"\n{'='*60}")
            print(f"🛠️  Executando: {arquivo_mep}")
            print(f"{'-'*60}")

            if stderr_output:
                print(stderr_output.rstrip())

            if dados['entrada']:
                print(f"\n(Entrada Injetada):\n{dados['entrada'].strip()}")

            print("\n(Saída):")
            if stdout_output:
                print(stdout_output.rstrip())
            else:
                print("(vazio)")

            print(f"{'-'*60}")

            if passou:
                print(f"✅  {arquivo_mep}: PASSOU ({dados['desc']})")
            else:
                print(f"❌  {arquivo_mep}: FALHOU ({dados['desc']})")
                print(f"    Esperado: {esperado.replace(chr(10), ' ')}")
                print(f"    Recebido: {saida_limpa.replace(chr(10), ' ')}")

        else:
            if passou:
                print(f"✅ {arquivo_mep}: PASSOU ({dados['desc']})")
            else:
                print(f"❌ {arquivo_mep}: FALHOU ({dados['desc']})")
                print(f"   --> Esperado:\n{esperado}")
                print(f"   --> Recebido:\n{saida_limpa}")

        return passou

    except subprocess.TimeoutExpired:
        print(f"⏰ {arquivo_mep}: TIMEOUT (Loop infinito?)")
        return False
    except Exception as e:
        print(f"💥 Erro ao executar {arquivo_mep}: {e}")
        return False

def main():
    modo_detalhado = "-d" in sys.argv

    if not modo_detalhado:
        print("🚀 Iniciando Testes (Modo Compacto) - Use '-d' para detalhado\n")
    else:
        print("🚀 Iniciando Testes (Modo Detalhado)\n")

    sucessos = 0
    total = len(CASOS_TESTE)

    for arquivo, dados in CASOS_TESTE.items():
        if rodar_teste(arquivo, dados, modo_detalhado):
            sucessos += 1

    print("\n" + "=" * 40)
    print(f"📊 Resultado Final: {sucessos}/{total} testes passaram.")

if __name__ == "__main__":
    main()