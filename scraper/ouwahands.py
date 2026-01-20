import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from urllib.parse import urljoin

BASE_URL = "https://ouwehand.nl"
NEWS_URL = f"{BASE_URL}/nl/nieuws"

def scrape_ouwahands():
    items = []
    try:
        resp = requests.get(NEWS_URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[OUWEHANDS] Error fetching page: {e}")
        return items

    soup = BeautifulSoup(resp.text, "lxml")
    news_posts = soup.select("a.news-post")
    print(f"[OUWEHANDS] Found {len(news_posts)} items")

    for post in news_posts:
        try:
            title = post.select_one("h2.title").get_text(strip=True)
            link = post.get("href")
            if not link.startswith("http"):
                link = urljoin(BASE_URL, link)

            date_tag = post.select_one("time.date")
            pubDate = None
            if date_tag:
                dt = datetime.strptime(date_tag.get_text(strip=True), "%d-%m-%Y")
                pubDate = dt.replace(tzinfo=pytz.UTC)

            desc_tag = post.select_one("p.desc")
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            # Thumbnail
            img_tag = post.select_one("p.flex-img img")
            thumbnail = None
            if img_tag and img_tag.get("src"):
                thumbnail = urljoin(BASE_URL, img_tag["src"])

            items.append({
                "source": "Ouwehands",
                "title": title,
                "url": link,
                "description": description,
                "thumbnail": thumbnail,
                "pubDate": pubDate
            })
            print(f"[OUWEHANDS] Added to feed: {title}")
        except Exception as e:
            print(f"[OUWEHANDS] Parse error: {e}")
    return items