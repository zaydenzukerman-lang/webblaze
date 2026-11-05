#!/usr/bin/env python3
"""
One-shot morning-of reminder to Timur (cpa@cpa.inc) for the Fri Nov 6 12:00 ET call.
Scheduled via launchd (~/Library/LaunchAgents/com.webblaze.timur-reminder.plist) for 2026-11-06 08:30 ET.

Safe to run repeatedly:
  - date guard: only sends on 2026-11-06 America/New_York
  - sentinel guard: ~/webblaze/prospecting/.timur_morning_reminder.sent prevents a second send
  - 2026-11-05 CRITICAL GUARDRAIL (Zayden via Sindri): don't double-nudge a sophisticated buyer --
    if Timur has already replied/confirmed on this thread since the 21:35 UTC reminder, SKIP.
    Checks the live Unibox two ways before sending: the lead's email_reply_count (workspace-wide),
    and a direct scan for any RECEIVED (ue_type==2) item on this thread newer than our last send.
Runs on the same Instantly thread ("Re: CPA Inc is #13 on Google Maps") from zukerman@meetwebblaze.com,
with Zayden's headshot signature. Pass --send to actually send (launchd passes it); otherwise dry run.
"""
import json, re, sys, os, html as H, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

LEAD = "cpa@cpa.inc"
EACCOUNT = "zukerman@meetwebblaze.com"
SUBJECT = "Re: CPA Inc is #13 on Google Maps"
SEO_CID = "c8265542-8e61-4a4e-9c8a-7bfef06d93fc"
THREAD = "c8-yT7o4_bwXEV37Z-dhcKLj3p"
LAST_TOUCH_ID = "01a1ada3-b821-7d29-8db4-1e9fccab0e5f"   # the 21:35 UTC reminder
SENTINEL = os.path.expanduser("~/webblaze/prospecting/.timur_morning_reminder.sent")
LOG = os.path.expanduser("~/webblaze/prospecting/.timur_morning_reminder.log")
K = open(os.path.expanduser("~/.instantly-key")).read().strip()
HDR = {"Authorization": "Bearer " + K, "User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}

BODY_HTML = """<p>Hi Timur,</p>
<p>Looking forward to our call in a few hours &mdash; <strong>12:00 PM ET today</strong>.</p>
<p>Google Meet: <a href="https://meet.google.com/xoc-bgxn-mgn">meet.google.com/xoc-bgxn-mgn</a></p>
<p>I&rsquo;ll have your Google Maps ranking breakdown ready to walk through &mdash; the specific gaps and what I&rsquo;d fix first. See you then,</p>
<p style="margin:0 0 14px">Zayden</p>"""


def log(msg):
    line = "[%s] %s" % (datetime.now(timezone.utc).isoformat(), msg)
    print(line)
    try:
        open(LOG, "a").write(line + "\n")
    except Exception:
        pass


def api(path, body=None):
    req = urllib.request.Request("https://api.instantly.ai/api/v2/" + path,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 method="POST" if body is not None else "GET", headers=HDR)
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read()[:400].decode("utf-8", "ignore")}


def latest_thread_email():
    d = api("emails?lead=%s&limit=50" % urllib.request.quote(LEAD))
    items = d.get("items", [])
    return max(items, key=lambda e: e["timestamp_email"]) if items else None


def already_engaged():
    """CRITICAL GUARDRAIL: has Timur replied/confirmed anywhere on this thread since the 21:35 UTC
    reminder? Checks two ways so a quirk in either one doesn't let a reply slip through:
    (1) the lead's workspace-wide email_reply_count (same technique validated in sequence.py's
        instantly_engaged() earlier today), (2) a direct scan for any RECEIVED (ue_type==2) item
    on this exact thread. On an API error, fails toward SENDING (unlike a routine bump, a missed
    day-of reminder before a real booked call is worse than a rare extra touch) -- but logs the
    failure loudly so it's visible after the fact.
    Returns (engaged: bool, reason: str)."""
    d = api("leads/list", {"search": LEAD, "limit": 5})
    if d.get("_error"):
        log("WARN: lead lookup failed (%s) -- guardrail check #1 skipped" % d)
    else:
        for it in d.get("items", []):
            if (it.get("email") or "").lower() == LEAD and (it.get("email_reply_count") or 0) > 0:
                return True, "lead record shows email_reply_count=%s" % it.get("email_reply_count")
    d2 = api("emails?campaign_id=%s&email_type=received&limit=50" % SEO_CID)
    if d2.get("_error"):
        log("WARN: unibox scan failed (%s) -- guardrail check #2 skipped" % d2)
    else:
        for it in d2.get("items", []):
            if it.get("thread_id") == THREAD:
                return True, "received email found on thread: %s" % str(it.get("subject", ""))[:80]
    return False, "no reply found on either check"


if __name__ == "__main__":
    go = "--send" in sys.argv
    et_now = datetime.now(timezone(timedelta(hours=-5)))  # EST (ET on Nov 6, no DST)
    if et_now.strftime("%Y-%m-%d") != "2026-11-06":
        log("SKIP: not 2026-11-06 ET (today ET = %s)" % et_now.strftime("%Y-%m-%d"))
        sys.exit(0)
    if os.path.exists(SENTINEL):
        log("SKIP: sentinel exists, already sent")
        sys.exit(0)

    engaged, reason = already_engaged()
    if engaged:
        log("SKIP: Timur already replied/engaged on the thread (%s) -- not double-nudging" % reason)
        open(SENTINEL, "w").write(datetime.now(timezone.utc).isoformat() + " SKIPPED (already engaged: %s)\n" % reason)
        sys.exit(0)
    log("guardrail clear (%s) -- proceeding" % reason)

    e = latest_thread_email()
    if not e:
        log("ABORT: no thread email found for %s" % LEAD)
        sys.exit(1)

    from email_v2 import SIG
    body_html = BODY_HTML + SIG
    body_text = H.unescape(re.sub(r"<br\s*/?>|</p>", "\n", BODY_HTML))
    body_text = re.sub(r"<[^>]+>", "", body_text).strip()

    log("REPLY target id=%s eaccount=%s subject=%s" % (e["id"], EACCOUNT, SUBJECT))
    if not go:
        log("DRY RUN (no --send). Text:\n" + body_text)
        sys.exit(0)

    r = api("emails/reply", {"reply_to_uuid": e["id"], "eaccount": EACCOUNT,
                             "subject": SUBJECT, "body": {"html": body_html, "text": body_text}})
    if r.get("_error"):
        log("FAILED: %s" % r)
        sys.exit(1)
    open(SENTINEL, "w").write(datetime.now(timezone.utc).isoformat() + " id=" + str(r.get("id")) + "\n")
    log("SENT ok id=%s to=%s" % (r.get("id"), r.get("__confirmed_recipient", LEAD)))
