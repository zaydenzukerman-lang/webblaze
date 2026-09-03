#!/usr/bin/env python3
# WebBlaze — continuous Miami lead generation (robust CSV, endpoint rotation).
# Loops: OSM source by niche across Miami cities -> for new domains harvest email+score
# via scan.sh -> append leads WITH an email to the master (properly quoted).
import csv, os, subprocess, sys, time, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from source_osm import bad_email
except Exception:
    def bad_email(e): return not e or "@" not in e

HERE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(HERE, "leads_miami_master.csv")
SEENF  = os.path.join(HERE, "seen_domains.txt")
LOG    = os.path.join(HERE, "leadgen.log")
CITIES = os.path.join(HERE, "miami-cities.txt")
PRESETS = ["trades", "pro", "clinic", "local"]
FIELDS = ["name","website","domain","email","phone","city","niche","score","https","mobile","reason"]

def log(m):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), m)
    print(line, flush=True)
    with io.open(LOG, "a", encoding="utf-8") as f: f.write(line + "\n")

def load_seen():
    if not os.path.exists(SEENF): return set()
    return set(x.strip() for x in io.open(SEENF, encoding="utf-8") if x.strip())

def add_seen(dom):
    with io.open(SEENF, "a", encoding="utf-8") as f: f.write(dom + "\n")

def scan_one(domain):
    """Return (score, https, mobile, email, reason) via scan.sh, or blanks."""
    try:
        tmp = "/tmp/scan_%d.csv" % os.getpid()
        subprocess.run(["bash", os.path.join(HERE, "scan.sh"), "/dev/stdin", tmp],
                       input=domain + "\n", text=True, capture_output=True, timeout=60)
        rows = list(csv.reader(io.open(tmp, encoding="utf-8")))
        if len(rows) >= 2:
            r = rows[1]  # score,domain,https,mobile,builder,year,email,phone,reason
            return (r[0], r[2], r[3], r[6], r[8] if len(r) > 8 else "")
    except Exception as e:
        pass
    return ("", "", "", "", "")

def ensure_master():
    if not os.path.exists(MASTER):
        with io.open(MASTER, "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(FIELDS)

def append_rows(rows):
    with io.open(MASTER, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for r in rows: w.writerow([r.get(k, "") for k in FIELDS])

def main():
    ensure_master()
    seen = load_seen()
    rnd = 0
    while True:
        rnd += 1
        preset = PRESETS[(rnd - 1) % len(PRESETS)]
        raw = os.path.join(HERE, "raw_%s.csv" % preset)
        log("=== round %d | niche=%s | sourcing OSM ===" % (rnd, preset))
        subprocess.run([sys.executable, os.path.join(HERE, "source_osm.py"),
                        "--cities", CITIES, "--out", raw, "--tags", preset],
                       capture_output=True, text=True)
        if not os.path.exists(raw):
            log("  no raw output; sleeping"); time.sleep(60); continue
        added = 0; scanned = 0
        batch = []
        for row in csv.DictReader(io.open(raw, encoding="utf-8")):
            dom = (row.get("domain") or "").strip().lower()
            if not dom or dom in seen: continue
            seen.add(dom); add_seen(dom)
            email = (row.get("email") or "").strip()
            score = https = mobile = reason = ""
            if not email:
                score, https, mobile, semail, reason = scan_one(dom)
                scanned += 1
                if semail: email = semail
            if bad_email(email):
                continue  # no reachable / agency / junk email -> skip
            row["email"] = email; row["score"] = score
            row["https"] = https; row["mobile"] = mobile; row["reason"] = reason
            batch.append(row); added += 1
            if len(batch) >= 20:
                append_rows(batch); batch = []
        if batch: append_rows(batch)
        total = sum(1 for _ in io.open(MASTER, encoding="utf-8")) - 1
        log("round %d done | +%d new leads (scanned %d) | master total: %d" % (rnd, added, scanned, total))
        time.sleep(90)

if __name__ == "__main__":
    main()
