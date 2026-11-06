// Mobile menu, "what do you need?" picker -> form prefill, preview-only form submit.
(function () {
  var btn = document.querySelector('.menu-btn'), menu = document.getElementById('site-menu');
  if (btn && menu) btn.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  var need = document.getElementById('f-need'), msg = document.getElementById('f-msg');
  function prefill(item) {
    if (need) need.value = item;
    if (msg) {
      var line = 'I would like help with: ' + item + '.';
      if (!msg.value || /^I would like help with: /.test(msg.value)) msg.value = line + '\n\n';
    }
    [need, msg].forEach(function (el) { if (!el) return; el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); });
  }

  var picker = document.getElementById('picker');
  if (picker) {
    var chips = picker.querySelectorAll('.chip'), done = picker.querySelector('.pk-done');
    chips.forEach(function (c) {
      c.setAttribute('aria-pressed', 'false');
      c.addEventListener('click', function () {
        chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
        prefill(c.getAttribute('data-item'));
        if (done) done.hidden = false;
      });
    });
  }

  // Prefill from ?need= (links from Home picker to the Contact page)
  try {
    var q = new URLSearchParams(location.search);
    if (q.get('need')) prefill(q.get('need'));
  } catch (e) {}

  // Preview-only form
  document.querySelectorAll('form.consult').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      f.querySelector('.form-note').textContent = 'Thanks! This is a design preview, so nothing was sent.';
    });
  });
})();
