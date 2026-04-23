import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random
import re

def get_headers():
    ua = UserAgent()
    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-IN,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.amazon.in/",
    }

def parse_price(price_str):
    if not price_str:
        return None
    cleaned = re.sub(r"[^\d.]", "", price_str.replace(",", ""))
    try:
        return float(cleaned)
    except ValueError:
        return None

def scrape_amazon(query):
    search_url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    results = []

    try:
        time.sleep(random.uniform(1, 2.5))
        session = requests.Session()
        response = session.get(search_url, headers=get_headers(), timeout=12)

        if response.status_code != 200:
            print(f"[Amazon] Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "lxml")
        product_cards = soup.select('div[data-component-type="s-search-result"]')
        print(f"[Amazon] Raw cards found: {len(product_cards)}")

        for card in product_cards[:6]:

            # ── Title ──────────────────────────────────────────────
            # Full title lives inside the image link's span
            title = None
            for sel in [
                "a.a-link-normal.s-no-outline span",
                "a.a-link-normal span",
                "span.a-declarative",
            ]:
                tag = card.select_one(sel)
                if tag:
                    text = tag.get_text(strip=True)
                    # skip short/empty brand-only strings like "Samsung"
                    if text and len(text) > 12:
                        title = text
                        break

            if not title:
                continue

            # ── Price ──────────────────────────────────────────────
            price_tag = card.select_one("span.a-price span.a-offscreen")
            price_text = price_tag.get_text(strip=True) if price_tag else None
            price_raw  = parse_price(price_text)

            if not price_raw:
                continue

            # ── Rating ─────────────────────────────────────────────
            rating = "N/A"
            rating_tag = card.select_one("span.a-icon-alt")
            if rating_tag:
                match = re.search(r"([\d.]+)\s*out of", rating_tag.get_text())
                rating = match.group(1) if match else "N/A"

            # ── Reviews ────────────────────────────────────────────
            reviews = "N/A"
            reviews_tag = card.select_one("span.a-size-base.s-underline-text")
            if reviews_tag:
                reviews = reviews_tag.get_text(strip=True)

            # ── Link ───────────────────────────────────────────────
            link_tag = card.select_one("a.a-link-normal.s-no-outline")
            if not link_tag:
                link_tag = card.select_one("h2 a")
            link = (
                "https://www.amazon.in" + link_tag["href"]
                if link_tag and link_tag.get("href", "").startswith("/")
                else search_url
            )

            # ── Image ──────────────────────────────────────────────
            img_tag = card.select_one("img.s-image")
            image = img_tag["src"] if img_tag and img_tag.get("src") else None

            results.append({
                "source":    "Amazon",
                "title":     title,
                "price":     price_text,
                "price_raw": price_raw,
                "rating":    rating,
                "reviews":   reviews,
                "link":      link,
                "image":     image,
                "best_deal": False,
            })

    except requests.exceptions.Timeout:
        print("[Amazon] Request timed out")
    except requests.exceptions.ConnectionError:
        print("[Amazon] Connection error")
    except Exception as e:
        print(f"[Amazon] Unexpected error: {e}")

    print(f"[Amazon] Returning {len(results)} results for '{query}'")
    return results
