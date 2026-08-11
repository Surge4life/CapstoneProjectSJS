/* GODS Admin live density — divisions + SETHS→TS→MADIBA loop actions */
(function(){
  if(window.__GODS_ADMIN_DENSITY__) return;
  window.__GODS_ADMIN_DENSITY__=true;
  const API = (localStorage.getItem('gods_api_url')) || location.origin;
  function tok(){ return sessionStorage.getItem('gods_api_tok')||''; }
  async function req(path, opts){
    const h=Object.assign({'Content-Type':'application/json'}, (opts&&opts.headers)||{});
    const t=tok(); if(t) h.Authorization='Bearer '+t;
    const r=await fetch(String(API).replace(/\/$/,'')+path, Object.assign({}, opts||{}, {headers:h}));
    if(!r.ok){
      let det=''; try{ det=await r.text(); }catch(_){}
      throw new Error(path+' '+r.status+(det?(' '+det.slice(0,140)):''));
    }
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
      '</div><div id="'+panelId+'-body">…</div><div id="'+panelId+'-term" style="margin-top:8px;font-family:ui-monospace,monospace;font-size:11px;color:#7A7A8A;min-height:14px;white-space:pre-wrap"></div>';
    const hdr=page.querySelector('.pg-hdr');
    if(hdr && hdr.nextSibling) page.insertBefore(el, hdr.nextSibling);
    else page.appendChild(el);
    return el;
  }
  function setBody(id, html){ const b=document.getElementById(id+'-body'); if(b) b.innerHTML=html; }
  function term(id, msg, ok){
    const t=document.getElementById(id+'-term');
    if(t){ t.textContent=msg; t.style.color=ok===false?'#E85D5D':(ok?'#2D9B5A':'#7A7A8A'); }
  }
  function kpiGrid(items){
    return '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px">'+
      items.map(([l,v,c])=>'<div style="background:#060E1C;border:1px solid #1A3050;border-radius:8px;padding:10px">'+
        '<div style="color:#7A7A8A;font-size:10px;text-transform:uppercase;letter-spacing:.06em">'+esc(l)+'</div>'+
        '<div style="font-size:1.25rem;font-weight:700;color:'+(c||'#F5F0E8')+'">'+esc(v)+'</div></div>').join('')+
      '</div>';
  }
  function btn(label, id, ghost){
    const st=ghost
      ?'margin:4px 4px 0 0;padding:6px 10px;background:transparent;color:#D4CEBC;border:1px solid #243A5A;border-radius:6px;font-size:11px;cursor:pointer'
      :'margin:4px 4px 0 0;padding:6px 10px;background:#C9A84C;color:#060E1C;border:0;border-radius:6px;font-weight:700;font-size:11px;cursor:pointer';
    return '<button type="button" id="'+id+'" style="'+st+'">'+esc(label)+'</button>';
  }
  function navStrip(){
    if(document.getElementById('gods-div-nav')) return;
    const bar=document.createElement('div');
    bar.id='gods-div-nav';
    bar.style.cssText='position:fixed;left:12px;bottom:16px;z-index:99999;display:flex;flex-wrap:wrap;gap:6px;max-width:52vw';
    const links=[['/udoc-admin','UDOC Admin'],['/Sentinel','Sentinel'],['/gbs','GBS'],['/seths','SETHS'],['/ts','TS'],['/madiba','MADIBA'],['/divisions','Divisions'],['/portals','Portals'],['/eif-ui','EIF']];
    bar.innerHTML=links.map(([h,l])=>'<a href="'+h+'" style="text-decoration:none;background:#0B1829;border:1px solid #243A5A;color:#00C2D4;padding:6px 10px;border-radius:8px;font:11px system-ui">'+l+'</a>').join('');
    document.body.appendChild(bar);
  }
  function globalPanels(){
    if(document.getElementById('gods-live-regulator')) return;
    const wrap=document.createElement('div'); wrap.id='gods-live-global'; document.body.appendChild(wrap);
    function panel(id,title){
      const el=document.createElement('div'); el.id=id;
      el.style.cssText='margin:12px 16px;padding:12px 14px;background:#0B1829;border:1px solid #243A5A;border-radius:10px;color:#D4CEBC;font:12px/1.45 system-ui,sans-serif';
      el.innerHTML='<div style="color:#C9A84C;font-weight:700;margin-bottom:8px">'+esc(title)+'</div><div id="'+id+'-body">…</div><div id="'+id+'-term" style="margin-top:6px;font:11px ui-monospace,monospace;color:#7A7A8A"></div>';
      wrap.appendChild(el);
    }
    panel('gods-live-regulator','Regulator summary · LIVE');
    panel('gods-live-pillars','Constitutional pillars · LIVE');
    panel('gods-live-gbs','GBS freeze · LIVE');
    panel('gods-live-divisions','Division operators · LIVE · SETHS→TS→MADIBA');
  }
  function once(id, fn){
    const el=document.getElementById(id);
    if(el && !el.__wired){ el.__wired=true; el.addEventListener('click', fn); }
  }

  async function densify(){
    if(!tok()) return;
    navStrip(); globalPanels();
    try{
      const [reg, pillars, gbs, arch, ready, status, sm, tm, mm, projects, learners, pipeline]=await Promise.all([
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
        req('/seths/learners').catch(()=>({learners:[]})),
        req('/madiba/engage/pipeline').catch(()=>({list:[]})),
      ]);
      const L=Array.isArray(learners.learners)?learners.learners:(Array.isArray(learners)?learners:[]);
      const rows=Array.isArray(projects)?projects:[];
      window.__GODS_DIV_STATE__={learners:L, projects:rows, sm, tm, mm};

      if(reg.error) setBody('gods-live-regulator','<span style="color:#E8A13A">'+esc(reg.error)+'</span>');
      else {
        const by=reg.by_outcome||{};
        setBody('gods-live-regulator', kpiGrid([
          ['Decisions', reg.decisions??'—'],['APPROVE', by.APPROVE??0, '#2D9B5A'],
          ['BLOCK', by.BLOCK??0, '#E85D5D'],['Open oversight', reg.open_oversight??0, '#E8A13A'],
        ]));
      }
      const plist=pillars.pillars||pillars.constitutional_pillars||[];
      if(!pillars.error) setBody('gods-live-pillars', plist.map(p=>{
        return '<span style="display:inline-block;margin:3px;padding:3px 8px;border:1px solid #243A5A;border-radius:12px;font-size:11px">'+esc(p.id||p.numeral||'')+' · '+esc(p.name||'')+' <span style="color:#2D9B5A">'+esc(p.status||'operational')+'</span></span>';
      }).join(' ')||'—');

      const honesty=(gbs.honesty&&gbs.honesty.note)||'';
      const divs=(arch.divisions||[]).map(d=>esc(d.division||'')+' <span style="color:#7A7A8A">('+(d.mode||'')+')</span>').join(' · ');
      setBody('gods-live-gbs','<div>Demo ready: <b>'+esc(String(ready.ready))+'</b> · models '+(status.models??'—')+' · learners '+(status.learners??'—')+' · TS '+(status.ts_projects??'—')+'</div>'+
        '<div style="margin-top:6px">'+ (divs||'SETHS · MADIBA · TS · UDOC') +'</div>'+
        '<div style="margin-top:6px;color:#E8A13A;font-size:11px">'+esc(honesty||'capital not_deployed')+'</div>');

      setBody('gods-live-divisions', kpiGrid([
        ['SETHS total', sm.total??'—', '#00C2D4'],['SETHS placed', sm.placed??'—', '#00C2D4'],
        ['TS projects', tm.projects??'—', '#10B981'],['TS workers', tm.workers_absorbed??'—', '#10B981'],
        ['MADIBA cycles', mm.cycles??'—', '#C9A84C'],['MADIBA recycled', fmt(mm.cumulative_recycled), '#C9A84C'],
      ]) + '<div style="margin-top:10px">'+btn('Run SETHS→TS→MADIBA loop','btn-run-loop')+btn('Refresh all','btn-refresh-all', true)+'</div>'+
        '<p style="color:#7A7A8A;font-size:11px;margin:8px 0 0">Loop: enrol → advance to PLACED → assign-worker on SPV → allocate cycle · capital not_deployed</p>');

      ensureIn('page-seths-dash','live-seths-metrics','SETHS live metrics · Core API','/seths');
      setBody('live-seths-metrics', kpiGrid([
        ['Learners', sm.total??0],['Placed', sm.placed??0, '#2D9B5A'],['Completed', sm.completed??0],
        ['Placement rate', sm.placement_rate!=null?Math.round(sm.placement_rate*100)+'%':'—'],
        ['Monthly output', fmt(sm.monthly_economic_output)],
      ]) + '<div style="margin-top:8px">'+btn('Enrol demo','btn-seths-enrol')+btn('Advance next','btn-seths-advance')+btn('Refresh','btn-seths-refresh',true)+'</div>');

      ensureIn('page-seths-intake','live-seths-learners','SETHS learner roster · LIVE','/seths');
      setBody('live-seths-learners',
        (L.length?('<table style="width:100%;border-collapse:collapse;font-size:11px"><thead><tr style="color:#7A7A8A;text-align:left"><th>Ref</th><th>Status</th><th>Stream</th><th>NQF</th><th>Value</th></tr></thead><tbody>'+
          L.slice(0,25).map(x=>'<tr style="border-top:1px solid #1A3050"><td class="mono">'+esc(x.ref)+'</td><td>'+esc(x.status)+'</td><td>'+esc(x.stream)+'</td><td>'+esc(x.nqf_level)+'</td><td>'+esc(x.monthly_value)+'</td></tr>').join('')+
          '</tbody></table>'):'<span style="color:#7A7A8A">No learners</span>')+
        '<div style="margin-top:8px">'+btn('Enrol demo','btn-seths-enrol-2')+btn('Advance next','btn-seths-advance-2')+'</div>');

      ensureIn('page-madiba-dash','live-madiba-metrics','MADIBA live ledger · Core API','/madiba');
      setBody('live-madiba-metrics', kpiGrid([
        ['Cycles', mm.cycles??0],['Total inflow', fmt(mm.total_inflow)],
        ['Recycled → SETHS', fmt(mm.cumulative_recycled), '#C9A84C'],
        ['Recycle ratio', mm.recycle_ratio!=null?Number(mm.recycle_ratio).toFixed(2):'—'],
      ]) + '<div style="margin-top:8px">'+btn('Allocate demo cycle','btn-madiba-alloc')+btn('New engagement','btn-madiba-engage')+'</div>'+
        '<p style="color:#E8A13A;margin:8px 0 0;font-size:11px">Demonstration ledger only · capital not_deployed</p>');

      ensureIn('page-madiba-impact','live-madiba-pipeline','MADIBA engage pipeline · LIVE','/madiba');
      const eng=pipeline.list||[];
      setBody('live-madiba-pipeline', kpiGrid([
        ['Engagements', pipeline.engagements??eng.length],
        ['Indicated', fmt(pipeline.indicated_total)],
        ['Committed', fmt(pipeline.committed_total), '#C9A84C'],
      ]) + (eng.length?('<table style="width:100%;border-collapse:collapse;font-size:11px;margin-top:8px"><thead><tr style="color:#7A7A8A;text-align:left"><th>Ref</th><th>Investor</th><th>Stage</th><th>Type</th></tr></thead><tbody>'+
        eng.slice(0,15).map(x=>'<tr style="border-top:1px solid #1A3050"><td>'+esc(x.ref)+'</td><td>'+esc(x.investor)+'</td><td>'+esc(x.stage||x.state)+'</td><td>'+esc(x.type)+'</td></tr>').join('')+'</tbody></table>'):''));

      ensureIn('page-ts-dash','live-ts-metrics','TS Industries live · Core API','/ts');
      const by=tm.by_subsidiary||{};
      const sub=Object.keys(by).map(k=>esc(k)+': '+(by[k].projects||0)+'p/'+(by[k].workers||0)+'w').join(' · ');
      setBody('live-ts-metrics', kpiGrid([
        ['Projects / SPVs', tm.projects??0, '#10B981'],
        ['Workers absorbed', tm.workers_absorbed??0],
        ['Monthly profit', fmt(tm.monthly_operating_profit)],
      ]) + (sub?'<div style="margin-top:8px;color:#7A7A8A;font-size:11px">'+sub+'</div>':'')+
        '<div style="margin-top:8px">'+btn('Deploy demo SPV','btn-ts-deploy')+btn('Assign PLACED→SPV','btn-ts-assign')+'</div>');

      ensureIn('page-ts-projects','live-ts-projects','TS SPV list · LIVE','/ts');
      setBody('live-ts-projects', rows.length
        ? ('<table style="width:100%;border-collapse:collapse;font-size:11px"><thead><tr style="color:#7A7A8A;text-align:left"><th>SPV</th><th>Sector</th><th>Sub</th><th>Equity</th><th>Workers</th><th>Revenue</th></tr></thead><tbody>'+
          rows.slice(0,20).map(p=>'<tr style="border-top:1px solid #1A3050"><td class="mono">'+esc(p.spv_id)+'</td><td>'+esc(p.sector)+'</td><td>'+esc(p.subsidiary)+'</td><td>'+esc(p.equity_pct)+'</td><td>'+esc(p.workers)+'</td><td>'+esc(p.monthly_revenue)+'</td></tr>').join('')+
          '</tbody></table>')
        : '<span style="color:#7A7A8A">No SPVs</span>')+
        '<div style="margin-top:8px">'+btn('Deploy demo SPV','btn-ts-deploy-2')+btn('Assign PLACED→SPV','btn-ts-assign-2')+'</div>');

      ensureIn('page-spv','live-spv-panel','SPV live · TS projects','/ts');
      setBody('live-spv-panel', kpiGrid([['SPV count', rows.length, '#10B981'],['Workers', tm.workers_absorbed??0]])+
        '<p style="color:#7A7A8A;font-size:11px;margin-top:8px">capital not_deployed · equity structure documented</p>');

      ensureIn('page-placements','live-placements','SETHS → TS placement path · LIVE','/divisions');
      setBody('live-placements', kpiGrid([
        ['SETHS placed', sm.placed??0, '#00C2D4'],
        ['TS absorbed', tm.workers_absorbed??0, '#10B981'],
        ['Loop', (sm.placed&&tm.workers_absorbed)?'wired':'seed'],
      ]) + '<div style="margin-top:8px">'+btn('Assign PLACED→SPV','btn-ts-assign-3')+btn('Run full loop','btn-run-loop-2')+'</div>'+
        '<p style="color:#7A7A8A;margin:8px 0 0;font-size:11px">Requires Learner status=PLACED · FK-backed assign-worker</p>');

      async function enrol(panel){
        term(panel,'Enrolling…');
        const r=await req('/seths/enrol',{method:'POST',body:JSON.stringify({qualification:'Digital Operations & AI Literacy',count:1})});
        term(panel,'Enrolled '+(r.ref||(r.learners&&r.learners[0]&&r.learners[0].ref)||JSON.stringify(r).slice(0,80)), true);
      }
      async function advance(panel){
        const st=window.__GODS_DIV_STATE__||{};
        const cand=(st.learners||[]).find(x=>String(x.status).toUpperCase()!=='PLACED') || (st.learners||[])[0];
        if(!cand){ term(panel,'No learner to advance — enrol first', false); return; }
        term(panel,'Advancing '+cand.ref+'…');
        const r=await req('/seths/'+encodeURIComponent(cand.ref)+'/advance?monthly_value=12000',{method:'POST'});
        term(panel,'Advanced '+cand.ref+' → '+(r.status||JSON.stringify(r).slice(0,80)), true);
      }
      async function deploy(panel){
        term(panel,'Deploying demo SPV…');
        const r=await req('/ts/projects',{method:'POST',body:JSON.stringify({sector:'ENERGY',subsidiary:'ENERGY',name:'Demo SPV',equity_pct:0.3})});
        term(panel,'Deployed '+(r.spv_id||JSON.stringify(r).slice(0,80)), true);
      }
      async function assign(panel){
        const st=window.__GODS_DIV_STATE__||{};
        const placed=(st.learners||[]).find(x=>String(x.status).toUpperCase()==='PLACED');
        const spv=(st.projects||[])[0];
        if(!placed){ term(panel,'No PLACED learner — enrol+advance first', false); return; }
        if(!spv){ term(panel,'No SPV — deploy first', false); return; }
        term(panel,'Assigning '+placed.ref+' → '+spv.spv_id+'…');
        const r=await req('/ts/projects/'+encodeURIComponent(spv.spv_id)+'/assign-worker',{
          method:'POST', body:JSON.stringify({learner_ref:placed.ref, role:'operator', monthly_wage:12000})
        });
        term(panel,'Assigned '+placed.ref+' → '+spv.spv_id+' '+(r.ok!==false?'ok':JSON.stringify(r).slice(0,80)), true);
      }
      async function allocate(panel){
        term(panel,'Allocating demo cycle…');
        const r=await req('/madiba/allocate',{method:'POST',body:JSON.stringify({month:8, total_inflow:50000})});
        term(panel,'Allocated · '+(r.cycle||r.id||JSON.stringify(r).slice(0,100)), true);
      }
      async function engage(panel){
        term(panel,'Creating engagement…');
        const r=await req('/madiba/engage',{method:'POST',body:JSON.stringify({investor_name:'GODS Admin Demo Fund', investor_type:'INSTITUTIONAL', instrument:'blended'})});
        term(panel,'Engage '+(r.ref||JSON.stringify(r).slice(0,80)), true);
      }
      async function runLoop(panel){
        try{
          term(panel,'1/4 enrol…'); await enrol(panel); await densify();
          term(panel,'2/4 advance…'); await advance(panel); await densify();
          const st=window.__GODS_DIV_STATE__||{};
          if(!(st.projects||[]).length){ term(panel,'3/4 deploy SPV…'); await deploy(panel); await densify(); }
          term(panel,'3/4 assign…'); await assign(panel); await densify();
          term(panel,'4/4 allocate…'); await allocate(panel); await densify();
          term(panel,'Loop complete · SETHS→TS→MADIBA (demo ledger)', true);
        }catch(e){ term(panel, String(e.message||e), false); }
      }

      const wrap=async(panel,fn)=>{ try{ await fn(panel); await densify(); }catch(e){ term(panel, String(e.message||e), false); } };
      once('btn-seths-enrol', ()=>wrap('live-seths-metrics', enrol));
      once('btn-seths-enrol-2', ()=>wrap('live-seths-learners', enrol));
      once('btn-seths-advance', ()=>wrap('live-seths-metrics', advance));
      once('btn-seths-advance-2', ()=>wrap('live-seths-learners', advance));
      once('btn-seths-refresh', densify);
      once('btn-madiba-alloc', ()=>wrap('live-madiba-metrics', allocate));
      once('btn-madiba-engage', ()=>wrap('live-madiba-metrics', engage));
      once('btn-ts-deploy', ()=>wrap('live-ts-metrics', deploy));
      once('btn-ts-deploy-2', ()=>wrap('live-ts-projects', deploy));
      once('btn-ts-assign', ()=>wrap('live-ts-metrics', assign));
      once('btn-ts-assign-2', ()=>wrap('live-ts-projects', assign));
      once('btn-ts-assign-3', ()=>wrap('live-placements', assign));
      once('btn-run-loop', ()=>runLoop('gods-live-divisions'));
      once('btn-run-loop-2', ()=>runLoop('live-placements'));
      once('btn-refresh-all', densify);

      const m=document.getElementById('gl-msg');
      if(m){ m.textContent='● GODS densify · loop actions bound'; m.style.color='#2D9B5A'; }
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
  setInterval(()=>{ if(tok()) densify(); }, 20000);
})();
