/*! udoc-admin-density.js — densify UDOC Admin (additive)
 * Core operators + EVA + ready — not intelligence-only.
 * Capstone Priority 1 density · 2026-08-14
 */
(function(){
  if(window.__UDOC_ADMIN_DENSITY__) return; window.__UDOC_ADMIN_DENSITY__=1;
  const API = location.origin;

  function el(tag, attrs, html){
    const n=document.createElement(tag);
    if(attrs) Object.keys(attrs).forEach(function(k){
      if(k==="style"&&typeof attrs[k]==="object") Object.assign(n.style, attrs[k]);
      else if(k==="onclick") n.onclick=attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    if(html!=null) n.innerHTML=html;
    return n;
  }

  function setK(id,v){ const n=document.getElementById(id); if(n) n.textContent=v; }

  async function probe(){
    try{
      const h=await(await fetch(API+"/health")).json();
      setK("uad-h", h.status||"ok");
    }catch(e){ setK("uad-h","FAIL"); }
    try{
      const r=await(await fetch(API+"/udoc/demo/ready")).json();
      setK("uad-r", r.ready?"READY":"NO");
    }catch(e){ setK("uad-r","FAIL"); }
    try{
      const j=await(await fetch(API+"/decisions/batch",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({scenarios:["fair","biased"]})
      })).json();
      const o=j.outcomes||{};
      const gate=Number(o.BLOCK||0)>=1?"PASS":"CHECK";
      setK("uad-e", gate+" · B"+(o.BLOCK||0)+"/A"+(o.APPROVE||0));
    }catch(e){ setK("uad-e","FAIL"); }
  }

  function chip(href, label, external){
    return '<a href="'+href+'" '+(external?'target="_blank" rel="noopener"':'')+
      ' style="border:1px solid #1c2a45;border-radius:16px;padding:6px 12px;font-size:12px;color:#e8edf6;text-decoration:none;background:#091022">'+label+'</a>';
  }

  function mount(){
    if(document.getElementById("uad-core-ops")) return;
    const host=document.querySelector("main")||document.querySelector(".wrap")||document.body;
    const root=el("div",{id:"uad-core-ops"});
    root.style.cssText="max-width:1100px;margin:12px auto;padding:0 16px 24px;font:13px/1.45 system-ui,sans-serif;color:#e8edf6";
    root.innerHTML=[
      '<div style="background:#0c1830;border:1px solid #C9A84C;border-radius:12px;padding:14px;margin-bottom:12px">',
      '<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px">',
      '<b style="color:#C9A84C">Core operators · full platform (not intelligence-only)</b>',
      '<span style="font-size:11px;color:#8fa0bd">UDOC Admin = governance · open division surfaces on Core</span>',
      '<span style="flex:1"></span>',
      '<button type="button" id="uad-probe" style="background:#00C2D4;color:#041018;border:none;border-radius:8px;padding:6px 12px;font-weight:600;cursor:pointer;font-size:12px">Probe Core</button>',
      '</div>',
      '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin-bottom:12px">',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">Health</div><div id="uad-h" style="font-weight:700">—</div></div>',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">Ready</div><div id="uad-r" style="font-weight:700">—</div></div>',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">EVA</div><div id="uad-e" style="font-weight:700">—</div></div>',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">Honesty</div><div style="font-weight:700;font-size:12px">not_deployed</div></div>',
      '</div>',
      '<div style="margin-bottom:6px;font-size:11px;color:#C9A84C;text-transform:uppercase">Division operators</div>',
      '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px">',
      chip("/seths","SETHS · develops"),
      chip("/ts","TS · deploys"),
      chip("/madiba","MADIBA · ledger ≠ AUM"),
      chip("/divisions","All divisions"),
      chip("/gbs","GBS · holdings"),
      chip("/eif-ui","EIF"),
      chip("/Sentinel","Sentinel · EVA"),
      chip("/portals","Portals · 24"),
      '</div>',
      '<div style="margin-bottom:6px;font-size:11px;color:#C9A84C;text-transform:uppercase">Governance · admin</div>',
      '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px">',
      chip("/admin","GODS Admin · constitutional"),
      chip("/udoc-admin","UDOC Admin · this surface"),
      '</div>',
      '<div style="margin-bottom:6px;font-size:11px;color:#C9A84C;text-transform:uppercase">Environments</div>',
      '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px">',
      chip("https://gods-udoc-gateway.onrender.com/","Gateway",true),
      chip("https://gods-udoc-client.onrender.com/","Client",true),
      chip("https://gods-udoc-client.onrender.com/citizen.html","Citizen",true),
      chip("https://gods-udoc-sector.onrender.com/","Sector",true),
      chip("https://gods-udoc-operator.onrender.com/","Operator",true),
      '</div>',
      '<p style="margin:0;font-size:11px;color:#8fa0bd">After Connect: use Layers / Control / Evidence tabs here. Division work opens on Core operator URLs above — not limited to Intelligence.</p>',
      '</div>'
    ].join("");
    if(host.firstChild) host.insertBefore(root, host.firstChild);
    else host.appendChild(root);
    const b=document.getElementById("uad-probe");
    if(b) b.onclick=probe;
    probe();
  }

  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",mount);
  else mount();
})();
