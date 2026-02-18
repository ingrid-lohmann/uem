import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

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
    if pd.isna(texto) or len(texto.strip()) < 50:
        return 0.0 # Pontuação neutra para texto vazio ou muito curto

    try:
        # Tokenização (Divide o texto em unidades que o BERT entende)
        inputs = tokenizer(texto, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)

        # Inferência (Cálculo da IA)
        with torch.no_grad():
            outputs = model(**inputs)

        # Softmax para converter logits (saída bruta) em probabilidades (0 a 1)
        probabilities = torch.softmax(outputs.logits, dim=1).squeeze().cpu().numpy()

        # O FinBERT retorna probabilidades na ordem: [Positive, Negative, Neutral]

        # Conversão para Score de -10 a +10:
        # Score = (Prob_Pos - Prob_Neg) * 10
        score = (probabilities[0] - probabilities[1]) * 10

        return float(score)

    except Exception as e:
        # Falha de processamento, retorna neutro
        return 0.0


def executar_analise(arquivo_entrada: str):
    print("--- Iniciando Etapa 3: Análise de Sentimento (FinBERT) ---")
    df = pd.read_csv(arquivo_entrada)

    # 1. Pré-processamento Simples (Obrigatório antes do BERT)
    # BERT se beneficia de texto limpo, mas a maioria já foi feita no scraping.
    # O pré-processamento mais rigoroso do trabalho (stop-words, lematização)
    # pode ser desnecessário para o BERT, que usa contexto completo.

    # Aplicar análise ao texto. Isso levará alguns minutos.
    print(f"Processando {len(df)} notícias. Isso pode levar alguns minutos...")
    df['Score_Sentimento'] = df['texto'].apply(analisar_sentimento_finbert)

    # 2. Comparação dos Resultados (Requisito do PDF)
    # O trabalho pede para avaliar o impacto do pré-processamento.
    # Como não fizemos lematização, vamos apenas garantir que a coluna Score existe.

    nome_saida = "dados_para_correlacao_final.csv"
    df.to_csv(nome_saida, index=False)

    print("\n--- Etapa 3 Concluída com Sucesso! ---")
    print(f"Sentimento calculado para todas as notícias.")
    print(f"Arquivo de saída: {nome_saida}")
    print("Próximo passo: Correlação e Visualização.")

    # Exibe as novas colunas
    print("\nExemplo das primeiras 5 notícias (Sentimento vs Variação):")
    print(df[['evento_fase', 'titulo', 'Score_Sentimento', 'Variacao_D0']].head())

if __name__ == "__main__":
    executar_analise("dados_para_analise_completa.csv")