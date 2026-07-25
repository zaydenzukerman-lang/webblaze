# Orange Beach Fish Charter Services — static site generator (WebBlaze rebuild)
import pathlib
B = pathlib.Path("/Users/zaydenzukerman/webblaze/public/orangebeachfish")
V = "1"  # asset version

TEL="+12519792682"; TN="(251) 979-2682"; EMAIL="tom@orangebeachfish.com"
FB="https://www.facebook.com/orangebeachfishcharterservices/"
ADDR="26619 Perdido Beach Blvd, Orange Beach, AL 36561"
BASE="https://orangebeachfish.webblaze.io"
NAME="Orange Beach Fish Charter Services"

FONTS=('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
'<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')

I={
 'phone':'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 'pin':'<path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
 'check':'<path d="M20 6L9 17l-5-5"/>','clock':'<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 'users':'<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/>',
 'award':'<path d="M12 15a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM8.2 13.3 7 22l5-3 5 3-1.2-8.7"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'chat':'<path d="M21 11.5a8.38 8.38 0 0 1-8.5 8.5 8.5 8.5 0 0 1-3.9-.9L3 20l1.1-3.3A8.4 8.4 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5z"/>',
 'fish':'<path d="M3 12c3-4 8-6 12-6 2.5 0 4.5.6 6 1.7-1 1.5-1 3 0 4.6C19.5 17.4 17.5 18 15 18c-4 0-9-2-12-6z"/><path d="M21 12c1-1 2-1 2-1s-1 0-2-1M6 11h.01"/>',
 'waves':'<path d="M2 8c2 0 2 2 4 2s2-2 4-2 2 2 4 2 2-2 4-2 2 2 4 2M2 14c2 0 2 2 4 2s2-2 4-2 2 2 4 2 2-2 4-2 2 2 4 2"/>',
 'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.4 1.4M17.6 17.6 19 19M19 5l-1.4 1.4M6.4 17.6 5 19"/>',
 'cal':'<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/>',
 'cash':'<path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
 'anchor':'<circle cx="12" cy="5" r="2.5"/><path d="M12 8v13M5 13a7 7 0 0 0 14 0M4 13h3M17 13h3"/>',
}
def ic(k): return f'<svg class="ico" viewBox="0 0 24 24">{I[k]}</svg>'

MARK=('<svg class="mark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#08293A"/>'
 '<circle cx="24" cy="19" r="7" fill="#FF6A3B"/>'
 '<path d="M9 29c3 0 3 2 6 2s3-2 6-2 3 2 6 2 3-2 6-2" stroke="#F2A93B" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
 '<path d="M9 35c3 0 3 2 6 2s3-2 6-2 3 2 6 2 3-2 6-2" stroke="#7FD4C7" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg>')

SPECIES=["Red Snapper","Amberjack","Tuna","King Mackerel","Triggerfish","Speckled Trout","Redfish","Shark"]

def img(name): return f"img/{name}.jpg?v={V}"

def head(title,desc,canon):
    return ('<!DOCTYPE html><html lang="en"><head><script>document.documentElement.classList.add("js");</script>'
     '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
     f'<title>{title}</title><meta name="description" content="{desc}">'
     '<link rel="icon" href="favicon.svg" type="image/svg+xml">'
     f'{FONTS}<link rel="stylesheet" href="styles.css?v={V}">'
     f'<link rel="canonical" href="{canon}">'
     '<meta name="robots" content="noindex,follow"><!-- PREVIEW: flip to index,follow on the live domain -->'
     '<meta property="og:type" content="website">'
     f'<meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{title}">'
     f'<meta property="og:description" content="{desc}"><meta property="og:url" content="{canon}">'
     f'<meta property="og:image" content="{BASE}/{img("hero")}"><meta name="twitter:card" content="summary_large_image">'
     '</head><body>')

def util():
    return (f'<div class="util"><div class="wrap util-in"><div class="util-l">'
     f'<a href="tel:{TEL}">{ic("phone")}{TN}</a><a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a></div>'
     f'<a href="book.html">{ic("pin")}Orange Beach, Alabama</a></div></div>')

