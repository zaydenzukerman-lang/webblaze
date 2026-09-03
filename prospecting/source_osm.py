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
import sys, json, csv, time, argparse, urllib.parse, urllib.request, urllib.error, re

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.osm.jp/api/interpreter",
]
_ep_idx = [0]

# OSM tag filters by preset. These map to WebBlaze's ICP (old trades + small pro services).
PRESETS = {
    "trades": [
        'shop=upholsterer', 'shop=car_repair', 'craft=upholsterer', 'craft=electrician',
        'craft=plumber', 'craft=hvac', 'craft=carpenter', 'craft=metal_construction',
        'craft=blacksmith', 'craft=welder', 'craft=sawmill', 'craft=painter',
        'craft=roofer', 'craft=stonemason', 'shop=trade', 'shop=hardware',
        'shop=doityourself', 'craft=glaziery', 'craft=signmaker',
        'craft=tiler', 'craft=plasterer', 'craft=cabinet_maker', 'craft=locksmith',
        'craft=gardener', 'craft=insulation', 'craft=scaffolder', 'craft=floorer',
        'craft=window_construction', 'craft=heating_engineer', 'craft=key_cutter',
        'shop=locksmith', 'shop=paint', 'shop=fireplace', 'shop=doors', 'shop=pool',
        'shop=kitchen', 'shop=bathroom_furnishing', 'shop=window_blind', 'shop=tyres',
        'shop=fabric', 'shop=sewing', 'shop=trophy', 'shop=security',
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
        'shop=dry_cleaning', 'shop=laundry', 'shop=travel_agency', 'shop=music',
        'shop=musical_instrument', 'shop=pet', 'shop=pet_grooming', 'shop=garden_centre',
        'shop=hairdresser', 'shop=beauty', 'shop=car_parts', 'shop=antiques',
        'shop=appliance', 'shop=vacuum_cleaner', 'shop=bicycle', 'shop=computer',
        'craft=confectionery', 'craft=jeweller', 'craft=watchmaker', 'office=travel_agent',
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

CHAINS = set(x.strip() for x in """
disney.go.com pandora.net starbucks.com mcdonalds.com subway.com dominos.com
walmart.com target.com cvs.com walgreens.com homedepot.com lowes.com bestbuy.com
 upsstore.com fedex.com autozone.com oreillyauto.com jiffylube.com midas.com
h&rblock.com hrblock.com jacksonhewitt.com edwardjones.com statefarm.com
allstate.com geico.com farmers.com pandora.net verizon.com att.com t-mobile.com
7-eleven.com dennys.com ihop.com wendys.com burgerking.com tacobell.com kfc.com
chase.com wellsfargo.com bankofamerica.com regions.com pnc.com citibank.com
uhaul.com penske.com enterprise.com hertz.com avis.com massageenvy.com
anytimefitness.com planetfitness.com lafitness.com orangetheory.com
greatclips.com supercuts.com sportclips.com europeanwax.com
firestone.com goodyear.com discounttire.com pepboys.com meineke.com aamco.com
century21.com coldwellbanker.com kw.com remax.com compass.com redfin.com zillow.com
""".split())

def is_chain(domain):
    d = domain.lower()
    return any(d == c or d.endswith("." + c) for c in CHAINS)

# franchise / dealership / national brands by NAME (OSM name substring, lowercased)
NAME_BLOCK = [
 "ace hardware","jiffy lube","firestone","midas","aamco","meineke","pep boys",
 "valvoline","u-haul","uhaul","penske","enterprise rent","hertz","avis","budget rent",
 "napa auto","o'reilly","oreilly","autozone","advance auto","mavis","discount tire",
 "tire kingdom","goodyear","big o tires","take 5","grease monkey","tires plus",
 "alfa romeo","fiat","ford","toyota","honda","nissan","chevrolet","chevy","hyundai",
 "kia ","bmw","mercedes","volkswagen","mazda","subaru","jeep","dodge","chrysler",
 "cadillac","buick","gmc","lexus","acura","infiniti","mitsubishi","volvo","audi",
 "porsche","land rover","jaguar","genesis","ram truck","lincoln","mini cooper",
 "7-eleven","circle k","wawa","dunkin","starbucks","mcdonald","burger king","wendy",
 "subway","domino","pizza hut","papa john","little caesar","taco bell","kfc","popeyes",
 "chick-fil","panera","chipotle","five guys","wingstop","planet fitness","la fitness",
 "anytime fitness","orangetheory","crunch fitness","massage envy","great clips",
 "supercuts","sport clips","european wax","the ups store","fedex office","h&r block",
 "jackson hewitt","edward jones","state farm","allstate","geico","farmers insurance",
 "re/max","remax","century 21","keller williams","coldwell banker","exp realty",
]
def is_brand_name(name):
    n = (name or "").lower()
    return any(b in n for b in NAME_BLOCK)

FOREIGN_TLD = (".au",".es",".uk",".ca",".de",".fr",".it",".mx",".br",".in",".nz",".co.uk",".ie",".pt",".nl",".be",".ch",".ar",".cl",".co")
def is_foreign(domain):
    d = domain.lower()
    return any(d.endswith(t) for t in FOREIGN_TLD)

# email domains belonging to web agencies / builders (false "owner" emails)
EMAIL_BLOCK = ["pixelmotion.com","godaddy.com","wix.com","squarespace.com","weebly.com",
    "duda.co","dudamobile.com","vistaprint.com","networksolutions.com","web.com",
    "thryv.com","yodle.com","hibu.com","reachlocal.com","townsquareinteractive.com",
    "sitemason.com","example.com","sentry.io","wordpress.com"]
def bad_email(email):
    e = (email or "").lower()
    if not e or "@" not in e: return True
    dom = e.split("@")[-1]
    return any(dom == b or dom.endswith("." + b) for b in EMAIL_BLOCK)

def domain_of(url):
    try:
        d = urllib.parse.urlparse(url).netloc.lower()
        return d[4:] if d.startswith("www.") else d
    except Exception:
        return ""

def _fetch(q):
    data = urllib.parse.urlencode({"data": q}).encode()
    last = None
    for attempt in range(5):
        ep = OVERPASS_ENDPOINTS[_ep_idx[0] % len(OVERPASS_ENDPOINTS)]
        req = urllib.request.Request(ep, data=data,
            headers={"User-Agent": "WebBlaze-lead-sourcer/1.0 (hello@webblaze.io)"})
        try:
            return urllib.request.urlopen(req, timeout=120).read()
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 504, 502, 503):
                _ep_idx[0] += 1                      # rotate endpoint
                time.sleep(min(60, 8 * (attempt + 1)))  # backoff
                continue
            raise
        except Exception as e:
            last = e; _ep_idx[0] += 1; time.sleep(6)
    raise last

def query_city(city, filters, niche_label):
    q = build_query(city, filters)
    try:
        raw = _fetch(q)
    except Exception as e:
        print(f"  ! {city}: {e}", file=sys.stderr); return []
    els = json.loads(raw).get("elements", [])
    rows = []
    for e in els:
        t = e.get("tags", {})
        site = t.get("website") or t.get("contact:website") or ""
        if not site.startswith("http"):
            continue
        dom = domain_of(site)
        if not dom or is_chain(dom) or is_foreign(dom) or is_brand_name(t.get("name", "")):
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
        sys.stdout.flush()
        time.sleep(4)  # be polite to Overpass (avoid 429)

    with_email = sum(1 for r in all_rows if r["email"])
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name","website","domain","email","phone","city","niche"])
        w.writeheader(); w.writerows(all_rows)
    print(f"\nWROTE {len(all_rows)} unique leads -> {args.out}")
    print(f"  {with_email} already have an email in OSM; {len(all_rows)-with_email} need scan.sh to harvest one")

if __name__ == "__main__":
    main()
