import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sys
import os 

# --- CONFIGURAÇÃO DO MODELO FINBERT ---
MODEL_NAME = "ProsusAI/finbert" 

# O BERT usa uma GPU ou CPU para calcular. No Replit, será CPU.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device)

def analisar_sentimento_finbert(texto: str) -> float:
    """
    Processa o texto usando o FinBERT e retorna uma pontuação de -10 a +10.
    """
    if pd.isna(texto) or len(str(texto).strip()) < 50:
        return 0.0 # Pontuação neutra para texto vazio ou muito curto

    try:
        inputs = tokenizer(texto, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)

        with torch.no_grad():
            outputs = model(**inputs)

        probabilities = torch.softmax(outputs.logits, dim=1).squeeze().cpu().numpy()

        # Score = (Prob_Pos - Prob_Neg) * 10
        score = (probabilities[0] - probabilities[1]) * 10

        return float(score)

    except Exception as e:
        return 0.0


def executar_analise(caminho_entrada: str):
    print("--- Iniciando Etapa 3: Análise de Sentimento (FinBERT) ---")
    
    # CRÍTICO: Carrega o arquivo usando o caminho completo do Drive
    df = pd.read_csv(caminho_entrada)

    print(f"Processando {len(df)} notícias. Isso pode levar alguns minutos...")
    df['Score_Sentimento'] = df['texto'].apply(analisar_sentimento_finbert)

    # CRÍTICO: Define o caminho de saída completo no Drive, usando o diretório do arquivo de entrada
    diretorio_saida = os.path.dirname(caminho_entrada)
    nome_saida = "dados_para_correlacao_final.csv"
    caminho_saida = os.path.join(diretorio_saida, nome_saida)
    
    df.to_csv(caminho_saida, index=False)

    print("\n--- Etapa 3 Concluída com Sucesso! ---")
    print(f"Sentimento calculado para todas as notícias.")
    print(f"Arquivo de saída salvo em: {caminho_saida}")
    print("Próximo passo: Correlação e Visualização.")

    # CRÍTICO: CORREÇÃO DOS NOMES DAS COLUNAS para evitar KeyError
    print("\nExemplo das primeiras 5 notícias (Sentimento vs Variação):")
    # Colunas corretas: 'categoria', 'title_real', 'Score_Sentimento', 'Variacao_D+0'
    print(df[['categoria', 'title_real', 'Score_Sentimento', 'Variacao_D+0']].head())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERRO: O caminho completo do arquivo CSV de entrada deve ser passado como argumento.")
        sys.exit(1)
    else:
        # Usa o argumento passado (que deve ser o caminho completo do Drive)
        caminho_do_csv_de_entrada = sys.argv[1]
        executar_analise(caminho_do_csv_de_entrada)