#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
W Employment Law — static site generator
=========================================

Owns the shared shell (head / utility bar / nav / footer / scripts) for the W Employment
Law site and renders every page from it, so the whole site shares one look, one nav, one
footer, and one tracking setup. Run it from anywhere:

    python3 sitegen/custom/wemploymentlaw/build.py

It writes into ``public/wemploymentlaw/`` (relative to the webblaze repo root). It is safe
to re-run any time — it only ever (re)writes the files it owns (see OUTPUT below) and never
touches img/, styles.css, or i18n.js.

URL STRUCTURE
-------------
Every real page is a **folder with an index.html** (e.g. ``contact/index.html``), mirroring
the old wemploymentlaw.com WordPress URLs 1:1 so no Google ranking/traffic is lost on
go-live. All internal links and asset references are **relative**, computed from how deep
the page sits (e.g. ``../../styles.css``), so the exact same output works both at
``https://webblaze.io/wemploymentlaw/`` (preview) and at the domain root
``https://wemploymentlaw.com/`` after go-live — no path rewriting needed, just flip
GO_LIVE below and rebuild.

GO-LIVE
-------
Flip ``GO_LIVE = True`` below, re-run this script, redeploy. That's the single switch that
changes BASE_URL (used for canonical/OG/sitemap/JSON-LD) from the webblaze.io preview to
the real domain. See WEL-HANDOFF.md for the full go-live checklist.

