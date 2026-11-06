#!/usr/bin/env python3
"""
WebBlaze Closer — auto-triages the Instantly unibox for the outreach campaign.

- NEGATIVE ("no / remove me / stop / not interested")  -> delete lead from campaign + blocklist (never contacted again)
- POSITIVE ("yes / interested / how much / send it")    -> logged to HOT-LEADS.txt with the reply-stage pitch ready
- AUTO-REPLY / BOT (out-of-office, intercom, etc.)       -> ignored
- AMBIGUOUS                                              -> logged to REVIEW.txt for a human to read

Runs statelessly-safe: remembers what it already processed in .closer_seen.json so it never double-acts.
Usage:  python3 closer.py         (one pass)
Cron:   */30 * * * *  (every 30 min) — see install note at bottom.
"""
import json, os, re, time, hashlib, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
KEY  = open(os.path.expanduser("~/.instantly-key")).read().strip()
CID  = "5da84137-14a1-49ca-bd7e-b70c74132501"   # WebBlaze Miami Outreach
CIDS = [CID, "c8265542-8e61-4a4e-9c8a-7bfef06d93fc"]   # + WebBlaze SEO - Google Maps rank (2026-10-27)
UA   = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
SEEN = os.path.join(HERE, ".closer_seen.json")
HOT  = os.path.join(HERE, "HOT-LEADS.txt")
REV  = os.path.join(HERE, "REVIEW.txt")
LOG  = os.path.join(HERE, "closer.log")

def api(path, method="GET", body=None, json_body=True):
    headers = {"Authorization": "Bearer " + KEY, "User-Agent": UA}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"; data = json.dumps(body).encode()
    req = urllib.request.Request("https://api.instantly.ai/api/v2/" + path, data=data, method=method, headers=headers)
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read() or b"{}"), None
    except urllib.error.HTTPError as e:
        return None, (e.code, e.read().decode()[:160])

def log(msg):
    line = "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line)
    with open(LOG, "a", encoding="utf-8") as f: f.write(line + "\n")

# ---- classification ----
NEG = ["opt out","opt-out","optout","don't email","dont email","do not email","don't contact","dont contact","never email","lose my email","delete my email","stop messaging","leave me alone","unsubscribe","remove us","remove me","remove my","take us off","take me off","stop emailing",
       "stop contacting","not interested","no thank","no thanks","we are all set","we're all set",
       "do not contact","do not email","please stop","not looking","already have a","no soliciting",
       "no solicitations","leave us alone","not needed","we're good","we are good","thanks but no","but no thanks",
       "just launched a new","not at this time","keep your information on file","which broker","purchasing the data",
       "how did you get my","how did you get this","stop sending",
       "i am all set","i'm all set","im all set","i'm ok,","im ok,","i'm ok.","im ok.","i'm good,","im good,","no need","we're covered","not for us",
       "dont follow up","don't follow up","happy with our current","happy with our set up","happy with our setup"]
POS = ["interested","yes please","i'd be interested","i would be interested","tell me more","how much",
       "what would it cost","what's the cost","sounds good","let's do","let us do","please build","go ahead",
       "send me","i'd like","i would like","would like to see","let's talk","lets talk","give me a call",
       "call me","set up a call","yes i","yes, i","sure,","sure ","that would be great","love to see","yes, we can","yes we can",
       "we can talk","can talk about","let's talk","lets talk","how much do you charge","how much is","what do you charge","send me"]
# Definite automation — checked BEFORE positive (OOO replies often contain polite/positive-sounding words)
AUTO_STRONG = ["automatic reply","auto reply","auto-reply","autoreply","out of office","out of the office",
        "on vacation","maternity leave","currently away","away from the office","away until","on leave",
        "annual leave","undeliverable","delivery status notification","mailer-daemon","do not reply",
        "this is an automated","automated response","automatic response","paternity leave",
        "thank you for contacting","thank you for choosing","we received your message","we've received your message","regular office hours","messages received outside","thanks for emailing","we have received your","we will respond to your email","respond to your email within",
        "has been received and is being reviewed","your request (","type your reply above this line","reply above this line",
        "i am currently checking and responding","within one business day","within 24 hours",
        "no longer with","please send all e-mails to","please send all emails to"]
