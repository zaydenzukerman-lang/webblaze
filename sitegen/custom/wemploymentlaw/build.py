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
# Google reviews (homepage) are rendered at BUILD time from reviews.json, which
# fetch_reviews.py scrapes from the firm's Google Maps listing. See WEL-HANDOFF.md.
REVIEWS_JSON = pathlib.Path(__file__).resolve().parent / "reviews.json"
TEAM_JSON = pathlib.Path(__file__).resolve().parent / "team.json"
HS_GUIDE_FORM_ID = "2860c01f-db29-45c3-bc90-567d6cc5d835"  # old site's "free guide" lead-magnet form
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
    "faq": "/faq/",
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
    "LAW_GUIDES": "law-guides", "FAQ": "faq", "PRICING": "pricing", "REFERRALS": "referrals",
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
        {"label": "Pricing", "es": "Precios", "key": "pricing"},
        {"label": "Referrals", "es": "Referencias", "key": "referrals"},
    ]},
    {"label": "Resources", "es": "Recursos", "key": "blog", "children": [
        {"label": "Insights", "es": "Recursos", "key": "blog"},
        {"label": "Free Law Guides", "es": "Guías Legales Gratuitas", "key": "law-guides"},
        {"label": "Wage Calculator", "es": "Calculadora de Salarios", "key": "calculator"},
        {"label": "FAQ", "es": "Preguntas Frecuentes", "key": "faq"},
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
    if "{{AWARDS_MARQUEE}}" in out:
        out = out.replace("{{AWARDS_MARQUEE}}", render_awards_marquee()).replace("{{IMG}}", "../" * depth(from_path))
    for token, fn in (("{{GOOGLE_REVIEWS}}", render_google_reviews), ("{{TEAM_GRID}}", render_team_grid)) + ROUND4_TOKENS:
        if token in out:
            out = out.replace(token, fn()).replace("{{IMG}}", "../" * depth(from_path))
            out = substitute_paths_only(out, from_path)
    out = out.replace("{{HS_GUIDE_FORM}}", HS_GUIDE_FORM_ID).replace("{{HS_FORM}}", HS_FORM_ID)
    return out


def substitute_paths_only(html, from_path):
    """Re-run the {{TOKEN}} -> relative path swap (for HTML generated after the first pass)."""
    for token, key in TOKEN_MAP.items():
        html = html.replace("{{%s}}" % token, rel(from_path, PATHS[key]))
    return html


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

# ---------------------------------------------------------------------------
# "Recognized by" awards marquee (homepage). Client round 3: bigger badges in a continuous
# horizontal scroll like haelaw.com. Pure CSS: the set is rendered 4x inside a track that
# translates -50% forever (2 copies per half, so one half is always wider than a 1920px
# screen = seamless loop). Only the first copy is exposed to screen readers. Pauses on
# hover/focus; prefers-reduced-motion shows one static wrapped row instead.
# ---------------------------------------------------------------------------
AWARD_BADGES = [
    ("avvo-rating-10.webp", 150, 122, "Avvo Rating 10.0 — Jacob N Whitehead, Top Attorney"),
    ("super-lawyers-rising-stars.webp", 150, 141, "Super Lawyers Rising Stars — Jacob Whitehead"),
    ("americas-top-100.webp", 150, 150, "America's Top 100 High Stakes Litigators"),
    ("multi-million-dollar-advocates.webp", 148, 149, "Multi-Million Dollar Advocates Forum"),
    ("aaj-member.webp", 284, 134, "American Association for Justice — Member"),
    ("expertise-best-2021.webp", 400, 320, "Expertise.com — Best Employment Lawyers in Irvine 2021"),
    ("avvo-clients-choice.webp", 150, 123, "Avvo Clients' Choice Award 2021 — Jacob N Whitehead"),
    ("top40-under40.webp", 150, 150, "Premier Lawyers Top 40 Under 40 of America 2020"),
]

# Dark artwork on a transparent background: rendered white on the dark band so it stays legible.
AWARD_INVERT = set()  # round 4: badges shown in full colour on a light band, nothing inverted


def render_awards_marquee():
    def one_set(hidden):
        items = "".join(
            f'<li{" class=aw-inv" if f in AWARD_INVERT else ""}><img src="{{{{IMG}}}}img/{f}" width="{w}" height="{h}" alt="{"" if hidden else alt}" decoding="async"></li>'
            for f, w, h, alt in AWARD_BADGES
        )
        aria = ' aria-hidden="true"' if hidden else ""
        return f'<ul class="aw-set"{aria}>{items}</ul>'
    sets = one_set(False) + one_set(True) * 3
    return (f'<div class="aw-marquee" role="region" aria-label="Awards and recognition">'
            f'<div class="aw-track">{sets}</div></div>')


# ---------------------------------------------------------------------------
# Google reviews section (homepage token {{GOOGLE_REVIEWS}}). Layout modelled on
# frontierlawcenter.com/los-angeles-employment-lawyer/ "What Our Clients Are Saying":
# Google "G" on each card, quote, client's Google photo + name, swipeable row of cards with
# dots, then a "Google Reviews ★★★★★ 4.x (N reviews)" summary linking to the listing.
# Data: reviews.json (real reviews only, written by fetch_reviews.py; never hand-written).
# ---------------------------------------------------------------------------
REVIEWS_SHOWN = 5
G_ICON_SVG = ('<svg class="grev-g" viewBox="0 0 48 48" aria-hidden="true">'
    '<path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.6-.4-3.5z"/>'
    '<path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>'
    '<path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/>'
    '<path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.6-.4-3.5z"/></svg>')


def _esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def render_google_reviews():
    data = json.loads(REVIEWS_JSON.read_text(encoding="utf-8"))
    # Skip reviews that use an old firm name (client asked for "W Employment Law" everywhere;
    # we never edit a reviewer's words, so we just don't feature those reviews).
    old_names = re.compile(r"W Employment Law Group|\bSW ?Employment Law|Whitehead Employment Law", re.I)
    revs = [r for r in data.get("reviews", []) if r.get("rating") == 5 and (r.get("text") or "").strip()
            and not old_names.search(r.get("text") or "")]
    revs = revs[:REVIEWS_SHOWN]
    if not revs:
        raise SystemExit("reviews.json has no 5-star reviews with text; refusing to render an empty section")
    cards = []
    for i, r in enumerate(revs):
        name = _esc(r["name"])
        paras = "".join(f"<p>{_esc(x.strip())}</p>" for x in r["text"].split("\n") if x.strip())
        if r.get("photo"):
            av = f'<img class="grev-av" src="{{{{IMG}}}}{_esc(r["photo"])}" width="52" height="52" alt="" loading="lazy" decoding="async">'
        else:
            av = f'<span class="grev-av grev-av-i" aria-hidden="true">{_esc(r["name"][:1].upper())}</span>'
        cards.append(
            f'<li class="grev-card" id="grev-{i+1}"><article aria-label="Google review by {name}">'
            f'<div class="grev-top">{G_ICON_SVG}<span class="grev-stars" role="img" aria-label="Rated 5 out of 5">★★★★★</span></div>'
            f'<div class="grev-text">{paras}</div>'
            f'<button class="grev-more" type="button" aria-expanded="false" hidden data-es="Leer más">Read more</button>'
            f'<div class="grev-who">{av}<span><b>{name}</b><small data-es="Reseña de Google">Google review</small></span></div>'
            f'</article></li>')
    dots = "".join(f'<button type="button" class="grev-dot" aria-label="Show review {i+1}" data-i="{i}"></button>' for i in range(len(revs)))
    rating = data.get("rating")
    total = data.get("total_reviews")
    listing = _esc(data.get("listing_url") or "")
    rating_txt = f"{rating:.1f}" if isinstance(rating, (int, float)) else ""
    total_txt = f" ({total} reviews)" if total else ""
    total_es = f" ({total} reseñas)" if total else ""
    summary = (f'<a class="grev-summary" href="{listing}" target="_blank" rel="noopener">'
               f'<span class="grev-wordmark" aria-hidden="true"><i style="color:#4285F4">G</i><i style="color:#EA4335">o</i><i style="color:#FBBC05">o</i><i style="color:#4285F4">g</i><i style="color:#34A853">l</i><i style="color:#EA4335">e</i></span>'
               f'<span class="grev-sum-r"><span class="grev-stars" aria-hidden="true">★★★★★</span>'
               f'<span class="grev-sum-t" data-es="{rating_txt}{total_es} en Google">{rating_txt}{total_txt} on Google</span></span></a>')
    return f"""<section class="grev" id="google-reviews" aria-labelledby="grev-h"><div class="wrap">
  <div class="grev-head">
    <h2 class="sec-h" id="grev-h" data-es="Lo Que Dicen Nuestros Clientes">What Our Clients Are Saying</h2></div>
  <ul class="grev-track" tabindex="0" aria-label="Latest 5-star Google reviews (scroll sideways for more)">{''.join(cards)}</ul>
  <div class="grev-nav"><button type="button" class="grev-arrow" data-dir="-1" aria-label="Previous reviews">‹</button><div class="grev-dots">{dots}</div><button type="button" class="grev-arrow" data-dir="1" aria-label="Next reviews">›</button></div>
  {summary}
</div></section>
<script>
(function(){{
  var sec=document.getElementById('google-reviews'); if(!sec) return;
  var track=sec.querySelector('.grev-track'), cards=[].slice.call(track.children), dots=[].slice.call(sec.querySelectorAll('.grev-dot'));
  /* "Read more" only on cards whose text is actually clamped */
  cards.forEach(function(c){{var t=c.querySelector('.grev-text'),b=c.querySelector('.grev-more');
    if(t.scrollHeight>t.clientHeight+4){{b.hidden=false;}}
    b.addEventListener('click',function(){{var o=c.classList.toggle('open');b.setAttribute('aria-expanded',o);
      var es=(document.documentElement.lang||'').slice(0,2)==='es';b.textContent=o?(es?'Leer menos':'Read less'):(es?'Leer más':'Read more');}});}});
  function step(){{return cards.length>1?cards[1].offsetLeft-cards[0].offsetLeft:track.clientWidth;}}
  function cur(){{return Math.round(track.scrollLeft/step());}}
  function go(i){{i=Math.max(0,Math.min(cards.length-1,i));track.scrollTo({{left:i*step(),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}});}}
  sec.querySelectorAll('.grev-arrow').forEach(function(b){{b.addEventListener('click',function(){{go(cur()+(+b.getAttribute('data-dir')));}});}});
  dots.forEach(function(d,i){{d.addEventListener('click',function(){{go(i);}});}});
  function sync(){{var i=cur(),vis=Math.max(1,Math.round(track.clientWidth/step())),max=track.scrollWidth-track.clientWidth;
    if(track.scrollLeft>=max-4) i=cards.length-vis;
    dots.forEach(function(d,k){{d.classList.toggle('on',k>=i&&k<i+vis);d.hidden=false;}});
    sec.classList.toggle('grev-static',max<=4);}}
  track.addEventListener('scroll',function(){{window.requestAnimationFrame(sync);}},{{passive:true}});
  window.addEventListener('resize',sync); sync();
}})();
</script>
"""


# ---------------------------------------------------------------------------
# Team grid (our-team page token {{TEAM_GRID}}). Client round 3: full-bleed photo grid like
# haelaw.com "Meet Alreen and Team" + frontierlawcenter.com/about/: no gutters, photos black &
# white -> colour on hover/keyboard focus, name + title on the photo. Jacob opens his bio page;
# every other tile links to that person's vCard (.vcf, served by app.swemploymentlaw.com).
# Data: team.json (order, vCard TITLE, photo per person; see WEL-HANDOFF.md).
# ---------------------------------------------------------------------------
def render_team_grid():
    team = json.loads(TEAM_JSON.read_text(encoding="utf-8"))
    tiles = []
    for m in team:
        name = _esc(m["name"]); title = _esc(m.get("title") or "")
        if m.get("kind") == "bio":
            href = "{{ABOUT}}"; extra = ""
            label = f"{name}, {title}: view full bio" if title else f"{name}: view full bio"
            act = '<span class="tg-act" data-es="Ver biografía →">View bio →</span>'
        else:
            href = _esc(m["vcard"]); fname = _esc(m["vcard"].rsplit("/", 1)[-1])
            extra = f' download="{fname}" type="text/vcard"'
            label = f"Download vCard for {name}"
            act = '<span class="tg-act"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 19h16"/></svg> <span data-es="Descargar vCard">Download vCard</span></span>'
        if m.get("photo"):
            ph = m["photo"]; md = ph.replace(".webp", "-md.webp")
            srcset = (f' srcset="{{{{IMG}}}}{_esc(md)} 640w, {{{{IMG}}}}{_esc(ph)} 1280w" sizes="(min-width:900px) 20vw, (min-width:700px) 34vw, 50vw"'
                      if (OUT / md).exists() else "")
            media = f'<img src="{{{{IMG}}}}{_esc(md if srcset else ph)}"{srcset} width="640" height="800" alt="" loading="lazy" decoding="async">'
        else:
            media = f'<span class="tg-initials" aria-hidden="true">{_esc(m.get("initials") or name[:2].upper())}</span>'
        tiles.append(
            f'<li{" class=tg-lead" if m.get("kind") == "bio" else ""}><a class="tg-card{" tg-noimg" if not m.get("photo") else ""}" href="{href}"{extra} aria-label="{label}">'
            f'{media}<span class="tg-cap"><b>{name}</b>'
            f'{f"<span class=tg-title>{title}</span>" if title else ""}{act}</span></a></li>')
    return f'<ul class="tg-grid" role="list">{"".join(tiles)}</ul>'


# ---------------------------------------------------------------------------
# ROUND 4 shared components (client round-4 feedback, 2026-10-08). Each is a {{TOKEN}}
# so the homepage and the Jacob page render the exact same markup.
# ---------------------------------------------------------------------------
FA = json.loads((ROOT / "fa_icons.json").read_text(encoding="utf-8"))  # Font Awesome 5 solid (same icons as live site)
FAQ_JSON = ROOT / "faq.json"


def fa(name, cls=""):
    vb, d = FA[name]
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true" focusable="false"><path fill="currentColor" d="{d}"/></svg>'


def render_why_hire():
    """'Why Hire W Employment Law?' — mirrors the live site: real office photo under a 75% black
    overlay, 6 framed gold circles (Font Awesome icons the live site uses), live wording only,
    icon turns teal on hover (live hover), row fades in on scroll with a 300ms delay (live fadeIn)."""
    items = [("balance-scale", "Free Legal Advice", "Asesoría Legal Gratuita"),
             ("money-check-alt", "No Win No Fees", "Sin Ganar, Sin Honorarios"),
             ("university", "Power &amp; Resources", "Poder y Recursos"),
             ("user-tie", "Vast Experience", "Amplia Experiencia"),
             ("hands-helping", "Proven Results", "Resultados Comprobados"),
             ("eye-slash", "Confidential Advice", "Asesoría Confidencial")]
    boxes = "".join(
        f'<div class="wh-box" style="--d:{i*90}ms"><span class="wh-ic">{fa(ic)}</span><h3 data-es="{es}">{en}</h3></div>'
        for i, (ic, en, es) in enumerate(items))
    return (f'<section class="wh" id="why"><div class="wh-in">'
            f'<h2 data-es="¿Por Qué Contratar a W Employment Law?">Why Hire W Employment Law?</h2>'
            f'<div class="wh-grid wh-anim">{boxes}</div></div></section>')


TESTIMONIAL_VIDEOS = [("-D92OtPtzRc", "testimonial-zhubin.webp", "Zhubin", "meal &amp; rest break violations"),
                      ("Vi-P5Tldse8", "testimonial-caila.webp", "Caila", "wrongful termination"),
                      ("tHGyjLnjqx4", "testimonial-daniel.webp", "Daniel", "employment case")]


def render_testimonial_videos():
    """Video testimonials — mirrors live: #EDEDED band, 'Testimonials' + short gold divider,
    full-bleed row of videos (no side space, no border, no rounded corners)."""
    vids = "".join(
        f'<button class="yt-lite tvid" type="button" data-yt="{yt}" aria-label="Play video testimonial from {n}">'
        f'<img src="{{{{IMG}}}}img/{img}" width="960" height="480" alt="{n}, client video testimonial ({what})" loading="lazy">'
        f'<span class="yt-play" aria-hidden="true"></span></button>' for yt, img, n, what in TESTIMONIAL_VIDEOS)
    return (f'<section class="tv" id="reviews"><h2 data-es="Testimonios">Testimonials</h2>'
            f'<span class="tv-div" aria-hidden="true"></span><div class="tv-row">{vids}</div></section>')


def render_faq_accordion():
    """'California Employment Law FAQ' — accordion styled after frontierlawcenter.com
    (dark band, full-width bordered cards, +/− icon, open card highlighted with an accent bar,
    smooth height animation, one open at a time, first open by default). W Employment Law's
    own FAQ text from faq.json."""
    items = json.loads(FAQ_JSON.read_text(encoding="utf-8"))
    cards = []
    for i, it in enumerate(items):
        op = i == 0
        cards.append(
            f'<div class="fq-item{" open" if op else ""}"><h3 class="fq-t"><button type="button" class="fq-btn" id="fq-b{i}" '
            f'aria-expanded="{"true" if op else "false"}" aria-controls="fq-p{i}"><span data-es="{_esc(it["q_es"])}">{it["q"]}</span>'
            f'<span class="fq-ic" aria-hidden="true"></span></button></h3>'
            f'<div class="fq-p" id="fq-p{i}" role="region" aria-labelledby="fq-b{i}"><div class="fq-pi">'
            f'<p data-es="{_esc(it["a_es"])}">{it["a"]}</p></div></div></div>')
    return (f'<section class="fq" id="faq"><div class="fq-in">'
            f'<h2 data-es="Preguntas Frecuentes sobre el Derecho Laboral de California">California Employment Law FAQ</h2>'
            f'<div class="fq-list">{"".join(cards)}</div></div></section>')


HOW_STEPS = [
    ("Tell Us What Happened", "Call or send the form. It is free, confidential, and takes a few minutes.",
     "Cuéntenos Qué Pasó", "Llame o envíe el formulario. Es gratis, confidencial y toma solo unos minutos."),
    ("We Review Your Case", "An employment attorney reads what happened and walks you through your options.",
     "Revisamos Su Caso", "Un abogado laboral lee lo que pasó y le explica sus opciones."),
    ("We Take It From There", "If we take the case, we deal with your employer. You do not have to worry.",
     "Nosotros Nos Encargamos", "Si tomamos el caso, nosotros tratamos con su empleador. Usted no tiene que preocuparse."),
    ("No Win, No Fee", "You pay nothing unless we recover compensation for you.",
     "Sin Ganar, Sin Honorarios", "No paga nada a menos que recuperemos una compensación para usted."),
]


def render_how_it_works():
    """'How It Works' — layout/animation modelled on the steps section of
    frontierlawcenter.com/los-angeles-employment-lawyer/: dark rounded panel, zig-zag numbered
    steps, a dashed gradient curve drawn between consecutive steps as you scroll (scrubbed),
    number badge fills when the step reaches 70% of the viewport, each step fades up into view.
    Client-supplied copy (exact). prefers-reduced-motion: everything shown, no animation."""
    steps = "".join(
        f'<li class="hw-step hw-{"l" if i % 2 == 0 else "r"}"><span class="hw-badge">{i+1}</span>'
        f'<h3 data-es="{tes}">{t}</h3><p data-es="{xes}">{x}</p></li>'
        for i, (t, x, tes, xes) in enumerate(HOW_STEPS))
    return (f'<section class="hw" id="how-it-works"><div class="hw-panel">'
            f'<div class="hw-head"><h2 data-es="Cómo W Employment Law Lucha Por Usted">How W Employment Law Fights For You</h2>'
            f'<p data-es="Nosotros nos encargamos del caso para que usted pueda seguir adelante.">We handle the case so you can focus on moving forward.</p></div>'
            f'<div class="hw-wrap"><svg class="hw-lines" aria-hidden="true" focusable="false"></svg><ol class="hw-list">{steps}</ol></div>'
            f'</div></section>')


ROUND4_TOKENS = (("{{WHY_HIRE}}", render_why_hire), ("{{TESTIMONIAL_VIDEOS}}", render_testimonial_videos),
                 ("{{FAQ_ACCORDION}}", render_faq_accordion), ("{{HOW_IT_WORKS}}", render_how_it_works))


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
                f'<div class="nav-item has-drop"><a href="{href}" '
                f'aria-haspopup="true" aria-expanded="false"><span data-es="{item["es"]}">{item["label"]}</span> <svg class="car" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
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
  <h3 data-es="Síganos en Redes Sociales">Follow Us on Social Media</h3>
  <div class="ic">{icons}</div>
</div></div>
"""


def render_footer(from_path):
    """Footer mirrors the live wemploymentlaw.com layout (client requests 2026-10-06 + 2026-10-07):
    full-bleed black band (no side gutters: 3% padding like the live Elementor section), 4 equal
    columns = logo + socials | Contact | Quick Access | Free Case Review form, form fields styled
    like the live HubSpot embed (#F5F8FA fields, #ECD62B Poppins submit). Still posts via our
    shared HubSpot handler (form[data-hs-form])."""
    h = lambda key: rel(from_path, PATHS[key])
    img_prefix = "../" * depth(from_path)
    socials = "".join(
        f'<a href="{SOCIAL[k]}" target="_blank" rel="noopener" aria-label="{k.title()}">{SOCIAL_ICONS_SVG[k]}</a>'
        for k in ("instagram", "facebook", "youtube", "linkedin", "tiktok")
    )
    quick = [("home", "Home", "Inicio"), ("about", "About", "Nosotros"), ("practice-areas", "Practice Areas", "Áreas de Práctica"),
             ("law-guides", "Free Law Guides", "Guías Legales Gratuitas"), ("pricing", "Pricing", "Precios"),
             ("referrals", "Referrals", "Referencias"), ("faq", "FAQ", "Preguntas Frecuentes"), ("contact", "Contact", "Contacto")]
    quick_html = "".join(f'<a href="{h(k)}" data-es="{es}">{en}</a>' for k, en, es in quick)
    return f"""<!-- FOOTER (layout mirrors live wemploymentlaw.com: full-bleed black, 4 equal columns, HubSpot-style form) -->
<footer><div class="f-wrap">
  <div class="f-cols">
    <div class="f-brand">
      <img src="{img_prefix}img/logo-white.png" alt="W Employment Law" class="brand-logo-f">
      <div class="f-soc">{socials}</div>
    </div>
    <div><h4 data-es="Contacto">Contact</h4>
      <div class="row-i"><span class="g"><svg class="ico-f" viewBox="0 0 512 512" aria-hidden="true"><path d="M497.4 361.8l-112-48a24 24 0 0 0-28 6.9l-49.6 60.6A370.7 370.7 0 0 1 130.6 204.1l60.6-49.6a23.9 23.9 0 0 0 6.9-28l-48-112A24.2 24.2 0 0 0 122.6.6l-104 24A24 24 0 0 0 0 48c0 256.5 207.9 464 464 464a24 24 0 0 0 23.4-18.6l24-104a24.3 24.3 0 0 0-14-27.6z"/></svg></span><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div>
      <div class="row-i"><span class="g"><svg class="ico-f" viewBox="0 0 384 512" aria-hidden="true"><path d="M172.3 501.7C27 291 0 269.4 0 192 0 86 86 0 192 0s192 86 192 192c0 77.4-27 99-172.3 309.7a24 24 0 0 1-39.5 0zM192 272a80 80 0 1 0 0-160 80 80 0 0 0 0 160z"/></svg></span><span>{ADDRESS_HTML}</span></div>
      <div class="row-i"><span class="g"><svg class="ico-f" viewBox="0 0 512 512" aria-hidden="true"><path d="M502.3 190.8c3.9-3.1 9.7-.2 9.7 4.7V400c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V195.6c0-5 5.7-7.8 9.7-4.7 22.4 17.4 52.1 39.5 154.1 113.6 21.1 15.4 56.7 47.8 92.2 47.6 35.7.3 72-32.8 92.3-47.6 102-74.1 131.6-96.3 154-113.7zM256 320c23.2.4 56.6-29.2 73.4-41.4 132.7-96.3 142.8-104.7 173.4-128.7 5.8-4.5 9.2-11.5 9.2-18.9v-19c0-26.5-21.5-48-48-48H48C21.5 64 0 85.5 0 112v19c0 7.4 3.4 14.3 9.2 18.9 30.6 23.9 40.7 32.4 173.4 128.7 16.8 12.2 50.2 41.8 73.4 41.4z"/></svg></span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div class="row-i"><span class="g"><svg class="ico-f" viewBox="0 0 512 512" aria-hidden="true"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm57.1 350.1L224.9 294c-3.1-2.3-4.9-5.9-4.9-9.7V116c0-6.6 5.4-12 12-12h48c6.6 0 12 5.4 12 12v137.7l63.5 46.2c5.4 3.9 6.5 11.4 2.6 16.8l-28.2 38.8c-3.9 5.3-11.4 6.5-16.8 2.6z"/></svg></span><span data-es="Disponibles 24/7 · Hablamos Español">Available 24/7 · Hablamos Español</span></div>
    </div>
    <div class="f-quick"><h4 data-es="Acceso Rápido">Quick Access</h4>{quick_html}</div>
    <div><h4 data-es="Revisión Gratuita de su Caso">Free Case Review</h4>
      <form class="f-form" data-hs-form="{HS_FORM_ID}">
        <input class="field" data-f="first" required placeholder="First name*" data-es-ph="Nombre*" aria-label="First name" autocomplete="given-name">
        <input class="field" data-f="last" required placeholder="Last name*" data-es-ph="Apellido*" aria-label="Last name" autocomplete="family-name">
        <input class="field" data-f="email" type="email" required placeholder="Email*" data-es-ph="Correo electrónico*" aria-label="Email" autocomplete="email">
        <input class="field" data-f="phone" type="tel" required placeholder="Phone Number*" data-es-ph="Número de teléfono*" aria-label="Phone" autocomplete="tel">
        <textarea class="field" data-f="msg" rows="2" placeholder="Tell Us About Your Employment Issue" data-es-ph="Cuéntenos sobre su problema laboral" aria-label="Tell us about your employment issue"></textarea>
        <input data-f="co" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
        <button class="btn btn-gold" type="submit" data-f="btn" data-es="Enviar">Submit</button>
        <p class="f-note" data-f="note"></p>
      </form>
    </div>
  </div>
  <div class="disc"><span data-es="<b>Publicidad de Abogados.</b> La información de este sitio web tiene fines informativos generales únicamente y no pretende ser, ni debe tomarse como, asesoría legal para ningún caso o situación individual. Esta información no pretende crear, y su recepción o visualización no constituye, una relación abogado-cliente. Los resultados anteriores no garantizan un resultado similar. Los testimonios reflejan experiencias individuales de clientes y no garantizan resultados futuros."><b>Attorney Advertising.</b> The information on this website is for general informational purposes only and is not intended to be, and should not be taken as, legal advice for any individual case or situation. This information is not intended to create, and receipt or viewing does not constitute, an attorney-client relationship. Prior results do not guarantee a similar outcome. Testimonials reflect individual client experiences and are not a guarantee of future results.</span>
    <div class="f-legal">© <span id="yr"></span> <a class="f-home" href="{h('home')}">W Employment Law</a> | <a href="{h('privacy')}" data-es="Política de Privacidad">Privacy Policy</a> | <a href="{h('terms')}" data-es="Términos de Uso">Terms of Use</a></div>
  </div>
</div></footer>

<div class="mbar"><a class="btn btn-teal" href="tel:{PHONE_TEL}"><svg class="ico" viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2z"/></svg> <span data-es="Llamar Ahora">Call Now</span></a><a class="btn btn-gold" href="{h('contact')}"><span data-es="Revisión Gratis">Free Review</span></a></div>
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
  /* Shared HubSpot form handler. Works for EVERY form[data-hs-form] on a page (hero/contact
     #caseForm, the footer form, the homepage free-guide form). Fields are looked up inside
     each form by data-f="first|last|email|phone|msg|sms|co|btn|note", falling back to the
     older #f_first-style ids so existing practice-area pages keep working unchanged. */
  var PORTAL = "7690372";
  /* TODO(client): set to the real HubSpot SMS subscription-type ID once their admin creates one
     (Settings > Communications > Subscription Types). Until then a checked SMS box is recorded
     as a note on the message field so no opt-in is ever lost. */
  var SMS_SUBSCRIPTION_ID = null;
  function es(){return (document.documentElement.lang||'').slice(0,2)==='es';}
  function getCookie(name){var m=document.cookie.match('(?:^|; )'+name+'=([^;]*)');return m?decodeURIComponent(m[1]):'';}
  function F(form,key){return form.querySelector('[data-f="'+key+'"]')||form.querySelector('#f_'+key);}
  function okMsg(download){
    var dl = download ? '<a class="btn btn-gold" style="margin-top:14px" href="'+download+'" target="_blank" rel="noopener" download>'+(es()?'Descargar la guía (PDF)':'Download the guide (PDF)')+'</a>' : '';
    return es()
      ? '<div class="form-ok"><h3>Gracias.</h3><p>'+(download?'Su guía gratuita está lista.':'Recibimos su solicitud. Un abogado se comunicará con usted pronto. Para hablar con alguien ahora, llame al <b>888-492-0633</b>.')+'</p>'+dl+'</div>'
      : '<div class="form-ok"><h3>Thank you.</h3><p>'+(download?'Your free guide is ready.':'Your request has been received. An attorney will reach out shortly. To speak with someone now, call <b>888-492-0633</b>.')+'</p>'+dl+'</div>';}
  document.querySelectorAll('form[data-hs-form]').forEach(function(form){
    var ENDPOINT = "https://api.hsforms.com/submissions/v3/integration/submit/"+PORTAL+"/"+form.getAttribute('data-hs-form');
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var hp=F(form,'co'); if(hp && hp.value){return;}
      var btn=F(form,'btn'), note=F(form,'note');
      var label=btn.textContent; btn.disabled=true; btn.textContent=es()?'Enviando…':'Sending…';
      var msgEl=F(form,'msg'), smsEl=F(form,'sms');
      var msgVal = msgEl ? msgEl.value.trim() : '';
      var smsChecked = !!(smsEl && smsEl.checked);
      var fields=[
        {name:"firstname",value:F(form,'first').value.trim()},
        {name:"lastname", value:F(form,'last').value.trim()},
        {name:"email",    value:F(form,'email').value.trim()},
        {name:"phone",    value:F(form,'phone').value.trim()}
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
        .then(function(){ var dl=form.getAttribute('data-download'); form.innerHTML=okMsg(dl); if(window.welTrackLead) welTrackLead();
          /* live site's guide form redirects straight to the PDF after submit (HubSpot redirectUrl) */
          if(dl && form.hasAttribute('data-redirect')){ setTimeout(function(){ location.href=dl; },600); } })
        .catch(function(){ btn.disabled=false; btn.textContent=label; if(note) note.innerHTML=es()?'Algo salió mal. Por favor llame al <b>888-492-0633</b> y lo atenderemos.':'Something went wrong. Please call <b>888-492-0633</b> and we\\'ll get you taken care of.'; });
    });
  });
})();
(function(){
  /* Count-up for result numbers, same feel as the live site's Elementor counters.
     The real amount is in the HTML (SEO / no-JS); JS animates from 0 when it scrolls into view. */
  var els=document.querySelectorAll('[data-count]'); if(!els.length) return;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fmt(n,el){return (el.getAttribute('data-prefix')||'')+Math.round(n).toLocaleString('en-US');}
  function run(el){var to=+el.getAttribute('data-count'),t0=null,dur=1500;
    function step(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/dur),e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;el.textContent=fmt(to*e,el);if(k<1)requestAnimationFrame(step);}
    requestAnimationFrame(step);}
  if(reduce||!('IntersectionObserver' in window)) return;
  els.forEach(function(el){el.textContent=fmt(0,el);});
  var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){run(e.target);io.unobserve(e.target);}});},{threshold:.4});
  els.forEach(function(el){io.observe(el);});
})();
(function(){
  /* Click-to-play YouTube (thumbnail first, player loads only on click: keeps the page fast). */
  document.addEventListener('click',function(e){
    var b=e.target.closest('.yt-lite'); if(!b) return;
    var id=b.getAttribute('data-yt'), f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&playsinline=1';
    f.title=b.getAttribute('aria-label')||'Video'; f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'; f.allowFullscreen=true;
    b.replaceWith(f);
  });
})();
(function(){
  /* ROUND 4 — nav dropdowns: aria-expanded, Escape to close, tap-to-open on touch (CSS does the animation) */
  var items=[].slice.call(document.querySelectorAll('.nav-item.has-drop'));
  function setOpen(it,o){it.classList.toggle('open',o);var a=it.querySelector(':scope>a');if(a)a.setAttribute('aria-expanded',o?'true':'false');}
  items.forEach(function(it){
    var a=it.querySelector(':scope>a');
    it.addEventListener('mouseenter',function(){it.classList.remove('esc');setOpen(it,true);});
    it.addEventListener('mouseleave',function(){setOpen(it,false);});
    it.addEventListener('focusin',function(){if(!it.classList.contains('esc'))setOpen(it,true);});
    it.addEventListener('focusout',function(e){if(!it.contains(e.relatedTarget)){it.classList.remove('esc');setOpen(it,false);}});
    it.addEventListener('keydown',function(e){if(e.key==='Escape'){it.classList.add('esc');setOpen(it,false);a.focus();}else if(e.key==='ArrowDown'&&e.target===a){e.preventDefault();it.classList.remove('esc');setOpen(it,true);var f=it.querySelector('.nav-drop a');if(f)f.focus();}});
    a.addEventListener('click',function(e){ /* first tap on a touch screen opens the menu instead of navigating */
      if(matchMedia('(hover: none)').matches && matchMedia('(min-width: 961px)').matches && !it.classList.contains('open')){e.preventDefault();items.forEach(function(o){setOpen(o,o===it);});}
    });
  });
  document.addEventListener('click',function(e){items.forEach(function(it){if(!it.contains(e.target))setOpen(it,false);});});
})();
(function(){
  /* ROUND 4 — FAQ accordion (frontierlawcenter style): one open at a time, height animated in CSS */
  document.querySelectorAll('.fq-list').forEach(function(list){
    list.addEventListener('click',function(e){
      var b=e.target.closest('.fq-btn'); if(!b) return;
      var it=b.closest('.fq-item'), open=!it.classList.contains('open');
      list.querySelectorAll('.fq-item').forEach(function(o){o.classList.remove('open');o.querySelector('.fq-btn').setAttribute('aria-expanded','false');});
      if(open){it.classList.add('open');b.setAttribute('aria-expanded','true');}
    });
  });
})();
(function(){
  /* ROUND 4 — "Why Hire" icons fade in once (live: Elementor fadeIn, 300ms delay) */
  var g=document.querySelectorAll('.wh-anim'); if(!g.length) return;
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){g.forEach(function(x){x.classList.add('in');});return;}
  var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.2});
  g.forEach(function(x){io.observe(x);});
})();
(function(){
  /* ROUND 4 — How It Works (modelled on frontierlawcenter.com steps): dashed gold curve between
     consecutive badges drawn as you scroll (scrubbed), badge fills at 70% of the viewport,
     each step fades up into view. Reduced motion: all visible, lines fully drawn, no animation. */
  var sec=document.querySelector('.hw'); if(!sec) return;
  var wrap=sec.querySelector('.hw-wrap'), svg=sec.querySelector('.hw-lines'), steps=[].slice.call(sec.querySelectorAll('.hw-step'));
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches, NS='http://www.w3.org/2000/svg', segs=[];
  sec.classList.add(reduce?'hw-static':'hw-live');
  function el(n,a){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);return e;}
  function draw(){
    while(svg.firstChild) svg.removeChild(svg.firstChild); segs=[];
    var wr=wrap.getBoundingClientRect(); svg.setAttribute('width',wr.width); svg.setAttribute('height',wr.height); svg.setAttribute('viewBox','0 0 '+wr.width+' '+wr.height);
    if(getComputedStyle(svg).display==='none') return;
    var defs=el('defs',{}); svg.appendChild(defs);
    for(var i=0;i<steps.length-1;i++){
      var a=steps[i].querySelector('.hw-badge').getBoundingClientRect(), b=steps[i+1].querySelector('.hw-badge').getBoundingClientRect();
      var x1=a.left-wr.left+a.width/2, y1=a.top-wr.top+a.height/2, x2=b.left-wr.left+b.width/2, y2=b.top-wr.top+b.height/2, dx=x2-x1, dy=y2-y1, d;
      if(dx>0){ x1-=a.width*1.2; d='M'+x1+' '+(y1+4)+' C'+(x1+.27*(x2-x1))+' '+(y1-.2*dy)+' '+(x1+.78*(x2-x1))+' '+(y1+.15*dy)+' '+x2+' '+(y2-b.height/2); }
      else { d='M'+(x1+a.width*1.1)+' '+(y1+a.height/2)+' C'+(x1+.15*dx)+' '+(y1+.62*dy)+' '+(x1+.55*dx)+' '+(y1+1.12*dy)+' '+x2+' '+(y2-2); }
      var gid='hwg'+i, mid='hwm'+i;
      var g=el('linearGradient',{id:gid,gradientUnits:'userSpaceOnUse',x1:dx>0?x1:x1+a.width,y1:y1,x2:x2,y2:y2});
      g.appendChild(el('stop',{'stop-color':'#ECD62B','stop-opacity':'0'})); g.appendChild(el('stop',{offset:'1','stop-color':'#ECD62B'})); defs.appendChild(g);
      var m=el('mask',{id:mid,maskUnits:'userSpaceOnUse',x:0,y:0,width:wr.width,height:wr.height}); var mp=el('path',{d:d,stroke:'#fff','stroke-width':'8',fill:'none'}); m.appendChild(mp); defs.appendChild(m);
      var p=el('path',{d:d,stroke:'url(#'+gid+')','stroke-width':'3','stroke-dasharray':'6 6',fill:'none',mask:'url(#'+mid+')'}); svg.appendChild(p);
      var L=mp.getTotalLength(); mp.style.strokeDasharray=L; mp.style.strokeDashoffset=reduce?0:L; segs.push({m:mp,L:L,box:steps[i]});
    }
    tick();
  }
  function tick(){
    if(reduce) return; var vh=innerHeight;
    segs.forEach(function(s){ /* 0 when this badge is at 80% of the viewport, 1 when the next badge reaches 60% */
      var sT=s.box.querySelector('.hw-badge').getBoundingClientRect().top, nT=s.box.nextElementSibling.querySelector('.hw-badge').getBoundingClientRect().top;
      var k=Math.max(0,Math.min(1,(vh*.8-sT)/((nT-sT)+vh*.2))); s.m.style.strokeDashoffset=s.L*(1-k);});
    steps.forEach(function(st){var t=st.getBoundingClientRect().top; if(t<vh*.88) st.classList.add('in'); st.classList.toggle('on',t<vh*.7);});
  }
  if(reduce){steps.forEach(function(st){st.classList.add('in','on');});}
  var raf=0; addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(function(){raf=0;tick();});},{passive:true});
  var rt; addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(draw,120);});
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(draw); addEventListener('load',draw); draw();
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
    styles_href = f"{img_prefix}styles.css?v=20261010"
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
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700;800;900&family=Didact+Gothic&family=Karla:wght@400;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
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
