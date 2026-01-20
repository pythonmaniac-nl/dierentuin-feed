import sys
import os

# Voeg repo root toe zodat scraper module gevonden wordt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from feedgen.feed import FeedGenerator
from scraper.ouwahands import scrape_ouwahands
from scraper.burgerszoo import scrape_burgerszoo
from scraper.pairidaiza import scrape_pairidaiza
import os

FEED_DIR = "feed"
FEED_FILE = os.path.join(FEED_DIR, "feed.xml")
os.makedirs(FEED_DIR, exist_ok=True)

# Scrape all parks
all_items = []
for scraper in [scrape_ouwahands, scrape_burgerszoo, scrape_pairidaiza]:
    try:
        scraped = scraper()
        all_items.extend(scraped)
    except Exception as e:
        print(f"[FEED] Scraper failed: {e}")

# Remove items without URL or date
all_items = [i for i in all_items if i.get("url") and i.get("pubDate")]

# Sort by date descending
all_items.sort(key=lambda x: x["pubDate"], reverse=True)

# Generate feed
fg = FeedGenerator()
fg.title("Dierentuin Nieuws NL + Pairi Daiza")
fg.link(href="https://pythonmaniac-nl.github.io/dierentuin-feed/feed/feed.xml")
fg.description("Kort nieuws van alle geselecteerde dierentuinen")
fg.language("nl")

for item in all_items:
    fe = fg.add_entry()
    fe.title(f"{item['source']}: {item['title']}")
    fe.link(href=item["url"])
    fe.pubDate(item["pubDate"])
    # Inline image + media:content
    content = ""
    if item.get("thumbnail"):
        content += f'<p><img src="{item["thumbnail"]}" style="max-width:800px;height:auto;"></p>'
        fe.enclosure(item["thumbnail"], 0, "image/jpeg")
    if item.get("description"):
        content += f"<p>{item['description']}</p>"
    fe.content(content, type="CDATA")

# Write feed
fg.rss_file(FEED_FILE)
print(f"[FEED] Feed written: {FEED_FILE} | Total items: {len(all_items)}")