#!/usr/bin/env python3
"""Blaidd — the lead-gen agent. Turns scanner output into pipeline leads.
Reads a scan.sh results CSV, keeps only qualified + reachable prospects
(score >= min AND has an email), and drops each into the client DB as status='lead'
with the flaw as the outreach hook. Dedupes automatically.

Usage:
  blaidd.py ingest <results.csv> [minscore=3]     # ingest an existing scan CSV
  blaidd.py hunt <domains.txt> [minscore=3]       # run scan.sh, then ingest
"""
import sys, os, re, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import db

PROSPECT = os.path.expanduser("~/webblaze/prospecting")

def slugify(domain):
    d = re.sub(r'^www\.', '', domain.strip().lower())
    return re.sub(r'[^a-z0-9]+', '-', d.split('.')[0]).strip('-')

def ingest(results_csv, minscore=3):
    added = skipped = 0
    with open(results_csv) as f:
        next(f, None)  # header
        for line in f:
            parts = line.rstrip("\n").split(",")
            if len(parts) < 8:
                skipped += 1; continue
            score_s, domain, https, mobile, builder, year, email, phone = parts[:8]
            reason = ",".join(parts[8:]).strip().strip('"')
            try: score = int(score_s)
            except: score = 0
            email = email.strip(); domain = domain.strip()
            if score < minscore or not email or not domain or email.lower().startswith("johndoe"):
                skipped += 1; continue
            slug = slugify(domain)
            if db.get(slug):        # already in pipeline
                skipped += 1; continue
            db.add_client({
                "slug": slug, "business": domain, "email": email,
                "phone": phone.strip(), "domain": domain,
                "plan": "website", "status": "lead",
                "notes": f"[score {score}] {reason}" if reason else f"[score {score}]",
            }, actor="blaidd")
            added += 1
    print(f"[Blaidd] +{added} leads into the pipeline (skipped {skipped}: low score / no email / dupes).")
    return added

def hunt(domains_txt, minscore=3):
    out = "/tmp/blaidd_scan.csv"
    print(f"[Blaidd] scanning {domains_txt} ...")
    subprocess.run(["bash", os.path.join(PROSPECT, "scan.sh"), os.path.expanduser(domains_txt), out], check=True)
    ingest(out, minscore)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    ms = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    (ingest if sys.argv[1] == "ingest" else hunt)(os.path.expanduser(sys.argv[2]), ms)
