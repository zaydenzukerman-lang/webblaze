#!/usr/bin/env python3
"""Andre — WebBlaze site generator.
Turns a client intake JSON into a complete, responsive, conversion-focused website.
Usage: python3 generate.py clients/<slug>.json  ->  output/<slug>/index.html
Design: client's brand color drives the theme; every section is data-driven.
"""
import json, sys, os, html

def esc(s): return html.escape(str(s), quote=True)

def services_html(services):
    out = []
    for s in services:
        out.append(f'''      <div class="svc">
        <div class="svc-ic">{esc(s.get("icon","✓"))}</div>
        <h3>{esc(s["name"])}</h3>
        <p>{esc(s.get("desc",""))}</p>
      </div>''')
    return "\n".join(out)

def why_html(points):
    return "\n".join(f'        <li><span class="ck">✓</span>{esc(p)}</li>' for p in points)

def reviews_html(reviews):
    out = []
    for r in reviews:
        initial = esc(r["author"][0]) if r.get("author") else "★"
        out.append(f'''      <div class="rev">
        <div class="stars">★★★★★</div>
        <p>{esc(r["text"])}</p>
        <div class="who"><span class="av">{initial}</span>{esc(r.get("author",""))}</div>
      </div>''')
    return "\n".join(out)

def build(c):
    tel = "".join(ch for ch in c["phone"] if ch.isdigit())
    hero_bg = f"background-image:url('{esc(c['hero_image'])}');" if c.get("hero_image") else ""
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(c["name"])} — {esc(c.get("tagline",""))}</title>
<meta name="description" content="{esc(c["name"])} in {esc(c.get("city",""))}. {esc(c.get("tagline",""))} Call {esc(c["phone"])}.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--brand:{esc(c.get("brand","#1f6feb"))};--brand-d:{esc(c.get("brand_dark",c.get("brand","#1a5fd0")))};
  --ink:#14181f;--muted:#5d6670;--line:#e7e9ee;--paper:#ffffff;--soft:#f5f7fa;--gold:#f5a623}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,system-ui,Arial,sans-serif;color:var(--ink);background:var(--paper);line-height:1.6;-webkit-font-smoothing:antialiased}}
