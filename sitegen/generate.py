#!/usr/bin/env python3
"""
WebBlaze site factory — turn a client config (JSON) into a full, polished single-page site.
Usage:  python3 generate.py configs/<slug>.json
Output: ~/webblaze/public/<slug>/index.html  (+ img/ hero)

Every change a client emails (new phone, hours, a service, a photo, colors) is just a config
edit + re-run. No hand-coding. Sites differ by industry theme + their real content, so they
don't look cloned.
"""
import json, sys, os, re, html, urllib.request, urllib.parse

ROOT = os.path.expanduser("~/webblaze")
PEXELS = "85gzYeGliCl062HE8cT3bQZRphoW2iaH9pI2oxmLxJ7zE1KTttQe8eXL"

# ---- industry themes: (primary, dark, accent, hero search term) ----
THEMES = {
    "roofing":     ("#1f4e79", "#13314d", "#f5852a", "roofing house exterior"),
    "construction":("#334155", "#1e293b", "#f59e0b", "construction building"),
    "contractor":  ("#334155", "#1e293b", "#f59e0b", "contractor tools"),
    "hvac":        ("#1d4ed8", "#0f2a6b", "#ef4444", "air conditioning technician"),
    "air conditioning":("#1d4ed8","#0f2a6b","#ef4444","air conditioning unit"),
    "plumb":       ("#0369a1", "#083344", "#ef4444", "plumber pipes"),
    "electric":    ("#1e3a8a", "#111c44", "#facc15", "electrician wiring"),
    "law":         ("#0e2a47", "#08192b", "#c9a227", "law office courthouse"),
    "attorney":    ("#0e2a47", "#08192b", "#c9a227", "attorney office"),
    "dental":      ("#0e7490", "#083344", "#22d3ee", "dental office smile"),
    "dentist":     ("#0e7490", "#083344", "#22d3ee", "dentist clinic"),
    "chiro":       ("#0d9488", "#083d3a", "#f59e0b", "chiropractor wellness"),
    "landscap":    ("#166534", "#0b3d1f", "#eab308", "landscaping garden"),
    "lawn":        ("#166534", "#0b3d1f", "#eab308", "green lawn yard"),
    "auto":        ("#0f172a", "#020617", "#ef4444", "auto repair garage"),
    "upholst":     ("#7c2d12", "#3b160a", "#f59e0b", "furniture upholstery"),
    "weld":        ("#111827", "#030712", "#f97316", "welding metal fabrication"),
    "cabinet":     ("#78350f", "#3b1e08", "#f59e0b", "kitchen cabinets wood"),
    "sign":        ("#6d28d9", "#2e1065", "#f472b6", "sign shop storefront"),
    "pool":        ("#0891b2", "#083344", "#facc15", "swimming pool clean"),
    "pest":        ("#15803d", "#0b3d1f", "#f59e0b", "pest control home"),
    "floor":       ("#7c2d12", "#3b160a", "#d97706", "hardwood flooring"),
    "paint":       ("#1e3a8a", "#111c44", "#f97316", "house painting"),
    "clean":       ("#0e7490", "#083344", "#22d3ee", "cleaning service home"),
}
DEFAULT_THEME = ("#0f172a", "#020617", "#f59e0b", "modern local business storefront")

def theme_for(niche):
    n = (niche or "").lower()
    for k, v in THEMES.items():
        if k in n:
            return v
    return DEFAULT_THEME

def esc(s): return html.escape(str(s or ""))