THE page() API
---------------
    page(path, title, description, body_html, *,
         h1=None, eyebrow=None, es_h1=None, es_eyebrow=None,
         breadcrumbs=None, schema=None, es=None, og_image=None,
         extra_head='', extra_scripts='')

    path          site-root path, starting AND ending with '/': '/', '/contact/',
                  '/wrongful-termination/', '/blog/my-post-slug/' ...
                  Written to public/wemploymentlaw/<path-without-leading-slash>index.html
    title         <title> text (plain, no " | W Employment Law" suffix needed — added
                  automatically unless the title already contains "W Employment Law").
    description   meta description / og:description / twitter:description (~155 chars).
    body_html     raw HTML for everything between the nav and the footer. May reference
                  these tokens, which get swapped for the correct *relative* link for THIS
                  page's depth automatically:
                    {{HOME}} {{CONTACT}} {{PRACTICE}} {{ABOUT}} {{CALC}} {{BLOG}}
                    {{PRIVACY}} {{TERMS}} {{OUR_TEAM}} {{WHY_US}} {{VIDEOS}}
                    {{CLASS_ACTION}} {{WORK_REIMBURSEMENTS}} {{LAW_GUIDES}}
                    {{IMG}}   -> relative prefix to the site root, so write {{IMG}}img/foo.jpg
                  Add new entries to PATHS below as new sections of the site are built.
    h1 / eyebrow  if given, page() auto-renders the standard teal ".phead" banner (same
                  look as practice-areas/calculator/blog/jacob pages) BEFORE body_html, so
                  new pages don't need to hand-roll that markup. Pass es_h1/es_eyebrow for
                  the Spanish (data-es) version. Pages that build their own hero (home,
                  the 5 migrated pages) just omit h1 and put everything in body_html.
    breadcrumbs   optional list of (label, path_or_None) tuples rendered inside the phead
                  (only used when h1 is also given). Last tuple's path should be None.
    schema        optional dict of extra JSON-LD to emit IN ADDITION to the default
                  LegalService schema (e.g. a FAQPage or Article dict) — appended as a
                  second <script type="application/ld+json"> block.
    es            optional dict {'h1': '...', 'eyebrow': '...', 'description': '...'} —
                  Spanish text for the auto-phead and the meta description's data-es twin
                  (meta tags themselves aren't translated by i18n.js, only on-page text is).
    og_image      override the default og:image (jacob-share.jpg).
    extra_head    raw HTML appended inside <head> (e.g. a page-specific <link>).
    extra_scripts raw HTML appended just before </body> (e.g. a page-specific <script>).

Every call to page() also registers the path for sitemap.xml / robots.txt generation —
nothing else to do. Call register_json_pages() (done automatically in build()) to also
pull in any sitegen/custom/wemploymentlaw/content/*.json pages the crawler/next agent adds
(see JSON PAGE SCHEMA below) — drop a .json file in content/ and it gets its own page next
build, no code changes needed.

JSON PAGE SCHEMA  (content/<slug>.json)
----------------------------------------
IMPORTANT: the crawler drops RAW scraped data into content/*.json (old_url, title_tag,
meta_description, h1, body_html straight from the old WordPress markup, images[], etc.) —
that is reference material for a human/agent to rewrite from, NOT something this build
should auto-publish verbatim (it's unstyled WP markup, not matched to this design system,
and the whole point of ITEM 1 is hand-authored pages that look like the rest of the site).
So register_json_pages() below only republishes a JSON file as a real page once it has
been turned into **page-ready** JSON: add "page_ready": true plus this shape, then rebuild:

    {
      "page_ready": true,
      "path": "/our-team/",
      "title": "Our Team",
      "description": "...",
      "h1": "Meet Our Team",
      "eyebrow": "About the firm",
      "es_h1": "...", "es_eyebrow": "...",
      "breadcrumbs": [["Home", "/"], ["About", "/jacob-n-whitehead/"], ["Our Team", null]],
      "body_html": "<section class=\"sec\">...</section>"   <- styled HTML using this
                                                                 site's existing classes
                                                                 (.sec, .wrap, .phead, etc.)
    }

Any content/*.json WITHOUT "page_ready": true (i.e. every file the crawler writes) is
counted and skipped with a one-line summary — never crashes the build, and never
publishes raw/unstyled content.

REDIRECT STUBS
---------------
The 5 old flat files (about.html, contact.html, practice-areas.html, calculator.html,
blog.html) are replaced with tiny stub pages (meta refresh + canonical + JS
location.replace) pointing at the new folder URLs, so any link already emailed to the
client, bookmarked, or indexed keeps working. See OLD_FLAT_REDIRECTS below.

OUTPUT
------
  public/wemploymentlaw/index.html                  (home)
  public/wemploymentlaw/contact/index.html
  public/wemploymentlaw/practice-areas/index.html
  public/wemploymentlaw/blog/index.html
  public/wemploymentlaw/jacob-n-whitehead/index.html
  public/wemploymentlaw/calculator/index.html
  public/wemploymentlaw/{about,contact,practice-areas,calculator,blog}.html   (redirect stubs)
  public/wemploymentlaw/sitemap.xml
  public/wemploymentlaw/robots.txt
  public/wemploymentlaw/_redirects
  + one folder/index.html per content/*.json page
"""

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent                     # sitegen/custom/wemploymentlaw
WEBBLAZE_ROOT = ROOT.parent.parent.parent                           # webblaze/
OUT = WEBBLAZE_ROOT / "public" / "wemploymentlaw"
PAGES_DIR = ROOT / "pages"
CONTENT_DIR = ROOT / "content"

# ---------------------------------------------------------------------------
# GO-LIVE SWITCH — the one thing to flip when moving to the client's domain.
# ---------------------------------------------------------------------------
GO_LIVE = False
BASE_URL = "https://wemploymentlaw.com/" if GO_LIVE else "https://webblaze.io/wemploymentlaw/"

# ---------------------------------------------------------------------------
# Verified real facts (see WEL-HANDOFF.md "Verified real facts" — never fabricate).
# ---------------------------------------------------------------------------
PHONE_DISPLAY = "888-492-0633"
PHONE_TEL = "+18884920633"
EMAIL = "contact@wemploymentlaw.com"
ADDRESS_HTML = "7700 Irvine Center Drive, Suite 800<br>Irvine, CA 92618"
ADDRESS_PLAIN = "7700 Irvine Center Drive, Suite 800, Irvine, CA 92618"

SOCIAL = {
    "facebook": "https://www.facebook.com/wemploymentlaw",
    "instagram": "https://www.instagram.com/wemploymentlaw/",
    "youtube": "https://www.youtube.com/channel/UCmUnEU5NU5jlZQTVZqrRhRQ",
    "tiktok": "https://www.tiktok.com/@employmentattorney",
    "linkedin": "https://www.linkedin.com/company/w-e-law",
}

GA4_ID = "G-6BN0TWE10Q"
META_PIXEL_ID = "2130487443675029"
HS_PORTAL = "7690372"
HS_FORM_ID = "460ba517-6b2d-47cc-9f1d-379c4bd53ee4"  # the one real form w/ message field; see WEL-HANDOFF.md

# ---------------------------------------------------------------------------
# PATHS — logical name -> site-root path. Mirrors the old WordPress site's URL slugs
# (verified via https://wemploymentlaw.com/page-sitemap.xml). Add to this as new sections
# are built; everything else (nav, footer, {{TOKEN}} substitution) reads from here.
# ---------------------------------------------------------------------------
PATHS = {
    "home": "/",
    "contact": "/contact/",
    "practice-areas": "/practice-areas/",
    "about": "/jacob-n-whitehead/",
    "calculator": "/calculator/",
    "blog": "/blog/",
    "our-team": "/our-team/",
    "why-choose-us": "/why-choose-us/",
    "videos": "/videos/",
    "law-guides": "/free-law-guides/",
    "privacy": "/privacy-policy/",
    "terms": "/terms-of-use/",
    "pricing": "/pricing/",
    "referrals": "/referrals/",
    "class-action": "/california-employee-class-action-attorneys/",
    "work-reimbursements": "/work-related-reimbursements/",
    "wrongful-termination": "/wrongful-termination/",
    "discrimination": "/discrimination/",
    "sexual-harassment": "/sexual-harassment/",
    "overtime-violations": "/overtime-violations/",
    "meal-breaks": "/meal-breaks-and-rest-breaks/",
    "pregnancy-discrimination": "/pregnancy-discrimination/",
    "medical-leave-disability": "/medical-leave-disability/",
    "whistleblower-protection": "/whistleblower-protection/",
    "independent-contractors": "/independent-contractors/",
}

# Token name (used in page fragments) -> PATHS key
TOKEN_MAP = {
    "HOME": "home", "CONTACT": "contact", "PRACTICE": "practice-areas",
    "ABOUT": "about", "CALC": "calculator", "BLOG": "blog",
    "PRIVACY": "privacy", "TERMS": "terms", "OUR_TEAM": "our-team",
    "WHY_US": "why-choose-us", "VIDEOS": "videos",
    "CLASS_ACTION": "class-action", "WORK_REIMBURSEMENTS": "work-reimbursements",
    "LAW_GUIDES": "law-guides",
}

# Nav structure: (label, en-es pair, path-key, [children...]). Children same shape w/o grandchildren.
NAV = [
    {"label": "Home", "es": "Inicio", "key": "home"},
    {"label": "Practice Areas", "es": "Áreas de Práctica", "key": "practice-areas", "children": [
        {"label": "All Practice Areas", "es": "Todas las Áreas", "key": "practice-areas"},
        {"label": "Wrongful Termination", "es": "Despido Injustificado", "key": "wrongful-termination"},
        {"label": "Discrimination", "es": "Discriminación", "key": "discrimination"},
        {"label": "Sexual Harassment", "es": "Acoso Sexual", "key": "sexual-harassment"},
        {"label": "Unpaid Wages & Overtime", "es": "Salarios y Horas Extra", "key": "overtime-violations"},
        {"label": "Meal & Rest Breaks", "es": "Descansos y Comidas", "key": "meal-breaks"},
        {"label": "Pregnancy Discrimination", "es": "Discriminación por Embarazo", "key": "pregnancy-discrimination"},
        {"label": "Medical Leave & Disability", "es": "Licencia Médica y Discapacidad", "key": "medical-leave-disability"},
        {"label": "Whistleblower Retaliation", "es": "Represalias por Denunciar", "key": "whistleblower-protection"},
        {"label": "Contractor Misclassification", "es": "Clasificación Errónea", "key": "independent-contractors"},
        {"label": "Class Action & PAGA", "es": "Demandas Colectivas y PAGA", "key": "class-action"},
        {"label": "Work Expense Reimbursements", "es": "Reembolsos de Gastos Laborales", "key": "work-reimbursements"},
    ]},
    {"label": "About", "es": "Nosotros", "key": "about", "children": [
        {"label": "Jacob N. Whitehead", "es": "Jacob N. Whitehead", "key": "about"},
        {"label": "Our Team", "es": "Nuestro Equipo", "key": "our-team"},
        {"label": "Why Choose Us", "es": "Por Qué Elegirnos", "key": "why-choose-us"},
        {"label": "Videos", "es": "Videos", "key": "videos"},
    ]},
    {"label": "Resources", "es": "Recursos", "key": "blog", "children": [
        {"label": "Insights", "es": "Recursos", "key": "blog"},
        {"label": "Free Law Guides", "es": "Guías Legales Gratuitas", "key": "law-guides"},
        {"label": "Wage Calculator", "es": "Calculadora de Salarios", "key": "calculator"},
    ]},
    {"label": "Contact", "es": "Contacto", "key": "contact"},
]

# Old flat file -> new folder it now redirects to (relative, same depth: site root).
OLD_FLAT_REDIRECTS = {
    "about.html": "about",
    "contact.html": "contact",
    "practice-areas.html": "practice-areas",
    "calculator.html": "calculator",
    "blog.html": "blog",
}

PAGE_REGISTRY = []  # list of abs paths, populated by page()


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------
def depth(path):
    """Number of folders deep a site-root path sits. '/' -> 0, '/contact/' -> 1."""
    return 0 if path == "/" else path.strip("/").count("/") + 1


def rel(from_path, to_abs_path):
    """Relative href from `from_path` (a page's abs path) to `to_abs_path` (abs path or
    bare asset name like 'styles.css')."""
    d = depth(from_path)
    prefix = "../" * d
    if to_abs_path.startswith("/"):
        return prefix + to_abs_path.lstrip("/") if to_abs_path != "/" else (prefix or "./")
    return prefix + to_abs_path


def substitute_tokens(html, from_path):
    out = html
    for token, key in TOKEN_MAP.items():
        out = out.replace("{{%s}}" % token, rel(from_path, PATHS[key]))
    out = out.replace("{{IMG}}", "../" * depth(from_path))
    return out


def load_fragment(name):
    return (PAGES_DIR / f"{name}.html").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Shared shell pieces
# ---------------------------------------------------------------------------
SOCIAL_ICONS_SVG = {
    "facebook": '<svg viewBox="0 0 24 24"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.7 4.53-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.49 0-1.96.93-1.96 1.89v2.26h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23a3.7 3.7 0 0 1-.9 1.38 3.7 3.7 0 0 1-1.38.9c-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16M12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63a5.9 5.9 0 0 0-2.12 1.38A5.9 5.9 0 0 0 .63 4.14C.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.3.79.72 1.46 1.38 2.12.66.66 1.33 1.08 2.12 1.38.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56.79-.3 1.46-.72 2.12-1.38.66-.66 1.08-1.33 1.38-2.12.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91a5.9 5.9 0 0 0-1.38-2.12A5.9 5.9 0 0 0 19.86.63c-.76-.3-1.64-.5-2.91-.56C15.67.01 15.26 0 12 0m0 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84m0 10.16A4 4 0 1 1 16 12a4 4 0 0 1-4 4m6.41-10.85a1.44 1.44 0 1 0 1.44 1.44 1.44 1.44 0 0 0-1.44-1.44"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24"><path d="M23.5 6.19a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 0 0 .5 6.19C0 8.08 0 12 0 12s0 3.92.5 5.81a3.02 3.02 0 0 0 2.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 0 0 2.12-2.14C24 15.92 24 12 24 12s0-3.92-.5-5.81M9.55 15.57V8.43L15.82 12z"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.95v5.66H9.34V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.38-1.85 3.6 0 4.27 2.37 4.27 5.46zM5.34 7.43a2.07 2.07 0 1 1 0-4.13 2.07 2.07 0 0 1 0 4.13M7.12 20.45H3.56V9h3.56zM22.22 0H1.77C.8 0 0 .78 0 1.75v20.5C0 23.22.8 24 1.77 24h20.45c.98 0 1.78-.78 1.78-1.75V1.75C24 .78 23.2 0 22.22 0"/></svg>',
}

PHEAD_TMPL = """<section class="phead"><div class="wrap">
  {breadcrumbs}<span class="eyebrow"{eyebrow_es}>{eyebrow}</span>
  <h1{h1_es}>{h1}</h1>
</div></section>
"""


def _es_attr(text):
    return f' data-es="{text}"' if text else ""


def render_phead(h1, eyebrow, breadcrumbs, es_h1, es_eyebrow, from_path):
    bc_html = ""
    if breadcrumbs:
        parts = []
        for label, bpath in breadcrumbs:
            if bpath:
                parts.append(f'<a href="{rel(from_path, bpath)}">{label}</a>')
            else:
                parts.append(f"<span>{label}</span>")
        bc_html = '<div class="bc">' + ' <span>/</span> '.join(parts) + "</div>\n  "
    return PHEAD_TMPL.format(
        breadcrumbs=bc_html,
        eyebrow=eyebrow or "", eyebrow_es=_es_attr(es_eyebrow),
        h1=h1 or "", h1_es=_es_attr(es_h1),
    )


def render_nav(from_path):
    items = []
    for item in NAV:
        href = rel(from_path, PATHS[item["key"]])
        if item.get("children"):
            kids = "".join(
                f'<a href="{rel(from_path, PATHS[c["key"]])}" data-es="{c["es"]}">{c["label"]}</a>'
                for c in item["children"]
            )
            items.append(
                f'<div class="nav-item has-drop"><a href="{href}" data-es="{item["es"]}" '
                f'aria-haspopup="true">{item["label"]} <span class="car">▾</span></a>'
                f'<div class="nav-drop" role="menu">{kids}</div></div>'
            )
        else:
            items.append(f'<div class="nav-item"><a href="{href}" data-es="{item["es"]}">{item["label"]}</a></div>')
    nav_links = "".join(items)
    home_href = rel(from_path, PATHS["home"])
    contact_href = rel(from_path, PATHS["contact"])
    img_prefix = "../" * depth(from_path)
    return f"""<!-- UTILITY BAR -->
<div class="util"><div class="wrap util-in">
  <span data-es="Al servicio de los empleados en todo California">Serving employees across all of California</span>
  <div class="u-r"><span class="dot">●</span> <span data-es="Disponibles 24/7">Available 24/7</span> <span>·</span> Hablamos Español <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div>
</div></div>

<!-- NAV -->
<header class="nav" id="nav"><div class="wrap nav-in">
  <a class="brand" href="{home_href}"><img src="{img_prefix}img/logo.png" alt="W Employment Law" class="brand-logo"></a>
  <nav class="nav-links">
    {nav_links}
  </nav>
  <div class="nav-r"><button class="langtog" id="langtog" type="button" aria-label="Switch to Spanish" onclick="toggleLang()"><span class="l-en active">EN</span><span class="l-es">ES</span></button>
    <a class="ph" href="tel:{PHONE_TEL}"><svg class="ico" viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2z"/></svg> {PHONE_DISPLAY}</a>
    <a class="btn btn-gold" href="{contact_href}" data-es="Consulta Gratis">Free Case Review</a>
    <button class="hamb" aria-label="Menu" onclick="document.getElementById('nav').classList.toggle('open')">&#9776;</button>
  </div>
</div></header>
"""


def render_social_band():
    icons = "".join(
        f'<a href="{SOCIAL[k]}" target="_blank" rel="noopener" aria-label="{k.title()}">{SOCIAL_ICONS_SVG[k]}</a>'
        for k in ("facebook", "instagram", "youtube", "tiktok", "linkedin")
    )
    return f"""<div class="f-social"><div class="wrap">
  <h3 data-es="Síganos">Follow Us</h3>
  <div class="ic">{icons}</div>
</div></div>
"""


def render_footer(from_path):
    practice_href = rel(from_path, PATHS["practice-areas"])
    calc_href = rel(from_path, PATHS["calculator"])
    blog_href = rel(from_path, PATHS["blog"])
    about_href = rel(from_path, PATHS["about"])
    contact_href = rel(from_path, PATHS["contact"])
    privacy_href = rel(from_path, PATHS["privacy"])
    terms_href = rel(from_path, PATHS["terms"])
    img_prefix = "../" * depth(from_path)
    return f"""<!-- FOOTER -->
<footer><div class="wrap">
  <div class="f-cols">
    <div>
      <img src="{img_prefix}img/logo-white.png" alt="W Employment Law" class="brand-logo-f">
      <p style="margin-top:16px;max-width:40ch" data-es="Defendiendo a los empleados de California contra el despido injustificado, la discriminación, el acoso y el robo de salarios. Sin Ganar, Sin Honorarios.">Standing up for California employees against wrongful termination, discrimination, harassment, and wage theft. No Win, No Fee.</p>
      <div class="row-i"><span class="g"><svg class="ico" viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2z"/></svg></span><a href="tel:{PHONE_TEL}" style="font-weight:800;color:#fff">{PHONE_DISPLAY}</a></div>
      <div class="row-i"><span class="g"><svg class="ico" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg></span><a href="mailto:{EMAIL}" style="color:#fff">{EMAIL}</a></div>
      <div class="row-i"><span class="g"><svg class="ico" viewBox="0 0 24 24"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></span><span>{ADDRESS_HTML}</span></div>
      <div class="row-i"><span class="g"><svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span><span data-es="Disponibles 24/7 · Hablamos Español">Available 24/7 · Hablamos Español</span></div>
    </div>
    <div><h4 data-es="Sitio">Site</h4>
      <a href="{practice_href}" data-es="Áreas de Práctica">Practice Areas</a><a href="{calc_href}" data-es="Calculadora de Salarios">Wage Calculator</a><a href="{blog_href}" data-es="Recursos">Insights</a><a href="{about_href}" data-es="Nosotros">About</a><a href="{contact_href}" data-es="Contacto">Contact</a>
      <a href="{privacy_href}" data-es="Política de Privacidad">Privacy Policy</a><a href="{terms_href}" data-es="Términos de Uso">Terms of Use</a>
    </div>
    <div><h4 data-es="Revisión Gratuita">Free Case Review</h4>
      <p style="margin:0 0 14px;max-width:34ch" data-es="Díganos qué pasó, un abogado se comunicará con usted. Gratis y confidencial.">Tell us what happened — an attorney will reach out. Free &amp; confidential.</p>
      <a class="btn btn-gold" href="{contact_href}" data-es="Iniciar Mi Revisión Gratuita →">Start My Free Review →</a>
    </div>
  </div>
  <div class="disc">© <span id="yr"></span> W Employment Law. <span data-es="<b>Publicidad de Abogados.</b> La información de este sitio web tiene fines informativos generales únicamente y no pretende ser, ni debe tomarse como, asesoría legal para ningún caso o situación individual. Esta información no pretende crear, y su recepción o visualización no constituye, una relación abogado-cliente. Los resultados anteriores no garantizan un resultado similar. Los testimonios reflejan experiencias individuales de clientes y no garantizan resultados futuros."><b>Attorney Advertising.</b> The information on this website is for general informational purposes only and is not intended to be, and should not be taken as, legal advice for any individual case or situation. This information is not intended to create, and receipt or viewing does not constitute, an attorney-client relationship. Prior results do not guarantee a similar outcome. Testimonials reflect individual client experiences and are not a guarantee of future results.</span></div>
</div></footer>

<div class="mbar"><a class="btn btn-teal" href="tel:{PHONE_TEL}"><svg class="ico" viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2z"/></svg> <span data-es="Llamar Ahora">Call Now</span></a><a class="btn btn-gold" href="{contact_href}"><span data-es="Revisión Gratis">Free Review</span></a></div>
"""


TRACKING_JS = f"""
<script>
/* Tracking: only fires on the real client domain, never on the webblaze.io preview. */
(function(){{
  if(!/(^|\\.)wemploymentlaw\\.com$/.test(location.hostname)) return;
  window.dataLayer=window.dataLayer||[];
  function gtag(){{dataLayer.push(arguments);}}
  window.gtag=gtag;
  var g=document.createElement('script');g.async=true;g.src='https://www.googletagmanager.com/gtag/js?id={GA4_ID}';document.head.appendChild(g);
  gtag('js',new Date());gtag('config','{GA4_ID}');

  !function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
  fbq('init','{META_PIXEL_ID}');fbq('track','PageView');

  var hs=document.createElement('script');hs.id='hs-script-loader';hs.async=true;hs.defer=true;hs.src='https://js.hs-scripts.com/{HS_PORTAL}.js';document.body.appendChild(hs);
}})();
function welTrackLead(){{
  try{{if(window.gtag)gtag('event','generate_lead');}}catch(e){{}}
  try{{if(window.fbq)fbq('track','Lead');}}catch(e){{}}
}}
</script>
"""

COMMON_SCRIPT = """
<script>
document.getElementById('yr').textContent=new Date().getFullYear();
document.addEventListener('click',function(e){var a=e.target.closest('a[href^="#"]');if(a)document.getElementById('nav').classList.remove('open');});
(function(){
  /* Shared Free Case Review form handler — works on any page with #caseForm (home + contact). */
  var form=document.getElementById('caseForm'); if(!form) return;
  var formId = form.getAttribute('data-hs-form') || '460ba517-6b2d-47cc-9f1d-379c4bd53ee4';
  var ENDPOINT = "https://api.hsforms.com/submissions/v3/integration/submit/7690372/" + formId;
  /* TODO(client): set this to the real HubSpot SMS subscription-type ID once the client's
     HubSpot admin creates one under Settings > Communications > Subscription Types, then
     legalConsentOptions below will actually record the opt-in on the contact's subscriptions.
     Until then, a checked SMS box is still safely recorded as a note on the message field
     so no opt-in is ever silently lost. */
  var SMS_SUBSCRIPTION_ID = null;
  var note=document.getElementById('f_note'), btn=document.getElementById('f_btn');
  function es(){return (document.documentElement.lang||'').slice(0,2)==='es';}
  function getCookie(name){var m=document.cookie.match('(?:^|; )'+name+'=([^;]*)');return m?decodeURIComponent(m[1]):'';}
  function okMsg(){return es()
    ? '<div style="padding:14px 0;text-align:center"><h3 style="font-family:Roboto Slab,serif;color:#0a6b78;font-size:1.4rem">Gracias.</h3><p style="color:#697079;margin-top:8px">Recibimos su solicitud. Un abogado se comunicará con usted pronto. Para hablar con alguien ahora, llame al <b>888-492-0633</b>.</p></div>'
    : '<div style="padding:14px 0;text-align:center"><h3 style="font-family:Roboto Slab,serif;color:#0a6b78;font-size:1.4rem">Thank you.</h3><p style="color:#697079;margin-top:8px">Your request has been received. An attorney will reach out shortly. To speak with someone now, call <b>888-492-0633</b>.</p></div>';}
  form.addEventListener('submit',function(e){
    e.preventDefault();
    if(document.getElementById('f_co').value){return;}
    var label=btn.textContent; btn.disabled=true; btn.textContent=es()?'Enviando…':'Sending…';
    var msgEl=document.getElementById('f_msg'), smsEl=document.getElementById('f_sms');
    var msgVal = msgEl ? msgEl.value.trim() : '';
    var smsChecked = !!(smsEl && smsEl.checked);
    var fields=[
      {name:"firstname",value:document.getElementById('f_first').value.trim()},
      {name:"lastname", value:document.getElementById('f_last').value.trim()},
      {name:"email",    value:document.getElementById('f_email').value.trim()},
      {name:"phone",    value:document.getElementById('f_phone').value.trim()}
    ];
    if(smsEl){ msgVal = (msgVal?msgVal+'\\n\\n':'') + '[SMS opt-in: '+(smsChecked?'YES':'no')+']'; }
    if(msgVal){ fields.push({name:"message", value: msgVal}); }
    var payload={fields:fields, context:{pageUri:location.href,pageName:document.title}};
    var hutk=getCookie('hubspotutk'); if(hutk) payload.context.hutk=hutk;
    if(smsEl && SMS_SUBSCRIPTION_ID){
      payload.legalConsentOptions={consent:{consentToProcess:true,text:"Submitted via W Employment Law website form.",
        communications:[{value:smsChecked,subscriptionTypeId:SMS_SUBSCRIPTION_ID,text:smsEl.nextElementSibling.textContent}]}};
    }
    fetch(ENDPOINT,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)})
      .then(function(r){return r.ok?r.json():Promise.reject(r);})
      .then(function(){ form.innerHTML=okMsg(); if(window.welTrackLead) welTrackLead(); })
      .catch(function(){ btn.disabled=false; btn.textContent=label; note.innerHTML=es()?'Algo salió mal. Por favor llame al <b>888-492-0633</b> y lo atenderemos.':'Something went wrong. Please call <b>888-492-0633</b> and we\\'ll get you taken care of.'; });
  });
})();
(function(){var els=document.querySelectorAll('.reveal');
function showAll(){els.forEach(function(e){e.classList.add('in');});}
if(!('IntersectionObserver' in window)){showAll();return;}
var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.08,rootMargin:'0px 0px -4% 0px'});
els.forEach(function(e){io.observe(e);});
window.addEventListener('load',function(){setTimeout(showAll,1600);});
})();
</script>
"""

DEFAULT_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "LegalService",
    "name": "W Employment Law",
    "description": "California employment law firm representing employees in wrongful termination, discrimination, harassment, unpaid wages and overtime, and retaliation. No fee unless we win.",
    "url": BASE_URL,
    "telephone": "+1-888-492-0633",
    "image": BASE_URL + "img/jacob-share.jpg",
    "priceRange": "No fee unless we win",
    "areaServed": {"@type": "State", "name": "California"},
    "address": {"@type": "PostalAddress", "streetAddress": "7700 Irvine Center Drive, Suite 800",
                "addressLocality": "Irvine", "addressRegion": "CA", "postalCode": "92618", "addressCountry": "US"},
    "founder": {"@type": "Person", "name": "Jacob N. Whitehead", "jobTitle": "Founding Attorney"},
    "knowsLanguage": ["English", "Spanish"],
    "sameAs": [SOCIAL["facebook"], SOCIAL["instagram"], SOCIAL["youtube"], SOCIAL["tiktok"], SOCIAL["linkedin"]],
}


# ---------------------------------------------------------------------------
# page() — the main public API
# ---------------------------------------------------------------------------
def page(path, title, description, body_html, *,
         h1=None, eyebrow=None, es_h1=None, es_eyebrow=None,
         breadcrumbs=None, schema=None, es=None, og_image=None,
         extra_head="", extra_scripts=""):
    assert path.startswith("/") and path.endswith("/"), f"path must start/end with '/': {path!r}"

    body_html = substitute_tokens(body_html, path)
    phead = ""
    if h1:
        phead = render_phead(h1, eyebrow, breadcrumbs, es_h1, es_eyebrow, path)

    full_title = title if "W Employment Law" in title else f"{title} | W Employment Law"
    canonical = BASE_URL.rstrip("/") + path
    og_img = og_image or (BASE_URL.rstrip("/") + "/img/jacob-share.jpg")
    img_prefix = "../" * depth(path)
    styles_href = f"{img_prefix}styles.css?v=20261007"
    i18n_href = f"{img_prefix}i18n.js"

    schema_blocks = [json.dumps(DEFAULT_SCHEMA, ensure_ascii=False)]
    if schema:
        schema_blocks.append(json.dumps(schema, ensure_ascii=False))
    schema_html = "\n".join(f'<script type="application/ld+json">\n{s}\n</script>' for s in schema_blocks)

    html = f"""<!DOCTYPE html>
