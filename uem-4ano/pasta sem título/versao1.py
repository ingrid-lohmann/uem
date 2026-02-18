import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import sys
import os

def executar_correlacao_e_graficos(caminho_entrada_drive):
    print("\n--- Etapa 4: Correlação e Visualização ---")
    
    try:
        # CORREÇÃO CRÍTICA: Carregamos o arquivo EXATAMENTE como foi passado (o arquivo _SENTIMENTO.csv)
        df = pd.read_csv(caminho_entrada_drive)
    except FileNotFoundError:
        # Se o arquivo não for encontrado, tentamos a forma mais antiga (para segurança)
        try:
             caminho_sentimento_backup = caminho_entrada_drive.replace('.csv', '_SENTIMENTO.csv')
             df = pd.read_csv(caminho_sentimento_backup)
        except FileNotFoundError:
             print(f"ERRO: Arquivo de sentimento não encontrado em: {caminho_entrada_drive}")
             return

    # 1. Cálculo da Correlação de Pearson
    
    dias_offsets = [-2, -1, 0, 1, 2] 
    colunas_correlacao = [f'Variacao_D{offset:+d}' for offset in dias_offsets]
    
    resultados_correlacao = {}
    
    for coluna in colunas_correlacao:
        df_temp = df[[coluna, 'Score_Sentimento']].dropna()
        
        if len(df_temp) > 2:
            try:
                coef_pearson, p_value = pearsonr(df_temp['Score_Sentimento'], df_temp[coluna])
                resultados_correlacao[coluna] = {
                    'Pearson_r': f"{coef_pearson:.3f}",
                    'P_value': f"{p_value:.4f}",
                    'Significancia': 'SIM (<0.05)' if p_value < 0.05 else 'NÃO'
                }
            except ValueError:
                resultados_correlacao[coluna] = {'Pearson_r': 'ERRO', 'P_value': 'ERRO', 'Significancia': 'ERRO'}
        else:
            resultados_correlacao[coluna] = {'Pearson_r': 'N/A', 'P_value': 'N/A', 'Significancia': 'N/A'}

    print("\n### Coeficientes de Correlação de Pearson (Sentimento vs. Variação) ###")
    df_correlacao = pd.DataFrame.from_dict(resultados_correlacao, orient='index')
    print(df_correlacao)
    print("----------------------------------------------------------------------")
    
    
    # 2. Geração dos Gráficos de Dispersão (Visualização de Suporte)
    
    sns.set_style("whitegrid")
    
    fig, axes = plt.subplots(1, 5, figsize=(25, 5))
    fig.suptitle('Correlação entre Sentimento (FinBERT) e Variação Percentual da VALE3', fontsize=16)

    for i, offset in enumerate(dias_offsets): 
        coluna_var = f'Variacao_D{offset:+d}' 
        
        df_plot = df[[coluna_var, 'Score_Sentimento']].dropna()

        sns.regplot(x='Score_Sentimento', y=coluna_var, data=df_plot, ax=axes[i], scatter_kws={'alpha':0.6}, line_kws={"color":"red"})
        
        r_val = df_correlacao.loc[coluna_var, 'Pearson_r'] if coluna_var in df_correlacao.index else 'N/A'
        
        axes[i].set_title(f'Dia D{offset:+d} (r = {r_val})')
        axes[i].set_xlabel('Score de Sentimento (-10 a +10)')
        axes[i].set_ylabel('Variação Percentual')
        axes[i].axhline(0, color='grey', linestyle='--', linewidth=0.8)
        axes[i].axvline(0, color='grey', linestyle='--', linewidth=0.8)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Salva o gráfico
    caminho_imagem = caminho_entrada_drive.replace('.csv', '_GRAFICOS_FIM.png')
    plt.savefig(caminho_imagem)
    print(f"\n✅ Gráficos salvos em: {caminho_imagem}")
    plt.show()
    
    print("\n--- Etapa 4 Concluída: Resultados Gerados ---")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERRO: O caminho do arquivo CSV deve ser passado como argumento.")
        exit()
        
    caminho_do_csv_sentimento = sys.argv[1]
    executar_correlacao_e_graficos(caminho_do_csv_sentimento)