h1,h2,h3{{font-family:"Plus Jakarta Sans",sans-serif;margin:0;line-height:1.15;letter-spacing:-.01em}}
a{{color:inherit;text-decoration:none}}img{{max-width:100%;display:block}}
.wrap{{max-width:1140px;margin:0 auto;padding:0 22px}}
.btn{{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-family:"Plus Jakarta Sans",sans-serif;padding:13px 22px;border-radius:9px;cursor:pointer;transition:.15s;border:0}}
.btn-brand{{background:var(--brand);color:#fff}}.btn-brand:hover{{background:var(--brand-d)}}
.btn-out{{background:#fff;color:var(--ink);border:1.5px solid var(--line)}}.btn-out:hover{{border-color:var(--brand);color:var(--brand)}}
.topbar{{background:var(--ink);color:#dfe4ea;font-size:.86rem}}
.topbar .wrap{{display:flex;justify-content:space-between;align-items:center;height:38px;gap:14px;flex-wrap:wrap}}
.topbar b{{color:#fff}}
header.nav{{position:sticky;top:0;z-index:40;background:#fff;box-shadow:0 1px 0 var(--line)}}
.nav-in{{display:flex;align-items:center;justify-content:space-between;height:70px}}
.brand-logo{{font-family:"Plus Jakarta Sans";font-weight:800;font-size:1.25rem;display:flex;align-items:center;gap:9px}}
.brand-logo .dot{{width:30px;height:30px;border-radius:8px;background:var(--brand);color:#fff;display:grid;place-items:center;font-size:1rem}}
.nav-links{{display:flex;gap:26px;font-weight:600;font-size:.95rem}}.nav-links a:hover{{color:var(--brand)}}
.nav-cta{{display:flex;align-items:center;gap:14px}}
.hero{{position:relative;color:#fff;padding:92px 0 100px;{hero_bg}background-size:cover;background-position:center}}
.hero:before{{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(10,14,20,.88),rgba(10,14,20,.55) 60%,rgba(10,14,20,.25))}}
.hero-in{{position:relative;max-width:640px}}
.hero .eyebrow{{color:#fff;background:var(--brand);display:inline-block;font-weight:700;font-size:.8rem;letter-spacing:.04em;padding:5px 12px;border-radius:6px}}
.hero h1{{font-size:clamp(2.1rem,5vw,3.4rem);font-weight:800;margin:16px 0 0}}
.hero p{{font-size:1.15rem;color:#eaeef3;margin:14px 0 0;max-width:52ch}}
.hero-cta{{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}}
.hero-cta .btn-out{{background:transparent;color:#fff;border-color:rgba(255,255,255,.5)}}
.trust{{background:var(--soft);border-bottom:1px solid var(--line)}}
.trust .wrap{{display:flex;flex-wrap:wrap;justify-content:center;gap:14px 40px;padding:16px 22px;font-weight:600;font-size:.95rem;color:var(--ink)}}
.trust span{{display:flex;align-items:center;gap:8px}}.trust .g{{color:var(--brand);font-weight:800}}
section{{padding:76px 0}}
.sec-head{{text-align:center;max-width:640px;margin:0 auto 44px}}
.sec-head .eyebrow{{color:var(--brand);font-weight:700;font-size:.82rem;letter-spacing:.12em;text-transform:uppercase}}
.sec-head h2{{font-size:clamp(1.7rem,3.6vw,2.5rem);font-weight:800;margin:8px 0 0}}
.sec-head p{{color:var(--muted);margin:12px 0 0;font-size:1.05rem}}
.svc-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
.svc{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:26px 24px;transition:.16s}}
.svc:hover{{border-color:var(--brand);box-shadow:0 12px 30px rgba(20,24,31,.08);transform:translateY(-3px)}}
.svc-ic{{width:46px;height:46px;border-radius:11px;background:color-mix(in srgb,var(--brand) 14%,#fff);color:var(--brand);display:grid;place-items:center;font-size:1.3rem;font-weight:800}}
.svc h3{{font-size:1.2rem;margin:16px 0 6px}}.svc p{{color:var(--muted);margin:0;font-size:.98rem}}
.split{{display:grid;grid-template-columns:1fr 1fr;gap:50px;align-items:center}}
.split .ph{{border-radius:16px;min-height:380px;background-size:cover;background-position:center;box-shadow:0 20px 44px rgba(20,24,31,.14)}}
.why-list{{list-style:none;padding:0;margin:22px 0 0;display:grid;gap:13px}}
.why-list li{{display:flex;gap:12px;align-items:flex-start;font-size:1.05rem;font-weight:500}}
.why-list .ck{{flex:0 0 26px;width:26px;height:26px;border-radius:50%;background:var(--brand);color:#fff;display:grid;place-items:center;font-weight:800;font-size:.8rem;margin-top:2px}}
.reviews{{background:var(--soft)}}
.rev-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
.rev{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:24px}}
.stars{{color:var(--gold);letter-spacing:2px}}
.rev p{{font-size:1.02rem;margin:12px 0 0;color:#333}}
.rev .who{{margin-top:16px;font-weight:700;display:flex;align-items:center;gap:10px}}
.rev .av{{width:34px;height:34px;border-radius:50%;background:var(--brand);color:#fff;display:grid;place-items:center;font-weight:700}}
.cta-band{{background:var(--brand);color:#fff;text-align:center}}
.cta-band h2{{font-size:clamp(1.7rem,4vw,2.6rem);font-weight:800}}
.cta-band p{{opacity:.92;font-size:1.1rem;margin:12px 0 0}}
.cta-band .btn{{background:#fff;color:var(--brand);margin-top:24px;font-size:1.05rem;padding:15px 30px}}
.contact-grid{{display:grid;grid-template-columns:1fr 1fr;gap:44px}}
.info-row{{display:flex;gap:14px;padding:16px 0;border-bottom:1px solid var(--line)}}
.info-row .ic{{width:44px;height:44px;border-radius:11px;background:var(--soft);color:var(--brand);display:grid;place-items:center;font-size:1.2rem;flex:0 0 44px}}
.info-row b{{display:block;font-family:"Plus Jakarta Sans";font-size:1.05rem}}
.info-row span{{color:var(--muted)}}
.form{{background:var(--soft);border:1px solid var(--line);border-radius:16px;padding:28px}}
.field{{width:100%;padding:12px 14px;border:1px solid var(--line);border-radius:9px;font:inherit;margin-top:10px;background:#fff}}
.field:focus{{outline:0;border-color:var(--brand)}}
footer{{background:var(--ink);color:#9aa3af;padding:44px 0 28px;font-size:.95rem}}
.foot-in{{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:center}}
footer .brand-logo{{color:#fff}}
.foot-disc{{border-top:1px solid #262c35;margin-top:24px;padding-top:18px;font-size:.82rem;color:#69727d}}
.mbar{{display:none}}
@media(max-width:900px){{
  .nav-links{{display:none}}.svc-grid,.rev-grid{{grid-template-columns:1fr}}
  .split,.contact-grid{{grid-template-columns:1fr}}.split .ph{{min-height:240px;order:-1}}
  section{{padding:56px 0}}.nav-cta .btn-out{{display:none}}
  .mbar{{display:grid;grid-template-columns:1fr 1fr;gap:8px;position:fixed;bottom:0;left:0;right:0;z-index:60;background:#fff;padding:9px;box-shadow:0 -4px 20px rgba(0,0,0,.15)}}
  body{{padding-bottom:72px}}
}}
</style></head>
<body>
<div class="topbar"><div class="wrap"><span>\U0001f4cd {esc(c.get("address",""))}</span><span>\U0001f552 <b>{esc(c.get("hours",""))}</b></span></div></div>
<header class="nav"><div class="wrap nav-in">
  <a class="brand-logo" href="#"><span class="dot">{esc(c["name"][0])}</span>{esc(c["name"])}</a>
  <nav class="nav-links"><a href="#services">Services</a><a href="#why">Why Us</a><a href="#reviews">Reviews</a><a href="#contact">Contact</a></nav>
  <div class="nav-cta"><a class="btn btn-out" href="tel:{tel}">\U0001f4de {esc(c["phone"])}</a><a class="btn btn-brand" href="#contact">{esc(c.get("cta","Get a Quote"))}</a></div>
</div></header>

<section class="hero"><div class="wrap hero-in">
  <span class="eyebrow">{esc(c.get("badge","Locally owned & trusted"))}</span>
  <h1>{esc(c.get("headline",c["name"]))}</h1>
  <p>{esc(c.get("tagline",""))}</p>
  <div class="hero-cta"><a class="btn btn-brand" href="#contact">{esc(c.get("cta","Get a Free Quote"))}</a><a class="btn btn-out" href="tel:{tel}">Call {esc(c["phone"])}</a></div>
</div></section>

<div class="trust"><div class="wrap">
  <span><i class="g">★★★★★</i> Trusted by {esc(c.get("city","local"))} customers</span>
  <span><i class="g">✓</i> Serving {esc(c.get("city",""))} since {esc(c.get("years",""))}</span>
  <span><i class="g">✓</i> Free estimates</span>
  <span><i class="g">✓</i> Licensed &amp; insured</span>
</div></div>

<section id="services"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">What we do</div><h2>Our Services</h2><p>Everything you need, done right the first time.</p></div>
  <div class="svc-grid">
{services_html(c.get("services",[]))}
  </div>
</div></section>

<section id="why" style="background:var(--soft)"><div class="wrap"><div class="split">
  <div>
    <div class="eyebrow" style="color:var(--brand);font-weight:700;font-size:.82rem;letter-spacing:.12em;text-transform:uppercase">Why {esc(c["name"])}</div>
    <h2 style="font-size:clamp(1.7rem,3.6vw,2.4rem);font-weight:800;margin:8px 0 0;font-family:'Plus Jakarta Sans'">{esc(c.get("why_head","The name your neighbors trust"))}</h2>
    <p style="color:var(--muted);margin-top:12px">{esc(c.get("about",""))}</p>
    <ul class="why-list">
{why_html(c.get("why",[]))}
    </ul>
  </div>
  <div class="ph" style="background-image:url('{esc(c.get("about_image",c.get("hero_image","")))}')"></div>
</div></div></section>

<section class="reviews" id="reviews"><div class="wrap">
  <div class="sec-head"><div class="eyebrow">Reviews</div><h2>What our customers say</h2></div>
  <div class="rev-grid">
{reviews_html(c.get("reviews",[]))}
  </div>
</div></section>

<section class="cta-band"><div class="wrap">
  <h2>{esc(c.get("cta_head","Ready to get started?"))}</h2>
  <p>Call now or request a free quote — we'll take care of the rest.</p>
  <a class="btn" href="tel:{tel}">\U0001f4de Call {esc(c["phone"])}</a>
</div></section>

<section id="contact"><div class="wrap"><div class="contact-grid">
  <div>
    <div class="eyebrow" style="color:var(--brand);font-weight:700;font-size:.82rem;letter-spacing:.12em;text-transform:uppercase">Get in touch</div>
    <h2 style="font-size:clamp(1.7rem,3.6vw,2.3rem);font-weight:800;margin:8px 0 18px;font-family:'Plus Jakarta Sans'">Contact {esc(c["name"])}</h2>
    <div class="info-row"><div class="ic">\U0001f4de</div><div><b><a href="tel:{tel}">{esc(c["phone"])}</a></b><span>Call or text us anytime</span></div></div>
    <div class="info-row"><div class="ic">\U0001f4cd</div><div><b>{esc(c.get("address",""))}</b><span>Serving {esc(c.get("city",""))} &amp; nearby</span></div></div>
    <div class="info-row"><div class="ic">\U0001f552</div><div><b>{esc(c.get("hours",""))}</b><span>Business hours</span></div></div>
    <div class="info-row"><div class="ic">✉️</div><div><b><a href="mailto:{esc(c.get("email",""))}">{esc(c.get("email",""))}</a></b><span>Email us</span></div></div>
  </div>
  <form class="form" onsubmit="event.preventDefault();this.innerHTML='<h3 style=&quot;font-family:Plus Jakarta Sans&quot;>Thanks!</h3><p style=&quot;color:#5d6670&quot;>We got your request and will reach out shortly. Prefer to talk now? Call <b>{esc(c["phone"])}</b>.</p>'">
    <h3 style="font-family:'Plus Jakarta Sans';font-size:1.3rem">{esc(c.get("cta","Request a Free Quote"))}</h3>
    <input class="field" placeholder="Your name" required>
    <input class="field" type="tel" placeholder="Phone number" required>
    <textarea class="field" rows="3" placeholder="How can we help?"></textarea>
    <button class="btn btn-brand" type="submit" style="width:100%;margin-top:12px">{esc(c.get("cta","Send Request"))}</button>
  </form>
</div></div></section>

<footer><div class="wrap">
  <div class="foot-in">
    <a class="brand-logo" href="#"><span class="dot">{esc(c["name"][0])}</span>{esc(c["name"])}</a>
    <div><a class="btn btn-brand" href="tel:{tel}">\U0001f4de Call {esc(c["phone"])}</a></div>
  </div>
  <div class="foot-disc">© <span id="yr"></span> {esc(c["name"])} · {esc(c.get("address",""))} · Serving {esc(c.get("city",""))} since {esc(c.get("years",""))}. Website by WebBlaze.</div>
</div></footer>
<div class="mbar"><a class="btn btn-out" href="tel:{tel}">\U0001f4de Call</a><a class="btn btn-brand" href="#contact">{esc(c.get("cta","Free Quote"))}</a></div>
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>
</body></html>'''

def main():
    path = sys.argv[1]
    c = json.load(open(path))
    outdir = os.path.join(os.path.dirname(__file__), "output", c["slug"])
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir,"index.html"),"w").write(build(c))
    print("built:", os.path.join(outdir,"index.html"))

if __name__ == "__main__":
    main()
