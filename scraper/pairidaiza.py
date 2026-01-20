import requests
from datetime import datetime
from urllib.parse import urljoin

BASE_URL = "https://www.pairidaiza.eu/nl/news"

def scrape_pairidaiza():
    items = []
    try:
        resp = requests.get(BASE_URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[PAIRIDAIZA] Error fetching page: {e}")
        return items

    soup = BeautifulSoup(resp.text, "lxml")
    cards = soup.select(".card-news-inner.has-video, .card-news-inner.has-text")  # general selector
    print(f"[PAIRIDAIZA] Found {len(cards)} items")

    for card in cards:
        try:
            # Title
            title_tag = card.select_one("h3.card-news__content__title-inner")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            # URL
            link_tag = card.select_one("a.btn")
            url = urljoin(BASE_URL, link_tag["href"]) if link_tag and link_tag.get("href") else None

            # Date
            date_tag = card.select_one("span.t-label")
            pubDate = None
            if date_tag:
                try:
                    pubDate = datetime.strptime(date_tag.get_text(strip=True), "%d.%m.%Y")
                except:
                    pubDate = None

            # Thumbnail
            img_tag = card.select_one("img")
            thumbnail = None
            if img_tag:
                if img_tag.has_attr("srcset"):
                    parts = [p.split()[0] for p in img_tag["srcset"].split(",")]
                    thumbnail = urljoin(BASE_URL, parts[-1])
                elif img_tag.has_attr("src"):
                    thumbnail = urljoin(BASE_URL, img_tag["src"])

            # Description: intro + first p from detail
            desc_tag = card.select_one(".card-news__content__copy")
            description = desc_tag.get_text(" ", strip=True) if desc_tag else ""
            if url and not description:
                try:
                    detail_resp = requests.get(url, timeout=10)
                    detail_soup = BeautifulSoup(detail_resp.text, "lxml")
                    p = detail_soup.select_one("p")
                    description = p.get_text(strip=True) if p else ""
                except:
                    description = ""

            items.append({
                "source": "Pairi Daiza",
                "title": title,
                "url": url,
                "description": description,
                "thumbnail": thumbnail,
                "pubDate": pubDate
            })

        except Exception as e:
            print(f"[PAIRIDAIZA] Parse error: {e}")
    return items