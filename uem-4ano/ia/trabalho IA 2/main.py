import requests
import pandas as pd
from tqdm import tqdm
from newspaper import Article
import time

# ============================================================
# 1) Função segura para pegar JSON
# ============================================================

def safe_get_json(url, params, max_retries=4):
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)

            if r.status_code != 200:
                print(f"[{attempt+1}/{max_retries}] HTTP {r.status_code}")
                time.sleep(1.5)
                continue

            try:
                return r.json()
            except:
                print(f"[{attempt+1}/{max_retries}] Resposta não é JSON:")
                print(r.text[:300])
                time.sleep(1.5)
                continue

        except Exception as e:
            print(f"[{attempt+1}/{max_retries}] Erro:", e)
            time.sleep(1.5)

    print("❌ Falha ao obter JSON após múltiplas tentativas.")
    return None


# ============================================================
# 2) Função de busca GDELT (sem domínio; filtragem .br removida)
# ============================================================

def search_gdelt(query, start_date, end_date):
    base_url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": f"({query})",
        "mode": "ArtList",
        "maxrecords": "250",
        "format": "json",
        "startdatetime": start_date + "000000",
        "enddatetime": end_date + "235959"
    }

    data = safe_get_json(base_url, params)

    if not data or "articles" not in data:
        print("⚠️ Nenhum artigo retornado.")
        return pd.DataFrame()

    return pd.DataFrame(data["articles"])


# ============================================================
# 3) BUSCA SOMENTE DE BRUMADINHO (25–29 JAN)
# ============================================================

print("\n🔍 Buscando notícias sobre Brumadinho (25–29 jan)...")
bruma_df = search_gdelt(
    query="Brumadinho OR barragem OR Vale",
    start_date="20190125",
    end_date="20190129"
)

bruma_df["categoria"] = "brumadinho"


# ============================================================
# 4) Limpeza básica
# ============================================================

def clean_df(df):
    if df.empty:
        print("⚠️ DataFrame vazio – pulando limpeza.")
        return df
    df = df.drop_duplicates(subset=["url"], keep="first")
    df = df[df["url"].notnull()]
    df = df[df["url"].str.contains("http", na=False)]
    return df.reset_index(drop=True)

bruma_df = clean_df(bruma_df)


# ============================================================
# 5) Extração de texto com Newspaper3K
# ============================================================

def extract_article(url):
    try:
        a = Article(url)
        a.download()
        a.parse()
        return a.title, a.text, a.publish_date
    except:
        return None, None, None


def enrich_with_text(df):
    if df.empty:
        return df

    titles, texts, dates = [], [], []

    for url in tqdm(df["url"], desc="Extraindo textos"):
        t, body, d = extract_article(url)
        titles.append(t)
        texts.append(body)
        dates.append(d)

    df["title_real"] = titles
    df["texto"] = texts
    df["data_real"] = dates
    return df

bruma_df = enrich_with_text(bruma_df)


# ============================================================
# 6) FILTRAR APENAS NOTÍCIAS EM INGLÊS
# ============================================================

def filter_english(df):
    if df.empty:
        return df
    return df[df["language"] == "English"].reset_index(drop=True)

bruma_df = filter_english(bruma_df)


# ============================================================
# 7) Remover títulos duplicados
# ============================================================

def drop_duplicate_titles(df):
    if df.empty:
        return df
    return df.drop_duplicates(subset=["title_real"], keep="first").reset_index(drop=True)

bruma_df = drop_duplicate_titles(bruma_df)


# ============================================================
# 8) Manter notícias que têm título, texto, data e URL
# ============================================================

def ensure_required_fields(df):
    if df.empty:
        return df

    df = df[
        df["title_real"].notnull() &
        df["texto"].notnull() &
        df["data_real"].notnull() &
        df["url"].notnull()
    ]

    # Remover textos vazios ou extremamente curtos
    df = df[df["texto"].str.len() > 50]

    return df.reset_index(drop=True)

bruma_df = ensure_required_fields(bruma_df)


# ============================================================
# 9) Limitar para 15 notícias
# ============================================================

bruma_df = bruma_df.head(15)


# ============================================================
# 10) Gerar CSV final
# ============================================================

bruma_df.to_csv("noticias_brumadinho_filtradas_2019.csv", index=False, encoding="utf-8")

print("\n🎉 CSV GERADO: noticias_brumadinho_filtradas_2019.csv")
print(f"Total de notícias finais: {len(bruma_df)}")

print("\nPrévia:")
print(bruma_df[["title_real", "data_real", "url"]].head(15))
