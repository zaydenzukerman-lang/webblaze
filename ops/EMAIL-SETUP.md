# Curb — Email Infrastructure Setup (Zayden's 30-minute guide)

Goal: send cold email from hello@curbwebsites.com that lands in inboxes, not spam.

## Step 1 — Domain (10 min, with dad's card)
Buy **curbwebsites.com** at Cloudflare Registrar (at-cost, free DNS) or Namecheap. Dad's name/card.

## Step 2 — Mailbox (10 min) — forwarding is NOT enough, we must SEND
Pick one:
- **Zoho Mail Free** — free, 1 custom-domain mailbox. Fine for us. zoho.com/mail → add domain → create hello@curbwebsites.com
- **Google Workspace** (~$7/mo) — nicer, Gmail interface. Either works.

## Step 3 — DNS records (10 min — paste these in the registrar's DNS panel)
Zoho/Google will show you the exact values during setup. You will paste:
1. **MX records** — mail delivery (from Zoho/Google setup screen)
2. **SPF** (TXT record) — e.g. Zoho: `v=spf1 include:zohomail.com ~all`
3. **DKIM** (TXT record) — generated in the Zoho/Google admin panel, copy-paste
4. **DMARC** (TXT record, name `_dmarc`): `v=DMARC1; p=none; rua=mailto:hello@curbwebsites.com`
Then send a test email to your personal Gmail → check it arrives NOT in spam → open
"show original" → confirm SPF: PASS, DKIM: PASS. Tell Claude the domain is live → I wire the
website contact button + quote form the same day.

## Step 4 — Mailing address (CAN-SPAM, required in every email footer)
Home address is legally sufficient and free — use it unless dad wants privacy, in which case a
P.O. box (~$12/mo) works too. 2-minute decision, not a purchase blocker.

## Step 5 — Warmup schedule (don't skip — new domains that blast get burned permanently)
- Days 1–2: email friends/family from the new address, get replies. 5-10 sends.
- Days 3–7: 10–15 cold sends/day max
- Week 2+: up to 25–30/day. Never more, never bulk tools, always personalized.
- Watch: if replies stop landing / you see bounces, STOP and tell Claude.

## Footer that goes on every cold email (compliance, already in templates)
> Curb · [P.O. Box ___, City, ST ZIP] · If you'd rather not hear from me, reply "no" and that's the end of it.
