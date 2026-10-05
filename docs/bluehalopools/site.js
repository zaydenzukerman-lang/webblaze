
(function(){
  var b=document.querySelector('.burger'),u=document.querySelector('.links');
  if(b&&u)b.addEventListener('click',function(){var o=u.classList.toggle('open');b.setAttribute('aria-expanded',o);});
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.1}):null;
  document.querySelectorAll('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in');});
  // Pool Health Report
  var R=window.BH_REPORT, rep=document.getElementById('report');
  if(R&&rep){
    function draw(k){var d=R[k],svg=document.getElementById('rt-svg'),W=520,H=170,pl=40,pr=14,pt=14,pb=28;
      var vals=d.pts.map(function(p){return p[1]}),lo=Math.min(d.min,Math.min.apply(0,vals)),hi=Math.max(d.max,Math.max.apply(0,vals)),pad=(hi-lo)*.15;lo-=pad;hi+=pad;
      var x=function(i){return pl+i*(W-pl-pr)/(d.pts.length-1)},y=function(v){return pt+(hi-v)*(H-pt-pb)/(hi-lo)};
      var band='<rect x="'+pl+'" y="'+y(d.max)+'" width="'+(W-pl-pr)+'" height="'+(y(d.min)-y(d.max))+'" fill="#e6f2fa" rx="6"/>';
      var line=d.pts.map(function(p,i){return (i?'L':'M')+x(i).toFixed(1)+' '+y(p[1]).toFixed(1)}).join(' ');
      var dots=d.pts.map(function(p,i){var last=i===d.pts.length-1;return '<circle cx="'+x(i)+'" cy="'+y(p[1])+'" r="'+(last?6:4.5)+'" fill="'+(last?'#1d6e9e':'#fff')+'" stroke="#1d6e9e" stroke-width="2.5"><title>'+p[0]+' — '+p[1]+(d.unit?' '+d.unit:'')+'</title></circle>'+
        '<text x="'+x(i)+'" y="'+(H-8)+'" text-anchor="middle" font-size="11" fill="#5a6c79">'+p[0]+'</text>'+
        '<text x="'+x(i)+'" y="'+(y(p[1])-11)+'" text-anchor="middle" font-size="11" font-weight="600" fill="#15324a">'+p[1]+'</text>'}).join('');
      var lab='<text x="4" y="'+(y(d.max)+4)+'" font-size="10.5" fill="#5a6c79">'+d.max+'</text><text x="4" y="'+(y(d.min)+4)+'" font-size="10.5" fill="#5a6c79">'+d.min+'</text>';
      svg.innerHTML=band+lab+'<path d="'+line+'" fill="none" stroke="#3fa9e0" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'+dots;
      svg.setAttribute('aria-label',d.h+'. '+d.pts.map(function(p){return p[0]+' '+p[1]}).join(', '));
      document.getElementById('rt-h').textContent=d.h;document.getElementById('rt-tg').textContent=d.tg;document.getElementById('rt-n').textContent=d.note;
      rep.querySelectorAll('.tile').forEach(function(t){t.setAttribute('aria-pressed',t.dataset.k===k)});}
    rep.querySelectorAll('.tile').forEach(function(t){t.addEventListener('click',function(){draw(t.dataset.k)})});draw('cl');
  }
  // quote builder
  var f=document.getElementById('qform');
  if(f){
    var plan=new URLSearchParams(location.search).get('plan'),qp=document.getElementById('qplan');
    if(plan&&qp){qp.style.display='block';qp.innerHTML='<b>Plan selected:</b> Halo '+plan.charAt(0).toUpperCase()+plan.slice(1)+' · <a href="#" id="qclear" style="text-decoration:underline">clear</a>';document.getElementById('qclear').onclick=function(e){e.preventDefault();qp.style.display='none';};}
    var bar=document.getElementById('qbar');
    function go(n){f.querySelectorAll('.qstep').forEach(function(s){s.classList.toggle('on',s.dataset.s==n)});bar.style.width=(n==1?50:100)+'%';f.scrollIntoView({behavior:'smooth',block:'start'});}
    document.getElementById('qnext').onclick=function(){go(2)};document.getElementById('qback').onclick=function(){go(1)};
    f.addEventListener('submit',function(e){e.preventDefault();var bad=[].filter.call(f.querySelectorAll('.qstep[data-s="2"] [required]'),function(i){return i.type==='checkbox'?!i.checked:!i.value.trim()});
      if(bad.length){bad[0].focus();bad[0].reportValidity&&bad[0].reportValidity();return;}
      f.querySelectorAll('.qstep').forEach(function(s){s.classList.remove('on')});document.querySelector('.prog').style.display='none';document.getElementById('qthanks').style.display='block';});
  }
  // area checker
  var fs=document.getElementById('finder');
  if(fs){var res=document.getElementById('fres');fs.addEventListener('change',function(){var o=fs.selectedOptions[0];
    if(!fs.value){res.innerHTML='';return;}
    if(fs.value==='other'){res.innerHTML='Send the address through and we\'ll tell you which day we run near you. <a href="../quote/" style="color:var(--deep);font-weight:600">Get a quote →</a>';return;}
    res.innerHTML='<b>Yes, we service '+o.textContent+'.</b> <a href="../'+fs.value+'/" style="color:var(--deep);font-weight:600">See what we see there →</a>';});}
})();