<html lang="en"><head><script>document.documentElement.classList.add('js')</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{full_title}</title>
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:site_name" content="W Employment Law">
<meta property="og:type" content="website">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{full_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_img}">
<meta name="description" content="{description}">
<link rel="icon" type="image/png" sizes="32x32" href="{img_prefix}img/favicon-32.png">
<link rel="icon" type="image/png" sizes="180x180" href="{img_prefix}img/favicon.png">
<link rel="apple-touch-icon" href="{img_prefix}img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Karla:wght@400;500;600;700;800&family=Roboto+Slab:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{styles_href}">
{schema_html}
{extra_head}
</head>
<body id="top">
{render_nav(path)}
{phead}
{body_html}
{render_social_band()}
{render_footer(path)}
{COMMON_SCRIPT}
{TRACKING_JS}
{extra_scripts}
<script src="{i18n_href}"></script>
</body></html>
"""
    out_file = OUT / path.lstrip("/") / "index.html" if path != "/" else OUT / "index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    PAGE_REGISTRY.append(path)
    return out_file


# ---------------------------------------------------------------------------
# content/*.json loader (for the next agent's ~35 pages)
# ---------------------------------------------------------------------------
def register_json_pages():
    if not CONTENT_DIR.exists():
        return
    skipped_raw = 0
    published = 0
    for f in sorted(CONTENT_DIR.glob("*.json")):
        if f.name == "_special.json":
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  ! {f.name}: unreadable ({exc}) — skipped")
            continue
        if not data.get("page_ready"):
            skipped_raw += 1  # raw crawl dump — reference material, not a page yet
            continue
        path = data.get("path", "")
        if not (path.startswith("/") and path.endswith("/")) or "body_html" not in data:
            print(f"  ! {f.name}: page_ready=true but path/body_html malformed — skipped")
            continue
        bc = data.get("breadcrumbs")
        if bc:
            bc = [tuple(x) for x in bc]
        page(
            path, data.get("title", path), data.get("description", ""),
            data["body_html"], h1=data.get("h1"), eyebrow=data.get("eyebrow"),
            es_h1=data.get("es_h1"), es_eyebrow=data.get("es_eyebrow"),
            breadcrumbs=bc, schema=data.get("schema"),
        )
        published += 1
        print(f"  + {path}  (from {f.name})")
    if skipped_raw:
        print(f"  ({skipped_raw} raw crawl file(s) in content/ awaiting page_ready authoring — not published)")
    if not published and not skipped_raw:
        print("  (content/ has no page-ready JSON yet)")


# ---------------------------------------------------------------------------
# Redirect stubs for the old flat files
# ---------------------------------------------------------------------------
REDIRECT_STUB_TMPL = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<title>W Employment Law</title>
<link rel="canonical" href="{target_abs}">
<meta http-equiv="refresh" content="0; url={target_rel}">
<meta name="robots" content="noindex,follow">
<script>location.replace({target_rel!r});</script>
</head><body>
<p>This page has moved to <a href="{target_rel}">{target_rel}</a>.</p>
</body></html>
"""


