#!/usr/bin/env python3
"""Fetch REAL Google reviews for W Employment Law (Irvine) from Google Maps.

Usage:
    cd ~/webblaze && python3 sitegen/custom/wemploymentlaw/fetch_reviews.py
    # then rebuild the site:
    cd ~/webblaze && python3 sitegen/custom/wemploymentlaw/build.py

What it does:
  - Opens Google Maps (Playwright + Chromium), lands on the W Employment Law
    place panel (7700 Irvine Center Dr), records rating / review count /
    listing URL / place id.
  - Opens Reviews, sorts by Newest, scrolls, expands "More", and keeps up to
    12 five-star reviews with text (verbatim -- never edited).
  - Downloads reviewer avatars to public/wemploymentlaw/img/reviews/*.webp
  - Writes sitegen/custom/wemploymentlaw/reviews.json

Safe to re-run. On failure it exits non-zero and leaves any existing
reviews.json untouched. Debug screenshots go to $REVIEWS_DEBUG_DIR
(default: /tmp/wel_reviews_debug).
"""
import io
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]  # ~/webblaze
OUT_JSON = Path(__file__).resolve().parent / "reviews.json"
IMG_DIR = ROOT / "public" / "wemploymentlaw" / "img" / "reviews"
DEBUG_DIR = Path(os.environ.get("REVIEWS_DEBUG_DIR", "/tmp/wel_reviews_debug"))

QUERY = "W Employment Law 7700 Irvine Center Drive Irvine CA 92618"
NAME_RE = re.compile(r"W\s*Employment\s*Law", re.I)
ADDR_RE = re.compile(r"7700\s+Irvine\s+Center", re.I)
MAX_KEEP = 12
TARGET_LOADED = 60

PLACE_IDS = []

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")


def log(*a):
    print("[reviews]", *a, flush=True)


def shot(page, name):
    try:
        DEBUG_DIR.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(DEBUG_DIR / f"{name}.png"))
    except Exception as e:  # noqa: BLE001
        log("screenshot failed", name, e)


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s or "reviewer"


def handle_consent(page):
    if "consent.google" not in page.url:
        return
    log("consent page shown, accepting")
    for label in ("Accept all", "Reject all", "I agree"):
        btn = page.get_by_role("button", name=label)
        if btn.count():
            btn.first.click()
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)
            return


def ensure_place(page):
    """Make sure we are on the correct place panel (not a results list)."""
    page.wait_for_selector("h1", timeout=20000)
    time.sleep(2)
    h1s = page.locator("h1").all_inner_texts()
    if any(NAME_RE.search(t) for t in h1s):
        return True
    # Results list: click the matching result
    links = page.locator('a[href*="/maps/place/"]')
    for i in range(links.count()):
        lab = links.nth(i).get_attribute("aria-label") or ""
        if NAME_RE.search(lab):
            log("clicking result", lab)
            links.nth(i).click()
            page.wait_for_function(
                "() => [...document.querySelectorAll('h1')].some(h => /W\\s*Employment\\s*Law/i.test(h.innerText))",
                timeout=20000)
            time.sleep(2)
            return True
    return False


def place_info(page):
    info = {}
    info["place_name"] = next(
        (t.strip() for t in page.locator("h1").all_inner_texts() if NAME_RE.search(t)), None)
    addr_btn = page.locator('button[data-item-id="address"]')
    addr = None
    if addr_btn.count():
        addr = (addr_btn.first.get_attribute("aria-label") or "").replace("Address:", "").strip()
    info["address"] = addr
    # rating + count: look for aria-label like "4.9 stars" and "123 reviews"
    rating, total = None, None
    for el in page.locator('[role="img"][aria-label*="star"]').all()[:5]:
        m = re.search(r"([0-9.]+)\s*star", el.get_attribute("aria-label") or "")
        if m:
            rating = float(m.group(1))
            break
    # The header shows e.g. <span role="img" aria-label="119 reviews">
    for el in page.locator('[role="img"][aria-label$="reviews"]').all()[:10]:
        m = re.fullmatch(r"\s*([\d,]+)\s+reviews\s*", el.get_attribute("aria-label") or "")
        if m:
            total = int(m.group(1).replace(",", ""))
            break
    info["rating"], info["total_reviews"] = rating, total
    pid = re.search(r'(ChIJ[A-Za-z0-9_-]{20,})', page.content())
    info["place_id"] = PLACE_IDS[0] if PLACE_IDS else (pid.group(1) if pid else None)
    info["listing_url"] = page.url.split("?")[0] if "/maps/place/" in page.url else page.url
    # Stable short link: the hex feature id "0x...:0xCID" -> ?cid=<decimal>
    m = re.search(r"!1s0x[0-9a-f]+:(0x[0-9a-f]+)", page.url)
    info["cid_url"] = f"https://maps.google.com/?cid={int(m.group(1), 16)}" if m else None
    return info


def reviews_tab(page):
    return page.locator('button[role="tab"][aria-label^="Reviews"]')


