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
- Deploy staging: `cd ~/webblaze && npm run build && git add -A && git commit -m "…" && vercel --prod --yes --scope hbz-holdings`. (Vercel scope `hbz-holdings`, team `team_wy9hEdFNi11gAe8NqbwTQiRx`, webblaze project id `prj_IKQlruOVyixsZq2rs6se1pdB6QPc`.) Propagation lag ~10–30s; recheck with `?cb=$RANDOM`.
- Vercel API token: `~/Library/Application Support/com.vercel.cli/auth.json` → field `token`.
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
- **DO NEXT:** (1) Actually open `wemploymentlaw.com`, screenshot it, and study its real design — fonts, colors, imagery, layout — then rebuild to **match/parody that** and improve it (not a generic bold template). (2) Use plenty of **real images**. (3) **Kill empty space + glitches** — tight, full sections. (4) Keep it distinct from Sun.
- At go-live the client needs to provide: a real headshot of Jacob (currently a "JW" monogram — do NOT fake it), full testimonials, and an intake email so the Free Case Review form actually delivers (currently a demo form).
