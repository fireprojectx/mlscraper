import requests
from bs4 import BeautifulSoup
import re

def scrape_mercado_livre(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Preço do produto
    price_tag = soup.find('span', class_='andes-money-amount__fraction')
    price = price_tag.get_text().strip() if price_tag else 'N/A'

    # Estoque disponível
    stock_tag = soup.find('span', class_='ui-pdp-buybox__quantity__available')
    stock = stock_tag.get_text().strip() if stock_tag else 'N/A'

    # Número de vendas
    sales_tag = soup.find('span', class_='ui-pdp-subtitle')
    sales_match = re.search(r'(\d+) vendidos?', sales_tag.get_text()) if sales_tag else None
    sales = sales_match.group(1) if sales_match else 'N/A'

    # Início do anúncio (startTime)
    start_time_script = soup.find('script', text=re.compile(r'\"start_time\"'))
    start_time_match = re.search(r'\"start_time\":\"([^\"]+)\"', start_time_script.string) if start_time_script else None
    start_time = start_time_match.group(1) if start_time_match else 'N/A'

    return {
        'price': price,
        'stock': stock,
        'sales': sales,
        'start_time': start_time
    }
