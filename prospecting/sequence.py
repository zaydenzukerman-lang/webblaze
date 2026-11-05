#!/usr/bin/env python3
"""
Personal-email sequencer: owner-named, problem-proven emails from zayden@webblaze.io, no preview, goal = a booked call.

  python3 sequence.py queue [--limit 10]      pull top LeadFinder leads not yet in the sequence -> drafts -> sequence/approve.html
  python3 sequence.py approve [--skip a.com,b.com]   approve everything queued (minus skips)
  python3 sequence.py send [--dry-run]         send what is due: step 0 (approved), step 1 (+3 days), step 2 (+7 days); stops on reply/booking
  python3 sequence.py check                    scan Gmail for replies, bookings, bounces (bounce -> resend to the business inbox)
  python3 sequence.py status                   one-screen summary
  python3 sequence.py test <email>             send step 0 for the first queued lead to <email> (to see it)

Rules baked in: DAILY_CAP sends/day, 20s between sends, every email has an opt-out line, nothing is claimed that LeadFinder didn't verify.
"""
import argparse, email, html, imaplib, json, os, re, smtplib, subprocess, sys, time
import socket; socket.setdefaulttimeout(90)  # 2026-11-02: an IMAP read hung 3 days after the Mac slept mid-connection; never block forever
from datetime import datetime, timedelta
from email.header import decode_header, make_header
from email.message import EmailMessage
from email.utils import formataddr, make_msgid

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
DIR = os.path.join(HERE, "sequence"); os.makedirs(DIR, exist_ok=True)
DB = os.path.join(DIR, "leads.json"); APPROVE = os.path.join(DIR, "approve.html"); LOG = os.path.join(DIR, "sequence.log")
LF_LEADS = os.path.join(HERE, "leadfinder", "leads.json"); LF_SENT = os.path.join(HERE, "leadfinder", "sent_personal.json")
USER = "zayden@webblaze.io"; NAME = "Zayden Zukerman"
PW = open(os.path.expanduser("~/.maya-gmail-pass")).read().strip()
CAL = "https://calendly.com/zayden-webblaze/30min"
SEO_SHARE = 4             # of the daily new emails, this many go to the SEO track (good site, not top 3 on Maps)
DAILY_CAP = 10            # raise to 20 once a business mailing address is in the footer (CAN-SPAM)
STEP_DAYS = {1: 3, 2: 7}  # follow-ups: days after step 0
P = 'style="margin:0 0 14px"'
from email_v2 import SIG  # headshot signature


def jload(p, d):
    try: return json.load(open(p))
    except Exception: return d
def jsave(p, o): json.dump(o, open(p, "w"), indent=1)
def log(m):
    line = "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), m); print(line, flush=True); open(LOG, "a").write(line + "\n")
def now(): return datetime.now().isoformat(timespec="seconds")


