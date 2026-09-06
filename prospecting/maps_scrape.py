#!/usr/bin/env python3
# Scrape Google Maps for local businesses' WEBSITES (bypasses the 403s that block curl).
# Usage: python3 maps_scrape.py "<niche>" "<city> FL"   -> prints website domains
import sys, re, time, urllib.parse
from playwright.sync_api import sync_playwright

def domain_of(url):
    try:
        d = urllib.parse.urlparse(url).netloc.lower()
        return d[4:] if d.startswith("www.") else d
    except Exception:
        return ""

SKIP = ("google.","gstatic","schema.org","w3.org","youtube","facebook","instagram")

def scrape(query, max_scrolls=12):
    url = "https://www.google.com/maps/search/" + urllib.parse.quote(query)
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page(locale="en-US")
        pg.goto(url, timeout=45000)
        # consent screen (EU) — click if present
        try:
            pg.click('button[aria-label*="Accept"], form[action*="consent"] button', timeout=3000)
        except Exception:
            pass
        try:
            pg.wait_for_selector('div[role="feed"]', timeout=15000)
        except Exception:
            pass
        feed = 'div[role="feed"]'
        seen_h = 0
        for _ in range(max_scrolls):
            try:
                pg.eval_on_selector(feed, "el => el.scrollBy(0, el.scrollHeight)")
            except Exception:
                break
            time.sleep(1.4)
            h = pg.eval_on_selector(feed, "el => el.scrollHeight") if pg.query_selector(feed) else 0
            if h == seen_h:
                break
            seen_h = h
        # website links live on each card as an anchor with a real (non-google) href
        hrefs = pg.eval_on_selector_all(
            'a[href^="http"]',
            "els => els.map(a => a.href)")
        b.close()
    doms = []
    for h in hrefs:
        d = domain_of(h)
        if d and not any(s in d for s in SKIP) and "." in d:
            doms.append(d)
    # dedupe preserve order
    seen = set(); res = []
    for d in doms:
        if d not in seen:
            seen.add(d); res.append(d)
    return res

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "roofing contractor Miami FL"
    for d in scrape(q):
        print(d)
