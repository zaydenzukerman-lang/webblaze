# W Employment Law site — handoff state (read this first)

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