def nav(active):
    L=[("Home","index.html"),("Trips","trips.html"),("Gallery","gallery.html"),("Book","book.html")]
    items="".join(f'<a href="{h}"{" class=\"on\"" if n==active else ""}>{n}</a>' for n,h in L)
    return ('<nav class="nav"><div class="wrap nav-in">'
     f'<a class="brand" href="index.html">{MARK}<span><span class="bt">Orange Beach Fish</span><span class="bs">Charter Co. · Est. 1980</span></span></a>'
     f'<div class="nav-links">{items}</div>'
     f'<a class="btn btn-coral" href="book.html">Book a trip</a>'
     '<button class="nav-toggle" aria-label="Menu" aria-expanded="false"><svg viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>'
     '</div></nav>')

def footer():
    return ('<footer><div class="wrap"><div class="foot-grid">'
     f'<div class="foot-brand"><span class="serif">{NAME}</span>'
     '<p>Family-owned inshore, offshore &amp; deep sea fishing charters serving Orange Beach, Gulf Shores &amp; Perdido Key since 1980.</p></div>'
     '<div><h4>Trips</h4><a href="trips.html">Inshore fishing</a><br><a href="trips.html">Offshore &amp; deep sea</a><br>'
     '<a href="trips.html">Family fun cruises</a><br><a href="gallery.html">Gallery</a></div>'
     f'<div><h4>Contact &amp; Book</h4><a href="tel:{TEL}">{TN}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br>'
     f'<a href="{FB}" target="_blank" rel="noopener">Message us on Facebook</a><br><span style="color:var(--on-sea-soft)">{ADDR}</span></div>'
     f'</div><div class="compliance"><span>© {NAME} · {ADDR}</span><span>Family fun fishing since 1980</span></div></div></footer>'
     f'<div class="ribbon"><b>PREVIEW</b> — redesign concept built by WebBlaze for {NAME} · not the live site</div>'
     '<script>document.querySelectorAll(".nav-toggle").forEach(function(t){t.addEventListener("click",function(){var n=t.closest(".nav").querySelector(".nav-links");var o=n.classList.toggle("open");t.setAttribute("aria-expanded",o);});});'
     'const els=document.querySelectorAll(".reveal");if(matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver"in window)){els.forEach(e=>e.classList.add("in"));}'
     'else{const io=new IntersectionObserver(en=>en.forEach(e=>{if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}}),{threshold:.12});els.forEach(e=>io.observe(e));}</script></body></html>')

def sec(inner,cls="",sid=""):
    return f'<section class="{cls}"{" id="+chr(34)+sid+chr(34) if sid else ""}><div class="wrap">{inner}</div></section>'
def hb(e,t,l="",center=False):
    cc=" center" if center else ""
    return (f'<div class="sec-head{cc} reveal"><p class="eyebrow">{e}</p><h2 class="sec-title">{t}</h2>'
     +(f'<p class="lead">{l}</p>' if l else '')+'</div>')
def pagehero(e,t,l,bg):
    return (f'<header class="pagehero"><div class="bg" style="background-image:url(\'{img(bg)}\')"></div><div class="wrap">'
     f'<p class="eyebrow reveal">{e}</p><h1 class="reveal">{t}</h1><p class="reveal">{l}</p></div></header>')
def cta():
    return sec('<div class="cta-in"><div class="reveal"><h2>Ready to get on the fish?</h2>'
     '<p>Tell us your dates and party size — we&apos;ll get right back with availability. Summer books up fast.</p></div>'
     f'<div class="cta-actions reveal"><a class="btn btn-coral btn-xl" href="book.html">Book a trip</a>'
     f'<a class="btn btn-ghost" href="tel:{TEL}" style="background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.4);color:#fff">Call {TN}</a></div></div>',"cta")

def faq(items):
    rows="".join(f'<details class="faq reveal"><summary>{q}<span class="pl">+</span></summary><div class="fa">{a}</div></details>' for q,a in items)
    return f'<div class="faq-list">{rows}</div>'

