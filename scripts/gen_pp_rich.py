import pathlib
FONTS=('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
'<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">')
FAV=('<link rel="icon" href="img/favicon-32.png" sizes="32x32" type="image/png"><link rel="icon" href="img/favicon-192.png" sizes="192x192" type="image/png"><link rel="apple-touch-icon" href="img/favicon-192.png">')
I={'phone':'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 'pin':'<path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>','check':'<path d="M20 6L9 17l-5-5"/>',
 'shield':'<path d="M9 12l2 2 4-4M12 3l7 4v5c0 5-3.5 8-7 9-3.5-1-7-4-7-9V7z"/>','users':'<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/>',
 'clock':'<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>','award':'<path d="M12 15a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM8.2 13.3 7 22l5-3 5 3-1.2-8.7"/>',
 'cash':'<path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>','doc':'<path d="M2 7h20v10H2zM2 11h20M6 15h4"/>','bolt':'<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>','wallet':'<path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6M12 3v18"/>'}
def ic(k): return f'<svg class="ico" viewBox="0 0 24 24">{I[k]}</svg>'

def build(c):
    B=pathlib.Path(c["dir"]); tel=c["tel"]; tn=c["telnum"]
    def head(t,d): return (f'<!DOCTYPE html><html lang="en"><head><script>document.documentElement.classList.add("js");</script>'
     f'<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{t}</title>'
     f'<meta name="description" content="{d}">{FAV}{FONTS}<link rel="stylesheet" href="styles.css"></head><body>')
    util=(f'<div class="util"><div class="wrap util-in"><div class="util-l"><a href="tel:{tel}">{ic("phone")}{c["label"]} {tn}</a>'
     + "".join(f'<a href="{u}" target="_blank" rel="noopener">{ic(icn)}{lbl}</a>' for lbl,icn,u in c.get("utillinks",[]))
     + f'</div><a href="about.html">{ic("pin")}Metairie, Louisiana</a></div></div>')
    def nav(a):
        L=[("Home","index.html"),("How It Works","how-it-works.html"),("About","about.html"),("Apply","apply.html")]
        items="".join(f'<a href="{h}"{" style=\"color:var(--navy);font-weight:600\"" if n==a else ""}>{n}</a>' for n,h in L)
        return ('<nav class="nav"><div class="wrap nav-in"><a class="brand" href="index.html">'
        f'<img src="img/sun-logo.svg" alt="Sun" width="297" height="61"><span class="tag">{c["tag"]}</span></a>'
        f'<div class="nav-links">{items}</div><a class="btn btn-gold" href="apply.html" style="padding:11px 22px">{c["apply"]}</a>'
        '<button class="nav-toggle" aria-label="Menu" aria-expanded="false"><svg viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button></div></nav>')
    others="<br>".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n,u in c["others"])
    footer=('<footer><div class="wrap"><div class="foot-grid">'
     f'<div class="foot-brand"><span class="serif">{c["name"]}</span><p style="margin-top:12px;max-width:42ch">{c["footdesc"]}</p></div>'
     f'<div><h4>The Sun Companies</h4>{others}</div>'
     f'<div><h4>Company</h4><a href="how-it-works.html">How It Works</a><br><a href="about.html">Our Story</a><br><a href="apply.html">Apply</a>'
     + "".join(f'<br><a href="{u}" target="_blank" rel="noopener">{lbl}</a>' for lbl,icn,u in c.get("utillinks",[]))
     + (f'<br><a href="{c["blog"]}" target="_blank" rel="noopener">Blog</a>' if c.get("blog") else '')
     + f'<br><a href="tel:{tel}">{tn}</a></div></div>'
     f'<div class="compliance"><div class="ehl"><span>{c["compliance"]}</span></div>'
     f'<span>© {c["name"]} · Metairie, Louisiana{c["bbbtag"]}</span></div></div></footer>'
     f'<div class="ribbon"><b>PREVIEW</b> — redesign concept built by WebBlaze for {c["name"]} · not the live site</div>'
     '<script>document.querySelectorAll(".nav-toggle").forEach(function(t){t.addEventListener("click",function(){var n=t.closest(".nav").querySelector(".nav-links");var o=n.classList.toggle("open");t.setAttribute("aria-expanded",o);});});'
     'const els=document.querySelectorAll(".reveal");if(matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver"in window)){els.forEach(e=>e.classList.add("in"));}else{const io=new IntersectionObserver(en=>en.forEach(e=>{if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}}),{threshold:.1});els.forEach(e=>io.observe(e));}'
     'document.addEventListener("click",function(e){var a=e.target.closest("a[href^=\\"#\\"]");if(!a)return;var h=a.getAttribute("href");if(!h||h.length<2)return;var el=document.getElementById(h.slice(1));if(!el)return;e.preventDefault();el.classList.add("in");var y=el.getBoundingClientRect().top+window.scrollY-96;window.scrollTo({top:y,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});history.replaceState(null,"",h);});</script></body></html>')
    def page(t,d,a,m): return head(t,d)+util+nav(a)+m+footer
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
    SEAL='<span class="seal reveal">'+ic("award")+'Serving Louisiana since 1958</span>'
    def cta(h,p): return sec(f'<div class="cta-in"><div class="reveal"><h2>{h}</h2><p>{p}</p></div><div class="cta-actions reveal"><a class="btn btn-gold" href="apply.html">{c["apply"]}</a><a class="btn btn-ghost" href="tel:{tel}">Call {tn}</a></div></div>',"cta")
    cardrows="".join(f'<div class="card-row"><span>{s}</span><b>{v}</b></div>' for s,v in c["card"])
    trust="".join(f'<div class="t reveal"><b>{b}</b><span>{s}</span></div>' for b,s in c["trust"])
    steps_full="".join(prog(f"{i+1:02d}",t,d) for i,(t,d) in enumerate(c["steps"]))
    steps_prev="".join(prog(f"{i+1:02d}",t,d) for i,(t,d) in enumerate(c["steps"][:3]))
    feats="".join(feat(*w) for w in c["why"])
    revs="".join(f'<div class="review reveal"><div class="stars">★★★★★</div><p>{q}</p><div class="who">{w}</div></div>' for q,w in c["reviews"])

    HOME=(f'<header class="hero photo"><div class="hero-bg" style="background-image:url(\'img/hero.jpg\')"></div>'
     '<div class="wrap hero-in"><div class="hero-copy">'+SEAL+
     f'<h1 class="reveal">{c["h1"]}</h1>'
     f'<div class="hero-ctas reveal"><a class="btn btn-gold btn-xl" href="apply.html">{c["apply"]}</a>'
     f'<a class="hero-call" href="tel:{tel}">{ic("phone")}or call {tn}</a></div>'
     f'<div class="hero-trustline reveal"><span>{ic("cash")}{c["herostat"]}</span><span>{ic("check")}Local decisions, in-house</span><span>{ic("shield")}{c["trust3"]}</span></div>'
     '</div></div><a class="scrolldown" href="#more">Scroll ▾</a></header>'
     f'<div class="trust" id="more"><div class="wrap trust-in">{trust}</div></div>'
     +sec(hb('Why '+c["shortname"],c["whyhead"],c["whylead"])+'<div class="feature-grid">'+feats+'</div>',"sec-glow")
     +sec('<div class="imgsplit-in"><div class="ip-img reveal" style="background-image:url(\'img/accent.jpg\')"></div>'
       f'<div class="reveal"><p class="eyebrow">{c["spliteyebrow"]}</p><h2>{c["splithead"]}</h2><p class="lead">{c["splitlead"]}</p>'
       f'<a class="btn btn-gold" href="apply.html">{c["apply"]}</a></div></div>',"imgsplit")
     +sec(hb('How It Works',c["prodtitle"],c["prodlead"])+'<div class="progs">'+steps_prev+'</div><div class="center" style="margin-top:36px"><a class="btn btn-ghost reveal" href="how-it-works.html">See how it works →</a></div>',"sec-lines")
     +sec('<div class="lb-bg" style="background-image:url(\'img/people.jpg\')"></div>'
       f'<p class="eyebrow reveal">Proudly Local</p><h2 class="reveal">Rooted in Greater New Orleans since 1958.</h2>'
       f'<p class="reveal">{c["localp"]}</p><a class="btn btn-gold reveal" href="apply.html">{c["apply"]}</a>',"localband")
     +sec('<div class="heritage-in"><div class="reveal"><p class="eyebrow">Our Story</p><div class="quote-mark">&ldquo;</div>'
       f'<blockquote>Locally owned and operated in Louisiana since 1958.</blockquote><cite>— {c["name"]}, Metairie, Louisiana</cite>'
       '<div style="margin-top:24px"><a class="btn btn-gold" href="about.html">Our story</a></div></div>'
       f'<div class="h-points reveal"><div class="h-point">{ic("award")}<div><b>Locally owned &amp; operated</b><p>One of the Sun companies, serving Metairie and Louisiana since 1958.</p></div></div>'
       f'<div class="h-point">{ic("users")}<div><b>Real people, local service</b><p>Handled by a local team you can actually reach.</p></div></div></div></div>',"heritage")
     +sec(hb('Trusted Locally','Serving Louisiana since 1958.','One of the Sun companies, serving Metairie and Greater New Orleans.')+'<div class="review-grid">'+revs+'</div>',"sec-tint")
     +sec(hb('Questions','Good to know.')+'<div class="faq-list">'+"".join(faq(q,a) for q,a in c["faq_home"])+'</div>',"sec-glow")
     +cta(c["ctah"],c["ctap"]))

    PROD=(pagehero('How It Works',c["prodtitle"],c["prodlead"],'prod.jpg')
     +sec('<div class="progs">'+steps_full+'</div>',"sec-lines")
     +sec(hb('Why '+c["shortname"],c["whyhead"])+'<div class="feature-grid">'+feats+'</div>',"band-navy")
     +sec(hb('Questions')+'<div class="faq-list">'+"".join(faq(q,a) for q,a in c["faq_prod"])+'</div>',"sec-glow")
     +cta(c["ctah"],c["ctap"]))

    tl="".join(f'<div class="prog reveal"><span class="n">{y}</span><div><h4>{t}</h4><p>{d}</p></div></div>' for y,t,d in c["timeline"])
    vals="".join(feat(*v) for v in c["values"])
    team="".join(teamcard(*t) for t in c["team"])
    ABOUT=(pagehero('Our Story','Locally owned and operated in Louisiana.',c["aboutlead"],'about.jpg')
     +sec('<div class="heritage-in"><div class="reveal"><div class="quote-mark">&ldquo;</div>'
       '<blockquote>An established company that will be here tomorrow, just like we are today.</blockquote><cite>— serving Louisiana since 1958</cite></div>'
       f'<div class="h-points reveal"><div class="h-point">{ic("award")}<div><b>Serving Louisiana since 1958</b><p>One of the Sun companies, rooted in Metairie, Louisiana.</p></div></div>'
       f'<div class="h-point">{ic("check")}<div><b>{c["aboutp"]}</b><p>{c["aboutpp"]}</p></div></div>'
       f'<div class="h-point">{ic("users")}<div><b>Local decisions</b><p>Handled by a local team in Metairie, Louisiana.</p></div></div></div></div>',"heritage")
     +sec(hb('Our History','Serving Louisiana since 1958.')+'<div class="progs">'+tl+'</div>',"sec-lines")
     +sec(hb('What We Stand For','The way we&apos;ve always done business.')+'<div class="feature-grid">'+vals+'</div>',"sec-glow")
     +sec(hb('Meet the Team',f'The people behind {c["name"]}.','Real, local people you&apos;ll actually work with — with decades of experience right here in Metairie.')+'<div class="team-grid">'+team+'</div>')
     +sec(f'<div class="trust-in"><div class="t reveal"><b>1958</b><span>Serving Louisiana since</span></div><div class="t reveal"><b>{c["ab2b"]}</b><span>{c["ab2s"]}</span></div><div class="t reveal"><b>{c["ab3b"]}</b><span>{c["ab3s"]}</span></div><div class="t reveal"><b>Local</b><span>Metairie, LA</span></div></div>',"sec-tint")
     +cta(c["ctah"],c["ctap"]))

    opts="".join(f'<option>{o}</option>' for o in c["formopts"])
    APPLY=(pagehero('Apply',c["applyhead"],c["contactlead"],'loc.jpg')
     +sec('<div class="contact-grid"><div class="reveal">'
       f'<div class="locphoto" style="background-image:url(\'img/city.jpg\')"><div class="cap">{ic("pin")}Serving Metairie &amp; Greater New Orleans</div></div>'
       f'<div class="loc">{ic("pin")}<div><b>Main Office</b><span>3525 N. Causeway Blvd, Suite 900<br>Metairie, LA 70002</span></div></div>'
       f'<div class="loc">{ic("phone")}<div><b>Call Us</b><a href="tel:{tel}">{tn}</a><br><span>Fax {c["fax"]}</span></div></div>'
       f'<div class="loc">{ic("clock")}<div><b>Hours</b><span>Call us for current office hours.</span></div></div></div>'
       '<form class="cform reveal" onsubmit="event.preventDefault();var b=this.querySelector(\'button\');b.textContent=\'✓ Received — we\\\'ll be in touch shortly\';b.disabled=true;">'
       '<div class="form-h">Start your application</div><div class="form-sub">Takes about 2 minutes — no obligation.</div>'
       '<div class="row"><div><label for="n">Full name</label><input id="n" type="text" autocomplete="name" placeholder="Your name" required></div>'
       '<div><label for="p">Phone</label><input id="p" type="tel" autocomplete="tel" placeholder="(504) 000-0000" required></div></div>'
       f'<label for="t">What are you looking for?</label><select id="t">{opts}</select>'
       '<label for="m">Tell us a little about your situation</label><textarea id="m"></textarea>'
       f'<button class="btn btn-gold" type="submit">{c["apply"]}</button>'
       '<p class="form-fine">Your information stays with our local Metairie team.</p></form></div>',"contact")
     +sec(hb('Getting Started','Three steps, one local team.')+'<div class="progs">'
       +prog('01','Reach out','Call, or send the form — whatever&apos;s easiest.')
       +prog('02','Talk it through','A local team member reviews your needs and lays out your options.')
       +prog('03','Get a real answer','Reviewed in-house, with a fast, straightforward next step.')+'</div>',"sec-lines grain")
     +sec(hb('Questions','Quick answers.')+'<div class="faq-list">'+"".join(faq(q,a) for q,a in c["faq_contact"])+'</div>',"sec-glow grain"))

    pages={"index.html":(c["title"],c["desc"],"Home",HOME),
     "how-it-works.html":(f'How It Works — {c["name"]}',c["prodlead"],"How It Works",PROD),
     "about.html":(f'About {c["name"]} — Since 1958','Locally owned and operated in Louisiana since 1958. One of the Sun companies in Metairie.',"About",ABOUT),
     "apply.html":(f'Apply — {c["name"]} | Metairie, LA',c["contactlead"],"Apply",APPLY)}
    for fn,(t,d,a,m) in pages.items():
        (B/fn).write_text(page(t,d,a,m)); print(B.name,fn,len((B/fn).read_text()))

