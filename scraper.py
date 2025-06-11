import requests
from bs4 import BeautifulSoup
import re
import json

def scrape_mercado_livre(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Price, stock, sales...
    price_tag = soup.find('span', class_='price-tag-fraction')
    price = price_tag.text.strip() if price_tag else 'N/A'

    stock_tag = soup.find('p', class_='ui-pdp-quantity__available')
    stock = stock_tag.text.strip() if stock_tag else 'N/A'

    sales_tag = soup.find('span', class_='ui-pdp-subtitle__sold-quantity')
    sales = re.search(r'(\d+)', sales_tag.text).group(1) if sales_tag else 'N/A'

    start_time = 'N/A'
    # 🧠 Procura por JSON que contenha "startTime"
    scripts = soup.find_all('script')
    for script in scripts:
        if 'startTime' in script.text:
            # Extrai JSON com regex
            m = re.search(r'\{.*"startTime":".*?".*\}', script.text, re.S)
            if m:
                try:
                    data = json.loads(m.group(0))
                    start_time = data.get('startTime', 'N/A')
                    break
                except json.JSONDecodeError:
                    pass

    return {
        'price': price,
        'stock': stock,
        'sales': sales,
        'start_time': start_time
    }

