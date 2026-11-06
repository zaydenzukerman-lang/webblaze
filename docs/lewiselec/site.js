(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Preview-only forms
  document.querySelectorAll('[data-preview-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var done = f.querySelector('.form-done');
      if (done) { done.hidden = false; }
    });
  });

  // Prefill form from ?service=
  function prefill(key, title) {
    var sel = document.getElementById('cf-service'), msg = document.getElementById('cf-msg');
    if (sel && key) sel.value = key;
    if (msg && title && !msg.value) msg.value = 'I would like information about: ' + title + '.';
  }
  try {
    var q = new URLSearchParams(location.search).get('service');
    if (q) {
      var sel = document.getElementById('cf-service');
      var opt = sel && sel.querySelector('option[value="' + q.replace(/[^a-z]/g, '') + '"]');
      if (opt) prefill(opt.value, opt.textContent);
    }
  } catch (e) {}

  // Service picker (home)
  var dataEl = document.getElementById('pick-data');
  if (dataEl) {
    var data = JSON.parse(dataEl.textContent), current = null;
    var t = document.getElementById('pick-title'), d = document.getElementById('pick-desc'), go = document.getElementById('pick-go');
    document.querySelectorAll('.chip').forEach(function (c) {
      c.addEventListener('click', function () {
        document.querySelectorAll('.chip').forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        c.setAttribute('aria-pressed', 'true');
        current = c.getAttribute('data-svc');
        var item = data[current] || { t: c.textContent, d: '' };
        t.textContent = item.t; d.textContent = item.d;
        go.textContent = 'Request info: ' + item.t;
      });
    });
    go.addEventListener('click', function () {
      if (!current) return;
      var sel = document.getElementById('cf-service'), msg = document.getElementById('cf-msg');
      if (sel) sel.value = current;
      if (msg) msg.value = 'I would like information about: ' + (data[current] ? data[current].t : current) + '.';
    });
  }

  // Ohm's law calculator
  var ohm = document.getElementById('ohm');
  if (ohm) {
    var out = document.getElementById('ohm-out');
    var names = ['v', 'i', 'r', 'p'];
    function fmt(x) {
      if (!isFinite(x)) return '';
      var a = Math.abs(x);
      if (a !== 0 && (a < 0.001 || a >= 1e7)) return x.toExponential(3);
      return String(parseFloat(x.toPrecision(5)));
    }
    ohm.addEventListener('reset', function () {
      ohm.querySelectorAll('.unit-in').forEach(function (u) { u.classList.remove('calc'); });
      out.textContent = 'Enter two values to begin.';
    });
    ohm.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = {}, given = [];
      names.forEach(function (n) {
        var el = ohm.elements[n], raw = el.value.trim();
        el.parentNode.classList.remove('calc');
        if (raw !== '' && !el.dataset.calc) { var x = parseFloat(raw); if (isFinite(x) && x > 0) { v[n] = x; given.push(n); } }
        delete el.dataset.calc;
      });
      if (given.length !== 2) {
        out.textContent = 'Please enter exactly two positive values (clear the others).';
        return;
      }
      var E = v.v, I = v.i, R = v.r, P = v.p, k = given.sort().join('');
      if (k === 'iv') { R = E / I; P = E * I; }
      else if (k === 'rv') { I = E / R; P = E * E / R; }
      else if (k === 'pv') { I = P / E; R = E * E / P; }
      else if (k === 'ir') { E = I * R; P = I * I * R; }
      else if (k === 'ip') { E = P / I; R = P / (I * I); }
      else if (k === 'pr') { E = Math.sqrt(P * R); I = Math.sqrt(P / R); }
      var res = { v: E, i: I, r: R, p: P };
      names.forEach(function (n) {
        if (given.indexOf(n) < 0) {
          var el = ohm.elements[n]; el.value = fmt(res[n]); el.dataset.calc = '1';
          el.parentNode.classList.add('calc');
        }
      });
      out.textContent = fmt(E) + ' V  |  ' + fmt(I) + ' A  |  ' + fmt(R) + ' ohms  |  ' + fmt(P) + ' W';
    });
    names.forEach(function (n) {
      ohm.elements[n].addEventListener('input', function () { delete this.dataset.calc; this.parentNode.classList.remove('calc'); });
    });
  }

  // Surplus search
  var s = document.getElementById('sp-search');
  if (s) {
    var rows = Array.prototype.slice.call(document.querySelectorAll('#sp-table tbody tr'));
    var cnt = document.getElementById('sp-count');
    s.addEventListener('input', function () {
      var q = s.value.toLowerCase().trim(), n = 0;
      rows.forEach(function (r) { var hit = !q || r.textContent.toLowerCase().indexOf(q) >= 0; r.hidden = !hit; if (hit) n++; });
      cnt.textContent = n + ' of ' + rows.length + ' items';
    });
  }
})();
