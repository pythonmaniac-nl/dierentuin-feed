import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/items.json")

def fetch_news():
    url = "https://ouwehand.nl/nieuws"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    articles = []

    for item in soup.select(".news-item")[:5]:
        title = item.select_one(".title").get_text(strip=True)
        link = item.select_one("a")["href"]
        date_str = item.select_one(".date").get_text(strip=True)
        date = datetime.strptime(date_str, "%d-%m-%Y")
        summary = item.select_one(".summary").get_text(strip=True)

        articles.append({
            "title": title,
            "link": link,
            "date": date.isoformat(),
            "summary": summary,
            "source": "Ouwehands Dierenpark"
        })

    return articles

if __name__ == "__main__":
    articles = fetch_news()
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.extend(articles)
    seen = set()
    data = [x for x in data if not (x['link'] in seen or seen.add(x['link']))]

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