# ---------- copy ----------
def problem_lines(L):
    """Turn LeadFinder's verified findings into subject + 1-2 plain sentences. Evidence only."""
    d = L["domain"]; kinds = {k: e for k, _, e in L.get("problems", [])}
    if "hacked" in kinds:
        subj, line = "%s has hidden spam links" % d, "I was looking at %s and found hidden links on your homepage to sites selling fake Oakleys, cheap jerseys and Pandora jewelry. Visitors can't see them, but Google can, and it usually means the site was hacked at some point. That can hurt how you show up in searches." % d if "oakley" in kinds["hacked"] else "I was looking at %s and found hidden spam links on your homepage (%s). Visitors can't see them, but Google can, and it usually means the site was hacked at some point." % (d, kinds["hacked"].split("to ", 1)[-1])
    elif "cert" in kinds:
        m = re.search(r"expired (\w+ +\d+ [\d:]+ \d{4})", kinds["cert"])
        when = (" The site's security certificate expired on %s." % datetime.strptime(m.group(1).replace("  ", " "), "%b %d %H:%M:%S %Y").strftime("%B %-d, %Y")) if m else ""
        subj, line = "%s shows a security warning" % d, "I pulled up %s and browsers show a security warning before the site even opens.%s That warning scares a lot of people away before they call." % (d, when)
    elif "insecure" in kinds:
        subj, line = '%s shows "Not secure"' % d, 'I pulled up %s and Chrome labels it "Not secure" in the address bar, because the site has no security certificate. A lot of people close a page when they see that.' % d
    elif "down" in kinds:
        subj, line = "%s won't load" % d, "I tried to open %s a couple of times and it wouldn't load, so anyone searching for you right now hits a dead end." % d
    elif "placeholder" in kinds:
        subj, line = "Your website still has placeholder text", "I was on %s and noticed it still shows template placeholder text (%s)." % (d, kinds["placeholder"].split(":", 1)[-1].strip()[:60])
    elif "localfile" in kinds:
        subj, line = "An image on %s isn't loading for visitors" % d, "I was on %s and one of the images loads from a file on your own computer, so visitors see a blank spot where it should be." % d
    elif "mobile" in kinds:
        subj, line = "%s on a phone" % d, "I pulled up %s on my phone and it isn't built for mobile, so everything is tiny and hard to tap. Most of your customers are finding you from their phones." % d
    elif "outdated" in kinds and int(re.search(r"(\d{4})", kinds["outdated"]).group(1)) <= datetime.now().year - 3:
        y = re.search(r"(\d{4})", kinds["outdated"]).group(1)
        subj, line = "Your website still says %s" % y, "I was on %s and noticed the bottom of the site still says %s. When people see an old year, a lot of them assume the business might be closed." % (d, y)
    elif "brokenimg" in kinds:
        subj, line = "Broken images on %s" % d, "I was on %s and noticed some of the images don't load (%s)." % (d, kinds["brokenimg"][:60])
    elif "title" in kinds:
        subj, line = "Your website's title in Google", "I was on %s and noticed the page title Google shows is %s, instead of your business name." % (d, kinds["title"].split("is", 1)[-1].strip())
    elif "slow" in kinds:
        subj, line = "%s took a while to load" % d, "I pulled up %s and it %s. Most people give up on a site after about 3 seconds." % (d, kinds["slow"])
    else:
        subj, line = "Quick question about %s" % d, "I was looking at %s and had a few ideas for making it bring in more customers." % d
    extra = [k for k in ("mobile", "outdated") if k in kinds and k not in subj.lower() and k not in line.lower()]
    if "mobile" in extra and "mobile" not in line: line += " It also isn't built for phones."
    if "outdated" in extra and "says" not in line and int(re.search(r"(\d{4})", kinds["outdated"]).group(1)) <= datetime.now().year - 3: line += " And the footer still says %s." % re.search(r"(\d{4})", kinds["outdated"]).group(1)
    return subj, line


def cal_button():
    return f"""<table cellpadding="0" cellspacing="0" style="margin:6px 0 8px"><tr><td bgcolor="#F7551F" style="background:#F7551F;border-radius:10px">
<a href="{CAL}" target="_blank" style="display:inline-block;padding:15px 26px;font-family:Arial,Helvetica,sans-serif;font-size:17px;font-weight:bold;color:#ffffff;text-decoration:none">&#128197; Book a call with me on Calendly</a>
</td></tr></table>
<p style="margin:0 0 16px;font-size:13px;color:#666">Or open this link: <a href="{CAL}" style="color:#666">{CAL.replace('https://', '')}</a></p>"""


OPTOUT = '<p style="margin:14px 0 0;font-size:12px;color:#888">Not interested? Just reply "no" and I won\'t email you again.</p>'


def nice_biz(name, domain):
    """'ACCOMPTAX, INC.' -> 'Accomptax'. Registry names are uppercase with legal suffixes."""
    n = re.sub(r"[,.]?\s*\b(inc|llc|l\.l\.c|corp|corporation|co|p\.?a|pllc|ltd|lc)\b\.?$", "", (name or domain).strip(), flags=re.I).strip(" ,.")
    if n.isupper(): n = " ".join(w if w in ("LLC", "PA", "CPA", "AC", "DJ", "USA") else w.capitalize() for w in n.split())
    return n or domain


PUBLIC = os.path.join(HERE, "..", "public"); PREVIEWS = os.path.join(DIR, "previews.json")   # {domain: slug}

def preview_url(L):
    slug = L.get("slug") or jload(PREVIEWS, {}).get(L["domain"])
    if slug and os.path.exists(os.path.join(PUBLIC, slug, "email-preview.jpg")):
        return "https://webblaze.io/%s/" % slug
    return None



