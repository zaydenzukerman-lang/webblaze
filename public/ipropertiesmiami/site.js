
(function(){
  var b=document.querySelector('.burger'),u=document.querySelector('.nav ul');
  if(b&&u)b.addEventListener('click',function(){var o=u.classList.toggle('open');b.setAttribute('aria-expanded',o);});
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12}):null;
  document.querySelectorAll('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in');});
  // contact form (preview: confirms on the page)
  var f=document.getElementById('cform');
  if(f){
    var q=new URLSearchParams(location.search),plan=q.get('plan'),svc=q.get('service');
    if(plan){var m=document.getElementById('cm');m.value=(document.documentElement.lang==='es'?'Mi solicitud desde su sitio web:\n'+plan+'\n\nPor favor contácteme.':'My request from your website:\n'+plan+'\n\nPlease get in touch.');}
    if(svc){var s=document.getElementById('cs');Array.prototype.forEach.call(s.options,function(o){if(o.value===svc)o.selected=true;});}
    f.addEventListener('submit',function(e){e.preventDefault();document.getElementById('cthanks').style.display='block';f.querySelectorAll('input,select,textarea,button').forEach(function(x){x.disabled=true;});});
  }
  // Home Watch plan builder
  var pb=document.getElementById('pb');
  if(pb){
    var ES=document.documentElement.lang==='es';
    var TYPE=ES?{condo:'Condominio o apartamento',home:'Casa unifamiliar',estate:'Residencia frente al agua',invest:'Propiedad de inversión'}:{condo:'Condo or apartment',home:'Single-family home',estate:'Waterfront estate',invest:'Investment property'};
    var USE=ES?{seasonal:'Fuera por temporada',travel:'El propietario viaja con frecuencia',vacant:'La casa está desocupada',primary:'Residencia principal'}:{seasonal:"Away for the season",travel:'Owner travels often',vacant:'Home sits vacant',primary:'Primary home'};
    var CARE=ES?{watch:'Home Watch',maint:'Mantenimiento preventivo',handy:'Servicios de handyman',vendors:'Coordinación de proveedores',emergency:'Supervisión de emergencias'}:{watch:'Home Watch',maint:'Preventative Maintenance',handy:'Handyman Services',vendors:'Vendor coordination',emergency:'Emergency oversight'};
    var TX=ES?{prop:'Su propiedad',pick:'Elija con qué le gustaría recibir ayuda',propw:'Propiedad',int:'Le interesa: '}:{prop:'Your property',pick:'Choose what you would like help with',propw:'Property',int:'Interested in: '};
    function val(n){var c=pb.querySelector('input[name='+n+']:checked');return c?c.value:null;}
    function upd(){
      var t=val('type'),a=val('away'),cs=[].map.call(pb.querySelectorAll('input[name=care]:checked'),function(x){return x.value;});
      document.getElementById('pt').textContent=t?TYPE[t]:TX.prop;
      document.getElementById('pfs').textContent=a?USE[a]:'';
      document.getElementById('pl').innerHTML=(cs.length?cs.map(function(c){return '<li>'+CARE[c]+'</li>';}).join(''):'<li>'+TX.pick+'</li>');
      var summary=(t?TYPE[t]:TX.propw)+' | '+(a?USE[a]:'')+(cs.length?' | '+TX.int+cs.map(function(c){return CARE[c];}).join(', '):'');
      document.getElementById('pgo').href='../contact/?service=Home+Watch+Program&plan='+encodeURIComponent(summary)+'#form';
    }
    pb.addEventListener('change',upd);upd();
  }
})();
