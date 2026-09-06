# Miami leads — status & the real next step (read this)

## Where we are
- **Clean source that works:** OpenStreetMap (Overpass). Free, no blocking. Running continuously
  via `miami_leadgen.py` across 84 Miami-area cities x 8 niche groups, filtering out chains,
  car dealers, foreign sites, and web-agency emails. Output: `leads_miami_master.csv`.
- **Current volume:** ~40 clean, genuinely-local leads with emails (real ICP: roofers, plumbers,
  AC repair, glass/marble shops, upholstery, etc.).

## What did NOT work (tested, don't retry)
- **Business directories** (Manta, Cylex, Hotfrog, ChamberOfCommerce, Brownbook, eLocal):
  all return **403 (Cloudflare bot-block)** to scripts.
- **Bing/DuckDuckGo free scraping:** decodes, but returns **junk** (out-of-state companies,
  weather.com, github, job sites) with no reliable localization. Disabled (`bing_leadgen.py.disabled`).
- Free scraping caps out here. OSM is clean but naturally limited — most small businesses simply
  aren't in OSM with a contact email.

## The real path to HUNDREDS/day (needs your call)
1. **Instantly Lead Finder / Supersearch** (you already pay $100/mo — BEST option).
   Filter by industry + location + company size, get **verified** personal emails, push straight
   to a campaign. Higher reply rate than info@/contact@. This is the unlock.
2. **Google Places API** (needs a Google Cloud billing key). Pull every business by type+city with
   website/phone at scale, then harvest emails. ~$0.017/search; a few $ = thousands of businesses.
3. **Apollo.io / similar** B2B database (free tier + paid) for verified emails.

When you're back, point me at one of these (or drop in a Places API key) and I'll wire the whole
pipeline into Instantly.
