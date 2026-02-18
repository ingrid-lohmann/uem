import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import sys
import os

def plotar_5_graficos(df_subset, evento_nome, df_correlacao, caminho_base):
    """Gera um painel de 5 gráficos (D-2 a D+2) para um evento específico."""
    
    # O df_subset agora contém apenas os dados de Brumadinho
    dias_offsets = [-2, -1, 0, 1, 2] 
    
    # Criamos a figura e os 5 subplots
    fig, axes = plt.subplots(1, 5, figsize=(25, 6)) 
    
    # Ajusta o título para refletir que a análise é apenas sobre Brumadinho
    fig.suptitle(f'Correlação {evento_nome}: Sentimento (FinBERT) vs. Variação Percentual da VALE3', fontsize=16)

    for i, offset in enumerate(dias_offsets): 
        coluna_var = f'Variacao_D{offset:+d}' 
        
        # Filtra os dados apenas para as colunas necessárias e remove NaNs
        # Utilizamos 'evento_fase' que será a coluna renomeada ('categoria')
        df_plot = df_subset[[coluna_var, 'Score_Sentimento', 'evento_fase']].dropna() 

        # Plota os pontos coloridos
        # O 'hue' usará a única categoria existente ('brumadinho')
        sns.scatterplot(x='Score_Sentimento', y=coluna_var, hue='evento_fase', data=df_plot, ax=axes[i], alpha=0.7)
        
        # Opcional: Plota a linha de regressão geral para o subset (em preto)
        sns.regplot(x='Score_Sentimento', y=coluna_var, data=df_plot, ax=axes[i], scatter=False, line_kws={"color":"black", "linestyle":"--", "linewidth":1})

        # Adiciona o coeficiente 'r' ao título
        r_val = df_correlacao.loc[coluna_var, 'Pearson_r'] if coluna_var in df_correlacao.index else 'N/A'
        
        # Corrige o título do eixo X
        axes[i].set_title(f'Dia D{offset:+d} (r = {r_val})')
        axes[i].set_xlabel('Score de Sentimento (-10 a +10)')
        axes[i].set_ylabel('Variação Percentual')
        axes[i].axhline(0, color='grey', linestyle='--', linewidth=0.8)
        axes[i].axvline(0, color='grey', linestyle='--', linewidth=0.8)
        
        # Remove a legenda de todos os subplots, exceto o último, para limpar
        if i < 4:
            axes[i].get_legend().remove()
        
        # Garante que a legenda final seja exibida apenas uma vez
        if i == 4 and axes[i].legend_ != None:
            axes[i].legend(title="Evento", loc='upper right')


    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # SALVA CORRETAMENTE: Usando um nome específico para o evento
    caminho_imagem = caminho_base.replace('_FINAL.csv', f'_{evento_nome.upper()}_GRAFICOS_FIM.png')
    plt.savefig(caminho_imagem)
    print(f"\n✅ Gráficos de {evento_nome} salvos em: {caminho_imagem}")
    plt.show()
    return

def executar_correlacao_e_graficos(caminho_entrada_csv):
    print("\n--- Etapa 4: Correlação e Visualização ---")
    
    # O nome de entrada deve ser 'dados_para_correlacao_final.csv' gerado pelo analise_sentimento.py
    try:
        df = pd.read_csv(caminho_entrada_csv)
    except FileNotFoundError:
        print(f"ERRO: Arquivo de sentimento não encontrado em: {caminho_entrada_csv}")
        return
        
    # CRÍTICO: RENOMEAR 'categoria' para 'evento_fase'
    # Esta coluna foi criada no 'coletar_noticias.py' como 'categoria' e é usada
    # no plotar_5_graficos como 'evento_fase' (parâmetro hue do seaborn)
    if 'categoria' in df.columns:
        df = df.rename(columns={'categoria': 'evento_fase'})
    elif 'evento_fase' not in df.columns:
        print("AVISO: Coluna 'categoria' ou 'evento_fase' não encontrada. A plotagem de cores pode falhar.")
        # Se nenhuma for encontrada, cria uma neutra para evitar erro
        df['evento_fase'] = 'Brumadinho'

    # 1. CÁLCULO DA CORRELAÇÃO GERAL
    dias_offsets = [-2, -1, 0, 1, 2] 
    colunas_correlacao = [f'Variacao_D{offset:+d}' for offset in dias_offsets]
    resultados_correlacao = {}
    
    for coluna in colunas_correlacao:
        # Garante que apenas os dias com dados de sentimento E variação sejam usados
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

    print("\n### Coeficientes de Correlação de Pearson (Sentimento vs. Variação) ###")
    df_correlacao = pd.DataFrame.from_dict(resultados_correlacao, orient='index')
    print(df_correlacao)
    print("----------------------------------------------------------------------")

    # 2. PLOTAGEM DO EVENTO BRUMADINHO (DataFrame completo)
    
    # Como o escopo é apenas Brumadinho, passamos o DataFrame completo 'df'
    # O 'caminho_entrada_csv' é usado como caminho base para salvar a imagem
    plotar_5_graficos(df, "Brumadinho", df_correlacao, caminho_entrada_csv)
    
    print("\n--- Etapa 4 Concluída: Estudo de Caso de Brumadinho Gerado ---")

if __name__ == '__main__':
    # Modificando a chamada para usar o nome do arquivo gerado pelo analise_sentimento.py
    caminho_do_csv_sentimento = "dados_para_correlacao_final.csv" 
    executar_correlacao_e_graficos(caminho_do_csv_sentimento)