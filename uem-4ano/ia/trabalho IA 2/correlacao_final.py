import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from scipy.stats import ConstantInputWarning
import sys
import os
import warnings
from datetime import timedelta, datetime

# Suprime o aviso de input constante (que ocorre quando a variação é zero)
warnings.simplefilter('ignore', ConstantInputWarning)


def plotar_5_graficos(df_subset, evento_nome, df_correlacao, caminho_base):
    """Gera um painel de 5 gráficos (D-2 a D+2) para um evento específico."""
    
    dias_offsets = [-2, -1, 0, 1, 2] 
    
    fig, axes = plt.subplots(1, 5, figsize=(25, 6)) 
    
    fig.suptitle(f'Correlação {evento_nome}: Sentimento (FinBERT) vs. Variação Percentual da VALE3', fontsize=16)

    for i, offset in enumerate(dias_offsets): 
        # CRÍTICO: Mapeamento do nome da coluna real do CSV para o plot (ex: Variacao_D+0)
        if offset == 0:
            coluna_var = 'Variacao_D+0'
        elif offset > 0:
            coluna_var = f'Variacao_D+{offset}' 
        else: # offset < 0
            coluna_var = f'Variacao_D{offset}' 
        
        # O nome usado para a correlação (Pearson_r) é sempre Variacao_D+0, Variacao_D+1, etc.
        coluna_corr_df = f'Variacao_D{offset:+d}'


        df_plot = df_subset[[coluna_var, 'Score_Sentimento', 'evento_fase']].dropna(subset=[coluna_var]) 

        # Plota os pontos coloridos
        sns.scatterplot(x='Score_Sentimento', y=coluna_var, hue='evento_fase', data=df_plot, ax=axes[i], alpha=0.7)
        
        # Opcional: Plota a linha de regressão geral para o subset (em preto)
        sns.regplot(
    x='Score_Sentimento', 
    y=coluna_var, 
    data=df_plot, 
    ax=axes[i], 
    scatter=False, 
    line_kws={"color":"red", "linestyle":"-", "linewidth":2}, # Linha vermelha sólida
    color="lightcoral", # Cor para a área de confiança (tom de rosa)
    ci=95 # Mostra o intervalo de confiança de 95%
)

        # Adiciona o coeficiente 'r' ao título
        r_val = df_correlacao.loc[coluna_corr_df, 'Pearson_r'] if coluna_corr_df in df_correlacao.index else 'N/A'
        
        # Corrige o título do eixo X
        axes[i].set_title(f'Dia D{offset:+d} (r = {r_val})')
        axes[i].set_xlabel('Score de Sentimento (-10 a +10)')
        axes[i].set_ylabel('Variação Percentual')
        axes[i].axhline(0, color='grey', linestyle='--', linewidth=0.8)
        axes[i].axvline(0, color='grey', linestyle='--', linewidth=0.8)
        
        # Remove a legenda de todos os subplots, exceto o último
        if i < 4:
            axes[i].get_legend().remove()
        
        # Garante que a legenda final seja exibida apenas uma vez
        if i == 4 and axes[i].legend_ != None:
            axes[i].legend(title="Evento", loc='upper right')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # CORREÇÃO CRÍTICA DO SALVAMENTO: Usa os.path.splitext para garantir a extensão .png
    base, _ = os.path.splitext(caminho_base)
    caminho_imagem = f'{base}_{evento_nome.upper()}_GRAFICOS_FIM.png'
    
    plt.savefig(caminho_imagem)
    print(f"\n✅ Gráficos de {evento_nome} salvos em: {caminho_imagem}")
    plt.show() 
    return

def executar_correlacao_e_graficos(caminho_entrada_csv):
    print("\n--- Etapa 4: Correlação e Visualização ---")
    
    try:
        df = pd.read_csv(caminho_entrada_csv)
    except FileNotFoundError:
        print(f"ERRO: Arquivo de sentimento não encontrado em: {caminho_entrada_csv}")
        return
        
    # CRÍTICO: RENOMEAR 'categoria' para 'evento_fase' (para fins de plotagem)
    if 'categoria' in df.columns:
        df = df.rename(columns={'categoria': 'evento_fase'})
    elif 'evento_fase' not in df.columns:
        df['evento_fase'] = 'Brumadinho'

    # 1. CÁLCULO DA CORRELAÇÃO GERAL
    dias_offsets = [-2, -1, 0, 1, 2] 
    
    # Mapeamento de nomes de colunas do DataFrame (CSV) para o cálculo (loop)
    # Note: 'Variacao_D+0' é o nome da coluna no CSV. 'Variacao_D+0' é o nome na tabela de resultados.
    colunas_csv = ['Variacao_D-2', 'Variacao_D-1', 'Variacao_D+0', 'Variacao_D+1', 'Variacao_D+2']
    colunas_correlacao = [f'Variacao_D{offset:+d}' for offset in dias_offsets]
    
    resultados_correlacao = {}
    
    for nome_loop, nome_csv in zip(colunas_correlacao, colunas_csv):
        # Garante que apenas os dias com dados de sentimento E variação sejam usados
        if nome_csv not in df.columns:
             print(f"AVISO: Coluna {nome_csv} ausente no CSV. Ignorando cálculo.")
             continue
             
        df_temp = df[[nome_csv, 'Score_Sentimento']].dropna()
        
        # CRÍTICO: Testa se a coluna tem valores constantes (evita o ConstantInputWarning)
        if len(df_temp) > 2 and df_temp[nome_csv].nunique() > 1: 
            try:
                # O cálculo usa a coluna do CSV (nome_csv)
                coef_pearson, p_value = pearsonr(df_temp['Score_Sentimento'], df_temp[nome_csv])
                resultados_correlacao[nome_loop] = {
                    'Pearson_r': f"{coef_pearson:.3f}",
                    'P_value': f"{p_value:.4f}",
                    'Significancia': 'SIM (<0.05)' if p_value < 0.05 else 'NÃO'
                }
            except ValueError:
                # Caso de falha de cálculo (ex: todas as colunas NaN)
                 resultados_correlacao[nome_loop] = {'Pearson_r': 'nan', 'P_value': 'nan', 'Significancia': 'NÃO'}
        else:
            # Caso em que o input é constante (ConstantInputWarning)
             resultados_correlacao[nome_loop] = {'Pearson_r': 'nan', 'P_value': 'nan', 'Significancia': 'NÃO'}

    print("\n### Coeficientes de Correlação de Pearson (Sentimento vs. Variação) ###")
    df_correlacao = pd.DataFrame.from_dict(resultados_correlacao, orient='index')
    print(df_correlacao)
    print("----------------------------------------------------------------------")

    # 2. PLOTAGEM DO EVENTO BRUMADINHO (DataFrame completo)
    plotar_5_graficos(df, "Brumadinho", df_correlacao, caminho_entrada_csv)
    
    print("\n--- Etapa 4 Concluída: Estudo de Caso de Brumadinho Gerado ---")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERRO: O caminho completo do arquivo CSV de sentimento deve ser passado como argumento.")
        sys.exit(1)
        
    caminho_do_csv_sentimento = sys.argv[1]
    executar_correlacao_e_graficos(caminho_do_csv_sentimento)