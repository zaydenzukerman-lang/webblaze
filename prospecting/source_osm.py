#!/usr/bin/env python3
"""
WebBlaze lead sourcer (OpenStreetMap / Overpass) — free, no API key, no bot-blocking.
Pulls local businesses (with websites, often emails) for a niche across many cities.

Usage:
  python3 source_osm.py --cities cities.txt --out leads.csv [--tags PRESET]
  echo "Santa Ana\nTustin\nOrange" | python3 source_osm.py --out leads.csv

Output CSV columns: name,website,domain,email,phone,city,niche
Leads WITHOUT an email are still written (scan.sh can harvest one from the site later).
"""
import sys, json, csv, time, argparse, urllib.parse, urllib.request, re

OVERPASS = "https://overpass-api.de/api/interpreter"

# OSM tag filters by preset. These map to WebBlaze's ICP (old trades + small pro services).
PRESETS = {
    "trades": [
        'shop=upholsterer', 'shop=car_repair', 'craft=upholsterer', 'craft=electrician',
        'craft=plumber', 'craft=hvac', 'craft=carpenter', 'craft=metal_construction',
        'craft=blacksmith', 'craft=welder', 'craft=sawmill', 'craft=painter',
        'craft=roofer', 'craft=stonemason', 'shop=trade', 'shop=hardware',
        'shop=doityourself', 'craft=glaziery', 'craft=signmaker',
    ],
    "pro": [
        'office=lawyer', 'office=accountant', 'office=tax_advisor',
        'office=insurance', 'office=estate_agent', 'office=financial',
        'office=notary', 'office=employment_agency',
    ],
    "clinic": [
        'amenity=dentist', 'healthcare=dentist', 'amenity=veterinary',
        'healthcare=physiotherapist', 'shop=optician', 'healthcare=chiropractor',
    ],
    "local": [
        'shop=florist', 'shop=jewelry', 'shop=shoe_repair', 'craft=photographer',
        'shop=bakery', 'shop=furniture', 'shop=frame', 'craft=tailor',
    ],
}

def build_query(city, filters):
    parts = []
    for f in filters:
        k, v = f.split('=', 1)
        parts.append(f'  nwr(area.a)["{k}"="{v}"]["website"];')
    body = "\n".join(parts)
    # match city as administrative area by name
    return f'''[out:json][timeout:60];
area["name"="{city}"]["boundary"="administrative"]->.a;
(
{body}
);
out tags center 200;'''

def domain_of(url):
    try:
        d = urllib.parse.urlparse(url).netloc.lower()
        return d[4:] if d.startswith("www.") else d
    except Exception:
        return ""

def query_city(city, filters, niche_label):
    q = build_query(city, filters)
    data = urllib.parse.urlencode({"data": q}).encode()
    req = urllib.request.Request(OVERPASS, data=data,
        headers={"User-Agent": "WebBlaze-lead-sourcer/1.0 (contact hello@webblaze.io)"})
    try:
        raw = urllib.request.urlopen(req, timeout=90).read()
    except Exception as e:
        print(f"  ! {city}: {e}", file=sys.stderr); return []
    els = json.loads(raw).get("elements", [])
    rows = []
    for e in els:
        t = e.get("tags", {})
        site = t.get("website") or t.get("contact:website") or ""
        if not site.startswith("http"):
            continue
        rows.append({
            "name": t.get("name", "").strip(),
            "website": site.strip(),
            "domain": domain_of(site),
            "email": (t.get("email") or t.get("contact:email") or "").strip().lower(),
            "phone": (t.get("phone") or t.get("contact:phone") or "").strip(),
            "city": city,
            "niche": niche_label,
        })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cities", help="file of city names, one per line (else stdin)")
    ap.add_argument("--out", default="leads.csv")
    ap.add_argument("--tags", default="trades,pro,clinic,local",
                    help="comma list of presets: " + ",".join(PRESETS))
    args = ap.parse_args()

    if args.cities:
        cities = [c.strip() for c in open(args.cities) if c.strip()]
    else:
        cities = [c.strip() for c in sys.stdin if c.strip()]

    presets = [p.strip() for p in args.tags.split(",") if p.strip() in PRESETS]
    filters = []
    for p in presets:
        filters += PRESETS[p]
    niche_label = "+".join(presets)

    seen = set(); all_rows = []
    for i, city in enumerate(cities, 1):
        rows = query_city(city, filters, niche_label)
        fresh = 0
        for r in rows:
            key = r["domain"] or r["name"].lower()
            if not key or key in seen:
                continue
            seen.add(key); all_rows.append(r); fresh += 1
        print(f"[{i}/{len(cities)}] {city}: {len(rows)} found, {fresh} new (total {len(all_rows)})")
        time.sleep(1.2)  # be polite to Overpass

    with_email = sum(1 for r in all_rows if r["email"])
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name","website","domain","email","phone","city","niche"])
        w.writeheader(); w.writerows(all_rows)
    print(f"\nWROTE {len(all_rows)} unique leads -> {args.out}")
    print(f"  {with_email} already have an email in OSM; {len(all_rows)-with_email} need scan.sh to harvest one")

if __name__ == "__main__":
    main()
