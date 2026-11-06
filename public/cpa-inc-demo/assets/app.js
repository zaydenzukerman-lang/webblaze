// CPA Inc. demo — shared behaviour: EN/ES translator + form demo
// English is the no-JS default; Spanish is a faithful mirror via data-es attributes.
function cpaDemo(e){
  e.preventDefault();
  var m=document.getElementById('msg'); if(m) m.style.display='block';
  var b=e.target.querySelector('.submit');
  if(b) b.textContent = document.documentElement.getAttribute('lang')==='es' ? 'Enviado (demo)' : 'Sent (demo)';
  return false;
}
(function(){
  var KEY='cpaLang';
  function apply(lang){
    var es = lang==='es';
    document.documentElement.setAttribute('lang', es?'es':'en');
    [].forEach.call(document.querySelectorAll('[data-es]'), function(el){
      if(!el.hasAttribute('data-en')) el.setAttribute('data-en', el.innerHTML);
      el.innerHTML = es ? el.getAttribute('data-es') : el.getAttribute('data-en');
    });
    [].forEach.call(document.querySelectorAll('[data-es-ph]'), function(el){
      if(!el.hasAttribute('data-en-ph')) el.setAttribute('data-en-ph', el.getAttribute('placeholder')||'');
      el.setAttribute('placeholder', es ? el.getAttribute('data-es-ph') : el.getAttribute('data-en-ph'));
    });
    var btn=document.getElementById('langTog');
    if(btn){ btn.lastChild.textContent = es?'EN':'ES'; btn.setAttribute('aria-label', es?'Switch to English':'Cambiar a Español'); }
    try{ localStorage.setItem(KEY, lang); }catch(e){}
  }
  var saved='en'; try{ saved=localStorage.getItem(KEY)||'en'; }catch(e){}
  if(saved==='es') apply('es');
  document.addEventListener('click', function(ev){
    var t=ev.target.closest && ev.target.closest('#langTog');
    if(!t) return;
    apply(document.documentElement.getAttribute('lang')==='es' ? 'en' : 'es');
  });
})();
