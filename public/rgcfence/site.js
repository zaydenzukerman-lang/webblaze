/* RGC Fence Inc. - preview by WebBlaze */
(function(){
  "use strict";
  // mobile menu
  var btn=document.querySelector(".menu-btn"),nav=document.getElementById("nav");
  if(btn&&nav){btn.addEventListener("click",function(){var o=nav.classList.toggle("open");btn.setAttribute("aria-expanded",o?"true":"false");});}

  // preview-only forms
  document.querySelectorAll("form[data-preview]").forEach(function(f){
    f.addEventListener("submit",function(e){
      e.preventDefault();
      var ok=f.querySelector(".form-ok");
      if(ok){ok.textContent="Thanks! This is a design preview, so nothing was sent.";ok.classList.add("show");ok.focus&&ok.focus();}
    });
  });

  // fence picker (descriptions are RGC Fence's own wording from rgcfence.com)
  var picker=document.getElementById("picker");
  if(picker){
    var DESC={
      "Vinyl / PVC":"Vinyl fencing is attractive and easy to maintain. It is inexpensive and made from PVC, so it doesn't rot or warp like wood fences do. It also doesn't require painting.",
      "Wood":"Wood is a common option for fencing because it is attractive and popular. There are many types of wood to choose from: Redwood, Cedar, Pine, Fir, and Spruce.",
      "Aluminum":"Aluminum fencing gives you the look of wrought iron in a low maintenance, durable finish. In other words, no rust.",
      "Wrought Iron":"Wrought Iron fencing is long-lasting and very attractive. There are several styles to choose from, require little maintenance, and add curb appeal to your property.",
      "Chain Link":"Chain link fences are low maintenance and inexpensive. They offer security from vandalism and theft as well as help to keep your pets in your back yard.",
      "Gate":"We offer Cantilever, Wooden, Metal and PVC gates, let us help you come to a solution that fits your needs.",
      "Not sure yet":"No problem. RGC Fence Inc. offers free estimates and can help you choose the right fence for your property."
    };
    var state={};
    var out=document.getElementById("picked");
    function render(){
      var m=state.material,html="";
      if(!m&&!state.job&&!state.purpose&&!state.property){out.innerHTML="Pick a few options and we will write your estimate request for you.";return;}
      html="<strong>"+[state.job,m?(m==="Not sure yet"?"fence (material not decided)":m+(m==="Gate"?"":" fence")):"",state.purpose?"for "+state.purpose.toLowerCase():"",state.property?"("+state.property.toLowerCase()+")":""].filter(Boolean).join(" ")+"</strong>";
      if(m&&DESC[m]){html+="<br>"+DESC[m]+"<span class=\"src\">From RGC Fence Inc.</span>";}
      out.innerHTML=html;
    }
    picker.querySelectorAll(".opts").forEach(function(g){
      g.addEventListener("click",function(e){
        var b=e.target.closest(".opt");if(!b)return;
        g.querySelectorAll(".opt").forEach(function(x){x.setAttribute("aria-pressed","false");});
        b.setAttribute("aria-pressed","true");
        state[g.getAttribute("data-key")]=b.getAttribute("data-v")||b.textContent.trim();
        render();
      });
    });
    render();
    var use=document.getElementById("use-pick");
    if(use){use.addEventListener("click",function(){
      var msg=document.getElementById("msg"),parts=[];
      if(state.job)parts.push("Job: "+state.job);
      if(state.material)parts.push("Fence type: "+state.material);
      if(state.purpose)parts.push("Purpose: "+state.purpose);
      if(state.property)parts.push("Property: "+state.property);
      msg.value=(parts.length?"Free estimate request\n"+parts.join("\n")+"\n\n":"")+"Details: ";
      var t=document.getElementById("est-form");
      t.scrollIntoView({behavior:"smooth",block:"start"});
      setTimeout(function(){msg.focus();msg.setSelectionRange(msg.value.length,msg.value.length);},400);
    });}
  }

  // gallery filter + lightbox
  var gal=document.querySelector(".gal");
  if(gal){
    document.querySelectorAll(".filters .opt").forEach(function(f){
      f.addEventListener("click",function(){
        document.querySelectorAll(".filters .opt").forEach(function(x){x.setAttribute("aria-pressed","false");});
        f.setAttribute("aria-pressed","true");
        var c=f.getAttribute("data-f");
        gal.querySelectorAll("button").forEach(function(b){b.hidden=!(c==="all"||b.getAttribute("data-cat")===c);});
      });
    });
    var lb=document.getElementById("lb");
    if(lb&&lb.showModal){
      var li=lb.querySelector("img"),lp=lb.querySelector("p");
      gal.addEventListener("click",function(e){
        var b=e.target.closest("button");if(!b)return;
        var im=b.querySelector("img");
        li.src=b.getAttribute("data-full");li.alt=im.alt;lp.textContent=im.alt;
        lb.showModal();
      });
      lb.querySelector(".lb-close").addEventListener("click",function(){lb.close();});
      lb.addEventListener("click",function(e){if(e.target===lb)lb.close();});
    }
  }
})();