FAQ_HOME=[
 ("Do I need a fishing license?","No — your license is covered under our charter. Rods, reels, bait and tackle are all included too. Just bring sunscreen and a cooler for your catch."),
 ("Are kids and first-timers welcome?","Absolutely — it&apos;s what we do best. We&apos;re patient with kids and happy to teach, and just as ready to put serious anglers on a trophy."),
 ("What will we catch?","Depending on the season and your trip: red snapper, amberjack, tuna, king mackerel, triggerfish, speckled trout, redfish and more."),
 ("Inshore or offshore — which should I pick?","Inshore is calm, close to shore and great for families and steady action. Offshore &amp; deep sea heads out to the reefs and rigs for the big ones. Not sure? Tell us your group and we&apos;ll help you pick."),
 ("How do I book?",f"Call {TN} (fastest way to lock a date), message us on Facebook, or send the form on our Book page. Summer books up fast, so earlier is better."),
]

# ---------------- HOME ----------------
def trip_card(bg,tag,title,desc):
    return (f'<div class="trip reveal"><div class="ph" style="background-image:url(\'{img(bg)}\')"><span class="tag">{tag}</span></div>'
     f'<div class="body"><h3>{title}</h3><p>{desc}</p><a class="go" href="trips.html">See trip details <span class="ar">&rarr;</span></a></div></div>')
def feat(icon,t,p): return f'<div class="feature reveal"><div class="fi">{ic(icon)}</div><h3>{t}</h3><p>{p}</p></div>'

HOME=(f'<header class="hero"><div class="hero-bg" style="background-image:url(\'{img("hero")}\')"></div>'
 '<div class="wrap hero-in">'
 f'<span class="seal reveal">{ic("award")}Family-owned · Est. 1980</span>'
 '<h1 class="reveal">Gulf Coast fishing, <em>since 1980.</em></h1>'
 '<p class="reveal">Get on the fish with a crew that&apos;s run these waters for 45 years — inshore, offshore and deep sea out of Orange Beach, Alabama. First-timers, kids and serious anglers all welcome. We handle the gear and the know-how.</p>'
 f'<div class="hero-ctas reveal"><a class="btn btn-coral btn-xl" href="book.html">Book a trip</a>'
 f'<a class="hero-call" href="tel:{TEL}">{ic("phone")}or call {TN}</a></div>'
 f'<div class="hero-trust reveal"><span>{ic("check")}Rods, bait &amp; license included</span><span>{ic("users")}Family owned &amp; operated</span><span>{ic("waves")}Kids &amp; first-timers welcome</span></div>'
 '</div><a class="scrolldown" href="#trips">Scroll &#9662;</a></header>'
 '<div class="trust"><div class="wrap trust-in">'
 '<div class="t reveal"><b>1980</b><span>Fishing the Gulf since</span></div>'
 '<div class="t reveal"><b>45+</b><span>Years of local know-how</span></div>'
 '<div class="t reveal"><b>Family</b><span>Owned &amp; operated</span></div>'
 '<div class="t reveal"><b>All ages</b><span>Kids &amp; first-timers</span></div></div></div>'
 +sec(hb("Our Trips","Pick your water.","From calm-bay family mornings to serious blue-water runs — every trip comes with an experienced captain who knows exactly where they&apos;re biting.",True)
   +'<div class="trips-grid">'
   +trip_card("inshore","Great for families","Inshore Fishing","Calm, protected waters close to shore. Perfect for kids, first-timers and anyone who wants steady action without the long ride out.")
   +trip_card("offshore","The full experience","Offshore &amp; Deep Sea","Head out to the reefs and rigs for the big ones — red snapper, amberjack, tuna and more. This is the trip the Gulf is famous for.")
   +trip_card("cruise","Everyone aboard","Family Fun Cruises","Not everything needs a hook. Easy cruises on the Gulf — dolphins, sunsets and the best views in Orange Beach for the whole crew.")
   +'</div>',"sec-sand grain")
 +sec('<div class="split"><div class="split-img reveal" style="background-image:url(\''+img("catch")+'\')"></div>'
   '<div class="reveal">'+hb("The Catch","One of America&apos;s best fisheries.","The Alabama Gulf Coast is famous for a reason. Depending on the season and your trip, here&apos;s what you&apos;ll be going after:")
   +'<div class="chips">'+"".join(f'<span class="chip">{s}</span>' for s in SPECIES)+'</div></div></div>',"")
 +sec(hb("Why book with us","Four decades on the same water.","Two generations of guests have caught their first fish on our decks — and plenty come back every single summer.",True)
   +'<div class="feature-grid">'
   +feat("pin","45 years of local know-how","We know where they&apos;re biting in every season — you spend the day catching, not searching.")
   +feat("check","Everything&apos;s included","Rods, reels, bait, tackle and your license are all on us. Just bring sunscreen and a cooler.")
   +feat("users","Built for families &amp; first-timers","Patient with kids, happy to teach — and just as ready to put serious anglers on a trophy.")
   +feat("anchor","Local, since 1980","Family owned and operated out of Orange Beach, serving Gulf Shores &amp; Perdido Key.")
   +'</div>',"sec-tint")
 +'<section class="band"><div class="bg" style="background-image:url(\''+img("beach")+'\')"></div><div class="wrap reveal">'
   '<p class="eyebrow">Proudly Local</p><h2>Orange Beach, Gulf Shores &amp; Perdido Key.</h2>'
   '<p>We fish the water we grew up on. From a calm morning in the bay to a blue-water run offshore, you&apos;re in the hands of a crew that has called the Alabama Gulf Coast home since 1980.</p>'
   '<a class="btn btn-coral" href="book.html">Check availability</a></div></section>'
 +sec(hb("On the Water","A few days out on the Gulf.","Real trips, real Gulf. Here&apos;s a look at the water you&apos;ll be fishing.",True)
   +'<div class="gallery">'
   +'<div class="big" style="background-image:url(\''+img("gallery1")+'\')"></div>'
   +'<div style="background-image:url(\''+img("gallery3")+'\')"></div>'
   +'<div style="background-image:url(\''+img("gallery2")+'\')"></div>'
   +'<div style="background-image:url(\''+img("gear")+'\')"></div>'
   +'<div style="background-image:url(\''+img("gallery4")+'\')"></div>'
   +'</div><div class="center" style="text-align:center;margin-top:34px"><a class="btn btn-ghost reveal" href="gallery.html">See the full gallery &rarr;</a></div>',"sec-sand")
 +'<section class="band quote"><div class="bg" style="background-image:url(\''+img("offshore")+'\')"></div><div class="wrap reveal">'
   '<div class="qm">&ldquo;</div><blockquote>Family fun fishing, inshore to offshore. That&apos;s been the whole idea since day one.</blockquote>'
   f'<cite>&mdash; {NAME}, Orange Beach, AL</cite></div></section>'
 +sec(hb("Good to know","Questions before you book.","",True)+faq(FAQ_HOME),"")
 +cta())

