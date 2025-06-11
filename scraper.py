import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def scrape_mercado_livre(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    # ————————————— Dados principais —————————————
    # Título do produto
    titulo_tag = soup.find('h1')
    titulo = titulo_tag.text.strip() if titulo_tag else "N/A"

    # Preço
    preco_tag = soup.find('span', class_='price-tag-fraction')
    preco = preco_tag.text.strip() if preco_tag else "N/A"

    # Vendas
    vendidos_tag = soup.find('span', class_='ui-pdp-subtitle__sold-quantity')
    vendidos_match = re.search(r'(\d+)', vendidos_tag.text) if vendidos_tag else None
    vendidos = vendidos_match.group(1) if vendidos_match else "N/A"

    # ————————————— Extract & format startTime —————————————
    starttime = "Não encontrado"
    script_text = response.text
    starttime_match = re.search(r'"startTime"\s*:\s*"([^"]+)"', script_text)
    if starttime_match:
        raw_date = starttime_match.group(1)
        try:
            # Parse string como ISO-8601 com 'Z' de UTC
            date_obj = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
            starttime = date_obj.strftime("%d/%m/%y")
        except ValueError:
            starttime = raw_date

    return {
        "Título": titulo,
        "Preço": preco,
        "Vendidos": vendidos,
        "Data de início (dd/mm/aa)": starttime
    }
