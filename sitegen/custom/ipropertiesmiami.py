#!/usr/bin/env python3
"""
iProperties Miami — multi-page preview site (hand-designed, not the sitegen template).
Builds ~/webblaze/public/ipropertiesmiami/{index,services,home-watch,contact,privacy}.
Content parity: every piece of copy from ipropertiesmiami.com (Home, Services, Contact) is kept,
plus new sections. Images are THEIR OWN branded images (logo, checklist, technician, homes).
Run: python3 sitegen/custom/ipropertiesmiami.py
"""
import os

OUT = os.path.expanduser("~/webblaze/public/ipropertiesmiami")
PHONE, PHONE_LINK, EMAIL = "305-391-7095", "+13053917095", "info@ipropertiesmiami.com"

CSS = r"""
:root{--ink:#121417;--ink2:#1C2026;--gold:#B8914C;--gold2:#D9B66F;--sand:#F3EDE3;--sand2:#E9E0D2;--paper:#FBF8F2;--txt:#1E232A;--mut:#626B75;--line:#E4DBCC}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:Inter,system-ui,-apple-system,sans-serif;color:var(--txt);background:var(--paper);line-height:1.65;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
h1,h2,h3{font-family:Fraunces,Georgia,serif;font-weight:400;line-height:1.1;letter-spacing:-.01em}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--gold)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;padding:15px 26px;border-radius:2px;font-weight:600;font-size:15px;border:0;cursor:pointer;transition:background .2s,color .2s,box-shadow .2s;font-family:inherit}
.btn-gold{background:linear-gradient(135deg,var(--gold2),var(--gold));color:#121417}.btn-gold:hover{box-shadow:0 10px 30px rgba(184,145,76,.35)}
.btn-line{border:1px solid rgba(255,255,255,.7);color:#fff;background:transparent}.btn-line:hover{background:#fff;color:var(--ink)}
.btn-dark{background:var(--ink);color:#fff}.btn-dark:hover{background:var(--ink2)}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
.preview{background:#000;color:#bfc5cc;font-size:13px;text-align:center;padding:8px 16px}
.preview b{color:var(--gold2);font-weight:600}
header{position:sticky;top:0;z-index:40;background:rgba(18,20,23,.96);backdrop-filter:blur(10px);color:#fff}
.nav{display:flex;align-items:center;justify-content:space-between;height:82px;gap:20px}
.logo{display:flex;align-items:center;gap:12px}
.logo img{height:54px;width:auto}
.logo .lt{font-family:Fraunces,serif;font-size:23px;line-height:1;color:#fff;letter-spacing:.01em}
.logo .lt small{display:block;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.42em;text-transform:uppercase;color:var(--gold2);margin-top:5px}
.nav ul{display:flex;gap:30px;list-style:none;font-size:15px;font-weight:500;color:#c9ced4}
.nav ul a{padding:6px 0;border-bottom:1px solid transparent;transition:color .2s,border-color .2s}
.nav ul a:hover,.nav ul a.on{color:#fff;border-color:var(--gold)}
.nav .call{font-weight:600;color:var(--gold2);white-space:nowrap}
.burger{display:none;width:44px;height:44px;border:1px solid rgba(255,255,255,.3);border-radius:2px;background:transparent;color:#fff;font-size:20px;cursor:pointer}
@media(max-width:920px){.logo .lt{font-size:20px}.nav ul{display:none;position:absolute;left:0;right:0;top:82px;flex-direction:column;gap:0;background:var(--ink);padding:10px 24px 20px}
 .nav ul.open{display:flex}.nav ul a{display:block;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.08)}
 .burger{display:block}.nav .call{display:none}.logo img{height:44px}}
.hero{position:relative;min-height:86vh;display:flex;align-items:flex-end;color:#fff;background:#121417 center/cover}
.hero:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,20,23,.15) 0%,rgba(18,20,23,.3) 45%,rgba(18,20,23,.88) 100%)}
.hero .wrap{position:relative;padding:130px 24px 80px}
.hero .eyebrow{color:var(--gold2)}
.hero h1{font-size:clamp(42px,6.2vw,84px);max-width:15ch;margin-top:18px}
.hero p{font-size:clamp(17px,1.6vw,20px);max-width:580px;margin-top:20px;color:rgba(255,255,255,.88)}
.hero .row{display:flex;gap:14px;flex-wrap:wrap;margin-top:34px}
.phero{position:relative;color:#fff;background:#121417 center/cover;padding:150px 0 80px}
.phero:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,20,23,.55),rgba(18,20,23,.85))}
.phero .wrap{position:relative}.phero .eyebrow{color:var(--gold2)}
.phero h1{font-size:clamp(38px,5vw,64px);margin-top:14px;max-width:18ch}
.phero p{max-width:600px;margin-top:16px;color:rgba(255,255,255,.85);font-size:18px}
.stats{background:var(--ink);color:#fff;border-top:1px solid rgba(217,182,111,.25)}
.stats .wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;padding:36px 24px}
.stats b{display:block;font-family:Fraunces,serif;font-size:44px;font-weight:400;color:var(--gold2);line-height:1.1}
.stats span{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#9aa3ad}
@media(max-width:760px){.stats .wrap{grid-template-columns:1fr 1fr}}
.sec{padding:110px 0}.sand{background:var(--sand)}.dark{background:var(--ink);color:#fff}
.split{display:grid;grid-template-columns:1fr 1fr;gap:70px;align-items:center}
.split.rev>:first-child{order:2}
.split h2,.head h2{font-size:clamp(34px,4vw,52px);margin-top:14px;color:var(--ink)}
.dark .split h2,.dark .head h2{color:#fff}
.split p,.head p{margin-top:18px;color:var(--mut);font-size:17px}
.dark .split p,.dark .head p{color:#b5bcc4}
.split img{width:100%;aspect-ratio:4/5;object-fit:cover}
.split .wide{aspect-ratio:3/2}
@media(max-width:880px){.split{grid-template-columns:1fr;gap:40px}.split.rev>:first-child{order:0}.split img{aspect-ratio:4/3}}
.head{max-width:680px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:56px}
.card{background:var(--paper);border:1px solid var(--line);display:flex;flex-direction:column;transition:transform .3s,box-shadow .3s}
.card:hover{transform:translateY(-4px);box-shadow:0 20px 40px rgba(18,20,23,.08)}
.card img{width:100%;aspect-ratio:3/2;object-fit:cover}
.card .t{padding:30px;display:flex;flex-direction:column;flex:1}
.card small{font-size:12px;font-weight:600;letter-spacing:.18em;color:var(--gold)}
.card h3{font-size:28px;color:var(--ink);margin-top:8px}
.card p{color:var(--mut);margin-top:10px;flex:1}
.card .more{margin-top:20px;font-weight:600;font-size:14px;color:var(--ink);border-bottom:1px solid var(--gold);align-self:flex-start;padding-bottom:2px}
@media(max-width:920px){.cards{grid-template-columns:1fr}}
.ticks{list-style:none;margin-top:22px}
.ticks li{position:relative;padding:9px 0 9px 30px;border-bottom:1px solid var(--line);color:var(--txt)}
.dark .ticks li{border-color:rgba(255,255,255,.1);color:#e3e6ea}
.ticks li:before{content:"";position:absolute;left:0;top:17px;width:14px;height:8px;border-left:2px solid var(--gold);border-bottom:2px solid var(--gold);transform:rotate(-45deg)}
.steps{display:grid;grid-template-columns:repeat(4,1fr);margin-top:56px;border-top:1px solid var(--line)}
.step{padding:34px 26px 0 0}.step+.step{padding-left:26px;border-left:1px solid var(--line)}
.step b{font-family:Fraunces,serif;font-weight:400;font-size:46px;color:var(--gold)}
.step h3{font-size:22px;color:var(--ink);margin-top:4px}.step p{color:var(--mut);margin-top:8px;font-size:15px}
@media(max-width:880px){.steps{grid-template-columns:1fr 1fr}.step{padding:26px 16px 0 0!important;border-left:0!important}}
.who{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:50px}
.who div{background:var(--paper);border:1px solid var(--line);padding:28px}
.who h3{font-size:22px;color:var(--ink)}.who p{color:var(--mut);font-size:15px;margin-top:8px}
@media(max-width:920px){.who{grid-template-columns:1fr 1fr}}@media(max-width:520px){.who{grid-template-columns:1fr}}
.band{position:relative;color:#fff;background:#121417 center/cover}
.band:before{content:"";position:absolute;inset:0;background:rgba(18,20,23,.8)}
.band .wrap{position:relative;padding:110px 24px;text-align:center}
.band .eyebrow{color:var(--gold2)}
.band h2{font-size:clamp(34px,4.4vw,58px);max-width:20ch;margin:16px auto 0}
.band p{max-width:580px;margin:18px auto 0;color:rgba(255,255,255,.85);font-size:17px}
.band .row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:32px}
.det{border-top:1px solid var(--line);margin-top:28px}
.det div{display:flex;justify-content:space-between;gap:20px;padding:18px 0;border-bottom:1px solid var(--line)}
.det small{color:var(--mut);font-size:13px;letter-spacing:.12em;text-transform:uppercase}
.det a,.det span{font-weight:600;color:var(--ink);text-align:right}
form label{display:block;font-size:13px;font-weight:600;color:var(--ink);margin-top:16px}
form input,form select,form textarea{width:100%;margin-top:7px;padding:14px;border:1px solid var(--line);background:#fff;font:inherit;font-size:16px;border-radius:2px;color:var(--txt)}
form textarea{min-height:130px;resize:vertical}
form .btn{margin-top:22px;width:100%}
.req{font-size:12px;color:var(--mut);margin-top:10px}
.thanks{display:none;margin-top:18px;padding:16px;background:var(--sand);color:var(--ink);border-left:3px solid var(--gold)}
/* plan builder */
.pb{background:var(--paper);border:1px solid var(--line);margin-top:50px;display:grid;grid-template-columns:1.25fr .75fr}
.pb .q{padding:40px}
.pb fieldset{border:0;margin-top:30px}.pb fieldset:first-child{margin-top:0}
.pb legend{font-family:Fraunces,serif;font-size:22px;color:var(--ink)}
.pb legend span{font-family:Inter,sans-serif;font-size:12px;letter-spacing:.18em;color:var(--gold);display:block;margin-bottom:4px;font-weight:600}
.opts{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.opts label{margin:0;cursor:pointer}
.opts input{position:absolute;opacity:0;width:1px;height:1px}
.opts span{display:inline-block;padding:11px 16px;border:1px solid var(--line);background:#fff;font-size:14.5px;font-weight:500;color:var(--txt);transition:all .18s}
.opts input:checked+span{background:var(--ink);color:#fff;border-color:var(--ink)}
.opts input:focus-visible+span{outline:2px solid var(--gold);outline-offset:2px}
.opts label:hover span{border-color:var(--gold)}
.pb .r{background:var(--ink);color:#fff;padding:40px;display:flex;flex-direction:column}
.pb .r .eyebrow{color:var(--gold2)}
.pb .r h3{font-size:30px;margin-top:12px}
.pb .r .freq{font-family:Fraunces,serif;font-size:46px;color:var(--gold2);margin-top:18px;line-height:1}
.pb .r .freqs{font-size:13px;color:#9aa3ad;letter-spacing:.06em;margin-top:6px}
.pb .r ul{list-style:none;margin-top:22px;flex:1}
.pb .r li{padding:9px 0 9px 26px;position:relative;border-bottom:1px solid rgba(255,255,255,.1);font-size:15px;color:#e3e6ea}
.pb .r li:before{content:"";position:absolute;left:0;top:16px;width:12px;height:7px;border-left:2px solid var(--gold2);border-bottom:2px solid var(--gold2);transform:rotate(-45deg)}
.pb .r .btn{margin-top:26px}
.pb .r .fine{font-size:12px;color:#8b949e;margin-top:12px}
@media(max-width:900px){.pb{grid-template-columns:1fr}.pb .q,.pb .r{padding:28px}}
.legal h2{font-size:28px;color:var(--ink);margin-top:40px}.legal p{color:var(--mut);margin-top:12px}
footer{background:#000;color:#9aa3ad;padding:60px 0 30px;font-size:14px}
footer .top{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:40px}
footer img{height:84px;width:auto}
footer b{display:block;color:#fff;font-weight:600;margin-bottom:12px;letter-spacing:.08em;font-size:12px;text-transform:uppercase}
footer a{display:block;padding:4px 0}footer a:hover{color:var(--gold2)}
footer .bot{margin-top:40px;padding-top:22px;border-top:1px solid rgba(255,255,255,.08);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
@media(max-width:760px){footer .top{grid-template-columns:1fr}}
.mbar{display:none}
@media(max-width:760px){.mbar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:30}.mbar a{flex:1;text-align:center;padding:16px;font-weight:600;color:#fff}.mbar .c{background:var(--ink)}.mbar .q{background:var(--gold);color:var(--ink)}body{padding-bottom:54px}}
.reveal{opacity:0;transform:translateY(18px);transition:opacity .8s ease,transform .8s ease}.reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}html{scroll-behavior:auto}}
"""

