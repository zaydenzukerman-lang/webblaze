# WebBlaze Site Factory

Turn a lead into a live, polished website in minutes — and handle change requests in seconds.
This is how we build dozens of sites without hand-coding each one (WEL took hours; this takes ~2 min).

## New client (they said YES → build their free preview)
1. `python3 intake.py <domain> "<niche>" "<City, ST>" <slug>`
   → scrapes their existing site, writes `configs/<slug>.json` (name, phone, address pre-filled).
2. Open `configs/<slug>.json`, fix anything wrong (intake is a draft), add a tagline/about/reviews.
3. `python3 generate.py configs/<slug>.json` → builds `~/webblaze/public/<slug>/index.html`
   (auto-pulls a matching hero photo from Pexels, picks an industry color theme).
4. Preview: `cd ~/webblaze/public && python3 -m http.server 8899` → open `localhost:8899/<slug>/`.
5. `bash deploy.sh "add <slug>"` → live at `https://webblaze.io/<slug>/`.
6. Reply to the lead with the link. When they pay ($629/yr), it's already built.

## Change requests (the inbound firehose: "update my hours / new photo / add a service")
Almost everything is a config edit, not code:
- New phone / hours / address / services / reviews / tagline / colors → edit `configs/<slug>.json`
  → `python3 generate.py configs/<slug>.json` → `bash deploy.sh "update <slug>"`. Done in a minute.
- Config fields: business_name, niche, city, phone, email, address, hours, tagline, about,
  services[{icon,title,desc}], reviews[{name,text}], theme{primary,dark,accent}, hero_term.
- Only true design/structure changes need touching the template in `generate.py`.

## Why sites don't look cloned
`generate.py` picks a different color theme + hero image per industry, and every site uses the
client's real name, services, reviews, and photos. Roofers look like roofers, dentists like dentists.

## Scale plan
- For a batch of yeses: run intake on each domain, quick-edit configs, generate all, deploy once.
- A reviewer (you or Claude) spends ~2-3 min polishing each config instead of hours coding.
