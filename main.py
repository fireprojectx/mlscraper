from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from scraper import extrair_dados_produto

app = FastAPI()

@app.get("/scrape/")
def scrape_product(url: str):
    try:
        return extrair_dados_produto(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve frontend
app.mount("/", StaticFiles(directory="public", html=True), name="static")
