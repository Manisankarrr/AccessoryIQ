import requests
from config.settings import settings

def search_reviews(query):
    headers = {"X-API-KEY": settings.SERPER_API_KEY}
    payload = {"q": query, "num": 5}
    response = requests.post(
        "https://google.serper.dev/search",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    return response.json().get("organic", [])