def fetch_hero(term, out_path):
    """Download a landscape hero photo from Pexels. Returns True on success."""
    try:
        u = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
            {"query": term, "orientation": "landscape", "per_page": 5})
        req = urllib.request.Request(u, headers={"Authorization": PEXELS,
              "User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=20).read())
        photos = data.get("photos", [])
        if not photos: return False
        img_url = photos[0]["src"]["large2x"]
        req2 = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with open(out_path, "wb") as f:
            f.write(urllib.request.urlopen(req2, timeout=25).read())
        return True
    except Exception as e:
        print("  (hero image fetch failed: %s — using gradient)" % e)
        return False

def build(cfg):
    slug = cfg["slug"]
    site_dir = os.path.join(ROOT, "public", slug)
    img_dir = os.path.join(site_dir, "img")
    os.makedirs(img_dir, exist_ok=True)
    primary, dark, accent, hero_term = theme_for(cfg.get("niche"))
    if cfg.get("theme"):  # allow config override
        t = cfg["theme"]; primary=t.get("primary",primary); dark=t.get("dark",dark); accent=t.get("accent",accent)

    # hero image
    hero_ok = fetch_hero(cfg.get("hero_term") or hero_term, os.path.join(img_dir, "hero.jpg"))
    hero_bg = ("linear-gradient(120deg,rgba(0,0,0,.55),rgba(0,0,0,.35)),url('img/hero.jpg') center/cover"
               if hero_ok else "linear-gradient(120deg,%s,%s)" % (dark, primary))

    name = esc(cfg["business_name"]); phone = esc(cfg.get("phone","")); phone_link = re.sub(r"[^0-9+]","",cfg.get("phone",""))
    city = esc(cfg.get("city","")); tagline = esc(cfg.get("tagline") or ("%s you can count on in %s" % (cfg.get("niche","service").title(), cfg.get("city","your area"))))
    email = esc(cfg.get("email","")); address = esc(cfg.get("address",""))
    services = cfg.get("services") or []
    about = esc(cfg.get("about") or ("%s is a locally owned %s serving %s and the surrounding area. We take pride in quality work, fair pricing, and treating every customer right." % (cfg["business_name"], cfg.get("niche","business"), cfg.get("city","the community"))))
    hours = esc(cfg.get("hours",""))
    reviews = cfg.get("reviews") or []

    service_cards = "\n".join(
        '<div class="card"><div class="ci">%s</div><h3>%s</h3><p>%s</p></div>' % (
            (s.get("icon","✓") if isinstance(s,dict) else "✓"),
            esc(s.get("title") if isinstance(s,dict) else s),
            esc(s.get("desc","") if isinstance(s,dict) else ""))
        for s in services) or ""

    review_cards = "\n".join(
        '<div class="rev"><div class="stars">★★★★★</div><p>%s</p><b>%s</b></div>' % (
            esc(r.get("text") if isinstance(r,dict) else r),
            esc(r.get("name","") if isinstance(r,dict) else ""))
        for r in reviews)
    reviews_section = ('<section class="sec soft"><div class="wrap"><h2 class="center">What our customers say</h2><div class="revs">%s</div></div></section>' % review_cards) if reviews else ""

    hours_html = ('<div class="det"><b>Hours</b><span>%s</span></div>' % hours) if hours else ""
    addr_html = ('<div class="det"><b>Visit us</b><span>%s</span></div>' % address) if address else ""

    HERO_TERM_KEEP = hero_ok
    doc = TEMPLATE.format(
        name=name, tagline=tagline, phone=phone, phone_link=phone_link, city=city,
        email=email, primary=primary, dark=dark, accent=accent, hero_bg=hero_bg,
        service_cards=service_cards, about=about, reviews_section=reviews_section,
        hours_html=hours_html, addr_html=addr_html, year="2026",
        services_show=("block" if services else "none"))
    with open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    return site_dir

TEMPLATE = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} | {city}</title>
<meta name="description" content="{name} — {tagline}. Call {phone}.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{{--p:{primary};--d:{dark};--a:{accent};--ink:#0f172a;--mut:#64748b;--line:#e5e7eb}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Plus Jakarta Sans',system-ui,sans-serif;color:var(--ink);line-height:1.6}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 22px}}
a{{color:inherit}}
.btn{{display:inline-block;background:var(--a);color:#fff;font-weight:800;padding:14px 26px;border-radius:10px;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.18)}}
.btn.o{{background:transparent;border:2px solid #fff}}
header{{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid var(--line)}}
.nav{{display:flex;align-items:center;justify-content:space-between;padding:14px 0}}
.brand{{font-weight:800;font-size:1.25rem;color:var(--d)}}
.nav .call{{font-weight:800;color:var(--p);text-decoration:none}}
.hero{{background:{hero_bg};color:#fff}}
.hero-in{{padding:88px 0 96px;max-width:720px}}
.hero h1{{font-size:clamp(2rem,5vw,3.4rem);font-weight:800;line-height:1.1}}
.hero p{{font-size:1.2rem;margin:18px 0 28px;opacity:.95}}
.hero .row{{display:flex;gap:14px;flex-wrap:wrap}}
.trust{{background:var(--d);color:#fff}}
.trust .wrap{{display:flex;gap:26px;flex-wrap:wrap;justify-content:center;padding:16px 22px;font-weight:600;font-size:.95rem}}
.sec{{padding:72px 0}}
.sec.soft{{background:#f8fafc}}
h2{{font-size:clamp(1.6rem,3.4vw,2.3rem);font-weight:800;color:var(--d)}}
.center{{text-align:center}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;margin-top:34px;display:{services_show}}}
.card{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:26px;box-shadow:0 6px 20px rgba(2,6,23,.05)}}
.card .ci{{width:46px;height:46px;border-radius:12px;background:var(--p);color:#fff;display:grid;place-items:center;font-size:1.3rem;font-weight:800;margin-bottom:14px}}
.card h3{{font-size:1.15rem;color:var(--d)}}
.card p{{color:var(--mut);margin-top:6px}}
.about{{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:center}}
.about .box{{background:var(--d);color:#fff;border-radius:16px;padding:34px}}
.about .box .btn{{margin-top:16px}}
.revs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:30px}}
.rev{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:24px}}
.rev .stars{{color:var(--a)}}
.rev p{{margin:10px 0;color:#334155}}
.cta{{background:var(--p);color:#fff}}
.cta .wrap{{padding:64px 22px;text-align:center}}
.cta h2{{color:#fff}}
.cta .row{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:22px}}
.contact{{display:grid;grid-template-columns:1fr 1fr;gap:40px}}
.det{{display:flex;flex-direction:column;margin-bottom:18px}}
.det b{{color:var(--d)}}
.det span{{color:var(--mut)}}
form input,form textarea{{width:100%;padding:13px;border:1px solid var(--line);border-radius:10px;margin-top:10px;font:inherit}}
form button{{margin-top:14px;width:100%;border:0;cursor:pointer}}
footer{{background:var(--d);color:#cbd5e1;padding:30px 0;text-align:center}}
.mbar{{display:none}}
@media(max-width:820px){{.about,.contact{{grid-template-columns:1fr}}
 .nav .call{{display:none}}
 .mbar{{display:flex;position:fixed;bottom:0;left:0;right:0;z-index:30}}
 .mbar a{{flex:1;text-align:center;padding:15px;font-weight:800;text-decoration:none;color:#fff}}
 .mbar .c{{background:var(--p)}} .mbar .q{{background:var(--a)}}
 body{{padding-bottom:54px}}}}
</style></head><body>
<header><div class="wrap nav">
  <a class="brand" href="#">{name}</a>
  <a class="call" href="tel:{phone_link}">☎ {phone}</a>
</div></header>

<section class="hero"><div class="wrap hero-in">
  <h1>{tagline}</h1>
  <p>Serving {city} and nearby. Call today for a fast, free quote.</p>
  <div class="row">
    <a class="btn" href="tel:{phone_link}">Call {phone}</a>
    <a class="btn o" href="#contact">Get a Free Quote</a>
  </div>
</div></section>

<div class="trust"><div class="wrap">
  <span>★ Locally owned</span><span>✓ Licensed &amp; insured</span>
  <span>✓ Free estimates</span><span>✓ Fast response</span>
</div></div>

<section class="sec"><div class="wrap center">
  <h2>What we do</h2>
  <div class="cards">{service_cards}</div>
</div></section>

<section class="sec soft"><div class="wrap about">
  <div><h2>About {name}</h2><p style="margin-top:16px;color:#334155;font-size:1.05rem">{about}</p></div>
  <div class="box"><h3 style="font-size:1.3rem">Ready to get started?</h3>
    <p style="opacity:.9;margin-top:8px">Call now or request a free quote and we will get right back to you.</p>
    <a class="btn" href="tel:{phone_link}">Call {phone}</a></div>
</div></section>

{reviews_section}

<section class="cta"><div class="wrap">
  <h2>Get your free quote today</h2>
  <div class="row"><a class="btn o" href="tel:{phone_link}">Call {phone}</a>
    <a class="btn" href="#contact" style="background:#fff;color:var(--p)">Request Online</a></div>
</div></section>

<section class="sec" id="contact"><div class="wrap contact">
  <div><h2>Contact us</h2>
    <div style="margin-top:20px">
      <div class="det"><b>Call</b><span><a href="tel:{phone_link}" style="color:var(--p);font-weight:800;text-decoration:none">{phone}</a></span></div>
      {addr_html}{hours_html}
    </div>
  </div>
  <div><form onsubmit="this.innerHTML='<p style=\\'padding:20px 0\\'>Thanks! We will reach out shortly.</p>';return false">
    <input placeholder="Your name" required>
    <input placeholder="Phone number" required>
    <textarea placeholder="How can we help?" rows="4"></textarea>
    <button class="btn" type="submit">Send</button>
  </form></div>
</div></section>

<footer><div class="wrap">&copy; {year} {name}. Serving {city}. · <a href="tel:{phone_link}" style="color:#fff">{phone}</a></div></footer>
<div class="mbar"><a class="c" href="tel:{phone_link}">Call Now</a><a class="q" href="#contact">Free Quote</a></div>
</body></html>"""

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    d = build(cfg)
    print("built:", d + "/index.html")
    print("preview locally: open " + d + "/index.html")