def draft_seo(L, step, first, hi, biz):
    """Good website, not in Google Maps' top 3. Pitch = Maps/SEO. Proof = the exact search we ran."""
    q, pos = L["query"], L["pos"]; comps = [c["name"] for c in L.get("competitors", [])][:3]
    clist = ", ".join(comps[:-1]) + " and " + comps[-1] if len(comps) > 1 else (comps[0] if comps else "")
    if step == 0:
        subject = ("%s, you're #%d on Google Maps" % (first, pos)) if first else "%s is #%d on Google Maps" % (biz, pos)
        line = 'Your website looks great. But when I searched "%s" on Google Maps, %s came up #%d, below %s. Most people never scroll past the top 3, so a lot of those customers end up calling them.' % (q, html.escape(biz), pos, html.escape(clist))
        body = f"""<p {P}>{hi}</p>
<p {P}>{line}</p>
<p {P}>I'm a teenager who helps South Florida businesses climb into those top spots on Google Maps and Google search. That means a fully optimized Business Profile, more reviews, and pages on your site that match what people actually search for.</p>
<p {P}>Want me to show you exactly why they're ranking above you and what I'd change? It's a quick call, and you'll walk away with the list either way.</p>
{cal_button()}
<p style="margin:0 0 14px">Thanks,<br>Zayden</p>{SIG}{OPTOUT}"""
        text = (f"{hi}\n\n" + re.sub(r"<[^>]+>", "", html.unescape(line)) + "\n\nI'm a teenager who helps South Florida businesses climb into those top spots on Google Maps and Google search. That means a fully optimized Business Profile, more reviews, and pages on your site that match what people actually search for.\n\n"
                "Want me to show you exactly why they're ranking above you and what I'd change? It's a quick call, and you'll walk away with the list either way.\n\nBook a call: " + CAL + "\n\nThanks,\nZayden Zukerman\nWebBlaze | webblaze.io\n\nNot interested? Just reply \"no\" and I won't email you again.")
        return subject, body, text
    if step == 1:
        b = f"<p {P}>{hi}</p><p {P}>Bumping this in case it got buried. Happy to walk you through exactly what's keeping {html.escape(biz)} out of the top 3 on Google Maps. It takes about 15 minutes and you keep the list either way.</p>{cal_button()}<p style=\"margin:0 0 14px\">Thanks,<br>Zayden</p>{SIG}{OPTOUT}"
        t = f"{hi}\n\nBumping this in case it got buried. Happy to walk you through exactly what's keeping {biz} out of the top 3 on Google Maps. It takes about 15 minutes and you keep the list either way.\n\nBook a call: {CAL}\n\nThanks,\nZayden"
        return None, b, t
    b = f"<p {P}>{hi}</p><p {P}>I'll stop emailing after this one. If you ever want to get {html.escape(biz)} into the top 3 on Google Maps, you can grab a time with me anytime:</p>{cal_button()}<p style=\"margin:0 0 14px\">Thanks,<br>Zayden</p>{SIG}{OPTOUT}"
    t = f"{hi}\n\nI'll stop emailing after this one. If you ever want to get {biz} into the top 3 on Google Maps, you can grab a time with me anytime: {CAL}\n\nThanks,\nZayden"
    return None, b, t

