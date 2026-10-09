(function () {
  // Mobile menu
  var menu = document.getElementById('menu'), nav = document.getElementById('nav');
  if (menu && nav) menu.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Lightbox for gallery photos
  var lb = document.getElementById('lb'), lbImg = document.getElementById('lb-img');
  if (lb && lb.showModal) {
    document.querySelectorAll('[data-lb]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var im = a.querySelector('img');
        lbImg.src = a.getAttribute('href');
        lbImg.alt = im ? im.alt : '';
        lbImg.removeAttribute('width'); lbImg.removeAttribute('height');
        lb.showModal();
      });
    });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb-x')) lb.close(); });
  }

  // Glass job picker -> fills the estimate form
  var jobs = document.getElementById('jobs');
  var form = document.getElementById('quote');
  if (!jobs || !form) return;
  var summary = document.getElementById('summary');
  var msg = document.getElementById('msg');
  var state = { job: null, kind: null, picks: {} };
  var lastAuto = '';

  function text(el) { return el.textContent.replace(/\s+/g, ' ').trim(); }

  function render() {
    ['shower', 'tub', 'mirror', 'repair'].forEach(function (k) {
      var box = document.getElementById('opt-' + k);
      if (box) box.hidden = state.kind !== k;
    });
    if (!state.job) return;
    var parts = [state.job];
    var box = document.getElementById('opt-' + state.kind);
    if (box) box.querySelectorAll('[data-group]').forEach(function (g) {
      var v = state.picks[state.kind + ':' + g.getAttribute('data-group')];
      if (v) parts.push(v);
    });
    var line = parts.join(' · ');
    summary.textContent = 'Request: ' + line;
    summary.classList.add('on');
    var auto = 'Free estimate request: ' + line + '.';
    if (!msg.value || msg.value === lastAuto) { msg.value = auto; lastAuto = auto; }
  }

  function selectIn(group, btn) {
    group.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', c === btn ? 'true' : 'false'); });
  }

  jobs.addEventListener('click', function (e) {
    var b = e.target.closest('.chip'); if (!b) return;
    selectIn(jobs, b);
    state.job = text(b); state.kind = b.getAttribute('data-kind');
    render();
  });
  document.querySelectorAll('.opts [data-group]').forEach(function (g) {
    g.addEventListener('click', function (e) {
      var b = e.target.closest('.chip'); if (!b) return;
      selectIn(g, b);
      var kind = g.closest('.opts').id.replace('opt-', '');
      state.picks[kind + ':' + g.getAttribute('data-group')] = text(b);
      render();
    });
  });

  // Preselect from ?job= (e.g. /contact/?job=mirror)
  try {
    var q = new URLSearchParams(location.search).get('job');
    var pre = q && jobs.querySelector('[data-job="' + q.replace(/[^a-z]/g, '') + '"]');
    if (pre) pre.click();
  } catch (err) {}

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var note = document.getElementById('form-note');
    note.textContent = 'Thanks! This is a design preview, so nothing was sent.';
    note.hidden = false;
  });
})();
