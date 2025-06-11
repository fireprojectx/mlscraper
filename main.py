from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from scraper import scrape_mercado_livre

app = FastAPI()

# 1️⃣ Rota da API de scraping
@app.get("/scrape/")
def scrape_product(url: str):
    try:
        return scrape_mercado_livre(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2️⃣ Monta os arquivos estáticos somente após definir as rotas
app.mount("/", StaticFiles(directory="public", html=True), name="static")

