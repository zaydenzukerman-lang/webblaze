#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
W Employment Law — extra pages that can't be expressed as content/ready__*.json
=================================================================================

Currently just one page: /thank-you/ (exact copy of the old wemploymentlaw.com/thank-you/
page). It lives here instead of in content/ because it must be **noindex**, and build.py's
page() always writes ``<meta name="robots" content="index,follow,...">`` with no option to
change it. So this script renders it with build.page() and then swaps that one meta tag.

RUN ORDER (after the main build, any time build.py has been run):

    python3 sitegen/custom/wemploymentlaw/build.py
    python3 sitegen/custom/wemploymentlaw/pages_extra.py

It only ever writes public/wemploymentlaw/thank-you/index.html. It deliberately does NOT
touch sitemap.xml: a noindex thank-you page should not be in the sitemap, and calling
build.write_sitemap() from this process would overwrite the full sitemap with only the
pages registered here. Re-running build.py never deletes thank-you/ (it only rewrites the
files it owns), so this only needs re-running when the shell (nav/footer) changes.
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build  # noqa: E402

YT_ID = "MKocG_1ITCo"  # the video embedded on the old /thank-you/ page

PLAY_SVG = ('<svg viewBox="0 0 68 48" aria-hidden="true"><path class="tm-yt-bg" d="M66.5 7.7a8.5 8.5 0 0 0-6-6C55.3.3 34 .3 34 .3s-21.3 0-26.5 1.4a8.5 8.5 0 0 0-6 6C.1 13 .1 24 .1 24s0 11 1.4 16.3a8.5 8.5 0 0 0 6 6C12.7 47.7 34 47.7 34 47.7s21.3 0 26.5-1.4a8.5 8.5 0 0 0 6-6C67.9 35 67.9 24 67.9 24s0-11-1.4-16.3z"/>'
            '<path fill="#fff" d="M45 24 27 14v20z"/></svg>')

# Social labels are the old page's exact text. URLs use the verified links from build.SOCIAL
# (the old page pointed Instagram/Facebook at the typo'd "swemploymentlaw" handles).
SOCIAL_LINKS = "".join(
    f'<a class="btn btn-outt" href="{build.SOCIAL[k]}" target="_blank" rel="noopener">{label}</a>'
    for k, label in (("instagram", "Instagram"), ("facebook", "Facebook"), ("youtube", "Youtube"), ("tiktok", "Tiktok"))
)

BODY = f"""<section class="sec tm-sec"><div class="wrap tm-narrow tm-center">
  <h1 class="tm-h2 tm-thanks-h">Thank You for Your Submission!</h1>
  <p class="tm-lead" style="margin:14px auto 0">Thanks for submitting your contact info. Our team will be in touch shortly. In the meantime, check your email for more info.</p>
  <div class="tm-feature" style="margin-top:34px">
    <button type="button" class="tm-yt" data-yt="{YT_ID}" aria-label="Play video"><img src="https://i.ytimg.com/vi/{YT_ID}/hqdefault.jpg" alt="" decoding="async" width="480" height="360"><span class="tm-yt-play">{PLAY_SVG}</span></button>
  </div>
  <div class="tm-social">{SOCIAL_LINKS}</div>
</div></section>
<script>
document.addEventListener('click',function(e){{
  var b=e.target.closest('.tm-yt'); if(!b) return;
  var f=document.createElement('iframe');
  f.src='https://www.youtube-nocookie.com/embed/'+b.getAttribute('data-yt')+'?autoplay=1&rel=0';
  f.title='YouTube video'; f.allowFullscreen=true; f.className='tm-yt-frame';
  f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
  b.replaceWith(f);
}});
</script>
"""


def build_extra():
    out = build.page(
        "/thank-you/", "Thank You!",
        "Thanks for submitting your contact info. Our team will be in touch shortly.",
        BODY,
    )
    html = out.read_text(encoding="utf-8")
    old = '<meta name="robots" content="index,follow,max-image-preview:large">'
    assert old in html, "build.page() robots meta changed — update pages_extra.py"
    out.write_text(html.replace(old, '<meta name="robots" content="noindex,follow">'), encoding="utf-8")
    print(f"  + /thank-you/  (noindex, not in sitemap) -> {out}")


if __name__ == "__main__":
    build_extra()
