import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

BASE_URL = "https://www.ouwehand.nl/nieuws/"

def scrape_ouwahands():
    items = []
    try:
        r = requests.get(BASE_URL, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"[OUWEHANDS] Error: {e}")
        return items

    soup = BeautifulSoup(r.text, "lxml")
    cards = soup.select(".nieuws-item")
    print(f"[OUWEHANDS] Found {len(cards)} items")

    for c in cards:
        try:
            title = c.select_one(".nieuws-title").get_text(strip=True)
            url = urljoin(BASE_URL, c.select_one("a")["href"])
            date = c.select_one(".nieuws-datum").get_text(strip=True)
            pubDate = datetime.strptime(date, "%d-%m-%Y")
            description = c.select_one(".nieuws-intro").get_text(strip=True)

            items.append({
                "source": "Ouwehands",
                "title": title,
                "url": url,
                "description": description,
                "thumbnail": None,
                "pubDate": pubDate
            })

        except Exception as e:
            print(f"[OUWEHANDS] Parse error: {e}")

    return items