def draft(L, step):
    first = L.get("owner_first") or ""; hi = "Hi %s," % first if first else "Hi,"
    biz = nice_biz(L.get("business"), L["domain"])
    subj, line = problem_lines(L)
    url = preview_url(L)
    if L.get("kind") == "seo":
        return draft_seo(L, step, first, hi, biz)
    if step == 0 and url:
        subject = "%s, I rebuilt your website" % first if first else "I rebuilt your website"
        body = f"""<p {P}>{hi}</p>
<p {P}>{html.escape(line)}</p>
<p {P}>So I rebuilt it for you for free, using your own text and photos. Click the picture to see it:</p>
<p style="margin:0 0 16px"><a href="{url}" target="_blank"><img src="{url}email-preview.jpg" alt="Your new website: click to open" width="560" style="width:560px;max-width:100%;height:auto;border:1px solid #ddd;border-radius:8px;display:block"></a></p>
<p {P}>I'm a teenager who builds websites for South Florida businesses. If you like it, I'll make any changes you want on a quick call and it can be live the same day. You don't pay anything until it's live and you love it, and there's a 30-day money-back guarantee. I can also put your site in any language your customers speak, like Spanish, Haitian Creole or Portuguese, at no extra cost.</p>
<p style="margin:0 0 4px"><b>If you book this week, your first month of Google Maps is on me (normally $500).</b></p>
{cal_button()}
<p style="margin:0 0 14px">Thanks,<br>Zayden</p>{SIG}{OPTOUT}"""
        text = f"{hi}\n\n{line}\n\nSo I rebuilt it for you for free, using your own text and photos. See it here: {url}\n\nI'm a teenager who builds websites for South Florida businesses. If you like it, I'll make any changes you want on a quick call and it can be live the same day. You don't pay anything until it's live and you love it, and there's a 30-day money-back guarantee. I can also put your site in any language your customers speak, like Spanish, Haitian Creole or Portuguese, at no extra cost.\n\nIf you book this week, your first month of Google Maps is on me (normally $500).\n\nBook a call: {CAL}\n\nThanks,\nZayden Zukerman\nWebBlaze | webblaze.io\n\nNot interested? Just reply \"no\" and I won't email you again."
    elif step == 0:
        subject = ("%s, %s" % (first, subj[0].lower() + subj[1:])) if first else subj
        body = f"""<p {P}>{hi}</p>
<p {P}>{html.escape(line)}</p>
<p {P}>I'm a teenager who builds websites for South Florida businesses. I'd like to build {html.escape(biz)} a new version of the site, using your own photos and wording, so you can see exactly what you'd get before deciding anything.</p>
<p {P}>Here's how it works: on a quick call you tell me what you want the site to do. Then I build it and send you a short video walking you through it. You don't pay anything until it's live and you love it, and there's a 30-day money-back guarantee. I can also put your site in any language your customers speak, like Spanish, Haitian Creole or Portuguese, at no extra cost.</p>
<p style="margin:0 0 4px"><b>If you book this week, your first month of Google Maps is on me (normally $500).</b></p>
{cal_button()}
<p style="margin:0 0 14px">Thanks,<br>Zayden</p>{SIG}{OPTOUT}"""
        text = f"{hi}\n\n{line}\n\nI'm a teenager who builds websites for South Florida businesses. I'd like to build {biz} a new version of the site, using your own photos and wording, so you can see exactly what you'd get before deciding anything.\n\nHere's how it works: on a quick call you tell me what you want the site to do. Then I build it and send you a short video walking you through it. You don't pay anything until it's live and you love it, and there's a 30-day money-back guarantee. I can also put your site in any language your customers speak, like Spanish, Haitian Creole or Portuguese, at no extra cost.\n\nIf you book this week, your first month of Google Maps is on me (normally $500).\n\nBook a call: {CAL}\n\nThanks,\nZayden Zukerman\nWebBlaze | webblaze.io\n\nNot interested? Just reply \"no\" and I won't email you again."
    elif step == 1:
        subject = None  # same thread
        body = f"""<p {P}>{hi}</p>
<p {P}>{("Bumping this in case it got buried. The new site I built for you is still up here: <a href=\"%s\">%s</a>. Nothing to pay until it's live." % (url, url.replace("https://", ""))) if url else ("Bumping this in case it got buried. The offer still stands: a quick call, you tell me what you want %s's site to do, I build it and send you a video walkthrough. Nothing to pay until it's live." % html.escape(biz))}</p>
<p style="margin:0 0 4px"><b>The free first month of Google Maps (normally $500) still stands if you book by Friday.</b></p>
{cal_button()}
<p style="margin:0 0 14px">Thanks,<br>Zayden</p>{SIG}{OPTOUT}"""
        text = f"{hi}\n\nBumping this in case it got buried. The offer still stands: a quick call, you tell me what you want {biz}'s site to do, I build it and send you a video walkthrough. Nothing to pay until it's live.\n\nThe free first month of Google Maps (normally $500) still stands if you book by Friday.\n\nBook a call: {CAL}\n\nThanks,\nZayden"
    else:
        subject = None
        body = f"""<p {P}>{hi}</p>
<p {P}>I'll stop emailing after this one. If a new website ever comes up for {html.escape(biz)}, you can grab a time with me anytime:</p>
{cal_button()}
<p style="margin:0 0 14px">Thanks,<br>Zayden</p>{SIG}{OPTOUT}"""
        text = f"{hi}\n\nI'll stop emailing after this one. If a new website ever comes up for {biz}, you can grab a time with me anytime: {CAL}\n\nThanks,\nZayden"
    return subject, body, text


# ---------- queue / approve ----------
FREEMAIL = {"gmail.com","yahoo.com","hotmail.com","outlook.com","aol.com","icloud.com","bellsouth.net","msn.com","live.com","comcast.net","att.net"}


def pick_to(o, L):
    """Recipient for a personal email from zayden@webblaze.io. Guessed addresses (first@domain) bounced ~20%
    (Oct 21-28: 10 bounces) and bounces hurt webblaze.io itself, so: an owner email FOUND on their site wins,
    otherwise the business inbox listed on their site. Never send to an unverified guess. Returns (to, fallback)."""
    best, biz, basis = o.get("best_email") or "", L.get("email") or "", o.get("email_basis", "")
    def ours(e):   # address must belong to THIS business (federatedtitletrust.com once came with amy@pandoraevents.com)
        d = e.split("@")[-1].lower(); lab = re.sub(r"[^a-z0-9]", "", L["domain"].split(".")[0].lower()); dl = re.sub(r"[^a-z0-9]", "", d.split(".")[0])
        return d in FREEMAIL or dl[:5] == lab[:5]
    if biz and not ours(biz): biz = ""
    if best and (basis.startswith("found-on-site") or basis.startswith("site-personal")):
        return best, (biz if biz != best else "")
    return biz, ""


