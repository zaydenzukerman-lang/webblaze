// WebBlaze preview: mobile menu, practice-area picker, preview-only form, click-to-load videos.
(function () {
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Practice-area picker -> prefills the consultation form.
  var LINKS = {
    'living-trusts': ['affordable-living-trusts/', 'Revocable living trusts: $595 single person, $695 married couple.'],
    'wills': ['wills-trusts-estates/', 'Wills, revocable trusts, health care surrogate, living will and durable family power of attorney.'],
    'medicaid': ['medicaid-planning/', 'Medicaid Asset Protection Trusts, Personal Service Contracts and Qualified Income Trusts.'],
    'probate': ['probate-florida/', 'We offer flat fees for our services. There are no extra charges for phone calls.']
  };
  var root = (document.querySelector('link[rel="stylesheet"][href*="styles.css"]') || {}).getAttribute
    ? document.querySelector('link[rel="stylesheet"][href*="styles.css"]').getAttribute('href').replace(/styles\.css.*$/, '') : '';
  var select = document.getElementById('matter');
  var note = document.getElementById('pick-note');
  var picks = document.querySelectorAll('.pick');
  function choose(key, scroll) {
    picks.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-matter') === key ? 'true' : 'false'); });
    if (select) {
      select.value = key;
      select.classList.remove('hl'); void select.offsetWidth; select.classList.add('hl');
    }
    var desc = document.getElementById('desc');
    if (desc && select && select.selectedIndex > 0) {
      desc.placeholder = 'Tell us a little about your ' + select.options[select.selectedIndex].text + ' question.';
    }
    if (note && LINKS[key]) {
      note.hidden = false;
      note.innerHTML = LINKS[key][1] + ' <a href="' + root + LINKS[key][0] + '">Learn more</a>';
    }
    if (scroll && window.matchMedia('(max-width: 960px)').matches) {
      var f = document.getElementById('cform');
      if (f) f.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
  picks.forEach(function (b) {
    b.addEventListener('click', function () { choose(b.getAttribute('data-matter'), true); });
  });
  if (select) {
    select.addEventListener('change', function () { if (select.value) choose(select.value, false); });
    var m = /[?&]matter=([a-z-]+)/.exec(location.search);
    if (m && LINKS[m[1]]) choose(m[1], false);
  }

  // Preview-only form.
  var form = document.getElementById('cform');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = null;
      form.querySelectorAll('[required]').forEach(function (el) {
        var ok = el.value.trim() !== '' && (el.type !== 'email' || /.+@.+\..+/.test(el.value));
        el.classList.toggle('bad', !ok);
        if (!ok && !bad) bad = el;
      });
      if (bad) { bad.focus(); return; }
      var okMsg = document.getElementById('form-ok');
      okMsg.hidden = false;
      form.reset();
      picks.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      if (note) note.hidden = true;
    });
  }

  // Click-to-load YouTube (keeps pages fast).
  document.querySelectorAll('.vid-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + btn.getAttribute('data-yt') + '?autoplay=1&rel=0';
      f.title = btn.getAttribute('aria-label');
      f.allow = 'autoplay; encrypted-media; picture-in-picture';
      f.allowFullscreen = true;
      btn.replaceWith(f);
    });
  });
})();
