(function(){
var d=document;
var b=d.querySelector('.burger'),m=d.getElementById('mnav');
if(b&&m){b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Close menu':'Open menu');});}
// keyboard/touch dropdown
d.querySelectorAll('.hasdd').forEach(function(h){var a=h.querySelector('.ddlink');a.addEventListener('keydown',function(e){if(e.key==='Escape')h.classList.remove('open');});});
// forms (preview only)
d.querySelectorAll('form.qf').forEach(function(f){
 f.addEventListener('submit',function(e){e.preventDefault();var ok=true;
  f.querySelectorAll('[required]').forEach(function(i){var v=i.value.trim();var bad=!v||(i.type==='email'&&!/^\S+@\S+\.\S+$/.test(v));i.classList.toggle('bad',bad);if(bad)ok=false;});
  if(!ok){var first=f.querySelector('.bad');if(first)first.focus();return;}
  f.querySelector('.thanks').hidden=false;f.querySelector('button[type=submit]').disabled=true;});
 f.addEventListener('input',function(e){e.target.classList.remove('bad');});
});
// coverage picker
var P=d.getElementById('picker');
if(P){
 var chips=[].slice.call(P.querySelectorAll('.chip')),sel=[],list=P.querySelector('.plist'),empty=P.querySelector('.pempty'),form=P.querySelector('form.qf'),ta=form.querySelector('textarea'),last='',card=P.querySelector('.pcard');
 function msg(){if(!sel.length)return '';var n=sel.map(function(c){return c.dataset.name});var s=n.length>1?n.slice(0,-1).join(', ')+' and '+n[n.length-1]:n[0];return 'I would like a quote for '+s+' insurance.';}
 function render(){
  chips.forEach(function(c){c.setAttribute('aria-pressed',sel.indexOf(c)>-1)});
  list.innerHTML='';sel.forEach(function(c){var li=d.createElement('li');var a=d.createElement('a');a.href=c.dataset.url;a.textContent='What is included in '+c.dataset.name+' coverage';var x=d.createElement('button');x.type='button';x.setAttribute('aria-label','Remove '+c.dataset.name);x.textContent=c.dataset.name+' ×';x.addEventListener('click',function(){toggle(c)});li.appendChild(x);li.appendChild(a);list.appendChild(li);});
  list.hidden=!sel.length;empty.hidden=!!sel.length;
  var cur=ta.value.trim();if(!cur||cur===last){last=msg();ta.value=last;}
  card.classList.toggle('has',sel.length>0);
 }
 function toggle(c){var i=sel.indexOf(c);if(i>-1)sel.splice(i,1);else sel.push(c);render();}
 chips.forEach(function(c){c.addEventListener('click',function(){toggle(c)});});
 function pick(id,scroll){var c=chips.filter(function(x){return x.dataset.id===id})[0];if(c&&sel.indexOf(c)<0){sel.push(c);render();}if(scroll)P.scrollIntoView({behavior:'smooth',block:'start'});}
 d.querySelectorAll('[data-pick]').forEach(function(q){q.addEventListener('click',function(){pick(q.dataset.pick,true)});});
 var m=/[?&]need=([\w,]+)/.exec(location.search);if(m)m[1].split(',').forEach(function(id){pick(id,false)});
}
})();
