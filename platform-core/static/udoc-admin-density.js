/*! udoc-admin-density.js — densify UDOC Admin (additive)
 * Does not replace Layers / EVA / login core.
 */
(function(){
  if(window.__UDOC_ADMIN_DENSITY__) return; window.__UDOC_ADMIN_DENSITY__=1;
  const API = location.origin;

  function el(tag, attrs, html){
    const n=document.createElement(tag);
    if(attrs) Object.entries(attrs).forEach(function(pair){
      var k=pair[0], v=pair[1];
      if(k==='className') n.className=v;
      else if(k.startsWith('on') && typeof v==='function') n.addEventListener(k.slice(2).toLowerCase(),v);
      else n.setAttribute(k,v);
    });
    if(html!=null) n.innerHTML=html;
    return n;
  }

  function css(){
    if(document.getElementById('uad-css')) return;
    var s=el('style',{id:'uad-css'});
    s.textContent='#uad-root{margin:12px 16px 24px;max-width:1200px}.uad-panel{background:var(--navy2,#0c1830);border:1px solid var(--line,#1c2a45);border-radius:12px;padding:14px;margin-top:12px}.uad-panel h3{margin:0 0 10px;color:var(--gold,#C9A84C);font-size:13px}.uad-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.uad-chip{display:inline-block;border:1px solid var(--line,#1c2a45);border-radius:16px;padding:4px 10px;font-size:11px;cursor:pointer;background:transparent;color:var(--ink,#e8edf6);text-decoration:none}.uad-chip:hover{border-color:var(--cyan,#00C2D4)}.uad-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin-top:8px}.uad-card{background:#0a1528;border:1px solid var(--line,#1c2a45);border-radius:10px;padding:10px}.uad-card h4{margin:0 0 4px;font-size:10px;text-transform:uppercase;color:var(--gold,#C9A84C)}.uad-metric{font-size:1.1rem;font-weight:700}.uad-term{font-family:ui-monospace,monospace;font-size:11px;background:#050b16;border:1px solid #1c2a45;border-radius:8px;padding:10px;white-space:pre-wrap;max-height:200px;overflow:auto;margin-top:8px}.uad-mut{color:#8fa0bd;font-size:11px;margin:8px 0 0}.uad-assessor{border-color:rgba(0,194,212,.4);background:rgba(0,194,212,.07)}';
    document.head.appendChild(s);
  }

  function term(msg){
    var t=document.getElementById('uad-term');
    if(t) t.textContent=new Date().toLocaleTimeString()+' '+msg+'\n'+(t.textContent||'').slice(0,3000);
  }

  async function evaBatch(){
    try{
      var r=await fetch(API+'/decisions/batch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenarios:['fair','biased']})});
      var j=await r.json();
      var o=j.outcomes||{};
      var gate=(Number(o.BLOCK||0)>=1)?'PASS':'CHECK';
      var n=document.getElementById('uad-eva'); if(n) n.textContent=gate+' · B'+(o.BLOCK||0)+'/A'+(o.APPROVE||0);
      term('EVA '+gate+' '+JSON.stringify(o));
      return j;
    }catch(e){ term('EVA FAIL '+e.message); }
  }

  async function ready(){
    try{
      var j=await (await fetch(API+'/udoc/demo/ready')).json();
      var n=document.getElementById('uad-ready'); if(n) n.textContent=j.ready?'DEMO READY':'NOT READY';
      term('READY '+JSON.stringify({ready:j.ready,model:j.model_001,rules:j.active_rules}));
    }catch(e){ term('READY FAIL '+e.message); }
  }

  async function health(){
    try{ term('HEALTH '+JSON.stringify(await (await fetch(API+'/health')).json())); }
    catch(e){ term('HEALTH FAIL '+e.message); }
  }

  async function layersProbe(){
    try{
      var paths=['/udoc/lifecycle','/udoc/control','/policy/active','/gis/gbs/pillars'];
      var out=[];
      for(var i=0;i<paths.length;i++){
        var p=paths[i];
        try{ var r=await fetch(API+p); out.push(p+' → '+r.status); }catch(e){ out.push(p+' → ERR'); }
      }
      term('LAYERS probe\n'+out.join('\n'));
      await evaBatch();
    }catch(e){ term('LAYERS FAIL '+e.message); }
  }

  async function divStrip(){
    try{
      var pair=await Promise.all([
        fetch(API+'/seths/metrics').then(function(r){return r.ok?r.json():{};}).catch(function(){return {};}),
        fetch(API+'/ts/metrics').then(function(r){return r.ok?r.json():{};}).catch(function(){return {};}),
        fetch(API+'/madiba/metrics').then(function(r){return r.ok?r.json():{};}).catch(function(){return {};})
      ]);
      var s=pair[0], t=pair[1], m=pair[2];
      var el=document.getElementById('uad-div');
      if(el) el.textContent='SETHS placed '+(s.placed!=null?s.placed:'—')+' / '+(s.total!=null?s.total:'—')+' · TS projects '+(t.projects!=null?t.projects:'—')+' · MADIBA cycles '+(m.cycles!=null?m.cycles:'—')+' · recycled '+(m.cumulative_recycled!=null?m.cumulative_recycled:'—');
      term('DIV strip ok');
    }catch(e){ term('DIV FAIL '+e.message); }
  }

  function mount(){
    css();
    if(document.getElementById('uad-root')) return;
    var root=el('div',{id:'uad-root'});
    var a2=el('div',{className:'uad-panel uad-assessor'});
    a2.appendChild(el('h3',{},'UDOC Admin · Assessor density strip'));
    var row2=el('div',{className:'uad-row'});
    [['EVA fair/biased',evaBatch],['demo/ready',ready],['/health',health],['Layers probe',layersProbe],['Division strip',divStrip]].forEach(function(pair){
      var b=el('button',{type:'button',className:'uad-chip'},pair[0]); b.onclick=pair[1]; row2.appendChild(b);
    });
    ['/Sentinel','/divisions','/portals','/gbs','/seths','/admin'].forEach(function(h){
      row2.appendChild(el('a',{className:'uad-chip',href:h},h.slice(1)+' →'));
    });
    a2.appendChild(row2);
    var grid=el('div',{className:'uad-grid'});
    grid.innerHTML='<div class="uad-card"><h4>EVA gate</h4><div class="uad-metric" id="uad-eva">—</div></div><div class="uad-card"><h4>Ready</h4><div class="uad-metric" id="uad-ready">—</div></div><div class="uad-card"><h4>Honesty</h4><div class="uad-metric" style="font-size:0.85rem">capital not_deployed</div></div><div class="uad-card"><h4>Package</h4><div class="uad-metric" style="font-size:0.85rem">Internal UDOC</div></div>';
    a2.appendChild(grid);
    a2.appendChild(el('p',{className:'uad-mut'},'Additive density · Layers + EVA + policy remain source of truth · biased must BLOCK'));
    root.appendChild(a2);

    var div=el('div',{className:'uad-panel'});
    div.appendChild(el('h3',{},'Division strip · live'));
    div.appendChild(el('div',{id:'uad-div',className:'uad-mut'},'Run Division strip'));
    root.appendChild(div);

    var help=el('div',{className:'uad-panel'});
    help.innerHTML='<h3>UDOC Admin · Capstone map</h3><div class="uad-row"><span class="uad-chip">Layers probe</span><span class="uad-chip">EVA batch</span><span class="uad-chip">Policy-to-code</span><span class="uad-chip">EIF Diamond</span><span class="uad-chip">Intel dual-path</span><span class="uad-chip">HITL portals</span></div><p class="uad-mut">Staff: admin@gods.local / admin123 · seths@ / staff123 · Internal package only</p>';
    root.appendChild(help);

    var bridge=el('div',{className:'uad-panel'});
    bridge.appendChild(el('h3',{},'Admin density terminal'));
    bridge.appendChild(el('div',{className:'uad-term',id:'uad-term'},'UDOC Admin density · probes'));
    root.appendChild(bridge);

    var main = document.querySelector('main') || document.querySelector('.wrap') || document.body;
    if(main.firstChild) main.insertBefore(root, main.firstChild);
    else main.appendChild(root);

    setTimeout(function(){ ready().catch(function(){}); divStrip().catch(function(){}); }, 600);
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount);
  else mount();
})();
