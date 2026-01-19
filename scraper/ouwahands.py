import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import os

BASE_URL = "https://ouwehand.nl"
NEWS_URL = f"{BASE_URL}/nieuws"
FEED_DIR = "feed"
FEED_FILE = os.path.join(FEED_DIR, "feed.xml")

# Maak feed map aan als die niet bestaat
os.makedirs(FEED_DIR, exist_ok=True)

# Haal de nieuws pagina
response = requests.get(NEWS_URL)
if response.status_code != 200:
    print(f"Error fetching {NEWS_URL}: {response.status_code}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")

# Selecteer alle nieuwsitems
items = soup.select("a.news-post")
print(f"Found {len(items)} news items")

# Maak een feed
fg = FeedGenerator()
fg.title("Ouwehands Nieuws")
fg.link(href=BASE_URL)
fg.description("Automatisch bijgewerkte feed van Ouwehands Dierenpark")

for item in items:
    try:
        link = item["href"]
        if not link.startswith("http"):
            link = BASE_URL + link
        title = item.select_one("h2.title").get_text(strip=True)
        date = item.select_one("time.date").get_text(strip=True)
        description_tag = item.select_one("p.desc")
        description = description_tag.get_text(strip=True) if description_tag else ""
        
        # Print debug info
        print(f"{date} | {title} | {link}")
        
        # Voeg item toe aan feed
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=link)
        fe.pubDate(date)
        fe.description(description)
    except Exception as e:
        print(f"Error parsing item: {e}")

# Schrijf de feed naar file
fg.rss_file(FEED_FILE)
print(f"Feed written to {FEED_FILE}")
