# WEBBLAZE — working handoff (read this first)

You are the build partner for **WebBlaze**, Zayden's ($300/site) web-design agency.
This doc replaces cleared chat context. **Current job = the W Employment Law redesign** (§4).
Sun work is done/saved in `SUN-STATE.md` (reference only — don't re-touch unless asked).

## 1. USAGE DISCIPLINE (Zayden flagged this — take seriously)
- Be economical with tokens/tool calls. Batch edits into one script. **Deploy once**, not after every tweak.
- Verify with `curl` where possible; take **one** screenshot to judge a design, not many. Don't re-verify things that already passed.
- Don't crawl/loop unnecessarily. No giant multi-file dumps.

## 2. Infra & credentials
- Repo `~/webblaze` (Next.js). Client sites live in `public/<slug>/` (static HTML). A new slug must be added to the `DEMOS` array in **both** `src/proxy.ts` and `next.config.ts`.
- **DEPLOY (current — GitHub Pages, no token/login needed):** the apex `webblaze.io` homepage is a **static export hosted on GitHub Pages**, served from repo `zaydenzukerman-lang/webblaze`, branch `main`, folder `/docs`. Deploy =
  ```
  cd ~/webblaze && npm run build && rm -rf docs && cp -R out docs \
    && touch docs/.nojekyll && printf 'webblaze.io' > docs/CNAME \
    && git add -A && git commit -m "…" && git push origin main
  ```
  GitHub Pages rebuilds in ~1 min. `public/CNAME`=`webblaze.io` + `public/.nojekyll` are committed so they always land in the build. `next.config.ts` has `output:"export"`, `images.unoptimized:true`. GH CLI is already authed (`gh auth status`). No Vercel, no login — the "token that died" was Vercel's; we left it.
- **DNS (Cloudflare, token `~/.cf_webblaze_token`, zone `38f5574d3d2e456ed8f24ba23682d395`):** apex `webblaze.io` = 4 A records → `185.199.108–111.153` (GitHub Pages), `www` CNAME → `zaydenzukerman-lang.github.io`, DNS-only. **Revert to Vercel** = apex A → `76.76.21.21`, www CNAME → `cname.vercel-dns.com`.
- **⚠️ Still on the OLD Vercel deployment (frozen, last deploy still live):** the `<slug>.webblaze.io` demo subdomains AND the live client `.com` sites (`sunfinance.com`, `sunpremium.com`, `sunmortgagefunding.com`) run off `src/proxy.ts` middleware on Vercel — Pages can't run middleware, so those stayed on Vercel and are UNTOUCHED. Path-based demo access (`webblaze.io/<slug>/`) works on Pages via native directory-index. To *update* a client demo or add a subdomain again we'd need a fresh Vercel token from dad (project `prj_IKQlruOVyixsZq2rs6se1pdB6QPc`, scope `hbz-holdings`) — or migrate those to their own Pages repos.
- Vercel API token (DEAD — API returns `invalidToken`): was `~/Library/Application Support/com.vercel.cli/auth.json` → field `token`. Not used anymore.
- **New subdomain** `<slug>.webblaze.io`: (a) Cloudflare CNAME `<slug>` → `cname.vercel-dns.com` DNS-only, zone `38f5574d3d2e456ed8f24ba23682d395`, token `~/.cf_webblaze_token`; (b) attach domain via Vercel API `POST /v10/projects/<projId>/domains`.
- **Images: Pexels API** key `85gzYeGliCl062HE8cT3bQZRphoW2iaH9pI2oxmLxJ7zE1KTttQe8eXL` — send `Authorization: <key>` header + a normal browser User-Agent, use `src.large2x`, `orientation=landscape|portrait`. Free/commercial/no-attribution.
- Concierge = dad's Claude Code. Reach via `~/message-concierge.sh "msg"` (SSH to Forest's Mac mini — only works when this machine is on his home Wi-Fi, subnet 192.168.68.x) or GitHub issue `github.com/zaydenzukerman-lang/webblaze/issues/1`.
- Dad (Forest) owns Vercel/DNS/money. Zayden is 13.

