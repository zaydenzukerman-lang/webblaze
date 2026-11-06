/* Prestige Air Conditioning - WebBlaze preview */
(function () {
  // mobile menu
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var o = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', o ? 'true' : 'false');
  });

  // preview-only forms
  document.querySelectorAll('form[data-preview]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = f.querySelector('.form-ok');
      if (ok) { ok.classList.add('show'); ok.focus(); }
    });
  });

  // service picker -> prefills the comment box (contact page)
  var pick = document.querySelector('.pick');
  if (pick) {
    var target = document.getElementById(pick.getAttribute('data-target'));
    pick.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      var on = b.getAttribute('aria-pressed') !== 'true';
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var chosen = [].slice.call(pick.querySelectorAll('button[aria-pressed=true]')).map(function (x) { return x.textContent; });
      var rest = target.value.replace(/^I'm interested in:.*(\n|$)/, '');
      target.value = (chosen.length ? "I'm interested in: " + chosen.join(', ') + '\n' : '') + rest;
    });
  }

  // service-area checker (uses the city list from their own site)
  var cityIn = document.getElementById('city-q');
  if (cityIn) {
    var cities = JSON.parse(document.getElementById('city-data').textContent);
    var out = document.getElementById('city-out');
    var norm = function (s) { return s.toLowerCase().replace(/[^a-z]/g, ''); };
    var check = function () {
      var q = norm(cityIn.value);
      if (!q) { out.innerHTML = ''; return; }
      var hit = cities.filter(function (c) { return norm(c) === q; })[0] ||
                cities.filter(function (c) { return norm(c).indexOf(q) === 0 && q.length > 2; })[0];
      out.innerHTML = hit
        ? '<span class="ok">Yes - ' + hit + ' is on our service list.</span> Call <a href="tel:+15618338861">(561) 833-8861</a> to schedule.'
        : '<span class="no">' + cityIn.value.replace(/[<>&"]/g, '') + ' isn\'t on our published list.</span> Give us a call at <a href="tel:+15618338861">(561) 833-8861</a> and ask.';
    };
    cityIn.addEventListener('input', check);
    document.getElementById('city-form').addEventListener('submit', function (e) { e.preventDefault(); check(); });
  }

  // system size helper (uses the size chart from their quote form)
  var sq = document.getElementById('sqft');
  if (sq) {
    var rows = document.querySelectorAll('.size-list li');
    var msg = document.getElementById('sqft-out');
    var sel = document.getElementById('q-size');
    var run = function () {
      var v = parseInt(String(sq.value).replace(/[^0-9]/g, ''), 10), n = 0;
      rows.forEach(function (r) {
        var hit = v >= +r.dataset.min && v <= +r.dataset.max;
        r.classList.toggle('hit', !!hit); if (hit) n++;
      });
      if (!v) msg.textContent = '';
      else if (n === 0) msg.textContent = v < 900 ? 'That is smaller than our chart covers - call us and we will size it in person.' : 'That is larger than our chart covers - call us and we will size it in person.';
      else msg.textContent = n === 1 ? 'Highlighted: the size on our chart for ' + v.toLocaleString() + ' sq ft.' : 'Your home falls where two sizes overlap - both are highlighted. We confirm the right one on site.';
    };
    sq.addEventListener('input', run);
    document.querySelectorAll('.size-list button').forEach(function (b) {
      b.addEventListener('click', function () {
        sel.value = b.dataset.val;
        sel.scrollIntoView({ behavior: 'smooth', block: 'center' });
        sel.focus({ preventScroll: true });
      });
    });
  }
})();
