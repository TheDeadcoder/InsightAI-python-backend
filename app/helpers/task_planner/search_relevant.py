import requests
from bs4 import BeautifulSoup
from pydantic import parse_obj_as
import json
from app.core.config import settings
from app.schemas.task_planner import SearchResult
from .clean_bs4 import clean_page_content

def fetch_top_results(query: str) -> list[SearchResult]:
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "gl": "bd","num": 5})
    headers = {
        'X-API-KEY': settings.SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    search_data = response.json()

    organic_results = search_data.get('organic', [])
    results = []

    for result in organic_results:
        if "youtube.com" not in result['link'] and len(results) < 3:
            results.append(SearchResult(
                title=result['title'],
                link=result['link']
            ))

    for result in results:
        page_response = requests.get(result.link)
        soup = BeautifulSoup(page_response.content, 'html.parser')
        content = clean_page_content(soup.get_text(), result.title)
        result.content = content

    

    return results
