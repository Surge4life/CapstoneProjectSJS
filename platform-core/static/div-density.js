/*! div-density.js — expanded UDOC-admin parity for operator surfaces
 * Inject only. Does not replace login, guided path, or division APIs.
 */
(function(){
  if(window.__DIV_DENSITY__) return; window.__DIV_DENSITY__=1;
  const API = (typeof window.API==='string' && window.API) ? window.API : location.origin;
  const PATH = (location.pathname||'/').replace(/\/$/,'') || '/';

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
.dd-term{font-family:ui-monospace,monospace;font-size:11px;background:#050b16;border:1px solid var(--line,#1c2a45);border-radius:8px;padding:8px;white-space:pre-wrap;max-height:160px;overflow:auto;margin-top:8px}
.dd-mut{color:var(--mut,#8fa0bd);font-size:11px;margin:8px 0 0}
.dd-assessor{border-color:rgba(0,194,212,.35);background:rgba(0,194,212,.06)}
.dd-table{width:100%;border-collapse:collapse;font-size:12px;margin-top:8px}
.dd-table th,.dd-table td{text-align:left;padding:5px 6px;border-bottom:1px solid var(--line,#1c2a45)}
.dd-table th{color:var(--mut,#8fa0bd);font-size:10px;text-transform:uppercase}
`;
    document.head.appendChild(s);
  }

  function logTerm(msg){
    const term=document.getElementById('dd-term')||document.getElementById('term')||document.getElementById('bridge-term');
    if(term) term.textContent=new Date().toLocaleTimeString()+' '+msg+'\n'+(term.textContent||'').slice(0,2000);
  }

  async function evaSmoke(){
    try{
      const r=await fetch(API+'/decisions/batch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenarios:['fair','biased']})});
      const j=await r.json();
      const o=j.outcomes||{};
      const gate=(Number(o.BLOCK||0)>=1)?'PASS':'CHECK';
      ['k-eva','k-eva2','dd-eva'].forEach(id=>{ const n=document.getElementById(id); if(n) n.textContent=gate+' · B'+(o.BLOCK||0)+'/A'+(o.APPROVE||0); });
      logTerm('EVA '+gate+' '+JSON.stringify(o));
      return j;
    }catch(e){ logTerm('EVA FAIL '+e.message); }
  }

  async function probeReady(){
    try{
      const r=await fetch(API+'/udoc/demo/ready');
      const j=await r.json();
      const n=document.getElementById('dd-ready')||document.getElementById('ready-tag');
      if(n) n.textContent=j.ready?'DEMO READY':'NOT READY';
      logTerm('READY '+JSON.stringify({ready:j.ready,model:j.model_001&&j.model_001.status,rules:j.active_rules}));
      return j;
    }catch(e){ const n=document.getElementById('dd-ready'); if(n) n.textContent='probe fail'; logTerm('READY FAIL '+e.message); }
  }

  async function probeHealth(){
    try{
      const r=await fetch(API+'/health'); const j=await r.json();
      logTerm('HEALTH '+JSON.stringify(j));
    }catch(e){ logTerm('HEALTH FAIL '+e.message); }
  }

  async function probePillars(){
    try{
      let j=null, used='';
      for(const p of ['/gis/gbs/pillars','/gis/gbs/overview','/gis/gbs/architecture']){
        try{ const r=await fetch(API+p); if(r.ok){ j=await r.json(); used=p; break; } }catch(_){}
      }
      logTerm(j?('PILLARS '+used+' '+JSON.stringify(j).slice(0,600)):'PILLARS no route');
      const el=document.getElementById('dd-pillars-out');
      if(el && j) el.textContent=JSON.stringify(j,null,2).slice(0,1800);
    }catch(e){ logTerm('PILLARS FAIL '+e.message); }
  }

  async function probeDivMetrics(){
    try{
      const [s,t,m]=await Promise.all([
        fetch(API+'/seths/metrics').then(r=>r.ok?r.json():{}).catch(()=>({})),
        fetch(API+'/ts/metrics').then(r=>r.ok?r.json():{}).catch(()=>({})),
        fetch(API+'/madiba/metrics').then(r=>r.ok?r.json():{}).catch(()=>({})),
      ]);
      const el=document.getElementById('dd-div-kpis');
      if(el){
        el.innerHTML='<table class="dd-table"><thead><tr><th>Division</th><th>KPI</th><th>Value</th><th>Honesty</th></tr></thead><tbody>'+
          '<tr><td><b>SETHS</b></td><td>total / placed</td><td>'+(s.total??'—')+' / '+(s.placed??'—')+'</td><td class="dd-mut">demo learners</td></tr>'+
          '<tr><td><b>TS</b></td><td>projects / workers</td><td>'+(t.projects??'—')+' / '+(t.workers_absorbed??'—')+'</td><td class="dd-mut">capital not_deployed</td></tr>'+
          '<tr><td><b>MADIBA</b></td><td>cycles / recycled</td><td>'+(m.cycles??'—')+' / '+(m.cumulative_recycled??'—')+'</td><td class="dd-mut">ledger ≠ AUM</td></tr>'+
          '</tbody></table>';
      }
      logTerm('DIV KPIs seths.placed='+(s.placed??0)+' ts='+(t.projects??0)+' madiba='+(m.cycles??0));
    }catch(e){ logTerm('DIV KPIs FAIL '+e.message); }
  }

  function surfaceTruth(){
    const map={
      '/seths':{title:'SETHS truth',chips:['placement_rate = live Neon','not funded programme','PLACED → TS assign FK','demo learners OK'],loop:'Enrol → Advance → PLACED → open TS → Assign → MADIBA'},
      '/ts':{title:'TS truth',chips:['SPVs = Neon rows','equity 20–60% structure','capital not_deployed','assign requires PLACED'],loop:'Ensure PLACED on SETHS → Deploy SPV → Assign worker → MADIBA'},
      '/madiba':{title:'MADIBA truth',chips:['ledger only · not AUM','capital not_deployed','recycle ratio = ledger math','EIF parallel audit'],loop:'Allocate cycle → Engage → Advance → EIF nominate'},
      '/gbs':{title:'GBS freeze truth',chips:['pillars + /gis/gbs/* live','nodes may be empty','Sovereign-Verified = designed_not_built','four-division symmetry'],loop:'Load overview → Nodes → Division KPIs → EVA'},
      '/eif-ui':{title:'EIF truth',chips:['nominate = audit-only','no Diamond grant free tier','parallel Sovereign-Verified','madiba@ / staff123'],loop:'Load framework → Fill demo → Nominate audit → MADIBA'},
      '/portals':{title:'Portals truth',chips:['Core-routed controls','CITIZEN → /citizen/challenge','OversightCase on Neon','not 24 Render services'],loop:'Open CITIZEN/REGULATOR → Run control → EVA'},
      '/divisions':{title:'Divisions cockpit',chips:['SETHS→TS→MADIBA loop','zeros OK','MADIBA ≠ AUM','FK-backed assign'],loop:'Run full loop → EVA → GBS probes'},
      '/Sentinel':{title:'Sentinel truth',chips:['EVA command surface','fair≠BLOCK biased=BLOCK','model-001 auto-heal','not commercial scale'],loop:'Demo ready → Fair → Biased → Full smoke'},
    };
    return map[PATH]||map['/divisions'];
  }

  function mount(){
    ensureStyle();
    const host = document.getElementById('ops') || document.querySelector('main') || document.querySelector('.wrap') || document.body;
    if(!host || document.getElementById('dd-root')) return;
    const root=el('div',{id:'dd-root'});
    const truth=surfaceTruth();

    const assessor=el('div',{className:'dd-panel dd-assessor'});
    assessor.innerHTML='<h3>Assessor strip · '+PATH+'</h3>';
    const row1=el('div',{className:'dd-row'});
    [['EVA fair/biased',evaSmoke],['demo/ready',probeReady],['/health',probeHealth],['Division KPIs',probeDivMetrics],['GBS pillars',probePillars]].forEach(([label,fn])=>{
      const b=el('button',{type:'button',className:'dd-chip'},label); b.onclick=fn; row1.appendChild(b);
    });
    ['/Sentinel','/udoc-admin','/admin','/divisions','/portals'].forEach(href=>{
      row1.appendChild(el('a',{className:'dd-chip',href:href},href.replace('/','')+' →'));
    });
    assessor.appendChild(row1);
    const kpis=el('div',{className:'dd-grid'});
    kpis.innerHTML='<div class="dd-card"><h4>EVA gate</h4><div class="dd-metric" id="dd-eva">run chip</div></div><div class="dd-card"><h4>Ready</h4><div class="dd-metric" id="dd-ready">—</div></div><div class="dd-card"><h4>Honesty</h4><div class="dd-metric" style="font-size:0.85rem">capital not_deployed</div></div><div class="dd-card"><h4>Surface</h4><div class="dd-metric" style="font-size:0.9rem">'+PATH+'</div></div>';
    assessor.appendChild(kpis);
    assessor.appendChild(el('p',{className:'dd-mut'},'Capstone: zeros OK · MADIBA ≠ AUM · Sovereign-Verified = designed_not_built · biased must BLOCK'));
    root.appendChild(assessor);

    const truthP=el('div',{className:'dd-panel'});
    truthP.innerHTML='<h3>'+truth.title+'</h3>';
    const chips=el('div',{className:'dd-row'});
    truth.chips.forEach(c=>chips.appendChild(el('span',{className:'dd-chip'},c)));
    truthP.appendChild(chips);
    truthP.appendChild(el('p',{className:'dd-mut'},'Operator loop: '+truth.loop));
    root.appendChild(truthP);

    const mapEl=el('div',{className:'dd-panel'});
    mapEl.innerHTML='<h3>Surface map · operator</h3>';
    const row2=el('div',{className:'dd-row'});
    [['/seths','SETHS'],['/ts','TS'],['/madiba','MADIBA'],['/gbs','GBS'],['/eif-ui','EIF'],['/divisions','Divisions'],['/portals','Portals'],['/Sentinel','Sentinel'],['/udoc-admin','UDOC Admin'],['/admin','GODS Admin']].forEach(([h,l])=>row2.appendChild(el('a',{className:'dd-chip',href:h},l)));
    mapEl.appendChild(row2);
    mapEl.appendChild(el('p',{className:'dd-mut'},'Staff: admin@gods.local / admin123 · seths@ · madiba@ · ts@ / staff123'));
    root.appendChild(mapEl);

    const divk=el('div',{className:'dd-panel'});
    divk.innerHTML='<h3>Four-division KPIs · live probe</h3><div id="dd-div-kpis" class="dd-mut">Click Division KPIs or wait…</div>';
    root.appendChild(divk);

    const pill=el('div',{className:'dd-panel'});
    pill.innerHTML='<h3>GBS / GIS probe output</h3><div class="dd-term" id="dd-pillars-out">Run GBS pillars chip</div>';
    root.appendChild(pill);

    const bridge=el('div',{className:'dd-panel'});
    bridge.innerHTML='<h3>Core bridge · live probes</h3>';
    bridge.appendChild(el('div',{className:'dd-term',id:'dd-term'},'Probes write here · Core must stay green for Capstone smoke'));
    root.appendChild(bridge);

    const help=el('div',{className:'dd-panel'});
    help.innerHTML='<h3>Capstone operator help</h3><table class="dd-table"><thead><tr><th>Action</th><th>Expected</th><th>Honesty</th></tr></thead><tbody><tr><td>EVA fair</td><td>APPROVE / non-BLOCK</td><td>deterministic gate</td></tr><tr><td>EVA biased</td><td>BLOCK</td><td>fail-closed policy</td></tr><tr><td>demo/ready</td><td>ready:true · model-001 ACTIVE</td><td>auto-heal on probe</td></tr><tr><td>Division metrics</td><td>Neon rows · may be zero</td><td>zeros OK</td></tr><tr><td>MADIBA allocate</td><td>CapitalCycle ledger write</td><td>not AUM · not cash</td></tr><tr><td>EIF nominate</td><td>sealed audit only</td><td>no funding on free tier</td></tr><tr><td>GBS nodes</td><td>list may be empty</td><td>designed_not_built OK</td></tr></tbody></table><p class="dd-mut">Assessor path: health → demo/ready → Sentinel Fair/Biased → division guided path → UDOC Admin Layers.</p>';
    root.appendChild(help);

    const cred=el('div',{className:'dd-panel'});
    cred.innerHTML='<h3>Staff credentials · Capstone</h3><div class="dd-row"><span class="dd-chip">admin@gods.local / admin123</span><span class="dd-chip">seths@gods.local / staff123</span><span class="dd-chip">madiba@gods.local / staff123</span><span class="dd-chip">ts@gods.local / staff123</span></div><p class="dd-mut">No new user registration on Neon free tier · staff seed only</p>';
    root.appendChild(cred);

    const termPanel = Array.from(host.querySelectorAll('.panel,div')).find(p=>/Ops terminal|Terminal/i.test(p.textContent||'') && p.querySelector('.term,#term'));
    if(termPanel && termPanel.parentNode) termPanel.parentNode.insertBefore(root, termPanel);
    else host.appendChild(root);

    setTimeout(function(){ probeReady().catch(function(){}); probeDivMetrics().catch(function(){}); }, 500);

    if(typeof window.evaSmoke==='function'){
      const orig=window.evaSmoke;
      window.evaSmoke=async function(){ try{ await orig.apply(this,arguments);}catch(_){} return evaSmoke(); };
    } else window.evaSmoke=evaSmoke;
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount);
  else mount();
})();
