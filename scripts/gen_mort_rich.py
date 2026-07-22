import pathlib, html
FONTS=('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
'<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">')
FAV=('<link rel="icon" href="img/favicon-32.png" sizes="32x32" type="image/png"><link rel="icon" href="img/favicon-192.png" sizes="192x192" type="image/png"><link rel="apple-touch-icon" href="img/favicon-192.png">')
I={'phone':'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 'pin':'<path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>','check':'<path d="M20 6L9 17l-5-5"/>',
 'shield':'<path d="M9 12l2 2 4-4M12 3l7 4v5c0 5-3.5 8-7 9-3.5-1-7-4-7-9V7z"/>','users':'<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/>',
 'clock':'<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>','award':'<path d="M12 15a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM8.2 13.3 7 22l5-3 5 3-1.2-8.7"/>',
 'bank':'<path d="M3 21h18M3 10h18M5 21V10M19 21V10M9 21V10M15 21V10M12 3 3 8h18z"/>','home':'<path d="M3 11l9-8 9 8M5 10v10h14V10M9 20v-6h6v6"/>'}
def ic(k): return f'<svg class="ico" viewBox="0 0 24 24">{I[k]}</svg>'
EHL=('<svg viewBox="0 0 48 48" aria-label="Equal Housing Lender"><rect width="48" height="48" rx="6" fill="none" stroke="rgba(255,255,255,.4)" stroke-width="1.4"/>'
 '<path d="M24 11l13 9v2h-3v14H14V22h-3v-2z" fill="none" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/>'
 '<path d="M19 41v-8h10v8" fill="none" stroke="#fff" stroke-width="1.5"/><path d="M17 27h5M26 27h5M17 31h5M26 31h5" stroke="#fff" stroke-width="1.3" stroke-linecap="round"/></svg>')

TEL="+15048373939"; TN="(504) 837-3939"; NAME="Sun Mortgage Funding"
B=pathlib.Path("/Users/zaydenzukerman/webblaze/public/sunmortgagefunding")
OTHERS=[("Sun Premium Financing","https://sunpremium.webblaze.io"),("Sun Finance · Personal Loans","https://sunfinance.webblaze.io")]

def head(t,d): return (f'<!DOCTYPE html><html lang="en"><head><script>document.documentElement.classList.add("js");</script>'
 f'<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{t}</title>'
 f'<meta name="description" content="{d}">{FAV}{FONTS}<link rel="stylesheet" href="styles.css"></head><body>')
UTIL=(f'<div class="util"><div class="wrap util-in"><div class="util-l"><a href="tel:{TEL}">{ic("phone")}Mortgage {TN}</a></div>'
 f'<a href="contact.html">{ic("pin")}Metairie, Louisiana</a></div></div>')
def nav(active):
    L=[("Home","index.html"),("Loan Programs","programs.html"),("About","about.html"),("Contact","contact.html")]
    items="".join(f'<a href="{h}"{" style=\"color:var(--navy);font-weight:600\"" if n==active else ""}>{n}</a>' for n,h in L)
    return ('<nav class="nav"><div class="wrap nav-in"><a class="brand" href="index.html" aria-label="Sun Mortgage Funding">'
     '<img src="img/sun-logo.svg" alt="Sun" width="297" height="61"><span class="tag">Mortgage<br>Funding</span></a>'
     f'<div class="nav-links">{items}</div><a class="btn btn-gold" href="contact.html" style="padding:11px 22px">Apply Now</a></div></nav>')
