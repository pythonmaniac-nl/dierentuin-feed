import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

BASE_URL = "https://www.burgerszoo.nl/nieuws"

def scrape_burgerszoo():
    items = []
    try:
        resp = requests.get(BASE_URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[BURGERS] Error fetching page: {e}")
        return items

    soup = BeautifulSoup(resp.text, "lxml")
    cards = soup.select(".card-news-inner")
    print(f"[BURGERS] Found {len(cards)} items")

    for card in cards:
        try:
            title = card.select_one("h3.card-news__content__title-inner")
            if not title:
                continue
            title = title.get_text(strip=True)

            btn = card.select_one("a.btn")
            if not btn or not btn.get("href"):
                continue
            url = urljoin(BASE_URL, btn["href"])

            date_tag = card.select_one("span.t-label")
            pubDate = None
            if date_tag:
                dt = date_tag.get_text(strip=True)
                try:
                    pubDate = datetime.strptime(dt, "%d.%m.%Y")
                except:
                    pubDate = None

            img = card.select_one("img")
            thumbnail = None
            if img:
                if img.has_attr("srcset"):
                    parts = [p.split()[0] for p in img["srcset"].split(",")]
                    thumbnail = urljoin(BASE_URL, parts[-1])
                elif img.has_attr("src"):
                    thumbnail = urljoin(BASE_URL, img["src"])

            intro = card.select_one(".card-news__content__copy")
            description = intro.get_text(" ", strip=True) if intro else ""

            if not description:
                try:
                    detail_resp = requests.get(url, timeout=10)
                    detail_soup = BeautifulSoup(detail_resp.text, "lxml")
                    p = detail_soup.select_one("p")
                    description = p.get_text(strip=True) if p else ""
                except:
                    description = ""

            items.append({
                "source": "Burgers' Zoo",
                "title": title,
                "url": url,
                "description": description,
                "thumbnail": thumbnail,
                "pubDate": pubDate
            })
        except Exception as e:
            print(f"[BURGERS] Parse error: {e}")

    return items