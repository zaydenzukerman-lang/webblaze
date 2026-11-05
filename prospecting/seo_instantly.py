#!/usr/bin/env python3
"""
Load SEO-track leads (seo/leads.json: good site, shown on Google Maps but not top 3) into the Instantly SEO campaign.

  python3 seo_instantly.py        load everything new; activate the campaign when it has leads

Rules:
- A business that ALREADY got emails from the main campaign is skipped (they already got 4 emails).
- A business sitting in the main campaign but NOT yet emailed is moved: deleted from main, added here (they get the SEO pitch instead).
- Blocklisted emails/domains are skipped. All text is ASCII-folded (deliverability rule).
- Instantly gets the business inbox (low bounce). The owner's first name, when known, goes in the greeting ("Hi Sean,").
"""
import json, os, re, sys, time, unicodedata, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
K = open(os.path.expanduser("~/.instantly-key")).read().strip()
H = {"Authorization": "Bearer " + K, "User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
MAIN = "5da84137-14a1-49ca-bd7e-b70c74132501"
SEO = open(os.path.join(HERE, "seo", "instantly_campaign_id")).read().strip()
LOADED = os.path.join(HERE, "seo", "instantly_loaded.json"); INDEX = os.path.join(HERE, "seo", "main_index.json")


def api(path, method="GET", body=None, tries=6):
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request("https://api.instantly.ai/api/v2/" + path, data=json.dumps(body).encode() if body is not None else None, method=method, headers=H), timeout=60)
            raw = r.read(); return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(5 * (i + 1)); continue
            return {"_error": e.code, "_body": e.read()[:200].decode("utf-8", "ignore")}
        except Exception as e:
            time.sleep(3); err = str(e)
    return {"_error": "retries", "_body": err if 'err' in dir() else ""}


