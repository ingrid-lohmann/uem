import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os


def plotar_correlacao_tempo_acao(df, caminho_base):
    """
    Converte colunas Variacao_D-2 a Variacao_D+2 em um gráfico temporal
    com regressão linear, comparando dia relativo ao evento vs variação da ação.
    """

    # Mapeamento das colunas conforme o CSV
    colunas = {
        -2: 'Variacao_D-2',
        -1: 'Variacao_D-1',
        0:  'Variacao_D+0',
        1:  'Variacao_D+1',
        2:  'Variacao_D+2'
    }

    dias = []
    valores = []

    # Extrai pares (dia, valor)
    for dia, col in colunas.items():
        if col in df.columns:
            serie = df[col].dropna()
            for v in serie.values:
                dias.append(dia)
                valores.append(v)

    if len(dias) == 0:
        print("❌ Nenhum dado válido para gerar o gráfico.")
        return

    # Converte para arrays NumPy
    dias = np.array(dias)
    valores = np.array(valores)

    # Gráfico
    plt.figure(figsize=(12, 6))
    plt.scatter(dias, valores, s=80, label="Dados")

    # Linha de regressão
    coef = np.polyfit(dias, valores, 1)
    poly = np.poly1d(coef)

    dias_linha = np.linspace(min(dias), max(dias), 100)
    plt.plot(dias_linha, poly(dias_linha), linewidth=2, label="Regressão linear")

    plt.title("Correlação entre Dia do Evento e Variação da Ação")
    plt.xlabel("Dia relativo ao evento (D)")
    plt.ylabel("Variação da ação (%)")
    plt.grid(True)
    plt.legend()

    # Nome do arquivo
    nome_saida = caminho_base.replace(".csv", "_correlacao_tempo.png")
    plt.savefig(nome_saida, dpi=300)
    plt.show()

    print(f"✅ Gráfico salvo em: {nome_saida}")


def executar_grafico(caminho_csv):
    """
    Carrega o CSV e gera o gráfico.
    """
    if not os.path.exists(caminho_csv):
        print(f"❌ Arquivo não encontrado: {caminho_csv}")
        return

    df = pd.read_csv(caminho_csv)
    plotar_correlacao_tempo_acao(df, caminho_csv)


# Execução via linha de comando ou import
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python correlacao_tempo_acao.py arquivo.csv")
    else:
        executar_grafico(sys.argv[1])
