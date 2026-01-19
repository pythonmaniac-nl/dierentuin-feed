# scraper/pairidaiza.py

from playwright.sync_api import sync_playwright
from datetime import datetime
import pytz

BASE_URL = "https://www.pairidaiza.eu"
NEWS_URL = f"{BASE_URL}/nl/news"

def scrape_pairidaiza():
    news_items = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("[PAIRIDAIZA] Loading page...")
        page.goto(NEWS_URL, timeout=60000)

        # infinite scroll / lazy load
        last_height = 0
        scroll_rounds = 0

        while scroll_rounds < 20:  # failsafe
            scroll_rounds += 1
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(800)
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print(f"[PAIRIDAIZA] Scroll completed in {scroll_rounds} rounds")

        cards = page.query_selector_all(".card-news-inner")
        print(f"[PAIRIDAIZA] Found {len(cards)} cards")

        for card in cards:
            try:
                date_tag = card.query_selector(".t-label")
                title_tag = card.query_selector("h3.card-news__content__title-inner")
                link_tag = card.query_selector("a.btn")

                if not (date_tag and title_tag and link_tag):
                    continue

                date_raw = date_tag.inner_text().strip()
                title = title_tag.inner_text().strip()
                link = link_tag.get_attribute("href")

                if not link.startswith("http"):
                    link = BASE_URL + link

                # Parse date dd.mm.yyyy -> datetime
                dt = datetime.strptime(date_raw, "%d.%m.%Y").replace(tzinfo=pytz.UTC)

                # Description fallback
                desc = card.query_selector("p")
                description = desc.inner_text().strip() if desc else ""

                if not description:
                    category = card.query_selector(".label")
                    description = category.inner_text().strip() if category else ""

                print(f"[PAIRIDAIZA] {date_raw} | {title}")

                news_items.append({
                    "source": "Pairi Daiza",
                    "title": title,
                    "link": link,
                    "description": description,
                    "pubDate": dt
                })

            except Exception as e:
                print(f"[PAIRIDAIZA] Parse error: {e}")

        browser.close()

    print(f"[PAIRIDAIZA] Total items found: {len(news_items)}")
    return news_items