PREMIUM=dict(dir="/Users/zaydenzukerman/webblaze/public/sunpremium",name="Sun Premium Financing",shortname="Sun Premium",tag="Premium<br>Financing",label="Premium Financing",apply="Get started",
 tel="+15048349400",telnum="(504) 834-9400",fax="(504) 834-9402",others=[("Sun Mortgage Funding","https://sunmortgagefunding.webblaze.io"),("Sun Finance · Personal Loans","https://sunfinance.webblaze.io")],
 h1="Keep your coverage. <em>Free up your cash.</em>",
 herop="Insurance premium financing from the Sun companies in Metairie, Louisiana since 1958 — for agents and their clients alike. We finance from $100 to $250,000 across more than ten types of insurance.",
 herostat="$100 – $250K financed",trust3="Agents &amp; individuals welcome",cardh="Premium Financing",cardcta="Request a quote",fine="Subject to approval. Terms vary by policy.",bbbtag="",ab3b="10+",ab3s="Insurance types",
 card=[("Amounts financed","$100 – $250K"),("Insurance types","10+"),("Agents &amp; individuals","Both"),("Local, since","1958")],
 trust=[("1958","Serving Louisiana since"),("$100–$250K","Financed"),("10+","Insurance types"),("Local","Metairie, LA")],
 whyhead="A premium finance partner that answers the phone.",whylead="We work directly with agents and insureds to keep coverage in force and cash free — with the personal service a national finance company can&apos;t match.",
 spliteyebrow="Why Sun Premium",splithead="A partner your clients can count on.",
 splitlead="From a single policy to a full commercial book, we structure premium financing that keeps coverage in force and cash working — backed by real people you can reach, not a call center.",
 localp="From Metairie to the North Shore, Sun Premium Financing keeps Louisiana businesses and their agents covered — with financing decisions made by people right here at home, since 1958.",
 why=[("wallet","Preserve your working capital","Pay premiums over time instead of one large lump sum — keep your cash for payroll, inventory and growth."),
      ("doc","10+ types of insurance","Commercial, property, life and specialty coverage — financed for agents and individuals alike."),
      ("users","A real, local partner","Accessible by phone and in person — a seamless experience for both agents and their clients.")],
 prodtitle="Big premiums, made manageable.",prodlead="Instead of paying a large insurance premium in one lump sum, let us finance it — you keep your cash working and your coverage in force.",
 steps=[("Secure your policy","Choose from more than ten types of coverage — commercial, property, life and specialty — through your agent."),
        ("We pay the premium","Sun Premium Financing pays your insurer the full annual premium up front, so your policy is fully in force from day one."),
        ("You repay in installments","Repay us in manageable scheduled payments across the policy term — no large lump sum out of pocket."),
        ("Keep your cash working","Your working capital stays free for the things that grow your business, instead of locked up in prepaid insurance.")],
 reviews=[("Agents rely on us as a steady financing partner — fast turnarounds and a team that picks up the phone.","Agent feedback <span>· Louisiana</span>"),
          ("Individuals keep valuable coverage in force without draining cash reserves.","Client feedback <span>· Metairie, LA</span>"),
          ("One of the Sun companies, serving Louisiana businesses and agents since 1958.","Serving since 1958 <span>· Metairie, LA</span>")],
 faq_home=[("Who can use premium financing?","Both insurance agents seeking a financing partner and individuals or businesses who&apos;d rather pay a large premium over time."),
           ("How much can you finance?","From $100 up to $250,000, across more than ten types of insurance.")],
 faq_prod=[("What types of insurance do you finance?","More than ten — including commercial, property, life and specialty coverage."),
           ("Do you work with my agent?","Yes. We work directly with agents and their clients for a seamless experience."),
           ("What are the terms?","Terms vary by policy and premium. Call us for a fast, specific quote.")],
 aboutlead="Sun Premium Financing is one of the Sun companies in Metairie, Louisiana, serving agents and insureds since 1958.",
 aboutp="For agents &amp; individuals",aboutpp="We work directly with insurance agents and their clients on more than ten types of coverage.",
 ab2b="$250K",ab2s="Financed, up to",
 timeline=[("1958","Serving Louisiana since 1958","One of the Sun companies, rooted in Metairie, Louisiana."),("Partner","A partner to agents","Sun Premium Financing helps agents and clients keep coverage in force."),("Today","Local &amp; personal","Real people you can reach, right here in Metairie.")],
 values=[("users","People over paperwork","A seamless experience for agents and insureds, backed by real service."),("shield","Coverage stays protected","We keep your policy in force so you&apos;re never caught uncovered."),("award","Here for the long run","An established company that will be here tomorrow, just like today.")],
 team=[("Aurora Surla","Manager","44 years with Sun Premium Financing"),("Rebecca Perret","Premium Financing","34 years with Sun Premium Financing")],
 formopts=["Commercial insurance premium","Property insurance premium","Life / specialty premium","I&apos;m an insurance agent","Not sure — help me decide"],
 ctah="Ready to finance a premium?",ctap="Agents and individuals welcome. Call for a fast quote.",
 contactlead="Request a quote, call us, or send a note — for agents and individuals alike.",
 applyhead="Keep your coverage. <em>Free up your cash.</em>",applyband="Serving Louisiana agents &amp; insureds since 1958.",
 utillinks=[("Agent Portal","users","https://www.portal.sunpremium.com:8443/Sun/faces/agents/AgentMain.jsp"),("Pay Online","cash","https://sunpremium.com/payment/")],blog="https://sunpremium.com/blog/",
 faq_contact=[("Are you set up for agents?","Absolutely — many of our relationships are with agents who use us as their financing partner."),("How fast can I get a quote?","Quickly — a real person follows up, usually the same or next business day.")],
 compliance='All financing subject to approval; terms vary by policy. Sun Premium Financing — locally owned and operated in Metairie, Louisiana since 1958.',
 footdesc="One of the Sun companies in Metairie, Louisiana since 1958 — insurance premium financing that keeps your coverage in force and your cash working.",
 title="Sun Premium Financing — Insurance Premium Financing in Louisiana Since 1958",
 desc="Insurance premium financing from the Sun companies in Metairie, Louisiana since 1958. $100 to $250,000 across 10+ insurance types, for agents and individuals.")

