(function(){
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var bg=$('#burger'),mn=$('#mnav');if(bg){bg.addEventListener('click',function(){var o=mn.classList.toggle('open');bg.setAttribute('aria-expanded',o)})}
var qp=new URLSearchParams(location.search);
// ZIP quick forms -> consultation picker
$$('form.zipf').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var z=f.querySelector('input').value.trim();var tgt=f.getAttribute('data-go');var u=tgt+'?'+(z?'zip='+encodeURIComponent(z)+'&':'')+(f.getAttribute('data-for')?'for='+f.getAttribute('data-for')+'&':'')+(f.getAttribute('data-need')?'need='+f.getAttribute('data-need'):'')+'#picker';if(f.hasAttribute('data-local')){var p=$('#picker');if(p){var zz=$('[name=zip]',p);if(zz)zz.value=z;p.scrollIntoView({behavior:'smooth'});return}}location.href=u})});
// Consultation picker
var WHO={me:'Just me',family:'My family',business:'My business',review:'I have a plan and want it reviewed'};
var NEED={ppo:'Private PPO plans',aca:'ACA Marketplace plans',group:'Small-business group, ICHRA or QSEHRA',cobra:'COBRA alternatives',dv:'Dental and vision add-ons',supp:'Supplemental or disability coverage'};
var SUG={me:['ppo','aca'],family:['ppo','aca'],business:['group'],review:['cobra','aca']};
$$('.pk').forEach(function(pk){
 var step=1,touched=false,notesEdited=false;
 var st=$$('.pst i',pk),panes=$$('[data-step]',pk),notes=$('[name=notes]',pk),sum=$('.sum',pk);
 function who(){var r=$('input[name=who]:checked',pk);return r?r.value:''}
 function needs(){return $$('input[name=need]:checked',pk).map(function(c){return c.value})}
 function show(n){step=n;panes.forEach(function(p){p.hidden=(+p.getAttribute('data-step')!==n)});st.forEach(function(s,i){s.classList.toggle('on',i<n)});var h=$('[data-step="'+n+'"] legend',pk);if(n>1&&h)h.scrollIntoView({block:'center',behavior:'smooth'})}
 function build(){var w=who(),n=needs(),z=$('[name=zip]',pk).value.trim();var t=[];if(w)t.push('Who needs coverage: '+WHO[w]+'.');if(n.length)t.push('I would like to compare: '+n.map(function(k){return NEED[k]}).join('; ')+'.');if(z)t.push('ZIP code: '+z+'.');return t.join(' ')}
 function upd(){var s=build();if(sum)sum.innerHTML=s?('<b>Your request so far</b><br>'+s.replace(/\. /g,'.<br>')):'<b>Your request so far</b><br>Choose an option above to start.';if(!notesEdited&&notes)notes.value=s}
 $$('input[name=who]',pk).forEach(function(r){r.addEventListener('change',function(){if(!touched){$$('input[name=need]',pk).forEach(function(c){c.checked=SUG[r.value].indexOf(c.value)>-1})}upd();$('[data-next="1"]',pk).disabled=false})});
 $$('input[name=need]',pk).forEach(function(c){c.addEventListener('change',function(){touched=true;upd()})});
 if(notes)notes.addEventListener('input',function(){notesEdited=true});
 $$('[name=zip]',pk).forEach(function(z){z.addEventListener('input',upd)});
 $$('[data-next]',pk).forEach(function(b){b.addEventListener('click',function(){show(+b.getAttribute('data-next')+1)})});
 $$('[data-back]',pk).forEach(function(b){b.addEventListener('click',function(){show(+b.getAttribute('data-back')-1)})});
 pk.addEventListener('submit',function(e){e.preventDefault();var ok=$('.ok',pk);ok.classList.add('show');ok.focus&&ok.focus();ok.scrollIntoView({block:'center',behavior:'smooth'})});
 // presets from URL
 var f=qp.get('for'),nd=qp.get('need'),z=qp.get('zip');
 if(z)$('[name=zip]',pk).value=z;
 if(f&&WHO[f]){var r=$('input[name=who][value='+f+']',pk);if(r){r.checked=true;$$('input[name=need]',pk).forEach(function(c){c.checked=SUG[f].indexOf(c.value)>-1});$('[data-next="1"]',pk).disabled=false}}
 if(nd){touched=true;var a=nd.split(',');$$('input[name=need]',pk).forEach(function(c){c.checked=a.indexOf(c.value)>-1})}
 var pre=pk.getAttribute('data-pre');
 show((f||nd)?2:1);upd();
 // when jumping from a page preset, do not scroll on load
});
// simple preview forms
$$('form[data-preview]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var o=$('.ok',f);if(o)o.classList.add('show')})});
// Countdown
var cd=$('#cd');if(cd){var T=new Date(2026,10,1,0,0,0).getTime();function tick(){var d=T-Date.now();if(d<=0){cd.innerHTML='<p><b>Open Enrollment 2027 is open.</b></p>';return}var s=Math.floor(d/1000),D=Math.floor(s/86400),H=Math.floor(s%86400/3600),M=Math.floor(s%3600/60),S=s%60;function p(n){return n<10?'0'+n:n}cd.innerHTML='<div><b>'+p(D)+'</b><span>DAYS</span></div><div><b>'+p(H)+'</b><span>HOURS</span></div><div><b>'+p(M)+'</b><span>MIN</span></div><div><b>'+p(S)+'</b><span>SEC</span></div>'}tick();setInterval(tick,1000)}
// Savings estimator (same ranges as the live calculator)
var ce=$('#calc');if(ce){var ci=$('#c-cobra'),ca=$('#c-age'),ch=$('#c-hh');function r5(x){return Math.round(x)}function calc(){var c=Math.max(0,+ci.value||0),a=Math.min(64,Math.max(18,+ca.value||35)),h=Math.min(8,Math.max(1,+ch.value||1));var lo,hi;if(a<30){lo=180;hi=330}else if(a<40){lo=270;hi=420}else if(a<50){lo=360;hi=510}else if(a<60){lo=450;hi=600}else{lo=500;hi=1000}var m=1+0.75*(h-1);if(a<60){lo*=m;hi*=m}else{lo*=m;hi*=m}lo=r5(lo);hi=r5(hi);$('#r-ppo').textContent='$'+lo+' - $'+hi+'/mo';$('#r-sav').textContent='$'+Math.max(0,c-hi)+' - $'+Math.max(0,c-lo)+'/mo'}[ci,ca,ch].forEach(function(i){i.addEventListener('input',calc)});calc()}
// Blog filter
var bf=$$('[data-cat]');if(bf.length){var cards=$$('[data-c]');bf.forEach(function(b){b.addEventListener('click',function(){bf.forEach(function(x){x.setAttribute('aria-pressed',x===b)});var c=b.getAttribute('data-cat');cards.forEach(function(k){k.hidden=!(c==='all'||k.getAttribute('data-c')===c)})})})}
// State search
var ss=$('#ssearch');if(ss){ss.addEventListener('input',function(){var v=ss.value.toLowerCase();$$('[data-st]').forEach(function(c){c.hidden=c.getAttribute('data-st').indexOf(v)<0})})}
})();