JS = r"""
(function(){
  var b=document.querySelector('.burger'),u=document.querySelector('.nav ul');
  if(b&&u)b.addEventListener('click',function(){var o=u.classList.toggle('open');b.setAttribute('aria-expanded',o);});
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12}):null;
  document.querySelectorAll('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in');});
  // contact form (preview: confirms on the page)
  var f=document.getElementById('cform');
  if(f){
    var q=new URLSearchParams(location.search),plan=q.get('plan'),svc=q.get('service');
    if(plan){var m=document.getElementById('cm');m.value='I built a Home Watch plan on your website:\n'+plan+'\n\nPlease contact me to set it up.';}
    if(svc){var s=document.getElementById('cs');Array.prototype.forEach.call(s.options,function(o){if(o.value===svc)o.selected=true;});}
    f.addEventListener('submit',function(e){e.preventDefault();document.getElementById('cthanks').style.display='block';f.querySelectorAll('input,select,textarea,button').forEach(function(x){x.disabled=true;});});
  }
  // Home Watch plan builder
  var pb=document.getElementById('pb');
  if(pb){
    var FREQ={vacant:['Weekly','visits while the home sits empty'],seasonal:['Bi-weekly','visits while you are away for the season'],travel:['Bi-weekly','visits, plus a check before you return'],rental:['Weekly','visits between guests or tenants']};
    var TYPE={condo:'Condo or apartment',home:'Single-family home',estate:'Waterfront estate',invest:'Investment property'};
    var CARE={water:'Leak, moisture and mold checks',ac:'A/C and humidity monitoring',security:'Doors, windows and security checks',storm:'Storm and emergency oversight',vendors:'Pool, landscaping and vendor coordination',repairs:'Handyman repairs as needed'};
    function val(n){var c=pb.querySelector('input[name='+n+']:checked');return c?c.value:null;}
    function upd(){
      var t=val('type'),a=val('away'),cs=[].map.call(pb.querySelectorAll('input[name=care]:checked'),function(x){return x.value;});
      var fr=FREQ[a||'seasonal'];
      document.getElementById('pf').textContent=fr[0];
      document.getElementById('pfs').textContent=fr[1];
      document.getElementById('pt').textContent=t?TYPE[t]:'Your property';
      var items=['Documented inspections, inside and out','Updates sent straight to you'].concat(cs.map(function(c){return CARE[c];}));
      document.getElementById('pl').innerHTML=items.map(function(x){return '<li>'+x+'</li>';}).join('');
      var summary=(t?TYPE[t]:'Property')+' | '+fr[0]+' '+fr[1]+(cs.length?' | Focus: '+cs.map(function(c){return CARE[c];}).join(', '):'');
      document.getElementById('pgo').href='../contact/?service=Home+Watch+Program&plan='+encodeURIComponent(summary)+'#form';
    }
    pb.addEventListener('change',upd);upd();
  }
})();
"""

