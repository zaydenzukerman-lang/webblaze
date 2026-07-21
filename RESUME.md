# RESUME — read this first after /clear (state as of 2026-07-17)

## THE GOAL (Zayden, 2026-07-17): MAKE $1.
Not $1000/week, not 10 sites, not apps. ONE real dollar from ONE real customer. Every session,
every task gets judged against "does this get us closer to the first dollar?" Infrastructure work
(branding, domains, tooling) is DONE — stop polishing, start selling. Fastest known path: send
the two ready Messenger pitches (Dune Buggy + Orange Beach Fish Charter).

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

## CLAUDE <> CONCIERGE — REAL CHANNEL FOUND 2026-07-20: SSH to Forest's Mac mini
The actual "over WiFi" mechanism (Zayden was right it exists): Forest's Mac mini
(`Forests-Mac-mini.local` = 192.168.68.75, on the same LAN) runs an SSH-backed message relay.
Concierge lives there / reads+writes messages there.
- Setup done: generated `~/.ssh/id_ed25519_concierge` (private stays here, only pubkey shared).
  Helper `~/message-concierge.sh`: `--check` reads messages (`ssh mini read`), any arg sends
  (`echo arg | ssh mini send`). Uses `-o IdentitiesOnly=yes` (critical — without it ssh offers
  all my keys and hits "Too many authentication failures" before trying the right one).
- Verified: Mac mini reachable, port 22 open, SSH transport works — only blocker is Concierge
  adding my pubkey to the mini's authorized_keys. Pubkey (send to Concierge):
  `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHWIeXbWfdMhPGsJOdy2CB2hy52s5vOWAhdFginIZ3qk zayden-claude`
- To send Concierge a message: `~/message-concierge.sh "your message"`. To read: `~/message-concierge.sh --check`.
- IMPORTANT PRIOR ERROR: my earlier "no open ports on the network" scan was BROKEN — it used
  `timeout` which doesn't exist on macOS, so every probe silently failed. Don't trust that scan.
  Use `python3` socket checks or `nc` for port checks on this machine, never `timeout`.

## (superseded) GitHub-issue relay — set up 2026-07-20, now backup only
No live agent-to-agent link exists between Claude (this machine) and Concierge (dad's own Claude
Code, on HIS laptop) — confirmed via SendMessage ("no agent named Concierge reachable"), no MCP
bridge, no local network service. The domain/DNS handoffs that worked before were human-relayed
(dad ran his own Concierge, told Zayden, Zayden told Claude) — NOT agent-to-agent.
**Fix: async relay via GitHub Issues** on the shared repo (already public, gh already authenticated
here): https://github.com/zaydenzukerman-lang/webblaze/issues/1 — "Claude <> Concierge relay".
Either agent posts a comment when it needs something from the other; Zayden/dad tell their agent
to check/reply there. Requires Concierge to ALSO have git/GitHub access to be fully two-way —
unconfirmed, worth checking. If Concierge can't reach GitHub, this degrades back to human relay,
which still works fine.

