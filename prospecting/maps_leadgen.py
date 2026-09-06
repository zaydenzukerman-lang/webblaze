#!/usr/bin/env python3
# WebBlaze — HIGH-VOLUME lead engine via Google Maps (headless browser).
# Maps -> business website domains -> concurrent email harvest -> filtered leads.
# Own files (leads_maps_master.csv / maps_seen.txt) so it never races the OSM engine.
import sys, os, re, csv, io, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from source_osm import is_chain, is_foreign, is_brand_name, bad_email
import maps_scrape

HERE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(HERE, "leads_maps_master.csv")
SEENF  = os.path.join(HERE, "maps_seen.txt")
LOG    = os.path.join(HERE, "maps_leadgen.log")
FIELDS = ["name","website","domain","email","phone","city","niche","source"]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

NICHES = [
 "roofing contractor","plumber","hvac contractor","air conditioning repair","auto repair shop",
 "auto body shop","upholstery shop","welding shop","electrician","landscaping company",
 "pest control","cabinet maker","sign shop","machine shop","locksmith","flooring contractor",
 "pool service","garage door repair","appliance repair","tree service","fence company",
 "concrete contractor","painting contractor","tile contractor","glass shop","dry cleaner",
 "print shop","tax preparation service","bookkeeping service","insurance agency",
 "immigration attorney","family law attorney","dentist","chiropractor","florist",
 "jewelry store","pet grooming","catering service","towing service","pressure washing",
 "handyman service","window installation","irrigation contractor","paving contractor",
 "cleaning service","moving company","auto glass","marble and granite","awning company","screen enclosure",
]
def _load_cities():
    f = os.path.join(HERE, "miami-cities.txt")
    try:
        c = [x.strip() for x in io.open(f, encoding="utf-8") if x.strip()]
        return [(x if x.upper().endswith(" FL") else x + " FL") for x in c]
    except Exception:
        return ["Miami FL","Hialeah FL","Fort Lauderdale FL","Boca Raton FL"]
CITIES = _load_cities()  # all ~84 Miami-area cities => keeps discovering NEW businesses

# emails we never want (builders/agencies/tracking) beyond bad_email's list
EMAIL_JUNK = ("sentry","wixpress.com","example.com","@2x","godaddy","cloudflare","w3.org",
 "yourdomain","domain.com","email.com","test.com","abc.com","guacdigital.com",
 "getjobber.com","housecallpro","thryv","wix.com","squarespace","duda","vistaprint",
 "latinotype.com","myfonts.com","fonts.com","fontshare","typekit","fontspring",
 "sentry.io","@sentry","wpengine","kinsta","hubspot.com","mailchimp",
 "mystore.com","micahrich.com","yourstore.com","shopify.com","bigcommerce.com",
 "myftpupload.com","mysite.com","wordpress.com","weebly.com","godaddysites.com",
 "sentry-next.wixpress","business.site","square.site","godaddy.com",
 "dharmamarketing","marketing.cloud",".agency","seo",".marketing",
 "johndoe","janedoe","john.doe","jane.doe","name@","youremail","your.email","noreply","no-reply",
 "way.com","ubreakifix.com","mysite.com","yelp.com","angi.com","thumbtack","carvana","carmax",
 "latofonts.com","fonts.google","typography","dafont","1001fonts",
 "astigmatic.com","impallari","typedesign","typedesign@","fontfabric","typotheque",
 "@astigmatic","typeface","letterhead-studio","fonts@",
 "pixelspread","pixelspread.com","webdesign","digitalagency","webflow.io","framer.website",
 "insitesoft.com","testaccount","test@","demo@","admin@admin","insitesoft",
 "therankinggeeks","eyebytes","rankinggeeks",".ai","geeks","webdev","devteam",
 "webador.com","webador","jimdo","strikingly","site123","weebly","ionos",
 "aptleasing","rentcafe","webcommunitywebsite","aptleasing.in",".in","apartments.com",
 "indiantypefoundry","typefoundry","fontfoundry","monotype","linotype",
 "linkeo.net","linkeo","hibu","yodle","vivial","localiq",
 "getsquire","bowlero","bowlerocorp","booksy","vagaro","fresha","mindbody",
 "coinhubatm","coinhub","key.me","aspendental",".org","bitcoindepot","athena",
 ".css",".js",".min","slick-slider","schools.")

