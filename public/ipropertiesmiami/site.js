
(function(){
  var b=document.querySelector('.burger'),u=document.querySelector('.nav ul');
  if(b&&u)b.addEventListener('click',function(){var o=u.classList.toggle('open');b.setAttribute('aria-expanded',o);});
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12}):null;
  document.querySelectorAll('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in');});
  // contact form (preview: confirms on the page)
  var f=document.getElementById('cform');
  if(f){
    var q=new URLSearchParams(location.search),plan=q.get('plan'),svc=q.get('service');
    if(plan){var m=document.getElementById('cm');m.value='I built a Home Watch plan on your website:\n'+plan+'\n\nPlease contact me to set it up.';}
    if(svc){var s=document.getElementById('cs');Array.prototype.forEach.call(s.options,function(o){if(o.value===svc)o.selected=true;});}
    f.addEventListener('submit',function(e){e.preventDefault();document.getElementById('cthanks').style.display='block';f.querySelectorAll('input,select,textarea,button').forEach(function(x){x.disabled=true;});});
  }
  // Home Watch plan builder
  var pb=document.getElementById('pb');
  if(pb){
    var FREQ={vacant:['Weekly','visits while the home sits empty'],seasonal:['Bi-weekly','visits while you are away for the season'],travel:['Bi-weekly','visits, plus a check before you return'],rental:['Weekly','visits between guests or tenants']};
    var TYPE={condo:'Condo or apartment',home:'Single-family home',estate:'Waterfront estate',invest:'Investment property'};
    var CARE={water:'Leak, moisture and mold checks',ac:'A/C and humidity monitoring',security:'Doors, windows and security checks',storm:'Storm and emergency oversight',vendors:'Pool, landscaping and vendor coordination',repairs:'Handyman repairs as needed'};
    function val(n){var c=pb.querySelector('input[name='+n+']:checked');return c?c.value:null;}
    function upd(){
      var t=val('type'),a=val('away'),cs=[].map.call(pb.querySelectorAll('input[name=care]:checked'),function(x){return x.value;});
      var fr=FREQ[a||'seasonal'];
      document.getElementById('pf').textContent=fr[0];
      document.getElementById('pfs').textContent=fr[1];
      document.getElementById('pt').textContent=t?TYPE[t]:'Your property';
      var items=['Documented inspections, inside and out','Updates sent straight to you'].concat(cs.map(function(c){return CARE[c];}));
      document.getElementById('pl').innerHTML=items.map(function(x){return '<li>'+x+'</li>';}).join('');
      var summary=(t?TYPE[t]:'Property')+' | '+fr[0]+' '+fr[1]+(cs.length?' | Focus: '+cs.map(function(c){return CARE[c];}).join(', '):'');
      document.getElementById('pgo').href='../contact/?service=Home+Watch+Program&plan='+encodeURIComponent(summary)+'#form';
    }
    pb.addEventListener('change',upd);upd();
  }
})();
