# Curb — SEO & Marketing Master Reference
Researched 2026-07-10. This is the "why" behind CLIENT-RESULTS-PLAYBOOK.md's "what." Skills loaded:
seo, seo-audit, growth-engine, paid-ads (available for deeper on-demand work per client).

---

## 1. How Google Business Profile ranking ACTUALLY works (2026)
Three pillars, in order of what we control:
- **Relevance** — the single most influential factor is the PRIMARY GBP category. "Pressure
  washing service" as primary beats a vague "Cleaning service." Secondary categories add support.
  Keywords in the business description and on the linked website reinforce this.
- **Proximity** — non-negotiable, we can't change where the client is physically located. This is
  why service-area accuracy matters (don't claim towns they don't actually serve — hurts trust
  signals and wastes ad budget on LSA).
- **Prominence** — reviews, citations, links, reputation. **Review RECENCY now matters more than
  raw count** — 10 recent reviews mentioning specific services can outrank 50 old generic ones.
  This changes our advice: push clients to ask for reviews continuously, not in one initial burst.
- **Practical implication:** GBP optimization is legitimately the highest-ROI, lowest-cost lever
  we have. It's also the one most owners have never touched. This is the correct Week-1 priority.

## 2. Citations — quality beats quantity, and it's not close
- 30-50 accurate, high-authority citations (BBB, Yelp, Angi, industry-specific directories)
  outperform 200 generic directory listings. **BBB-tier citations carry ~10-15x the ranking
  weight of free generic directories.**
- Exact NAP (Name/Address/Phone) format must be identical everywhere — pick ONE format
  (e.g. always "St" not sometimes "Street") and use it on every listing, the site, and GBP.
- **Implication for our Distribb use:** don't chase citation volume as a vanity metric in
  reports. Report the QUALITY tier (BBB, Yelp, industry sites) not just a raw count.

## 3. Schema markup — a real, measurable lever (now implemented)
- Pages with complete LocalBusiness JSON-LD schema appear in the local pack **30-50% more often**
  than identical pages without it. This is one of the few "add code, get ranking benefit" wins.
- **Done tonight:** added LocalBusiness (HomeAndConstructionBusiness subtype — schema.org has no
  dedicated "pressure washing" type) JSON-LD to the TidalWave template — services, prices, hours,
  service areas, review data. Every cloned client site inherits this automatically. Client sites
  need their REAL review count/rating swapped in from their GBP — never fabricate this.
- Also matters for AI search (ChatGPT/Perplexity-style answers) — schema is how those engines
  understand "who is this business" when answering "best pressure washer near me" style queries.
- **Do NOT use:** FAQ schema (Google restricted rich-result eligibility to gov't/healthcare sites
  in 2023) or HowTo schema (deprecated). Skip both — no ranking benefit, wasted effort.

## 4. Google Local Services Ads — the eligibility reality check
- Background checks run through third-party screener (e.g. Evident): identity + criminal history
  + license + insurance verification. **Full verification takes 3-4 WEEKS**, not days — this
  confirms our "start day 1" runbook advice is correct, it's just slower than clients expect.
  Set that expectation explicitly at kickoff so it's not a surprise in week 2.
- **Categories are added quarterly without announcement** — before promising LSA to any specific
  prospect, check the live LSA portal for "pressure washing" eligibility in THEIR metro. Don't
  promise it in a sales email before confirming.
- The "Google Guaranteed" badge itself is a trust signal worth real money to close — lean on that
  in the pitch once a client is enrolled.

## 5. Call tracking — implementation detail that protects our SEO
- **Dynamic Number Insertion (DNI)** swaps the displayed number via JavaScript per visitor/source
  — but the number hardcoded in the HTML (what search engine bots see) should stay the client's
  real static number. This avoids any risk of Google associating the wrong number with the
  business (a real NAP-consistency risk if done wrong).
- Session-level tracking (unique number per visitor) is more precise than source-level (one
  number per channel) but burns through more phone numbers — source-level is enough for our
  client size; don't oversell precision they don't need.
- **The pitch stat:** phone calls in home services close at MUCH higher rates than form fills — a
  call is someone with an urgent need, a form-fill is someone comparison shopping. This justifies
  why we lead every site with a phone number and text button, not just a form.

## 6. Website conversion — hard numbers to benchmark against
- Average service-business site converts 2-4%. Best-in-class: 7-12%. **Our own bar should be
  best-in-class** — TidalWave already does the big two things right (short forms, one clear CTA),
  keep enforcing this on every clone.