OTH="<br>".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n,u in OTHERS)
FOOTER=('<footer><div class="wrap"><div class="foot-grid">'
 '<div class="foot-brand"><span class="serif">Sun Mortgage Funding</span><p style="margin-top:12px;max-width:42ch">A locally owned and operated mortgage lender serving Metairie, Louisiana since 1958 — home purchase, refinancing and renovation. One of the Sun companies.</p></div>'
 f'<div><h4>The Sun Companies</h4>{OTH}</div>'
 f'<div><h4>Company</h4><a href="programs.html">Loan Programs</a><br><a href="about.html">Our Story</a><br><a href="contact.html">Contact &amp; Apply</a><br><a href="tel:{TEL}">{TN}</a></div></div>'
 '<div class="compliance"><div class="ehl"><span>All loans subject to credit approval. Sun Mortgage Funding, Inc. — NMLS #71517. BBB A+ accredited since 1996. <span class="ph">[Final state/licensing disclosures confirmed with client before launch.]</span></span></div>'
 '<span>© Sun Mortgage Funding, Inc. · Metairie, Louisiana · BBB A+ Accredited</span></div></div></footer>'
 '<div class="ribbon"><b>PREVIEW</b> — redesign concept built by WebBlaze for Sun Mortgage Funding · not the live site</div>'
 '<script>const els=document.querySelectorAll(".reveal");if(matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver"in window)){els.forEach(e=>e.classList.add("in"));}else{const io=new IntersectionObserver(en=>en.forEach(e=>{if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}}),{threshold:.1});els.forEach(e=>io.observe(e));}'
 'document.addEventListener("click",function(e){var a=e.target.closest("a[href^=\\"#\\"]");if(!a)return;var h=a.getAttribute("href");if(!h||h.length<2)return;var el=document.getElementById(h.slice(1));if(!el)return;e.preventDefault();el.classList.add("in");var y=el.getBoundingClientRect().top+window.scrollY-96;window.scrollTo({top:y,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});history.replaceState(null,"",h);});</script></body></html>')

def hb(e,t='',l='',center=True):
    cc=" center" if center else ""
    return f'<div class="sec-head{cc} reveal"><p class="eyebrow">{e}</p><h2 class="sec-title">{t}</h2>'+(f'<p class="lead">{l}</p>' if l else '')+'</div>'
def sec(inner,cls="",sid=""): return f'<section class="{cls}"{" id="+chr(34)+sid+chr(34) if sid else ""}><div class="wrap">{inner}</div></section>'
def feat(icon,t,p): return f'<div class="feature reveal"><div class="fi">{ic(icon)}</div><h3>{t}</h3><p>{p}</p></div>'
def prog(n,t,d): return f'<div class="prog reveal"><span class="n">{n}</span><div><h4>{t}</h4><p>{d}</p></div></div>'
def faq(q,a): return f'<details class="faq reveal"><summary>{q}<span class="pl">+</span></summary><div class="fa">{a}</div></details>'
def pagehero(e,t,l,img): return (f'<header class="pagehero" id="top"><div class="ph-bg" style="background-image:url(\'img/{img}\')"></div>'
    f'<div class="wrap"><p class="eyebrow reveal">{e}</p><h1 class="reveal">{t}</h1>'+(f'<p class="reveal">{l}</p>' if l else '')+'</div></header>')
def initials(n): return "".join(w[0] for w in n.split()[:2]).upper()
def teamcard(name,role,meta): return f'<div class="tm reveal"><div class="av">{initials(name)}</div><h4>{name}</h4>'+(f'<div class="role">{role}</div>' if role else '')+f'<div class="meta">{meta}</div></div>'
TEAM=('<div class="team-grid">'
 +teamcard('David Daube','President','43 years in finance · 28 as President')
 +teamcard('Brian Daube','Vice President','15 years in finance')
 +teamcard('Annette Hesse','Licensed Loan Originator','NMLS #90346 · 40 years in finance')
 +teamcard('Tammie Cavanagh','Licensed Loan Originator','NMLS #164425 · 40 years in finance')+'</div>')
def cta(h,p): return sec(f'<div class="cta-in"><div class="reveal"><h2>{h}</h2><p>{p}</p></div><div class="cta-actions reveal"><a class="btn btn-gold" href="contact.html">Apply now</a><a class="btn btn-ghost" href="tel:{TEL}">Call {TN}</a></div></div>',"cta")

def page(t,d,active,main): return head(t,d)+UTIL+nav(active)+main+FOOTER

WHY=('<div class="feature-grid">'
 +feat('bank','More programs than a bank','More loan programs than a traditional bank lets us structure a loan around your situation — not force your situation into a box.')
 +feat('users','Real people, local decisions','Your file is handled by a local team in Metairie you can actually reach — not an out-of-state call center.')
 +feat('shield','We say yes more often','Credit issues, bankruptcy, past foreclosure — we specialize in the scenarios big banks turn away.')+'</div>')

