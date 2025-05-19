from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class SearchQuery(BaseModel):
    question: str

@app.post("/web_search")
def web_search(query: SearchQuery):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://html.duckduckgo.com/html/?q={query.question}"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.select("a.result__a")

    top_results = []
    for r in results[:5]:
        title = r.get_text()
        link = r.get("href")
        top_results.append({"title": title, "link": link})

    return {"results": top_results}

@app.get("/")
def root():
    return {"message": "API працює!"}