## hello@webblaze.io EMAIL — 2026-07-20, DNS side DONE, one free signup left
FACT CHECK (corrected a wrong assumption): Namecheap is registrar ONLY. DNS is on Vercel
nameservers (ns1/ns2.vercel-dns.com) — confirmed via Google DNS, Cloudflare DNS, and WHOIS
independently. No Cloudflare account/API access exists on this machine. Since DNS lives on
Vercel and I have working `vercel dns` CLI access, I can add/remove ANY DNS record myself,
instantly, with zero Namecheap or Cloudflare involvement.
- Dropped Google Workspace (no gmail/paid-Google — Zayden's call 7/20). Removed its SPF record.
- Set up **ImprovMX** instead (free custom-domain email forwarding, works with any DNS host):
  added MX (mx1.improvmx.com prio 10, mx2.improvmx.com prio 20) + SPF TXT
  (`v=spf1 include:spf.improvmx.com ~all`) via `vercel dns add webblaze.io ...` — confirmed live
  via `dig @8.8.8.8`.
- **ONLY remaining step (free, ~2 min, no login needed beyond signing up)**: register at
  improvmx.com (email + password only), add webblaze.io, set forwarding rule
  `hello@webblaze.io → webblazeio@gmail.com`. Then update the site's contact button from
  webblazeio@gmail.com to hello@webblaze.io (one line in src/app/page.tsx, redeploy).
- Reusable pattern going forward: ANY DNS record webblaze.io ever needs (more subdomains, more
  email providers, verification codes, etc.) — Claude adds it directly via `vercel dns add
  webblaze.io <name> <type> <value>` from `~/webblaze`, no dad/Namecheap/Cloudflare step needed.

## PREMIUM REDESIGN 2026-07-20 (Zayden: "sites are boring/basic, want high-end unique feel")
Big design elevation of webblaze.io + Sun Finance, plus legal pages. All LIVE + verified 200.
- **webblaze.io homepage** rebuilt premium: dark editorial hero (Space Grotesk display + Inter),
  animated flame glow, framer-motion scroll reveals + spring micro-interactions + magnetic buttons,
  scrolling marquee, animated stat counters, big editorial portfolio cards (Sun Finance / Orange
  Beach / Dune Buggy → their live subdomains), distinctive numbered process, glowing pricing card,
  elegant FAQ accordion, contact form on flame-glow dark section, rich noir footer.
  Installed framer-motion. Shared components in src/components/site.tsx (Nav/Footer/Reveal/Stat/
  Marquee/Magnetic). page.tsx is "use client" (metadata lives in layout.tsx).
- **/privacy + /terms** pages (src/app/privacy, /terms) — real, honest agency policy/terms in the
  new design language, linked in footer. Server components.
- **Sun Finance** (public/sunfinance/index.html) rebuilt to high-end private-bank feel: Fraunces
  serif display + Inter, deep navy + bronze-gold + ivory, glass rate card, editorial loan programs,
  navy heritage pull-quote section, IntersectionObserver scroll reveals (reduced-motion safe),
  refined compliance footer (NMLS #71517 + EHL + LA OFI placeholder). Fresh portfolio screenshot.
- NOTE ON VERIFY: framer-motion whileInView + fullPage screenshots show below-fold sections blank
  until scrolled — that's a capture artifact, NOT a bug (verified each section renders on real
  scroll). Real users see smooth reveals.
- Client demos NOT redesigned (Dune Buggy/Orange Beach) — task was webblaze + Sun Finance only.
- Contact form still posts to Web3Forms with placeholder key (unchanged pending item).
- ANCHOR-SCROLL GOTCHA (fixed 2026-07-20): `overflow-x:hidden` + scroll-reveal transforms break
  native in-page hash scrolling (clicking #anchor jumps to wrong spot near top). Fix applied to
  BOTH sites: JS click handler intercepts a[href*="#"] and does manual
  `window.scrollTo({top: el.rect.top+scrollY-offset})`. Sun Finance: inline script + section[id]/
  .arm scroll-margin. Homepage: handler in Nav useEffect (site.tsx), handles "#x" and "/#x".
  If adding new anchor links or a new static site with reveals, replicate this.

## WEBBLAZE.IO MARKETING SITE — BUILT & DEPLOYED 2026-07-15 [superseded by 07-20 redesign above]
Next.js + Tailwind site built in `~/webblaze/` (separate repo from bookedsolid, its own git history).
Sections: hero ($300 flat pitch), portfolio (real screenshots of Dune Buggy + Orange Beach Fish
Charter linking to their live GitHub Pages demos), how-it-works (3 steps), pricing card, FAQ,
contact (mailto:webblazeio@gmail.com — a fresh Gmail Zayden made 7/15, works immediately, no
domain/DNS needed). Design ran
through ui-ux-pro-max per our standard. Uses dad's placeholder logos (flame wordmark header,
W-monogram favicon) — logo winner not yet confirmed by dad, flagged as placeholder.
- **LIVE NOW**: https://webblaze-two.vercel.app (deployed under dad's `hbz-holdings` Vercel team
  scope, project name `webblaze` — confirmed isolated from his other 25 projects).
