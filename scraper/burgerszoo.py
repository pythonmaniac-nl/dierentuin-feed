import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import locale

locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")

BASE_URL = "https://www.burgerszoo.nl"
NEWS_URL = f"{BASE_URL}/nieuws"

def scrape_burgerszoo():
    response = requests.get(NEWS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("a.block-news-item")
    print(f"[Burgers] Found {len(items)} items")

    results = []
    for item in items:
        try:
            link = item["href"]
            if not link.startswith("http"):
                link = BASE_URL + link

            title = item.select_one("h2.card-title").get_text(strip=True)

            desc = item.select_one("p.card-text")
            description = desc.get_text(strip=True) if desc else ""

            date_str = item.select_one("p.card-date").get_text(strip=True)
            dt = datetime.strptime(date_str, "%d %B %Y").replace(tzinfo=pytz.UTC)

            results.append({
                "source": "Burgers Zoo",
                "title": title,
                "link": link,
                "description": description,
                "pubDate": dt
            })
        except Exception as e:
            print(f"[Burgers] Parse error: {e}")

    return results