# ---------------- TRIPS ----------------
def detail(bg,e,title,desc,items,rev=False):
    rc=" rev" if rev else ""
    lis="".join(f'<li>{ic("check")}<div>{x}</div></li>' for x in items)
    return (f'<div class="detail{rc}"><div class="d-img reveal" style="background-image:url(\'{img(bg)}\')"></div>'
     f'<div class="reveal"><p class="eyebrow">{e}</p><h2>{title}</h2><p class="lead" style="margin-top:12px">{desc}</p><ul>{lis}</ul>'
     f'<div style="margin-top:26px"><a class="btn btn-coral" href="book.html">Book this trip</a></div></div></div>')

TRIPS=(pagehero("Our Trips","Pick your water.","Inshore, offshore and family cruises out of Orange Beach — every trip captained by someone who&apos;s fished this coast for decades.","offshore")
 +sec(detail("inshore","Inshore","Inshore Fishing",
     "Calm, protected waters close to shore — the easiest, most relaxed way to get on the fish. Perfect for kids, first-timers and families who want steady action without a long ride out.",
     ["Speckled trout, redfish and more","Calm water — great for kids &amp; new anglers","Shorter runs, steady bites all trip","Rods, reels, bait &amp; license included"])
   +detail("offshore","Offshore &amp; Deep Sea","Offshore &amp; Deep Sea",
     "The trip the Gulf is famous for. We run out to the reefs and rigs where the big ones live — this is where the trophies come from.",
     ["Red snapper, amberjack, tuna, king mackerel","Fish the reefs, wrecks &amp; rigs","Big-game rods, reels &amp; tackle provided","Best for anglers chasing a trophy"],rev=True)
   +detail("cruise","Family Fun Cruises","Family Fun Cruises",
     "Not everything needs a hook. Easy cruises on the Gulf for the whole crew — dolphins, sunsets and the best views in Orange Beach.",
     ["Dolphin &amp; sightseeing cruises","Sunset runs on the Gulf","Perfect for all ages &amp; non-anglers","Relaxed pace, unbeatable views"])
   ,"")
 +sec('<div class="split"><div class="reveal">'+hb("What&apos;s included","Just bring sunscreen and a cooler.","Every charter comes fully rigged. Here&apos;s what&apos;s already taken care of &mdash; and the little you need to bring.")
   +'<ul style="list-style:none;display:flex;flex-direction:column;gap:12px;margin-top:8px">'
   +"".join(f'<li style="display:flex;gap:12px;align-items:flex-start;color:var(--soft)">{ic("check")}<div><b style="color:var(--sea)">{t}</b> &mdash; {d}</div></li>' for t,d in [
      ("Rods, reels &amp; tackle","Quality gear matched to your trip, all set up and ready."),
      ("Bait","Fresh bait for whatever&apos;s biting that day."),
      ("Fishing license","Covered under our charter &mdash; no paperwork for you."),
      ("Local expertise","A captain who knows where the fish are in every season."),
      ("You bring","Sunscreen, a hat, sunglasses, snacks/drinks and a cooler for the catch.")])
   +'</ul></div><div class="split-img reveal" style="background-image:url(\''+img("gear")+'\')"></div></div>',"sec-sand")
 +cta())