def write_redirect_stubs():
    for old_name, new_key in OLD_FLAT_REDIRECTS.items():
        target_abs_path = PATHS[new_key]
        target_abs = BASE_URL.rstrip("/") + target_abs_path
        target_rel = target_abs_path.lstrip("/")  # same depth (site root), so just the folder name
        html = REDIRECT_STUB_TMPL.format(target_abs=target_abs, target_rel=target_rel)
        (OUT / old_name).write_text(html, encoding="utf-8")
    # Folder-level stubs for old WP URLs with no real content of their own.
    for old_path, target_path in FOLDER_REDIRECTS.items():
        d = OUT / old_path.strip("/")
        d.mkdir(parents=True, exist_ok=True)
        target_abs = BASE_URL.rstrip("/") + target_path
        target_rel = "../" * depth(old_path) + target_path.lstrip("/")
        (d / "index.html").write_text(REDIRECT_STUB_TMPL.format(target_abs=target_abs, target_rel=target_rel), encoding="utf-8")


# Old WordPress URLs that were empty/orphaned: keep the URL alive by forwarding it.
FOLDER_REDIRECTS = {
    "/fired-while-on-medical-leave/": "/blog/fired-while-on-medical-leave-learn-about-your-rights/",
    "/video/": "/videos/",
}


