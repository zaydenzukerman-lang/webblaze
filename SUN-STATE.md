# SUN — saved state (reference; work is essentially done)

Three sister companies, Metairie LA, 3525 N. Causeway Blvd Suite 900, since 1958.
Tagline (all): "New Day, New Challenges, New Solutions."

## Deployment topology (IMPORTANT — this caused hours of confusion)
- **LIVE .com sites = 3 SEPARATE Vercel projects** (team `hbz-holdings`), each hosts ONE site at its root (static, directory-style pages `/team/` → `team/index.html`):
  - `sun-sunfinance-site` → sunfinance.com
  - `sun-sunpremium-site` → sunpremium.com
  - `sun-sunmortgagefunding-site` → sunmortgagefunding.com
  - **To deploy a Sun change to a live .com:** `cp -R ~/webblaze/public/<slug> /tmp/x && cd /tmp/x && vercel link --yes --project sun-<slug>-site --scope hbz-holdings && vercel --prod --yes --scope hbz-holdings`
- **STAGING = the `webblaze` project** → `*.webblaze.io` subdomains. Deploying `~/webblaze` (`vercel --prod`) updates staging ONLY, NOT the live .com. (Dad's Concierge separated these so staging no longer overrides .com.)
- Live .com currently show the **OLD original WordPress design** (dad's choice). Our **redesign** is on staging + saved on git branch **`sun-redesign`** (tag `sun-redesign-snapshot`).

## Redesign build
- Generator `scripts/gen_pp_rich.py` builds Finance (config dict `PERSONAL`) + Premium (`PREMIUM`). Shared `build()` — guard per-site with `c.get(...)`. Mortgage is hand-edited HTML (`gen_mort_rich.py` OUT OF SYNC — edit HTML directly). After regen: `sed 's|styles.css|styles.css?v=10|'` + images `?v=4`; do NOT re-run seo_inject (it re-adds noindex).
- Flat pages: index/about/apply/how-it-works.html (Fin/Prem), index/about/apply/programs.html (Mort). Extra: Mortgage `/calculator` + `/blog` (5 photo cards); Premium `/payment` (Pay by Web + AW form PDF at `/aw-form.pdf`).
- Design = navy + gold, Fraunces/Inter serif, mobile hamburger, section cards.

## GA4 (per-site; each its own property)
Finance `G-6GYKFE11YF` · Premium `G-K5RG2PE7HL` · Mortgage `G-5K4DCC2N6F`. Generator injects via per-site `ga` config field.

## Real external links (verified working)
- Finance apply → `https://inspree.formstack.com/forms/personal_loan_application_online`
- Premium apply / Mortgage apply → `https://secure-apps.smartapp1003.com/200591/`  ⚠️ `secure.smartapp1003.com` (no hyphen) is DEAD — always use `secure-apps`.
- Premium "Pay by Web" → `https://inspree.formstack.com/forms/sun_premium_financing`
- Contact forms → `inspree.formstack.com/forms/{sfc_contact_us | spf_contact_us}`
- Agent Portal → `https://www.portal.sunpremium.com:8443/...` (login; 401 is EXPECTED, not broken)
- Mortgage Facebook `facebook.com/SunMortgageFunding` · Maps `g.page/SunMortgageFunding`
- Cross-company "The Sun Companies" links → the sibling **.com** (never webblaze.io).

## Verified facts (never fabricate)
Since 1958. NMLS #71517 (Mortgage). BBB A+: Mortgage accredited 1996, Finance 1987; **Premium has none**. Phones: Finance 504.837.9400 / Premium 504.834.9400 / Mortgage 504.837.3939. Mortgage: $5,000–$10M, "over 15 types of loans," non-bank (all VERIFIED on their live site). Finance personal loans $500–$3,000. Premium $100–$250K, 10+ insurance types. Team names verified per site (see git history if needed). Premium mailing: P.O. Box 6953, Metairie LA 70009.

## Status
Redesigns are link-audited (all clickable links + images OK), SEO complete (canonicals → .com, JSON-LD on every page, OG/Twitter/meta), GA per-site. **Ready for dad to push live to the 3 `sun-*-site` projects.** Note: redesign canonicals point to `.com/apply.html` etc. — they only resolve once a `.com` is flipped to the redesign (harmless now).