def ascii(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip()


def short(name):
    n = ascii(name)
    n = re.split(r"\s+[|\-–:]\s+", n)[0]                       # "Lemus Dental Group | Coral Gables" -> "Lemus Dental Group"
    return n[:55].strip(" ,.")


def main_index(refresh=False):
    """email -> {id, contacted} for every lead in the main campaign (cached 6h)."""
    try:
        c = json.load(open(INDEX))
        if not refresh and time.time() - c["t"] < 6 * 3600: return c["v"]
    except Exception: pass
    out, cur = {}, None
    while True:
        body = {"campaign": MAIN, "limit": 100}
        if cur: body["starting_after"] = cur
        d = api("leads/list", "POST", body)
        if d.get("_error"): print("index error", d); break
        for it in d.get("items", []): out[it["email"].lower()] = {"id": it["id"], "contacted": bool(it.get("timestamp_last_contact"))}
        cur = d.get("next_starting_after")
        if not cur or not d.get("items"): break
    json.dump({"t": time.time(), "v": out}, open(INDEX, "w")); print("main campaign index: %d leads" % len(out))
    return out


def blocklist():
    import feed_campaign; return {b.lower() for b in feed_campaign.blocklist()}


# 2026-11-05: same list-quality fix as feed_campaign.py — before this, no lead in either Instantly
# lead list had ever been run through Instantly's own (already-paid-for) email verification. This
# runs hourly (vs feed_campaign's every-2h), so the per-run cap is smaller to keep combined spend
# across both scripts from draining the shared credit balance (check it periodically either way).
VERIFY_PER_RUN = 50          # ~12.5 credits/run max
verified_this_run = 0

def verify_quality(email):
    """Returns (ok_to_feed, note). Only hard-skips on a confirmed 'invalid' result; everything else
    (verified, catch_all, risky, pending, or an API error) still feeds — a bounce filter, not a
    stricter gate than Instantly's own send pipeline already applies. Fails open on any error so a
    verification hiccup can never be the reason the SEO campaign starves of leads."""
    global verified_this_run
    if verified_this_run >= VERIFY_PER_RUN:
        return True, "skipped (per-run cap)"
    verified_this_run += 1
    d = api("email-verification", "POST", {"email": email})
    if d.get("_error"):
        return True, "verify-api-error:%s" % (d.get("_error"),)
    status = d.get("verification_status", "")
    if status == "invalid":
        return False, "invalid"
    return True, status or "unknown"


_FIRST = None
def first_from_email(email):
    """sean@hummelaw.com -> 'Sean' when the inbox name is a common first name (Florida registry first-name table)."""
    global _FIRST
    if _FIRST is None:
        import sqlite3
        try: _FIRST = {r[0].lower() for r in sqlite3.connect(os.path.join(HERE, "ownerfinder", "data", "sunbiz.db")).execute("select name from firstname where n >= 200")}
        except Exception: _FIRST = set()
    local = email.split("@")[0].lower()
    return local.title() if local in _FIRST and len(local) > 2 else ""


MAX_POS = 20          # 2026-10-29: #21-#80 were mostly irrelevant results (dental temp agency as "dentist #71", Chase bank -> phishing report)
BIG_BRANDS = {"chase.com","bankofamerica.com","wellsfargo.com","statefarm.com","allstate.com","geico.com","progressive.com","farmersinsurance.com",
              "nationwide.com","libertymutual.com","citi.com","citibank.com","usbank.com","pnc.com","truist.com","hrblock.com","jacksonhewitt.com",
              "aspendental.com","heartland.com","westernunion.com","ups.com","fedex.com","walgreens.com","cvs.com","walmart.com","homedepot.com"}
ROLE_BAD = re.compile(r"^(phishing|abuse|security|privacy|legal|compliance|noreply|no-reply|donotreply|postmaster|webmaster|careers|jobs|hr|media|press|investor)", re.I)


def ok_lead(L, email):
    """SEO pitch only makes sense for a real local business that's close to the top: #4-#20, not a national brand, real name."""
    pos = L.get("pos") or 0
    if pos <= 3 or pos > MAX_POS: return False
    dom = (L.get("domain") or "").lower().removeprefix("www.")
    if dom in BIG_BRANDS or email.split("@")[-1] in BIG_BRANDS or ROLE_BAD.match(email): return False
    name = re.sub(r"[^a-z ]", "", (L.get("maps_name") or L.get("name") or "").lower()).strip()
    if len(name.split()) < 2: return False                     # "Dental", "Insurance": a category, not a business name
    return True


def run():
    leads = json.load(open(os.path.join(HERE, "seo", "leads.json")))
    loaded = set(json.load(open(LOADED))) if os.path.exists(LOADED) else set()
    idx = main_index(); bl = blocklist()
    added = moved = skipped_contacted = skipped_bl = skipped_invalid = 0
    for L in leads:
        email = re.sub(r"^mailto:|[\u200b-\u200f\ufeff\s]", "", (L.get("email") or "").strip().lower())
        if not re.fullmatch(r"[a-z0-9][a-z0-9._%+-]*@[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}", email or "") or ".." in email or "@." in email or ".@" in email: continue
        if not email or not ok_lead(L, email) or email in loaded: continue
        if email in bl or email.split("@")[-1] in bl or L["domain"] in bl: skipped_bl += 1; continue
        comps = [short(c["name"]) for c in L.get("competitors", [])][:3]
        if len(comps) < 3: continue
        m = idx.get(email)
        if m and m["contacted"]: skipped_contacted += 1; loaded.add(email); continue
        # verify last, right before the real POST — no point spending a credit on a lead that would
        # have been filtered out anyway (already contacted, <3 competitors, etc.)
        feed_ok, note = verify_quality(email)
        if not feed_ok: skipped_invalid += 1; loaded.add(email); print("skipped (verify: %s): %s" % (note, email)); continue
        if m and not m["contacted"]:
            d = api("leads/" + m["id"], "DELETE"); moved += 1
        o = L.get("owner") or {}; first = ascii(o.get("owner_first", "")).split(" ")[0].title() or first_from_email(email)
        biz = short(L.get("maps_name") or L.get("name") or L["domain"])
        body = {"campaign": SEO, "email": email, "first_name": first, "company_name": biz, "website": "https://" + L["domain"],
                "skip_if_in_workspace": False,
                "custom_variables": {"greeting": ("Hi %s," % first) if first else "Hi,", "maps_query": ascii(L["query"]), "maps_pos": str(L["pos"]),
                                     "biz_name": biz, "comp1": comps[0], "comp2": comps[1], "comp3": comps[2]}}
        d = api("leads", "POST", body)
        if d.get("_error"): print("add failed", email, d); continue
        loaded.add(email); added += 1
    json.dump(sorted(loaded), open(LOADED, "w"))
    print("SEO campaign: +%d leads (%d moved out of the main campaign before being emailed); skipped %d already emailed, %d blocklisted, %d invalid-on-verify (%d verify checks used)" % (added, moved, skipped_contacted, skipped_bl, skipped_invalid, verified_this_run))
    c = api("campaigns/" + SEO)
    if added and c.get("status") != 1:
        r = api("campaigns/%s/activate" % SEO, "POST", {}); print("campaign activated" if not r.get("_error") else ("activate failed %s" % r))


if __name__ == "__main__":
    run()