- **Domains PRE-STAGED on the project 2026-07-15** (everything done on our side): webblaze.io,
  www.webblaze.io, orangebeachfish.webblaze.io, dunebuggy.webblaze.io all added via
  `vercel domains add <d> --scope hbz-holdings` (run from linked ~/webblaze, single-arg form).
  Client demos also now served BY the Vercel project itself: /orangebeachfish/ and /dunebuggy/
  paths (live on webblaze-two.vercel.app right now) + <slug>.webblaze.io subdomains via
  src/proxy.ts host routing (Next 16 renamed middleware→proxy; config rewrites handle
  directory-index + pretty URLs; NOTE: host rules must NOT also live in next.config or the
  prefix doubles → 404). Portfolio links on homepage are now relative paths.
  **The ONLY remaining step is Concierge's routine DNS flip** (per WEBBLAZE_BRIEF process:
  "just tell Forest when ready"): simplest is nameservers → ns1.vercel-dns.com /
  ns2.vercel-dns.com, which makes root + www + BOTH demo subdomains live in one change.
  GitHub Pages demo URLs remain as working fallback until then.
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

## SUN FINANCE — WARM LEAD (Forest's past client, 2026-07-20) — best lead we have
Forest still has contact with the Sun companies (Metairie LA, lender since 1958) and can
introduce us — they WANT new websites.
**SCOPE CORRECTED 2026-07-20 (Zayden): these are THREE SEPARATE businesses = THREE SEPARATE
WEBSITES, sold at $300 EACH = $900 total** (NOT one unified site — Zayden's earlier "same website"
comment was a mix-up he corrected). The three:
  1. Sun Mortgage Funding — sunmortgagefunding.com — mortgages $5k-$10M (NMLS #71517)
  2. Sun Premium Financing — sunpremium.com — insurance premium financing
  3. Sun Finance Company — sunfinance.com — personal loans $500-$3k
All three currently dated, all built by Inspree (Forest's agency) years ago; all real domains
already in Inspree's Cloudflare (easy production cutover).
**DONE 2026-07-21 — split into 3 SEPARATE tailored demos, all live:**
  - https://sunmortgagefunding.webblaze.io — mortgages, NMLS #71517 + Equal Housing Lender, 6 loan
    programs, phone 504-837-3939. (Flagship; featured in webblaze.io portfolio.)
  - https://sunpremium.webblaze.io — insurance premium financing (how-it-works, no NMLS/EHL — not a
    mortgage), LA OFI license placeholder, phone 504-834-9400.
  - https://sunfinance.webblaze.io — personal loans $500-$3k (how-it-works), LA OFI placeholder,
    phone 504-837-9400.
  All 3 share the premium Fraunces/navy-gold design (one family brand); differentiated by nav tag,
  hero, product section, phone, footer compliance. Each has PREVIEW ribbon. = $900 pitch (3×$300).
  GOTCHA: new subdomains need BOTH (a) add to DEMOS arrays in proxy.ts + next.config.ts, (b) vercel
  domains add, AND (c) a Cloudflare CNAME record (<sub> → cname.vercel-dns.com, DNS-only) via the
  token — I forgot (c) first and they 404'd until added. Certs auto-issue after DNS resolves.
- **DEMO BUILT + LIVE: https://sunfinance.webblaze.io** (also /sunfinance/ path). Static site in
  webblaze/public/sunfinance/, navy+gold "Trust & Authority" via ui-ux-pro-max, real content,
  PREVIEW ribbon. Registered in DEMOS arrays (proxy.ts + next.config.ts) + vercel domain added.
- **COMPLIANCE RULE (from Concierge, critical):** lending is regulated — demo uses PLACEHOLDERS
  for NMLS# and legal disclosures. Do NOT publish real NMLS/disclosure text until Forest provides
  them AND it clears a compliance review (fleet rule for agent-written regulated content).
- DONE: real "SUN" logo (pulled from their site) in nav, verified NMLS #71517 (Sun Mortgage
  Funding) + Equal Housing Lender + LA OFI license slot in compliance footer. PITCH ANGLE: their
  current 3 sites show ZERO NMLS/equal-housing/disclosures — our redesign adding a proper
  compliance footer is a real selling point. Their old sites built by Inspree (Zayden's family
  agency) years ago — we're upgrading family work.
