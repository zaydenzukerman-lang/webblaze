# RESUME — read this first after /clear (state as of 2026-07-12)

## What this business is
**Webblaze** (renaming FROM "Curb" — rebrand not yet executed, waiting on domain confirmation).
We sell **$300 flat websites** to small businesses via cold outreach, then upsell lead-gen/marketing
retainers after they're paying customers. Goal: sell 10 websites at $300. Dad handles money/accounts
(Zayden is a minor — contracts & payments in dad's name).

## READ THESE FILES IN ORDER
1. `~/.claude/projects/-Users-zaydenzukerman-north-star-game/memory/bookedsolid_business_model.md`
   — full business model, all decisions, rebrand history, current state. THE master doc.
2. `ops/SETUP.md` — Zayden's setup checklist (domain, FreshBooks, address, FB account)
3. `outreach/cold-email.md` + `ops/FACEBOOK-OUTREACH.md` — the outreach scripts/playbooks
4. `outreach/leads-nowebsite.md` — verified/dead lead statuses (mostly burned; only Dune Buggy usable)
5. `ops/CLIENT-RESULTS-PLAYBOOK.md`, `ops/SEO-MARKETING-MASTER.md` — fulfillment + marketing research
6. `ops/REPO-LEVERAGE.md` — the /ads audit skill + camoufox we adopted from the IG post
7. `clients/dunebuggy/` — the finished 5-page spec site (live at zaydenzukerman-lang.github.io/curb/dunebuggy/)

## DECISIONS LOCKED (don't re-litigate)
- Payments: **FreshBooks** (dad's account, includes card processing). Not PayPal, not Stripe.
- Channel: **Facebook Messenger** + email. Targeting: business must have **ZERO website** (any other
  online presence OK). NEW dad principle: prefer businesses that NEED a site to make money →
  **high-ticket BOOKING niches**: fishing charters, wedding vendors (DJ/photog/planner), party/event
  rentals (bounce house/photo booth), contractors. NOT product e-commerce (Shopify's turf).
- Website = build FIRST, they pay only if happy. First Messenger msg has NO link (ask "want the link?").
- No AI mentioned publicly ever. Never fake personal claims (no "I tried your burger").
- **BUDGET RULE (violated twice, do not violate again): NO parallel research subagents. Do lead
  research directly in main thread via WebSearch/WebFetch. See feedback_token_budget.md.**

## VERIFICATION RULE (learned hard — cheap agents fabricated "no website" ~60% of the time)
Every lead: Claude probes domain patterns + checks directory/FB, THEN Zayden does final 10-sec check
on the business's FB page (Intro → Website field) before sending. Zayden is the last gate.

## IN-FLIGHT LEADS — VERIFIED 2026-07-12, batch mostly BURNED
8 of 9 had websites (charters/party rentals need booking sites — wrong niche for zero-website
targeting). Full statuses in outreach/leads-nowebsite.md.
- **Only survivor: Orange Beach Fish Charter Services** (fb/orangebeachfishcharterservices,
  since 1980) — Zayden's FB check 7/15 found their FB links to orangebeachfish.com which is
  DEAD (503). Reclassified as a BROKEN-SITE lead (hotter: losing bookings in peak season).
  **Spec site BUILT 7/15**: clients/orangebeachfish/ → live at
  zaydenzukerman-lang.github.io/curb/orangebeachfish/. Opener angle: "your website link is broken."
  Phone/captain unknown — Zayden grabs from FB Intro, Claude wires in.
- Usable send list is now: Dune Buggy (site done) + Orange Beach Fish Charter (site done) +
  Small Town Lawn Service (probable-clean from earlier batch).
- Broken-site targeting implicitly opened 7/15 (Zayden ordered the build) — widens sourcing a lot.
- Don't source more leads until sending is unblocked — they go stale.

## PRICING CONFIRMED (2026-07-15): $300 flat stays
Zayden considered lowering, decided to TEST $300 first — still far under standard, maximizes
revenue. Websites are the ONLY product being sold right now; SEO/marketing/retainer services
launch later and get pitched to PREVIOUS (happy, paying) clients first.

## FACEBOOK ACCOUNT: ZAYDEN ALREADY HAS ONE, ~1 YEAR OLD (corrected 2026-07-15)
No creation, no warmup week needed — outreach can start IMMEDIATELY. (I wrongly kept listing
"create FB account" as a blocker; the FACEBOOK-OUTREACH.md setup/warmup section is N/A for him.)
Volume rules still apply: it's aged but has zero outreach history → start ~5 new businesses/day,
no links in message 1.

## STILL BLOCKED ON ZAYDEN
1. SEND the two ready messages (Dune Buggy + Orange Beach Fish Charter) — nothing blocks this now.
2. webblaze.io — bought? which registrar? (needed for rebrand + pro URL + email)
3. FreshBooks account (dad) — needed before first "yes"
4. Optional: install NotFair plugin (/plugin marketplace add nowork-studio/notfair ; /plugin install notfair@nowork-studio)

## TOOLS NOW AVAILABLE TO CLAUDE
- `/ads audit` skill installed (~/.claude/skills/ads) — paid-ads audit, basis for a "Webblaze Ad
  Audit" product ($150-300) for businesses already running ads.
- camoufox browser (~/.camoufox-venv) — anti-detect, for verification; Yelp still 403s headless.
- Repo: github.com/zaydenzukerman-lang/curb (will rename to webblaze on rebrand). Pages from /docs.