def page(slug, title, desc, body, active):
    r = "../" if slug else ""
    nav = [("", "Home"), ("services/", "Services"), ("home-watch/", "Home Watch"), ("contact/", "Contact")]
    links = "".join('<li><a href="%s%s"%s>%s</a></li>' % (r, h, ' class="on" aria-current="page"' if h == active else "", n) for h, n in nav)
    return """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="{r}img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}site.css">
</head><body>
<div class="preview">Free preview designed for <b>iProperties Miami</b> by WebBlaze</div>
<header><div class="wrap nav">
  <a class="logo" href="{r}" aria-label="iProperties Miami home"><img src="{r}img/emblem.png" alt=""><span class="lt">iProperties<small>Miami</small></span></a>
  <ul>{links}</ul>
  <a class="call" href="tel:{pl}">{phone}</a>
  <button class="burger" aria-label="Menu" aria-expanded="false">&#9776;</button>
</div></header>
{body}
<footer><div class="wrap">
  <div class="top">
    <div><img src="{r}img/logo.png" alt="iProperties Miami"><p style="margin-top:16px;max-width:340px">Luxury property care and preventative maintenance, protecting high-value homes throughout Miami.</p></div>
    <div><b>Explore</b><a href="{r}">Home</a><a href="{r}services/">Services</a><a href="{r}home-watch/">Home Watch</a><a href="{r}contact/">Contact</a></div>
    <div><b>Contact</b><a href="tel:{pl}">{phone}</a><a href="mailto:{email}">{email}</a><span style="display:block;padding:4px 0">Mon - Fri, 9am - 5pm</span></div>
  </div>
  <div class="bot"><span>&copy; 2026 iProperties Miami. All rights reserved.</span><a href="{r}privacy/">Privacy Policy</a></div>
</div></footer>
<div class="mbar"><a class="c" href="tel:{pl}">Call</a><a class="q" href="{r}contact/#form">Get in touch</a></div>
<script src="{r}site.js"></script>
</body></html>""".format(title=title, desc=desc, r=r, links=links, pl=PHONE_LINK, phone=PHONE, email=EMAIL, body=body)