def open_reviews(page):
    tab = reviews_tab(page)
    tab.first.click()
    page.wait_for_selector("div[data-review-id]", timeout=20000)
    time.sleep(2)
    sort = page.locator('button[aria-label*="Sort reviews"], button[aria-label="Most relevant"]')
    sort.first.click()
    newest = page.get_by_role("menuitemradio", name=re.compile("Newest", re.I))
    try:
        newest.first.wait_for(state="visible", timeout=6000)
    except Exception:  # noqa: BLE001
        # Logged-out sessions are sometimes A/B-gated: clicking Sort shows a
        # "Sign-in to get the best of Google Maps" modal instead of the menu.
        shot(page, "sort_gated")
        dismiss = page.get_by_role("button", name=re.compile("^Dismiss$", re.I))
        if dismiss.count():
            dismiss.first.click()
        raise RuntimeError("Sort menu gated behind sign-in modal (Google A/B); retrying fresh")
    newest.first.click()
    time.sleep(3)


def scroll_reviews(page):
    last, stable = 0, 0
    for _ in range(60):
        n = page.evaluate("""() => {
            const r = document.querySelector('div[data-review-id]');
            let el = r;
            while (el && !(el.scrollHeight > el.clientHeight + 50 &&
                   getComputedStyle(el).overflowY.match(/auto|scroll/))) el = el.parentElement;
            if (el) el.scrollTop = el.scrollHeight;
            return new Set([...document.querySelectorAll('div[data-review-id]')]
                .map(d => d.getAttribute('data-review-id'))).size;
        }""")
        if n >= TARGET_LOADED:
            break
        stable = stable + 1 if n == last else 0
        last = n
        if stable >= 6:
            break
        time.sleep(1.2)
    log("reviews loaded:", last)


def expand_more(page):
    for _ in range(3):
        btns = page.locator('div[data-review-id] button[aria-label="See more"], '
                            'div[data-review-id] button:has-text("More")')
        c = btns.count()
        if not c:
            return
        for i in range(c):
            try:
                btns.nth(i).click(timeout=1500)
            except Exception:  # noqa: BLE001
                pass
        time.sleep(0.8)


EXTRACT_JS = r"""() => {
  const out = []; const seen = new Set();
  for (const d of document.querySelectorAll('div[data-review-id]')) {
    const id = d.getAttribute('data-review-id');
    if (seen.has(id)) continue;
    // only top-level review containers (they have an aria-label = reviewer name)
    if (!d.getAttribute('aria-label')) continue;
    seen.add(id);
    const starEl = d.querySelector('[role="img"][aria-label*="star"]');
    const m = starEl ? (starEl.getAttribute('aria-label').match(/(\d)/)) : null;
    const img = d.querySelector('img[src*="googleusercontent"]');
    const prof = d.querySelector('button[data-href*="/contrib/"], a[href*="/contrib/"]');
    let dateText = null;
    if (starEl) {
      const sib = starEl.nextElementSibling;
      if (sib) dateText = sib.innerText.trim();
    }
    // review text: span inside the element with lang / id ending text
    let text = '';
    // first .wiI7pd is the reviewer's text (owner reply comes later in the DOM)
    const tEl = d.querySelector('span.wiI7pd') || d.querySelector('div[lang] > span, div[id] > span');
    if (tEl) text = tEl.innerText.trim();
    out.push({
      id, name: d.getAttribute('aria-label').trim(),
      rating: m ? parseInt(m[1]) : null,
      date_text: dateText,
      text,
      photo_src: img ? img.getAttribute('src') : null,
      profile_url: prof ? (prof.getAttribute('data-href') || prof.getAttribute('href')) : null,
    });
  }
  return out;
}"""


def upgrade_photo(url):
    if not url:
        return url
    if re.search(r"=[swh]\d+[^/]*$", url):
        return re.sub(r"=[^=/]*$", "=s240-c", url)
    return url + "=s240-c"


