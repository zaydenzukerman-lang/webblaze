# W Employment Law site — handoff state (read this first)

## 2026-10-07 — ROUND 3 client feedback (names, hero photo, awards marquee, Google reviews, team grid, footer)

Rebuild as always: `cd ~/webblaze && python3 sitegen/custom/wemploymentlaw/build.py && python3 sitegen/custom/wemploymentlaw/pages_extra.py`
(styles.css cache-bust is now `?v=20261009`).

- **A. Brand name.** Every published source (content/ready__*.json, pages/*.html, build.py) now says
  "W Employment Law". Replaced: "W Employment Law Group" (13, Terms of Use), "Whitehead Employment Law" (4),
  "SWemploymentlaw" as visible link text (6), standalone "W Law"/"W law" (8), "W Employment Law,," (5).
  Left alone on purpose: URLs/emails, app.swemploymentlaw.com vCard links, "Jacob N. Whitehead, APC",
  links to the old whiteheademploymentlaw.com domain inside one practice page (URLs, not text), and the
  raw crawl dumps in content/*.json without the ready__ prefix (never published). One Google review on
  the homepage quotes "W Employment Law Group" verbatim; reviews are never edited.
  Check: `grep -rniE "SW Employment Law|Whitehead Employment Law|W Employment Law Group|W Employment Law,,|\bW Law\b|>\s*SWemploymentlaw" public/wemploymentlaw --include=index.html`
- **B. Hero photo.** Desktop only (`@media(min-width:961px)` round-3 block at the end of styles.css): image
  `height:min(84%,720px)`, bottom-anchored. Mobile is unchanged.
- **C. Awards.** `{{AWARDS_MARQUEE}}` token -> `build.py render_awards_marquee()` (list = `AWARD_BADGES`).
  The CSS marquee renders the set 4 times and translates the track -50%, so the loop is seamless. It pauses on hover/focus.
  With prefers-reduced-motion it shows one static wrapped row. The band is dark teal with monochrome badges, like haelaw.com.
  To add a badge, put the webp in img/ and append it to `AWARD_BADGES`. Dark artwork on a transparent background goes in `AWARD_INVERT`.
- **D. Google reviews.** The data is REAL. `sitegen/custom/wemploymentlaw/fetch_reviews.py` (Playwright) scrapes the
  Google Maps listing (Newest, 5-star with text, expanded) into `reviews.json` and saves avatars to
  `public/wemploymentlaw/img/reviews/*.webp`. `build.py render_google_reviews()` renders the newest 5
  (`REVIEWS_SHOWN`) at build time through the `{{GOOGLE_REVIEWS}}` token on home.html. It also renders the rating summary, which links to
  `listing_url`. **To refresh reviews:** run `python3 sitegen/custom/wemploymentlaw/fetch_reviews.py`, then rebuild, then deploy.
  The script sometimes hits Google's sign-in popup. It retries (up to 8 fresh browsers). If every try fails it exits non-zero
  and leaves the old reviews.json untouched. NEVER hand-write or edit a review in reviews.json.
  The old static 4 cards (Alberto/Nava/Shauna/Larry) were removed from the homepage. They are still on the Jacob page.
  The never-configured Places-API "live reviews loader" (JS + GOOGLE_PLACES_API_KEY config + CSS) was deleted.
- **E. Team page** (/our-team/). `{{TEAM_GRID}}` -> `build.py render_team_grid()` from `team.json`. Each entry has
  name, vCard FN + TITLE, vcard URL, photo and initials. The order in team.json is the order on the page.
  Jacob's tile links to /jacob-n-whitehead/. Every other tile is `<a href="https://app.swemploymentlaw.com/vcards/<slug>.vcf" download>`
  with aria-label "Download vCard for X". Photos are 640x800 4:5 crops in `img/team/v2/`.
  The grid is full-bleed: 7 columns at 1600px+, 5 from 1100px, 3 from 700px, 2 on phones; a short last row is centred.
  Photos are B&W and turn colour on hover/focus. Touch devices stay B&W and show colour while tapped.
  A person with no photo gets a dark initials tile.
  **To add/update a person:** download their vCard, use the vCard TITLE, crop the photo to 4:5, then edit team.json and rebuild.
  Photo sources: vCard PHOTO for most people (420px originals, so the crops are 220-548px wide).
  Gladys uses the existing gladys.webp because it is sharper. Jacob uses jacob-cutout.png.
  **No photo anywhere (initials tiles): Dave Anas, Debi Pugliese, Vikas Kheni.** Their vCards have no PHOTO.
  Pamela's crop is the smallest (220x275). The server sends .vcf as `text/vcard` with `Content-Disposition: inline`.
  Because the vCard host is cross-origin, browsers ignore our `download` attribute. Phones will usually offer "Add to Contacts".
  For a forced download everywhere, the server would need to send `attachment`.
- **F. Footer** now matches the live site (measured with Playwright). Full-bleed #000, 3% side padding, 4 equal columns,
  Roboto 28.8px/400 headings, Didact Gothic contact/links with filled olive icons, HubSpot-style fields
  (#F5F8FA / #CBD6E2 / 3px / 40px tall), and a #ECD62B Poppins "Submit". There is a white rule, then a Karla #CBCBCB disclaimer.
  It still posts through our shared HubSpot handler (form 460ba517). Fonts were added to the Google Fonts link in page().

## 2026-10-06 — RESTRUCTURE: generator + folder URLs + results/badges/forms/tracking (READ FIRST)

The site is now **generated**, not hand-edited HTML. Source of truth moved to
`sitegen/custom/wemploymentlaw/` (build.py + pages/*.html fragments). **Do not hand-edit
`public/wemploymentlaw/*/index.html` directly — edit the fragment or build.py and rebuild:**
```
cd ~/webblaze && python3 sitegen/custom/wemploymentlaw/build.py
```
Full generator API/docstring is at the top of `sitegen/custom/wemploymentlaw/build.py` —
read it before adding pages. Quick summary: call `page(path, title, description, body_html,
h1=..., breadcrumbs=..., schema=...)` once per page; `path` must start+end with `/` and
mirrors the OLD wemploymentlaw.com WordPress URL (full map below) so no SEO/traffic is lost.
All asset/internal links are relative, computed from page depth — same output works at
`/wemploymentlaw/` (preview) or domain root (go-live).

### GO-LIVE: flip one switch
In `build.py`, set `GO_LIVE = True` (near the top), rebuild, redeploy. That swaps
`BASE_URL` from `https://webblaze.io/wemploymentlaw/` to `https://wemploymentlaw.com/` for
canonical/OG/sitemap/JSON-LD, and un-blocks robots.txt (preview is `Disallow: /` on purpose
so Google never indexes the staging copy). Also then: remove any preview banner (none exists
today), double check DNS/CNAME, and re-submit sitemap.xml in Google Search Console.

### New URL structure (every page = folder/index.html)
| Old file (this repo, now a redirect stub) | New URL | Mirrors old wemploymentlaw.com URL |
|---|---|---|
| index.html | `/` | `/` |
| about.html | `/jacob-n-whitehead/` | `/jacob-n-whitehead/` |
| contact.html | `/contact/` | `/contact/` |
| practice-areas.html | `/practice-areas/` | `/practice-areas/` |
| calculator.html | `/calculator/` | *(new — no old equivalent)* |
| blog.html | `/blog/` | `/blog/` |

Old flat `.html` files now contain tiny redirect stubs (meta-refresh + canonical + JS
`location.replace`) so any already-emailed/bookmarked/indexed link keeps working. `_redirects`
(Cloudflare Pages/Netlify format) also documents this; it's a no-op if the host doesn't read it.

### Full old-site URL map (from https://wemploymentlaw.com/page-sitemap.xml — for the next
agent building the ~35 remaining pages; register each with `page()` once written, using the
SAME slug so Google keeps the ranking):
```
/                                                 -> done (home)
/jacob-n-whitehead/                               -> done (Jacob's full bio page)
/contact/                                         -> done
/practice-areas/                                  -> done (overview/index of all areas)
/blog/                                             -> done (Insights index)
/our-team/                                        -> TODO (nav: About > Our Team)
/why-choose-us/                                   -> TODO (nav: About > Why Choose Us)
/videos/  (old also has dup /video/, use /videos/) -> TODO (nav: About > Videos)
/pricing/                                          -> TODO
/referrals/                                        -> TODO
/privacy-policy/                                   -> TODO (footer link already points here)
/terms-of-use/                                     -> TODO (footer link already points here)
/sms/                                               -> TODO (old SMS compliance notice page)
/faq/                                               -> optional; our /contact/ already has an FAQ section
/california-employee-class-action-attorneys/      -> TODO (nav: Practice Areas > Class Action & PAGA)
/work-related-reimbursements/                     -> TODO (nav: Practice Areas > Work Expense Reimbursements)
/wrongful-termination/                            -> TODO (individual practice-area pages;
/discrimination/                                      practice-areas/ today only has in-page
/sexual-harassment/                                   anchors for these — next agent can give
/overtime-violations/                                 each its own full page at these exact
/meal-breaks-and-rest-breaks/                         slugs and have practice-areas/ link out
/pregnancy-discrimination/                            to them instead of/in addition to anchors)
/medical-leave-disability/
/whistleblower-protection/
/independent-contractors/
/free-law-guides-8-new-laws-in-2021/              -> TODO (3 known law-guide slugs; nav: Resources > Free Law Guides)
/free-law-guides-first-steps-to-take-if-your-employment-rights-have-been-violated/ -> TODO
/free-law-guides-how-to-file-a-discrimination-claim-with-or-without-an-attorney/   -> TODO
/blog/<slug>/  (~20 individual posts)             -> TODO; slugs + scraped source text are in
                                                      sitegen/custom/wemploymentlaw/content/blog__*.json
/thank-you/                                        -> low priority; our forms show an inline
                                                      thank-you message instead of redirecting
not mirrored (internal WP design drafts, skip): /pre-home/, /home-2/ through /home-15/, /test/
```
content/*.json is **raw crawl data** (old_url, title_tag, body_html straight from WP, etc.) —
reference material, not ready to publish. See the "JSON PAGE SCHEMA" docstring section in
build.py: add `"page_ready": true` + the documented shape to a file once it's been rewritten
in this site's own styled markup, and `build.py` will pick it up automatically.

### What changed this pass (ITEM numbers from the restructure brief)
- **00 (homepage "$0" bug):** old homepage never actually showed "$0" as a result — that was
  an Elementor counter animation (`data-to-value`) the crawler's static fetch caught at its
  starting frame. Real numbers (confirmed from the old site's raw HTML): **$7,200,000** and
  **$1,700,000** "for class action — unpaid wages", **$2,650,000** "for disability
  discrimination". Added a real `.results-band` "Our Latest Settlements" section with these
  verbatim amounts + a "Prior results do not guarantee a similar outcome" disclaimer directly
  beneath. Reworded the `$0` value-card to **"No Upfront Fees"** (same meaning, can't be
  mistaken for a result). No `$0` left anywhere on the homepage.
- **09 (award badges):** downloaded the firm's real badge images from the old site
  (`why-choose-us/` page's 8-slide carousel), trimmed + converted to webp at native/2x crispness
  into `img/`: `avvo-rating-10`, `avvo-clients-choice`, `super-lawyers-rising-stars`,
  `americas-top-100`, `multi-million-dollar-advocates`, `aaj-member`, `expertise-best-2021`,
  `top40-under40`. All 8 shown on the homepage; 7 (all but Expertise.com, kept for variety) also
  shown on the Jacob page under the bio.
- **03 (Jacob's page):** original 4-paragraph bio kept 100% verbatim (client-approved, untouched).
  Added a new "Credentials" grid pulled verbatim from https://wemploymentlaw.com/jacob-n-whitehead/:
  Bar Admissions (California, Washington D.C.), Languages (English, Spanish — fluent), Focus Areas
  (Class Actions, PAGA Representative Actions, Wrongful Termination & Retaliation, Wage & Hour),
  Professional Memberships (AAJ, Consumer Attorneys of California, CELA, Consumer Attorneys of LA).
  All new labels have ES translations.
- **07/footer:** added Privacy Policy + Terms of Use links (point at `/privacy-policy/` and
  `/terms-of-use/`, pages not yet built — see URL map). Added LinkedIn icon. See social link
  verification below.
- **08 (forms):** homepage hero form now has the "Tell us what happened" textarea (previously
  contact-page-only) and BOTH forms now post to the **same** HubSpot form, `460ba517-…-ee4`
  (the one that actually has a `message` field — verified via
  `forms.hsforms.com/embed/v3/form/7690372/<id>/json`; the old home-page form id `2860c01f…`
  turned out to be a different, unrelated lead-magnet/PDF-download form with no message field,
  so switching both forms to `460ba517` was the correct fix, not a guess — see "SMS consent"
  below for the one open item this surfaced). Added an SMS consent checkbox (optional, unchecked
  by default — old site had no checkbox, consent was just a notice under the HubSpot embed, so an
  explicit opt-in checkbox is the safer upgrade) with the OLD SITE'S VERBATIM consent text
  (STOP/HELP, rates, links to the new privacy/terms URLs). `hutk` cookie + `pageUri`/`pageName`
  context included when present. All bilingual via data-es.
- **11 (tracking):** GA4 `G-6BN0TWE10Q` (this is the SAME ID already live on
  wemploymentlaw.com — confirmed from its page source, not guessed), Meta Pixel
  `2130487443675029`, HubSpot loader `js.hs-scripts.com/7690372.js` — all added to the shared
  shell, loaded async, but **gated** behind `location.hostname` ending in `wemploymentlaw.com`
  so the webblaze.io preview never pollutes the client's real analytics. `generate_lead` (GA4)
  + `Lead` (Meta) fire on successful form submit via a shared `welTrackLead()` hook.

### Social link verification (done this pass)
Checked every social URL against the live profile (HTTP status + WebFetch content check):
- **Facebook** `facebook.com/wemploymentlaw` — Meta blocks bot/non-browser requests (HTTP 400)
  for both this and the old `swemploymentlaw` variant, so status alone was inconclusive; kept
  the brand-consistent `wemploymentlaw` handle (matches the firm's current name, not the old
  "SW Employment Law" pre-rebrand handle).
- **Instagram** `instagram.com/wemploymentlaw/` — verified LIVE and active (469 followers,
  posts into 2026, matches brand). Old footer's `w_employment_law` variant could not be
  confirmed active — not used.
- **YouTube / TikTok** — unchanged, both confirmed live (200, correct channel).
- **LinkedIn** `linkedin.com/company/w-e-law` (added — wasn't on the old site's homepage at
  all) — verified LIVE: real company page, "W Employment Law", Irvine CA, 402 followers, 14
  listed employees including Jacob Whitehead, founded 2015. The old site's leftover
  `sw-employment-law` slug currently resolves to the SAME page (LinkedIn vanity-URL redirect
  from the pre-rebrand name) — either works, used the current one as specified.

### Open items I could not finish without client access
1. **SMS consent → HubSpot subscription type.** The consent checkbox is live, correctly worded,
   optional, and safely recorded (appended to the `message` field with the literal text
   `[SMS opt-in: YES/no]` on every submit, so no opt-in is ever silently lost). To make it ALSO
   write to a real HubSpot communication-subscription record via `legalConsentOptions`, the
   client's HubSpot admin needs to create an SMS subscription type under **Settings →
   Communications → Subscription Types** and give us its numeric ID — then set
   `SMS_SUBSCRIPTION_ID` in the shared form script (`build.py` → `COMMON_SCRIPT`) to that value.
   I did not invent a placeholder ID since a wrong one risks breaking real submissions.
2. **Facebook link** couldn't be positively confirmed live via automated check (Meta blocks
   bots) — someone should just click it once logged into Facebook to eyeball it.
3. The ~35 remaining pages (practice-area detail pages, team, why-choose-us, blog posts, law
   guides, videos, pricing, referrals, privacy/terms) are NOT built — that's explicitly the next
   agent's job, using `page()` + the content/*.json crawl data as source material.

### Test results (this pass)
`python3 -m http.server` + Python Playwright, both 1440×900 and 390×844, all 6 built pages:
0 console errors, 0 failed requests, 0 horizontal overflow on either viewport. Desktop nav
dropdowns open on hover/focus; mobile hamburger opens with all links reachable. EN/ES toggle
verified (h1 text changes). All 5 old-flat-file redirect stubs resolve to the correct new
folder URL. Form submission intercepted at the network layer on both `/` and `/contact/` —
confirmed it POSTs to `api.hsforms.com/.../460ba517-…`, payload has correct
firstname/lastname/email/phone + message (with SMS opt-in note when checked), and the request
was fulfilled locally so **no test lead ever reached HubSpot**. Screenshots of home/jacob/contact
at both sizes reviewed — mobile hero confirmed single-column, not squeezed.


Client demo site for **W Employment Law** (a real CA employment law firm), built to pitch them.
Hosted on **GitHub Pages** at **https://webblaze.io/wemploymentlaw/**. Zayden is 13; his dad
**Forest** reviews the work and sends the client-facing emails.

## Deploy (no Vercel — the whole webblaze.io site is on GitHub Pages)
Repo `zaydenzukerman-lang/webblaze`, branch `main`, folder `/docs`. `gh` CLI is authed. Deploy:
```
cd ~/webblaze && npm run build && rm -rf docs && cp -R out docs \
  && touch docs/.nojekyll && printf 'webblaze.io' > docs/CNAME \
  && git add -A && git commit -m "…" && git pull --rebase origin main && git push origin main
```
GitHub Pages rebuilds in ~30s. DNS is on Cloudflare (token `~/.cf_webblaze_token`). Vercel token is DEAD — do not use. Full infra notes in `WEBBLAZE-HANDOFF.md`.

**Cache gotcha:** `styles.css` and images are cached hard. When screenshotting via Playwright,
bust cache first: `document.querySelector('link[href*=styles.css]').href='styles.css?b='+Date.now()`
and same for `img[src*=logo]` / the hero img. Tell Zayden to hard-refresh (Cmd+Shift+R).

## Files: `~/webblaze/public/wemploymentlaw/`
Multi-page site (each is a real separate page): `index.html` (Home), `practice-areas.html`,
`calculator.html` (Unpaid Wages/Overtime calculator, real math), `blog.html` (Insights, 6 articles),
`about.html`, `contact.html`. Shared `styles.css`. `i18n.js` = EN/ES toggle.
`img/`: `jacob.png` (AI-enhanced 1024px founder photo, identity preserved; backup `jacob_orig_348.png`),
`logo.png` (official teal logo, header), `logo-white.png` (footer/navy), `favicon.png`+`favicon-32.png`
(official W mark), `city.jpg` (the OCEAN aerial shot used on the CTA band — dad loves it),
`consult.jpg` (why-us bg), `workers.jpg`, `pa-*.jpg` (9 practice-area photos), `hero.jpg`/`atty.jpg` (UNUSED stock — do not use).

## Homepage hero (locked look Zayden approved after MANY iterations)
Minimal, full-height (one screen, no mid-fold cutoff): LEFT = slogan `Fighting for California Employees`
+ the Free Case Review form (form must be visible above the fold — it's the money-maker). RIGHT half =
large Jacob photo with gold "Founding Attorney" caption. Nothing else in the hero.

## Form → their real HubSpot CRM
POST to `https://api.hsforms.com/submissions/v3/integration/submit/7690372/2860c01f-db29-45c3-bc90-567d6cc5d835`
fields `firstname,lastname,email,phone`. Portal `7690372`. Leads land in THEIR HubSpot. 2 test contacts
labeled "WEBBLAZE TEST / PLEASE DELETE" are in their HubSpot (they can delete; can't be deleted by us).

## Verified real facts — NEVER fabricate (Zayden is strict on this)
Phone **888-492-0633**; **7700 Irvine Center Drive, Suite 800, Irvine, CA 92618**; founder **Jacob N.
Whitehead**; testimonials **Alberto, Nava, Shauna, Larry** (real, verbatim). Practice areas + 6 FAQs verified.
**Email: contact@wemploymentlaw.com** (Zayden confirmed this is the firm's real email — it's in the footer site-wide + the contact page. It was NOT on their public site, so I'd removed it earlier, but Zayden verified it's correct.)

## Done so far
Multi-page structure; HubSpot form; SEO (canonical, robots, OG/Twitter, LegalService JSON-LD, sitemap.xml,
robots.txt on all pages); official logo in header+footer+favicon; AI-enhanced Jacob photo; EN/ES language
toggle on the HOMEPAGE (persists via localStorage; 37 strings translated + placeholders).

## PENDING — dad's latest notes (DO THESE NEXT)
1. **Fix the logo — it looks "washed out."** Header logo `img/logo.png` is a medium-teal wordmark on white;
   at 58px it reads pale. Boost contrast/saturation/darken it (e.g. ImageMagick `-modulate 100,130` +
   `-brightness-contrast -8x15`) so it's crisp, or swap to a stronger teal. Redeploy + verify.
2. **Add a SUBTLE background to the green sections.** Dad: "the ocean in the bottom green looks perfect"
   = the `.cta-bg` band uses `img/city.jpg` (ocean) under a teal overlay. He wants that same subtle,
   almost-transparent treatment on the flat green areas: the **hero** (`.hero`, styles.css ~line 42,
   currently a flat teal gradient) and the **middle green band** (`.band-h` = the "Serving All of
   California / Practice Areas" band, ~line 90, flat teal). Add `url('img/city.jpg') center/cover` UNDER a
   heavy teal overlay (~0.88–0.92 opacity, like `.cta-bg:after` rgba(8,63,71,.82)) so the ocean is barely
   visible. Keep it subtle. Redeploy + screenshot to confirm it's not too strong.
3. **Client email for dad to send** (see below) — the long version I wrote was rejected as too long.

## Client email — REWRITE SHORT (Zayden's rules)
It is **FROM DAD (Forest), introducing Zayden, explaining the site + $500/mo**, copy-paste ready.
Zayden's email rules (hard): **short**, plain, **no em-dashes**, write like a text, minimal punctuation
(no heavy use of `( ) - :`), sounds human not AI, no fabrication. ~5-7 short lines max.
Include: intro of Zayden/WebBlaze, the link `webblaze.io/wemploymentlaw/`, 2-3 punchy benefits (feeds their
HubSpot, mobile+Google, one-click Spanish), the price **$500/month all-inclusive** (hosting, updates,
weekly reports, Google growth), $200 off first month, soft CTA. Keep it tight.
NOTE: confirm with Zayden whether $500 is monthly all-in or the Google service on top of the $300/yr site.

## Other open threads
- EN/ES toggle is homepage-only; extending site-wide is a nice follow-up.
- In Spanish the nav is a bit crowded (phone wraps) — could shorten ES labels.
- Zayden's Instantly cold-email signature: headshot hosted at **webblaze.io/zayden.png** (circular);
  signature HTML uses WebBlaze orange `#F7551F`. He was adding it in Instantly → Email Accounts → Signature.
- Bigger WebBlaze context + all creds/pricing/agents: `WEBBLAZE-HANDOFF.md`, `LOCAL-SEO-PLAYBOOK.md`,
  `prospecting/cold-email-templates.md` (Patches' email voice rules).

## 2026-10-05 — CLIENT PAID. Form routing verified
- Both forms (index.html, contact.html) POST to HubSpot portal 7690372 form 2860c01f… with firstname/lastname/email/phone.
  Verified: HubSpot form exists (400 REQUIRED_FIELD on probe → firstname, lastname, phone required = our names; all 4 required on our side).
  Browser test EN+ES with request intercepted (no fake leads): payload correct, confirmation shown.
- Fixed: honeypot f_co was off-screen (autofill could fill it → lead silently dropped) → now display:none.
- Fixed: Spanish visitors now get Spanish confirmation / sending / error text (lang from <html lang>).
- Go-live: their domain DNS is on THEIR Cloudflare (NS gerald/lucy), current site WordPress, email = Google Workspace (MX aspmx) — don't touch MX.
- Client email drafted for Zayden asking for Cloudflare access + Google Business Profile manager access.
- Still open: dad's notes (washed-out logo, subtle ocean bg on green sections).
- 2026-10-05: Verified THEIR live site uses the same HubSpot portal: home = form 2860c01f (we match), contact = form 460ba517
  with optional `message` textarea → our contact.html now posts to 460ba517 + optional message (EN/ES placeholder). Tested.
- 2026-10-06 (Gladys request): AI photo of Jacob REPLACED with real photos she sent (Downloads/@faveofJW*.jpg):
  home hero = img/jacob-hero.webp (studio shot, bg removed with rembg isnet), about = img/jacob-about.webp (palms/office crop),
  og/twitter = img/jacob-share.jpg. Old jacob.png / jacob-cutout.png no longer referenced. About bio = Jacob's FULL original
  4-paragraph bio verbatim from wemploymentlaw.com/jacob-n-whitehead/ + "Founder and Managing Attorney" (Spanish via data-es).
  Fixed phone hero (was 2 columns, form squeezed to 185px) → one column. styles.css?v=20261006 cache-bust.
- DEPLOY GOTCHA: `npm run build` can fail on a transient Google-font fetch → whole && chain silently skips commit/push. Check exit code.