def cta(r):
    return """<section class="band" style="background-image:url({r}img/villa-sunset.webp)"><div class="wrap reveal">
  <div class="eyebrow">Do you have any questions?</div>
  <h2>Wherever you are, your home is in good hands.</h2>
  <p>Write to us and we will get back to you right away.</p>
  <div class="row"><a class="btn btn-gold" href="{r}contact/#form">Get in touch</a><a class="btn btn-line" href="tel:{pl}">{phone}</a></div>
</div></section>""".format(r=r, pl=PHONE_LINK, phone=PHONE)

SERVICES = [
  ("home-watch/", "checklist.webp", "Branded iProperties Miami preventative maintenance checklist at a client's front door", "01", "Home Watch",
   "A trusted, consistent presence at the home, checking for signs of damage, maintenance issues, security concerns and other problems that may go unnoticed when a property is vacant."),
  ("services/#maintenance", "interior-loft.webp", "Bright, well-maintained living space in a Miami home", "02", "Preventative Maintenance",
   "We help identify and address potential issues before they become costly problems, keeping your property protected, maintained and in excellent condition year-round."),
  ("services/#handyman", "interior-living.webp", "Bright luxury living room in a Miami home", "03", "Handyman Services",
   "From refined repairs and installations to detailed property enhancements, discreet, professional service tailored to the standards of luxury homes."),
]