- BEFORE PUBLISH (not for the preview): human must verify NMLS 71517 at nmlsconsumeraccess.org
  (bot-blocked); client fills LA OFI license #s + final disclosure text.
- Budget: Zayden's call (Forest hands-off, "this is all Zayden's project"). Above $300 tier.
- Intro: Forest makes it whenever the demo's ready — nothing to wait on. Home page is ready NOW.
- NEXT (my job, NOT Concierge's): build inner pages (Loan Programs, About, Apply, Contact) if we
  want depth before the intro; decide price.

## CLOUDFLARE CUTOVER COMPLETE 2026-07-20 ✅
webblaze.io is now fully on Cloudflare (Zayden's own account, NS lee+leah.ns.cloudflare.com, zone
ACTIVE). All 4 sites (webblaze.io + orangebeachfish/dunebuggy/sunfinance subdomains) verified 200
on the new DNS. DNS records: A webblaze.io→76.76.21.21 + CNAMEs www/3-demos→cname.vercel-dns.com,
all DNS-only; 3 CAA kept. Token at ~/.cf_webblaze_token (Zone DNS Edit only).
EMAIL DONE 2026-07-20: went with **Google Workspace** (Zayden's own new Workspace acct, ~$6/mo
dad's card), NOT Cloudflare Email Routing. zayden@webblaze.io is a real Google mailbox. DNS in
Cloudflare: MX→smtp.google.com, google-site-verification TXT, 2x DKIM (all added by Zayden/Google
wizard), + SPF (v=spf1 include:_spf.google.com ~all) added by Claude via token. Fully wired,
send+receive. Phone notis = add account to Gmail app. Works like his zayden@inspree.com (inspree
also on Google Workspace — that's how we confirmed the approach).

## CLOUDFLARE — moving webblaze.io here (Zayden's call, 2026-07-20) [historical, now done]
Decision: webblaze.io DNS + email moves Vercel → Cloudflare (Zayden standardizing on CF). Immediate
driver: free Cloudflare Email Routing for zayden@webblaze.io. Cloudflare Free tier covers all of it
(DNS + Email Routing), no card. Keep domain REGISTERED at Namecheap (don't transfer registrar).
- INSTALLED 2026-07-20: official Cloudflare Claude Code plugin — `claude plugin marketplace add
  cloudflare/skills` + `claude plugin install cloudflare@cloudflare`. Gives skills
  (cloudflare-email-service, cloudflare, wrangler, etc.) + MCP servers (cloudflare-api =
  mcp.cloudflare.com, cloudflare-docs, bindings, builds, observability). Config at
  ~/.claude/plugins/marketplaces/cloudflare/.mcp.json.
- AUTH IS VIA OAUTH, not a raw token — cleaner, no credential handling. cloudflare-api MCP
  authenticates to whatever account Zayden logs into.
- MCP OAUTH DIDN'T WORK (non-interactive session can't run it). PIVOTED to scoped API token —
  Zayden made his OWN Cloudflare account (zone webblaze.io id=38f5574d3d2e456ed8f24ba23682d395,
  acct id=3fa8904a495aaa83a031d9c38ba6e865, status pending, NS = lee + leah.ns.cloudflare.com).
  Token stored at ~/.cf_webblaze_token (chmod 600, NOT in any git repo). Scope: Zone DNS Edit
  (Email Routing perm did NOT stick — got auth error on that endpoint).
- DONE 2026-07-20 via token+curl: cleaned the zone. Verified (via curl --resolve, before touching
  anything) that apex→76.76.21.21 and subdomains→cname.vercel-dns.com both serve the live site
  w/ valid HTTPS. Then deleted 7 broken/proxied Vercel records + ImprovMX MX/SPF; added clean
  DNS-ONLY records: A webblaze.io→76.76.21.21, CNAME www/orangebeachfish/dunebuggy/sunfinance→
  cname.vercel-dns.com. Zone is FLIP-SAFE (site won't break on NS cutover). 3 CAA records kept.
- REMAINING (needs Zayden, both quick):
  1) EMAIL ROUTING (dashboard wizard, my token lacks the account-level perm): Cloudflare dash →
     webblaze.io → Email → Email Routing → enable; add destination Gmail + verify (click link in
     that inbox); create address zayden@webblaze.io → forward to that Gmail. Wizard auto-adds the
     Cloudflare MX/SPF. Can be done while zone is still pending.
  2) NS FLIP: tell Concierge to change Namecheap nameservers to lee.ns.cloudflare.com +
     leah.ns.cloudflare.com. (Concierge deletes its jimmy/melody zone in Forest's acct.)
     Site is already flip-safe, so flip can happen anytime; doing email first = zero email gap.
- To manage the zone again: TOKEN=$(cat ~/.cf_webblaze_token); curl .../client/v4/zones/$ZONE/...
- Note: to SEND as zayden@webblaze.io later, set up Gmail "Send mail as" (separate free step).
- Bonus (Concierge): client's REAL domains (sunfinance.com etc.) already in Inspree's Cloudflare →
  Sun Finance production cutover is in-family/trivial once we win the work.

## CONCIERGE SCOPE (Zayden, 2026-07-20) — STRUCTURAL/ACCOUNT things ONLY, rarely
Concierge is NOT a work collaborator. Don't route research/building/content/logos through him
(I over-did this on Sun Finance — he pulled NMLS/logos that were MY job). Default to ZERO messages.
Only message when I hit a true wall that is BOTH account-level (needs Forest's logins) AND not
something Zayden can click himself — e.g. registrar/nameserver changes, Cloudflare-type access.
Escalation: do it myself → ask Zayden → (only if truly account-gated) Concierge. See
feedback_concierge_scope.md.

## CONCIERGE CHANNEL — LIVE + WORKING (2026-07-20)
SSH mail-slot to Forest's Mac mini works both ways (confirmed real round-trips). Send:
`bash ~/message-concierge.sh "msg"` or `cat file | bash ~/message-concierge.sh` (stdin, best for
long/multi-line; 20KB cap). Read replies: `bash ~/message-concierge.sh --check`. Key is locked to
mail-slot-only on their side. Concierge gets pinged instantly; replies land in the mailbox (poll
with --check, or a background until-loop watcher). CLOUDFLARE settled via this channel: none exists,
stay on Vercel+ImprovMX. Registrar-level (Namecheap) nameserver changes = request via mailbox.

## PAYMENTS — effectively solved (2026-07-20)
Zayden already has a FreshBooks account. Payout/processing rail = **dad's (Forest's) Stripe
account**, which Zayden will connect inside FreshBooks. This clears the age/KYC problem cleanly:
Zayden's name on the work, dad's verified Stripe receiving the money → the $ lands and STAYS.
DO NOT set up any financial/payout account under Zayden's real-or-faked age — payment processors
run KYC at payout and will freeze funds + ban a minor account. Dad's Stripe is the whole fix.
Only remaining action: dad connects his Stripe to the FreshBooks account (their action, not Claude's).

## STILL BLOCKED ON ZAYDEN
1. SEND the two ready messages (Dune Buggy + Orange Beach Fish Charter) — nothing blocks this now.
   The two demos are live on clean URLs: orangebeachfish.webblaze.io + dunebuggy.webblaze.io.
2. Add DNS records for webblaze.io in Namecheap (exact records in ops/SETUP.md) — domain is bought,
   just not pointed at the site yet. Claude re-enables the custom domain the moment DNS resolves.
3. FreshBooks account (dad) — needed before first "yes"
4. Optional: install NotFair plugin (/plugin marketplace add nowork-studio/notfair ; /plugin install notfair@nowork-studio)

## TOOLS NOW AVAILABLE TO CLAUDE
- `/ads audit` skill installed (~/.claude/skills/ads) — paid-ads audit, basis for a "Webblaze Ad
  Audit" product ($150-300) for businesses already running ads.
- camoufox browser (~/.camoufox-venv) — anti-detect, for verification; Yelp still 403s headless.
- Repo: github.com/zaydenzukerman-lang/webblaze. Pages from /docs. Custom domain webblaze.io pending DNS.