PERSONAL=dict(dir="/Users/zaydenzukerman/webblaze/public/sunfinance",name="Sun Finance",shortname="Sun Finance",tag="Personal<br>Loans",label="Personal Loans",apply="Apply now",
 tel="+15048379400",telnum="(504) 837-9400",fax="(504) 837-9494",others=[("Sun Mortgage Funding","https://sunmortgagefunding.webblaze.io"),("Sun Premium Financing","https://sunpremium.webblaze.io")],
 h1="Life&apos;s little surprises, <em>handled.</em>",
 herop="Fast, friendly personal loans from $500 to $3,000 — from the Sun companies in Metairie, Louisiana since 1958. Reviewed and serviced in-house by people you can actually reach, right here at home.",
 herostat="$500 – $3,000 loans",trust3="BBB A+ Accredited",cardh="Personal Loans At A Glance",cardcta="Start your application",fine="Subject to credit approval.",bbbtag=" · BBB A+ Accredited",ab3b="In-house",ab3s="Loans serviced",
 card=[("Loan amounts","$500 – $3K"),("Decisions made","Locally"),("Serviced in-house","Always"),("Trusted since","1958")],
 trust=[("1958","Serving Louisiana since"),("A+","BBB · since 1987"),("$500–$3K","Personal loan amounts"),("In-house","Reviewed &amp; serviced")],
 whyhead="A personal loan, from people who treat you like one.",whylead="No big-bank runaround and no out-of-state call center — just fast, friendly help from a lender Louisiana has trusted since 1958.",
 spliteyebrow="Why Sun Finance",splithead="Real help, from real neighbors.",
 splitlead="A short application, a real local decision, and money for whatever life throws at you — car repairs, bills, emergencies. Reviewed and serviced in-house by people who treat you like a neighbor, because you are one.",
 localp="Right here in Metairie and across Greater New Orleans, Sun Finance has helped Louisiana families through life&apos;s surprises since 1958 — with fast, friendly, local decisions.",
 why=[("bolt","Fast, simple decisions","A short application and a real, local decision — money for whatever life throws at you."),
      ("users","People you can reach","Reviewed and serviced in-house by folks right here in Metairie, not an algorithm."),
      ("award","Trusted since 1958","BBB accredited since 1987 — a lender that will be here tomorrow, just like today.")],
 prodtitle="Simple, fast, and local.",prodlead="No big-bank runaround. A quick application, a real local decision, and money for whatever life throws at you.",
 steps=[("Apply in minutes","Call us or stop by — a short, straightforward application, no mountain of paperwork."),
        ("A real, local decision","Your loan is reviewed in-house by people right here in Louisiana — not an out-of-state algorithm."),
        ("Get your funds","Approved borrowers get $500 to $3,000 quickly — for car repairs, bills, emergencies, whatever you need."),
        ("Pay it back your way","Manageable payments, serviced in-house, with people you can reach if anything comes up.")],
 reviews=[("Neighbors come to us for quick help with car repairs, bills and life&apos;s surprises — and get treated like people.","Client feedback <span>· Metairie, LA</span>"),
          ("Serviced in-house means a real person to call if anything changes.","Client feedback <span>· Louisiana</span>"),
          ("BBB-accredited with an A+ rating since 1987 — decades of doing right by Louisiana families.","BBB A+ <span>· since 1987</span>")],
 faq_home=[("How much can I borrow?","Personal loans range from $500 to $3,000, based on a quick, local review."),
           ("Are you actually local?","Yes — locally owned and operated in Metairie since 1958, and every loan is serviced in-house.")],
 faq_prod=[("What can I use the loan for?","Anything you need — car repairs, medical bills, emergencies, or getting through a tight month."),
           ("How fast can I get funds?","Fast. A short application and a real, local decision mean approved borrowers get funds quickly."),
           ("Do you service the loan yourselves?","Always. You&apos;ll deal with real people right here — not a distant call center.")],
 aboutlead="Sun Finance Company has served Metairie, Louisiana since 1958 — offering fast, friendly personal loans, reviewed and serviced in-house.",
 aboutp="Serviced in-house",aboutpp="Every personal loan is reviewed and serviced by real people, right here in Metairie.",
 ab2b="1987",ab2s="BBB accredited since",
 timeline=[("1958","Founded in 1958","Sun Finance Company has served Louisiana families since 1958."),("1987","BBB A+ accreditation","Accredited by the Better Business Bureau with an A+ rating."),("Today","Local &amp; in-house","Still local, still serviced in-house, in Metairie.")],
 values=[("users","People over paperwork","Real conversations, real decisions, made by people you can reach."),("bolt","Fast when it matters","Life doesn&apos;t wait — quick, local decisions when you need them."),("award","Here for the long run","An established company that will be here tomorrow, just like today.")],
 team=[("David Daube","President","44 years in finance · 28 as President"),("Brian Daube","Vice President","15 years in finance"),("Ashley Pabst","Manager","20 years with the company"),("Kim Naquin","Client Services","21 years with the company"),("Liz Jones","Manager","31 years with the company")],
 formopts=["Personal loan","Returning customer","Not sure — help me decide"],
 ctah="Need a hand this month?",ctap="Apply in minutes or call a local lender — no pressure.",
 contactlead="Apply, call, or send a note — a real, local person will get back to you fast.",
 applyhead="Life&apos;s little surprises, <em>handled.</em>",applyband="Helping Louisiana families since 1958.",
 utillinks=[("Locations","pin","https://www.sunfinance.com/locations/")],
 faq_contact=[("Does applying affect my credit?","We&apos;ll always tell you before any step that involves a credit check — no surprises."),("Is there any obligation?","None. Get your options and a real answer, then decide on your own terms.")],
 compliance='All loans subject to credit approval. Sun Finance Co. LLC — locally owned and operated in Metairie, Louisiana since 1958. BBB A+ accredited since 1987.',
 footdesc="One of the Sun companies in Metairie, Louisiana since 1958 — fast, friendly personal loans from $500 to $3,000, reviewed and serviced by real local people.",
 title="Sun Finance — Personal Loans in Louisiana Since 1958 | $500–$3,000",
 desc="Fast, friendly personal loans from $500 to $3,000 — from the Sun companies in Metairie, Louisiana since 1958. Serviced in-house.")

build(PREMIUM); build(PERSONAL)
