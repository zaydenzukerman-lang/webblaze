(function(){
  // mobile nav
  var t=document.querySelector('.menu-toggle'),n=document.getElementById('nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});}

  // preview-only forms
  document.querySelectorAll('form[data-preview]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var m=f.querySelector('.form-msg');
      if(m){m.textContent='Thanks! This is a design preview, so nothing was sent.';m.classList.add('show');m.focus&&m.focus();}
    });
  });

  // event planner (facts quoted from the menus on chefrichperry.com)
  var P=document.getElementById('planner');
  if(!P)return;
  var MENUS={
    'passed-appetizers':{name:'Sample Passed Appetizers',url:'../menus/passed-appetizers/',notes:['Pricing based on 50 or more guests will range from 10 to 15 dollars per person for appetizer hour before a catered dinner and 20 to 30 dollars per person for heavy hors d\u2019oeuvres through the night.'],min:50},
    'hors-doeuvres':{name:'Sample Hors d\u2019Oeuvres',url:'../menus/hors-doeuvres/',notes:['Passed and table hors d\u2019oeuvres, Southern menu selections, a carving table presentation and a dessert and coffee presentation.']},
    'entrees':{name:'Sample Entrees',url:'../menus/entrees/',notes:['All our menus are designed with your tastes and dietary needs in mind.']},
    'four-course':{name:'Sample Four Course Dinner',url:'../menus/four-course-dinner/',notes:['Dinner Menus start at $75 per person for 6 or more guests; includes dessert and Four Star Service without the \u201cfour star\u201d prices!'],min:6},
    'buffet':{name:'Beautiful Budget Buffet Package',url:'../menus/budget-buffet/',notes:['Price range $28 to $32 per person, menus designed for you with the seasons and theme in mind.','Includes Bar Snacks, choice of Appetizers for Happy Hour, Two Entrees, Two Starches, Two Veggies, a Caesar or House Salad, and Fresh Bread, Biscuits or Cornbread.']},
    'bbq':{name:'BBQ, Pig Pickin\u2019 and Just Havin\u2019 Fun',url:'../menus/bbq/',notes:['Sample Prices for 50 or more Guests, discounts for numbers 150 and over.','Sample packages on the menu run from $30 per person (Whole Chicken and Ribs with five side dishes) to $90 per person (Lobster, Clams, Shrimp and Mussels with five side dishes).','For specialty whole meat, give two months\u2019 notice so the farmer can select and feed the animal.'],min:50,bulk:150},
    'theme':{name:'Paella & Theme Menus',url:'../menus/paella-theme/',notes:['Spanish Paella Parties, \u201cThe Great Gatsby\u201d 1925 Dinner Party and Tropical Tiki Lounge at the Beach menus.','Our Paella Pescado and Verduras are both gluten free.']},
    'vegetarian':{name:'Vegetarian Sample Menu',url:'../menus/vegetarian/',notes:['Organic produce and vegan groceries can be arranged!']},
    'holiday':{name:'Turkey for the Holidays',url:'../menus/holiday-turkey/',notes:['Holiday Dinner: $40 per person.','Substitute for an item on the menu, or add vegetables for $2 per.']},
    'food-truck':{name:'Longfin Grill Food Truck',url:'../food-truck/',notes:['A 30 foot, commercial kitchen trailer \u2014 a nicer kitchen than many restaurants.']},
    'class':{name:'Team Cooking / Cooking Class',url:'../cooking-classes/',notes:['Most classes average $25 to $45 per person with five person minimum and up to 20 students per class.'],min:5}
  };
  var SUGGEST={
    'Wedding':['passed-appetizers','four-course','buffet','bbq','food-truck'],
    'Corporate event':['passed-appetizers','hors-doeuvres','buffet','bbq','class'],
    'Private dinner party':['four-course','entrees','theme','vegetarian'],
    'BBQ / pig roast / seafood boil':['bbq','buffet'],
    'Cocktail party':['passed-appetizers','hors-doeuvres','theme'],
    'Theme party':['theme','passed-appetizers'],
    'Holiday dinner':['holiday','four-course'],
    'Team cooking / class':['class'],
    'Other occasion':['buffet','passed-appetizers','four-course','bbq']
  };
  var GUESTS={'Under 6':[1,5],'6 to 49':[6,49],'50 to 99':[50,99],'100 to 149':[100,149],'150 or more':[150,9999]};
  var state={type:null,guests:null,menu:null};
  function q(s){return P.querySelector(s);}
  function setPressed(group,val){P.querySelectorAll('[data-group="'+group+'"]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.val===val?'true':'false');});}
  function renderMenus(){
    var box=q('#menu-opts');box.innerHTML='';
    var keys=state.type?SUGGEST[state.type]:Object.keys(MENUS);
    keys.forEach(function(k){var b=document.createElement('button');b.type='button';b.className='opt';b.dataset.group='menu';b.dataset.val=k;b.textContent=MENUS[k].name;b.setAttribute('aria-pressed',state.menu===k?'true':'false');box.appendChild(b);});
  }
  function render(){
    var out=q('#plan-out');
    if(!state.menu){out.innerHTML='<p class="src" style="margin:0">Pick an occasion, your guest count and a menu style to see what Classic Caterers\u2019 sample menus say about it.</p>';return;}
    var m=MENUS[state.menu],h='<h3>'+m.name+'</h3><ul>';
    m.notes.forEach(function(x){h+='<li>'+x+'</li>';});
    var g=state.guests?GUESTS[state.guests]:null;
    if(g&&m.min&&g[1]<m.min){h+='<li><b>Note:</b> the sample pricing above is written for '+m.min+' or more guests, so ask Richard about a menu for your group size.</li>';}
    if(g&&m.bulk&&g[0]>=m.bulk){h+='<li><b>Good news:</b> the BBQ menu lists discounts for numbers 150 and over.</li>';}
    h+='</ul><p class="src">Every menu is designed specifically for you; these notes come from the sample menus. <a href="'+m.url+'">See the full menu</a></p>';
    h+='<button type="button" class="btn btn-primary" id="plan-apply">Add this to my inquiry</button>';
    out.innerHTML=h;
    q('#plan-apply').addEventListener('click',apply);
  }
  function apply(){
    var f=document.getElementById('inquiry');if(!f)return;
    if(state.type)f.elements['event'].value=state.type;
    if(state.guests)f.elements['guests'].value=state.guests;
    if(state.menu)f.elements['menu'].value=MENUS[state.menu].name;
    var msg=f.elements['message'];
    var line='I\u2019m planning: '+(state.type||'an event')+(state.guests?', '+state.guests+' guests':'')+', interested in the '+MENUS[state.menu].name+'.';
    if(msg.value.indexOf('I\u2019m planning:')!==0){msg.value=line+(msg.value?'\n'+msg.value:'');}else{msg.value=line+msg.value.slice(msg.value.indexOf('\n')>-1?msg.value.indexOf('\n'):msg.value.length);}
    f.scrollIntoView({behavior:'smooth',block:'start'});
    setTimeout(function(){f.elements['name'].focus({preventScroll:true});},500);
  }
  P.addEventListener('click',function(e){
    var b=e.target.closest('.opt');if(!b)return;
    var g=b.dataset.group,v=b.dataset.val;
    state[g]=v;setPressed(g,v);
    if(g==='type'){if(state.menu&&SUGGEST[v].indexOf(state.menu)<0)state.menu=null;renderMenus();}
    render();
  });
  // ?menu= preselect from menu pages
  var pm=(location.search.match(/[?&]menu=([a-z-]+)/)||[])[1];
  if(pm&&MENUS[pm]){state.menu=pm;}
  renderMenus();render();
})();
