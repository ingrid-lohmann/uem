import pandas as pd
import matplotlib.pyplot as plt

# Carrega o CSV
df = pd.read_csv("/content/drive/MyDrive/trabalho IA/resultados/dados_para_analise_completa.csv")

# Calcula o preço médio para cada dia relativo
medias = {
    "D-2": df["Preco_D-2"].mean(),
    "D-1": df["Preco_D-1"].mean(),
    "D0":  df["Preco_D+0"].mean(),
    "D+1": df["Preco_D+1"].mean(),
    "D+2": df["Preco_D+2"].mean()
}

# Converte para DataFrame ordenado
df_medias = pd.DataFrame({
    "Dia": ["D-2", "D-1", "D0", "D+1", "D+2"],
    "PrecoMedio": list(medias.values())
})

# Configura estilo premium
plt.figure(figsize=(14, 6))
plt.plot(df_medias["Dia"], df_medias["PrecoMedio"],
         linewidth=3,
         color="#c90076")

plt.grid(True, linestyle="--", alpha=0.25)
plt.title("Preço Médio da Ação ao Redor do Evento", fontsize=20, weight="bold")
plt.ylabel("Preço médio (R$)", fontsize=14)
plt.xlabel("Dias relativos ao evento", fontsize=14)

# Remove o spines laterais
for spine in ["top", "right"]:
    plt.gca().spines[spine].set_visible(False)

plt.tight_layout()

# 👉 SALVA O GRÁFICO
plt.savefig("/content/drive/MyDrive/trabalho IA/resultados/preco_medio_evento.png", dpi=300, bbox_inches="tight")

plt.show()
