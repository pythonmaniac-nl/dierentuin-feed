import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

BASE_URL = "https://www.pairidaiza.eu"
news_items = []


import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

BASE_URL = "https://www.pairidaiza.eu"
NEWS_URL = f"{BASE_URL}/nieuws"

def scrape_pairidaiza():
    response = requests.get(NEWS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("a.news-post")
    print(f"[PairiDaiza] Found {len(items)} items")

    results = []
    for item_card in soup.select("div.card-news-inner"):
    title_tag = item_card.select_one("h3.card-news__content__title-inner")
    title = title_tag.get_text(strip=True) if title_tag else "Geen titel"

    link_tag = item_card.select_one("a.btn[href]")
    link = link_tag["href"] if link_tag else "#"
    if not link.startswith("http"):
        link = BASE_URL + link

    date_tag = item_card.select_one("span.t-label")
    date_str = date_tag.get_text(strip=True) if date_tag else None
    dt = datetime.strptime(date_str, "%d.%m.%Y").replace(tzinfo=pytz.UTC) if date_str else datetime.now(pytz.UTC)

    # ✅ Fetch article detail for description
    description = ""
    try:
        resp = requests.get(link)
        if resp.status_code == 200:
            article_soup = BeautifulSoup(resp.text, "html.parser")
            intro_tag = article_soup.select_one("div.article-intro, div.intro, p")  # pas selector aan op echte structuur
            if intro_tag:
                description = intro_tag.get_text(strip=True)
        if not description:
            description = f"Lees meer: {link}"
    except Exception as e:
        description = f"Lees meer: {link}"

    news_items.append({
        "title": title,
        "link": link,
        "description": description,
        "pubDate": dt,
        "source": "Pairi Daiza"
    })
        except Exception as e:
            print(f"[PairiDaiza] Parse error: {e}")

    return results
