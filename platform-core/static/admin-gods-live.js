/* GODS Admin live density — divisions + constitutional + GBS (additive) */
(function(){
  if(window.__GODS_ADMIN_DENSITY__) return;
  window.__GODS_ADMIN_DENSITY__=true;
  const API = (localStorage.getItem('gods_api_url')) || location.origin;
  function tok(){ return sessionStorage.getItem('gods_api_tok')||''; }
  async function req(path, opts){
    const h=Object.assign({'Content-Type':'application/json'}, (opts&&opts.headers)||{});
    const t=tok(); if(t) h.Authorization='Bearer '+t;
    const r=await fetch(String(API).replace(/\/$/,'')+path, Object.assign({}, opts||{}, {headers:h}));
    if(!r.ok) throw new Error(path+' '+r.status);
    const ct=r.headers.get('content-type')||'';
    return ct.includes('json')? r.json(): r.text();
  }
  function esc(s){ const d=document.createElement('div'); d.textContent=String(s??''); return d.innerHTML; }
  function fmt(n){
    n=Number(n); if(!isFinite(n)) return '—';
    if(Math.abs(n)>=1e6) return 'R'+(n/1e6).toFixed(2)+'M';
    if(Math.abs(n)>=1e3) return 'R'+(n/1e3).toFixed(1)+'k';
    return String(n);
  }
  function ensureIn(pageId, panelId, title, opHref){
    const page=document.getElementById(pageId);
    if(!page) return null;
    let el=document.getElementById(panelId);
    if(el) return el;
    el=document.createElement('div');
    el.id=panelId;
    el.style.cssText='margin:12px 0;padding:12px 14px;background:#0B1829;border:1px solid #243A5A;border-radius:10px;color:#D4CEBC;font:12px/1.45 system-ui,sans-serif';
    el.innerHTML='<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px">'+
      '<div style="color:#C9A84C;font-weight:700;letter-spacing:.04em;flex:1">'+esc(title)+'</div>'+
      (opHref?('<a href="'+opHref+'" style="color:#00C2D4;text-decoration:none;font-size:11px;border:1px solid #243A5A;padding:4px 8px;border-radius:6px">Open operator →</a>'):'')+
      '</div><div id="'+panelId+'-body">…</div>';
    const hdr=page.querySelector('.pg-hdr');
    if(hdr && hdr.nextSibling) page.insertBefore(el, hdr.nextSibling);
    else page.appendChild(el);
    return el;
  }
  function setBody(id, html){
    const b=document.getElementById(id+'-body');
    if(b) b.innerHTML=html;
  }
  function kpiGrid(items){
    return '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px">'+
      items.map(([l,v,c])=>'<div style="background:#060E1C;border:1px solid #1A3050;border-radius:8px;padding:10px">'+
        '<div style="color:#7A7A8A;font-size:10px;text-transform:uppercase;letter-spacing:.06em">'+esc(l)+'</div>'+
        '<div style="font-size:1.25rem;font-weight:700;color:'+(c||'#F5F0E8')+'">'+esc(v)+'</div></div>').join('')+
      '</div>';
  }
  function navStrip(){
    if(document.getElementById('gods-div-nav')) return;
    const bar=document.createElement('div');
    bar.id='gods-div-nav';
    bar.style.cssText='position:fixed;left:12px;bottom:16px;z-index:99999;display:flex;flex-wrap:wrap;gap:6px;max-width:48vw';
    const links=[
      ['/udoc-admin','UDOC Admin'],['/Sentinel','Sentinel'],['/gbs','GBS'],
      ['/seths','SETHS'],['/ts','TS'],['/madiba','MADIBA'],
      ['/divisions','Divisions'],['/portals','Portals'],['/eif-ui','EIF'],
    ];
    bar.innerHTML=links.map(([h,l])=>'<a href="'+h+'" style="text-decoration:none;background:#0B1829;border:1px solid #243A5A;color:#00C2D4;padding:6px 10px;border-radius:8px;font:11px system-ui">'+l+'</a>').join('');
    document.body.appendChild(bar);
  }
  function globalPanels(){
    if(document.getElementById('gods-live-regulator')) return;
    const wrap=document.createElement('div');
    wrap.id='gods-live-global';
    wrap.style.cssText='position:relative;z-index:1';
    document.body.appendChild(wrap);
    function panel(id,title){
      const el=document.createElement('div');
      el.id=id;
      el.style.cssText='margin:12px 16px;padding:12px 14px;background:#0B1829;border:1px solid #243A5A;border-radius:10px;color:#D4CEBC;font:12px/1.45 system-ui,sans-serif';
      el.innerHTML='<div style="color:#C9A84C;font-weight:700;margin-bottom:8px">'+esc(title)+'</div><div id="'+id+'-body">…</div>';
      wrap.appendChild(el);
    }
    panel('gods-live-regulator','Regulator summary · LIVE');
    panel('gods-live-pillars','Constitutional pillars · LIVE');
    panel('gods-live-gbs','GBS freeze · LIVE');
    panel('gods-live-divisions','Division operators · LIVE');
  }

  async function densify(){
    if(!tok()) return;
    navStrip();
    globalPanels();
    try{
      const [reg, pillars, gbs, arch, ready, status, sm, tm, mm, projects]=await Promise.all([
        req('/udoc/regulator/summary').catch(e=>({error:String(e)})),
        req('/udoc/constitutional/pillars').catch(()=>req('/udoc/pillars').catch(e=>({error:String(e)}))),
        req('/gis/gbs/overview').catch(e=>({error:String(e)})),
        req('/gis/gbs/architecture').catch(e=>({error:String(e)})),
        req('/udoc/demo/ready').catch(()=>({})),
        req('/admin/status').catch(()=>({})),
        req('/seths/metrics').catch(e=>({error:String(e)})),
        req('/ts/metrics').catch(e=>({error:String(e)})),
        req('/madiba/metrics').catch(e=>({error:String(e)})),
        req('/ts/projects').catch(()=>[]),
      ]);

      if(reg.error) setBody('gods-live-regulator','<span style="color:#E8A13A">'+esc(reg.error)+'</span>');
      else {
        const by=reg.by_outcome||{};
        setBody('gods-live-regulator', kpiGrid([
          ['Decisions', reg.decisions??'—'],
          ['APPROVE', by.APPROVE??0, '#2D9B5A'],
          ['BLOCK', by.BLOCK??0, '#E85D5D'],
          ['Open oversight', reg.open_oversight??0, '#E8A13A'],
        ]));
      }

      const plist=pillars.pillars||pillars.constitutional_pillars||[];
      if(pillars.error) setBody('gods-live-pillars','<span style="color:#E8A13A">'+esc(pillars.error)+'</span>');
      else setBody('gods-live-pillars', plist.map(p=>{
        const name=p.name||p.title||'';
        const id=p.id||p.numeral||'';
        const st=p.status||'operational';
        return '<span style="display:inline-block;margin:3px;padding:3px 8px;border:1px solid #243A5A;border-radius:12px;font-size:11px">'+esc(id)+' · '+esc(name)+' <span style="color:#2D9B5A">'+esc(st)+'</span></span>';
      }).join(' ')||'—');

      const honesty=(gbs.honesty&&gbs.honesty.note)||'';
      const divs=(arch.divisions||[]).map(d=>esc(d.division||'')+' <span style="color:#7A7A8A">('+(d.mode||'')+')</span>').join(' · ');
      setBody('gods-live-gbs',
        '<div>Demo ready: <b>'+esc(String(ready.ready))+'</b> · models '+(status.models??'—')+' · learners '+(status.learners??'—')+' · TS projects '+(status.ts_projects??'—')+'</div>'+
        '<div style="margin-top:6px">Architecture: '+(divs||'SETHS · MADIBA · TS · UDOC')+'</div>'+
        '<div style="margin-top:6px;color:#E8A13A;font-size:11px">'+esc(honesty||'capital not_deployed · designed_not_built where noted')+'</div>');

      setBody('gods-live-divisions', kpiGrid([
        ['SETHS total', sm.total??'—', '#00C2D4'],
        ['SETHS placed', sm.placed??'—', '#00C2D4'],
        ['TS projects', tm.projects??'—', '#10B981'],
        ['TS workers', tm.workers_absorbed??'—', '#10B981'],
        ['MADIBA cycles', mm.cycles??'—', '#C9A84C'],
        ['MADIBA recycled', fmt(mm.cumulative_recycled), '#C9A84C'],
      ]) +
        '<div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:8px">'+
        '<a href="/seths" style="color:#00C2D4">SETHS operator</a> · '+
        '<a href="/ts" style="color:#10B981">TS operator</a> · '+
        '<a href="/madiba" style="color:#C9A84C">MADIBA operator</a> · '+
        '<a href="/divisions">All divisions</a> · '+
        '<a href="/gbs">GBS freeze</a></div>'+
        '<p style="color:#7A7A8A;font-size:11px;margin:8px 0 0">Honesty: MADIBA ledger ≠ AUM · capital not_deployed · staff seths@/madiba@/ts@ · staff123</p>');

      ensureIn('page-seths-dash','live-seths-metrics','SETHS live metrics · Core API','/seths');
      if(sm.error) setBody('live-seths-metrics','<span style="color:#E8A13A">'+esc(sm.error)+'</span>');
      else setBody('live-seths-metrics', kpiGrid([
        ['Learners', sm.total??0],
        ['Placed', sm.placed??0, '#2D9B5A'],
        ['Completed', sm.completed??0],
        ['Placement rate', sm.placement_rate!=null?Math.round(sm.placement_rate*100)+'%':'—'],
        ['Monthly output', fmt(sm.monthly_economic_output)],
      ]) + '<p style="color:#7A7A8A;margin:8px 0 0;font-size:11px">Source: GET /seths/metrics · enrol/advance on /seths or /divisions</p>');

      ensureIn('page-madiba-dash','live-madiba-metrics','MADIBA live ledger · Core API','/madiba');
      if(mm.error) setBody('live-madiba-metrics','<span style="color:#E8A13A">'+esc(mm.error)+'</span>');
      else setBody('live-madiba-metrics', kpiGrid([
        ['Cycles', mm.cycles??0],
        ['Total inflow', fmt(mm.total_inflow)],
        ['Recycled → SETHS', fmt(mm.cumulative_recycled), '#C9A84C'],
        ['Recycle ratio', mm.recycle_ratio!=null?Number(mm.recycle_ratio).toFixed(2):'—'],
      ]) + '<p style="color:#E8A13A;margin:8px 0 0;font-size:11px">Demonstration ledger only · capital not_deployed · allocate on /madiba</p>');

      ensureIn('page-ts-dash','live-ts-metrics','TS Industries live · Core API','/ts');
      if(tm.error) setBody('live-ts-metrics','<span style="color:#E8A13A">'+esc(tm.error)+'</span>');
      else {
        const by=tm.by_subsidiary||{};
        const sub=Object.keys(by).map(k=>esc(k)+': '+(by[k].projects||0)+' proj / '+(by[k].workers||0)+' w').join(' · ');
        setBody('live-ts-metrics', kpiGrid([
          ['Projects / SPVs', tm.projects??0, '#10B981'],
          ['Workers absorbed', tm.workers_absorbed??0],
          ['Monthly profit', fmt(tm.monthly_operating_profit)],
        ]) + (sub?'<div style="margin-top:8px;color:#7A7A8A;font-size:11px">By subsidiary: '+sub+'</div>':'') +
          '<p style="color:#7A7A8A;margin:8px 0 0;font-size:11px">Source: GET /ts/metrics · deploy/assign on /ts</p>');
      }

      ensureIn('page-ts-projects','live-ts-projects','TS SPV list · LIVE','/ts');
      const rows=Array.isArray(projects)?projects:[];
      setBody('live-ts-projects', rows.length
        ? ('<table style="width:100%;border-collapse:collapse;font-size:11px"><thead><tr style="color:#7A7A8A;text-align:left"><th>SPV</th><th>Sector</th><th>Sub</th><th>Equity</th><th>Workers</th><th>Revenue</th></tr></thead><tbody>'+
          rows.slice(0,20).map(p=>'<tr style="border-top:1px solid #1A3050"><td class="mono">'+esc(p.spv_id)+'</td><td>'+esc(p.sector)+'</td><td>'+esc(p.subsidiary)+'</td><td>'+esc(p.equity_pct)+'</td><td>'+esc(p.workers)+'</td><td>'+esc(p.monthly_revenue)+'</td></tr>').join('')+
          '</tbody></table>')
        : '<span style="color:#7A7A8A">No SPVs yet · open /ts → Deploy demo SPV</span>');

      ensureIn('page-placements','live-placements','SETHS → TS placement path · LIVE','/divisions');
      setBody('live-placements', kpiGrid([
        ['SETHS placed', sm.placed??0, '#00C2D4'],
        ['TS absorbed', tm.workers_absorbed??0, '#10B981'],
        ['Loop note', (sm.placed&&tm.workers_absorbed)?'wired':'seed'],
      ]) + '<p style="color:#7A7A8A;margin:8px 0 0;font-size:11px">Operator path: /seths enrol→PLACED → /ts assign worker → /madiba recycle</p>');

      const m=document.getElementById('gl-msg');
      if(m){ m.textContent='● GODS densify · divisions + regulator + GBS bound'; m.style.color='#2D9B5A'; }
    }catch(e){
      const m=document.getElementById('gl-msg');
      if(m){ m.textContent='GODS densify: '+e.message; m.style.color='#E8A13A'; }
    }
  }
  function arm(){
    const btn=document.getElementById('gl-connect');
    const refresh=document.getElementById('gl-refresh');
    if(btn && !btn.__gods_d){ btn.__gods_d=true; btn.addEventListener('click',()=>setTimeout(densify,900)); }
    if(refresh && !refresh.__gods_d){ refresh.__gods_d=true; refresh.addEventListener('click',()=>setTimeout(densify,200)); }
    if(tok()) densify();
    const pass=document.getElementById('gl-pass');
    if(pass && !pass.value) pass.placeholder='admin123';
    const email=document.getElementById('gl-email');
    if(email && !email.value) email.value='admin@gods.local';
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(arm,300));
  else setTimeout(arm,300);
  setInterval(()=>{ if(tok()) densify(); }, 12000);
})();
