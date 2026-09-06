#!/usr/bin/env python3
# Bulk-upload all_leads.csv into an Instantly lead list via the v2 API.
import csv, io, json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

KEY = open(os.path.expanduser("~/.instantly-key")).read().strip()
LIST_ID = sys.argv[1] if len(sys.argv) > 1 else open("/tmp/wb_listid").read().strip()
URL = "https://api.instantly.ai/api/v2/leads"
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "instantly_upload.log")

def log(m):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), m)
    print(line, flush=True)
    with io.open(LOG, "a", encoding="utf-8") as f: f.write(line + "\n")

rows = list(csv.DictReader(io.open(os.path.join(HERE, "all_leads.csv"), encoding="utf-8")))
log("uploading %d leads to list %s" % (len(rows), LIST_ID))

ok = [0]; fail = [0]
def add(r):
    body = json.dumps({
        "list_id": LIST_ID,
        "email": r["email"],
        "company_name": r.get("company", ""),
        "website": ("https://" + r.get("company", "")) if r.get("company") else "",
        "custom_variables": {"niche": r.get("niche", ""), "city": r.get("city", "")},
    }).encode()
    req = urllib.request.Request(URL, data=body, method="POST",
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": UA})
    for attempt in range(4):
        try:
            urllib.request.urlopen(req, timeout=30).read()
            ok[0] += 1; return
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 * (attempt + 1)); continue
            fail[0] += 1; return
        except Exception:
            time.sleep(1.5); continue
    fail[0] += 1

with ThreadPoolExecutor(max_workers=6) as ex:
    for i, _ in enumerate(ex.map(add, rows), 1):
        if i % 250 == 0:
            log("progress %d/%d (ok=%d fail=%d)" % (i, len(rows), ok[0], fail[0]))
log("DONE uploaded ok=%d fail=%d of %d" % (ok[0], fail[0], len(rows)))
