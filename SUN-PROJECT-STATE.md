# WebBlaze — Sun Sites Project State (handoff)

Last updated: 2026-07-22. Read this first when resuming.

## 0. YOUR ROLE, ZAYDEN, AND THE MISSION (the *why* — read to understand everything else)
**You are Zayden's web-design & build partner.** Zayden Zukerman is 13, a young entrepreneur building
**WebBlaze**, a web-design agency whose product is **$300/year websites + $100/month SEO** (separate packages).
Your job: design and *ship* genuinely high-end, conversion-focused client websites — behave like a real
professional studio, not a cheap Fiverr gig. Work **autonomously**: plan → build → deploy to production →
verify → iterate. Dad handles money/legal (Zayden is 13, can't hold Stripe/bank accounts himself).

**The goal / why this matters:** Zayden's north star is to **make his first real money** with WebBlaze. The
immediate path is the warm lead **"Sun"** (dad's past client) — 3 sister companies = 3 sites = **$900/year**,
plus optional **$100/mo SEO each** (recurring revenue is the real prize). Land Sun, then reuse the playbook for
more clients + monthly SEO retainers. Later: point the SEO engine at webblaze.io itself for inbound leads.

**How to work with Zayden (hard-won — honor these):**
- Be a partner who *actually gets it* — not a yes-man, not a "brick wall." Understand the real request; never
  ship surface-level work and call it done. He *will* tell you when it's amateur; believe him and fix the root.
- **Conversion is #1, design is #2.** Every page's job is to make the visitor act (Apply / contact). The form
  and the primary CTA must dominate. Design serves conversion.
- **Professional & trustworthy** — real photography, restraint, high-end (Compass/Sotheby's energy). NEVER
  gimmicky/abstract (the giant "sun-disc" concept was rejected — see design state).
- Honest and direct. Push back when an idea won't work. Admit weak work and re-do it — don't over-apologize.
- Keep replies brief. Ship + deploy every session. Verify before claiming done.
- Mind usage (see bottom): prefer `curl` over browser, avoid unneeded subagents/long sessions, /compact often.

**Where it stands overall:** All 3 Sun sites are BUILT and live as previews on `*.webblaze.io` subdomains —
fact-checked, image-rich; the Mortgage flagship is the most polished (esp. its Apply page). **Not yet pitched
to the client.** SEO baseline is in place; the SEO-retainer product is defined but not sold. (Zayden also has
other ventures — North Star game, Blue Spark, Crammify — but THIS project is WebBlaze/Sun; stay focused here.)

## ROADMAP (near-term → launch)
1. **Design polish (in progress):** use the 3 logo colors more everywhere; propagate the Mortgage flagship's
   Apply-rename + emphasized-form + photo/grain treatment to Premium & Finance so all 3 match.
2. **Content/compliance pass:** confirm w/ client — NMLS #71517 active status, LA OFI license #s (placeholders
   now), real office hours, and get real staff headshots (currently initial-avatars).
3. **Pitch Sun:** draft outreach for dad to send (3 sites @ $300/yr = $900/yr + SEO upsell). Give the preview links.
4. **On client "yes":** deploy to their real domains, flip previews from `noindex`→`index`, submit sitemaps to
   Google Search Console, set up GA4.
5. **Grow:** sell $100/mo SEO retainers (the recurring engine); point SEO at webblaze.io for inbound clients.

## ⏳ PENDING / NEXT UP
1. ~~**INTERRUPTED REQUEST:** "Use the logo colors more everywhere on the whole site."~~ **✅ DONE 2026-07-22.**
   Appended an identical **"BRAND COLOR ENRICHMENT v3"** block to the END of all 3 stylesheets (after the
   `:root` override, so it auto-tints per site from `--sun-y/o/r`/`--gold`). Adds the logo trio to the chrome
   while keeping navy/ivory base: nav bottom hairline + animated link underline, a short brand accent rule above
   every `.sec-title`, brand-tinted trust dividers, util/faq/chip hovers, inline-copy links, `::selection`, and a
   footer top edge. Applies to every page of every site (shared stylesheet). Verified live + screenshots (yellow
   on Mortgage, terracotta on Premium) — tasteful, not garish. **CSS versions bumped: Mortgage v9→v10,
   Premium/Finance v6→v7.** NOTE: to tweak the enrichment, edit that v3 block in each of the 3 styles.css (it is
   duplicated identically in all three); the generators do NOT emit it.
2. ~~**Propagate flagship improvements to Premium & Finance.**~~ **✅ DONE 2026-07-22.** Both sites now match
   the Mortgage flagship Apply page: Contact→Apply rename (`contact.html` deleted, new `apply.html`; nav+footer
   label "Apply", all links/util/CTAs → apply.html, sitemap regenerated), navy `.contact` form-emphasis section
   (elevated white `.cform` card + gold top bar + spotlight glow, "Start your application" heading + 2-min
   reassurance sub, full-width brand Apply button, `.form-fine` reassurance line, `.locphoto` city image beside
   the form), getting-started 3-step band (grain), FAQ band (grain), and a "Proudly Local" photo-trio band.
   **This was done via the generator** `scripts/gen_pp_rich.py` (Premium/Finance are the source of truth there):
   rewrote the CONTACT builder → APPLY, added `applyhead`/`applyband` config fields; then `rm contact.html`,
   sed CSS `?v=8`, re-ran `seo_inject.py`. Form-emphasis CSS block appended to Premium/Finance `styles.css`.
   **CSS versions now: Premium/Finance v=8** (Mortgage still v=10). Verified live + screenshot (terracotta Premium).
   Softened the Hours line to "Call us for current office hours." (real hours still need client confirmation).

## ✅ FIXED 2026-07-22 — pretty-URL asset bug
The bare pretty URLs (subdomain `/apply`, `/about`, `/how-it-works`, `/programs`, and dunebuggy `/menu` etc.)
used to 308-redirect to a trailing-slash form (`/apply/`), which broke the pages' **relative** asset paths
(`img/…`, `styles.css` resolved against `/apply/` → 404 → unstyled page). **Fix:** set `trailingSlash: false`
in `next.config.ts` (one line). Now subdomain `/apply` stays slash-less, relative `img/` → `/img/` and the proxy
(`src/proxy.ts`) prefixes the slug; a stray `/apply/` self-heals via Next's 308 back to `/apply`.
**Verified before deploy** with a local `Host:`-header matrix (`npm start` on :3999, curl with subdomain hosts):
subdomain index + all pretty pages + `/img/*` + `/styles.css` all 200 across the 3 Sun sites AND dunebuggy;
`/apply.html` still 200; 404s for missing pages; marketing site (`/`, `/privacy`, `/terms`) unaffected.
**Known trade-off (dev-only, acceptable):** path-based *apex* access `webblaze.io/<slug>` (bare index, no slash)
now 404s its relative assets. Path-based *pretty pages* (`/<slug>/apply`) and `/<slug>/index.html` still work,
and all real client links are subdomains (DNS live). Bottom line: **pretty `/apply` links are now safe to share.**

## BUSINESS CONTEXT
- WebBlaze = Zayden's agency. Model: **websites $300/YEAR**, **SEO $100/MONTH** (separate packages).
- Client "Sun" = dad's warm lead. THREE sister companies at 3525 N. Causeway Blvd Ste 900, Metairie LA 70002:
  Sun Mortgage Funding, Sun Premium Financing, Sun Finance Company. = 3 sites = **$900/yr** + optional SEO.
- Goal: land the first real dollar. Payments via dad's Stripe/FreshBooks (Zayden is 13, can't hold accounts).

## ARCHITECTURE
- Repo: `~/webblaze` (Next.js 16 + Tailwind), deployed to Vercel **scope `hbz-holdings`, project `webblaze`**.
- Static client demos live in `public/<slug>/` served via subdomain proxy (`src/proxy.ts`, host-based rewrite)
  + path rewrites (`next.config.ts`). `DEMOS` array in both: orangebeachfish, dunebuggy, sunfinance,
  sunmortgagefunding, sunpremium. Pretty URLs: `/apply` → `/apply.html` via proxy regex `/^\/[a-z-]+$/`.
- Cloudflare DNS (Zayden's own acct, token at `~/.cf_webblaze_token`): apex A→76.76.21.21, subdomains
  CNAME→cname.vercel-dns.com (DNS-only). Google Workspace email zayden@webblaze.io.
- **Deploy:** `cd ~/webblaze && npm run build && git add -A && git commit && vercel --prod --yes --scope hbz-holdings`
- **Cache-busting (critical — same filenames reused):** image URLs use `?v=2`; stylesheet `styles.css?v=N`.
  Bump `?v=N` in the HTML whenever CSS changes (currently **Mortgage v=10, Premium/Finance v=8**). Verify with curl, not just deploy.
  NOTE: `gen_pp_rich.py` writes `href="styles.css"` (no version) — after any regen, re-add `?v=N` via sed on the HTML.

## THE 3 SITES (live)
- https://sunmortgagefunding.webblaze.io  — brand color **yellow #FFC114**. Pages: index, programs, about, **apply.html**.
- https://sunpremium.webblaze.io           — brand color **terracotta #DC632C**. Pages: index, how-it-works, about, **apply.html**.
- https://sunfinance.webblaze.io           — brand color **orange #FF822A**. Pages: index, how-it-works, about, **apply.html**.
- Real 3-dot Sun favicon + logo in each `img/`. Footer "The Sun Companies" cross-links the OTHER two sites only.
- Per-site brand color is set via a `:root{--gold;--gold-2;--sun-y;--sun-o;--sun-r;...}` override appended at the
  END of each site's `styles.css` (that's why the 3 stylesheets differ). Buttons/blooms auto-tint from these vars.

## DESIGN STATE (current, approved direction)
- Base = **photo-hero template**: full-bleed real photo hero + scrim, minimal conversion-first hero (dominant
  Apply Now), then sections (why / imgsplit / offer / localband / how-it-works / heritage / reviews / faq / cta).
- Richer backgrounds: `.sec-glow` (warm gradient + brand sun-blooms), `.sec-tint` (gradient + dot texture),
  `.sec-lines` (gradient + diagonal lines), `.grain` (SVG noise overlay), `.photo-trio` (3-image strip).
- Imagery = **REAL photos, NO AI, NO attribution-required stock**. Original 6 per site (`hero, accent, city,
  prod, about, loc` .jpg, `?v=2`) = CC0 New Orleans (Openverse/Wikimedia). **Added 2026-07-22: 3 more per site**
  (`people.jpg, people2.jpg, street.jpg`, no `?v`) sourced from **Pexels** (Pexels license = free, commercial,
  no attribution needed) — warm, local, people-forward: homebuyers+realtor, small-business owners, friends/
  couples, French Quarter streets, a brass-band musician. Sourced via Pexels API (Zayden's key) with helper
  scripts in `/tmp` (pex.py/pool.py/dl.py — temp, not committed). **Placement:** home "Why us" split + local
  band now show people/street; home, apply & about pages each have a people+city `.photo-trio` band.
- **Top-right utility location link now → about.html** (was apply.html) per Zayden — About also got a photo band.
- ⚠️ **"Their actual building" is NOT shown** — we have no real photo of 3525 N. Causeway. Photos are honest
  area/lifestyle imagery (never captioned as "our office/staff/clients"). **Real office photo = client-provide TODO.**
- ⚠️ **REJECTED redesign:** a ground-up "Golden Hour / giant sun-disc art object" hero was tried and the user
  hated it ("gimmicky", "so much worse"). Reverted. **Do NOT do abstract giant shapes / art-student concepts.**

## WHAT THE USER WANTS (hard-won lessons — honor these)
1. **Conversion is #1, design #2.** The first screen = Apply Now as the single focal point; minimal text, no
   "story sentence" clutter. Forms must visually dominate (see Mortgage apply page: navy section + white
   elevated card + gold bar + spotlight + big gold button).
2. **Professional / trustworthy / "billion-dollar company" feel** — via real photography + restraint (think
   Compass/Sotheby's), NOT gimmicks.
3. **Not boring/flat beige** — sections need texture/warmth/imagery.
4. **Use the 3 logo colors** (see pending #1).
5. Real people/city photos (done — CC0 New Orleans).

## FLAGSHIP (Mortgage) — DONE
- All 4 pages live. **Apply page** (`apply.html`, renamed from contact): warm hero "Let's get you home.",
  location photo (streetcar) beside form, **form is the visual anchor** (navy section, white card, gold top
  bar, shadow, spotlight glow, "Start your application" heading, full-width gold "Apply now" button,
  reassurance line), grain on plain sections, "Proudly Local" photo-trio band, fixed FAQ heading.
- ⚠️ **GOTCHA:** Mortgage `index.html` and `apply.html` were HAND-EDITED after generation. The generator
  `scripts/gen_mort_rich.py` is now OUT OF SYNC — re-running it will OVERWRITE those hand-edits. Edit the HTML
  directly, or reconcile the generator first. (Premium/Finance are still in sync with `scripts/gen_pp_rich.py`.)

## VERIFIED FACTS (only use these — everything was fact-checked against official sites, BBB, NMLS)
- Since 1958 (on all 3 official sites). NMLS **#71517** (Mortgage). BBB **A+**: Mortgage accredited 1996,
  Finance accredited 1987. Premium has **no verifiable BBB** — do not claim BBB for Premium.
- Addresses: all 3525 N. Causeway Blvd (Ste 900 Mortgage/Premium), Metairie LA 70002.
- Phones: Mortgage (504) 837-3939 · Premium (504) 834-9400 · Finance (504) 837-9400.
- Amounts: Premium **$100–$250K**, **10+ insurance types** (their site). Finance **$500–$3,000** (their site).
  Mortgage: "more programs than a traditional bank" (NO specific $ range — their site gives none).
- Real team (from their team pages):
  - Mortgage: David Daube (President, 43yr/28 as Pres), Brian Daube (VP, 15yr), Annette Hesse (Loan Originator,
    NMLS #90346, 40yr), Tammie Cavanagh (Loan Originator, NMLS #164425, 40yr).
  - Premium: Aurora Surla (Manager, 44yr), Rebecca Perret (34yr).
  - Finance: David Daube, Brian Daube, Ashley Pabst (Mgr, 20yr), Kim Naquin (21yr), Liz Jones (Mgr, 31yr).

## ❌ FABRICATIONS REMOVED — never reintroduce
"Albert Daube" (wrong — real principal is **David Daube**); "family-owned / 2nd & 3rd generation" (sites say
"locally owned and operated"); Mortgage "$5K–$10M" & "15+ programs"; "Equal Housing Lender" badge; "65+ years"
(use "since 1958"); Premium BBB accreditation. "5.0★/9 reviews" only exists on a directory (Chamber of Commerce),
not Google/Yelp — keep soft ("5.0★ rated").

## STILL NEEDS CLIENT CONFIRMATION before real launch
NMLS #71517 "active" status (manual check at nmlsconsumeraccess.org); LA OFI license #s (placeholders
`[to confirm]` on Premium/Finance compliance); real office hours (currently softened to "Call us for current
office hours."); real staff headshots (currently initial-avatars); **real photo of the office/building** (to
show on About/Apply — currently using honest NOLA area photos instead).

## SEO (baseline done; playbook available)
- Baseline technical SEO on all 3 sites: canonical, OG/Twitter, LocalBusiness JSON-LD, sitemap.xml, robots.txt.
  Previews are **noindex** (flip to index on client's real domain). Sun's official sites use the SAME 4 NOLA
  slider photos with logo baked in (can't reuse cleanly).
- Dad relayed an SEO playbook (was a copy-paste, NOT a live agent named "Madison"): tools = Vercel + Google
  Search Console + GA4 + Distribb backlinks + Gmail outreach; daily 1500-word article workflow; tiers
  $500/$1k/$2k /mo. This is the recurring-revenue product on top of the $300/yr sites.

## BUILD SCRIPTS (in ~/webblaze/scripts/)
`gen_mort_rich.py` (Mortgage — OUT OF SYNC, see gotcha), `gen_pp_rich.py` (Premium+Finance), `seo_inject.py`
(adds SEO tags + sitemap/robots; idempotent; RE-RUN after any regeneration since it's wiped by regen).

## USAGE DISCIPLINE (important)
Usage got very high from subagent-heavy + long + Playwright-heavy sessions. Going forward: avoid subagents
unless necessary, verify with `curl` (not browser screenshots) where possible, limit Playwright, `/compact`
mid-task, `/clear` when switching tasks.