## 3. DESIGN RULES / FUNDAMENTALS (honor these — I've been failing them)
1. **Study the client's OWN current site FIRST** — screenshot it, note its fonts, colors, imagery, layout, sections, vibe. **Match/parody its style closely**, then elevate. Don't impose a generic template.
2. **Every client site must be UNIQUE.** Never let two clients look alike (W Employment looked too much like Sun = a fail).
3. **Real images are mandatory** — full-bleed photography, image splits, textured sections. Color blocks alone read as "boring/dull." Pull the client's real photos if possible; else Pexels.
4. **No large empty spaces. No visual glitches.** Tight, intentional layout. Test at desktop + mobile.
5. **Real facts only** — never fabricate names, reviews, credentials, stats. Use the client's real content.
6. **Conversion-first** — the primary CTA (call / free review / apply) dominates. Mobile hamburger + sticky call/CTA bar.
7. Law firms: include an **attorney-advertising / not-legal-advice disclaimer**; **never put a stock face on a named attorney**.
8. Make reveal/animations **progressive-enhancement** (content visible without JS — gate `opacity:0` behind an `html.js` class, add `.in` on scroll, fallback reveals all if no IntersectionObserver).

## 4. CURRENT TASK — W Employment Law redesign
- Client: **W Employment Law** (`wemploymentlaw.com`) — California **employee-side** employment law firm. "Fighting for California Employees." Contingency / **No Win No Fee**.
- Founder: **Jacob N. Whitehead** (Founding Partner). Office: **7700 Irvine Center Drive, Suite 800, Irvine, CA 92618**. Phone **888-492-0633**.
- Practice areas (11): Wrongful Termination, Discrimination, Sexual Harassment, Unpaid Wages & Overtime, Meal & Rest Breaks, Pregnancy Discrimination, Medical Leave & Disability, Whistleblower Retaliation, Independent-Contractor Misclassification, Employee Class Actions, Work-Related Reimbursements.
- Real testimonials on their site (excerpts only were visible): Alberto, Nava, Shauna, Larry. Value props they use: Free Legal Advice, No Win No Fee, Power & Resources, Vast Experience, Proven Results, Confidential Advice.
- Built at `public/wemploymentlaw/index.html` → live `wemploymentlaw.webblaze.io` (subdomain already set up; slug already in DEMOS). Images downloaded in `public/wemploymentlaw/img/` (hero, workers, consult, city, atty .jpg).
- **REJECTED so far (v1 + v2). Zayden's feedback:** "doesn't parody good enough — look at the OLD site's style (images, fonts, etc.)"; "visuals still boring"; "a bunch of visual glitches"; "70% is random empty spaces."
- **v3 SHIPPED (live now — awaiting Zayden review).** Rebuilt to parody the REAL site's DNA: **teal `#0e8291` + gold `#f4b400`**, **Karla + Roboto Slab** fonts, photo-left / gold **Free Case Review form-card** hero, **3×3 practice-area PHOTO grid** (9 real Pexels photos in `img/pa-*.jpg`), dark **"Why Hire" band w/ 6 gold circle icons**, testimonials (real Alberto/Nava/Shauna/Larry excerpts + gold stars), JW-monogram attorney (no fake face), CA-coast CTA, FAQ accordion, teal social band, navy footer. Now visually distinct from Sun (Sun = blue+Archivo). **Root-cause glitch fixed:** reveal-on-scroll sections were stuck `opacity:0` because `html.js .reveal` (spec 0,2,1) out-specified `.reveal.in` (0,2,0) → changed to `html.js .reveal.in` + added a 1.6s safety-net that reveals all. This was likely a real contributor to the "empty space" complaints. Verified desktop+mobile screenshots, no empty gaps/overflow. Prod deploy `dpl_Dh5CEFxnX7kpdXUwR4USovHRP5sD`.
- **DO NEXT (if v3 still gets notes):** get SPECIFIC feedback before re-touching. Everything else (headshot, full testimonials, intake email) is client-provided at go-live — see below.
- At go-live the client needs to provide: a real headshot of Jacob (currently a "JW" monogram — do NOT fake it), full testimonials, and an intake email so the Free Case Review form actually delivers (currently a demo form).

