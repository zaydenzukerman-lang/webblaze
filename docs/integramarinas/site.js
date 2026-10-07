/* Williams Island Marina - WebBlaze preview */
(function(){
  "use strict";
  var doc=document.documentElement; doc.classList.remove("no-js");
  var MAX_LOA=140, MAX_DRAFT=10; /* published on integramarinas.com marina page */

  /* mobile menu */
  var bt=document.querySelector(".burger"), menu=document.getElementById("menu");
  if(bt&&menu){bt.addEventListener("click",function(){var o=menu.classList.toggle("open");bt.setAttribute("aria-expanded",o?"true":"false");});}

  /* reveal on scroll */
  var rv=document.querySelectorAll(".rv");
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});},{rootMargin:"0px 0px -8% 0px"});
    rv.forEach(function(el){io.observe(el);});
  } else rv.forEach(function(el){el.classList.add("in");});

  /* preview-only forms */
  document.querySelectorAll("form[data-preview]").forEach(function(f){
    f.addEventListener("submit",function(ev){
      ev.preventDefault();
      var ok=f.querySelector(".form-ok"); if(ok){ok.classList.add("show");ok.focus&&ok.focus();}
    });
  });

  /* hero video: desktop only, after load, respects reduced motion + data saver */
  var hv=document.querySelector("[data-hero-video]");
  if(hv){
    var slow=navigator.connection&&(navigator.connection.saveData||/2g/.test(navigator.connection.effectiveType||""));
    var rm=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if(!slow&&!rm&&window.matchMedia("(min-width: 900px)").matches){
      window.addEventListener("load",function(){
        var v=document.createElement("video");
        v.muted=true;v.loop=true;v.playsInline=true;v.setAttribute("muted","");v.setAttribute("playsinline","");v.setAttribute("aria-hidden","true");
        v.preload="auto";v.src=hv.getAttribute("data-hero-video");
        v.addEventListener("canplaythrough",function(){var p=v.play();if(p&&p.catch)p.catch(function(){});v.classList.add("on");},{once:true});
        hv.appendChild(v);
      });
    }
  }

  /* today's hours */
  var today=new Date().getDay();
  document.querySelectorAll(".hours tr[data-d]").forEach(function(tr){if(+tr.getAttribute("data-d")===today)tr.classList.add("today");});

  /* live conditions (Open-Meteo, no key) */
  var cd=document.getElementById("conditions");
  if(cd&&window.fetch){
    var url="https://api.open-meteo.com/v1/forecast?latitude=25.9402&longitude=-80.1364&current=temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=kn&timezone=America%2FNew_York";
    fetch(url).then(function(r){return r.ok?r.json():null;}).then(function(d){
      if(!d||!d.current)return;
      var c=d.current, dirs=["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"];
      var dir=dirs[Math.round(((c.wind_direction_10m||0)%360)/22.5)%16];
      var set=function(k,v){var el=cd.querySelector("[data-k="+k+"]");if(el)el.textContent=v;};
      set("t",Math.round(c.temperature_2m)+"\u00B0F");
      set("w",Math.round(c.wind_speed_10m)+" kn "+dir);
      set("g",Math.round(c.wind_gusts_10m)+" kn");
      set("p",(c.precipitation_probability==null?"-":c.precipitation_probability+"%"));
      var n=document.getElementById("cond-time");
      if(n){var t=new Date(c.time);n.textContent="Live from Open-Meteo, updated "+t.toLocaleTimeString([], {hour:"numeric",minute:"2-digit"})+".";}
    }).catch(function(){});
  }

  /* helpers */
  function num(el){if(!el)return NaN;var v=parseFloat(el.value);return isNaN(v)?NaN:v;}
  function ftm(v){return (v*0.3048).toFixed(1)+" m";}

  /* home: quick fit check -> slips page */
  var mini=document.getElementById("fitmini");
  if(mini){
    var ml=mini.querySelector("[name=loa]"), md=mini.querySelector("[name=draft]"), out=document.getElementById("fitmini-out");
    var upd=function(){
      var L=num(ml),D=num(md);
      if(isNaN(L)&&isNaN(D)){out.className="verdict";out.textContent="Enter your boat's length and draft to check it against the marina's published limits.";return;}
      var bad=[];
      if(!isNaN(L)&&L>MAX_LOA)bad.push("length is over the 140 ft maximum");
      if(!isNaN(D)&&D>MAX_DRAFT)bad.push("draft is over the 10 ft maximum");
      if(bad.length){out.className="verdict no";out.textContent="Your "+bad.join(" and ")+". Call the marina office at (305) 937-7813 to talk it through.";}
      else{out.className="verdict ok";out.textContent="Within the published limits (up to 140 ft length, 10 ft draft). Next step: send your slip request.";}
    };
    ml.addEventListener("input",upd);md.addEventListener("input",upd);upd();
    mini.addEventListener("submit",function(e){
      e.preventDefault();
      var q=[];if(ml.value)q.push("loa="+encodeURIComponent(ml.value));if(md.value)q.push("draft="+encodeURIComponent(md.value));
      location.href="slips/"+(q.length?"?"+q.join("&"):"")+"#builder";
    });
  }

  /* slips: request builder */
  var b=document.getElementById("builder-form");
  if(b){
    var g=function(n){return b.querySelector("[name="+n+"]");};
    var qs=new URLSearchParams(location.search);
    ["loa","beam","draft"].forEach(function(k){var v=qs.get(k);if(v&&!isNaN(parseFloat(v)))g(k).value=parseFloat(v);});
    var today0=new Date();today0.setHours(0,0,0,0);
    var iso=function(d){var m=d.getMonth()+1,dd=d.getDate();return d.getFullYear()+"-"+(m<10?"0":"")+m+"-"+(dd<10?"0":"")+dd;};
    g("arrive").min=iso(today0); g("depart").min=iso(today0);
    var bars={loa:[MAX_LOA,"ft"],draft:[MAX_DRAFT,"ft"]};
    function render(){
      var L=num(g("loa")),B=num(g("beam")),D=num(g("draft"));
      Object.keys(bars).forEach(function(k){
        var v=num(g(k)), row=document.querySelector(".bar[data-k="+k+"]"); if(!row)return;
        var pct=isNaN(v)?0:Math.min(100,v/bars[k][0]*100);
        row.querySelector(".fill").style.width=pct+"%";
        row.classList.toggle("over",!isNaN(v)&&v>bars[k][0]);
        row.querySelector(".val").textContent=isNaN(v)?"- / "+bars[k][0]+" ft":v+" / "+bars[k][0]+" ft";
      });
      var a=g("arrive").value,d=g("depart").value,nights=NaN;
      if(a&&d){nights=Math.round((new Date(d+"T12:00")-new Date(a+"T12:00"))/864e5);}
      if(a&&g("depart").min!==a){g("depart").min=a;}
      var v=document.getElementById("verdict"), probs=[];
      if(!isNaN(L)&&L>MAX_LOA)probs.push("length is over the 140 ft maximum");
      if(!isNaN(D)&&D>MAX_DRAFT)probs.push("draft is over the 10 ft maximum");
      if(!isNaN(nights)&&nights<=0)probs.push("departure date needs to be after arrival");
      if(probs.length){v.className="verdict no";v.textContent="Heads up: your "+probs.join(", ")+". You can still send the request or call (305) 937-7813.";}
      else if(isNaN(L)||isNaN(D)){v.className="verdict";v.textContent="Add your length and draft to check the fit.";}
      else{v.className="verdict ok";v.textContent="Your boat fits the published limits. Add it to your request below.";}
      var s=[];
      if(!isNaN(L))s.push("<b>"+L+" ft</b> LOA ("+ftm(L)+")");
      if(!isNaN(B))s.push("<b>"+B+" ft</b> beam");
      if(!isNaN(D))s.push("<b>"+D+" ft</b> draft");
      if(g("power").value)s.push("<b>"+esc(g("power").value)+"</b> shore power");
      if(!isNaN(nights)&&nights>0)s.push("<b>"+nights+" night"+(nights===1?"":"s")+"</b>");
      document.getElementById("summary").innerHTML=s.length?"Your request: "+s.join(" &middot; "):"Your request summary will appear here.";
    }
    function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c];});}
    b.addEventListener("input",render);b.addEventListener("change",render);render();
    b.addEventListener("submit",function(e){
      e.preventDefault();
      var f=document.getElementById("slip-form"); if(!f)return;
      var map={loa:"length",beam:"beam",draft:"draftf",power:"shore",arrive:"arrival",depart:"departure",boat:"boatname"};
      Object.keys(map).forEach(function(k){
        var src=g(k), dst=f.querySelector("[name="+map[k]+"]");
        if(src&&dst&&src.value){dst.value=src.value+((k==="loa"||k==="beam"||k==="draft")?" ft":"");dst.classList.remove("prefilled");void dst.offsetWidth;dst.classList.add("prefilled");}
      });
      document.getElementById("request").scrollIntoView({behavior:"smooth",block:"start"});
      setTimeout(function(){var n=f.querySelector("[name=fullname]");if(n)n.focus({preventScroll:true});},600);
    });
  }
})();
