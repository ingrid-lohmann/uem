from GoogleNews import GoogleNews
from newspaper import Article, Config
import pandas as pd
import dateparser
import time
import re

# --- CONFIGURAÇÃO DE SEGURANÇA E DADOS ---
config_navegador = Config()
config_navegador.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
config_navegador.request_timeout = 15

TERMOS_GEOGRAFICOS = [
    'mariana', 'brumadinho', 'samarco', 'fundão', 'rio doce', 'feijão',
    'córrego'
]
TERMOS_BASELINE = ['produção', 'minério', 'resultado', 'guidance', 'lucro']
SITES_FINANCEIROS = "infomoney.com.br moneytimes.com.br braziljournal.com suno.com.br"
QUERY_SITES_FINANCEIROS = f"site:{' OR site:'.join(SITES_FINANCEIROS.split())}"


def limpar_url_google(url_suja):
    url_limpa = re.sub(r'&ved=.*', '', url_suja)
    url_limpa = re.sub(r'&usg=.*', '', url_limpa)
    return url_limpa


def validar_relevancia(titulo, texto, evento):
    """
    Filtro Definitivo 6.0: Exige 'Vale/VALE3' no TÍTULO e valida o contexto da Fase.
    """
    titulo_lower = titulo.lower()
    conteudo_completo = (titulo_lower + " " + texto.lower())

    # REGRA CRÍTICA 1: O TÍTULO DEVE FALAR DA EMPRESA
    if not ('vale' in titulo_lower or 'vale3' in titulo_lower):
        return False, "Regra de Ouro falhou: Vale/VALE3 não está no título"

    # REGRA CRÍTICA 2: FILTRO DE CONTEÚDO BASEADO NA FASE
    if 'Baseline' in evento:
        # FASES de Baseline: Deve ser sobre o NEGÓCIO (produção/lucro) e NUNCA sobre tragédia
        tem_baseline = any(t in titulo_lower for t in TERMOS_BASELINE)
        if any(t in conteudo_completo for t in TERMOS_GEOGRAFICOS):
            return False, "Tragédia citada na Baseline (excluído)"
        if not tem_baseline:
            return False, "Conteúdo Baseline muito vago"

    else:  # Fases de Impacto
        # FASES de Impacto: Deve ser sobre a TRAGÉDIA
        tem_geografico = any(t in conteudo_completo
                             for t in TERMOS_GEOGRAFICOS)
        if not tem_geografico:
            return False, "Desastre não citado no texto de Impacto"

    return True, "Aprovado"


def buscar_foco_financeiro():
    janelas = [
        # FASE 1: Baseline Mariana (Normalidade, NOT Tragédia)
        {
            'inicio': '10/25/2015',
            'fim': '11/04/2015',
            'termo_base': 'Vale (VALE3) produção minério',
            'evento': 'Baseline_Mariana',
            'meta': 6
        },
        # FASE 2: Impacto Mariana (Tragédia em 05/11/2015)
        {
            'inicio': '11/05/2015',
            'fim': '11/30/2015',
            'termo_base': 'Vale barragem Mariana',
            'evento': 'Impacto_Mariana',
            'meta': 6
        },

        # FASE 3: Baseline Brumadinho (Normalidade, NOT Tragédia)
        {
            'inicio': '01/15/2019',
            'fim': '01/24/2019',
            'termo_base': 'Vale (VALE3) produção resultados',
            'evento': 'Baseline_Brumadinho',
            'meta': 6
        },
        # FASE 4: Impacto Brumadinho (Tragédia em 25/01/2019)
        {
            'inicio': '01/25/2019',
            'fim': '02/20/2019',
            'termo_base': 'Vale barragem Brumadinho',
            'evento': 'Impacto_Brumadinho',
            'meta': 6
        },
    ]

    todas_noticias = []
    urls_ja_vistas = set()

    print(
        "=== Iniciando Coleta Definitiva (4 Fases e Filtro de Título Ativo) ==="
    )

    for janela in janelas:
        print(f"\n>>> Fase: {janela['evento']}")

        # Query única: Termo da fase + restrição aos sites financeiros
        query = f"{janela['termo_base']} {QUERY_SITES_FINANCEIROS}"

        gnews = GoogleNews(lang='pt',
                           region='BR',
                           start=janela['inicio'],
                           end=janela['fim'])
        gnews.search(query)

        aprovadas_fase = 0

        for p in range(1, 3):
            if aprovadas_fase >= janela['meta']: break
            gnews.get_page(p)
            time.sleep(3)  # Tempo de espera CRÍTICO

        resultados = gnews.results()

        for item in resultados:
            if aprovadas_fase >= janela['meta']: break

            url = limpar_url_google(item['link'])
            if url in urls_ja_vistas: continue

            conteudo = processar_noticia(url)

            if conteudo:
                aprovado, motivo = validar_relevancia(conteudo['titulo'],
                                                      conteudo['texto'],
                                                      janela['evento'])

                if aprovado:
                    urls_ja_vistas.add(url)
                    if not conteudo['data']:
                        conteudo['data'] = item.get('date')

                    conteudo['evento_fase'] = janela['evento']
                    todas_noticias.append(conteudo)
                    aprovadas_fase += 1
                    print(
                        f"   ✅ [SALVO: {janela['evento']}] {conteudo['titulo'][:35]}..."
                    )
                # else: print(f"   🚫 [Rejeitado - {motivo}]...") # Debug

        gnews.clear()
        time.sleep(5)

    return todas_noticias


def processar_noticia(url):
    try:
        article = Article(url, config=config_navegador)
        article.download()
        article.parse()
        if len(article.text) < 200: return None
        data_str = article.publish_date.strftime(
            '%Y-%m-%d') if article.publish_date else None
        return {
            "titulo": article.title,
            "texto": article.text,
            "url": url,
            "data": data_str
        }
    except:
        return None


if __name__ == "__main__":
    dados = buscar_foco_financeiro()
    if dados:
        df = pd.DataFrame(dados)
        df['data'] = pd.to_datetime(df['data'],
                                    errors='coerce').dt.strftime('%Y-%m-%d')
        df = df.dropna(subset=['data'])
        nome_arquivo = "noticias_vale_4_fases_final.csv"
        df.to_csv(nome_arquivo, index=False)
        print(
            f"\n🎉 Coleta Finalizada! {len(df)} notícias salvas em '{nome_arquivo}'"
        )
        print("\n--- Etapa 1 CONCLUÍDA: Base de Dados Pura e Focada. ---")
    else:
        print("\nNenhuma notícia passou no filtro.")