# Soft bot phrases — checked AFTER positive (so a real "yes, thanks for reaching out" still counts)
AUTO_SOFT = ["thank you for contacting","thanks for reaching out","thanks for contacting","we will get back",
        "someone will reach out","we'll get back to you","will get back to you as soon"]
AUTO_DOMAINS = ["intercom-mail.com","intercom.io","mailer-daemon","postmaster","noreply","no-reply"]

STANDALONE_POS = {"sure","yes","yes!","sure!","ok","okay","yep","yeah","please","interested","definitely","absolutely"}
STANDALONE_NEG = {"stop","no","unsubscribe","remove","pass","nope","no.","stop.","remove.","unsubscribe."}

def strip_quote(text):
    """Return only the NEW reply text, cutting off the quoted original message."""
    if not text: return ""
    out = []
    for ln in text.replace("\r", "").split("\n"):
        low = ln.strip().lower()
        if (low.startswith(">") or low.startswith("from:") or low.startswith("sent:")
            or low.startswith("to:") or low.startswith("subject:")
            or "-----original message" in low or "wrote:" in low
            or low.startswith("on ") and "wrote" in low
            or ("get outlook" in low) or low.startswith("date:")
            or (len(low) >= 8 and set(low) <= set("_-–—= "))          # underscore/dash separator line
            or "@meetwebblaze" in low or "@nowwebblaze" in low or "@getwebblaze" in low
            or "@appwebblaze" in low or "@hubwebblaze" in low or "@trywebblaze" in low
            or "@hqwebblaze" in low or "@prowebblaze" in low or "zayden zukerman" in low):
            break
        out.append(ln)
    cleaned = "\n".join(out).strip()
    return cleaned if cleaned else text.strip()   # fall back to full text if we stripped everything

def classify(sender, subject, text):
    reply = strip_quote(text)                       # classify ONLY the new reply, not the quoted email
    low = reply.lower().strip()
    words = [w.strip(".,!?;:'\"") for w in low.split()]
    subj = subject.lower().strip()
    dom = sender.split("@")[-1].lower() if "@" in sender else sender.lower()
    if any(d in dom for d in AUTO_DOMAINS): return "auto"
    if subj.startswith("automatic reply") or subj.startswith("auto") or subj.startswith("out of office"): return "auto"
    # one-word / short opt-outs ("stop", "no", "remove", "no thanks", "not interested")
    if words and len(words) <= 6 and any(w in STANDALONE_NEG for w in words): return "negative"
    # opt-out on the FIRST line, even with a long signature underneath ("Stop\n\nAventura Dental Arts, LLC | ...")
    first = next((ln.strip().lower() for ln in reply.replace("\r","").split("\n") if ln.strip()), "")
    fw = [w.strip(".,!?;:'\"") for w in first.split()]
    if fw and (len(fw) <= 4 and any(w in STANDALONE_NEG for w in fw) or fw[0] in ("stop","unsubscribe","remove") and (len(fw) < 2 or fw[1] not in ("by","in","over","into"))): return "negative"
    if any(k in low for k in NEG): return "negative"    # explicit opt-out always wins
    # one-word yes ("sure", "yes", "ok") on the first line = they want the preview
    if fw and len(fw) <= 3 and any(w in STANDALONE_POS for w in fw) and not any(w in STANDALONE_NEG for w in fw): return "positive"
    if any(k in low for k in AUTO_STRONG): return "auto" # definite OOO/bounce before positive
    if any(k in low for k in POS): return "positive"
    if any(k in low for k in AUTO_SOFT): return "auto"
    return "ambiguous"

