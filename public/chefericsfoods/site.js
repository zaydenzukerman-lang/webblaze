(function () {
  'use strict';
  // Mobile menu
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { menu.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Preview-only forms
  document.querySelectorAll('form[data-preview]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = f.querySelector('.form-msg');
      if (msg) { msg.hidden = false; msg.focus && msg.setAttribute('tabindex', '-1'); msg.focus(); }
    });
  });

  // Contact topic from query string (?topic=recipe)
  var topic = document.getElementById('topic');
  if (topic) {
    var m = /[?&]topic=([a-z]+)/.exec(location.search);
    if (m && topic.querySelector('option[value="' + m[1] + '"]')) topic.value = m[1];
  }

  // Order builder
  var steps = document.querySelectorAll('.step');
  if (!steps.length) return;
  var cart = {};
  var KEY = 'cefb-order';
  try { cart = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { cart = {}; }
  var byId = {};
  steps.forEach(function (s) { byId[s.dataset.id] = s; });
  Object.keys(cart).forEach(function (k) { if (!byId[k]) delete cart[k]; });

  var list = document.getElementById('sumList');
  var total = document.getElementById('sumTotal');
  var mini = document.getElementById('minibar');
  var miniCount = document.getElementById('miniCount');
  var miniTotal = document.getElementById('miniTotal');
  var orderText = document.getElementById('orderText');
  var touched = false;
  if (orderText) orderText.addEventListener('input', function () { touched = true; });

  function money(n) { return '$' + n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }

  function render() {
    var sum = 0, count = 0, lines = [];
    list.innerHTML = '';
    Object.keys(byId).forEach(function (id) {
      var s = byId[id], q = cart[id] || 0;
      s.querySelector('output').textContent = q;
      s.classList.toggle('has', q > 0);
      if (!q) return;
      var price = parseFloat(s.dataset.price), line = price * q;
      sum += line; count += q;
      var li = document.createElement('li');
      var name = document.createElement('span');
      name.textContent = q + ' x ' + s.dataset.name;
      var amt = document.createElement('b');
      amt.textContent = money(line);
      li.appendChild(name); li.appendChild(amt); list.appendChild(li);
      lines.push(q + ' x ' + s.dataset.name + ' @ ' + money(price) + ' = ' + money(line));
    });
    if (!count) {
      var e = document.createElement('li'); e.className = 'sum-empty';
      e.textContent = 'No items yet. Tap + on a product to start.'; list.appendChild(e);
    }
    total.textContent = money(sum);
    if (mini) {
      mini.hidden = count === 0;
      miniCount.textContent = count + (count === 1 ? ' item' : ' items');
      miniTotal.textContent = money(sum);
    }
    if (orderText && !touched) {
      orderText.value = count ? lines.join('\n') + '\nSubtotal: ' + money(sum) + ' (before shipping)' : '';
    }
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {}
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('.step button');
    if (!b) return;
    var s = b.closest('.step'), id = s.dataset.id, q = cart[id] || 0;
    q = b.classList.contains('inc') ? Math.min(q + 1, 99) : Math.max(q - 1, 0);
    if (q) cart[id] = q; else delete cart[id];
    touched = false;
    render();
  });

  var clear = document.getElementById('sumClear');
  if (clear) clear.addEventListener('click', function () { cart = {}; touched = false; render(); });

  // Category filter chips
  var chips = document.querySelectorAll('.chip');
  var cats = document.querySelectorAll('.cat');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.dataset.filter;
      chips.forEach(function (x) { var on = x === c; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      cats.forEach(function (sec) { sec.hidden = f !== 'all' && sec.dataset.cat !== f; });
    });
  });
  // Deep links to a category / product should show it even if filtered
  function showHash() {
    var t = location.hash && document.querySelector(location.hash);
    if (t && t.closest && t.closest('.cat') && t.closest('.cat').hidden) {
      chips[0].click();
      t.scrollIntoView();
    }
  }
  window.addEventListener('hashchange', showHash);

  render();
})();
