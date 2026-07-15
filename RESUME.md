# RESUME — read this first after /clear (state as of 2026-07-15)

## What this business is
**Webblaze** — rebrand from "Curb" EXECUTED 2026-07-15 (repo renamed, domain live, brand text
updated everywhere). We sell **$300 flat websites** to small businesses via cold outreach, then
upsell lead-gen/marketing retainers after they're paying customers. Goal: sell 10 websites at $300.
Dad handles money/accounts (Zayden is a minor — contracts & payments in dad's name).

## REBRAND EXECUTED 2026-07-15 — Webblaze is now the real, live brand
- Domain **webblaze.io** confirmed registered — turns out it's registered under **Forest Zukerman
  (Zayden's dad) / Proactium.ai**, Namecheap, WhoisGuard. GitHub repo renamed `curb` → `webblaze`.
  All "Curb" brand text replaced across every file (site, docs, ops, outreach).
- ops/curb-chrome.sh renamed to ops/webblaze-chrome.sh.

## ARCHITECTURE SPLIT 2026-07-15 (resolves a same-day domain collision — read this)
Same day the rebrand happened, Zayden's dad's own agent ("Concierge") independently dropped a
`~/webblaze/WEBBLAZE_BRIEF.md` + 4 logo concepts (`~/webblaze/branding/`), expecting a FRESH
Next.js/Vercel build at webblaze.io — dad has a Vercel account (`forest-9003`) with 25 OTHER live
production apps on it (courtcounsel-app, hqintake-portal, etc.) — extreme caution required, see
"VERCEL SAFETY RULES" below. Zayden's call (2026-07-15): **go with dad's Vercel/Next.js build for
the webblaze.io ROOT domain** (the agency's own marketing homepage). Resolution — no real conflict:
- **webblaze.io (root)** = new Next.js marketing site for the Webblaze agency itself, built in
  `~/webblaze/`, deployed via dad's Vercel. DNS for this gets pointed by Concierge/dad (his
  registrar account) — NOT the GitHub Pages A-records I originally drafted; those are retracted.
- **GitHub Pages (`zaydenzukerman-lang.github.io/webblaze/...`)** = stays exactly as-is, no domain
  needed. This is where CLIENT DEMO/SPEC sites live pre-payment (Dune Buggy, Orange Beach Fish
  Charter, future leads). Once a client pays, their site migrates to THEIR OWN domain anyway — it
  was never going to live at webblaze.io regardless of this collision.
- Old `site/index.html` / `docs/index.html` (the static "Curb"→"Webblaze" agency homepage) is now
  SUPERSEDED by the new Vercel build — kept in the repo as reference/backup only, not the canonical
  marketing site going forward.

## WEBBLAZE.IO MARKETING SITE — BUILT & DEPLOYED 2026-07-15
Next.js + Tailwind site built in `~/webblaze/` (separate repo from bookedsolid, its own git history).
Sections: hero ($300 flat pitch), portfolio (real screenshots of Dune Buggy + Orange Beach Fish
Charter linking to their live GitHub Pages demos), how-it-works (3 steps), pricing card, FAQ,
contact (mailto:webblazeio@gmail.com — a fresh Gmail Zayden made 7/15, works immediately, no
domain/DNS needed; hello@webblaze.io dropped since it required dad's Namecheap access with no
"another way" that avoids DNS entirely — domain email can wait). Design ran
through ui-ux-pro-max per our standard. Uses dad's placeholder logos (flame wordmark header,
W-monogram favicon) — logo winner not yet confirmed by dad, flagged as placeholder.
- **LIVE NOW**: https://webblaze-two.vercel.app (deployed under dad's `hbz-holdings` Vercel team
  scope, project name `webblaze` — confirmed isolated from his other 25 projects).
- **webblaze.io domain NOT attached yet** — that's dad/Concierge's step (`vercel domains add
  webblaze.io` + his Namecheap DNS change: A record @ → 76.76.21.21, CNAME www → cname.vercel-dns.com).
  Tell Zayden's dad the site is ready to go live whenever he wants to point the domain.
- To redeploy after changes: `cd ~/webblaze && vercel --yes --scope hbz-holdings` (preview) or
  add `--prod` to update production. ALWAYS pass `--scope hbz-holdings` explicitly (no default
  scope in non-interactive mode) and ALWAYS run from inside `~/webblaze`.

## VERCEL SAFETY RULES (from dad's brief — treat as hard law, not a suggestion)
- Vercel CLI on this machine is authenticated as dad's PERSONAL account (`forest-9003`), account-wide
  — it can see/delete ALL 25 of his projects, not just webblaze. No confirmation prompts.