## 5. WEEKLY ANALYTICS REPORTS (Sun — client Brian, every Monday)
- **Everything lives in `~/.ga-reports/` — read `~/.ga-reports/README.md` first.** It has the full pipeline: GA4 service-account key, the 3 property IDs, the puller script (`ga_report.py` + venv), the approved **report page** + **email** templates (`templates/`), and the PDF-generation command.
- Format is **client-approved** (Zayden said keep it): navy+gold Sun-branded PDF report + email body with per-site cards and an explicit **Direct / Organic Search / Referral** sources line. Reuse it, don't redesign.
- Data rules: exclude `webblaze.io` staging traffic; watch for bot/foreign traffic (Mortgage is mostly bots). Never fabricate numbers.
- Delivery: `open ~/Desktop/sun-report-email.html`, Zayden copies from the browser page into Gmail + attaches the PDF. First report (Aug 17–23) sent.
- Next upgrade pitched to client: GA4 key events (Apply/call/email/form) to report LEADS, not just visits.
- **US-only bot filter added 2026-08-31** (approved). Reporting uses `ga_full.py` (US-only + staging excluded). Bots were hiding real quality — Finance engagement 32%->69% once filtered.

## 6. NEW-CLIENT PROSPECTING (organic outreach, goal ~1 client/week)
- **Everything in `~/webblaze/prospecting/` — read `ICP.md` first.** Files: `ICP.md` (who to target + sourcing playbook), `scan.sh` (outdated-site scanner: `bash scan.sh domains.txt` → score+email, higher score=better target), `cold-email-templates.md` (A=free-preview [our edge], B=light, C=follow-up), `prospects.csv` (tracker — log every candidate + send).
- **Cadence: ~20 cold emails/day (~100/wk), 1% conversion target.** Bottleneck is SOURCING: scan.sh flags only ~10-20% as targets, so source ~150 domains/day (chamber/BBB/Yelp/Maps directories, NOT Google page-1) -> scan -> eyeball score>=3 -> email. Target small local service businesses with outdated INFORMATIONAL sites (law/CPA/contractor/trade B2B/charter/clinic). AVOID funeral homes (obituary systems) + e-comm/booking. Deliverability: send from hello@webblaze.io not raw Gmail; vary wording. First batch + drafts: prospecting/outreach-2026-08-31.md.
- **Key lesson (2026-08-31 first pass):** Google page-1 rankers usually already have decent sites; genuinely-outdated ones need smaller towns / low-web niches + directory mining, then scan.sh, then eyeball top scorers before emailing. First scan found no slam-dunk yet — sourcing needs to go deeper than top search results.
- Our edge: build a FREE live redesign preview on `<slug>.webblaze.io` and send the link (how Sun + WEL happened).

## 7. WEBBLAZE BRAND (our own look)
- **Read `BRAND.md`.** WebBlaze identity = warm ink #16130F + blaze-orange #F14E23, Sora + Hanken Grotesk. Used on OUR materials (outreach console, future webblaze.io). NEVER dress WebBlaze in a client's colors (Sun=navy/gold, WEL=teal). Client previews match the CLIENT; portfolio = show the client work.

## 8. GOOGLE MAPS / LOCAL SEO (new service direction, dad-backed 2026-08-31)
- **Read `LOCAL-SEO-PLAYBOOK.md`.** Verdict: Maps/local SEO is higher-value + RECURRING ($99-199/mo+) vs $300/yr sites. Best move = COMBINE: website = cheap foot-in-door, Maps growth = monthly upsell; on-page site work also boosts Maps rank (~19% of algo).
- Ranking levers: GBP claim/verify, primary+secondary categories, 100% complete profile, NAP consistency, REAL reviews (velocity+response), weekly posts, photos, citations.
- ⚠️ HARD ETHICS RULE: no fake/incentivized/gated/insider reviews (FTC fines ~$51k/violation). Ask ALL customers same public review link.
- Next: run it on first real client as a case study; build a monthly Maps report (reuse analytics report design).
