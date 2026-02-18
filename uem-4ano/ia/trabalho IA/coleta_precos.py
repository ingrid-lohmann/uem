import pandas as pd
import yfinance as yf
from datetime import timedelta, datetime

# Define o ticker da Vale na B3
TICKER = "VALE3.SA"


def calcular_variacao(preco_anterior, preco_atual):
    """Calcula a variação percentual: (Atual - Anterior) / Anterior * 100"""
    # A correção: Garante que os valores sejam float para evitar o erro 'ValueError'
    if preco_anterior is None or preco_anterior == 0 or pd.isna(
            preco_anterior):
        return 0.0
    return ((preco_atual - preco_anterior) / preco_anterior) * 100.0


def coletar_e_alinhar_precos(nome_arquivo_noticias: str):
    print("--- Iniciando Etapa 2: Coleta e Alinhamento de Preços ---")

    # 1. Carregar Notícias e Limpeza de Datas
    df_noticias = pd.read_csv(nome_arquivo_noticias)
    df_noticias['data'] = pd.to_datetime(df_noticias['data'])

    # CRÍTICO: Filtra notícias com data futura ou na data atual
    data_limite_download = datetime.now() - timedelta(days=1)
    df_noticias = df_noticias[df_noticias['data'] < data_limite_download]

    if df_noticias.empty:
        print(
            "ERRO: Nenhuma notícia válida (data anterior a hoje) encontrada. Verifique o CSV."
        )
        return None

    # CRÍTICO: FORÇA A DATA DE INÍCIO ANTES DA PRIMEIRA TRAGÉDIA (Mariana, 2015)
    data_inicio_fixa = datetime(2015, 1, 1)
    data_fim = data_limite_download

    # 2. Baixar Dados Históricos (yfinance)
    print(
        f"Baixando dados históricos de {TICKER} ({data_inicio_fixa.strftime('%Y-%m-%d')} a {data_fim.strftime('%Y-%m-%d')})..."
    )

    dados_acoes = yf.download(TICKER,
                              start=data_inicio_fixa,
                              end=data_fim,
                              progress=False,
                              auto_adjust=False)

    if dados_acoes.empty:
        print(
            "ERRO: yfinance retornou um DataFrame vazio. Não foi possível baixar os dados."
        )
        return None

    # 3. Mapeamento de Coluna
    if 'Adj Close' in dados_acoes.columns:
        coluna_preco = 'Adj Close'
    elif 'Close' in dados_acoes.columns:
        coluna_preco = 'Close'
    else:
        print(
            "ERRO: Colunas de preço (Adj Close ou Close) não encontradas no DataFrame."
        )
        return None

    # 4. Processamento de Preços e Variação
    colunas_variacao = []

    for index, row in df_noticias.iterrows():
        data_noticia = row['data']
        dados_linha = {}

        dias_offset = [-2, -1, 0, 1, 2]

        for offset in dias_offset:
            data_offset = data_noticia + timedelta(days=offset)

            # Buscamos o preço do dia D+offset e do dia anterior
            preco_hoje = None
            preco_anterior = None

            try:
                # Localiza o preço do dia de pregão mais próximo ou exato
                data_hoje_pregão = dados_acoes.index[dados_acoes.index >=
                                                     data_offset][0]
                # Pega o valor nativo do Python (float) para evitar o erro 'ValueError'
                preco_hoje = dados_acoes.loc[data_hoje_pregão,
                                             coluna_preco].item()

                # Localiza o preço de fechamento do dia de pregão ANTERIOR
                data_anterior_pregão = dados_acoes.index[dados_acoes.index <
                                                         data_hoje_pregão][-1]
                preco_anterior = dados_acoes.loc[data_anterior_pregão,
                                                 coluna_preco].item()

            except IndexError:
                # Índice fora do limite (início/fim do DataFrame)
                pass
            except KeyError:
                # Data não encontrada
                pass

            # A função calcula_variacao agora está protegida contra o erro de ambiguidade
            var_offset = calcular_variacao(preco_anterior, preco_hoje)

            # Adiciona ao dicionário com nome claro
            dados_linha[f'Preco_D{offset:+d}'] = preco_hoje
            dados_linha[f'Variacao_D{offset:+d}'] = var_offset

        colunas_variacao.append(dados_linha)

    # 5. Mesclar com as Notícias e Salvar
    df_variacao = pd.DataFrame(colunas_variacao)
    # Resetamos o índice da notícia e fazemos o concat
    df_final = pd.concat([df_noticias.reset_index(drop=True), df_variacao],
                         axis=1)

    nome_saida = "dados_para_analise_completa.csv"
    df_final.to_csv(nome_saida, index=False)

    print("\n--- Etapa 2 Concluída com Sucesso! ---")
    print(f"Arquivo de saída: {nome_saida}")
    print("Próximo passo: Análise de Sentimento (BERT).")

    return df_final.head()


if __name__ == "__main__":
    coletar_e_alinhar_precos("noticias_vale_4_fases_final.csv")