def service_cards(r):
    return "".join("""<a class="card reveal" href="{r}{h}"><img src="{r}img/{img}" alt="{alt}" loading="lazy"><div class="t"><small>{n}</small><h3>{t}</h3><p>{d}</p><span class="more">Learn more</span></div></a>""".format(r=r, h=h, img=img, alt=alt, n=n, t=t, d=d) for h, img, alt, n, t, d in SERVICES)

HOME = lambda r: """
<section class="hero" style="background-image:url(img/villa-sunset.webp)"><div class="wrap">
  <div class="eyebrow">Home Maintenance Elevated</div>
  <h1>Exceptional quality. Discreet service. Flawless execution.</h1>
  <p>Every time. We protect, maintain and care for high-value homes throughout Miami, year round, so you never have to wonder how your property is doing.</p>
  <div class="row"><a class="btn btn-gold" href="home-watch/#plan">Build your Home Watch plan</a><a class="btn btn-line" href="contact/#form">Get in touch</a></div>
</div></section>
<div class="stats"><div class="wrap">
  <div><b>240</b><span>Contracts</span></div><div><b>183</b><span>Projects</span></div>
  <div><b>4</b><span>Dedicated specialists</span></div><div><b>Year round</b><span>Property oversight</span></div>
</div></div>
<section class="sec"><div class="wrap split">
  <div class="reveal"><div class="eyebrow">Let us introduce ourselves</div>
    <h2>A trusted presence on the ground.</h2>
    <p>We provide exceptional property care for discerning homeowners, seasonal residents, investors and real estate professionals, ensuring every property remains protected, meticulously maintained and impeccably cared for year round.</p>
    <p>From our Home Watch Program and preventative maintenance to repairs and ongoing property oversight, our trusted team delivers a seamless level of care designed to preserve your property and provide complete peace of mind.</p>
    <p style="margin-top:28px"><a class="btn btn-dark" href="services/">Explore our services</a></p></div>
  <img class="reveal" src="img/technician.webp" alt="iProperties Miami technician at work in a luxury Miami home" loading="lazy">
</div></section>
<section class="sec sand"><div class="wrap">
  <div class="head reveal"><div class="eyebrow">Our services at a glance</div>
    <h2>Protecting your home requires more than occasional repairs.</h2>
    <p>We provide proactive property care designed to preserve your investment and give you complete peace of mind.</p></div>
  <div class="cards">""" + service_cards(r) + """</div>
</div></section>
<section class="sec dark"><div class="wrap split rev">
  <div class="reveal"><div class="eyebrow">Get an idea of what we do</div>
    <h2>Luxury property care, handled end to end.</h2>
    <p>iProperties Miami is a luxury property care and preventative maintenance company dedicated to protecting, maintaining and preserving high value homes throughout Miami.</p>
    <ul class="ticks"><li>Home Watch Program</li><li>Preventative maintenance</li><li>Handyman services</li><li>Vendor coordination</li><li>Emergency oversight</li></ul></div>
  <img class="reveal wide" src="img/hero.webp" alt="Miami waterfront homes and pools" loading="lazy" style="aspect-ratio:4/3">
</div></section>
<section class="sec"><div class="wrap">
  <div class="head reveal"><div class="eyebrow">Who we serve</div><h2>Built for people who can't always be here.</h2></div>
  <div class="who">
    <div class="reveal"><h3>Seasonal residents</h3><p>Your home stays checked and cared for while you're out of town.</p></div>
    <div class="reveal"><h3>Discerning homeowners</h3><p>One trusted team for upkeep, repairs and everything in between.</p></div>
    <div class="reveal"><h3>Investors</h3><p>Protect the value of your properties with proactive oversight.</p></div>
    <div class="reveal"><h3>Real estate professionals</h3><p>Listings that stay protected, maintained and show-ready.</p></div>
  </div>
</div></section>
""" + cta(r)