- **Mobile converts ~42% lower than desktop** — mostly friction (slow loads, small tap targets).
  Since most client traffic will be mobile (phone in the driveway), our mobile-first build
  standard isn't optional polish, it's the main conversion lever.
- **Load speed is brutal:** 1-second load = ~39% conversion rate; 6-second load = ~18%. Keep
  images compressed (<300KB, already our rule) and avoid heavy JS.
- Fixing a weak headline + shortening a form to 3-4 fields alone typically lifts conversion
  30-50%. This is EXACTLY what our audit template should flag on every prospect's current site.

## 7. Meta ads creative — what actually works (Full Funnel tier)
- **Authenticity beats polish.** Phone-shot before/afters and real crew footage outperform
  produced video. Corporate "About us, serving the community since..." openers kill attention in
  the first second — never write ad copy like that.
- Short vertical video sees ~34% higher engagement than static images for service ads.
- **Speed-to-lead is the single highest-leverage thing in this whole tier:** conversion drops
  sharply if a lead isn't contacted within 5 minutes. This must be non-negotiable client coaching
  — a $20/day ad budget is wasted if the owner replies six hours later.
- Before/after IS the native ad format for this industry — lean all the way into it, don't try to
  make it look like a "real" ad agency's polished reel.

## 8. TCPA — the compliance fix already applied tonight
- SMS MARKETING requires prior express written consent — no small-business exemption, fines
  $500-1,500 PER TEXT. This directly affected our reactivation campaign design (Lever 4) — fixed:
  reactivation now leads with email by default, SMS only for customers who've opted in going
  forward (consent checkbox added to the quote-form spec). Review-request texts (Lever 2) are
  transactional (immediately post-job, no discount) and lower-risk, but we still only text numbers
  given for service communication and honor any stop request instantly.
- Never let a client "just text the whole customer list a promo" — that's the exact fact pattern
  TCPA class actions are built on, and it would be OUR system that caused it.

## 9. The real numbers behind why retention/reactivation matters
- Average pressure-washing customer: ~$225/job, ~2 jobs/year, ~5-year relationship = **~$5,250
  lifetime value.** Top performers see 60-76% repeat rates; industry average is 30-50%.
- **This is the number that should anchor every retainer pitch.** A $1,200/quarter retainer isn't
  expensive against a single customer's $5,250 lifetime value — reframe every price objection
  through this lens instead of "is $800/mo a lot of money."
- Good CLV:CAC ratio benchmark industry-wide is 3:1 — useful shorthand when explaining ad spend
  ROI to a client ("if a Google lead costs you $75 and one job is worth $225 immediately, that's
  already 3:1 on the FIRST job alone, before repeat visits").

## Concrete actions this research changed (already done)
1. ✅ Added LocalBusiness JSON-LD schema to TidalWave template (inherited by all future clones)
2. ✅ Fixed reactivation campaign to default to email, gated SMS behind real consent (TCPA)
3. ✅ Noted transactional-vs-marketing SMS distinction in the review-request flow

## Actions to take when we have a real client (not urgent pre-revenue)
- Confirm LSA eligibility for pressure washing in the CLIENT'S specific metro before promising it
- Set up DNI correctly: static number in HTML, JS swap for tracking — verify with view-source
- Add the SMS opt-in checkbox to each client's live quote form once built
- Use the $5,250 CLV stat explicitly in the sales pitch and in monthly reports ("this client's
  reactivation batch pulled forward ~$X of five-year value this month")

Sources: [Local ranking factors 2026](https://www.brightlocal.com/learn/google-local-algorithm-and-ranking-factors/) ·
[GBP category = top factor](https://localdominator.co/local-search-ranking-factors/) ·
[Citation quality](https://navoto.com/blog/local-citation-guide/) ·
[Schema 30-50% lift](https://gatilab.com/local-business-schema-markup/) ·
[LSA background checks](https://support.google.com/localservices/answer/12174778) ·
[DNI & SEO](https://www.ctm.com/blog/marketing/attribution/seo-dynamic-number-insertion/) ·
[CRO benchmarks](https://www.bspkn.co/insights/conversion-rate-optimization-service-businesses-2026/) ·
[Meta ads for service biz](https://adadvisor.ai/blog/facebook-ads-for-service-businesses-in-2026-what-actually-works) ·
[TCPA 2026 rules](https://activeprospect.com/blog/tcpa-text-messages/) ·
[Pressure washing CLV](https://awcmag.com/customer-lifetime-value/)
