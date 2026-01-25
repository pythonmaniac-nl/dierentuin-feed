import sys, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from feedgen.feed import FeedGenerator
from scraper.ouwahands import scrape_ouwahands
from scraper.burgerszoo import scrape_burgerszoo
from scraper.pairidaiza import scrape_pairidaiza

items = []
for s in [scrape_ouwahands, scrape_burgerszoo, scrape_pairidaiza]:
    try:
        items.extend(s())
    except Exception as e:
        print(f"[FEED] Scraper failed: {e}")

items = [i for i in items if i.get("url") and i.get("pubDate")]
items.sort(key=lambda x: x["pubDate"], reverse=True)

fg = FeedGenerator()
fg.title("Dierentuinen Nieuws")
fg.link(href="https://pythonmaniac-nl.github.io/dierentuin-feed/feed.xml")
fg.description("Nieuws uit NL en BE dierentuinen")
fg.language("nl")

for i in items:
    fe = fg.add_entry()
    fe.id(i["url"])
    fe.title(f"{i['source']}: {i['title']}")
    fe.link(href=i["url"])
    fe.pubDate(i["pubDate"])

    content = ""
    if i.get("thumbnail"):
        content += f'<img src="{i["thumbnail"]}" /><br>'
        fe.enclosure(i["thumbnail"], 0, "image/jpeg")
    if i.get("description"):
        content += f"<p>{i['description']}</p>"

    fe.content(content, type="CDATA")

fg.rss_file("feed/feed.xml")
print(f"[FEED] Done: {len(items)} items")