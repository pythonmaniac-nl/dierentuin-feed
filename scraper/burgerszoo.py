import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

BASE_URL = "https://www.burgerszoo.nl"
NEWS_URL = f"{BASE_URL}/nieuws"

# Maanden mapping voor Nederlandse datums
MONTHS = {
    "januari": 1, "februari": 2, "maart": 3, "april": 4,
    "mei": 5, "juni": 6, "juli": 7, "augustus": 8,
    "september": 9, "oktober": 10, "november": 11, "december": 12,
}

def scrape_burgerszoo():
    news_items = []

    try:
        response = requests.get(NEWS_URL)
        response.raise_for_status()
    except Exception as e:
        print(f"[BURGERS] Error fetching news page: {e}")
        return news_items

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select("a.block-news-item")

    for item in items:
        try:
            # Link
            link = item.get("href")
            if link and not link.startswith("http"):
                link = BASE_URL + link

            # Titel
            title_tag = item.select_one("h2.card-title")
            title = title_tag.get_text(strip=True) if title_tag else "Geen titel"

            # Beschrijving
            desc_tag = item.select_one("p.card-text")
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            # Datum
            dt = None
            date_tag = item.select_one("p.card-date")
            if date_tag:
                date_str = date_tag.get_text(strip=True)
                if date_str:
                    try:
                        d, m, y = date_str.split()
                        dt = datetime(int(y), MONTHS[m.lower()], int(d), tzinfo=pytz.UTC)
                    except Exception as e:
                        print(f"[BURGERS] Date parse error '{date_str}': {e}")
                        dt = datetime.now(pytz.UTC)  # fallback
                else:
                    dt = datetime.now(pytz.UTC)  # lege string fallback
            else:
                dt = datetime.now(pytz.UTC)  # geen date tag fallback

            # Voeg toe aan items
            news_items.append({
                "title": title,
                "link": link,
                "description": description,
                "pubDate": dt
            })

            print(f"[BURGERS] {dt.strftime('%d-%m-%Y')} | {title}")

        except Exception as e:
            print(f"[BURGERS] Parse error: {e}")

    print(f"[BURGERS] Total items found: {len(news_items)}")
    return news_items