PROGS4=('<div class="progs">'
 +prog('01','New Home Purchase','Whether you&apos;re a first-time buyer or moving up, we finance your dream home on realistic terms — working alongside your real estate agent or helping you start from scratch.')
 +prog('02','Mortgage Refinancing','Lower your rate, shorten your term, or pull equity from your primary or investment property for debt consolidation and bigger goals.')
 +prog('03','Home Renovation Loans','Remodel, repair or improve your home with interim and permanent financing rolled into one — including project planning and inspection guidance.')
 +prog('04','Investment &amp; Commercial','We finance investment and commercial property too — not just homes — with the same local, in-house approach.')+'</div>')

STEPS=('<div class="progs">'
 +prog('01','Talk to a local lender','A quick, no-pressure conversation about your goals, your timeline and your numbers.')
 +prog('02','Get matched to a program','We line up the right loan from our range of programs and tell you exactly what to expect — rate, terms, costs.')
 +prog('03','Submit &amp; get a real answer','We review locally and give you a straight answer fast, with a clear list of anything we need.')
 +prog('04','Close &amp; keep your lender','Close with people who know your name — and who still service the loan afterward.')+'</div>')

REVIEWS=('<div class="review-grid">'
 '<div class="review reveal"><div class="stars">★★★★★</div><p>Clients highlight smooth refinances and home purchases — and being treated like a person, not a file number.</p><div class="who">5.0★ rated <span>· client reviews</span></div></div>'
 '<div class="review reveal"><div class="stars">★★★★★</div><p>Loan originator Annette Hesse — with Sun Mortgage Funding since 2004 — is praised by name for guiding buyers through the process.</p><div class="who">Client feedback <span>· Metairie, LA</span></div></div>'
 '<div class="review reveal"><div class="stars">★★★★★</div><p>Accredited by the Better Business Bureau with an A+ rating since 1996 — a record of doing right by Louisiana homeowners.</p><div class="who">BBB A+ <span>· since 1996</span></div></div></div>')

HERO=('<header class="hero photo"><div class="hero-bg" style="background-image:url(\'img/hero.jpg\')"></div>'
 '<div class="wrap hero-in"><div class="hero-copy">'
 f'<span class="seal reveal">{ic("award")}Serving Louisiana since 1958</span>'
 '<h1 class="reveal">From your first home to your <em>next chapter.</em></h1>'
 '<p class="reveal">Louisiana&apos;s locally owned and operated mortgage lender, serving Metairie since 1958 — home purchases, refinancing, renovation and more, with more loan programs than a traditional bank and real, local people making the decisions.</p>'
 f'<div class="hero-ctas reveal"><a class="btn btn-gold btn-xl" href="contact.html">Apply now</a><a class="hero-call" href="tel:{TEL}">{ic("phone")}or call {TN}</a></div>'
 f'<div class="hero-trustline reveal"><span>{ic("home")}More programs than a bank</span><span>{ic("check")}NMLS #71517</span><span>{ic("award")}BBB A+ · accredited 1996</span></div>'
 '</div></div><a class="scrolldown" href="#more">Scroll ▾</a></header>')

TRUST=('<div class="trust" id="more"><div class="wrap trust-in">'
 '<div class="t reveal"><b>1958</b><span>Serving Louisiana since</span></div>'
 '<div class="t reveal"><b>50+</b><span>Years of experience</span></div>'
 '<div class="t reveal"><b>A+</b><span>BBB rating · since 1996</span></div>'
 '<div class="t reveal"><b>Local</b><span>Metairie, Louisiana</span></div></div></div>')

IMGSPLIT=sec('<div class="imgsplit-in"><div class="ip-img reveal" style="background-image:url(\'img/accent.jpg\')"></div>'
 '<div class="reveal"><p class="eyebrow">Why families choose us</p><h2>Keys in hand — and a lender who stays.</h2>'
 '<p class="lead">A local team you can actually reach — the same people from your first call through closing, not a national call center. That&apos;s the difference a locally owned lender makes.</p>'
 '<a class="btn btn-gold" href="contact.html">Apply now</a></div></div>',"imgsplit")

