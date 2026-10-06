// AAA Pool & Spa preview: mobile menu, preview-only forms, service picker.
(function(){
  var hdr=document.querySelector('.hdr'),b=document.querySelector('.burger');
  if(b){b.addEventListener('click',function(){var o=hdr.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}

  // Forms are preview-only: never submit anywhere.
  document.querySelectorAll('form.form').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var ok=f.querySelector('.ok');if(ok){ok.hidden=false;ok.scrollIntoView({block:'nearest',behavior:'smooth'});}
    });
  });

  // Service picker: shows what's included (from their services page) and fills "Type of service".
  var q=document.getElementById('quote');
  if(!q||!window.SVC)return;
  var boxes=q.querySelectorAll('input[name=svc]'),incl=document.getElementById('incl'),
      field=document.getElementById('svcfield'),chem=document.getElementById('chem');
  function update(){
    var names=[],html='',res=false;
    boxes.forEach(function(c){
      c.parentNode.classList.toggle('on',c.checked);
      if(!c.checked)return;
      var s=window.SVC[c.value];names.push(c.dataset.title);
      if(c.value==='residential')res=true;
      html+='<div class="box"><b>'+s.t+'</b><ul>'+s.inc.map(function(x){return '<li>'+x+'</li>';}).join('')+'</ul></div>';
    });
    chem.hidden=!res;
    var c=q.querySelector('input[name=chem]:checked');
    if(res&&c){var i=names.indexOf('Residential Pool Maintenance');names[i]+=' ('+c.value.toLowerCase()+')';}
    incl.innerHTML=html;
    field.value=names.join(', ');
  }
  boxes.forEach(function(c){c.addEventListener('change',update);});
  q.querySelectorAll('input[name=chem]').forEach(function(r){r.addEventListener('change',update);});
  // Deep link from the services page: ?service=residential
  var m=/[?&]service=([a-z-]+)/.exec(location.search);
  if(m){boxes.forEach(function(c){if(c.value===m[1])c.checked=true;});update();}
})();
