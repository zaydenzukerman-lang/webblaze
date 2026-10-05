#!/usr/bin/env python3
"""
Blue Halo Pools — preview redesign (WebBlaze).
All copy is Blue Halo's own, taken verbatim from bluehalopools.com (city pages parsed into cities.json).
Brand kept: navy #15324a, halo blue #3fa9e0, Poppins + Space Grotesk, their halo logo mark.
Every photo is used exactly once across the whole site.
Run: python3 sitegen/custom/bluehalo/build.py  -> ~/webblaze/public/bluehalopools/
"""
import os, json, re, html, subprocess, functools

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.expanduser("~/webblaze/public/bluehalopools")
DATA = json.load(open(os.path.join(HERE, "cities.json"), encoding="utf-8"))
ORDER, CITIES = DATA["order"], DATA["cities"]
PHONE, TEL, EMAIL = "(561) 300-0501", "+15613000501", "hello@bluehalopools.com"
E = lambda s: html.escape(s, quote=False)
MARK = open(os.path.join(OUT, "img", "logo-mark.svg")).read().replace('xmlns="http://www.w3.org/2000/svg"', 'xmlns="http://www.w3.org/2000/svg" class="mark" aria-hidden="true" focusable="false"')

@functools.lru_cache(None)
def dims(name):
    o = subprocess.run(["magick", "identify", "-format", "%w %h", os.path.join(OUT, "img", name + ".webp")], capture_output=True, text=True).stdout.split()
    return int(o[0]), int(o[1])