LOCALBAND=sec('<div class="lb-bg" style="background-image:url(\'img/city.jpg\')"></div>'
 '<p class="eyebrow reveal">Proudly Local</p><h2 class="reveal">Rooted in Greater New Orleans since 1958.</h2>'
 '<p class="reveal">From Metairie across Greater New Orleans, Sun Mortgage Funding has helped Louisiana homeowners finance their homes since 1958 — with decisions made by real people right here at home.</p>'
 '<a class="btn btn-gold reveal" href="contact.html">Apply now</a>',"localband")

HERITAGE=sec('<div class="heritage-in"><div class="reveal"><p class="eyebrow">Our Story</p><div class="quote-mark">&ldquo;</div>'
 '<blockquote>A locally owned and operated mortgage company, serving Louisiana since 1958.</blockquote>'
 '<cite>— Sun Mortgage Funding, Metairie, Louisiana</cite>'
 '<div style="margin-top:24px"><a class="btn btn-gold" href="about.html">Our story</a></div></div>'
 f'<div class="h-points reveal"><div class="h-point">{ic("award")}<div><b>Locally owned &amp; operated</b><p>Serving Metairie and the southeast Louisiana community since 1958.</p></div></div>'
 f'<div class="h-point">{ic("shield")}<div><b>NMLS #71517 · BBB A+</b><p>Licensed in Louisiana and BBB-accredited with an A+ rating since 1996.</p></div></div></div></div>',"heritage")

FAQ_HOME=('<div class="faq-list">'
 +faq('What kinds of loans do you offer?','More loan programs than a traditional bank — purchase, refinance, renovation, cash-out and equity, plus investment and commercial property — including credit-challenged and post-foreclosure scenarios.')
 +faq('Can you help if I&apos;ve had credit issues or a foreclosure?','Often, yes — it&apos;s a specialty of ours. Because we review locally, we can consider situations that automated big-bank systems reject outright.')
 +faq('Are you a local company?','Completely. Sun Mortgage Funding is locally owned and operated in Metairie, Louisiana, serving the community since 1958.')
 +faq('How fast can I get an answer?','Fast. A quick conversation gets you matched to a program, and our local review means a real, human answer without weeks of waiting.')+'</div>')

HOME=(HERO+TRUST
 +sec(hb('Why Sun Mortgage Funding','More programs. Local answers.','Big enough to offer more loan programs than a bank, local enough to know your name — a combination the national lenders can&apos;t offer.')+WHY,"sec-glow")
 +IMGSPLIT
 +sec(hb('What We Offer','More ways to get to yes.','More loan programs than a traditional bank — including options for buyers other lenders can&apos;t help. A few of the ones people ask about most.')+PROGS4+'<div class="center" style="margin-top:36px"><a class="btn btn-ghost reveal" href="programs.html">See all loan programs →</a></div>',"sec-tint")
 +LOCALBAND
 +sec(hb('How It Works','A clear path from hello to keys.','No runaround, no mystery. Here&apos;s exactly how getting a loan with us works.')+STEPS,"sec-lines")
 +HERITAGE
 +sec(hb('Trusted Locally','A 5.0-star reputation, earned over decades.','Our clients consistently rate us five stars and single out the people who got them to closing.')+REVIEWS,"sec-tint")
 +sec(hb('Questions','Good to know before you apply.')+FAQ_HOME,"sec-glow")
 +cta('Ready to get started?','Apply in minutes, or call to talk it through with a local lender.'))

