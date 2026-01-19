from feedgen.feed import FeedGenerator
from scraper.ouwahands import scrape_ouwahands
from scraper.burgerszoo import scrape_burgers

feed = FeedGenerator()
feed.title("Dierentuin Nieuws NL + Pairi Daiza")
feed.link(href="https://pythonmaniac-nl.github.io/dierentuin-feed/feed.xml")
feed.description("Kort nieuws van alle geselecteerde dierentuinen")
feed.language("nl")

# 🔽 haal op
items = []
items += scrape_ouwahands()
items += scrape_burgers()

# 🔽 sorteer op datum nieuw → oud
items = sorted(items, key=lambda x: x["pubDate"], reverse=True)

print(f"Total combined items: {len(items)}")

# 🔽 voeg toe aan feed.xml
for item in items:
    entry = feed.add_entry()
    entry.title(f"{item['source']}: {item['title']}")
    entry.link(href=item["link"])
    entry.description(item["description"])
    entry.pubDate(item["pubDate"])

feed.rss_file("feed/feed.xml")
print("Feed written: feed/feed.xml")