- ALWAYS `cd ~/webblaze` before any vercel command. Only ever operate on the `webblaze` project.
- NEVER run `vercel remove` / `vercel rm` / `vercel project rm` — against ANYTHING, ever.
- NEVER run `vercel ls` / `vercel projects ls` and act on the output — other projects aren't ours.
- NEVER touch env vars/domains/settings on any project except webblaze.
- If a vercel command errors in a way that tempts a broader/forceful fix — STOP, ask Zayden/dad.
- Logos are placeholder-approved by dad's brief: `01_flame_wordmark.png` (header) + 
  `02_W_monogram_flame.png` (favicon) — dad hasn't picked a winner yet, flag as placeholder in any
  build. Palette: flame red #D32F2F → orange #F4511E → ember #FF7A18, slate wordmark #3E4A54.

## READ THESE FILES IN ORDER
1. `~/.claude/projects/-Users-zaydenzukerman-north-star-game/memory/bookedsolid_business_model.md`
   — full business model, all decisions, rebrand history, current state. THE master doc.
2. `ops/SETUP.md` — Zayden's setup checklist (domain, FreshBooks, address, FB account)
3. `outreach/cold-email.md` + `ops/FACEBOOK-OUTREACH.md` — the outreach scripts/playbooks
4. `outreach/leads-nowebsite.md` — verified/dead lead statuses (mostly burned; only Dune Buggy usable)
5. `ops/CLIENT-RESULTS-PLAYBOOK.md`, `ops/SEO-MARKETING-MASTER.md` — fulfillment + marketing research
6. `ops/REPO-LEVERAGE.md` — the /ads audit skill + camoufox we adopted from the IG post
7. `clients/dunebuggy/` — the finished 5-page spec site (live at zaydenzukerman-lang.github.io/webblaze/dunebuggy/)

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

## CAPABILITY UNLOCKED 2026-07-15: Claude can READ Facebook business pages directly
Via the Playwright MCP (Claude's OWN browser, NOT Zayden's account, NO login needed): navigate to a
business's FB page and read innerText through the login-popup overlay. Yields tagline, category,
location, email, review count, recent posts — and the Intro's Website field (or absence of it =
confirms "no website"). Can also extract fbcdn image URLs (incl. full-res, e.g. 2048x1536) and curl
them down for building the client's site. This replaces (a) manual photo-saving and (b) most of the
"can't see their page" bottleneck. It does NOT need Zayden to control his laptop or hand over FB
login — and carries no account risk (reading public pages in Claude's own browser).
- How: mcp__playwright__browser_navigate → browser_evaluate (innerText + img srcs) → curl images.
- Limit: deep Photos-tab scrolling can hit harder login walls; the main page usually gives enough.
- Sending is STILL manual (Zayden pastes/sends) — automating sends risks the account; reading doesn't.

## VERIFICATION RULE (learned hard — cheap agents fabricated "no website" ~60% of the time)
Every lead: Claude probes domain patterns + NOW reads the FB page directly (Intro→Website field) via
Playwright, THEN Zayden does final 10-sec check on the business's FB page before sending. Zayden is
still the last gate, but Claude's direct read makes fabrication impossible (Claude sees the real page).

## IN-FLIGHT LEADS — VERIFIED 2026-07-12, batch mostly BURNED
8 of 9 had websites (charters/party rentals need booking sites — wrong niche for zero-website
targeting). Full statuses in outreach/leads-nowebsite.md.
- **Only survivor: Orange Beach Fish Charter Services** (fb/orangebeachfishcharterservices,
  since 1980) — Zayden's FB check 7/15 found their FB links to orangebeachfish.com which is
  DEAD (503). Reclassified as a BROKEN-SITE lead (hotter: losing bookings in peak season).
  **Spec site BUILT 7/15**: clients/orangebeachfish/ → live at
  zaydenzukerman-lang.github.io/webblaze/orangebeachfish/. Opener angle: "your website link is broken."
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
2. Add DNS records for webblaze.io in Namecheap (exact records in ops/SETUP.md) — domain is bought,
   just not pointed at the site yet. Claude re-enables the custom domain the moment DNS resolves.
3. FreshBooks account (dad) — needed before first "yes"
4. Optional: install NotFair plugin (/plugin marketplace add nowork-studio/notfair ; /plugin install notfair@nowork-studio)

## TOOLS NOW AVAILABLE TO CLAUDE
- `/ads audit` skill installed (~/.claude/skills/ads) — paid-ads audit, basis for a "Webblaze Ad
  Audit" product ($150-300) for businesses already running ads.
- camoufox browser (~/.camoufox-venv) — anti-detect, for verification; Yelp still 403s headless.
- Repo: github.com/zaydenzukerman-lang/webblaze. Pages from /docs. Custom domain webblaze.io pending DNS.