CHIPS='<div class="chips reveal">'+''.join(f'<span class="chip">{x}</span>' for x in ['First-time buyers','Move-up buyers','Investors','Self-employed','Credit challenges','Commercial'])+'</div>'
PROGS6=('<div class="progs">'
 +prog('01','New Home Purchase','Whether you&apos;re a first-time buyer or moving up, we finance your dream home on realistic terms — working alongside your real estate agent or helping you start from scratch.')
 +prog('02','Mortgage Refinancing','Lower your rate, shorten your term, or pull equity from your primary or investment property for debt consolidation and bigger goals.')
 +prog('03','Home Renovation Loans','Remodel, repair or improve your home with interim and permanent financing rolled into one — including project planning and inspection guidance.')
 +prog('04','Investment &amp; Commercial Property','Beyond primary homes, we finance investment and commercial properties across Louisiana.')
 +prog('05','Cash-Out &amp; Equity','Pull equity from your primary or investment property for debt consolidation and other goals, or flexible cash financing.')
 +prog('06','Credit &amp; Foreclosure Solutions','Had credit trouble, a bankruptcy, or a foreclosure? We specialize in paths forward that big banks won&apos;t consider — real people reviewing your real story.')+'</div>')
PROCESS_BAND=sec(hb('The Process','How a loan comes together.','Every program follows the same straightforward path — and a real person walks it with you.')+STEPS,"band-navy")
FAQ_PROG=('<div class="faq-list">'
 +faq('Which program is right for me?','A quick call is the fastest way to find out — we&apos;ll match your goals, timeline and numbers to the right program, with no pressure.')
 +faq('Do you finance investment and commercial property?','Yes. Alongside primary homes we finance investment and commercial properties across Louisiana.')
 +faq('What makes renovation loans different?','They roll the remodel and permanent financing together, with guidance along the way — so you&apos;re not juggling two separate loans.')+'</div>')
PROGRAMS=(pagehero('Loan Programs','More ways to get to yes.','More loan programs than a traditional bank — including options for buyers other lenders can&apos;t help. Here are the ones people ask about most.','prod.jpg')
 +sec(CHIPS+PROGS6,"sec-glow")
 +PROCESS_BAND
 +sec(hb('Program Questions')+FAQ_PROG,"sec-tint")
 +cta('Not sure which fits?','Call a local lender and we&apos;ll help you find the right program — no pressure.'))

TIMELINE=('<div class="progs">'
 +prog('1958','Serving Louisiana since 1958','The Sun companies have served Metairie and southeast Louisiana since 1958.')
 +prog('1996','BBB A+ accreditation','Accredited by the Better Business Bureau with an A+ rating — a standard held ever since.')
 +prog('Today','Locally run, in Metairie','Led by president David Daube, with a local team you can actually reach.')+'</div>')
VALUES=('<div class="feature-grid">'
 +feat('users','People over paperwork','Real conversations and real decisions, made by a local team you can reach by name.')
 +feat('bank','More ways to yes','More loan programs than a bank, with local review, mean we can say yes where big banks say no.')
 +feat('award','Here for the long run','An established, locally owned lender that will be here tomorrow.')+'</div>')
ABOUT=(pagehero('Our Story','Locally owned and operated in Louisiana.','A locally owned and operated mortgage lender serving Metairie and southeast Louisiana since 1958, led by president David Daube.','about.jpg')
 +sec('<div class="heritage-in"><div class="reveal"><div class="quote-mark">&ldquo;</div>'
   '<blockquote>A locally owned and operated mortgage company, serving Louisiana since 1958.</blockquote><cite>— Sun Mortgage Funding</cite></div>'
   f'<div class="h-points reveal"><div class="h-point">{ic("award")}<div><b>Serving Louisiana since 1958</b><p>A local mortgage lender rooted in the Metairie community.</p></div></div>'
   f'<div class="h-point">{ic("shield")}<div><b>NMLS #71517 · BBB A+ since 1996</b><p>Licensed in Louisiana and BBB-accredited with an A+ rating.</p></div></div>'
   f'<div class="h-point">{ic("users")}<div><b>Local decisions</b><p>Handled by a local team in Metairie, Louisiana — over 50 years of combined experience.</p></div></div></div></div>',"heritage")
 +sec(hb('Our History','Serving Louisiana since 1958.')+TIMELINE,"sec-lines")
 +sec(hb('What We Stand For','The way we&apos;ve always done business.')+VALUES,"sec-glow")
 +sec(hb('Meet the Team','The people behind Sun Mortgage Funding.','Real, local people you&apos;ll actually work with — with decades of mortgage experience right here in Metairie.')+TEAM)
 +sec('<div class="trust-in"><div class="t reveal"><b>1958</b><span>Serving Louisiana since</span></div><div class="t reveal"><b>1996</b><span>BBB accredited since</span></div><div class="t reveal"><b>A+</b><span>BBB rating</span></div><div class="t reveal"><b>Local</b><span>Metairie, LA</span></div></div>',"sec-tint")
 +cta('Ready to get started?','Apply in minutes, or call to talk it through with a local lender.'))

