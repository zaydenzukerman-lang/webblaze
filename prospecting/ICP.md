# WebBlaze — who we cold-email (Ideal Client Profile)

Goal: **~20 cold emails/day (~100/business-week)** → ~1% conversion → ~1 client/week → ~$300/wk.

## Volume math (the real bottleneck is SOURCING)
- scan.sh flags roughly ~10-20% of random small-biz domains as genuine targets, and a screenshot
  cuts that further (many "old jQuery/tables" sites are Weebly/Wix and actually look fine).
- So to email ~20 good targets/day you must SOURCE ~100-200 domains/day and scan them.
- Best domain sources at volume (not Google page-1, which skews modern):
  chamber-of-commerce member directories, BBB category lists, Yelp/YellowPages category pages,
  Google Maps listings for a niche+town. Collect raw domains → domains.txt → scan.sh.
- Realistic flow per day: pull ~150 domains → `scan.sh` → eyeball the score>=3 ones →
  email the ones that are truly dated. Fill remaining volume with a general (non-"your site is
  bad") offer to decent-but-plain sites.
- **Deliverability at 20/day:** send from a real domain address (hello@webblaze.io), NOT a raw
  Gmail; vary the wording per prospect (identical blasts get spam-filtered); keep it plain text.

## RULE: signals flag, screenshot decides
scan.sh SCORE is a filter, not a verdict. Always eyeball a score>=3 before emailing "your site
looks dated" — Weebly/Wix sites trip the old-jQuery/tables flags but often render fine.

## The target
A small **local service business** with an **outdated, generic, or non-mobile website**,
whose site is **purely informational** (marketing, not a web app).

Good fits (like our first clients — Sun finance, W Employment Law, Orange Beach charter):
- Solo / small **law firms** (estate, family, immigration, employment — not big PI firms)
- **Accountants / CPAs / tax prep / bookkeeping**
- **Insurance / financial** agencies (some — many already modern)
- **Contractors**: roofing, HVAC, plumbing, electrical, pool, landscaping, fencing
- **Trade B2B**: small manufacturers, machine shops, suppliers, wholesalers (often the WORST sites, real budgets)
- Small **medical/dental/chiro/vet** practices
- **Charters / tours / local attractions**, event & wedding vendors
- Local **restaurants**, real estate agents, nonprofits

## AVOID (bad fit for a simple static redesign)
- **Funeral homes** — need obituary/tribute systems (industry platforms). Too much functionality.
- Anything needing **e-commerce, booking engines, portals, or a CMS the owner edits daily**.
- Big firms with a marketing dept (they won't buy from a solo).
- Sites already on a clean modern build (see scanner — skip low scores).

## How to find the outdated ones (sourcing playbook)
Page-1 Google rankers usually already have decent sites. The outdated ones are found by:
1. Search `"<niche>" "<small/mid town>"` — smaller towns = older sites. Rotate towns.
2. Mine directories (Yelp/BBB/chamber-of-commerce member lists) for raw business domains.
3. Collect ~15–30 candidate domains into a `domains.txt`.
4. Run the scanner: `bash scan.sh domains.txt` — it flags NO-MOBILE, OLD-JQ, TABLES,
   FLASH, STALE-YEAR, CONSUMER-EMAIL and grabs a contact email. **Score >=4 = strong target.**
5. Eyeball the top scorers (one screenshot) to confirm it genuinely looks dated before emailing.
   Never cold-email "your site looks dated" about a site that's actually fine.

## What makes a reachable lead
- A real **owner email** on the site (mailto), ideally a consumer domain (gmail/aol/rr = low web
  sophistication = more likely to say yes). A contact form only = harder, lower priority.
- Small enough that the owner decides. $300 flat is an easy, low-risk yes.

## The pitch that converts (our edge)
We already build **free live redesign previews** (that's how Sun + WEL happened). For a hot
prospect, build a quick homepage redesign on `<slug>.webblaze.io` and send the live link:
"I rebuilt your homepage — free preview here." Seeing it beats describing it.

## NICHE YIELD (learned 2026-08-31)
HIGH-YIELD (genuinely outdated, often no-HTTPS/no-mobile — scanner nails them, no screenshot needed):
  welding/machine shops, upholstery, small-engine repair, bail bonds, older appliance shops,
  gun shops, feed stores, sign/trophy — the OLD TRADES that don't compete on Google.
LOW-YIELD (mostly modern lead-gen sites — skip or expect <10% hits):
  roofing, fencing, tree service, garage door, pool service, HVAC, plumbing, marine, pest/lawn,
  insurance. These compete on Google so they've already upgraded.
Rule: mine the OLD trades for volume. The reliable signal is NO-HTTPS / NO-MOBILE (a fact, no
screenshot needed); the soft "dated design" pitch needs an eyeball and converts worse.
