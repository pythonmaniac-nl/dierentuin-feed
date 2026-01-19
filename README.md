# Dierentuin Nieuws NL + Pairi Daiza

Deze repository genereert een master-feed van 11 Nederlandse dierentuinen + Pairi Daiza.

- Feed korte items: titel + korte samenvatting
- Volgorde: nieuwste bovenaan
- Cron: GitHub Actions, elke 30 minuten
- Feed URL (na Pages activatie):  
https://pythonmaniac-nl.github.io/dierentuin-feed/feed.xml

## Scrapers
- scraper/ouwahands.py
- scraper/burgerszoo.py
- scraper/artis.py
- ...

## Feed generator
- feed/generate_feed.py

## Data
- data/items.json
