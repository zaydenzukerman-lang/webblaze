// Rainbow Air Conditioning preview - small, dependency-free interactions.
(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var svc = document.getElementById('f-service'), msg = document.getElementById('f-msg');
  function prefill(service, note) {
    if (svc && service) svc.value = service;
    if (msg && note && !msg.value) msg.value = note;
  }

  // Symptom picker -> suggested service -> prefilled quote form
  var chips = document.querySelectorAll('.chip');
  var full = document.querySelector('.pa-full'), empty = document.querySelector('.pa-empty');
  var chosen = null;
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
      c.setAttribute('aria-pressed', 'true');
      chosen = c;
      var t = document.getElementById('sym-' + c.dataset.sym);
      full.querySelector('.pa-svc').textContent = c.dataset.service;
      var note = full.querySelector('.pa-note');
      note.innerHTML = '';
      if (t) note.appendChild(t.content.cloneNode(true));
      empty.hidden = true; full.hidden = false;
    });
  });
  var go = document.getElementById('pa-go');
  if (go) go.addEventListener('click', function () {
    if (!chosen) return;
    if (msg) msg.value = 'My AC: ' + chosen.textContent.toLowerCase() + '.';
    prefill(chosen.dataset.service);
  });

  // Links that prefill a service (e.g. "Ask about installation")
  document.querySelectorAll('[data-prefill]').forEach(function (a) {
    a.addEventListener('click', function () { prefill(a.dataset.prefill); });
  });

  // ?service=coil from other pages
  var map = { coil: 'Evaporator Coil Cleaning', repair: 'AC Repair', maintenance: 'AC Maintenance', install: 'AC Installation' };
  var m = /[?&]service=([a-z]+)/.exec(location.search);
  if (m && map[m[1]]) prefill(map[m[1]]);

  // Preview-only form
  var form = document.getElementById('quote-form');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var ok = true;
    form.querySelectorAll('[required]').forEach(function (f) {
      var bad = !f.value.trim();
      f.classList.toggle('bad', bad);
      if (bad) ok = false;
    });
    if (!ok) return;
    var done = form.querySelector('.form-ok');
    done.hidden = false;
    form.querySelector('button[type=submit]').disabled = true;
  });

  // Parts finder on the service page
  var q = document.getElementById('part-q'), list = document.getElementById('part-list'), none = document.getElementById('part-none');
  if (q && list) q.addEventListener('input', function () {
    var v = q.value.trim().toLowerCase(), shown = 0;
    list.querySelectorAll('li').forEach(function (li) {
      var hit = !v || li.textContent.toLowerCase().indexOf(v) > -1;
      li.hidden = !hit; if (hit) shown++;
    });
    none.hidden = shown > 0;
  });
})();
