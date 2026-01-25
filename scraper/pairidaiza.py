import requests
from datetime import datetime

API = "https://cms.pairidaiza.eu/api/news?lang=nl"

def scrape_pairidaiza():
    items = []
    try:
        r = requests.get(API, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"[PAIRIDAIZA] Error: {e}")
        return items

    news = data.get("data", [])
    print(f"[PAIRIDAIZA] Found {len(news)} items")

    for n in news:
        try:
            title = n.get("title", "").strip()
            url = "https://www.pairidaiza.eu" + n.get("slug")
            description = (n.get("intro") or "").strip()
            thumbnail = n.get("bigImageUrl")

            dt = n.get("publishedAt")
            pubDate = datetime.fromisoformat(dt.replace("Z", "+00:00")) if dt else None

            items.append({
                "source": "Pairi Daiza",
                "title": title,
                "url": url,
                "description": description,
                "thumbnail": thumbnail,
                "pubDate": pubDate,
            })

        except Exception as e:
            print(f"[PAIRIDAIZA] Parse error: {e}")

    return items