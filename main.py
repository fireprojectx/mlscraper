from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from scraper import scrape_mercado_livre
import os

app = FastAPI()

# Servir arquivos estáticos do frontend (HTML)
app.mount("/", StaticFiles(directory="public", html=True), name="static")

# Rota de scraping
@app.get("/scrape/")
def scrape_product(url: str):
    try:
        data = scrape_mercado_livre(url)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
