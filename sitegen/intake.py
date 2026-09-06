#!/usr/bin/env python3
"""
WebBlaze intake — scrape a lead's existing site to pre-fill a site config.
Usage:  python3 intake.py <domain> <niche> <city> [slug]
Writes: configs/<slug>.json   (then eyeball/edit + run generate.py)
"""
import sys, re, json, os, urllib.request, html

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

# sensible default service sets per niche keyword
SERVICE_SETS = {
    "roofing": ["Roof Repair","Roof Replacement","Storm & Leak Repair","Free Inspections"],
    "hvac": ["AC Repair","AC Installation","Heating Service","Maintenance Plans"],
    "air conditioning": ["AC Repair","AC Installation","Emergency Service","Tune-Ups"],
    "plumb": ["Leak Repair","Drain Cleaning","Water Heaters","Emergency Plumbing"],
    "electric": ["Wiring & Rewiring","Panel Upgrades","Lighting","Emergency Electrical"],
    "landscap": ["Lawn Care","Landscape Design","Tree & Shrub Care","Irrigation"],
    "auto": ["Diagnostics","Brakes & Suspension","Oil & Maintenance","Engine Repair"],
    "dental": ["Cleanings & Exams","Cosmetic Dentistry","Emergency Dental","Implants"],
    "attorney": ["Free Consultation","Case Evaluation","Aggressive Representation","No Fee Unless You Win"],
    "law": ["Free Consultation","Case Evaluation","Experienced Counsel","Results Driven"],
    "cabinet": ["Custom Cabinets","Kitchen Remodels","Cabinet Refacing","Countertops"],
    "weld": ["Custom Fabrication","Mobile Welding","Repairs","Structural Work"],
    "paint": ["Interior Painting","Exterior Painting","Cabinet Refinishing","Free Estimates"],
    "pool": ["Pool Cleaning","Repairs","Equipment Install","Weekly Service"],
    "pest": ["Pest Control","Termite Treatment","Rodent Removal","Recurring Plans"],
    "clean": ["Home Cleaning","Deep Cleaning","Move In/Out","Recurring Service"],
}
def services_for(niche):
    n=(niche or "").lower()
    for k,v in SERVICE_SETS.items():
        if k in n: return v
    return ["Quality Service","Free Estimates","Fast Response","Fair Pricing"]

def fetch(url):
    try:
        return urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":UA}),timeout=15).read().decode("utf-8","ignore")
    except Exception: return ""

def main():
    domain=sys.argv[1].replace("https://","").replace("http://","").strip("/")
    niche=sys.argv[2] if len(sys.argv)>2 else ""
    city=sys.argv[3] if len(sys.argv)>3 else ""
    slug=sys.argv[4] if len(sys.argv)>4 else re.sub(r"[^a-z0-9]","",domain.split(".")[0].lower())
    pages=""
    for p in ("","/contact","/about"):
        pages+=fetch("https://"+domain+p) or ""
    # business name from <title>
    m=re.search(r"<title>(.*?)</title>", pages, re.I|re.S)
    name=html.unescape(re.sub(r"\s+"," ",m.group(1)).split("|")[0].split("-")[0].strip()) if m else domain.split(".")[0].title()
    if len(name)<2 or len(name)>60: name=domain.split(".")[0].title()
    # phone: prefer tel: links, then strictly-formatted US numbers (paren or dash separators).
    # Avoid bare digit runs (version numbers, coords) that cause false positives.
    phone=""
    tel=re.search(r"tel:\+?1?[\s-]?(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})", pages)
    if tel:
        phone=tel.group(1)
    else:
        for m in re.finditer(r"(\(\d{3}\)\s?\d{3}[\s.-]?\d{4}|\d{3}-\d{3}-\d{4})", pages):
            phone=m.group(1); break
    phone=re.sub(r"\s+"," ",phone).strip()
    # email (mailto)
    em=re.search(r"mailto:([^\"'?>\s]+@[^\"'?>\s]+)", pages)
    email=em.group(1) if em else "info@"+domain
    # address (rough: line with FL zip)
    ad=re.search(r"([0-9]{1,6}[^<>\n,]{3,40},?\s*[A-Za-z .]{3,30},?\s*FL\s*\d{5})", pages)
    address=html.unescape(re.sub(r"\s+"," ",ad.group(1))).strip() if ad else ""

    cfg={
        "slug":slug,"business_name":name,"niche":niche,"city":city,
        "phone":phone,"email":email,"address":address,"hours":"",
        "tagline":"","about":"",
        "services":[{"title":s} for s in services_for(niche)],
        "reviews":[],
    }
    os.makedirs(os.path.join(os.path.dirname(__file__),"configs"),exist_ok=True)
    out=os.path.join(os.path.dirname(__file__),"configs",slug+".json")
    json.dump(cfg,open(out,"w"),indent=2)
    print("wrote",out)
    print("  name:",name,"| phone:",phone or "(none found)","| addr:",address or "(none)")
    print("  -> review/edit then: python3 generate.py configs/%s.json"%slug)

if __name__=="__main__": main()
