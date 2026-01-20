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
            title_tag = card.select_one("h3.card-news__content__title-inner")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            link_tag = card.select_one("a.btn")
            if not link_tag or not link_tag.get("href"):
                continue
            url = urljoin(BASE_URL, link_tag["href"])

            date_tag = card.select_one("span.t-label")
            pubDate = None
            if date_tag:
                try:
                    pubDate = datetime.strptime(date_tag.get_text(strip=True), "%d.%m.%Y")
                except:
                    pubDate = None

            img_tag = card.select_one("img")
            thumbnail = None
            if img_tag:
                if img_tag.has_attr("srcset"):
                    parts = [p.split()[0] for p in img_tag["srcset"].split(",")]
                    thumbnail = urljoin(BASE_URL, parts[-1])
                elif img_tag.has_attr("src"):
                    thumbnail = urljoin(BASE_URL, img_tag["src"])

            intro_tag = card.select_one(".card-news__content__copy")
            description = intro_tag.get_text(" ", strip=True) if intro_tag else ""

            # Fallback: fetch detail page for description if missing
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