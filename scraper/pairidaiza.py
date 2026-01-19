# scraper/pairidaiza.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

BASE_URL = "https://www.pairidaiza.eu"
NEWS_URL = f"{BASE_URL}/nl/news"

def scrape_pairidaiza():
    news_items = []
    print("[PAIRIDAIZA] Fetching news...")
    
    try:
        response = requests.get(NEWS_URL)
        response.raise_for_status()
    except Exception as e:
        print(f"[PAIRIDAIZA] Error fetching overview page: {e}")
        return news_items

    soup = BeautifulSoup(response.text, "html.parser")
    # selecteer alle nieuws-kaarten
    cards = soup.select("div.card-news-inner")
    print(f"[PAIRIDAIZA] Found {len(cards)} news items")

    for card in cards:
        try:
            # Titel
            title_tag = card.select_one("h3.card-news__content__title-inner")
            title = title_tag.get_text(strip=True) if title_tag else "Geen titel"

            # Link
            link_tag = card.select_one("a.btn[href]")
            link = link_tag["href"] if link_tag else "#"
            if not link.startswith("http"):
                link = BASE_URL + link

            # Datum
            date_tag = card.select_one("span.t-label")
            date_str = date_tag.get_text(strip=True) if date_tag else None
            if date_str:
                dt = datetime.strptime(date_str, "%d.%m.%Y").replace(tzinfo=pytz.UTC)
            else:
                dt = datetime.now(pytz.UTC)

            # Description (intro van detailpagina)
            description = ""
            try:
                resp = requests.get(link)
                resp.raise_for_status()
                detail_soup = BeautifulSoup(resp.text, "html.parser")
                # Zoek intro tekst, fallback naar eerste <p> als nodig
                intro_tag = detail_soup.select_one("div.article-intro, div.intro, p")
                description = intro_tag.get_text(strip=True) if intro_tag else f"Lees meer: {link}"
            except Exception as e:
                description = f"Lees meer: {link}"

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

# Alleen uitvoeren als dit script direct wordt gerund
if __name__ == "__main__":
    scrape_pairidaiza()