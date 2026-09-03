/* EN/ES language toggle for W Employment Law.
   Elements carry data-es (translated innerHTML) and/or data-es-ph (translated placeholder).
   Choice persists in localStorage and is applied on load. */
(function () {
  var KEY = 'wel_lang';
  function getStored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function store(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function apply(lang) {
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-es]').forEach(function (el) {
      if (!el.hasAttribute('data-en')) el.setAttribute('data-en', el.innerHTML);
      el.innerHTML = (lang === 'es') ? el.getAttribute('data-es') : el.getAttribute('data-en');
    });
    document.querySelectorAll('[data-es-ph]').forEach(function (el) {
      if (!el.hasAttribute('data-en-ph')) el.setAttribute('data-en-ph', el.getAttribute('placeholder') || '');
      el.setAttribute('placeholder', (lang === 'es') ? el.getAttribute('data-es-ph') : el.getAttribute('data-en-ph'));
    });
    var t = document.getElementById('langtog');
    if (t) {
      var en = t.querySelector('.l-en'), es = t.querySelector('.l-es');
      if (en) en.classList.toggle('active', lang !== 'es');
      if (es) es.classList.toggle('active', lang === 'es');
      t.setAttribute('aria-label', lang === 'es' ? 'Cambiar a inglés' : 'Switch to Spanish');
    }
    store(lang);
  }

  window.toggleLang = function () {
    var cur = getStored() || document.documentElement.lang || 'en';
    apply(cur === 'es' ? 'en' : 'es');
  };

  var start = getStored() || 'en';
  if (document.readyState !== 'loading') apply(start);
  else document.addEventListener('DOMContentLoaded', function () { apply(start); });
})();
