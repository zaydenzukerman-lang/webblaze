import pathlib, re, html

ADDR = dict(street="3525 N. Causeway Blvd, Suite 900", city="Metairie", region="LA", zip="70002")
SITES = {
 "sunmortgagefunding": dict(name="Sun Mortgage Funding", tel="+1-504-837-3939",
   sameas="https://sunmortgagefunding.webblaze.io", price="$$",
   others=["https://sunpremium.webblaze.io","https://sunfinance.webblaze.io"]),
 "sunpremium": dict(name="Sun Premium Financing", tel="+1-504-834-9400",
   sameas="https://sunpremium.webblaze.io", price="$$",
   others=["https://sunmortgagefunding.webblaze.io","https://sunfinance.webblaze.io"]),
 "sunfinance": dict(name="Sun Finance", tel="+1-504-837-9400",
   sameas="https://sunfinance.webblaze.io", price="$$",
   others=["https://sunmortgagefunding.webblaze.io","https://sunpremium.webblaze.io"]),
}
ROOT = pathlib.Path("/Users/zaydenzukerman/webblaze/public")
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta name="description" content="(.*?)"', re.S)

def canon(base, fn):
    return f"{base}/" if fn == "index.html" else f"{base}/{fn}"

def jsonld(s, base):
    import json
    d = {
      "@context":"https://schema.org","@type":"FinancialService",
      "name":s["name"],"url":base,"telephone":s["tel"],
      "foundingDate":"1958","priceRange":s["price"],
      "areaServed":{"@type":"State","name":"Louisiana"},
      "address":{"@type":"PostalAddress","streetAddress":ADDR["street"],
        "addressLocality":ADDR["city"],"addressRegion":ADDR["region"],
        "postalCode":ADDR["zip"],"addressCountry":"US"},
      "openingHoursSpecification":{"@type":"OpeningHoursSpecification",
        "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],
        "opens":"09:00","closes":"17:00"},
      "sameAs":s["others"],
    }
    # unescape HTML entities in name for valid JSON text
    d["name"] = html.unescape(d["name"])
    return '<script type="application/ld+json">'+json.dumps(d,separators=(",",":"))+'</script>'

def head_block(s, base, title, desc, fn):
    c = canon(base, fn)
    t = html.unescape(title); dsc = html.unescape(desc)
    tags = [
      f'<link rel="canonical" href="{c}">',
      '<meta name="robots" content="noindex,follow"><!-- PREVIEW demo: flip to index,follow when deployed to client\'s live domain -->',
      '<meta property="og:type" content="website">',
      f'<meta property="og:site_name" content="{s["name"]}">',
      f'<meta property="og:title" content="{title}">',
      f'<meta property="og:description" content="{desc}">',
      f'<meta property="og:url" content="{c}">',
      f'<meta property="og:image" content="{base}/img/favicon-192.png">',
      '<meta name="twitter:card" content="summary">',
      f'<meta name="twitter:title" content="{title}">',
      f'<meta name="twitter:description" content="{desc}">',
    ]
    if fn == "index.html":
        tags.append(jsonld(s, base))
    return "".join(tags)

def robots(base):
    return f"User-agent: *\nDisallow:\n\nSitemap: {base}/sitemap.xml\n"

def sitemap(base, files):
    urls = "".join(f"  <url><loc>{canon(base,f)}</loc><changefreq>monthly</changefreq><priority>{'1.0' if f=='index.html' else '0.8'}</priority></url>\n" for f in files)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'

for slug, s in SITES.items():
    d = ROOT / slug
    base = s["sameas"]
    files = sorted([p.name for p in d.glob("*.html")])
    # order: index first
    files = (["index.html"] if "index.html" in files else []) + [f for f in files if f != "index.html"]
    for fn in files:
        p = d / fn
        txt = p.read_text()
        if 'rel="canonical"' in txt:
            print(f"skip (already done) {slug}/{fn}"); continue
        title = (TITLE_RE.search(txt).group(1) if TITLE_RE.search(txt) else s["name"]).strip()
        desc = (DESC_RE.search(txt).group(1) if DESC_RE.search(txt) else "").strip()
        block = head_block(s, base, title, desc, fn)
        txt = txt.replace("</head>", block + "</head>", 1)
        p.write_text(txt)
        print(f"inject {slug}/{fn}  (+{len(block)} bytes)")
    (d / "robots.txt").write_text(robots(base)); print(f"  wrote {slug}/robots.txt")
    (d / "sitemap.xml").write_text(sitemap(base, files)); print(f"  wrote {slug}/sitemap.xml ({len(files)} urls)")
