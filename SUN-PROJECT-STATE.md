# WebBlaze — Sun Sites Project State (handoff)

Last updated: 2026-07-22. Read this first when resuming.

## ⏳ PENDING / NEXT UP
1. **INTERRUPTED REQUEST (do this first):** "Use the logo colors more everywhere on the whole site."
   The sun logo trio is **#FFC114 (yellow) → #FF822A (orange) → #DC632C (terracotta)**. Each site owns ONE
   as its brand accent (Mortgage=yellow, Premium=terracotta, Finance=orange) — but the user wants the colors
   used MORE throughout (accents, dividers, icons, hovers, section touches), while keeping navy/ivory as base.
   Don't go garish; tasteful but more present. Apply across all pages of all 3 sites.
2. **Propagate flagship improvements to Premium & Finance** (currently only done on Mortgage):
   - Rename their **Contact page → Apply** (file `contact.html`→`apply.html`, nav+footer label, links, sitemap).
   - Apply the **form-emphasis treatment**: navy `.contact` section, elevated white `.cform` card w/ gold top
     bar + big shadow + spotlight glow, "Start your application" heading, full-width brand Apply button,
     reassurance line, `.locphoto` image beside the form.
   - Add the **photo-trio band** + **grain texture** on plain sections (already in their styles.css).

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
  Bump `?v=N` in the HTML whenever CSS changes (Mortgage is currently at **v=9**). Verify with curl, not just deploy.

## THE 3 SITES (live)
- https://sunmortgagefunding.webblaze.io  — brand color **yellow #FFC114**. Pages: index, programs, about, **apply.html**.
- https://sunpremium.webblaze.io           — brand color **terracotta #DC632C**. Pages: index, how-it-works, about, contact.html.
- https://sunfinance.webblaze.io           — brand color **orange #FF822A**. Pages: index, how-it-works, about, contact.html.
- Real 3-dot Sun favicon + logo in each `img/`. Footer "The Sun Companies" cross-links the OTHER two sites only.
- Per-site brand color is set via a `:root{--gold;--gold-2;--sun-y;--sun-o;--sun-r;...}` override appended at the
  END of each site's `styles.css` (that's why the 3 stylesheets differ). Buttons/blooms auto-tint from these vars.

## DESIGN STATE (current, approved direction)
- Base = **photo-hero template**: full-bleed real photo hero + scrim, minimal conversion-first hero (dominant
  Apply Now), then sections (why / imgsplit / offer / localband / how-it-works / heritage / reviews / faq / cta).
- Richer backgrounds: `.sec-glow` (warm gradient + brand sun-blooms), `.sec-tint` (gradient + dot texture),
  `.sec-lines` (gradient + diagonal lines), `.grain` (SVG noise overlay), `.photo-trio` (3-image strip).
- Imagery = **REAL, CC0/public-domain New Orleans photos** (Openverse + Wikimedia), 6 unique per site:
  `hero, accent, city, prod, about, loc` .jpg (all `?v=2`). NO AI images, NO stock needing attribution.
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
`[to confirm]` on Premium/Finance compliance); real office hours; real staff headshots (currently initial-avatars).

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
