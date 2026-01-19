import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz
import os

# --- Config ---
BASE_URL = "https://ouwehand.nl"
NEWS_URL = f"{BASE_URL}/nieuws"
FEED_DIR = "feed"
FEED_FILE = os.path.join(FEED_DIR, "feed.xml")

# Maak map aan als die nog niet bestaat
os.makedirs(FEED_DIR, exist_ok=True)

# --- Scraper ---
print("Starting Ouwehands scraper...")
response = requests.get(NEWS_URL)
if response.status_code != 200:
    print(f"Error fetching {NEWS_URL}: {response.status_code}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")
items = soup.select("a.news-post")
print(f"Found {len(items)} news items")

# --- Feed setup ---
fg = FeedGenerator()
fg.title("Dierentuin Nieuws NL + Pairi Daiza")
fg.link(href="https://pythonmaniac-nl.github.io/dierentuin-feed/feed.xml")
fg.description("Kort nieuws van alle geselecteerde dierentuinen")
fg.language("nl")

# --- Voeg items toe ---
for item in items:
    try:
        link = item["href"]
        if not link.startswith("http"):
            link = BASE_URL + link
        title = item.select_one("h2.title").get_text(strip=True)
        date_str = item.select_one("time.date").get_text(strip=True)
        description_tag = item.select_one("p.desc")
        description = description_tag.get_text(strip=True) if description_tag else ""

        # Parse datum en voeg timezone toe
        dt = datetime.strptime(date_str, "%d-%m-%Y")
        dt = dt.replace(tzinfo=pytz.UTC)

        # Voeg toe aan feed
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=link)
        fe.description(description)
        fe.pubDate(dt)

        print(f"Added to feed: {title}")
    except Exception as e:
        print(f"Error parsing item: {e}")

# --- Schrijf feed.xml ---
fg.rss_file(FEED_FILE)
print(f"Feed written to {FEED_FILE}")
