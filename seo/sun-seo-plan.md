# Sun Companies — SEO execution plan (ready to run on "yes")

3 sites, Metairie LA / Greater New Orleans. All since 1958. Keywords chosen for **local intent + buying intent** (people who search these are close to acting). Nothing here is published yet — sites are `noindex` previews until the client says go.

---

## 1) Sun Mortgage Funding — keyword map
**Primary (money) keywords**
- mortgage lender Metairie / Metairie LA
- home loans New Orleans / Greater New Orleans
- refinance Metairie / mortgage refinance New Orleans
- first-time home buyer Louisiana
- FHA loan New Orleans · VA loan Louisiana
- renovation / construction loan New Orleans
- mortgage broker Metairie LA

**Informational (top-of-funnel) topics → articles**
- How much down payment do you need to buy a home in Louisiana?
- FHA vs. conventional loans: which is right for a New Orleans buyer?
- First-time homebuyer programs in Louisiana (2026 guide)
- Should you refinance your Metairie home right now?
- What credit score do you need for a mortgage in Louisiana?
- Buying a historic home in New Orleans: financing what to know
- Renovation loans explained: fund repairs into your mortgage
- The New Orleans homebuying timeline, step by step

## 2) Sun Premium Financing — keyword map
**Primary**
- insurance premium financing Louisiana
- premium finance company New Orleans / Metairie
- commercial insurance financing Louisiana
- premium financing for insurance agents Louisiana
- finance insurance premium New Orleans

**Informational → articles**
- What is insurance premium financing and how does it work?
- Premium financing for Louisiana businesses: keep cash, keep coverage
- A guide for agents: offering premium financing to your clients
- How premium financing protects your business from a lapse in coverage
- Commercial vs. personal insurance premium financing
- 10+ types of insurance you can finance in Louisiana
- Cash flow 101: why smart businesses finance their premiums

## 3) Sun Finance — keyword map
**Primary**
- personal loans Metairie LA / New Orleans
- small personal loan Louisiana
- installment loans New Orleans
- local lender personal loans Metairie
- quick personal loan Louisiana

**Informational → articles**
- How to cover an unexpected expense in New Orleans (without a credit card)
- Personal loans vs. payday loans: know the difference
- What you need to apply for a personal loan in Louisiana
- 5 smart uses for a small personal loan
- How local lenders decide (and why in-house servicing matters)
- Building credit with a personal loan in Louisiana
- Emergency car repair? Your options in Metairie

---

## First 8 weeks — content calendar (4 articles/week per site)
Run all 3 sites in parallel. Weeks map to the topic lists above; each article = one target keyword.

| Week | Mortgage focus | Premium focus | Finance focus |
|------|----------------|---------------|---------------|
| 1 | Down payment guide + FHA vs conventional + first-time programs + refinance-now | What is premium financing + business cash guide + agent guide + lapse protection | Cover an expense + personal vs payday + how to apply + 5 smart uses |
| 2 | Credit score needed + historic home financing + renovation loans + homebuying timeline | Commercial vs personal + 10+ insurance types + cash flow 101 + FAQ deep-dive | In-house servicing + build credit + emergency car repair + local lender FAQ |
| 3–8 | Rotate long-tail variations of the primary keywords + answer real GSC queries as they appear + seasonal ("2026", "spring buying season", "hurricane-season coverage" for Premium) |

**Rule:** from Week 2 on, let **Google Search Console decide** — write toward the queries already showing impressions but ranking on page 2 (fastest wins).

## Local SEO (high impact — 3 businesses, one address)
- **Google Business Profile** for each company at 3525 N. Causeway Blvd, Ste 900, Metairie, LA 70002.
  - Correct primary category (Mortgage Lender / Financial Institution / Loan Agency), services, hours, photos.
  - Weekly GBP post (link to a new article or the Apply page).
- **NAP consistency** everywhere (Name/Address/Phone identical to the site footer): Yelp, BBB, Chamber of Commerce, Apple Maps, Bing Places.
- **Reviews:** simple ask-flow — after a good closing, client sends the customer the Google review link. (Never fabricate reviews.)
- Distinct phone per company (already on sites): Mortgage 504-837-3939 · Premium 504-834-9400 · Finance 504-837-9400.

## On-page / technical (already strong — keep it up)
- ✅ Titles, meta descriptions, canonical, OG/Twitter, `FinancialService` + `PostalAddress` + `OpeningHours` JSON-LD, sitemap.xml, robots.txt (via `scripts/seo_inject.py`).
- **To add when live:** `/blog` section + `Article`/`FAQPage` schema on posts; internal links from articles → Apply; breadcrumbries; image alt text (done on site imagery).
- Keep Core Web Vitals green (static HTML on Vercel = already fast).

## Go-live setup order (per site)
1. Point real domain → Vercel; flip `noindex` → `index` (edit `seo_inject.py` robots meta).
2. GSC property + verify + submit sitemap.
3. GA4 property + tag + Apply-form conversion event.
4. Claim + optimize Google Business Profile.
5. Baseline rank snapshot for the primary keywords.
6. Publish `/blog` + Week-1 articles; Request Indexing in GSC.

## Realistic expectations (set these with the client)
- Local + long-tail keywords: **early movement in 4–8 weeks**, meaningful traffic in **3–6 months**.
- Money keywords ("mortgage lender Metairie") are competitive — the article engine + local SEO is how we climb steadily.
- Weekly reports show the trend so they always see progress, not silence.