# ---------------- GALLERY ----------------
GAL_IMGS=["gallery1","catch","offshore","gallery2","boat","gallery3","beach","gear","gallery4","sunset","hero","gallery5"]
def gal_tiles():
    out=[]
    for i,n in enumerate(GAL_IMGS):
        big=' big' if i==0 else ''
        out.append(f'<div class="{("reveal"+ (" big" if i==0 else "")).strip()}" style="background-image:url(\'{img(n)}\')"></div>')
    return '<div class="gallery">'+''.join(out)+'</div>'

GALLERY=(pagehero("On the Water","Real trips, real Gulf.","A look at the boats, the gear and the water you&apos;ll be fishing on the Alabama Gulf Coast.","gallery1")
 +sec(gal_tiles(),"sec-sand")
 +cta())

# ---------------- BOOK ----------------
opts=["Inshore fishing","Offshore / deep sea","Family fun cruise","Not sure yet — help me pick"]
BOOK=(pagehero("Book","Let&apos;s get you on the calendar.","Call, message us on Facebook, or send the form and we&apos;ll get right back to you with availability. Summer books up fast, so earlier is better.","sunset")
 +'<section class="book"><div class="wrap"><div class="book-grid"><div class="reveal">'
   +f'<div class="contact-photo" style="background-image:url(\'{img("boat")}\')"></div>'
   +f'<div class="loc">{ic("phone")}<div><b>Call to book</b><a href="tel:{TEL}">{TN}</a><br><span>Fastest way to lock a date</span></div></div>'
   +f'<div class="loc">{ic("mail")}<div><b>Email your dates</b><a href="mailto:{EMAIL}">{EMAIL}</a><br><span>Send party size &amp; preferred dates</span></div></div>'
   +f'<div class="loc">{ic("chat")}<div><b>Message on Facebook</b><a href="{FB}" target="_blank" rel="noopener">Quick questions &amp; availability</a></div></div>'
   +f'<div class="loc">{ic("pin")}<div><b>Where we run</b><span>{ADDR}<br>Serving Orange Beach, Gulf Shores &amp; Perdido Key</span></div></div>'
   +f'<div class="loc">{ic("clock")}<div><b>Season</b><span>Call for current availability &mdash; summer books up fast</span></div></div>'
   +'</div>'
   +'<form class="cform reveal" onsubmit="event.preventDefault();var b=this.querySelector(\'button\');b.textContent=\'\\u2713 Sent — we\\\'ll be in touch shortly\';b.disabled=true;">'
   +'<div class="form-h">Request availability</div><div class="form-sub">No deposit to ask — we&apos;ll confirm your dates first.</div>'
   +'<div class="row"><div><label for="n">Name</label><input id="n" type="text" autocomplete="name" placeholder="Your name" required></div>'
   +'<div><label for="p">Phone</label><input id="p" type="tel" autocomplete="tel" placeholder="(251) 000-0000" required></div></div>'
   +'<label for="t">Trip type</label><select id="t">'+"".join(f'<option>{o}</option>' for o in opts)+'</select>'
   +'<label for="m">Dates &amp; party size</label><textarea id="m" placeholder="e.g. July 12–15, party of 4, 2 kids"></textarea>'
   +'<button class="btn btn-coral" type="submit">Request availability</button>'
   +f'<p class="fine">Prefer to talk? Call {TN} or message us on Facebook.</p></form>'
   +'</div></div></section>')

