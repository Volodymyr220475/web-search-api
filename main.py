from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class SearchQuery(BaseModel):
    question: str

@app.post("/web_search")
def web_search(query: SearchQuery):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://html.duckduckgo.com/html/?q={query.question}"

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    soup = BeautifulSoup(response.text, "html.parser")
    result_links = soup.select("a.result__a")

    if not result_links:
        return {"results": [], "message": "No results found"}

    top_results = []
    for r in result_links[:5]:  # Топ-5
        title = r.get_text(strip=True)
        link = r.get("href")
        top_results.append({"title": title, "link": link})

    return {"results": top_results}