def is_default_avatar(img):
    """Detect Google's generated letter avatar (flat colour + one white letter).

    Real photos have many colours; letter avatars are ~1 background colour
    plus white/anti-aliased glyph pixels.
    """
    from collections import Counter
    small = img.convert("RGB").resize((48, 48))
    px = [small.getpixel((x, y)) for y in range(48) for x in range(48)]
    q = Counter((r // 16, g // 16, b // 16) for r, g, b in px)
    top = q.most_common(1)[0][1] / len(px)
    whiteish = sum(1 for r, g, b in px if min(r, g, b) > 225) / len(px)
    return top > 0.55 and top + whiteish > 0.8 and len(q) < 40


def download_photo(url, dest):
    from PIL import Image
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req, timeout=20).read()
    src = Image.open(io.BytesIO(data)).convert("RGBA")
    im = Image.new("RGB", src.size, (255, 255, 255))
    im.paste(src, mask=src.split()[3])
    default = is_default_avatar(im)
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    im = im.resize((120, 120), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=88)
    return default


def attempt(pw, headless, n):
    browser = pw.chromium.launch(headless=headless,
                                 args=["--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(user_agent=UA, locale="en-US",
                              timezone_id="America/Los_Angeles",
                              viewport={"width": 1440, "height": 900})
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    page = ctx.new_page()

    def on_resp(r):
        # The place id (ChIJ...) appears in the /maps/preview/place response.
        if "/maps/preview/place" in r.url:
            try:
                for m in re.findall(r"ChIJ[A-Za-z0-9_-]{20,}", r.text()):
                    if m not in PLACE_IDS:
                        PLACE_IDS.append(m)
            except Exception:  # noqa: BLE001
                pass
    page.on("response", on_resp)
    try:
        url = f"https://www.google.com/maps/search/{quote_plus(QUERY)}?hl=en&gl=us"
        log(f"attempt {n} headless={headless}:", url)
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(3)
        handle_consent(page)
        shot(page, f"a{n}_01_landing")
        if "/sorry/" in page.url:
            raise RuntimeError("Google /sorry/ block page")
        if not ensure_place(page):
            raise RuntimeError("could not find W Employment Law place panel")
        shot(page, f"a{n}_02_place")
        if True:
            # Google sometimes serves a "limited view" panel without the Reviews
            # tab (and fresh direct place loads never have it); loading the place
            # URL in the same session after the search reliably shows the tab.
            log("reloading place URL in same session")
            page.goto(page.url.split("?")[0] + "?hl=en&gl=us",
                      wait_until="domcontentloaded", timeout=45000)
            page.wait_for_selector("h1", timeout=20000)
            time.sleep(4)
            shot(page, f"a{n}_02b_place_reload")
            if not reviews_tab(page).count():
                raise RuntimeError("Reviews tab not available (limited view)")
        info = place_info(page)
        log("place info:", info)
        if not info["place_name"] or not (info["address"] and ADDR_RE.search(info["address"])):
            raise RuntimeError(f"wrong place? {info}")
        open_reviews(page)
        shot(page, f"a{n}_03_sorted")
        scroll_reviews(page)
        expand_more(page)
        first = page.locator("div[data-review-id][aria-label]").first
        if first.count():
            (DEBUG_DIR / "first_review.html").write_text(first.evaluate("e => e.outerHTML"))
        raw = page.evaluate(EXTRACT_JS)
        shot(page, f"a{n}_04_loaded")
        (DEBUG_DIR / "raw_reviews.json").write_text(json.dumps(raw, indent=2))
        return info, raw
    except Exception:
        shot(page, f"a{n}_zz_fail")
        raise
    finally:
        browser.close()


def main():
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    result, err = None, None
    with sync_playwright() as pw:
        # The Sort menu is randomly sign-in-gated (~50% of fresh sessions), so
        # retry with fresh browser contexts.
        for n, headless in enumerate([True, True, True, False, True, True, False, True], 1):
            PLACE_IDS.clear()
            try:
                result = attempt(pw, headless, n)
                break
            except Exception as e:  # noqa: BLE001
                err = e
                log(f"attempt {n} failed:", repr(e))
                time.sleep(4)
    if not result:
        log("FAILED -- reviews.json left untouched:", err)
        sys.exit(1)
    info, raw = result
    log(f"raw reviews: {len(raw)}")
    keep = [r for r in raw if r["rating"] == 5 and r["text"].strip()][:MAX_KEEP]
    if not keep:
        log("FAILED -- no 5-star reviews with text extracted; reviews.json untouched")
        sys.exit(1)

    reviews, used = [], set()
    for r in keep:
        slug = base = slugify(r["name"])
        i = 2
        while slug in used:
            slug, i = f"{base}-{i}", i + 1
        used.add(slug)
        src = upgrade_photo(r["photo_src"])
        photo, default = None, False
        if src:
            try:
                default = download_photo(src, IMG_DIR / f"{slug}.webp")
                # Custom uploaded photos live under /a-/ALV-...; generated letter
                # avatars are under /a/ACg8oc... -- require both signals.
                default = default and "/a-/" not in src
                photo = f"img/reviews/{slug}.webp"
            except Exception as e:  # noqa: BLE001
                log("photo download failed", r["name"], e)
        prof = r["profile_url"]
        if prof:
            prof = prof.split("?")[0]
        reviews.append({
            "name": r["name"], "photo": photo, "photo_src": src,
            "profile_url": prof, "rating": 5, "date_text": r["date_text"],
            "text": r["text"], "default_avatar": default,
        })

    pid = info["place_id"]
    out = {
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "Google Maps",
        "place_name": info["place_name"],
        "address": info["address"],
        "rating": info["rating"],
        "total_reviews": info["total_reviews"],
        "listing_url": info["listing_url"],
        "cid_url": info["cid_url"],
        "write_review_url": f"https://search.google.com/local/writereview?placeid={pid}" if pid else None,
        "place_id": pid,
        "reviews": reviews,
    }
    tmp = OUT_JSON.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    tmp.replace(OUT_JSON)
    log(f"wrote {OUT_JSON} with {len(reviews)} reviews")


if __name__ == "__main__":
    main()
