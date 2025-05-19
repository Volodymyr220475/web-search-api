from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class SearchQuery(BaseModel):
    question: str

@app.post("/web_search")
def web_search(query: SearchQuery):
    try:
        url = f"https://html.duckduckgo.com/html?q={query.question}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = requests.get(url, headers=headers, timeout=7)

        if response.status_code != 200:
            return {"error": f"Search request failed with status {response.status_code}"}

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        for result in soup.select("a.result__a")[:10]:
            title = result.get_text(strip=True)
            href = result.get("href")
            if title and href:
                results.append({"title": title, "url": href})

        return {"results": results}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "API працює"}