SERVICES_PAGE = lambda r: """
<section class="phero" style="background-image:url(../img/interior-living.webp)"><div class="wrap">
  <div class="eyebrow">Services</div>
  <h1>Exceptional care for exceptional properties.</h1>
  <p>From our Home Watch Program and preventative maintenance to handyman services, vendor coordination and emergency oversight, we provide a trusted presence on the ground and peace of mind that your property is properly cared for year round.</p>
</div></section>
<section class="sec" id="homewatch"><div class="wrap split">
  <div class="reveal"><div class="eyebrow">01 &middot; Home Watch</div><h2>Eyes on your home while you're away.</h2>
    <p>iProperties Miami provides a trusted, consistent presence at the home, checking for signs of damage, maintenance issues, security concerns and other problems that may go unnoticed when a property is vacant.</p>
    <ul class="ticks"><li>Regular inspections while you're away</li><li>Checks for damage, leaks and security concerns</li><li>Findings reported straight to you</li></ul>
    <p style="margin-top:28px"><a class="btn btn-dark" href="../home-watch/#plan">Build your plan</a></p></div>
  <img class="reveal" src="../img/checklist.webp" alt="iProperties Miami maintenance checklist being completed at a client's home" loading="lazy">
</div></section>
<section class="sec sand" id="maintenance"><div class="wrap split rev">
  <div class="reveal"><div class="eyebrow">02 &middot; Preventative Maintenance</div><h2>Finding small problems before they become expensive.</h2>
    <p>We help identify and address potential issues before they become costly problems, keeping your property protected, maintained and in excellent condition year-round.</p>
    <ul class="ticks"><li>Scheduled preventative checks</li><li>Early detection of wear and damage</li><li>Vendor coordination when specialists are needed</li></ul>
    <p style="margin-top:28px"><a class="btn btn-dark" href="../contact/?service=Preventative+Maintenance#form">Ask about maintenance</a></p></div>
  <img class="reveal" src="../img/technician.webp" alt="iProperties Miami technician performing maintenance" loading="lazy">
</div></section>
<section class="sec" id="handyman"><div class="wrap split">
  <div class="reveal"><div class="eyebrow">03 &middot; Handyman Services</div><h2>Refined repairs, done discreetly.</h2>
    <p>From refined repairs and installations to detailed property enhancements, iProperties Miami provides discreet, professional service tailored to the standards of luxury homes.</p>
    <ul class="ticks"><li>Professional repairs and installations</li><li>Detailed property enhancements</li><li>Emergency oversight</li></ul>
    <p style="margin-top:28px"><a class="btn btn-dark" href="../contact/?service=Handyman+Services#form">Request a repair</a></p></div>
  <img class="reveal" src="../img/interior-loft.webp" alt="Luxury living space maintained by iProperties Miami" loading="lazy">
</div></section>
<section class="sec dark"><div class="wrap">
  <div class="head reveal"><div class="eyebrow">How it works</div><h2>Simple for you. Thorough for your home.</h2></div>
  <div class="steps" style="border-color:rgba(255,255,255,.12)">
    <div class="step"><b>1</b><h3 style="color:#fff">Consultation</h3><p style="color:#9aa3ad">Tell us about your property and how often you're away.</p></div>
    <div class="step" style="border-color:rgba(255,255,255,.12)"><b>2</b><h3 style="color:#fff">Custom plan</h3><p style="color:#9aa3ad">We build a care plan around your home and schedule.</p></div>
    <div class="step" style="border-color:rgba(255,255,255,.12)"><b>3</b><h3 style="color:#fff">Regular care</h3><p style="color:#9aa3ad">Inspections and maintenance happen on time, every time.</p></div>
    <div class="step" style="border-color:rgba(255,255,255,.12)"><b>4</b><h3 style="color:#fff">Peace of mind</h3><p style="color:#9aa3ad">You get updates and a team ready if anything comes up.</p></div>
  </div>
</div></section>
""" + cta(r)