def queue(limit):
    db = jload(DB, []); have = {x["domain"] for x in db}
    sent_lf = set(jload(LF_SENT, [])); added = []
    pv = jload(PREVIEWS, {})
    pool = sorted(jload(LF_LEADS, []), key=lambda L: (L["domain"] not in pv, -L["score"]))   # leads with a finished preview go first
    for L in pool:
        if L["domain"] in have or L["domain"] in sent_lf: continue
        o = L.get("owner") or {}
        to, fb = pick_to(o, L)
        if not to: continue
        # Business name: the Google Maps listing name first (what the owner calls it), registry name second.
        # Never a name scraped off the site (pgtcpa.com came back as "Intuit Inc." from a QuickBooks badge).
        label = re.sub(r"[^a-z0-9]", "", L["domain"].split(".")[0])
        cands = [L.get("name"), o.get("sunbiz_name"), o.get("business")]
        biz = next((c for c in cands if c and (re.sub(r"[^a-z0-9]", "", c.lower())[:5] in label or label[:5] in re.sub(r"[^a-z0-9]", "", c.lower()) or c == L.get("name"))), L.get("name") or L["domain"])
        rec = dict(domain=L["domain"], business=biz[:60], owner_first=o.get("owner_first", ""), owner_last=o.get("owner_last", ""),
                   to=to, fallback=fb, email_basis=o.get("email_basis", ""),
                   niche=L.get("niche", ""), city=L.get("city", ""), phone=L.get("phone", ""), problems=L.get("problems", []), score=L["score"],
                   status="approved", steps=[], created=now(), notes="", slug=pv.get(L["domain"], ""))   # Zayden 10-14: send without an approval step
        db.append(rec); added.append(rec)
        if len(added) >= limit: break
    # SEO track: good websites that aren't in Google Maps' top 3 (seo/leads.json from seofinder.py)
    seo_room = max(0, SEO_SHARE - sum(1 for x in db if x["status"] == "approved" and x.get("kind") == "seo"))
    for L in jload(os.path.join(HERE, "seo", "leads.json"), []):
        if seo_room <= 0: break
        if L["domain"] in have or L["domain"] in sent_lf or not L.get("pos"): continue
        o = L.get("owner") or {}; to, fb = pick_to(o, L)
        if not to: continue
        import seo_instantly
        if not seo_instantly.ok_lead(L, to): continue          # same quality bar as the Instantly SEO campaign (#4-#20, real local business)
        rec = dict(domain=L["domain"], kind="seo", business=(L.get("maps_name") or L.get("name") or o.get("sunbiz_name") or L["domain"])[:60], owner_first=o.get("owner_first", ""), owner_last=o.get("owner_last", ""),
                   to=to, fallback=fb, email_basis=o.get("email_basis", ""), niche=L.get("niche", ""), city=L.get("city", ""),
                   query=L["query"], pos=L["pos"], competitors=L.get("competitors", []), problems=[], score=L.get("score", 0), status="approved", steps=[], created=now(), notes="", slug="")
        db.append(rec); added.append(rec); have.add(L["domain"]); seo_room -= 1
    jsave(DB, db); log("queued %d (auto-approved)" % len(added)); build_approve(db)


def build_approve(db):
    q = [x for x in db if x["status"] in ("queued", "approved") and not x["steps"]]
    cards = ""
    for x in q:
        subject, body, _ = draft(x, 0)
        basis = "found on their site" if x["email_basis"].startswith("found-on-site") else "pattern guess (bounce -> %s)" % (x["fallback"] or "none")
        cards += f"""<div class=c><div class=m><b>{html.escape(x['business'])}</b> · {html.escape(x['niche'])} · {html.escape(x['city'])} · score {x['score']}<br>
<b>To:</b> {html.escape(x['to'])} <small>({basis})</small> &nbsp; <b>Subject:</b> {html.escape(subject)}<br><small>proof: {html.escape('; '.join(e for _,_,e in x['problems'])[:200])}</small>
<br><code>skip: {x['domain']}</code></div><div class=mail>{body}</div></div>"""
    open(APPROVE, "w").write(f"""<!doctype html><meta charset=utf-8><title>Approve today's batch</title><style>
body{{font-family:-apple-system,sans-serif;background:#f4f6f8;padding:28px;max-width:760px;margin:auto;color:#1d2733}}
.c{{background:#fff;border-radius:14px;margin:18px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);overflow:hidden}}.m{{padding:14px 20px;border-bottom:1px solid #eef1f4;font-size:14px}}
.mail{{padding:20px 24px;font:15px/1.55 Arial;color:#222}}code{{background:#eef1f4;padding:2px 6px;border-radius:6px;font-size:12px}}</style>
<h1>Next batch: {len(q)} emails</h1><p>These go out automatically at 9:30 AM on weekdays (cap {DAILY_CAP}/day). Tell Claude "skip X" to pull one.</p>{cards}""")


