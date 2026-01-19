# scraper/pairidaiza.py
import requests
from datetime import datetime
import pytz

BASE_URL = "https://www.pairidaiza.eu"
# JSON-endpoint dat de nieuwsitems levert (categorie: Ervaring en activiteiten)
API_URL = "https://cms.pairidaiza.eu/api/news?category=ervaring-activiteiten"

def scrape_pairidaiza():
    news_items = []
    print("[PAIRIDAIZA] Fetching news via JSON endpoint...")

    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[PAIRIDAIZA] Error fetching JSON: {e}")
        return news_items

    items = data.get("items", [])
    print(f"[PAIRIDAIZA] Found {len(items)} items in JSON")

    for item in items:
        try:
            title = item.get("title", "Geen titel")
            url_path = item.get("url", "#")
            link = BASE_URL + url_path if not url_path.startswith("http") else url_path
            description = item.get("intro", "")
            date_str = item.get("date")  # ISO format bijv. "2026-01-15T10:00:00"
            if date_str:
                dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            else:
                dt = datetime.now(pytz.UTC)

            news_items.append({
                "title": title,
                "link": link,
                "description": description if description else f"Lees meer: {link}",
                "pubDate": dt,
                "source": "Pairi Daiza"
            })
            print(f"[PAIRIDAIZA] Added: {title}")
        except Exception as e:
            print(f"[PAIRIDAIZA] Parse error: {e}")

    print(f"[PAIRIDAIZA] Total items added: {len(news_items)}")
    return news_items

# Alleen uitvoeren bij direct run
if __name__ == "__main__":
    scrape_pairidaiza()