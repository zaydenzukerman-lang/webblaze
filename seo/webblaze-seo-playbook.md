# WebBlaze SEO Playbook (operating manual)

The recurring-revenue product on top of the $300/yr sites. Sold to Sun as **$100/mo per site — "aggressive SEO with weekly reporting."** This doc is *how I actually deliver it* every week.

Source: the SEO workflow Dad relayed (tools = Vercel + Google Search Console + GA4 + Distribb backlinks + Gmail outreach; high-volume ~1,500-word articles). Adapted to WebBlaze's $100/mo price point.

---

## What the client is paying for (the pitch, in plain terms)
Getting **found on Google** when local people search for what they do — and proving it with a report every week.

Five pillars, every month:
1. **Content** — fresh keyword-targeted articles published to their site (the engine of rankings).
2. **Technical SEO** — site stays fast, mobile-clean, fully indexed, with rich schema.
3. **Local SEO** — Google Business Profile + local citations so they win the map pack for "…near Metairie."
4. **Off-page** — backlinks (Distribb) + light outreach (Gmail) to build authority.
5. **Reporting** — a plain-English weekly report: what I did, what moved, what's next.

## Tools (the stack)
| Tool | Use |
|------|-----|
| **Vercel** | Hosting + deploy the new article pages (already how the sites run) |
| **Google Search Console (GSC)** | Submit sitemaps, watch indexing, mine the queries people actually type |
| **Google Analytics 4 (GA4)** | Traffic, top pages, form conversions |
| **Distribb** | Backlink building |
| **Gmail** | Outreach for links / local citations / guest posts |
| **Claude (me)** | Draft the 1,500-word articles + keyword research + reports |

## Cadence (per site, $100/mo = "aggressive")
- **4 articles / week** (~16/mo), 1,200–1,500 words each, one clear target keyword + supporting terms.
- **Weekly technical sweep** (see checklist).
- **Weekly local-SEO task** (rotates: GBP post, citation, review request).
- **1 weekly report** emailed Friday.
- *(Daily-article "max" cadence is the upsell if they want more.)*

## The weekly routine (repeatable checklist)
**Mon — Plan & research**
- [ ] Pull last week's GSC queries → find rising/near-page-2 keywords ("striking distance")
- [ ] Pick the week's 4 article targets from the content calendar + GSC gaps
- [ ] Draft outlines (Claude)

**Tue–Thu — Produce & publish**
- [ ] Draft 4 articles (Claude), 1,200–1,500 words, each: target keyword in H1/title/URL/first 100 words, 2–3 internal links (to Apply + a service page), 1 local reference (Metairie/Greater New Orleans), FAQ block
- [ ] Add each as a page under `/blog/<slug>` on the site, `?v` cache-bust css, run `seo_inject.py`, deploy
- [ ] Submit new URLs in GSC (Request Indexing)

**Fri — Off-page + report**
- [ ] 1–2 backlinks via Distribb; 1 outreach email (Gmail) for a citation/link
- [ ] Update GBP (post + photo), request 1 review from the client's happy customers
- [ ] Fill the weekly report (template) and email it

## On-page rules for every article (non-negotiable)
- Target keyword in: `<title>`, H1, URL slug, first paragraph, one H2, meta description.
- Unique meta description (150–160 chars), written for clicks.
- `Article` + `FAQPage` JSON-LD (extend `seo_inject.py`).
- Internal links: every article links to the **Apply** page and one service page.
- Louisiana/Metairie/Greater New Orleans mentioned naturally (local relevance).
- Never keyword-stuff; write for a real reader first.

## Guardrails (from our house rules)
- **No fake reviews, no fabricated claims, no fake credentials.** Only verified facts (see SUN-PROJECT-STATE.md "VERIFIED FACTS").
- Honest, useful content — Google rewards it and it protects the client's license/compliance.
- Everything ships + deploys; verify live with `curl`, don't just assume.

## Setup checklist (do once, per site, on client "yes")
- [ ] Deploy to the client's real domain; flip `noindex,follow` → `index,follow`
- [ ] GSC: add property, verify, submit `sitemap.xml`
- [ ] GA4: create property, add tag, mark the Apply form as a conversion
- [ ] Google Business Profile: claim/optimize (categories, services, hours, photos, NAP)
- [ ] Baseline rank check for the target keywords (so weekly reports show movement)
- [ ] Build the `/blog` index + first 4 articles
