from fastapi import FastAPI, HTTPException
from scraper import scrape_mercado_livre

app = FastAPI()

@app.get("/scrape/")
def scrape_product(url: str):
    try:
        data = scrape_mercado_livre(url)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
