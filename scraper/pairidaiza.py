# scraper/pairidaiza.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

BASE_URL = "https://www.pairidaiza.eu"
NEWS_URL = f"{BASE_URL}/nl/news"
news_items = []

def scrape_pairidaiza():
    print("[PAIRIDAIZA] Fetching news...")
    try:
        response = requests.get(NEWS_URL)
        response.raise_for_status()
    except Exception as e:
        print(f"[PAIRIDAIZA] Error fetching overview page: {e}")
        return news_items

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select("div.card-news-inner")
    print(f"[PAIRIDAIZA] Found {len(cards)} news items")

    for item_card in cards:
        try:
            # Titel
            title_tag = item_card.select_one("h3.card-news__content__title-inner")
            title = title_tag.get_text(strip=True) if title_tag else "Geen titel"

            # Link
            link_tag = item_card.select_one("a.btn[href]")
            link = link_tag["href"] if link_tag else "#"
            if not link.startswith("http"):
                link = BASE_URL + link

            # Datum
            date_tag = item_card.select_one("span.t-label")
            date_str = date_tag.get_text(strip=True) if date_tag else None
            if date_str:
                dt = datetime.strptime(date_str, "%d.%m.%Y").replace(tzinfo=pytz.UTC)
            else:
                dt = datetime.now(pytz.UTC)

            # Intro / description
            description = ""
            try:
                resp = requests.get(link)
                resp.raise_for_status()
                article_soup = BeautifulSoup(resp.text, "html.parser")
                # Pas deze selector aan als intro anders in HTML staat
                intro_tag = article_soup.select_one("div.article-intro, div.intro, p")
                if intro_tag:
                    description = intro_tag.get_text(strip=True)
                if not description:
                    description = f"Lees meer: {link}"
            except Exception as e:
                description = f"Lees meer: {link}"

            # Voeg item toe
            news_items.append({
                "title": title,
                "link": link,
                "description": description,
                "pubDate": dt,
                "source": "Pairi Daiza"
            })

            print(f"[PAIRIDAIZA] Added: {title}")

        except Exception as e:
            print(f"[PAIRIDAIZA] Error parsing card: {e}")

    print(f"[PAIRIDAIZA] Total items found: {len(news_items)}")
    return news_items