def approve(skips):
    db = jload(DB, []); n = 0
    for x in db:
        if x["status"] in ("queued", "approved") and not x["steps"]:
            if x["domain"] in skips: x["status"] = "skipped"
            else: x["status"] = "approved"; n += 1
    jsave(DB, db); log("approved %d, skipped %d" % (n, len(skips)))


# ---------- gmail ----------
def imap(box="INBOX"):
    m = imaplib.IMAP4_SSL("imap.gmail.com"); m.login(USER, PW); m.select(box, readonly=True); return m

def hdr(v): return str(make_header(decode_header(v or "")))

def body_text(msg):
    if msg.is_multipart():
        for p in msg.walk():
            if p.get_content_type() == "text/plain": return p.get_payload(decode=True).decode(p.get_content_charset() or "utf-8", "replace")
        return ""
    return msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", "replace")


def instantly_engaged(x):
    """2026-11-05: this personal sequence and the Instantly campaigns are separate reply-tracking
    silos. check() used to only scan the zayden@webblaze.io Gmail thread for replies, so a lead who
    replied on an INSTANTLY thread instead (exactly how Kenaz Cohen's lead was created in the first
    place -- email_basis 'replied-on-instantly') stayed status 'sent' forever and kept getting
    auto-bumped on schedule, even after he'd already replied and declined the website. This looks the
    lead up directly in Instantly (any campaign, not just the one it came from) by email/domain and
    returns (True, reason) if they've already replied or been blocklisted ANYWHERE. Call before every
    send, not just bumps -- an 'approved' lead that already replied on Instantly before we ever sent
    step 0 should never get step 0 either."""
    import feed_campaign
    dom = (x.get("domain") or "").lower()
    candidates = [e.lower() for e in (x.get("to"), x.get("fallback")) if e]
    try:
        if any(e in feed_campaign.blocklist() for e in candidates) :
            return True, "blocklisted"
    except Exception as e:
        log("instantly_engaged: blocklist check failed for %s: %s" % (dom, e))
    for term in candidates or [dom]:
        try:
            d, err = feed_campaign.api("leads/list", "POST", {"search": term, "limit": 5})
            if err or not d: continue
            for it in d.get("items", []):
                lead_email = (it.get("email") or "").lower()
                if lead_email not in candidates and dom and dom not in lead_email: continue
                if (it.get("email_reply_count") or 0) > 0:
                    return True, "replied-on-instantly (%s)" % (it.get("timestamp_last_reply") or "")
        except Exception as e:
            log("instantly_engaged: lookup failed for %s: %s" % (term, e))
    return False, ""


def sync_instantly_status(db, save=True):
    """Cross-silo fix: before any send/bump decision, catch leads that engaged on the Instantly side
    (reply or opt-out) that our Gmail-only check() would otherwise miss. Does NOT fire the
    telegram-ping / call-brief side effects check() uses for brand-new live replies -- this is just
    catching up stale status on something that (by definition) already happened and was likely
    already handled by hand; it should be quiet, not re-alert."""
    watched = [x for x in db if x["status"] in ("sent", "bounced", "approved")]
    for x in watched:
        engaged, reason = instantly_engaged(x)
        if not engaged: continue
        if reason == "blocklisted":
            x["status"] = "optout"; x["notes"] = ((x.get("notes") or "") + " | SYNCED FROM INSTANTLY: blocklisted/opted out elsewhere").strip()
        else:
            x["status"] = "replied"; x["notes"] = ((x.get("notes") or "") + " | SYNCED FROM INSTANTLY: %s" % reason).strip()
        log("SYNC: %s (%s) -> %s [%s]" % (x["business"], x["domain"], x["status"], reason))
    if save: jsave(DB, db)
    return db


