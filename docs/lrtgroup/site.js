(function(){
  // mobile nav
  var b=document.querySelector('.burger'),n=document.querySelector('.nav');
  if(b&&n){b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}

  // Printer finder: facts only, taken from lrtgroup.com
  // PX800: 360 DPI, tape 1/6" to 1-1/2", computer, app, router/LAN
  // PX400: 180 DPI, tape 1/6" to 1", computer, app (Bluetooth), portable
  // C610 : 360 DPI, tape 1/6" to 1", computer, app
  var P={
    'LW-PX800':{w:1.5,dpi:360,net:true,port:false},
    'LW-PX400':{w:1,dpi:180,net:false,port:true},
    'LW-C610':{w:1,dpi:360,net:false,port:false}
  };
  var f=document.getElementById('finder');
  function val(name){var el=f.querySelector('input[name="'+name+'"]:checked');return el?el.value:'any';}
  function run(){
    var width=val('width'),dpi=val('dpi'),conn=val('conn');
    var cards=f.querySelectorAll('.pcard'),fits=[];
    cards.forEach(function(c){
      var m=c.getAttribute('data-model'),p=P[m],why=[];
      if(width==='1.5'&&p.w<1.5) why.push('Takes tapes up to 1" only');
      if(dpi==='360'&&p.dpi<360) why.push('Prints at 180 DPI');
      if(conn==='net'&&!p.net) why.push('No router / network option listed');
      if(conn==='field'&&!p.port) why.push('Not the portable Bluetooth model');
      c.classList.remove('best','nofit');
      var w=c.querySelector('.why');
      if(why.length){c.classList.add('nofit');w.className='why bad';w.textContent=why.join(' \u00b7 ');}
      else{fits.push(c);w.className='why good';w.textContent='Fits what you picked';}
    });
    // highlight the single best fit: if several fit, prefer the lowest listed price
    if(fits.length){
      fits.sort(function(a,b){return +a.getAttribute('data-price')-+b.getAttribute('data-price');});
      fits[0].classList.add('best');
    }
  }
  if(f){f.addEventListener('change',run);run();}

  // "Request this printer" buttons prefill the order form
  var sel=document.getElementById('q-printer');
  document.querySelectorAll('[data-pick]').forEach(function(a){
    a.addEventListener('click',function(e){
      if(sel){e.preventDefault();sel.value=a.getAttribute('data-pick');
        var t=document.getElementById('order');if(t)t.scrollIntoView({behavior:'smooth',block:'start'});
        setTimeout(function(){var nm=document.getElementById('q-name');if(nm)nm.focus({preventScroll:true});},500);}
    });
  });
  // prefill from ?printer= on the contact page
  try{var q=new URLSearchParams(location.search).get('printer');if(q&&sel){for(var i=0;i<sel.options.length;i++){if(sel.options[i].value===q){sel.value=q;break;}}}}catch(e){}

  // preview-only form
  document.querySelectorAll('form.qf').forEach(function(form){
    form.addEventListener('submit',function(e){e.preventDefault();
      var d=form.querySelector('.done');d.textContent='Thanks! This is a design preview, so nothing was sent.';d.classList.add('show');
      form.querySelector('button[type=submit]').disabled=true;});
  });

  // click-to-load YouTube
  document.querySelectorAll('.vid[data-yt]').forEach(function(v){
    v.addEventListener('click',function(){
      var id=v.getAttribute('data-yt'),fr=document.createElement('iframe');
      fr.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0';
      fr.title=v.getAttribute('aria-label')||'Video';fr.allow='autoplay; encrypted-media; picture-in-picture';fr.allowFullscreen=true;
      v.innerHTML='';v.appendChild(fr);
    },{once:true});
  });
})();