def log(m):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), m); print(line, flush=True)
    with io.open(LOG, "a", encoding="utf-8") as f: f.write(line + "\n")

def load_seen():
    return set(x.strip() for x in io.open(SEENF, encoding="utf-8")) if os.path.exists(SEENF) else set()

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        return urllib.request.urlopen(req, timeout=12).read().decode("utf-8", "ignore")
    except Exception:
        return ""

def harvest_email(domain):
    """Fetch homepage + /contact, return the best public email or ''."""
    found = []
    for path in ("", "/contact", "/contact-us", "/about"):
        html = fetch("https://" + domain + path) or (fetch("http://" + domain + path) if path == "" else "")
        if not html: continue
        # prefer mailto:
        for m in re.findall(r'mailto:([^"\'?>]+)', html):
            found.append(m.strip().lower())
        for m in EMAIL_RE.findall(html):
            found.append(m.strip().lower())
        if found: break
    for e in found:
        e = urllib.parse.unquote(e).strip().strip('.').rstrip('%20').strip()
        if not e or len(e) > 60 or " " in e or "%" in e or e.count("@") != 1: continue
        if any(c in e for c in "<>&\"'\\/"): continue  # reject captured HTML/markup blobs
        if any(j in e for j in EMAIL_JUNK): continue
        if e.endswith((".png",".jpg",".jpeg",".gif",".webp",".svg")): continue
        if bad_email(e): continue
        # prefer an email on the business's own domain
        return e
    return ""

def ensure():
    if not os.path.exists(MASTER):
        with io.open(MASTER, "w", encoding="utf-8", newline="") as f: csv.writer(f).writerow(FIELDS)

def main():
    ensure()
    seen = load_seen()
    zero_streak = 0   # consecutive queries that scraped nothing => likely Google block
    # progress persistence: resume at the (niche,city) we left off after a reboot/hang
    PROG = os.path.join(HERE, ".maps_progress")
    tasks = [(n, c) for n in NICHES for c in CITIES]
    try:
        start = int(io.open(PROG).read().strip())
    except Exception:
        start = 0
    passn = 0
    while True:
        passn += 1
        for idx in range(start, len(tasks)):
            niche, city = tasks[idx]
            try: io.open(PROG, "w").write(str(idx))
            except Exception: pass
            if True:
                q = "%s %s" % (niche, city)
                try:
                    doms = maps_scrape.scrape(q)
                except Exception as e:
                    log("  ! maps '%s': %s" % (q, e)); doms = []
                # block detection: several empty scrapes in a row = throttled/CAPTCHA
                if len(doms) == 0:
                    zero_streak += 1
                    # sparse niches (sign shop, machine shop) legitimately return 0 in many
                    # small cities, so only treat a LONG streak as a real Google block.
                    if zero_streak >= 12:
                        log("  ! %d empty scrapes in a row — likely Google block; backing off 15 min" % zero_streak)
                        time.sleep(900); zero_streak = 0
                    continue
                else:
                    zero_streak = 0
                fresh = []
                for d in doms:
                    if d in seen: continue
                    if is_chain(d) or is_foreign(d) or is_brand_name(d): continue
                    seen.add(d)
                    with io.open(SEENF, "a", encoding="utf-8") as f: f.write(d + "\n")
                    fresh.append(d)
                # harvest emails concurrently
                rows = []
                if fresh:
                    with ThreadPoolExecutor(max_workers=8) as ex:
                        emails = list(ex.map(harvest_email, fresh))
                    for d, e in zip(fresh, emails):
                        if not e: continue
                        rows.append({"name": d, "website": "https://"+d, "domain": d, "email": e,
                                     "phone": "", "city": city, "niche": niche, "source": "gmaps"})
                if rows:
                    with io.open(MASTER, "a", encoding="utf-8", newline="") as f:
                        w = csv.writer(f)
                        for r in rows: w.writerow([r[k] for k in FIELDS])
                total = sum(1 for _ in io.open(MASTER, encoding="utf-8")) - 1
                log("%s | %s | scraped %d, +%d leads | maps total: %d" %
                    (niche, city, len(doms), len(rows), total))
                time.sleep(1.0)
        start = 0  # completed a full pass; next pass re-covers everything (dedup via seen)
        try: io.open(PROG, "w").write("0")
        except Exception: pass
        log("=== full Maps pass %d done; sleeping 600s ===" % passn)
        time.sleep(600)

if __name__ == "__main__":
    main()
