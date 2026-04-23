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
        "Referer": "https://www.flipkart.com/",
    }

def parse_price(price_str):
    """Extract a clean float from strings like ₹1,23,456"""
    if not price_str:
        return None
    cleaned = re.sub(r"[^\d.]", "", price_str.replace(",", ""))
    try:
        return float(cleaned)
    except ValueError:
        return None

def scrape_flipkart(query):
    search_url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
    results = []

    try:
        time.sleep(random.uniform(1, 2.5))

        session = requests.Session()

        # Flipkart sometimes shows a login popup — this first request
        # dismisses it by hitting the homepage once to set cookies
        session.get("https://www.flipkart.com", headers=get_headers(), timeout=10)

        response = session.get(search_url, headers=get_headers(), timeout=12)

        if response.status_code != 200:
            print(f"[Flipkart] Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "lxml")

        # Flipkart uses two card layouts depending on category
        # Layout A: grid cards (electronics, phones)
        # Layout B: list cards (books, accessories)
        product_cards = (
            soup.select("div.slAVV4")    # 2025 grid layout
            or soup.select("div.tUxRFH")
            or soup.select("div._1AtVbE")
            or soup.select("div._13oc-S")
            or soup.select("div._2kHMtA")
        )

        # Filter out empty/header cards
        product_cards = [
            c for c in product_cards
            if c.select_one("div._4rR01T, a.s1Q9rs, div.KzDlHZ, div._2WkVRV, div.wjcEIp")
        ]

        for card in product_cards[:6]:

            # ── Title ──────────────────────────────────────────────
            title_tag = (
                card.select_one("div.wjcEIp")    # 2025 layout
                or card.select_one("div._4rR01T")
                or card.select_one("a.s1Q9rs")
                or card.select_one("div.KzDlHZ")
                or card.select_one("div._2WkVRV")
            )
            title = title_tag.get_text(strip=True) if title_tag else None
            if not title:
                continue

            # ── Price ──────────────────────────────────────────────
            price_tag = (
                card.select_one("div._30jeq3")   # original price
                or card.select_one("div._25b18c") # discounted price
                or card.select_one("div.Nx9bqj")  # newer layout
                or card.select_one("div._16Jk6d")
            )
            price_text = price_tag.get_text(strip=True) if price_tag else None
            price_raw  = parse_price(price_text)

            if not price_raw:
                continue

            # ── Rating ─────────────────────────────────────────────
            rating_tag = (
                card.select_one("div._3LWZlK")  # star rating box
                or card.select_one("div.XQDdHH")
            )
            rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

            # ── Reviews count ──────────────────────────────────────
            reviews_tag = (
                card.select_one("span._2_R_DZ")
                or card.select_one("span.Wphh3N")
            )
            reviews = "N/A"
            if reviews_tag:
                # Extract just the number part e.g. "(12,345 Reviews)"
                match = re.search(r"[\d,]+", reviews_tag.get_text())
                reviews = match.group(0) if match else "N/A"

            # ── Discount label (bonus info) ────────────────────────
            discount_tag = (
                card.select_one("div._3Ay6Sb")
                or card.select_one("div.UkUFwK")
            )
            discount = discount_tag.get_text(strip=True) if discount_tag else None

            # ── Product link ───────────────────────────────────────
            link_tag = (
                card.select_one("a._1fQZEK")
                or card.select_one("a.s1Q9rs")
                or card.select_one("a._2rpwqI")
                or card.select_one("a")
            )
            link = (
                "https://www.flipkart.com" + link_tag["href"]
                if link_tag and link_tag.get("href", "").startswith("/")
                else search_url
            )

            # ── Image ──────────────────────────────────────────────
            img_tag = (
                card.select_one("img._396cs4")
                or card.select_one("img._2r_T1I")
                or card.select_one("img.DByuf4")
                or card.select_one("img")
            )
            image = img_tag["src"] if img_tag and img_tag.get("src") else None

            results.append({
                "source":    "Flipkart",
                "title":     title,
                "price":     price_text,
                "price_raw": price_raw,
                "rating":    rating,
                "reviews":   reviews,
                "discount":  discount,
                "link":      link,
                "image":     image,
                "best_deal": False,
            })

    except requests.exceptions.Timeout:
        print("[Flipkart] Request timed out")
    except requests.exceptions.ConnectionError:
        print("[Flipkart] Connection error")
    except Exception as e:
        print(f"[Flipkart] Unexpected error: {e}")

    print(f"[Flipkart] Found {len(results)} results for '{query}'")
    return results