def opts(name, items, typ="radio", checked=None):
    return '<div class="opts">' + "".join('<label><input type="%s" name="%s" value="%s"%s><span>%s</span></label>' % (typ, name, v, " checked" if v in (checked or []) else "", t) for v, t in items) + "</div>"

HOMEWATCH_PAGE = lambda r: """
<section class="phero" style="background-image:url(../img/checklist.webp)"><div class="wrap">
  <div class="eyebrow">Home Watch Program</div>
  <h1>Your home, watched over while you're away.</h1>
  <p>Regular inspections while you're away. A trusted, consistent presence at the home, checking for the problems that go unnoticed when a property is vacant.</p>
</div></section>
<section class="sec sand" id="plan"><div class="wrap">
  <div class="head reveal"><div class="eyebrow">Build your plan</div><h2>See what your Home Watch plan could look like.</h2>
    <p>Answer three quick questions. We'll suggest a starting plan, and you can send it straight to our team.</p></div>
  <form class="pb reveal" id="pb" onsubmit="return false">
    <div class="q">
      <fieldset><legend><span>Step 1</span>What kind of property?</legend>""" + opts("type", [("condo","Condo or apartment"),("home","Single-family home"),("estate","Waterfront estate"),("invest","Investment property")], checked=["home"]) + """</fieldset>
      <fieldset><legend><span>Step 2</span>How is the home used?</legend>""" + opts("away", [("seasonal","I'm away for the season"),("travel","I travel often"),("vacant","It sits empty"),("rental","Rental between guests")], checked=["seasonal"]) + """</fieldset>
      <fieldset><legend><span>Step 3</span>What matters most?</legend>""" + opts("care", [("water","Leaks and moisture"),("ac","A/C and humidity"),("security","Security"),("storm","Storm and emergencies"),("vendors","Pool and landscaping vendors"),("repairs","Repairs")], "checkbox", ["water","ac"]) + """</fieldset>
    </div>
    <div class="r" aria-live="polite">
      <div class="eyebrow">Your suggested plan</div>
      <h3 id="pt">Single-family home</h3>
      <div class="freq" id="pf">Bi-weekly</div><div class="freqs" id="pfs">visits while you are away for the season</div>
      <ul id="pl"></ul>
      <a class="btn btn-gold" id="pgo" href="../contact/#form">Send this plan to our team</a>
      <p class="fine">A starting point only. We confirm every detail with you in a free consultation.</p>
    </div>
  </form>
</div></section>
<section class="sec"><div class="wrap split">
  <div class="reveal"><div class="eyebrow">What we check</div><h2>Thorough, documented, every visit.</h2>
    <p>Every visit follows a checklist built for Miami homes, so small problems are caught early.</p>
    <ul class="ticks"><li>Signs of damage inside and out</li><li>Maintenance issues and wear</li><li>Security concerns at doors and windows</li><li>Problems that go unnoticed when a home is vacant</li></ul></div>
  <img class="reveal" src="../img/interior-loft.webp" alt="Well-kept home interior checked by iProperties Miami" loading="lazy">
</div></section>
""" + cta(r)

