import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

BASE_URL = "https://www.burgerszoo.nl/nieuws"

def scrape_burgerszoo():
    items = []
    html = requests.get(BASE_URL, timeout=10).text
    soup = BeautifulSoup(html, "lxml")

    cards = soup.select(".card-news-inner")
    for card in cards:
        try:
            title_tag = card.select_one("h3.card-news__content__title-inner")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            # URL
            link_tag = card.select_one("a.btn")
            if not link_tag or not link_tag.get("href"):
                continue
            url = urljoin(BASE_URL, link_tag["href"])

            # Date
            date_tag = card.select_one("span.t-label")
            pub_date = None
            if date_tag:
                try:
                    pub_date = datetime.strptime(date_tag.get_text(strip=True), "%d.%m.%Y")
                except:
                    pass

            # Thumbnail
            thumb = None
            img = card.select_one("img")
            if img:
                # srcset → neem grootste resolution
                if img.has_attr("srcset"):
                    parts = [p.split(" ")[0] for p in img["srcset"].split(",")]
                    thumb = parts[-1] if parts else None
                elif img.has_attr("src"):
                    thumb = img["src"]

                if thumb and thumb.startswith("/"):
                    thumb = urljoin(BASE_URL, thumb)

            # Intro / teaser
            intro_tag = card.select_one(".card-news__content__copy")
            intro = intro_tag.get_text(" ", strip=True) if intro_tag else None

            # Fallback: detailpagina scannen
            if not intro:
                try:
                    detail_html = requests.get(url, timeout=10).text
                    detail_soup = BeautifulSoup(detail_html, "lxml")
                    p = detail_soup.select_one("p")
                    intro = p.get_text(" ", strip=True) if p else ""
                except:
                    intro = ""

            items.append({
                "source": "Burgers' Zoo",
                "title": title,
                "url": url,
                "description": intro,
                "thumbnail": thumb,
                "pubDate": pub_date.isoformat() if pub_date else None
            })

        except Exception as e:
            print(f"[BURGERS] Error: {e}")

    print(f"[BURGERS] Upgraded items: {len(items)}")
    return items