# 2026-11-05 (Hermes): we have ZERO testimonials, so any real praise in a reply matters. These are
# deliberately multi-word (an adjective attached to "looks"/"love"/"work"/"this/it"), not bare
# positive words, so "no thanks, great day" doesn't false-positive and sarcasm like "at least mine
# loads" (no phrase here matches it) doesn't either. Additive only -- never changes the normal
# negative/positive/ambiguous handling, just also tags + logs a candidate quote.
PRAISE_PHRASES = ["looks great", "looks amazing", "looks good", "looks awesome", "love it", "love this",
    "really like it", "really like this", "better than mine", "nice work", "great work", "amazing work",
    "impressive", "that's awesome", "thats awesome", "this is awesome", "wow"]
TESTIMONIALS = os.path.join(HERE, "TESTIMONIALS.txt")


def extract_praise(text):
    """Returns (matched_phrase, the_sentence_it_was_in) or (None, None). Operates on the same
    quote-stripped text classify() uses, so a praise line quoted FROM our own old email never
    counts -- only something the lead actually just wrote."""
    reply = strip_quote(text)
    low = reply.lower()
    for phrase in PRAISE_PHRASES:
        if phrase not in low: continue
        parts = re.split(r"(?<=[.!?])\s+|\n+", reply)
        line = next((p.strip() for p in parts if phrase in p.lower()), reply.strip())
        return phrase, line[:300]
    return None, None


def log_testimonial(sender, e, phrase, line):
    biz = ""
    try:
        biz = ((e.get("from_address_json") or [{}])[0].get("name") or "").strip()
    except Exception:
        pass
    if not biz and "@" in sender: biz = sender.split("@")[-1]
    with open(TESTIMONIALS, "a", encoding="utf-8") as f:
        f.write("[%s] %s | %s | matched \"%s\"\n  \"%s\"\n\n" % (
            time.strftime("%Y-%m-%d %H:%M"), sender, biz or "(unknown)", phrase, line))


def load_seen():
    try: return set(json.load(open(SEEN)))
    except Exception: return set()

def save_seen(seen):
    json.dump(sorted(seen), open(SEEN, "w"))

def reply_pitch():
    p = os.path.join(HERE, "campaign-copy", "REPLY-when-interested.txt")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else "(reply-stage pitch template missing)"

def remove_lead(email):
    """delete from campaign + add to blocklist"""
    for cid in CIDS:
        d, _ = api("leads/list", "POST", {"campaign": cid, "search": email, "limit": 5})
        for it in (d.get("items") if d else []):
            if it["email"].lower() == email.lower():
                api("leads/" + it["id"], "DELETE", body=None)   # DELETE, no json body
    api("block-lists-entries", "POST", {"bl_value": email})

