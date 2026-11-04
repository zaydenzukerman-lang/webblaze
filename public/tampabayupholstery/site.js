(function(){
var mb=document.querySelector('.menu-btn'),ul=document.querySelector('nav ul');
mb.addEventListener('click',function(){var o=ul.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
ul.addEventListener('click',function(e){if(e.target.tagName==='A')ul.classList.remove('open')});
var sel=document.getElementById('service'),msg=document.getElementById('message');
var T={boat_canvas:['Boat canvas','I need boat canvas (Sunbrella). Boat type and what I need covered: '],
boat_upholstery:['Boat upholstery','I need boat upholstery (Naugahyde vinyl). Boat type and which seats: '],
awning:['Awning or shade structure','I need an awning or shade structure for: '],
restaurant_hotel:['Restaurant or hotel seating','I need restaurant or hotel seating reupholstered. Business name and what needs work: ']};
var opts=document.querySelectorAll('.opt');
opts.forEach(function(b){b.addEventListener('click',function(){
opts.forEach(function(x){x.setAttribute('aria-pressed','false')});b.setAttribute('aria-pressed','true');
var k=b.dataset.k;sel.value=T[k][0];msg.value=T[k][1];
document.getElementById('quote-form').scrollIntoView({behavior:'smooth',block:'center'});msg.focus({preventScroll:true});
})});
sel.addEventListener('change',function(){opts.forEach(function(b){b.setAttribute('aria-pressed',T[b.dataset.k][0]===sel.value?'true':'false')})});
document.querySelectorAll('form').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();f.querySelector('.thanks').classList.add('show')})});
var ph=document.getElementById('photos');ph.addEventListener('change',function(){document.getElementById('fl').textContent=[].map.call(ph.files,function(f){return f.name}).join(', ')});
var fs=document.querySelectorAll('.f'),figs=document.querySelectorAll('.grid figure');
fs.forEach(function(b){b.addEventListener('click',function(){
fs.forEach(function(x){x.setAttribute('aria-pressed','false')});b.setAttribute('aria-pressed','true');
figs.forEach(function(g){g.hidden=!(b.dataset.f==='all'||g.dataset.c===b.dataset.f)})})});
})();
