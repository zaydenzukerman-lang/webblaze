
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
$('.menu')?.addEventListener('click',e=>{const n=$('nav');n.classList.toggle('open');e.target.setAttribute('aria-expanded',n.classList.contains('open'))});
const sel=new Set();const msg=$('#msg');
function upd(){ if(!msg)return; const touched=msg.dataset.touched; if(touched&&!msg.dataset.auto)return;
 msg.value=sel.size?'I would like help with: '+[...sel].join('; ')+'.':'';msg.dataset.auto='1'}
msg?.addEventListener('input',()=>{delete msg.dataset.auto;msg.dataset.touched='1'});
$$('.chip').forEach(c=>c.addEventListener('click',()=>{const on=c.getAttribute('aria-pressed')!=='true';c.setAttribute('aria-pressed',on);on?sel.add(c.textContent):sel.delete(c.textContent);upd();
 if(on&&!c.closest('.picker').dataset.scrolled){}}));
$$('.tab').forEach(t=>t.addEventListener('click',()=>{$$('.tab').forEach(x=>x.setAttribute('aria-selected',x===t));$$('.chip').forEach(c=>c.hidden=c.dataset.g!==t.dataset.g)}));
$('form.contact')?.addEventListener('submit',e=>{e.preventDefault();$('.note').textContent='Thanks! This is a design preview, so nothing was sent.'});