USED = []
def img(r, name, alt, cls="", sizes="(min-width:900px) 50vw, 100vw", eager=False):
    USED.append(name); w, h = dims(name)
    return ('<img class="%s" src="%simg/%s.webp" srcset="%simg/%s-md.webp 900w, %simg/%s.webp %dw" sizes="%s" width="%d" height="%d" alt="%s"%s>'
            % (cls, r, name, r, name, r, name, w, sizes, w, h, html.escape(alt), ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'))

CSS = r"""
:root{--navy:#15324a;--navy2:#0d2232;--blue:#3fa9e0;--deep:#1d6e9e;--sky:#e6f2fa;--sky2:#f3f8fc;--sand:#f2ede4;--ink:#15324a;--txt:#2a3d4c;--mut:#5a6c79;--line:#dbe6ee;--white:#fff;--r:18px;--sh:0 1px 2px rgba(13,34,50,.06),0 12px 32px rgba(13,34,50,.08)}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{font-family:Poppins,system-ui,-apple-system,sans-serif;color:var(--txt);background:#fff;line-height:1.65;-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}a{color:inherit;text-decoration:none}button{font:inherit;cursor:pointer}
h1,h2,h3,h4{font-family:'Space Grotesk',Poppins,sans-serif;font-weight:600;color:var(--ink);line-height:1.08;letter-spacing:-.015em}
.wrap{max-width:1200px;margin:0 auto;padding:0 24px}
.eyebrow{font-size:12.5px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--deep)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:14px 24px;border-radius:999px;font-weight:600;font-size:15px;border:0;transition:transform .2s,box-shadow .2s,background .2s}
.btn-blue{background:var(--blue);color:#06263a;box-shadow:0 8px 24px rgba(63,169,224,.35)}.btn-blue:hover{transform:translateY(-1px);box-shadow:0 12px 30px rgba(63,169,224,.45)}
.btn-navy{background:var(--navy);color:#fff}.btn-navy:hover{background:var(--navy2)}
.btn-ghost{border:1.5px solid rgba(255,255,255,.75);color:#fff}.btn-ghost:hover{background:rgba(255,255,255,.14)}
.btn-line{border:1.5px solid var(--navy);color:var(--navy)}.btn-line:hover{background:var(--navy);color:#fff}
:focus-visible{outline:3px solid var(--blue);outline-offset:3px;border-radius:6px}
.preview{background:var(--navy2);color:#b8cbd8;font-size:13px;text-align:center;padding:8px 16px}.preview b{color:#fff;font-weight:600}
header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.94);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;gap:26px;height:76px}
.brand{display:flex;align-items:center;gap:12px;margin-right:auto}
.brand .mark{width:46px;height:38px}
.brand .bw{display:flex;flex-direction:column;line-height:1}
.brand .bw b{font-family:'Space Grotesk',sans-serif;font-size:21px;color:var(--navy);font-weight:600;letter-spacing:-.01em}
.brand .bw span{font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--deep);margin-top:3px;font-weight:500}
.links{display:flex;gap:26px;list-style:none;font-size:15px;font-weight:500}
.links a{color:var(--mut);padding:6px 0;border-bottom:2px solid transparent}.links a:hover,.links a.on{color:var(--navy);border-color:var(--blue)}
.nav .tel{font-weight:600;color:var(--navy);white-space:nowrap;font-size:15px}
.nav .btn{padding:11px 20px;font-size:14px}
.burger{display:none;width:44px;height:44px;border-radius:12px;border:1px solid var(--line);background:#fff;font-size:20px;color:var(--navy)}
@media(max-width:1000px){.links{display:none;position:absolute;left:0;right:0;top:76px;flex-direction:column;gap:0;background:#fff;padding:8px 24px 18px;border-bottom:1px solid var(--line)}
 .links.open{display:flex}.links a{display:block;padding:13px 0;border-bottom:1px solid var(--line)}.burger{display:block}.nav .tel{display:none}}
@media(max-width:560px){.nav .btn{display:none}}
.hero{position:relative;min-height:calc(100vh - 110px);display:flex;align-items:center;color:#fff;overflow:hidden;background:var(--navy2)}
.hero .bg,.phero .bg,.band .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(13,34,50,.88) 0%,rgba(13,34,50,.62) 46%,rgba(13,34,50,.15) 100%)}
.hero .wrap{position:relative;z-index:2;display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center;padding-top:70px;padding-bottom:70px;width:100%}
.pill{display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);font-size:13px;font-weight:500;color:#e6f2fa;backdrop-filter:blur(6px)}
.pill i{width:8px;height:8px;border-radius:50%;background:var(--blue);box-shadow:0 0 0 4px rgba(63,169,224,.25)}
.hero h1{color:#fff;font-size:clamp(46px,6.6vw,88px);margin-top:20px}.hero h1 em{font-style:normal;color:#7fd0f5}
.hero p.lead{font-size:clamp(16px,1.4vw,19px);margin-top:20px;max-width:560px;color:rgba(255,255,255,.88)}
.hero .row{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.hero .fine{margin-top:16px;font-size:14px;color:rgba(255,255,255,.78)}.hero .fine a{color:#7fd0f5;font-weight:600}
.glass{background:rgba(255,255,255,.96);color:var(--txt);border-radius:22px;padding:24px 26px;box-shadow:0 30px 60px rgba(0,0,0,.25)}
.glass h3{font-size:19px}.glass .sub{font-size:13px;color:var(--mut);margin-top:2px}
.checks{list-style:none;margin-top:14px}
.checks li{display:grid;grid-template-columns:26px 1fr;gap:10px;padding:9px 0;border-top:1px solid var(--line)}
.checks li:before{content:"";width:22px;height:22px;border-radius:50%;background:var(--sky) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231d6e9e' stroke-width='3'%3E%3Cpath d='M5 12l5 5 9-10'/%3E%3C/svg%3E") center/13px no-repeat;margin-top:2px}
.checks b{display:block;font-size:14.5px;color:var(--ink);font-weight:600}.checks small{font-size:13px;color:var(--mut)}
.glass .foot{font-size:12.5px;color:var(--mut);margin-top:10px}
@media(max-width:960px){.hero .wrap{grid-template-columns:1fr}.hero{min-height:auto}}
.trust{background:var(--navy);color:#fff}
.trust .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;padding:26px 24px}
.trust b{display:block;font-family:'Space Grotesk',sans-serif;font-size:18px}.trust span{font-size:14px;color:#b8cbd8}
@media(max-width:700px){.trust .wrap{grid-template-columns:1fr}}
.sec{padding:110px 0}.sky{background:var(--sky2)}.sandbg{background:var(--sand)}.dark{background:var(--navy);color:#cfdce6}.dark h2,.dark h3{color:#fff}.dark .eyebrow{color:#7fd0f5}
.head{max-width:720px}.head.c{margin:0 auto;text-align:center}
.head h2,.split h2{font-size:clamp(34px,4.2vw,54px);margin-top:12px}
.head p,.split p{margin-top:16px;font-size:17px;color:var(--mut)}.dark .head p,.dark .split p{color:#b8cbd8}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:56px}
.step{background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh)}
.step img{width:100%;aspect-ratio:16/10;object-fit:cover}.step .t{padding:24px}
.step .n{font-family:'Space Grotesk';font-size:14px;font-weight:600;color:var(--deep)}.step h3{font-size:24px;margin-top:6px}.step p{color:var(--mut);margin-top:8px;font-size:15.5px}
@media(max-width:900px){.steps{grid-template-columns:1fr}}
.split{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}
.split.top{align-items:start}
.photo{border-radius:24px;width:100%;aspect-ratio:4/3;object-fit:cover;box-shadow:var(--sh)}
@media(max-width:920px){.split{grid-template-columns:1fr;gap:40px}}
/* Pool Health Report */
.report{background:#fff;color:var(--txt);border-radius:24px;box-shadow:0 30px 70px rgba(0,0,0,.28);overflow:hidden}
.report .top{background:linear-gradient(135deg,var(--deep),var(--navy));color:#fff;padding:20px 24px}
.report .top b{font-family:'Space Grotesk';font-size:20px}.report .top small{display:block;font-size:12.5px;color:#cfe6f5;margin-top:2px}
.report .body{padding:20px 22px 22px}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.tile{border:1.5px solid var(--line);border-radius:14px;padding:12px;text-align:left;background:#fff;transition:border-color .2s,background .2s}
.tile small{display:block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);font-weight:600}
.tile b{display:block;font-family:'Space Grotesk';font-size:21px;color:var(--ink);margin-top:3px}
.tile em{display:inline-block;margin-top:4px;font-style:normal;font-size:11.5px;font-weight:600;padding:2px 8px;border-radius:999px;background:#e3f4ea;color:#23784a}
.tile em.adj{background:#fff1dc;color:#9a5b0b}
.tile[aria-pressed=true]{border-color:var(--blue);background:var(--sky2)}
.trend{margin-top:16px;border:1px solid var(--line);border-radius:16px;padding:16px}
.trend h4{font-size:15px}.trend .tg{font-size:12.5px;color:var(--mut)}
.trend svg{width:100%;height:auto;margin-top:8px;display:block}
.trend p{font-size:13.5px;color:var(--mut);margin-top:8px}
.rlist{list-style:none;margin-top:14px;font-size:14px}.rlist li{padding:6px 0 6px 24px;position:relative;border-top:1px solid var(--line)}
.rlist li:before{content:"✓";position:absolute;left:2px;color:var(--deep);font-weight:700}
.tech{margin-top:12px;background:var(--sky2);border-radius:12px;padding:12px 14px;font-size:14px}.tech small{display:block;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);font-weight:600}
.tapnote{font-size:12px;color:var(--mut);margin:-4px 0 10px}
@media(max-width:520px){.tiles{grid-template-columns:1fr 1fr}}
/* plans */
.plans{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:56px;align-items:stretch}
.plan{background:#fff;border:1px solid var(--line);border-radius:22px;padding:30px 28px;display:flex;flex-direction:column;box-shadow:var(--sh);position:relative}
.plan.pop{background:var(--navy);color:#cfdce6;border-color:var(--navy);transform:translateY(-10px)}
.plan.pop h3,.plan.pop .price b{color:#fff}
.plan .tag{position:absolute;top:-13px;left:28px;background:var(--blue);color:#06263a;font-size:12px;font-weight:600;padding:5px 12px;border-radius:999px}
.plan h3{font-size:24px}.plan .q{font-style:italic;color:var(--deep);font-size:14.5px;margin-top:4px}.plan.pop .q{color:#7fd0f5}
.price{margin-top:18px}.price small{font-size:13px;color:var(--mut)}.plan.pop .price small{color:#9fb6c6}
.price b{font-family:'Space Grotesk';font-size:48px;color:var(--ink);font-weight:600}.price span{font-size:15px}
.plan .desc{font-size:14.5px;margin-top:8px}
.plan ul{list-style:none;margin:18px 0 22px;flex:1}.plan li{font-size:14.5px;padding:8px 0 8px 26px;position:relative;border-top:1px solid var(--line)}.plan.pop li{border-color:rgba(255,255,255,.1)}
.plan li:before{content:"✓";position:absolute;left:3px;color:var(--blue);font-weight:700}
.plan .plus{font-weight:600;font-size:14px;color:var(--ink);margin-top:14px}.plan.pop .plus{color:#fff}
.away{margin-top:26px;display:flex;gap:16px;align-items:center;justify-content:center;flex-wrap:wrap;background:var(--sky);border-radius:999px;padding:14px 22px;font-size:15px;text-align:center}
.away a{font-weight:600;color:var(--deep)}
.small{font-size:13.5px;color:var(--mut);margin-top:22px;max-width:820px}
@media(max-width:960px){.plans{grid-template-columns:1fr}.plan.pop{transform:none}}
/* areas */
.cities{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:44px}
.city{display:block;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px;transition:border-color .2s,transform .2s,box-shadow .2s}
.city:hover{border-color:var(--blue);transform:translateY(-2px);box-shadow:var(--sh)}
.city b{font-family:'Space Grotesk';font-size:18px;color:var(--ink);display:flex;justify-content:space-between}.city b:after{content:"→";color:var(--blue)}
.city span{display:block;font-size:14px;color:var(--mut);margin-top:6px}
@media(max-width:900px){.cities{grid-template-columns:1fr 1fr}}@media(max-width:560px){.cities{grid-template-columns:1fr}}
.finder{margin-top:30px;display:flex;gap:10px;flex-wrap:wrap;max-width:620px}
.finder select{flex:1;min-width:220px;padding:14px 16px;border-radius:999px;border:1.5px solid var(--line);font:inherit;font-size:16px;background:#fff;color:var(--ink)}
.finder .res{flex-basis:100%;font-size:15px;margin-top:6px;min-height:24px}
/* faq */
.faq{max-width:860px;margin:44px auto 0}
.faq details{border-bottom:1px solid var(--line);padding:4px 0}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:20px;padding:18px 0;font-family:'Space Grotesk';font-size:19px;font-weight:600;color:var(--ink)}
.faq summary::-webkit-details-marker{display:none}.faq summary:after{content:"+";font-size:24px;color:var(--blue);line-height:1}
.faq details[open] summary:after{content:"−"}.faq p{padding:0 0 18px;color:var(--mut)}
/* quote */
.qgrid{display:grid;grid-template-columns:1.3fr .7fr;gap:24px;margin-top:44px;align-items:start}
.qcard{background:#fff;border:1px solid var(--line);border-radius:24px;padding:30px;box-shadow:var(--sh)}
.qcard .badge,.pcard .badge{display:inline-block;font-size:12px;font-weight:600;padding:5px 12px;border-radius:999px;background:var(--sky);color:var(--deep)}
.qcard h3,.pcard h3{font-size:26px;margin-top:12px}.qcard>p{color:var(--mut);margin-top:6px}
.prog{height:6px;border-radius:6px;background:var(--line);margin:20px 0 6px;overflow:hidden}.prog i{display:block;height:100%;width:50%;background:var(--blue);transition:width .4s}
.qstep{display:none}.qstep.on{display:block}
.qq{margin-top:18px}.qq>b{display:block;font-size:15px;color:var(--ink);font-weight:600}.qq>b small{font-weight:400;color:var(--mut)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:9px}
.chips label{cursor:pointer}.chips input{position:absolute;opacity:0;width:1px;height:1px}
.chips span{display:inline-block;padding:9px 14px;border-radius:12px;border:1.5px solid var(--line);font-size:14px;background:#fff}
.chips span small{display:block;font-size:11.5px;color:var(--mut)}
.chips input:checked+span{border-color:var(--navy);background:var(--navy);color:#fff}.chips input:checked+span small{color:#b8cbd8}
.chips input:focus-visible+span{outline:3px solid var(--blue);outline-offset:2px}
.qcard label.f{display:block;font-size:13.5px;font-weight:600;color:var(--ink);margin-top:14px}
.qcard input.f,.qcard select.f,.qcard textarea{width:100%;margin-top:6px;padding:13px 14px;border:1.5px solid var(--line);border-radius:12px;font:inherit;font-size:16px;color:var(--ink);background:#fff}
.qcard textarea{min-height:80px}
.consent{display:flex;gap:10px;align-items:flex-start;font-size:12.5px;color:var(--mut);margin-top:14px}.consent input{margin-top:3px}
.qnav{display:flex;justify-content:space-between;align-items:center;margin-top:22px;gap:12px}
.qnote{font-size:12.5px;color:var(--mut);text-align:center;margin-top:10px}
.pcard{background:var(--navy);color:#cfdce6;border-radius:24px;padding:30px}.pcard h3{color:#fff}.pcard .badge{background:rgba(127,208,245,.18);color:#7fd0f5}
.pcard .big{display:block;margin-top:18px;text-align:center;font-family:'Space Grotesk';font-size:24px;font-weight:600;background:var(--blue);color:#06263a;border-radius:999px;padding:14px}
.pcard p{font-size:14px;margin-top:12px}
.thanks{display:none;padding:26px;text-align:center;background:var(--sky2);border-radius:16px;margin-top:16px}.thanks h4{font-size:22px}
@media(max-width:900px){.qgrid{grid-template-columns:1fr}}
/* bands & page heroes */
.band{position:relative;color:#fff;overflow:hidden;background:var(--navy2)}
.band:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,34,50,.55),rgba(13,34,50,.82))}
.band .wrap{position:relative;z-index:2;text-align:center;padding:130px 24px}
.band h2{color:#fff;font-size:clamp(40px,5.4vw,72px)}.band p{max-width:560px;margin:16px auto 0;color:rgba(255,255,255,.88);font-size:17px}
.band .row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:30px}
.phero{position:relative;color:#fff;overflow:hidden;background:var(--navy2)}
.phero:after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(13,34,50,.88),rgba(13,34,50,.5))}
.phero .wrap{position:relative;z-index:2;padding:110px 24px 90px}
.phero .eyebrow{color:#7fd0f5}.phero h1{color:#fff;font-size:clamp(40px,5.4vw,68px);margin-top:14px;max-width:16ch}
.phero p{max-width:620px;margin-top:16px;color:rgba(255,255,255,.88);font-size:17.5px}
.phero .row{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.crumbs{font-size:13px;color:#b8cbd8;margin-bottom:6px}.crumbs a:hover{color:#fff}
.cards3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:44px}
.card{background:#fff;border:1px solid var(--line);border-radius:20px;padding:26px;box-shadow:var(--sh)}
.card .ic{width:44px;height:44px;border-radius:12px;background:var(--sky);display:grid;place-items:center;color:var(--deep);font-family:'Space Grotesk';font-weight:600}
.card h3{font-size:21px;margin-top:14px}.card p{color:var(--mut);font-size:15px;margin-top:8px}
.cards4{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:44px}
@media(max-width:960px){.cards3,.cards4{grid-template-columns:1fr 1fr}}@media(max-width:600px){.cards3,.cards4{grid-template-columns:1fr}}
.visit{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:44px}
.visit .card{padding:0;overflow:hidden}.visit .card img{width:100%;aspect-ratio:16/10;object-fit:cover}.visit .card div{padding:24px}
@media(max-width:900px){.visit{grid-template-columns:1fr}}
.facts{list-style:none;margin-top:24px;border-top:1px solid var(--line)}.facts li{display:grid;grid-template-columns:170px 1fr;gap:20px;padding:15px 0;border-bottom:1px solid var(--line);font-size:15.5px}
.facts b{color:var(--ink);font-weight:600}@media(max-width:600px){.facts li{grid-template-columns:1fr;gap:4px}}
.cmp{width:100%;border-collapse:separate;border-spacing:0;margin-top:40px;background:#fff;border:1px solid var(--line);border-radius:20px;overflow:hidden;box-shadow:var(--sh);font-size:15px}
.cmp th,.cmp td{padding:15px 18px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
.cmp thead th{background:var(--navy);color:#fff;font-family:'Space Grotesk';font-size:17px}.cmp thead th small{display:block;font-family:Poppins;font-weight:400;font-size:12.5px;color:#9fb6c6}
.cmp tbody th{font-weight:600;color:var(--ink);width:24%}.cmp td.no{color:#98a8b4}
.cmpwrap{overflow-x:auto}
.legal h2{font-size:26px;margin-top:40px}.legal p,.legal li{color:var(--mut);margin-top:10px}.legal ul{margin-left:20px}
.role{display:flex;justify-content:space-between;gap:20px;align-items:center;flex-wrap:wrap}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:30px}.metrics div{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px}.metrics b{font-family:'Space Grotesk';font-size:20px;color:var(--ink);display:block}.metrics span{font-size:13.5px;color:var(--mut)}
@media(max-width:800px){.metrics{grid-template-columns:1fr 1fr}}
footer{background:var(--navy2);color:#9fb6c6;padding:64px 0 30px;font-size:14.5px}
footer .top{display:grid;grid-template-columns:1.4fr 1fr 1.2fr 1.2fr;gap:36px}
footer .brand .bw b{color:#fff}footer .brand .bw span{color:#7fd0f5}
footer h5{color:#fff;font-size:12px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:12px;font-family:Poppins}
footer a{display:block;padding:4px 0}footer a:hover{color:#fff}
footer .bot{margin-top:44px;padding-top:20px;border-top:1px solid rgba(255,255,255,.08);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:13px}
@media(max-width:900px){footer .top{grid-template-columns:1fr 1fr}}@media(max-width:560px){footer .top{grid-template-columns:1fr}}
.mbar{display:none}@media(max-width:700px){.mbar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:60}.mbar a{flex:1;text-align:center;padding:15px;font-weight:600}.mbar .c{background:var(--navy);color:#fff}.mbar .q{background:var(--blue);color:#06263a}body{padding-bottom:52px}}
.reveal{opacity:0;transform:translateY(16px);transition:opacity .7s ease,transform .7s ease}.reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}html{scroll-behavior:auto}}
"""

REPORT_DATA = {
 "cl": {"label": "Free chlorine", "val": "2.8 ppm", "st": "In range", "h": "Free chlorine · last six visits", "tg": "Target 2.0–4.0 ppm", "min": 2.0, "max": 4.0, "unit": "ppm",
        "pts": [["7 Jul", 2.4], ["14 Jul", 1.9], ["21 Jul", 3.1], ["28 Jul", 2.6], ["4 Aug", 2.2], ["11 Aug", 2.8]],
        "note": "The dip on 14 July was a heavy-use week after the holiday. It recovered on its own by the next visit, so nothing was dosed."},
 "ph": {"label": "pH level", "val": "7.5", "st": "In range", "h": "pH level · last six visits", "tg": "Target 7.2–7.8", "min": 7.2, "max": 7.8, "unit": "",
        "pts": [["7 Jul", 7.6], ["14 Jul", 7.8], ["21 Jul", 7.4], ["28 Jul", 7.3], ["4 Aug", 7.6], ["11 Aug", 7.5]],
        "note": "Drifting up is normal on a plaster pool. Small acid doses on 21 and 28 July held it mid-band rather than chasing it from one end to the other."},
 "al": {"label": "Alkalinity", "val": "92 ppm", "st": "In range", "h": "Alkalinity · last six visits", "tg": "Target 80–120 ppm", "min": 80, "max": 120, "unit": "ppm",
        "pts": [["7 Jul", 88], ["14 Jul", 95], ["21 Jul", 110], ["28 Jul", 104], ["4 Aug", 97], ["11 Aug", 92]],
        "note": "Alkalinity is what keeps pH from swinging. Holding it near the middle of the band is why the pH line above stays flat."},
 "cy": {"label": "Cyanuric acid", "val": "61 ppm", "st": "Adjusted", "h": "Cyanuric acid · last six visits", "tg": "Target 40–80 ppm", "min": 40, "max": 80, "unit": "ppm",
        "pts": [["7 Jul", 58], ["14 Jul", 56], ["21 Jul", 54], ["28 Jul", 52], ["4 Aug", 49], ["11 Aug", 61]],
        "note": "Stabilizer is what stops the sun burning off your chlorine. It had drifted down to 49 through splash-out and rain, so 1 lb went in on this visit."},
}

def report():
    tiles = "".join('<button type="button" class="tile" data-k="%s" aria-pressed="%s"><small>%s</small><b>%s</b><em%s>%s</em></button>'
                    % (k, "true" if k == "cl" else "false", v["label"], v["val"], ' class="adj"' if v["st"] == "Adjusted" else "", v["st"]) for k, v in REPORT_DATA.items())
    return """<div class="report reveal" id="report">
  <div class="top"><b>Pool Health Report</b><small>Sample — this is what lands in your inbox · Tuesday 11 August · 10:42 AM</small></div>
  <div class="body">
    <p class="tapnote">Tap any reading to see its trend</p>
    <div class="tiles">%s</div>
    <div class="trend" aria-live="polite"><h4 id="rt-h"></h4><div class="tg" id="rt-tg"></div><svg id="rt-svg" viewBox="0 0 520 170" role="img"></svg><p id="rt-n"></p></div>
    <ul class="rlist"><li>Skimmed, brushed and vacuumed</li><li>Skimmer and pump baskets emptied</li><li>Filter pressure checked — 14 psi, normal</li><li>1 lb stabilizer, 2 tabs added</li></ul>
    <div class="tech"><small>Note from your technician</small>“Stabilizer was running low so I brought it back up. Everything else looked good — nothing you need to do.”</div>
  </div>
</div>""" % tiles

PLANS = [
 ("Halo Essential", "“We'll keep the water right.”", "129", "Weekly service and balanced water. Pay for the chemicals you use.", None,
  ["Weekly visit", "Full water test and chemical balancing", "Skim, brush walls and tile line, vacuum as needed", "Empty skimmer and pump baskets", "Filter pressure and equipment check", "Salt cell inspected every visit", "Pool Health Report emailed after every visit"], True),
 ("Halo Complete", "“We'll handle all of it.”", "179", "Flat monthly pricing, year round. The bill does not move with the seasons.", "Everything in Halo Essential, plus:",
  ["All routine chemicals included - one fixed monthly bill", "Filter clean and cartridge inspection every 4 weeks", "No trip or diagnostic charge on repairs", "Priority scheduling on service calls", "Annual Pool Report - chemistry, equipment and pool health metrics"], False),
 ("Halo Signature", "“You'll never think about it.”", "249", "For the pool you would rather never think about at all.", "Everything in Halo Complete, plus:",
  ["Your service day locked in for maintenance visits", "Filter cleaning every 2 weeks", "Salt cell descaled as needed on salt systems", "Equipment monitoring with proactive replacement notice", "Front of the queue on service calls", "Repair labor at half price", "50% off filter replacement", "One free annual spot treatment", "Storm prep and one post-storm cleanup"], False),
]
def plans(r):
    out = []
    for name, q, price, desc, plus, items, pop in PLANS:
        out.append('<div class="plan%s reveal">%s<h3>%s</h3><div class="q">%s</div><div class="price"><small>Starting at</small><br><b>$%s</b><span>/mo</span></div><p class="desc">%s</p>%s<ul>%s</ul><a class="btn %s" href="%squote/?plan=%s">Get started</a></div>'
                   % (" pop" if pop else "", '<span class="tag">Most popular</span>' if pop else "", name, q, price, desc, '<div class="plus">%s</div>' % plus if plus else "",
                      "".join("<li>%s</li>" % E(i) for i in items), "btn-blue" if pop else "btn-line", r, name.split()[1].lower()))
    return """<div class="plans">%s</div>
<div class="away reveal"><span><b>Travelling?</b> Halo Away keeps the pool right while you're gone — from $50 a visit, no plan required.</span><a href="%sservices-and-plans/#away">See how it works →</a></div>
<p class="small">Prices shown are starting prices for a standard residential pool on a weekly route. Every account is subject to a price quote by a technician or at the point of sale - pool size, surface, equipment, screen enclosure and tree cover all move the number. We quote before we service, and the quote is the price.</p>""" % ("".join(out), r)

def city_cards(r, slugs):
    return "".join('<a class="city" href="%s%s/"><b>%s</b><span>%s</span></a>' % (r, s, CITIES[s]["name"], E(CITIES[s]["blurb"])) for s in slugs)

HOME_FAQ = [
 ("How much does weekly pool service cost?", "Our plans start at $129 a month for weekly service on a standard residential pool, and every account is subject to a price quote by a technician or at the point of sale. Pool size, surface, equipment, screen enclosure and tree cover all affect the rate, which is why we quote each pool rather than publishing a flat price."),
 ("What is the Pool Health Report?", "It is an email you receive the moment we finish at your pool. It lists the chemistry readings we took, the chemicals we added and how much, the tasks we completed, the technician's name, and photos taken at your pool on that visit. You never have to wonder whether anyone showed up or what they did."),
 ("Do I need to be home for service?", "No. We work outside and only need gate access. Most of our customers are never home when we service, which is exactly why the report matters."),
 ("Which areas do you serve?", "Palm Beach County, from Boca Raton up to Jupiter and west to Wellington and Royal Palm Beach. Each city we cover has its own page describing what we actually see there. If your town isn't listed, call and we'll tell you honestly whether we can reach you."),
 ("How quickly can you start?", "Most new accounts start on the next weekly cycle. Call (561) 300-0501 and we can usually quote you on the phone and give you a start date the same day."),
]
SVC_FAQ = [
 ("What is included in a weekly visit?", "We test and balance the water, skim the surface, brush the walls and tile line, vacuum as needed, empty the skimmer and pump baskets, and check filter pressure and equipment. Every visit ends with a Pool Health Report emailed to you."),
 ("Is the chemical program separate?", "On Halo Essential, routine chemicals are billed as used. On Halo Complete and Halo Signature they are included in the flat monthly rate, so your bill does not move with the seasons."),
 ("Do you handle repairs?", "Yes. Pumps, motors, heaters, salt cells, filters, timers and automation. Repairs are quoted before any work starts and are billed separately from your monthly plan. Halo Complete removes the trip and diagnostic charge, and Halo Signature bills repair labor at half our standard rate."),
 ("Can you take on a green pool?", "Usually. Green-pool recovery is quoted as a one-off job based on what we find, and once the water is clear we can put the pool onto a weekly plan."),
 ("Do you service commercial pools?", "We service a small number of HOA and commercial pools on our route. Call us and we will tell you honestly whether we can do it properly."),
]
def faq(items):
    return '<div class="faq">%s</div>' % "".join("<details><summary>%s</summary><p>%s</p></details>" % (E(q), E(a)) for q, a in items)

QUOTE_CITIES = ["West Palm Beach", "Palm Beach Gardens", "Jupiter", "Wellington", "Royal Palm Beach", "Greenacres", "Lantana", "Riviera Beach", "Palm Springs", "North Palm Beach", "Palm Beach"]
def chips(name, opts, checked=None):
    return '<div class="chips">%s</div>' % "".join('<label><input type="radio" name="%s" value="%s"%s><span>%s%s</span></label>' % (name, v, " checked" if v == checked else "", v, "<small>%s</small>" % s if s else "") for v, s in opts)
def quote_block(r):
    city_opts = "".join("<option>%s</option>" % c for c in sorted({CITIES[s]["name"] for s in ORDER}) ) + "<option>Somewhere else in Palm Beach County</option>"
    return """<div class="qgrid">
  <form class="qcard reveal" id="qform" novalidate>
    <span class="badge">Within the hour</span>
    <h3>Price my pool</h3>
    <p>A few taps and your address, and we text you a real monthly rate — usually within the hour.</p>
    <p id="qplan" style="display:none;margin-top:10px;font-size:14px"></p>
    <div class="prog"><i id="qbar"></i></div>
    <div class="qstep on" data-s="1">
      <div class="qq"><b>How big is the pool?</b>""" + chips("size", [("Average", "most pools around here"), ("Small", "plunge or spool"), ("Large", "bigger than the neighbors'")], "Average") + """</div>
      <div class="qq"><b>What is around it?</b>""" + chips("around", [("Open", "little debris"), ("Screened", "under a cage"), ("Heavy trees", "constant leaf drop")], "Open") + """</div>
      <div class="qq"><b>Chlorine or salt?</b>""" + chips("water", [("Chlorine", ""), ("Salt", ""), ("Not sure", "")], "Chlorine") + """</div>
      <div class="qq"><b>Is there a spa attached?</b>""" + chips("spa", [("No spa", ""), ("Attached spa", "")], "No spa") + """</div>
      <div class="qq"><b>Who looks after it now?</b>""" + chips("now", [("A pool company", "we can take over"), ("I do it myself", "most of our customers used to"), ("Nobody right now", "it may need a clean-up first")], "A pool company") + """</div>
      <label class="f" for="q-change">What would you change about the service you have? <small style="font-weight:400;color:var(--mut)">optional</small></label><textarea id="q-change"></textarea>
      <div class="qnav"><span class="qnote" style="margin:0">No contact details on this screen.</span><button type="button" class="btn btn-navy" id="qnext">Continue</button></div>
    </div>
    <div class="qstep" data-s="2">
      <button type="button" class="btn btn-line" id="qback" style="padding:8px 14px;font-size:13px">← back</button>
      <label class="f" for="q-name">Your name</label><input class="f" id="q-name" required autocomplete="name">
      <label class="f" for="q-mobile">Mobile number</label><input class="f" id="q-mobile" type="tel" required autocomplete="tel">
      <label class="f" for="q-email">Email</label><input class="f" id="q-email" type="email" autocomplete="email">
      <label class="f" for="q-street">Street address</label><input class="f" id="q-street" required autocomplete="street-address">
      <label class="f" for="q-city">City</label><select class="f" id="q-city" required><option value="">Select your city</option>""" + city_opts + """</select>
      <label class="consent"><input type="checkbox" id="q-sms" required><span>Text me my quote at the number above. Message frequency varies. Message and data rates may apply. Reply STOP to opt out or HELP for help. We never share your number — see our <a href=\"""" + r + """privacy/" style="text-decoration:underline">privacy policy</a>.</span></label>
      <button type="submit" class="btn btn-blue" style="width:100%;margin-top:18px">Text me my quote</button>
      <p class="qnote">A real person prices it and checks your address against the route. No obligation.</p>
    </div>
    <div class="thanks" id="qthanks"><h4>Thanks, we've got it.</h4><p style="margin-top:8px;color:var(--mut)">This is a design preview, so nothing was sent. On the live site, your quote request goes straight to Blue Halo.</p></div>
  </form>
  <div class="pcard reveal"><span class="badge">Right now</span><h3>Get a price on the phone</h3><p>Two or three minutes for most pools. No visit, no callback queue.</p>
    <a class="big" href="tel:""" + TEL + """">""" + PHONE + """</a>
    <p style="text-align:center">or <a href="sms:""" + TEL + """" style="text-decoration:underline;color:#fff">text the same number</a></p>
    <p style="text-align:center;font-size:13px">7 days a week, 7am–6pm · On a pool when you call? Leave a message and we'll come straight back.</p></div>
</div>"""

def band(r, photo):
    return """<section class="band">%s<div class="wrap reveal"><h2>Stop thinking<br>about the pool.</h2>
<p>Get a free quote and we'll tell you what it costs and which day we run near you. No follow-up if it isn't for you.</p>
<div class="row"><a class="btn btn-blue" href="%squote/">Get a free quote</a><a class="btn btn-ghost" href="tel:%s">Call %s</a></div></div></section>""" % (img(r, photo, "", "bg", "100vw"), r, TEL, PHONE)

JS = r"""
(function(){
  var b=document.querySelector('.burger'),u=document.querySelector('.links');
  if(b&&u)b.addEventListener('click',function(){var o=u.classList.toggle('open');b.setAttribute('aria-expanded',o);});
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.1}):null;
  document.querySelectorAll('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in');});
  // Pool Health Report
  var R=window.BH_REPORT, rep=document.getElementById('report');
  if(R&&rep){
    function draw(k){var d=R[k],svg=document.getElementById('rt-svg'),W=520,H=170,pl=40,pr=14,pt=14,pb=28;
      var vals=d.pts.map(function(p){return p[1]}),lo=Math.min(d.min,Math.min.apply(0,vals)),hi=Math.max(d.max,Math.max.apply(0,vals)),pad=(hi-lo)*.15;lo-=pad;hi+=pad;
      var x=function(i){return pl+i*(W-pl-pr)/(d.pts.length-1)},y=function(v){return pt+(hi-v)*(H-pt-pb)/(hi-lo)};
      var band='<rect x="'+pl+'" y="'+y(d.max)+'" width="'+(W-pl-pr)+'" height="'+(y(d.min)-y(d.max))+'" fill="#e6f2fa" rx="6"/>';
      var line=d.pts.map(function(p,i){return (i?'L':'M')+x(i).toFixed(1)+' '+y(p[1]).toFixed(1)}).join(' ');
      var dots=d.pts.map(function(p,i){var last=i===d.pts.length-1;return '<circle cx="'+x(i)+'" cy="'+y(p[1])+'" r="'+(last?6:4.5)+'" fill="'+(last?'#1d6e9e':'#fff')+'" stroke="#1d6e9e" stroke-width="2.5"><title>'+p[0]+' — '+p[1]+(d.unit?' '+d.unit:'')+'</title></circle>'+
        '<text x="'+x(i)+'" y="'+(H-8)+'" text-anchor="middle" font-size="11" fill="#5a6c79">'+p[0]+'</text>'+
        '<text x="'+x(i)+'" y="'+(y(p[1])-11)+'" text-anchor="middle" font-size="11" font-weight="600" fill="#15324a">'+p[1]+'</text>'}).join('');
      var lab='<text x="4" y="'+(y(d.max)+4)+'" font-size="10.5" fill="#5a6c79">'+d.max+'</text><text x="4" y="'+(y(d.min)+4)+'" font-size="10.5" fill="#5a6c79">'+d.min+'</text>';
      svg.innerHTML=band+lab+'<path d="'+line+'" fill="none" stroke="#3fa9e0" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'+dots;
      svg.setAttribute('aria-label',d.h+'. '+d.pts.map(function(p){return p[0]+' '+p[1]}).join(', '));
      document.getElementById('rt-h').textContent=d.h;document.getElementById('rt-tg').textContent=d.tg;document.getElementById('rt-n').textContent=d.note;
      rep.querySelectorAll('.tile').forEach(function(t){t.setAttribute('aria-pressed',t.dataset.k===k)});}
    rep.querySelectorAll('.tile').forEach(function(t){t.addEventListener('click',function(){draw(t.dataset.k)})});draw('cl');
  }
  // quote builder
  var f=document.getElementById('qform');
  if(f){
    var plan=new URLSearchParams(location.search).get('plan'),qp=document.getElementById('qplan');
    if(plan&&qp){qp.style.display='block';qp.innerHTML='<b>Plan selected:</b> Halo '+plan.charAt(0).toUpperCase()+plan.slice(1)+' · <a href="#" id="qclear" style="text-decoration:underline">clear</a>';document.getElementById('qclear').onclick=function(e){e.preventDefault();qp.style.display='none';};}
    var bar=document.getElementById('qbar');
    function go(n){f.querySelectorAll('.qstep').forEach(function(s){s.classList.toggle('on',s.dataset.s==n)});bar.style.width=(n==1?50:100)+'%';f.scrollIntoView({behavior:'smooth',block:'start'});}
    document.getElementById('qnext').onclick=function(){go(2)};document.getElementById('qback').onclick=function(){go(1)};
    f.addEventListener('submit',function(e){e.preventDefault();var bad=[].filter.call(f.querySelectorAll('.qstep[data-s="2"] [required]'),function(i){return i.type==='checkbox'?!i.checked:!i.value.trim()});
      if(bad.length){bad[0].focus();bad[0].reportValidity&&bad[0].reportValidity();return;}
      f.querySelectorAll('.qstep').forEach(function(s){s.classList.remove('on')});document.querySelector('.prog').style.display='none';document.getElementById('qthanks').style.display='block';});
  }
  // area checker
  var fs=document.getElementById('finder');
  if(fs){var res=document.getElementById('fres');fs.addEventListener('change',function(){var o=fs.selectedOptions[0];
    if(!fs.value){res.innerHTML='';return;}
    if(fs.value==='other'){res.innerHTML='Send the address through and we\'ll tell you which day we run near you. <a href="../quote/" style="color:var(--deep);font-weight:600">Get a quote →</a>';return;}
    res.innerHTML='<b>Yes, we service '+o.textContent+'.</b> <a href="../'+fs.value+'/" style="color:var(--deep);font-weight:600">See what we see there →</a>';});}
})();
"""

def page(path, title, desc, body, active="", report_js=False, schema=None):
    depth = len(path.split("/")) if path else 0
    r = "../" * depth
    nav = [("services-and-plans/", "Services & Plans"), ("areas-we-serve/", "Areas We Serve"), ("about/", "About"), ("careers/", "Careers")]
    links = "".join('<li><a href="%s%s"%s>%s</a></li>' % (r, h, ' class="on" aria-current="page"' if h == active else "", n) for h, n in nav)
    foot_areas = "".join('<a href="%s%s/">%s</a>' % (r, s, CITIES[s]["name"]) for s in ORDER[:6])
    ld = ('<script type="application/ld+json">%s</script>' % json.dumps(schema, ensure_ascii=False)) if schema else ""
    rep = ("<script>window.BH_REPORT=%s</script>" % json.dumps(REPORT_DATA, ensure_ascii=False)) if report_js else ""
    return """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>%(title)s</title><meta name="description" content="%(desc)s">
<link rel="icon" href="%(r)simg/logo-mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap"></noscript>
<link rel="stylesheet" href="%(r)ssite.css">%(ld)s
</head><body>
<div class="preview">Free preview designed for <b>Blue Halo Pools</b> by WebBlaze</div>
<header><div class="wrap nav">
  <a class="brand" href="%(r)s">%(mark)s<span class="bw"><b>Blue Halo</b><span>Pools</span></span></a>
  <ul class="links">%(links)s</ul>
  <a class="tel" href="tel:%(tel)s">%(phone)s</a>
  <a class="btn btn-blue" href="%(r)squote/">Get a free quote</a>
  <button class="burger" aria-label="Menu" aria-expanded="false">&#9776;</button>
</div></header>
%(body)s
<footer><div class="wrap">
  <div class="top">
    <div><a class="brand" href="%(r)s">%(mark)s<span class="bw"><b>Blue Halo</b><span>Pools</span></span></a><p style="margin-top:14px;max-width:320px">Weekly pool service across Palm Beach County. Chemistry logged and photographed on every visit, emailed before we leave.</p></div>
    <div><h5>Service</h5><a href="%(r)sservices-and-plans/">Services &amp; Plans</a><a href="%(r)sabout/">About us</a><a href="%(r)squote/">Get a free quote</a><a href="%(r)scareers/">Careers</a></div>
    <div><h5>Areas we serve</h5>%(fa)s<a href="%(r)sareas-we-serve/" style="color:#fff">All Palm Beach County →</a></div>
    <div><h5>Get in touch</h5><a href="tel:%(tel)s">%(phone)s</a><a href="mailto:%(email)s">%(email)s</a><p style="margin-top:10px;font-size:13.5px">7 days a week, 7am–6pm. We serve customers at their homes and do not operate a walk-in location.</p></div>
  </div>
  <div class="bot"><span>&copy; 2026 Blue Halo Pools. Serving Palm Beach County, Florida.</span><a href="%(r)sprivacy/">Privacy policy</a></div>
</div></footer>
<div class="mbar"><a class="c" href="tel:%(tel)s">Call</a><a class="q" href="%(r)squote/">Free quote</a></div>
%(rep)s<script src="%(r)ssite.js"></script>
</body></html>""" % dict(title=E(title), desc=html.escape(desc), r=r, ld=ld, mark=MARK, links=links, tel=TEL, phone=PHONE, email=EMAIL, body=body, fa=foot_areas, rep=rep)

BIZ = {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": "Blue Halo Pools", "url": "https://bluehalopools.com/",
       "telephone": "+1-561-300-0501", "email": "hello@bluehalopools.com", "areaServed": [{"@type": "City", "name": CITIES[s]["name"] + ", FL"} for s in ORDER],
       "openingHours": "Mo-Su 07:00-18:00", "description": "Weekly pool service across Palm Beach County. Chemistry logged and photographed on every visit, emailed before we leave."}
def faq_ld(items): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def home():
    r = ""
    body = """
<section class="hero">%s<div class="wrap">
  <div><span class="pill"><i></i>Palm Beach County · Since 2019</span>
    <h1>Blue pool.<br>Every week.<br><em>Proof in your inbox.</em></h1>
    <p class="lead">Every visit ends the same way: the readings we took, the chemicals we added and photos from your pool, emailed before we pull out of the driveway. You never have to wonder whether anyone came or what they did.</p>
    <div class="row"><a class="btn btn-blue" href="quote/">Get a free quote</a><a class="btn btn-ghost" href="#plans">See plans &amp; pricing</a></div>
    <p class="fine">Month to month · 30 days' notice · no cancellation fee<br>Or call <a href="tel:%s">%s</a> for an instant quote.</p></div>
  <div class="glass reveal"><h3>Your service day</h3><div class="sub">The same list every week, whether or not you are home</div>
    <ul class="checks"><li><span><b>Water tested and balanced</b><small>chlorine, pH, alkalinity, stabiliser</small></span></li><li><span><b>Skimmed, brushed, vacuumed</b><small>walls and tile line, as needed</small></span></li><li><span><b>Baskets emptied</b><small>skimmer and pump</small></span></li><li><span><b>Equipment checked</b><small>filter pressure, pump, timer</small></span></li><li><span><b>You get the readings</b><small>and photos taken at your pool that day</small></span></li></ul>
    <div class="foot">The same list every week, and the report lands in your inbox before we leave.</div></div>
</div></section>
<div class="trust"><div class="wrap"><div><b>Locally owned</b><span>owner-run on this route since 2019</span></div><div><b>Quote to first service</b><span>usually within 7 days</span></div><div><b>Photos every visit</b><span>readings, chemicals and what we did</span></div></div></div>

<section class="sec"><div class="wrap">
  <div class="head c reveal"><div class="eyebrow">How it works</div><h2>Three steps, then you stop thinking about it</h2><p>No estimator to click through, no sales visit, no contract to sign before you know the price.</p></div>
  <div class="steps">
    <div class="step reveal">%s<div class="t"><div class="n">01</div><h3>Request a quote</h3><p>Tell us about the pool in two minutes. Most we can price on the phone, and there's no sales visit unless you want one.</p></div></div>
    <div class="step reveal">%s<div class="t"><div class="n">02</div><h3>We take over</h3><p>Your pool goes onto the weekly route and the reports start arriving. Most new accounts start on the next cycle.</p></div></div>
    <div class="step reveal">%s<div class="t"><div class="n">03</div><h3>You just enjoy it</h3><p>Clear blue water every week, ready whenever you are. No Saturday with a test kit, no bag of shock in the garage. One less thing on your plate.</p></div></div>
  </div>
</div></section>

<section class="sec dark" id="report-sec"><div class="wrap split">
  <div class="reveal"><div class="eyebrow">The Pool Health Report</div><h2>The part nobody else sends you</h2>
    <p>Pool service is a trust problem more than a cleaning problem. You're paying someone to come to your house while you're at work and do something you can't see.</p>
    <p>So we close that gap. When the technician marks your pool complete, the report goes out automatically: the readings taken at your pool, the chemicals added and how much, the tasks completed, who did the work, and photos shot on site that day. Not stock images, not last week's photos.</p>
    <p>If the water is off, you see it in the numbers before it turns green. If a filter pressure is climbing, you see that too, and we tell you what it means.</p>
    <p style="margin-top:24px"><a class="btn btn-blue" href="services-and-plans/#inbox">See what's in a report</a></p></div>
  %s
</div></section>

<section class="sec sky" id="plans"><div class="wrap">
  <div class="head c reveal"><div class="eyebrow">Plans</div><h2>Three plans, quoted before you commit</h2><p>Every plan includes weekly service and the Pool Health Report. What changes is how much of the chemistry and equipment care is folded into the flat rate.</p></div>
  %s
</div></section>

<section class="sec"><div class="wrap split top">
  <div class="reveal"><div class="eyebrow">Areas we serve</div><h2>Across Palm Beach County</h2><p>Boca Raton up to Jupiter, the coast out to Wellington. The same weekly service and the same report wherever your pool is.</p><p style="margin-top:24px"><a class="btn btn-line" href="areas-we-serve/">See all areas we serve</a></p>%s</div>
  <div class="cities reveal" style="grid-template-columns:1fr 1fr;margin-top:0">%s</div>
</div></section>

<section class="sec sky"><div class="wrap"><div class="head c reveal"><div class="eyebrow">Questions</div><h2>Straight answers</h2></div>%s</div></section>

<section class="sec" id="quote"><div class="wrap"><div class="head c reveal"><div class="eyebrow">Get a quote</div><h2>Two ways to get a price</h2><p>Pick whichever you prefer. Both reach the same person.</p></div>%s</div></section>
%s""" % (img(r, "hero-halo", "Overhead view of a circular swimming pool ringed by coconut palms", "bg", "100vw", True), TEL, PHONE,
         img(r, "step-quote", "Letter tiles spelling POOL at the edge of a swimming pool"), img(r, "step-takeover", "Pool ladder over clear blue water"), img(r, "step-enjoy", "Person relaxing on a float in a pool, seen from above"),
         report(), plans(r), img(r, "service-day", "Steps leading into a clean pool", "photo", sizes="(min-width:900px) 50vw, 100vw").replace('class="photo"', 'class="photo" style="margin-top:34px"'),
         city_cards(r, ORDER[:6]), faq(HOME_FAQ), quote_block(r), band(r, "cta"))
    return page("", "Weekly Pool Service in Boca Raton & Delray Beach | Blue Halo", "Weekly pool service across Palm Beach County with a Pool Health Report after every visit: readings, chemicals and photos, emailed before we leave.", body, "", True, [BIZ, faq_ld(HOME_FAQ)])

def services():
    r = "../"
    rows = [("Weekly visit &amp; Pool Health Report", "Included", "Included", "Included"),
            ("Routine chemicals", "Billed as used", "All routine chemicals included", "All routine chemicals included"),
            ("Filter cleans", None, "Every 4 weeks, with cartridge inspection", "Every 2 weeks"),
            ("Salt cell", "Inspected every visit", "Inspected every visit", "Descaled as needed on salt systems"),
            ("Scheduling", None, "Priority scheduling on service calls", "Service day locked in · front of the queue"),
            ("Repairs", "Quoted before any work starts", "No trip or diagnostic charge", "Repair labor at half price · 50% off filter replacement")]
    cell = lambda v: '<td class="no">—</td>' if v is None else "<td>%s</td>" % v
    table = '<div class="cmpwrap reveal"><table class="cmp"><thead><tr><th></th><th>Halo Essential<small>from $129/mo</small></th><th>Halo Complete<small>from $179/mo</small></th><th>Halo Signature<small>from $249/mo</small></th></tr></thead><tbody>%s</tbody></table></div>' % "".join("<tr><th>%s</th>%s</tr>" % (a, "".join(cell(x) for x in (b, c, d))) for a, b, c, d in rows)
    body = """
<section class="phero">%s<div class="wrap"><div class="eyebrow">Services &amp; plans</div><h1>Weekly service, priced honestly</h1>
<p>Three plans covering everything from a straightforward screened pool to a pool-and-spa with a salt system and heater. Every one of them is quoted on your pool before you commit to anything.</p>
<div class="row"><a class="btn btn-blue" href="../quote/">Get a free quote</a><a class="btn btn-ghost" href="tel:%s">Call %s</a></div></div></section>

<section class="sec sky"><div class="wrap">
  <div class="head c reveal"><div class="eyebrow">Plans</div><h2>Pick the one that fits your pool</h2><p>Every plan includes the weekly visit and the Pool Health Report. What changes is how much of the chemistry and equipment care sits inside the flat monthly rate instead of on your bill as an add-on — so each plan shows you what it covers and, where it matters, what it doesn't.</p></div>
  %s
  <h3 class="reveal" style="font-size:26px;margin-top:70px;text-align:center">Side by side</h3>
  %s
</div></section>

<section class="sec" id="away"><div class="wrap split">
  <div class="reveal"><div class="eyebrow">One-off &amp; seasonal</div><h2>Halo Away: “Going away? We'll cover it.”</h2>
    <p>Single visits while you're travelling, or a short run of them. No plan, no commitment, no reconnection fee when you get back.</p>
    <div class="price" style="margin-top:20px"><b>$50</b><span>/visit</span></div>
    <ul class="checks" style="margin-top:18px"><li><span><b>A full weekly-standard visit, one at a time</b></span></li><li><span><b>Water tested, balanced and dosed</b></span></li><li><span><b>Skimmed, brushed and baskets emptied</b></span></li><li><span><b>Chemicals included in the visit price</b></span></li><li><span><b>Pool Health Report after every visit</b></span></li></ul>
    <p style="margin-top:24px"><a class="btn btn-navy" href="tel:%s">Ask about Halo Away</a></p></div>
  %s
</div></section>

<section class="sec sky"><div class="wrap">
  <div class="head c reveal"><div class="eyebrow">The weekly visit</div><h2>What actually happens at your pool</h2><p>The same sequence every week, in the same order. Consistency is most of what keeps a pool from going wrong.</p></div>
  <div class="visit">
    <div class="card reveal">%s<div><h3>Water</h3><p>Test free and total chlorine, pH, total alkalinity, cyanuric acid and salt where applicable. Dose to bring the water back into range, and record both the reading and the dose.</p></div></div>
    <div class="card reveal">%s<div><h3>Surface and walls</h3><p>Skim the surface, brush the walls, steps and tile line, and vacuum when the pool needs it rather than on a fixed schedule you're paying for whether it helps or not.</p></div></div>
    <div class="card reveal">%s<div><h3>Equipment</h3><p>Empty the skimmer and pump baskets, check filter pressure against its clean baseline, and look over the pump, heater and automation for anything starting to go.</p></div></div>
  </div>
</div></section>

<section class="sec dark" id="inbox"><div class="wrap split">
  <div class="reveal"><div class="eyebrow">What lands in your inbox</div><h2>The report sends itself</h2>
    <p>When your pool is marked complete on the route, the report sends automatically. No one has to remember to write it, which is why it actually arrives every week.</p>
    <ul class="checks" style="margin-top:20px"><li><span><b style="color:#fff">Chemistry readings</b><small style="color:#b8cbd8">the numbers taken at your pool, not an average</small></span></li><li><span><b style="color:#fff">Chemicals added</b><small style="color:#b8cbd8">what went in and how much of it</small></span></li><li><span><b style="color:#fff">Tasks completed</b><small style="color:#b8cbd8">the checklist, ticked on site</small></span></li><li><span><b style="color:#fff">Photos</b><small style="color:#b8cbd8">taken at your pool that day, from the technician's phone</small></span></li><li><span><b style="color:#fff">Who did the work</b><small style="color:#b8cbd8">the technician's name, not a company signature</small></span></li></ul>
    <p>Photos have to be captured on site to be attached, so they can't be an old picture pulled from a camera roll. That constraint is the whole point.</p></div>
  %s
</div></section>

<section class="sec"><div class="wrap split">
  %s
  <div class="reveal"><div class="eyebrow">Beyond the weekly route</div><h2>Repairs and one-off work</h2><p>Quoted before any work starts, and billed separately from your monthly plan. We would rather tell you a part has two years left than replace it today.</p>
    <ul class="checks" style="margin-top:20px"><li><span><b>Equipment repair</b><small>Pumps, motors, heaters, salt cells, filters, timers and automation. Diagnosed on site and quoted before we order anything.</small></span></li><li><span><b>Green-pool recovery</b><small>Quoted as a one-off based on what we find. Once the water is clear and stable we can put the pool onto a weekly plan.</small></span></li><li><span><b>Filter cleans and openings</b><small>Cartridge and DE cleans, and a full equipment check before you arrive for the season if the house sits empty part of the year.</small></span></li></ul></div>
</div></section>

<section class="sec sky"><div class="wrap"><div class="head c reveal"><div class="eyebrow">Questions</div><h2>Straight answers</h2></div>%s</div></section>
%s""" % (img(r, "services-hero", "", "bg", "100vw", True), TEL, PHONE, plans(r), table, TEL,
         img(r, "away", "Two lounge chairs facing a pool", "photo"), img(r, "visit-water", "Sunlight patterns on clear pool water over tile"), img(r, "visit-surface", "Pool tile line at the waterline"), img(r, "visit-equipment", "Technician working on equipment"),
         report(), img(r, "repairs", "Water filtration tanks and plumbing", "photo"), faq(SVC_FAQ), band(r, "about-facts"))
    return page("services-and-plans", "Pool Service Plans & Pricing | Blue Halo", "Three weekly pool service plans from $129/mo, each quoted on your pool before you commit. Halo Away visits from $50. Repairs quoted first.", body, "services-and-plans/", True, [BIZ, faq_ld(SVC_FAQ)])

def about():
    r = "../"
    body = """
<section class="phero">%s<div class="wrap"><div class="eyebrow">About</div><h1>A small pool route, run properly</h1>
<p>Blue Halo Pools services residential pools across Palm Beach County. We've been doing it since 2019, and the owner is still on the route rather than behind a desk.</p></div></section>
<section class="sec"><div class="wrap">
  <div class="head c reveal"><div class="eyebrow">What we believe</div><h2>Four things we do differently</h2></div>
  <div class="cards4">
    <div class="card reveal"><div class="ic">01</div><h3>We show our work</h3><p>Readings and photos in your inbox after every visit, whether you ask for them or not.</p></div>
    <div class="card reveal"><div class="ic">02</div><h3>We quote first</h3><p>You know the monthly rate before we touch the pool, and a repair price before we order a part.</p></div>
    <div class="card reveal"><div class="ic">03</div><h3>We leave proof</h3><p>Readings, what we added and photos from your pool, emailed before we leave. Nothing to take on trust.</p></div>
    <div class="card reveal"><div class="ic">04</div><h3>We say no</h3><p>If your pool needs resurfacing rather than another year of chemicals, we tell you at the quote.</p></div>
  </div>
</div></section>
<section class="sec sky"><div class="wrap split top">
  <div class="reveal"><div class="eyebrow">The business, plainly</div><h2>Facts, for anyone checking</h2>
    <ul class="facts"><li><b>Business name</b><span>Blue Halo Pools</span></li><li><b>What we do</b><span>Weekly pool service, chemical programs and pool equipment repair. Mostly residential, plus a small number of HOA and commercial pools on the route.</span></li><li><b>Where</b><span>Palm Beach County, Florida — %s</span></li><li><b>Serving pools since</b><span>2019</span></li><li><b>How we work</b><span>We come to you. There's no walk-in location and no retail store.</span></li><li><b>Reach us</b><span><a href="tel:%s">%s</a> · <a href="mailto:%s">%s</a></span></li></ul></div>
  <div class="reveal"><div class="eyebrow">Have us look at your pool</div><h2>What happens next</h2><p>You send the form, a real person texts you back — usually the same day and normally within one business day. We ask a few questions about the pool, give you a rate, and if it works we put you on the next weekly cycle.</p><p>There's no contract to sign to get a price, and nobody will keep calling you if you decide against it.</p><p style="margin-top:24px"><a class="btn btn-blue" href="../quote/">Get a free quote</a></p></div>
</div></section>""" % (img(r, "about-hero", "", "bg", "100vw", True), ", ".join(CITIES[s]["name"] for s in ORDER), TEL, PHONE, EMAIL, EMAIL)
    return page("about", "About Blue Halo Pools | Palm Beach County Pool Service", "Blue Halo Pools services residential pools across Palm Beach County. Owner-run on the route since 2019.", body, "about/", schema=BIZ)

def areas():
    r = "../"
    opts = "".join('<option value="%s">%s</option>' % (s, CITIES[s]["name"]) for s in sorted(ORDER, key=lambda s: CITIES[s]["name"]))
    body = """
<section class="phero">%s<div class="wrap"><div class="eyebrow">Areas we serve</div><h1>Pool service across Palm Beach County</h1>
<p>Boca Raton up to Jupiter, the barrier islands out to Wellington. Wherever your pool is, it gets the same weekly service and the same report with readings and photos.</p>
<div class="finder"><label for="finder" class="eyebrow" style="flex-basis:100%%;color:#7fd0f5">Check if we cover you</label><select id="finder"><option value="">Choose your town</option>%s<option value="other">My town isn't listed</option></select><div class="res" id="fres" aria-live="polite" style="color:#fff"></div></div></div></section>
<section class="sec"><div class="wrap">
  <div class="head reveal"><div class="eyebrow">Cities we cover</div><h2>Where we work</h2><p>Each city has its own page covering what we actually see there, because a screened pool under oaks in west Boca, a well-water pool in Jupiter Farms and an oceanfront pool in Highland Beach are three genuinely different jobs.</p></div>
  <div class="cities reveal">%s</div>
</div></section>
<section class="sec sky"><div class="wrap split top">
  <div class="reveal"><div class="eyebrow">How the schedule works</div><h2>Routes are built by geography</h2><p>Pools near each other are serviced together. A tight route is what keeps the drive time out of your rate, and it is why we quote by address rather than off a price list.</p><p>It also means the honest answer about scheduling depends on where you are. When you call, we'll tell you which day we run near you and when we could start, rather than promising tomorrow and sorting it out afterwards.</p></div>
  <div class="reveal"><div class="eyebrow">Tell us where the pool is</div><h2>Don't see your city?</h2><p>Palm Beach County has more towns than we have pages. Send the address through and we'll tell you which day we run near you and when we could start, at no cost and with no follow-up if it isn't for you.</p><p>If we can't take your pool, we'll point you at someone local who can. It costs us nothing and it is what we would want.</p><p style="margin-top:24px"><a class="btn btn-blue" href="../quote/">Get a free quote</a></p></div>
</div></section>""" % (img(r, "areas-hero", "", "bg", "100vw", True), opts, city_cards(r, ORDER))
    return page("areas-we-serve", "Pool Service Areas in Palm Beach County | Blue Halo", "Weekly pool service from Boca Raton up to Jupiter and out to Wellington. Check if we cover your town.", body, "areas-we-serve/", schema=BIZ)

def quote():
    r = "../"
    body = """
<section class="phero" style="padding-bottom:0">%s<div class="wrap" style="padding-bottom:70px"><div class="eyebrow">Get a free quote</div><h1>Get a free pool service quote</h1><p>A few taps and your address, and we text you a real monthly rate — usually within the hour.</p></div></section>
<section class="sec sky" style="padding-top:60px"><div class="wrap">%s
  <div class="cards3" style="margin-top:60px">
    <div class="card reveal"><div class="eyebrow">After you send it</div><h3>We price it.</h3><p>From what you told us, against your address on the route.</p></div>
    <div class="card reveal"><div class="eyebrow">Then</div><h3>You get a text.</h3><p>A real number, usually within the hour.</p></div>
    <div class="card reveal"><div class="eyebrow">Finally</div><h3>Say yes.</h3><p>We enroll you and you're on the next weekly cycle.</p></div>
  </div>
  <div class="split top" style="margin-top:60px">
    <div class="reveal"><div class="eyebrow">Either way you get</div><ul class="checks" style="margin-top:12px"><li><span><b>Weekly service, year round</b></span></li><li><span><b>Readings and photos after every visit</b></span></li><li><span><b>Month to month, 30 days' notice</b></span></li><li><span><b>Referral bonuses when you send us a neighbor</b></span></li></ul></div>
    <div class="reveal"><div class="eyebrow">Where we work</div><p>Palm Beach County, from Boca Raton up to Jupiter and west to Wellington. We service pools at customers' homes and don't operate a walk-in location.</p><p>Outside the county line? Call us or send the form through anyway — we'll tell you honestly whether we can reach you, and we often can.</p></div>
  </div>
</div></section>""" % (img(r, "quote", "", "bg", "100vw", True), quote_block(r))
    return page("quote", "Get a Free Pool Service Quote | Blue Halo Pools", "Price your pool in two minutes. A real person texts you a monthly rate, usually within the hour.", body, "", schema=BIZ)

def careers():
    r = "../"
    body = """
<section class="phero">%s<div class="wrap"><div class="eyebrow">Careers</div><h1>Work on our route</h1><p>We service residential pools across Palm Beach County. When we're hiring, every open role is listed here with the pay, the area and how to apply.</p></div></section>
<section class="sec"><div class="wrap"><div class="head reveal"><div class="eyebrow">Open roles</div><h2>Hiring now</h2></div>
  <div class="card reveal" style="margin-top:30px"><div class="role"><div><h3 style="margin:0">Pool Service Technician II</h3><p>Independent contractor (1099) · South Palm Beach County: Lake Worth, Boynton Beach, Delray Beach, Boca Raton · About $3,000–$4,500 a month</p></div><a class="btn btn-blue" href="pool-service-technician/">See the role</a></div></div>
  <p class="reveal" style="margin-top:24px;color:var(--mut)">To apply, email your resume to <a href="mailto:careers@bluehalopools.com" style="color:var(--deep);font-weight:600">careers@bluehalopools.com</a> with the role in the subject line. Questions first? Call or text <a href="tel:%s" style="color:var(--deep);font-weight:600">%s</a>.</p>
</div></section>""" % (img(r, "careers-hero", "", "bg", "100vw", True), TEL, PHONE)
    return page("careers", "Careers at Blue Halo Pools | Palm Beach County", "Open roles at Blue Halo Pools, with the pay, the area and how to apply.", body, "careers/")

def role():
    r = "../../"
    body = """
<section class="phero">%s<div class="wrap"><div class="crumbs"><a href="../">Careers</a> / Pool Service Technician II</div><div class="eyebrow">Now hiring · South Palm Beach County</div><h1>Pool Service Technician II</h1>
<p>Run one of our established residential routes across Lake Worth, Boynton Beach, Delray Beach and Boca Raton. Two weeks of paid onboarding, then the route is yours.</p>
<div class="row"><a class="btn btn-blue" href="mailto:careers@bluehalopools.com?subject=Pool%%20Service%%20Technician%%20II">Apply by email</a><a class="btn btn-ghost" href="tel:%s">Questions? %s</a></div></div></section>
<section class="sec sky"><div class="wrap">
  <div class="metrics reveal" style="margin-top:0"><div><b>$3,000–$4,500/mo</b><span>depending on route size and experience</span></div><div><b>12–17 stops a day</b><span>Monday to Friday</span></div><div><b>Own truck preferred</b><span>we cover fuel, chemicals and equipment</span></div><div><b>Independent contractor</b><span>1099, with paid onboarding</span></div></div>
  <div class="split top" style="margin-top:60px">
    <div class="reveal"><div class="eyebrow">The route</div><h2>What you'll do</h2><ul class="checks" style="margin-top:16px"><li><span><b>Service 12–17 residential pools a day, Monday through Friday</b></span></li><li><span><b>Test and balance water; brush, vacuum, net and empty baskets</b></span></li><li><span><b>Clean filters on schedule and log every visit in our route app</b></span></li><li><span><b>Inspect equipment and write up anything failing so the repair can be quoted</b></span></li><li><span><b>Flag add-on work and talk with homeowners professionally when they're home</b></span></li></ul><p>Equipment repair and replacement are not part of this role. You catch problems, document them and hand them off.</p></div>
    <div class="reveal"><div class="eyebrow">Who we're looking for</div><h2>What you bring</h2><ul class="checks" style="margin-top:16px"><li><span><b>2+ years</b><small>running a residential pool route</small></span></li><li><span><b>Working command of pool chemistry</b><small>and able to clear algae, cloudy water and staining on your own</small></span></li><li><span><b>Can identify pumps, filters, heaters and automation</b><small>and describe what's failing</small></span></li><li><span><b>Valid Florida driver's license</b><small>and a clean driving record</small></span></li><li><span><b>Authorized to work in the U.S.</b><small>and able to provide a W-9</small></span></li></ul><p><b>Nice to have:</b> your own truck insured for business use (a company vehicle is available for top candidates), a CPO certification (or we pay for it), and saltwater, variable-speed pump or equipment repair experience.</p></div>
  </div>
</div></section>
<section class="sec"><div class="wrap" style="max-width:860px">
  <div class="reveal"><div class="eyebrow">What we provide</div><h2>Built so you can focus on the pools</h2><ul class="checks" style="margin-top:16px"><li><span><b>Your truck, our supplies</b><small>Start and end at home. We cover route fuel with a weekly allowance and supply the chemicals and equipment.</small></span></li><li><span><b>Tighter routes</b><small>Stops are sequenced to cut drive time, and we keep refining them so your day gets shorter.</small></span></li><li><span><b>Direct line to the owner</b><small>No dispatcher and no call center. You work with the person who built the route.</small></span></li><li><span><b>An app for the paperwork</b><small>Stops and directions laid out for you. Log chemicals and notes at each pool, with no end-of-day catch-up.</small></span></li></ul></div>
</div></section>
<section class="sec dark"><div class="wrap"><div class="head c reveal"><div class="eyebrow">Apply</div><h2>Ready to run a route?</h2><p>Email your resume with a short note on where you've run routes and how many stops a day you carried. Level II is our experienced tier, so we pay for the years you already have, and every technician is eligible for discretionary performance incentives.</p>
<p style="margin-top:24px"><a class="btn btn-blue" href="mailto:careers@bluehalopools.com?subject=Pool%%20Service%%20Technician%%20II">Apply by email</a> <a class="btn btn-ghost" href="tel:%s">Call or text %s</a></p>
<p style="margin-top:24px;font-size:13px">Blue Halo Pools engages contractors without regard to race, color, religion, sex, national origin, age, disability, or genetic information.</p></div></div></section>""" % (
        img(r, "careers-role", "", "bg", "100vw", True), TEL, PHONE, TEL, PHONE)
    return page("careers/pool-service-technician", "Pool Service Technician II, Palm Beach County | Blue Halo", "Run an established residential pool route in South Palm Beach County. $3,000–$4,500/mo, paid onboarding.", body, "careers/")

def city(slug, photo):
    c = CITIES[slug]; r = "../"
    i = ORDER.index(slug); nearby = [ORDER[(i + k) % len(ORDER)] for k in (1, 2, 3, -1, -2, -3)]
    wrong = "".join('<div class="card reveal"><div class="ic">%d</div><h3>%s</h3><p>%s</p></div>' % (n + 1, E(t), E(d)) for n, (t, d) in enumerate(c["wrong"]))
    body = """
<section class="phero">%s<div class="wrap"><div class="crumbs"><a href="../">Home</a> / <a href="../areas-we-serve/">Areas</a> / %s</div><div class="eyebrow">Pool service · %s, FL</div><h1>Weekly pool service in %s</h1><p>%s</p>
<div class="row"><a class="btn btn-blue" href="../quote/">Get a free quote</a><a class="btn btn-ghost" href="tel:%s">Call %s</a></div></div></section>
<section class="sec"><div class="wrap"><div class="head reveal"><div class="eyebrow">Pools in %s</div><h2>%s</h2><p>%s</p><p>%s</p></div></div></section>
<section class="sec sky"><div class="wrap"><div class="head reveal"><div class="eyebrow">Local know-how</div><h2>%s</h2></div><div class="cards3">%s</div></div></section>
<section class="sec dark"><div class="wrap split">
  <div class="reveal"><div class="eyebrow">The Pool Health Report</div><h2>Proof after every visit</h2><p>You get a Pool Health Report by email the moment we finish: the readings taken at your pool, what we added, what we did, and photos shot on site that day.</p></div>
  %s
</div></section>
<section class="sec"><div class="wrap split top">
  <div class="reveal"><div class="eyebrow">Pricing in %s</div><h2>Quoted on your pool</h2><p>%s</p><p>%s</p><p style="margin-top:24px"><a class="btn btn-blue" href="../quote/">Get a free quote</a></p></div>
  <div class="reveal"><div class="eyebrow">Pool service in %s</div><h2>Questions</h2>%s</div>
</div></section>
<section class="sec sky"><div class="wrap"><div class="head reveal"><div class="eyebrow">Nearby</div><h2>We also service</h2></div><div class="cities reveal">%s</div></div></section>
<section class="sec" style="padding:80px 0"><div class="wrap" style="text-align:center"><h2 class="reveal" style="font-size:clamp(30px,3.6vw,46px)">%s</h2><p class="reveal" style="margin-top:22px"><a class="btn btn-blue" href="../quote/">Get a free quote</a> <a class="btn btn-line" href="tel:%s">Call %s</a></p></div></section>""" % (
        img(r, photo, "Residential pool in the %s area" % c["name"], "bg", "100vw", True), c["name"], c["name"], c["name"], E(c["sub"]), TEL, PHONE,
        c["name"], E(c["h2"]), E(c["p"][0]), E(c["p"][1]), E(c["h_wrong"]), wrong, report(),
        c["name"], E(c["price"][0]), E(c["price"][1]), c["name"], faq(c["faq"]).replace('class="faq"', 'class="faq" style="margin-top:16px"'),
        city_cards(r, nearby), E(c["cta"]), TEL, PHONE)
    ld = dict(BIZ); ld["areaServed"] = {"@type": "City", "name": c["name"] + ", FL"}
    return page(slug, c["title"], c["sub"], body, "areas-we-serve/", True, [ld, faq_ld(c["faq"])])

def privacy():
    r = "../"
    raw = open(os.path.join(HERE, "privacy.html"), encoding="utf-8").read()
    body = '<section class="phero" style="padding-bottom:0"><div class="wrap" style="padding:90px 24px 60px"><div class="eyebrow">Effective August 30, 2026</div><h1>Privacy policy</h1></div></section><section class="sec"><div class="wrap legal" style="max-width:820px">%s</div></section>' % raw
    return page("privacy", "Privacy Policy | Blue Halo Pools", "What Blue Halo Pools collects when you ask for a quote or become a customer, and what we will never do with it.", body)

def main():
    USED.clear()
    open(os.path.join(OUT, "site.css"), "w").write(CSS)
    open(os.path.join(OUT, "site.js"), "w").write(JS)
    pages = {"": home(), "services-and-plans": services(), "about": about(), "areas-we-serve": areas(), "quote": quote(),
             "careers": careers(), "careers/pool-service-technician": role(), "privacy": privacy()}
    for slug in ORDER: pages[slug] = city(slug, "city-" + slug.replace("pool-service-", ""))
    for path, doc in pages.items():
        d = os.path.join(OUT, path); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)
    dup = [n for n in set(USED) if USED.count(n) > 1]
    print("built %d pages -> %s | photos used: %d | duplicates: %s" % (len(pages), OUT, len(USED), dup or "none"))

if __name__ == "__main__":
    main()
