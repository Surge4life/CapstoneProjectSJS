/* GODS Admin live density — constitutional + GBS + division bind (additive) */
(function(){
  if(window.__GODS_ADMIN_DENSITY__) return;
  window.__GODS_ADMIN_DENSITY__=true;
  const API = (localStorage.getItem('gods_api_url')) || location.origin;
  function tok(){ return sessionStorage.getItem('gods_api_tok')||''; }
  async function req(path){
    const h={'Content-Type':'application/json'};
    const t=tok(); if(t) h.Authorization='Bearer '+t;
    const r=await fetch(String(API).replace(/\/$/,'')+path,{headers:h});
    if(!r.ok) throw new Error(path+' '+r.status);
    const ct=r.headers.get('content-type')||'';
    return ct.includes('json')? r.json(): r.text();
  }
  function esc(s){ const d=document.createElement('div'); d.textContent=String(s??''); return d.innerHTML; }
  function ensurePanel(id, title, parent){
    let el=document.getElementById(id);
    if(el) return el;
    el=document.createElement('div');
    el.id=id;
    el.style.cssText='margin:12px 16px;padding:12px 14px;background:#0B1829;border:1px solid #243A5A;border-radius:10px;color:#D4CEBC;font:12px/1.45 system-ui,sans-serif';
    el.innerHTML='<div style="color:#C9A84C;font-weight:700;margin-bottom:8px;letter-spacing:.04em">'+esc(title)+'</div><div id="'+id+'-body" class="mut">…</div>';
    (parent||document.body).appendChild(el);
    return el;
  }
  function setBody(id, html){
    const b=document.getElementById(id+'-body');
    if(b) b.innerHTML=html;
  }
  function navStrip(){
    if(document.getElementById('gods-div-nav')) return;
    const bar=document.createElement('div');
    bar.id='gods-div-nav';
    bar.style.cssText='position:fixed;left:12px;bottom:16px;z-index:99999;display:flex;flex-wrap:wrap;gap:6px;max-width:42vw';
    const links=[
      ['/udoc-admin','UDOC Admin'],
      ['/Sentinel','Sentinel'],
      ['/gbs','GBS Freeze'],
      ['/seths','SETHS'],
      ['/ts','TS'],
      ['/madiba','MADIBA'],
      ['/divisions','Divisions'],
      ['/portals','Portals'],
      ['/eif-ui','EIF'],
    ];
    bar.innerHTML=links.map(([h,l])=>'<a href="'+h+'" style="text-decoration:none;background:#0B1829;border:1px solid #243A5A;color:#00C2D4;padding:6px 10px;border-radius:8px;font:11px system-ui">'+l+'</a>').join('');
    document.body.appendChild(bar);
  }
  async function densify(){
    if(!tok()) return;
    navStrip();
    try{
      const [reg, pillars, gbs, arch, ready, status]=await Promise.all([
        req('/udoc/regulator/summary').catch(e=>({error:String(e)})),
        req('/udoc/constitutional/pillars').catch(()=>req('/udoc/pillars').catch(e=>({error:String(e)}))),
        req('/gis/gbs/overview').catch(e=>({error:String(e)})),
        req('/gis/gbs/architecture').catch(e=>({error:String(e)})),
        req('/udoc/demo/ready').catch(()=>({})),
        req('/admin/status').catch(()=>({})),
      ]);
      ensurePanel('gods-live-regulator','Regulator summary · LIVE');
      if(reg.error) setBody('gods-live-regulator','<span style="color:#E8A13A">'+esc(reg.error)+'</span>');
      else {
        const by=reg.by_outcome||{};
        setBody('gods-live-regulator',
          '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px">'+
          '<div><div style="color:#7A7A8A">Decisions</div><div style="font-size:1.3rem;font-weight:700">'+(reg.decisions??'—')+'</div></div>'+
          '<div><div style="color:#7A7A8A">APPROVE</div><div style="font-size:1.3rem;color:#2D9B5A">'+(by.APPROVE??0)+'</div></div>'+
          '<div><div style="color:#7A7A8A">BLOCK</div><div style="font-size:1.3rem;color:#E85D5D">'+(by.BLOCK??0)+'</div></div>'+
          '<div><div style="color:#7A7A8A">Open oversight</div><div style="font-size:1.3rem">'+(reg.open_oversight??0)+'</div></div>'+
          '</div>');
      }
      ensurePanel('gods-live-pillars','Constitutional pillars · LIVE');
      const plist=pillars.pillars||pillars.constitutional_pillars||[];
      if(pillars.error) setBody('gods-live-pillars','<span style="color:#E8A13A">'+esc(pillars.error)+'</span>');
      else setBody('gods-live-pillars', plist.map(p=>{
        const name=p.name||p.title||'';
        const id=p.id||p.numeral||'';
        const st=p.status||'operational';
        return '<span style="display:inline-block;margin:3px;padding:3px 8px;border:1px solid #243A5A;border-radius:12px;font-size:11px">'+esc(id)+' · '+esc(name)+' <span style="color:#2D9B5A">'+esc(st)+'</span></span>';
      }).join(' ')||'—');
      ensurePanel('gods-live-gbs','GBS freeze · LIVE');
      const honesty=(gbs.honesty&&gbs.honesty.note)||(gbs.note)||'';
      const divs=(arch.divisions||[]).map(d=>esc(d.division||d.name||'')+' <span style="color:#7A7A8A">('+(d.mode||'')+')</span>').join(' · ');
      setBody('gods-live-gbs',
        '<div>Demo ready: <b>'+esc(String(ready.ready))+'</b> · models '+(status.models??'—')+' · learners '+(status.learners??'—')+' · TS projects '+(status.ts_projects??'—')+'</div>'+
        '<div style="margin-top:6px">Divisions: '+(divs||'SETHS · MADIBA · TS · UDOC')+'</div>'+
        '<div style="margin-top:6px;color:#E8A13A;font-size:11px">'+esc(honesty||'capital not_deployed · designed_not_built where noted')+'</div>');
      const m=document.getElementById('gl-msg');
      if(m){ m.textContent='● GODS densify · regulator + pillars + GBS bound'; m.style.color='#2D9B5A'; }
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