def check(db=None, save=True):
    """Replies, bookings, bounces since each lead's step 0. Returns list of events."""
    db = db if db is not None else jload(DB, []); events = []
    sync_instantly_status(db, save=False)   # cross-silo fix: catch Instantly-side replies/opt-outs first
    if save: jsave(DB, db)
    live = [x for x in db if x["status"] in ("sent", "bounced") and x["steps"]]
    if not live: return events
    since = min(x["steps"][0]["sent_at"] for x in live)[:10]
    m = imap(); d = datetime.fromisoformat(since).strftime("%d-%b-%Y")
    _, data = m.uid("search", None, "SINCE", d); uids = data[0].split()
    msgs = []
    for u in uids[-400:]:
        _, y = m.uid("fetch", u, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE IN-REPLY-TO)])")
        msgs.append((u, email.message_from_bytes(y[0][1])))
    for x in live:
        dom = x["domain"]; mids = {s.get("message_id") for s in x["steps"]}
        for u, h in msgs:
            frm = hdr(h["From"]).lower(); irt = (h["In-Reply-To"] or "").strip(); subj = hdr(h["Subject"])
            is_bounce = "mailer-daemon" in frm or "postmaster" in frm or re.search(r"delivery status notification|undeliverable|delivery has failed|returned mail|failure notice", subj, re.I)
            if not is_bounce and (("@" + dom) in frm or x["to"].lower() in frm or irt in mids):
                x["status"] = "replied"; x["notes"] = "reply %s: %s" % (hdr(h["Date"])[:16], subj[:60])
                try:                                                   # opt-out? -> blocklist in Instantly too, so no campaign ever emails them
                    _, full = m.uid("fetch", u, "(BODY.PEEK[])"); body = body_text(email.message_from_bytes(full[0][1]))
                    body = re.split(r"\n\s*On .{5,140}wrote:|\n>", body)[0]
                    import closer
                    if closer.classify(frm, subj, body) == "negative":
                        x["status"] = "optout"; x["notes"] += " | OPT-OUT"
                        import feed_campaign; feed_campaign.api("block-lists-entries", "POST", {"bl_value": x["to"].lower()})
                        s2 = set(jload(LF_SENT, [])); s2.add(x["domain"]); jsave(LF_SENT, sorted(s2))
                        events.append(("optout", x, subj)); break
                except Exception as e: log("opt-out check failed for %s: %s" % (x["to"], e))
                events.append(("reply", x, subj)); break
            if "calendly" in frm and "new event" in subj.lower():
                _, full = m.uid("fetch", u, "(BODY.PEEK[])"); t = body_text(email.message_from_bytes(full[0][1])).lower()
                if x["to"].lower() in t or ("@" + dom) in t:
                    x["status"] = "booked"; x["notes"] = "booked: " + subj[:70]; events.append(("booked", x, subj)); break
            if is_bounce and (irt in mids or True):
                _, full = m.uid("fetch", u, "(BODY.PEEK[])"); t = body_text(email.message_from_bytes(full[0][1])).lower()
                if x["to"].lower() in t and x["status"] != "bounced":
                    events.append(("bounce", x, x["to"]))
                    if x["fallback"]:
                        x["notes"] = "bounced %s -> resend to %s" % (x["to"], x["fallback"]); x["to"], x["fallback"] = x["fallback"], ""
                        x["steps"] = []; x["status"] = "approved"      # resend step 0 to the business inbox
                    else: x["status"] = "bounced"
                    break
    if save: jsave(DB, db)
    for ev, x, s in events: log("%s: %s (%s) %s" % (ev, x["business"], x["domain"], s[:50]))
    try:                                          # instant phone alert (2026-11-04)
        from tg_notify import ping
        for ev, x, s in events:
            if ev == "booked": ping("📅 CALL BOOKED: %s (%s)\n%s\nSay \"call brief %s\" and I'll prep you." % (x["business"], x["to"], s[:120], x["domain"]))
            elif ev == "reply": ping("💬 %s replied to your personal email (%s)\nSubject: %s\nSay \"handle %s\" and I'll draft a reply." % (x["business"], x["to"], s[:120], x["to"]))
    except Exception as e: log("telegram ping failed: %s" % e)
    for ev, x, s in events:                       # every booking or reply gets a call brief, opened right away
        if ev in ("booked", "reply"):
            try:
                import callbrief; path = callbrief.build(x["domain"])
                subprocess.run(["osascript", "-e", 'display notification "%s: call brief ready" with title "WebBlaze %s" sound name "Glass"' % (x["business"][:40].replace('"', "'"), ev.upper())])
            except Exception as e: log("call brief failed for %s: %s" % (x["domain"], e))
    return events


# ---------- send ----------
def send_one(x, step, smtp, to=None):
    subject, body, text = draft(x, step)
    msg = EmailMessage(); msg["From"] = formataddr((NAME, USER)); msg["To"] = to or x["to"]
    msg["Message-ID"] = make_msgid(domain="webblaze.io")
    if step == 0: msg["Subject"] = subject
    else:
        s0 = x["steps"][0]; msg["Subject"] = "Re: " + s0["subject"]; msg["In-Reply-To"] = s0["message_id"]; msg["References"] = s0["message_id"]
    msg.set_content(text); msg.add_alternative('<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#222">%s</div>' % body, subtype="html")
    smtp.send_message(msg)
    return dict(n=step, sent_at=now(), message_id=msg["Message-ID"], subject=msg["Subject"], to=msg["To"])