def main():
    seen = load_seen()
    items = []
    for cid in CIDS:
        d, err = api("emails?campaign_id=%s&email_type=received&limit=100" % cid)
        if err:
            log("ERROR fetching unibox for %s: %s" % (cid, err)); continue
        items += d.get("items", []) if isinstance(d, dict) else []
    new_pos = []; new_neg = []; new_amb = []; processed = 0
    for e in items:
        sender  = e.get("from_address_email") or e.get("from_address") or "?"
        subject = e.get("subject") or ""
        bodyobj = e.get("body") or {}
        text    = (bodyobj.get("text") or bodyobj.get("html") or e.get("preview") or "")
        key = e.get("id") or hashlib.md5((sender + subject + str(e.get("timestamp_created",""))).encode()).hexdigest()
        if key in seen:
            continue
        seen.add(key); processed += 1
        kind = classify(sender, subject, text)
        snippet = " ".join(text.split())[:200]
        phrase, praise_line = extract_praise(text)       # additive -- doesn't touch kind/handling below
        if phrase:
            log_testimonial(sender, e, phrase, praise_line)
            log("PRAISE -> TESTIMONIALS.txt: %s (matched \"%s\")" % (sender, phrase))
        if kind == "negative":
            remove_lead(sender)
            lead_addr = (e.get("lead") or "").strip()
            if lead_addr and lead_addr.lower() != sender.lower():   # replied from a forwarding/different address
                remove_lead(lead_addr); log("   also removed the address we originally emailed: %s" % lead_addr)
            new_neg.append(sender)
            log("NEGATIVE -> removed + blocklisted: %s  (\"%s\")" % (sender, snippet[:80]))
        elif kind == "positive":
            new_pos.append((sender, subject, snippet))
            log("POSITIVE -> HOT LEAD: %s  (\"%s\")" % (sender, snippet[:80]))
        elif kind == "ambiguous":
            new_amb.append((sender, subject, snippet))
            log("AMBIGUOUS -> review: %s  (\"%s\")" % (sender, snippet[:80]))
        else:
            log("auto/bot -> ignored: %s" % sender)
    save_seen(seen)

    if new_pos:
        with open(HOT, "a", encoding="utf-8") as f:
            for sender, subject, snip in new_pos:
                f.write("\n" + "="*70 + "\n")
                f.write("HOT LEAD  %s\n" % time.strftime("%Y-%m-%d %H:%M"))
                f.write("FROM: %s\nSUBJECT: %s\nTHEY SAID: %s\n" % (sender, subject, snip))
                f.write("-"*70 + "\nREPLY WITH THIS:\n" + reply_pitch() + "\n")
    if new_amb:
        with open(REV, "a", encoding="utf-8") as f:
            for sender, subject, snip in new_amb:
                f.write("[%s] %s | %s | %s\n" % (time.strftime("%Y-%m-%d %H:%M"), sender, subject, snip))

    log("pass done: %d new (%d hot, %d removed, %d review)" % (processed, len(new_pos), len(new_neg), len(new_amb)))
    # 2026-11-05 (Zayden): hand hot leads to the EMAIL AGENT to handle end-to-end — do NOT ping Zayden per reply.
    # Ambiguous stays in REVIEW.txt only (email agent sweeps it); no phone notification. Escalation is the agent's job.
    if new_pos:
        try:
            import subprocess as _sp
            for sender, subject, snip in new_pos:
                task = ("New WARM reply in Instantly from %s (subject: %s). They said: \"%s\". "
                        "Handle it end to end per your AUTONOMY rules: read the full thread in the Instantly Unibox, "
                        "reply in Zayden's voice, build + send a preview if they asked to see work, answer pricing if asked, "
                        "and book the call. Only tell Zayden if money/contract, a call is booked, or you're blocked."
                        % (sender, subject, snip[:300]))
                _sp.Popen(["python3", os.path.expanduser("~/claude-telegram-bot/team.py"), "ask", "email", task])
            log("handed %d hot lead(s) to email agent" % len(new_pos))
        except Exception as ex:
            log("email-agent handoff failed: %s" % ex)
    if new_pos:
        print("\n*** %d HOT LEAD(S) — see HOT-LEADS.txt and reply fast! ***" % len(new_pos))
        # Mac notification + sound so Zayden replies within minutes, not days
        import subprocess
        try:
            from reply_desk import add_hot          # reply from zayden@webblaze.io, not the outreach inboxes
            for sender, subject, snip in new_pos: add_hot(sender, subject, snip)
        except Exception as ex:
            log("reply desk error: %s" % ex)
        for sender, subject, snip in new_pos:
            msg = (snip[:120]).replace('"', "'").replace("\\", "")
            subprocess.run(["osascript", "-e",
                'display notification "%s" with title "HOT LEAD: %s" subtitle "Reply desk opened: reply from zayden@webblaze.io" sound name "Glass"' % (msg, sender.replace('"', ""))])

if __name__ == "__main__":
    main()
