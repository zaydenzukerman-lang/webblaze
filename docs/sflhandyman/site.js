(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Estimate picker: toggle chips, keep a summary, prefill the request form
  var picker = document.querySelector('[data-picker]');
  if (picker) {
    var chips = Array.prototype.slice.call(picker.querySelectorAll('.chip[data-job]'));
    var sum = picker.querySelector('[data-sum]');
    var go = picker.querySelector('[data-go]');
    var areaSel = picker.querySelector('[data-area]');
    var typeChips = Array.prototype.slice.call(picker.querySelectorAll('.chip[data-type]'));
    var form = document.getElementById('quote-form');

    function selected() {
      return chips.filter(function (c) { return c.getAttribute('aria-pressed') === 'true'; })
        .map(function (c) { return c.getAttribute('data-job'); });
    }
    function propType() {
      var t = typeChips.filter(function (c) { return c.getAttribute('aria-pressed') === 'true'; })[0];
      return t ? t.getAttribute('data-type') : '';
    }
    function update() {
      var jobs = selected();
      if (sum) {
        sum.innerHTML = jobs.length
          ? '<b>' + jobs.length + '</b> job' + (jobs.length > 1 ? 's' : '') + ' selected'
          : 'Pick one or more jobs above';
      }
      if (go && go.tagName === 'A') {
        var q = jobs.length ? '?jobs=' + encodeURIComponent(jobs.join('|')) : '';
        go.setAttribute('href', go.getAttribute('data-base') + q + '#request');
      }
      if (form) {
        var area = areaSel ? areaSel.value : '';
        var type = propType();
        var subj = form.querySelector('[name=subject]');
        var msg = form.querySelector('[name=message]');
        if (jobs.length) {
          subj.value = 'Estimate request: ' + jobs.slice(0, 3).join(', ') + (jobs.length > 3 ? ' + ' + (jobs.length - 3) + ' more' : '');
        }
        var lines = [];
        if (jobs.length) lines.push('Jobs: ' + jobs.join(', '));
        if (type) lines.push('Property: ' + type);
        if (area) lines.push('Area: ' + area);
        var user = msg.getAttribute('data-user') || '';
        msg.value = lines.join('\n') + (lines.length ? '\n\n' : '') + user;
      }
    }
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
        update();
      });
    });
    typeChips.forEach(function (c) {
      c.addEventListener('click', function () {
        var was = c.getAttribute('aria-pressed') === 'true';
        typeChips.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        c.setAttribute('aria-pressed', was ? 'false' : 'true');
        update();
      });
    });
    if (areaSel) areaSel.addEventListener('change', update);
    if (form) {
      var msgEl = form.querySelector('[name=message]');
      msgEl.addEventListener('input', function () {
        var v = msgEl.value;
        var i = v.indexOf('\n\n');
        var hasHeader = /^(Jobs|Property|Area): /.test(v);
        msgEl.setAttribute('data-user', hasHeader ? (i > -1 ? v.slice(i + 2) : '') : v);
      });
    }
    // Prefill from ?jobs= (sent from the home page or services list)
    try {
      var params = new URLSearchParams(location.search);
      var pre = (params.get('jobs') || '').split('|').filter(Boolean);
      if (pre.length) {
        chips.forEach(function (c) {
          if (pre.indexOf(c.getAttribute('data-job')) > -1) c.setAttribute('aria-pressed', 'true');
        });
      }
    } catch (e) {}
    update();
  }

  // Preview-only forms
  Array.prototype.forEach.call(document.querySelectorAll('form[data-preview]'), function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var m = f.querySelector('.form-msg');
      if (m) {
        m.textContent = 'Thanks! This is a design preview, so nothing was sent.';
        m.classList.add('show');
        m.setAttribute('tabindex', '-1');
        m.focus();
      }
    });
  });

  // Lightbox for project photos
  var lb = document.getElementById('lb');
  if (lb && typeof lb.showModal === 'function') {
    var lbImg = null;
    var lbCap = lb.querySelector('p');
    Array.prototype.forEach.call(document.querySelectorAll('[data-full]'), function (b) {
      b.addEventListener('click', function () {
        if (!lbImg) {
          lbImg = document.createElement('img');
          lbImg.width = 1000; lbImg.height = 1000;
          lb.insertBefore(lbImg, lbCap);
        }
        lbImg.src = b.getAttribute('data-full');
        lbImg.alt = b.getAttribute('data-cap');
        lbCap.textContent = b.getAttribute('data-cap');
        lb.showModal();
      });
    });
    lb.querySelector('.x').addEventListener('click', function () { lb.close(); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
  }
})();
