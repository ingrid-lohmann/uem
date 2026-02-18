from GoogleNews import GoogleNews
from newspaper import Article, Config
import pandas as pd
import dateparser
import time
import re

# Configuração de "Disfarce" para evitar bloqueios
config_navegador = Config()
config_navegador.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
config_navegador.request_timeout = 10

def limpar_url_google(url_suja):
    url_limpa = re.sub(r'&ved=.*', '', url_suja)
    url_limpa = re.sub(r'&usg=.*', '', url_limpa)
    return url_limpa

def buscar_por_janelas():
    # Definição das 4 Janelas Históricas (Data Inicial, Data Final, Tópico Principal)
    janelas = [
        # JANELA 1: Mariana (Tragédia em 05/11/2015)
        {'inicio': '10/25/2015', 'fim': '11/20/2015', 'termo': 'Vale barragem Mariana', 'evento': 'Mariana_2015'},

        # JANELA 2: Brumadinho (Tragédia em 25/01/2019)
        {'inicio': '01/15/2019', 'fim': '02/15/2019', 'termo': 'Vale barragem Brumadinho', 'evento': 'Brumadinho_2019'},

        # JANELA 3: Acordo Brumadinho (Assinado em 04/02/2021)
        {'inicio': '01/25/2021', 'fim': '02/15/2021', 'termo': 'Vale acordo Brumadinho', 'evento': 'Acordo_Brumadinho_2021'},

        # JANELA 4: Acordo Mariana (Assinado em 25/10/2024)
        {'inicio': '10/15/2024', 'fim': '11/15/2024', 'termo': 'Vale acordo Mariana repactuação', 'evento': 'Acordo_Mariana_2024'}
    ]

    noticias_coletadas = []

    for janela in janelas:
        print(f"\n--- Buscando Janela: {janela['evento']} ({janela['inicio']} a {janela['fim']}) ---")

        # Configura o GoogleNews com as datas específicas
        gnews = GoogleNews(lang='pt', region='BR', start=janela['inicio'], end=janela['fim'])
        gnews.search(janela['termo'])

        # Tenta pegar até 3 páginas para garantir volume
        for p in range(1, 4):
            gnews.get_page(p)
            time.sleep(1) # Respira para não bloquear

        resultados = gnews.results()
        print(f"Links encontrados na busca: {len(resultados)}")

        count_janela = 0
        for item in resultados:
            if count_janela >= 5: # Limite de 5 notícias boas por janela (total 20)
                break

            conteudo = processar_noticia(item['link'])
            if conteudo:
                conteudo['evento_fase'] = janela['evento'] # Marca qual fase pertence
                # Tenta usar data do Google se o newspaper falhar
                if not conteudo['data']:
                    conteudo['data'] = item.get('date')

                noticias_coletadas.append(conteudo)
                count_janela += 1
                print(f"✅ [{janela['evento']}] Salvo: {conteudo['titulo'][:40]}...")

        gnews.clear()

    return noticias_coletadas

def processar_noticia(url):
    try:
        url = limpar_url_google(url)
        article = Article(url, config=config_navegador)
        article.download()
        article.parse()

        if len(article.text) < 300: return None

        data_pub = article.publish_date
        data_str = data_pub.strftime('%Y-%m-%d') if data_pub else None

        return {
            "titulo": article.title,
            "texto": article.text,
            "url": url,
            "data": data_str
        }
    except:
        return None

if __name__ == "__main__":
    dados = buscar_por_janelas()

    if dados:
        df = pd.DataFrame(dados)
        # Limpeza final de datas
        df['data'] = pd.to_datetime(df['data'], errors='coerce').dt.strftime('%Y-%m-%d')
        df = df.dropna(subset=['data']) # Remove quem ficou sem data

        df.to_csv("noticias_eventos_vale.csv", index=False)
        print(f"\n🎉 Sucesso Total! {len(df)} notícias históricas salvas em 'noticias_eventos_vale.csv'")
    else:
        print("\nNenhuma notícia encontrada. Tente rodar novamente (bloqueio temporário pode ocorrer).")