CFORM=('<form class="cform reveal" onsubmit="event.preventDefault();var b=this.querySelector(\'button\');b.textContent=\'✓ Received — we\\\'ll be in touch shortly\';b.disabled=true;">'
 '<div class="row"><div><label for="n">Full name</label><input id="n" type="text" autocomplete="name" placeholder="Your name" required></div>'
 '<div><label for="p">Phone</label><input id="p" type="tel" autocomplete="tel" placeholder="(504) 000-0000" required></div></div>'
 '<label for="t">What are you looking for?</label><select id="t"><option>New home purchase</option><option>Refinance</option><option>Renovation / construction</option><option>Cash-out / cash financing</option><option>Credit or foreclosure help</option><option>Not sure — help me decide</option></select>'
 '<label for="m">Tell us a little about your situation</label><textarea id="m"></textarea>'
 '<button class="btn btn-gold" type="submit">Request a call back</button></form>')
CONTACT=(pagehero('Contact &amp; Apply','Let&apos;s talk.','Apply, call, or send a note — a real, local lender will get back to you fast.','loc.jpg')
 +sec(hb('Getting Started','Three steps, one local team.')+'<div class="progs">'
   +prog('01','Reach out','Call, or send the form below — whatever&apos;s easiest.')
   +prog('02','Talk it through','A local lender reviews your goals and lays out your loan options.')
   +prog('03','Get a real answer','Reviewed locally, with a fast, straightforward next step.')+'</div>',"sec-lines")
 +sec('<div class="contact-grid"><div class="reveal">'
   f'<div class="loc">{ic("pin")}<div><b>Main Office</b><span>3525 N. Causeway Blvd, Suite 900<br>Metairie, LA 70002</span></div></div>'
   f'<div class="loc">{ic("phone")}<div><b>Call Us</b><a href="tel:{TEL}">{TN}</a><br><span>NMLS #71517 · BBB A+</span></div></div>'
   f'<div class="loc">{ic("clock")}<div><b>Hours</b><span>Call us for current office hours.</span></div></div></div>'
   +CFORM+'</div>',"contact")
 +sec(hb('Before You Reach Out')+'<div class="faq-list">'
   +faq('Does applying affect my credit?','We&apos;ll always tell you before any step that involves a credit check — no surprises.')
   +faq('What do I need to get started?','Just a conversation. We&apos;ll tell you exactly what documents help once we know your goals.')+'</div>',"sec-glow"))

PAGES={
 "index.html":("Sun Mortgage Funding — Louisiana Home Loans Since 1958 | NMLS #71517","Locally owned and operated mortgage lender in Metairie, Louisiana since 1958. Purchase, refinance, renovation, cash-out, investment and commercial — more programs than a bank. NMLS #71517.","Home",HOME),
 "programs.html":("Loan Programs — Sun Mortgage Funding | Louisiana","More loan programs than a traditional bank: purchase, refinance, renovation, cash-out and equity, investment and commercial, plus credit and foreclosure solutions.","Loan Programs",PROGRAMS),
 "about.html":("About Sun Mortgage Funding — Serving Louisiana Since 1958","Locally owned and operated in Metairie, Louisiana since 1958. NMLS #71517, BBB A+ accredited since 1996. Led by president David Daube.","About",ABOUT),
 "contact.html":("Contact &amp; Apply — Sun Mortgage Funding | Metairie, LA","Apply for a Louisiana home loan or call (504) 837-3939. Locally owned in Metairie since 1958.","Contact",CONTACT),
}
for fn,(t,d,a,m) in PAGES.items():
    (B/fn).write_text(page(t,d,a,m)); print("sunmortgagefunding",fn,len((B/fn).read_text()))
