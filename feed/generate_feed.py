import json
import os
from feedgen.feed import FeedGenerator
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/items.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "feed.xml")

with open(DATA_FILE, "r") as f:
    items = json.load(f)

items.sort(key=lambda x: x['date'], reverse=True)

fg = FeedGenerator()
fg.title("Dierentuin Nieuws NL + Pairi Daiza")
fg.link(href="https://pythonmaniac-nl.github.io/dierentuin-feed/feed.xml")
fg.description("Kort nieuws van alle geselecteerde dierentuinen")
fg.language("nl")

for item in items:
    fe = fg.add_entry()
    fe.title(item['title'])
    fe.link(href=item['link'])
    fe.pubDate(datetime.fromisoformat(item['date']))
    fe.description(item['summary'])
    fe.source(item['source'], url="")

fg.rss_file(OUTPUT_FILE)
print(f"Feed gegenereerd: {OUTPUT_FILE}")
