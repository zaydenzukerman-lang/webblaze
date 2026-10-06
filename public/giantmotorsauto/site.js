// Giant Motors preview: mobile menu, service picker -> form prefill, preview-only forms, gallery lightbox.
(function () {
  var burger = document.querySelector('.burger'), menu = document.getElementById('menu');
  if (burger && menu) burger.addEventListener('click', function () {
    var open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });

  var form = document.getElementById('estimate');
  var select = form && form.querySelector('select[name=service]');
  function pick(name) {
    if (!select) return;
    for (var i = 0; i < select.options.length; i++) {
      if (select.options[i].text === name) { select.selectedIndex = i; break; }
    }
    select.classList.remove('flash'); void select.offsetWidth; select.classList.add('flash');
    document.querySelectorAll('.svc').forEach(function (b) {
      var on = b.getAttribute('data-service') === name;
      b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }
  // Service picker cards (home page)
  document.querySelectorAll('.svc').forEach(function (b) {
    b.setAttribute('aria-pressed', 'false');
    b.addEventListener('click', function () {
      var name = b.getAttribute('data-service');
      var txt = document.createElement('textarea'); txt.innerHTML = name; name = txt.value;
      pick(name);
      form.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setTimeout(function () { var n = form.querySelector('input[name=name]'); if (n) n.focus({ preventScroll: true }); }, 500);
    });
  });
  // ?service= prefill (services page links to contact page)
  try {
    var s = new URLSearchParams(location.search).get('service');
    if (s) pick(s);
  } catch (e) {}

  // Preview-only forms: nothing is sent
  document.querySelectorAll('form[data-preview]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = f.querySelector('.ok'); if (ok) { ok.hidden = false; ok.focus && ok.setAttribute('tabindex', '-1'); ok.focus(); }
    });
  });

  // Lightbox for equipment gallery
  var links = document.querySelectorAll('[data-lb]');
  if (links.length) {
    var lb = document.createElement('div');
    lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Photo viewer');
    lb.innerHTML = '<button type="button" aria-label="Close">&times;</button><img alt=""><p></p>';
    document.body.appendChild(lb);
    var img = lb.querySelector('img'), cap = lb.querySelector('p'), btn = lb.querySelector('button'), last;
    function close() { lb.classList.remove('open'); if (last) last.focus(); }
    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault(); last = a;
        var t = a.querySelector('img');
        img.src = a.getAttribute('href'); img.width = +t.getAttribute('width'); img.height = +t.getAttribute('height');
        img.alt = a.getAttribute('data-lb'); cap.textContent = a.getAttribute('data-lb');
        lb.classList.add('open'); btn.focus();
      });
    });
    btn.addEventListener('click', close);
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && lb.classList.contains('open')) close(); });
  }
})();