# ---------------------------------------------------------------------------
# sitemap.xml / robots.txt / _redirects
# ---------------------------------------------------------------------------
def write_sitemap():
    urls = []
    for p in PAGE_REGISTRY:
        urls.append(f"  <url><loc>{BASE_URL.rstrip('/')}{p}</loc></url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    (OUT / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots():
    txt = f"User-agent: *\nAllow: /\nSitemap: {BASE_URL.rstrip('/')}/sitemap.xml\n"
    if not GO_LIVE:
        # preview copy should not be indexed by Google at all
        txt = "User-agent: *\nDisallow: /\n"
    (OUT / "robots.txt").write_text(txt, encoding="utf-8")


def write_cf_redirects():
    lines = [
        "# W Employment Law — redirects (Cloudflare Pages / Netlify _redirects format)",
        "# The new site mirrors the old WordPress URL slugs 1:1 (see WEL-HANDOFF.md URL map),",
        "# so none of those need a redirect here — only the OLD FLAT .html files we replaced.",
        "",
    ]
    for old_name, new_key in OLD_FLAT_REDIRECTS.items():
        lines.append(f"/{old_name}  {PATHS[new_key]}  301")
    lines += [
        "",
        "# Old WordPress junk paths — only add these once the crawl confirms they're linked/indexed.",
        "# /feed/            /blog/   301",
        "# /category/*       /blog/   301",
        "# /wp-content/uploads/*   -> not redirected; those were media files, not pages.",
    ]
    (OUT / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    print(f"Building W Employment Law site -> {OUT}  (GO_LIVE={GO_LIVE}, BASE_URL={BASE_URL})")

    page(
        PATHS["home"],
        "W Employment Law — Fighting for California Employees | Free Case Review",
        "Fired, harassed, discriminated against, or owed unpaid wages? W Employment Law fights for California employees. No Win, No Fee. Free, confidential case review — call 888-492-0633.",
        load_fragment("home"),
    )
    page(
        PATHS["contact"],
        "Free Case Review — Contact W Employment Law | California",
        "Tell us what happened. Free, confidential case review for California employees — no obligation, no fee unless we win. Call 888-492-0633 or request a review online.",
        load_fragment("contact"),
    )
    page(
        PATHS["practice-areas"],
        "Practice Areas — California Employment Law | W Employment Law",
        "Wrongful termination, discrimination, harassment, unpaid wages and overtime, pregnancy and medical leave, whistleblower retaliation, and contractor misclassification — we represent California employees. Free case review.",
        load_fragment("practice-areas"),
    )
    page(
        PATHS["blog"],
        "Insights — California Employment Law, Explained | W Employment Law",
        "Plain-English guides to your rights as a California employee: wrongful termination, unpaid overtime, harassment, pregnancy leave, and contractor misclassification. Free case reviews.",
        load_fragment("blog"),
    )
    page(
        PATHS["about"],
        "About — Meet Jacob N. Whitehead | W Employment Law",
        "W Employment Law was founded by Jacob N. Whitehead to give California employees a real fighting chance against employers who break the law. Barred in California & Washington D.C., fluent Spanish. No Win, No Fee.",
        load_fragment("jacob"),
    )
    page(
        PATHS["calculator"],
        "Unpaid Wages & Overtime Calculator | W Employment Law",
        "Free California overtime calculator. Estimate the unpaid overtime wages your employer may owe you — then get a free, confidential case review. No fee unless we win.",
        load_fragment("calculator"),
    )

    print("Registering content/*.json pages (next agent's ~35 pages, if any exist yet)...")
    register_json_pages()

    write_redirect_stubs()
    write_sitemap()
    write_robots()
    write_cf_redirects()

    print(f"Done. {len(PAGE_REGISTRY)} pages written.")


if __name__ == "__main__":
    build()
