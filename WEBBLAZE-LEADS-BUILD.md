# WebBlaze — Cold-Lead Demo Builds (Fetchero + The Town Agency)

Task: build TWO **genuinely distinct, professional** demo sites (like the Sun previews on `*.webblaze.io`)
to pitch these prospects via cold email (dad's style), leading with the Sun sites as proof.
CRITICAL LESSON: each site must be a UNIQUE design — different type, color, AND layout structure.
Not a recolored template. Sun = navy/gold Fraunces private-bank. OBF concept = sea/coral Anton adventure.
These two must differ from those AND from each other. Rules: premium imagery, NO brand names in photos,
NO fabricated people/reviews/credentials (verified facts only), mobile hamburger nav, conversion-first
(prominent "Get a Quote"), verify live desktop+mobile before claiming done.

Deploy pattern: static files in `public/<slug>/`, add slug to DEMOS in BOTH `next.config.ts` and `src/proxy.ts`.
Deploy: `npm run build && git add -A && git commit && vercel --prod --yes --scope hbz-holdings`. trailingSlash:false.
Pexels API key (Zayden's): 85gzYeGliCl062HE8cT3bQZRphoW2iaH9pI2oxmLxJ7zE1KTttQe8eXL  (Authorization header, add User-Agent).

## Lead 1 — FETCHERO INSURANCE   → slug: `fetchero`  → https://fetchero.webblaze.io
- "Family-Owned Ohio Insurance Agency Since 1989"
- 107 E College Ave #202, Westerville, OH 43081 · 614-891-9311 · Kip@FetcheroInsurance.com
- Team: **Kip Fetchero** (Owner), **C.J. Fetchero** (Founder), **Bekah** (Customer Service Rep). "agents have 60+ years combined experience."
- Lines: Home, Auto, Life, Business. Independent agency (multiple carriers).
- Hours: Mon–Fri 8:30am–4:30pm; Sat/Sun by appointment.
- Real testimonials (use verbatim, short): "Superior customer service and they are very knowledgeable at what they do." · "Quick responses and great customer service." · "They answer any and all questions… response time is almost immediate."
- Current site: blue/white carousel, dated. Cold-email angle: warm family agency, weak/dated site + SEO.
- DESIGN DIRECTION (unique): **warm, human, family Midwest.** Palette deep EVERGREEN + warm CREAM + AMBER/honey accent.
  Friendly geometric sans (Poppins/DM Sans), rounded cards, soft shadows, generous whitespace, personal
  (meet Kip/C.J./Bekah via monogram avatars — no real photos available), simple "how it works", real reviews.

## Lead 2 — THE TOWN AGENCY   → slug: `thetownagency`  → https://thetownagency.webblaze.io
- Family-owned since 1968. 1205 Franklin Ave, Suite 102, Garden City, NY 11530.
- (516) 294-1000 · Text (516) 522-0387 · Fax (516) 741-6025 · info@thetownagency.com
- Lines: Homeowners, Auto, Home & Auto bundle, Flood (FEMA NFIP + private), Landlord, Umbrella, Business, Life.
- Carriers: Andover Companies, AARP/The Hartford, Progressive, Plymouth Rock, Assurant, Nationwide.
- Taglines: "Quick quote. No pressure." · "Trusted local insurance guidance since 1968."
- Service area: Garden City, Mineola, New Hyde Park, Westbury, Levittown, Hicksville, Nassau County, Suffolk County, NYC, NY State.
- 4.9/5 Google. No named owner — DO NOT invent names.
- DESIGN DIRECTION (unique): **established, editorial, refined Long Island.** Palette deep SLATE/INK + crisp WHITE +
  BURGUNDY (or deep harbor red) accent + subtle warm sand. Serif headings via **DM Serif Display** (NOT Fraunces) + Inter.
  Editorial/heritage layout: "since 1968" prominence, multi-carrier trust strip, comparison-shopping angle, more lines
  of coverage grid, Nassau County service-area map/list, 4.9 reviews. Traditional-refined, different structure from Fetchero.

## Status
- [x] Research both · [x] spec saved
- [x] Build Fetchero · [x] Build Town Agency · [x] deploy+verify (LIVE) · [ ] cold emails
- **LIVE:** https://fetchero.webblaze.io · https://thetownagency.webblaze.io (deployed, DNS+domains attached, verified 200 + assets).
- Slugs added to DEMOS in next.config.ts + src/proxy.ts. Cloudflare CNAMEs (fetchero, thetownagency -> cname.vercel-dns.com) + vercel domains add done.
