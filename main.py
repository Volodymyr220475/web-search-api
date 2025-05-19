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
    url = f"https://html.duckduckgo.com/html?q={query.question}"
    response = requests.get(url, headers=headers, timeout=5)

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.select("a.result__a")

    results = []
    for link in links[:5]:
        results.append({
            "title": link.get_text(),
            "url": link.get("href")
        })

    return {"results": results}


@app.get("/")
def read_root():
    return {"message": "API працює"}
