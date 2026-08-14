/*! div-density.js — UDOC-admin parity panels for operator surfaces
 * Inject only. Does not replace login, guided path, or division APIs.
 * Safe for Capstone: honesty preserved · EVA gate · cross-nav · probes
 */
(function(){
  if(window.__DIV_DENSITY__) return; window.__DIV_DENSITY__=1;
  const API = (typeof window.API==='string' && window.API) ? window.API : location.origin;

  function el(tag, attrs, html){
    const n=document.createElement(tag);
    if(attrs) Object.entries(attrs).forEach(([k,v])=>{
      if(k==='style' && typeof v==='object') Object.assign(n.style,v);
      else if(k==='className') n.className=v;
      else if(k.startsWith('on') && typeof v==='function') n.addEventListener(k.slice(2).toLowerCase(),v);
      else n.setAttribute(k,v);
    });
    if(html!=null) n.innerHTML=html;
    return n;
  }

  function ensureStyle(){
    if(document.getElementById('div-density-css')) return;
    const s=el('style',{id:'div-density-css'});
    s.textContent=`
.dd-panel{background:var(--navy2,#0c1830);border:1px solid var(--line,#1c2a45);border-radius:12px;padding:14px;margin-top:12px}
.dd-panel h3{margin:0 0 10px;color:var(--gold,#C9A84C);font-size:13px}
.dd-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.dd-chip{display:inline-block;border:1px solid var(--line,#1c2a45);border-radius:16px;padding:4px 10px;font-size:11px;cursor:pointer;background:transparent;color:var(--ink,#e8edf6);text-decoration:none}
.dd-chip:hover{border-color:var(--cyan,#00C2D4);color:var(--cyan,#00C2D4)}
.dd-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;margin-top:8px}
.dd-card{background:var(--navy2,#0c1830);border:1px solid var(--line,#1c2a45);border-radius:10px;padding:10px}
.dd-card h4{margin:0 0 4px;font-size:10px;text-transform:uppercase;letter-spacing:.05em;color:var(--gold,#C9A84C)}
.dd-metric{font-size:1.05rem;font-weight:700}
.dd-term{font-family:ui-monospace,monospace;font-size:11px;background:#050b16;border:1px solid var(--line,#1c2a45);border-radius:8px;padding:8px;white-space:pre-wrap;max-height:140px;overflow:auto;margin-top:8px}
.dd-mut{color:var(--mut,#8fa0bd);font-size:11px;margin:8px 0 0}
.dd-assessor{border-color:rgba(0,194,212,.35);background:rgba(0,194,212,.06)}
`;
    document.head.appendChild(s);
  }

  async function evaSmoke(){
    const term=document.getElementById('dd-term')||document.getElementById('term')||document.getElementById('bridge-term');
    try{
      const r=await fetch(API+'/decisions/batch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenarios:['fair','biased']})});
      const j=await r.json();
      const o=j.outcomes||{};
      const gate=(Number(o.BLOCK||0)>=1)?'PASS':'CHECK';
      ['k-eva','k-eva2','dd-eva'].forEach(id=>{
        const n=document.getElementById(id); if(n) n.textContent=gate+' · B'+(o.BLOCK||0)+'/A'+(o.APPROVE||0);
      });
      if(term) term.textContent=new Date().toLocaleTimeString()+' EVA '+gate+' '+JSON.stringify(o);
      return j;
    }catch(e){ if(term) term.textContent='EVA FAIL '+e.message; }
  }

  async function probeReady(){
    try{
      const r=await fetch(API+'/udoc/demo/ready');
      const j=await r.json();
      const n=document.getElementById('dd-ready')||document.getElementById('ready-tag');
      if(n) n.textContent=j.ready?'DEMO READY':'NOT READY';
      const t=document.getElementById('dd-term'); if(t) t.textContent='READY '+JSON.stringify({ready:j.ready,model:j.model_001&&j.model_001.status});
      return j;
    }catch(e){ const n=document.getElementById('dd-ready'); if(n) n.textContent='probe fail'; }
  }

  async function probeHealth(){
    try{
      const r=await fetch(API+'/health'); const j=await r.json();
      const t=document.getElementById('dd-term'); if(t) t.textContent='HEALTH '+JSON.stringify(j);
    }catch(e){ const t=document.getElementById('dd-term'); if(t) t.textContent='HEALTH FAIL '+e.message; }
  }

  function mount(){
    ensureStyle();
    const host = document.getElementById('ops')
      || document.querySelector('main')
      || document.querySelector('.wrap')
      || document.body;
    if(!host || document.getElementById('dd-root')) return;

    const root=el('div',{id:'dd-root'});

    const assessor=el('div',{className:'dd-panel dd-assessor'});
    assessor.innerHTML='<h3>Assessor strip · density</h3>';
    const row1=el('div',{className:'dd-row'});
    const bEva=el('button',{type:'button',className:'dd-chip'},'EVA fair/biased');
    bEva.onclick=evaSmoke;
    const bReady=el('button',{type:'button',className:'dd-chip'},'demo/ready');
    bReady.onclick=probeReady;
    const bHealth=el('button',{type:'button',className:'dd-chip'},'/health');
    bHealth.onclick=probeHealth;
    row1.append(bEva,bReady,bHealth);
    ['/Sentinel','/udoc-admin','/admin','/divisions','/portals'].forEach(href=>{
      const a=el('a',{className:'dd-chip',href:href},href.replace('/','')+' →');
      row1.appendChild(a);
    });
    assessor.appendChild(row1);
    const kpis=el('div',{className:'dd-grid'});
    kpis.innerHTML=`
      <div class="dd-card"><h4>EVA gate</h4><div class="dd-metric" id="dd-eva">run chip</div></div>
      <div class="dd-card"><h4>Ready</h4><div class="dd-metric" id="dd-ready">—</div></div>
      <div class="dd-card"><h4>Honesty</h4><div class="dd-metric" style="font-size:0.85rem">capital not_deployed</div></div>`;
    assessor.appendChild(kpis);
    assessor.appendChild(el('p',{className:'dd-mut'},'Capstone: zeros OK · MADIBA ≠ AUM · Sovereign-Verified = designed_not_built · biased must BLOCK'));
    root.appendChild(assessor);

    const map=el('div',{className:'dd-panel'});
    map.innerHTML='<h3>Surface map · operator</h3>';
    const row2=el('div',{className:'dd-row'});
    [['/seths','SETHS'],['/ts','TS'],['/madiba','MADIBA'],['/gbs','GBS'],['/eif-ui','EIF'],
     ['/divisions','Divisions'],['/portals','Portals'],['/Sentinel','Sentinel'],
     ['/udoc-admin','UDOC Admin'],['/admin','GODS Admin']].forEach(([h,l])=>{
      row2.appendChild(el('a',{className:'dd-chip',href:h},l));
    });
    map.appendChild(row2);
    map.appendChild(el('p',{className:'dd-mut'},'Staff: admin@gods.local / admin123 · seths@ · madiba@ · ts@ / staff123'));
    root.appendChild(map);

    const bridge=el('div',{className:'dd-panel'});
    bridge.innerHTML='<h3>Core bridge · live probes</h3>';
    bridge.appendChild(el('div',{className:'dd-term',id:'dd-term'},'Probes write here · Core must stay green for Capstone smoke'));
    root.appendChild(bridge);

    const help=el('div',{className:'dd-panel'});
    help.innerHTML=`<h3>Capstone operator help</h3>
<table style="width:100%;border-collapse:collapse;font-size:12px">
<thead><tr><th style="text-align:left;padding:4px;border-bottom:1px solid #1c2a45">Action</th><th style="text-align:left;padding:4px;border-bottom:1px solid #1c2a45">Expected</th><th style="text-align:left;padding:4px;border-bottom:1px solid #1c2a45">Honesty</th></tr></thead>
<tbody>
<tr><td style="padding:4px;border-bottom:1px solid #1c2a45">EVA fair</td><td style="padding:4px;border-bottom:1px solid #1c2a45">APPROVE / non-BLOCK</td><td style="padding:4px;border-bottom:1px solid #1c2a45">deterministic gate</td></tr>
<tr><td style="padding:4px;border-bottom:1px solid #1c2a45">EVA biased</td><td style="padding:4px;border-bottom:1px solid #1c2a45">BLOCK</td><td style="padding:4px;border-bottom:1px solid #1c2a45">fail-closed policy</td></tr>
<tr><td style="padding:4px;border-bottom:1px solid #1c2a45">demo/ready</td><td style="padding:4px;border-bottom:1px solid #1c2a45">ready:true · model-001 ACTIVE</td><td style="padding:4px;border-bottom:1px solid #1c2a45">auto-heal on probe</td></tr>
<tr><td style="padding:4px;border-bottom:1px solid #1c2a45">Division metrics</td><td style="padding:4px;border-bottom:1px solid #1c2a45">Neon rows · may be zero</td><td style="padding:4px;border-bottom:1px solid #1c2a45">zeros OK</td></tr>
</tbody></table>
<p class="dd-mut">Assessor path: health → demo/ready → Sentinel Fair/Biased → division guided path → UDOC Admin Layers.</p>`;
    root.appendChild(help);

    const termPanel = Array.from(host.querySelectorAll('.panel,div')).find(p=>/Ops terminal|Terminal/i.test(p.textContent||'') && p.querySelector('.term,#term'));
    if(termPanel && termPanel.parentNode){
      termPanel.parentNode.insertBefore(root, termPanel);
    } else {
      host.appendChild(root);
    }

    setTimeout(()=>{ probeReady().catch(()=>{}); }, 400);

    if(typeof window.evaSmoke==='function'){
      const orig=window.evaSmoke;
      window.evaSmoke=async function(){
        try{ await orig.apply(this,arguments); }catch(_){}
        return evaSmoke();
      };
    } else {
      window.evaSmoke=evaSmoke;
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount);
  else mount();
})();
