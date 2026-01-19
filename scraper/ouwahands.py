import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

BASE_URL = "https://ouwehand.nl"
NEWS_URL = f"{BASE_URL}/nieuws"

def scrape_ouwahands():
    response = requests.get(NEWS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("a.news-post")
    print(f"[Ouwehands] Found {len(items)} items")

    results = []
    for item in items:
        try:
            link = item["href"]
            if not link.startswith("http"):
                link = BASE_URL + link

            title = item.select_one("h2.title").get_text(strip=True)
            date_str = item.select_one("time.date").get_text(strip=True)
            desc = item.select_one("p.desc")
            description = desc.get_text(strip=True) if desc else ""

            dt = datetime.strptime(date_str, "%d-%m-%Y").replace(tzinfo=pytz.UTC)

            results.append({
                "source": "Ouwehands",
                "title": title,
                "link": link,
                "description": description,
                "pubDate": dt,
                "soruce": "Ouwehands Dierenpark"
            })
        except Exception as e:
            print(f"[Ouwehands] Parse error: {e}")

    return results
