import sys
import os 
import pandas as pd
import yfinance as yf
from datetime import timedelta, datetime, timezone

# Define o ticker da Vale na B3
TICKER = "VALE3.SA"


def calcular_variacao(preco_anterior, preco_atual):
    """Calcula a variação percentual: (Atual - Anterior) / Anterior * 100"""
    if preco_anterior is None or preco_anterior == 0 or pd.isna(
            preco_anterior):
        return 0.0
    return ((preco_atual - preco_atual) / preco_anterior) * 100.0


def coletar_e_alinhar_precos(nome_arquivo_noticias: str):
    print("--- Iniciando Etapa 2: Coleta e Alinhamento de Preços ---")

    # 1. Carregar Notícias e Limpeza de Datas
    df_noticias = pd.read_csv(nome_arquivo_noticias)
    
    # CRÍTICO V3: Converte para datetime, usando 'data_real', e força o UTC=True
    df_noticias['data'] = pd.to_datetime(df_noticias['data_real'], format='mixed', utc=True)

    # CRÍTICO: data_limite_download agora é UTC-aware para comparação consistente
    data_limite_download = datetime.now(timezone.utc) - timedelta(days=1)
    
    df_noticias = df_noticias[df_noticias['data'] < data_limite_download]

    if df_noticias.empty:
        print(
            "AVISO: Nenhuma notícia válida (data anterior a hoje) encontrada ou o DataFrame de notícias está vazio."
        )
        return None

    # CRÍTICO: FORÇA A DATA DE INÍCIO ANTES DA TRAGÉDIA (Mariana, 2015)
    data_inicio_fixa = datetime(2015, 1, 1)
    data_fim = data_limite_download.replace(tzinfo=None) 

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

    # 3. Mapeamento de Coluna (Mantido)
    if 'Adj Close' in dados_acoes.columns:
        coluna_preco = 'Adj Close'
    elif 'Close' in dados_acoes.columns:
        coluna_preco = 'Close'
    else:
        print(
            "ERRO: Colunas de preço (Adj Close ou Close) não encontradas no DataFrame."
        )
        return None
        
    # CRÍTICO: ADICIONAR COLUNA AUXILIAR DE VARIAÇÃO DIÁRIA (Pode simplificar o cálculo)
    dados_acoes['Variacao_Diaria'] = dados_acoes[coluna_preco].pct_change() * 100

    # 4. Processamento de Preços e Variação
    colunas_variacao = []

    for index, row in df_noticias.iterrows():
        # Data naive da notícia para comparação com o índice de dados_acoes
        data_noticia = row['data'].tz_localize(None).normalize()
        dados_linha = {}

        dias_offset = [-2, -1, 0, 1, 2]

        for offset in dias_offset:
            data_offset = data_noticia + timedelta(days=offset)

            preco_hoje = None
            var_offset = 0.0
            
            # --- LÓGICA DE BUSCA DE PREÇO CORRIGIDA ---
            try:
                # 1. Localiza o primeiro dia de pregão >= data_offset
                data_hoje_pregão = dados_acoes.index[dados_acoes.index >= data_offset][0]
                
                # 2. Localiza o dia de pregão imediatamente anterior para cálculo da variação
                # Este é o ponto mais crítico e propenso a falhas, vamos simplificá-lo
                
                # CRÍTICO: Se data_offset é o dia da notícia, queremos a variação desse dia
                # Para obter a variação de um dia específico (D), olhamos para a variação percentual
                # que já calculamos na coluna 'Variacao_Diaria'
                
                # Se for o dia D, D+1, D+2, estamos interessados na variação do pregão nesse dia
                
                # Preço de hoje
                preco_hoje = dados_acoes.loc[data_hoje_pregão, coluna_preco].item()
                
                # Variação: a variação diária do dia de pregão encontrado
                var_offset = dados_acoes.loc[data_hoje_pregão, 'Variacao_Diaria'].item()
                
                # O problema é que a variação diária compara D com D-1. O trabalho pedia para
                # observar a variação de preços, que é o que essa coluna já faz.
                # A variação é o impacto no preço do fechamento em data_hoje_pregão
                # em relação ao fechamento anterior.
                
                
                # Se a variação diária for NaN (primeiro dia de pregão), definimos como 0.0
                if pd.isna(var_offset):
                    var_offset = 0.0
                

            except IndexError:
                # Se não encontrar o dia (fora do range), define como None/0.0
                preco_hoje = None
                var_offset = 0.0
            except KeyError:
                # Se a data não estiver no índice de ações
                preco_hoje = None
                var_offset = 0.0
            except Exception as e:
                # Outros erros (ex: .item() em série vazia)
                # print(f"Erro ao buscar preço para {data_offset}: {e}")
                preco_hoje = None
                var_offset = 0.0
            # --- FIM DA LÓGICA DE BUSCA DE PREÇO CORRIGIDA ---

            # CRÍTICO: Garantir que as chaves sejam criadas SEMPRE
            dados_linha[f'Preco_D{offset:+d}'] = preco_hoje
            dados_linha[f'Variacao_D{offset:+d}'] = var_offset
            

        colunas_variacao.append(dados_linha)

    # 5. Mesclar com as Notícias e Salvar
    df_variacao = pd.DataFrame(colunas_variacao)
    
    # CRÍTICO: Usar reset_index(drop=True) para garantir a concatenação correta
    df_final = pd.concat([df_noticias.reset_index(drop=True), df_variacao.reset_index(drop=True)],
                         axis=1)

    nome_saida = "dados_para_analise_completa.csv"
    
    # Usa o diretório do arquivo de entrada para salvar (garante que está no Drive)
    diretorio_saida = os.path.dirname(nome_arquivo_noticias)
    caminho_saida = os.path.join(diretorio_saida, nome_saida)
    
    df_final.to_csv(caminho_saida, index=False)

    print("\n--- Etapa 2 Concluída com Sucesso! ---")
    print(f"Arquivo de saída salvo em: {caminho_saida}")
    print("Próximo passo: Análise de Sentimento (BERT).")

    return df_final.head()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERRO: O caminho completo do arquivo CSV de notícias deve ser passado como argumento.")
        sys.exit(1)
    
    # O argumento 1 é o caminho completo do CSV de notícias (ex: '/content/drive/.../noticias_brumadinho_filtradas_2019.csv')
    caminho_do_csv_de_entrada = sys.argv[1]
    coletar_e_alinhar_precos(caminho_do_csv_de_entrada)