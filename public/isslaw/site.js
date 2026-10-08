// Mobile menu, case picker -> form prefill, preview-only form submit.
(function () {
  var btn = document.querySelector('.menu-btn'), menu = document.getElementById('site-menu');
  if (btn && menu) btn.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  var area = document.getElementById('f-area'), msg = document.getElementById('f-msg');
  function prefill(a, item) {
    if (!area) return;
    if (a) area.value = a;
    if (msg && item) {
      var line = 'I would like to talk about: ' + item + '.';
      if (!msg.value || /^I would like to talk about: /.test(msg.value)) msg.value = line + '\n\n';
    }
    [area, msg].forEach(function (el) { if (!el) return; el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); });
  }

  // Picker
  var picker = document.getElementById('picker');
  if (picker) {
    var tabs = picker.querySelectorAll('.pk-tab'), panels = picker.querySelectorAll('.pk-panel'), done = picker.querySelector('.pk-done');
    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        tabs.forEach(function (x) { x.setAttribute('aria-pressed', x === t ? 'true' : 'false'); });
        panels.forEach(function (p) { p.hidden = p.getAttribute('data-key') !== t.getAttribute('data-key'); });
        picker.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
        done.hidden = true;
        prefill(t.getAttribute('data-area'), null);
      });
    });
    picker.querySelectorAll('.chip').forEach(function (c) {
      c.setAttribute('aria-pressed', 'false');
      c.addEventListener('click', function () {
        picker.querySelectorAll('.chip').forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
        prefill(c.getAttribute('data-area'), c.getAttribute('data-item'));
        done.hidden = false;
      });
    });
  }

  // Prefill from ?area=&item= (links on Practice Areas page)
  try {
    var q = new URLSearchParams(location.search);
    if (q.get('area') || q.get('item')) prefill(q.get('area'), q.get('item'));
  } catch (e) {}

  // Preview-only form
  document.querySelectorAll('form.consult').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      f.querySelector('.form-note').textContent = 'Thanks! This is a design preview, so nothing was sent.';
    });
  });
})();