CONTACT_PAGE = lambda r: """
<section class="phero" style="background-image:url(../img/villa-sunset.webp)"><div class="wrap">
  <div class="eyebrow">Contact</div><h1>How to find us.</h1>
  <p>Contact us to learn more about our solutions or to discuss your specific requirements. We are here to help you.</p>
</div></section>
<section class="sec" id="form"><div class="wrap split" style="align-items:start">
  <div class="reveal"><div class="eyebrow">Contact us</div><h2>Let's talk about your home.</h2>
    <div class="det">
      <div><small>Telephone</small><a href="tel:""" + PHONE_LINK + """">""" + PHONE + """</a></div>
      <div><small>E-mail</small><a href="mailto:""" + EMAIL + """">""" + EMAIL + """</a></div>
      <div><small>Office hours</small><span>Monday - Friday, 9am - 5pm</span></div>
      <div><small>Service area</small><span>Miami, Florida</span></div>
    </div></div>
  <form id="cform" class="reveal">
    <label for="cn">Name *</label><input id="cn" required autocomplete="name">
    <label for="ce">Email *</label><input id="ce" type="email" required autocomplete="email">
    <label for="cp">Phone</label><input id="cp" type="tel" autocomplete="tel">
    <label for="cs">I'm interested in</label>
    <select id="cs"><option>Home Watch Program</option><option>Preventative Maintenance</option><option>Handyman Services</option><option>Something else</option></select>
    <label for="cm">Message *</label><textarea id="cm" required></textarea>
    <p class="req">* Indicates required fields</p>
    <button class="btn btn-gold" type="submit">Send</button>
    <div class="thanks" id="cthanks">Thank you! We will get back to you as soon as possible.</div>
  </form>
</div></section>
"""

PRIVACY_PAGE = lambda r: """
<section class="phero" style="background-image:url(../img/interior-loft.webp);padding-bottom:60px"><div class="wrap"><div class="eyebrow">Legal</div><h1>Privacy Policy</h1></div></section>
<section class="sec"><div class="wrap legal" style="max-width:800px">
  <p>This page explains how iProperties Miami handles information you share with us through this website.</p>
  <h2>Information you send us</h2><p>When you use our contact form or plan builder, we receive the details you enter, such as your name, email, phone number and message. We use them only to respond to you and provide our services.</p>
  <h2>Sharing</h2><p>We do not sell your information. We only share it with trusted vendors when needed to carry out services you have requested.</p>
  <h2>Contact</h2><p>Questions about your information? Email """ + EMAIL + """ or call """ + PHONE + """.</p>
</div></section>
"""

def main():
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "site.css"), "w").write(CSS)
    open(os.path.join(OUT, "site.js"), "w").write(JS)
    pages = [("", "iProperties Miami | Luxury Home Watch & Property Care in Miami", "Home watch, preventative maintenance and handyman services for high-value Miami homes. Call 305-391-7095.", HOME, ""),
             ("services", "Services | iProperties Miami", "Home Watch, Preventative Maintenance and Handyman Services for luxury homes in Miami.", SERVICES_PAGE, "services/"),
             ("home-watch", "Home Watch Program | iProperties Miami", "Regular inspections while you're away. Build your Home Watch plan for your Miami home.", HOMEWATCH_PAGE, "home-watch/"),
             ("contact", "Contact | iProperties Miami", "Call 305-391-7095 or email info@ipropertiesmiami.com. Office hours Monday - Friday 9am - 5pm.", CONTACT_PAGE, "contact/"),
             ("privacy", "Privacy Policy | iProperties Miami", "Privacy policy for iProperties Miami.", PRIVACY_PAGE, None)]
    for slug, title, desc, fn, active in pages:
        d = os.path.join(OUT, slug); os.makedirs(d, exist_ok=True)
        r = "../" if slug else ""
        open(os.path.join(d, "index.html"), "w").write(page(slug, title, desc, fn(r), active))
    print("built", len(pages), "pages ->", OUT)

if __name__ == "__main__":
    main()