def send(dry):
    db = jload(DB, []); check(db, save=True); db = jload(DB, [])
    waiting = sum(1 for x in db if x["status"] == "approved")
    waiting_seo = sum(1 for x in db if x["status"] == "approved" and x.get("kind") == "seo")
    if (waiting < DAILY_CAP or waiting_seo < SEO_SHARE) and not dry:   # top up so the machine never runs dry, SEO always gets its share
        queue(max(0, DAILY_CAP - waiting)); db = jload(DB, [])
    today = time.strftime("%Y-%m-%d"); sent_today = sum(1 for x in db for s in x["steps"] if s["sent_at"][:10] == today)
    due = []
    for x in db:
        if x["status"] == "approved": due.append((x, 0))
        elif x["status"] == "sent":
            n = len(x["steps"]); t0 = datetime.fromisoformat(x["steps"][0]["sent_at"])
            if n in STEP_DAYS and datetime.now() >= t0 + timedelta(days=STEP_DAYS[n]): due.append((x, n))
    # Follow-ups are never capped (they're replies in an existing thread, a handful a day); the cap only limits NEW emails.
    # Order: hot-lead follow-ups, other follow-ups, then new emails with a preview, then new without.
    due.sort(key=lambda t: (t[1] == 0, t[0].get("score", 0) < 99, not preview_url(t[0])))
    # reserve SEO_SHARE of today's new-email slots for SEO-track leads
    new0 = [d for d in due if d[1] == 0]; seo0 = [d for d in new0 if d[0].get("kind") == "seo"][:SEO_SHARE]
    rest0 = [d for d in new0 if d not in seo0]
    due = [d for d in due if d[1] != 0] + seo0 + rest0
    new_today = sum(1 for x in db for s in x["steps"] if s["sent_at"][:10] == today and s["n"] == 0)
    room_new = max(0, DAILY_CAP - new_today)
    due = [d for d in due if d[1] != 0] + [d for d in due if d[1] == 0][:room_new]
    room = len(due)
    log("due: %d (step0 %d, followups %d); sent today %d; cap room %d" % (len(due), sum(1 for _, n in due if n == 0), sum(1 for _, n in due if n), sent_today, room))
    if dry:
        for x, n in due[:room]: print("  would send step", n, "->", x["to"], "|", x["business"], "| PREVIEW" if n == 0 and preview_url(x) else "")
        return
    smtp = None
    for x, n in due[:room]:
        if smtp is None: smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465); smtp.login(USER, PW)
        try:
            rec = send_one(x, n, smtp); x["steps"].append(rec); x["status"] = "sent" if n < 2 else "done"
            log("sent step %d -> %s (%s)" % (n, x["to"], x["business"]))
            if n == 0:
                s = set(jload(LF_SENT, [])); s.add(x["domain"]); jsave(LF_SENT, sorted(s))
            jsave(DB, db); time.sleep(20)
        except Exception as e: log("SEND FAILED %s: %s" % (x["to"], e))
    if smtp: smtp.quit()


def status():
    db = jload(DB, []); from collections import Counter
    c = Counter(x["status"] for x in db); print(dict(c), "| total", len(db))
    for x in db:
        if x["status"] in ("replied", "booked"): print("  ", x["status"].upper(), x["business"], x["to"], "|", x["notes"])


def wait_for_network(host="imap.gmail.com", minutes=20):
    """launchd fires right after the Mac wakes, before Wi-Fi is back (Oct 29: DNS error, no emails sent). Wait for it."""
    import socket, time as _t
    for _ in range(minutes * 6):
        try: socket.getaddrinfo(host, 993); return True
        except OSError: _t.sleep(10)
    return False


if __name__ == "__main__":
    wait_for_network()
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("queue").add_argument("--limit", type=int, default=10)
    sub.add_parser("approve").add_argument("--skip", default="")
    sub.add_parser("send").add_argument("--dry-run", action="store_true")
    sub.add_parser("check"); sub.add_parser("status"); sub.add_parser("test").add_argument("email")
    a = ap.parse_args()
    if a.cmd == "queue": queue(a.limit)
    elif a.cmd == "approve": approve({s.strip().lower() for s in a.skip.split(",") if s.strip()})
    elif a.cmd == "send": send(a.dry_run)
    elif a.cmd == "check": check()
    elif a.cmd == "status": status()
    elif a.cmd == "test":
        db = jload(DB, []); x = next((x for x in db if x["status"] in ("queued", "approved")), None)
        if not x: print("nothing queued"); sys.exit()
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465); s.login(USER, PW)
        print("sent test:", send_one(x, 0, s, to=a.email)["subject"]); s.quit()
    else: print(__doc__)