PAGES={
 "index.html":("Orange Beach Fish Charter Services — Gulf Coast Fishing Since 1980",
   "Family-owned fishing charters out of Orange Beach, AL since 1980. Inshore, offshore & deep sea trips — red snapper, tuna, amberjack and more. Rods, bait & license included. Call to book.","Home",HOME),
 "trips.html":("Fishing Trips — Inshore, Offshore & Deep Sea | Orange Beach Fish Charter",
   "Inshore, offshore & deep sea fishing charters and family cruises out of Orange Beach, AL. Everything included — rods, reels, bait, tackle and license. Book your trip.","Trips",TRIPS),
 "gallery.html":("Gallery — On the Water | Orange Beach Fish Charter Services",
   "The boats, the gear and the Gulf water you'll be fishing with Orange Beach Fish Charter Services — family fishing charters since 1980.","Gallery",GALLERY),
 "book.html":("Book a Trip | Orange Beach Fish Charter Services — Orange Beach, AL",
   "Book an inshore, offshore or family fishing trip out of Orange Beach, AL. Call (251) 979-2682, message on Facebook, or request availability online.","Book",BOOK),
}

JSONLD=('<script type="application/ld+json">{"@context":"https://schema.org","@type":"LocalBusiness",'
 f'"name":"{NAME}","url":"{BASE}","telephone":"{TEL}","email":"{EMAIL}","foundingDate":"1980","priceRange":"$$",'
 '"image":"'+BASE+'/'+img("hero")+'","description":"Family-owned inshore, offshore and deep sea fishing charters out of Orange Beach, Alabama since 1980.",'
 '"address":{"@type":"PostalAddress","streetAddress":"26619 Perdido Beach Blvd","addressLocality":"Orange Beach","addressRegion":"AL","postalCode":"36561","addressCountry":"US"},'
 f'"areaServed":["Orange Beach","Gulf Shores","Perdido Key"],"sameAs":["{FB}"]}}</script>')

for fn,(title,desc,active,body) in PAGES.items():
    canon=f"{BASE}/" if fn=="index.html" else f"{BASE}/{fn}"
    extra=JSONLD if fn=="index.html" else ""
    html=head(title,desc,canon).replace("</head>",extra+"</head>")+util()+nav(active)+body+footer()
    (B/fn).write_text(html); print(fn,len(html))

# favicon
(B/"favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><circle cx="24" cy="24" r="24" fill="#08293A"/><circle cx="24" cy="19" r="7" fill="#FF6A3B"/><path d="M9 29c3 0 3 2 6 2s3-2 6-2 3 2 6 2 3-2 6-2" stroke="#F2A93B" stroke-width="2.2" fill="none" stroke-linecap="round"/><path d="M9 35c3 0 3 2 6 2s3-2 6-2 3 2 6 2 3-2 6-2" stroke="#7FD4C7" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg>')
# sitemap + robots
urls="".join(f'  <url><loc>{BASE}/{"" if f=="index.html" else f}</loc><changefreq>monthly</changefreq><priority>{"1.0" if f=="index.html" else "0.8"}</priority></url>\n' for f in PAGES)
(B/"sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
(B/"robots.txt").write_text(f"User-agent: *\nDisallow:\n\nSitemap: {BASE}/sitemap.xml\n")
print("favicon + sitemap + robots written")
