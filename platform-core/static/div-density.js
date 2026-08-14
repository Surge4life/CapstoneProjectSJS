/*! div-density.js — multi-environment density for operator surfaces
 * Inject only. Links Core + Gateway + Client + Sector + Portals SaaS + Operator.
 */
(function(){
  if(window.__DIV_DENSITY__) return; window.__DIV_DENSITY__=1;
  const CORE = "https://gods-platform-core.onrender.com";
  const ENV = {
    core: CORE,
    gateway: "https://gods-udoc-gateway.onrender.com",
    adminHost: "https://gods-udoc-admin.onrender.com",
    client: "https://gods-udoc-client.onrender.com",
    sector: "https://gods-udoc-sector.onrender.com",
    portalsSaaS: "https://gods-udoc-portals.onrender.com",
    operator: "https://gods-udoc-operator.onrender.com",
    web: "https://gods-udoc-web.onrender.com"
  };
  const ON_CORE = /gods-platform-core\.onrender\.com$/i.test(location.hostname);
  const API = ON_CORE ? location.origin : (window.API || CORE);
  const PATH = (location.pathname||"/").replace(/\/$/,"") || "/";
  function corePath(p){ return ON_CORE ? p : (CORE + p); }

  function el(tag, attrs, html){
    const n=document.createElement(tag);
    if(attrs) Object.entries(attrs).forEach(function(pair){
      var k=pair[0], v=pair[1];
      if(k==="className") n.className=v;
      else if(k.startsWith("on") && typeof v==="function") n.addEventListener(k.slice(2).toLowerCase(),v);
      else n.setAttribute(k,v);
    });
    if(html!=null) n.innerHTML=html;
    return n;
  }

  function ensureStyle(){
    if(document.getElementById("div-density-css")) return;
    const s=el("style",{id:"div-density-css"});
    s.textContent=".dd-panel{background:var(--navy2,#0c1830);border:1px solid var(--line,#1c2a45);border-radius:12px;padding:14px;margin-top:12px}.dd-panel h3{margin:0 0 10px;color:var(--gold,#C9A84C);font-size:13px}.dd-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.dd-chip{display:inline-block;border:1px solid var(--line,#1c2a45);border-radius:16px;padding:4px 10px;font-size:11px;cursor:pointer;background:transparent;color:var(--ink,#e8edf6);text-decoration:none}.dd-chip:hover{border-color:var(--cyan,#00C2D4);color:var(--cyan,#00C2D4)}.dd-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;margin-top:8px}.dd-card{background:var(--navy2,#0c1830);border:1px solid var(--line,#1c2a45);border-radius:10px;padding:10px}.dd-card h4{margin:0 0 4px;font-size:10px;text-transform:uppercase;letter-spacing:.05em;color:var(--gold,#C9A84C)}.dd-metric{font-size:1.05rem;font-weight:700}.dd-term{font-family:ui-monospace,monospace;font-size:11px;background:#050b16;border:1px solid var(--line,#1c2a45);border-radius:8px;padding:8px;white-space:pre-wrap;max-height:160px;overflow:auto;margin-top:8px}.dd-mut{color:var(--mut,#8fa0bd);font-size:11px;margin:8px 0 0}.dd-assessor{border-color:rgba(0,194,212,.35);background:rgba(0,194,212,.06)}.dd-table{width:100%;border-collapse:collapse;font-size:12px;margin-top:8px}.dd-table th,.dd-table td{text-align:left;padding:5px 6px;border-bottom:1px solid var(--line,#1c2a45)}.dd-table th{color:var(--mut,#8fa0bd);font-size:10px;text-transform:uppercase}";
    document.head.appendChild(s);
  }

  function logTerm(msg){
    const term=document.getElementById("dd-term")||document.getElementById("term")||document.getElementById("bridge-term");
    if(term) term.textContent=new Date().toLocaleTimeString()+" "+msg+"\n"+(term.textContent||"").slice(0,2000);
  }

  async function evaSmoke(){
    try{
      const r=await fetch(API+"/decisions/batch",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({scenarios:["fair","biased"]})});
      const j=await r.json();
      const o=j.outcomes||{};
      const gate=(Number(o.BLOCK||0)>=1)?"PASS":"CHECK";
      ["k-eva","k-eva2","dd-eva"].forEach(function(id){ const n=document.getElementById(id); if(n) n.textContent=gate+" · B"+(o.BLOCK||0)+"/A"+(o.APPROVE||0); });
      logTerm("EVA "+gate+" "+JSON.stringify(o));
      return j;
    }catch(e){ logTerm("EVA FAIL "+e.message); }
  }

  async function probeReady(){
    try{
      const j=await (await fetch(API+"/udoc/demo/ready")).json();
      const n=document.getElementById("dd-ready"); if(n) n.textContent=j.ready?"DEMO READY":"NOT READY";
      logTerm("READY "+JSON.stringify({ready:j.ready,model:j.model_001&&j.model_001.status}));
      return j;
    }catch(e){ logTerm("READY FAIL "+e.message); }
  }

  async function probeHealth(){
    try{ logTerm("HEALTH "+JSON.stringify(await (await fetch(API+"/health")).json())); }
    catch(e){ logTerm("HEALTH FAIL "+e.message); }
  }

  async function probePillars(){
    try{
      let j=null, used="";
      for(const p of ["/gis/gbs/pillars","/gis/gbs/overview","/gis/gbs/architecture"]){
        try{ const r=await fetch(API+p); if(r.ok){ j=await r.json(); used=p; break; } }catch(_){}
      }
      logTerm(j?("PILLARS "+used+" "+JSON.stringify(j).slice(0,500)):"PILLARS no route");
      const eln=document.getElementById("dd-pillars-out");
      if(eln && j) eln.textContent=JSON.stringify(j,null,2).slice(0,1800);
    }catch(e){ logTerm("PILLARS FAIL "+e.message); }
  }

  async function probeDivMetrics(){
    try{
      const pair=await Promise.all([
        fetch(API+"/seths/metrics").then(function(r){return r.ok?r.json():{};}).catch(function(){return {};}),
        fetch(API+"/ts/metrics").then(function(r){return r.ok?r.json():{};}).catch(function(){return {};}),
        fetch(API+"/madiba/metrics").then(function(r){return r.ok?r.json():{};}).catch(function(){return {};})
      ]);
      const s=pair[0], t=pair[1], m=pair[2];
      const eln=document.getElementById("dd-div-kpis");
      if(eln){
        eln.innerHTML="<table class=\"dd-table\"><thead><tr><th>Division</th><th>KPI</th><th>Value</th><th>Honesty</th></tr></thead><tbody>"+
          "<tr><td><b>SETHS</b></td><td>total / placed</td><td>"+(s.total!=null?s.total:"—")+" / "+(s.placed!=null?s.placed:"—")+"</td><td class=\"dd-mut\">demo learners</td></tr>"+
          "<tr><td><b>TS</b></td><td>projects / workers</td><td>"+(t.projects!=null?t.projects:"—")+" / "+(t.workers_absorbed!=null?t.workers_absorbed:"—")+"</td><td class=\"dd-mut\">capital not_deployed</td></tr>"+
          "<tr><td><b>MADIBA</b></td><td>cycles / recycled</td><td>"+(m.cycles!=null?m.cycles:"—")+" / "+(m.cumulative_recycled!=null?m.cumulative_recycled:"—")+"</td><td class=\"dd-mut\">ledger ≠ AUM</td></tr>"+
          "</tbody></table>";
      }
      logTerm("DIV KPIs ok");
    }catch(e){ logTerm("DIV KPIs FAIL "+e.message); }
  }

  function surfaceTruth(){
    const map={
      "/seths":{title:"SETHS truth",chips:["placement_rate = live Neon","not funded programme","PLACED → TS assign FK","demo learners OK"],loop:"Enrol → Advance → PLACED → TS → MADIBA"},
      "/ts":{title:"TS truth",chips:["SPVs = Neon rows","capital not_deployed","assign requires PLACED"],loop:"PLACED on SETHS → Deploy SPV → Assign → MADIBA"},
      "/madiba":{title:"MADIBA truth",chips:["ledger only · not AUM","capital not_deployed","EIF parallel audit"],loop:"Allocate → Engage → EIF nominate"},
      "/gbs":{title:"GBS freeze truth",chips:["pillars live","nodes may be empty","Sovereign-Verified = designed_not_built"],loop:"Overview → Nodes → Division KPIs → EVA"},
      "/eif-ui":{title:"EIF truth",chips:["nominate = audit-only","no Diamond grant free tier"],loop:"Framework → Nominate → MADIBA"},
      "/portals":{title:"Portals truth",chips:["Core-routed","CITIZEN on Client host","OversightCase on Neon"],loop:"Open control → EVA"},
      "/divisions":{title:"Divisions cockpit",chips:["SETHS→TS→MADIBA","zeros OK","MADIBA ≠ AUM"],loop:"Full loop → EVA → GBS"},
      "/Sentinel":{title:"Sentinel truth",chips:["fair≠BLOCK biased=BLOCK","model-001 auto-heal"],loop:"Ready → Fair → Biased → Smoke"}
    };
    return map[PATH]||map["/divisions"];
  }

  function mount(){
    ensureStyle();
    const host = document.getElementById("ops") || document.querySelector("main") || document.querySelector(".wrap") || document.body;
    if(!host || document.getElementById("dd-root")) return;
    const root=el("div",{id:"dd-root"});
    const truth=surfaceTruth();

    const assessor=el("div",{className:"dd-panel dd-assessor"});
    assessor.appendChild(el("h3",{},"Assessor strip · "+PATH+(ON_CORE?"":" · via Core API")));
    const row1=el("div",{className:"dd-row"});
    [["EVA fair/biased",evaSmoke],["demo/ready",probeReady],["/health",probeHealth],["Division KPIs",probeDivMetrics],["GBS pillars",probePillars]].forEach(function(pair){
      const b=el("button",{type:"button",className:"dd-chip"},pair[0]); b.onclick=pair[1]; row1.appendChild(b);
    });
    assessor.appendChild(row1);
    const kpis=el("div",{className:"dd-grid"});
    kpis.innerHTML='<div class="dd-card"><h4>EVA gate</h4><div class="dd-metric" id="dd-eva">run chip</div></div><div class="dd-card"><h4>Ready</h4><div class="dd-metric" id="dd-ready">—</div></div><div class="dd-card"><h4>Honesty</h4><div class="dd-metric" style="font-size:0.85rem">capital not_deployed</div></div><div class="dd-card"><h4>API</h4><div class="dd-metric" style="font-size:0.75rem">'+(ON_CORE?"Core origin":"Core absolute")+'</div></div>';
    assessor.appendChild(kpis);
    assessor.appendChild(el("p",{className:"dd-mut"},"Capstone: zeros OK · MADIBA ≠ AUM · Sovereign-Verified = designed_not_built · biased must BLOCK"));
    root.appendChild(assessor);

    const truthP=el("div",{className:"dd-panel"});
    truthP.appendChild(el("h3",{},truth.title));
    const chips=el("div",{className:"dd-row"});
    truth.chips.forEach(function(c){ chips.appendChild(el("span",{className:"dd-chip"},c)); });
    truthP.appendChild(chips);
    truthP.appendChild(el("p",{className:"dd-mut"},"Operator loop: "+truth.loop));
    root.appendChild(truthP);

    const mapEl=el("div",{className:"dd-panel"});
    mapEl.appendChild(el("h3",{},"Core operator surfaces"));
    const row2=el("div",{className:"dd-row"});
    [["/seths","SETHS"],["/ts","TS"],["/madiba","MADIBA"],["/gbs","GBS"],["/eif-ui","EIF"],["/divisions","Divisions"],["/portals","Core Portals"],["/Sentinel","Sentinel"],["/udoc-admin","UDOC Admin"],["/admin","GODS Admin"]].forEach(function(pair){
      var a=el("a",{className:"dd-chip",href:corePath(pair[0])},pair[1]);
      if(!ON_CORE) a.setAttribute("target","_blank");
      row2.appendChild(a);
    });
    mapEl.appendChild(row2);
    root.appendChild(mapEl);

    const envP=el("div",{className:"dd-panel"});
    envP.appendChild(el("h3",{},"Environments · full stack"));
    const rowE=el("div",{className:"dd-row"});
    [[ENV.gateway,"Gateway"],[ENV.core,"Core API"],[ENV.adminHost,"Admin host"],[corePath("/udoc-admin"),"Core UDOC Admin"],[ENV.client,"Client Web"],[ENV.client+"/citizen.html","Citizen"],[ENV.sector,"Sector"],[ENV.portalsSaaS,"SaaS Portals"],[ENV.operator,"Operator"],[ENV.web,"UDOC App"]].forEach(function(pair){
      rowE.appendChild(el("a",{className:"dd-chip",href:pair[0],target:"_blank",rel:"noopener"},pair[1]));
    });
    envP.appendChild(rowE);
    envP.appendChild(el("p",{className:"dd-mut"},"Core hosts division operators · Client hosts Citizen · Gateway routes by role · all share Core API / Neon"));
    root.appendChild(envP);

    const divk=el("div",{className:"dd-panel"});
    divk.innerHTML='<h3>Four-division KPIs · live probe</h3><div id="dd-div-kpis" class="dd-mut">Click Division KPIs or wait…</div>';
    root.appendChild(divk);

    const pill=el("div",{className:"dd-panel"});
    pill.innerHTML='<h3>GBS / GIS probe output</h3><div class="dd-term" id="dd-pillars-out">Run GBS pillars chip</div>';
    root.appendChild(pill);

    const bridge=el("div",{className:"dd-panel"});
    bridge.appendChild(el("h3",{},"Core bridge · live probes"));
    bridge.appendChild(el("div",{className:"dd-term",id:"dd-term"},"API="+API));
    root.appendChild(bridge);

    const help=el("div",{className:"dd-panel"});
    help.innerHTML='<h3>Capstone operator help</h3><table class="dd-table"><thead><tr><th>Action</th><th>Expected</th><th>Honesty</th></tr></thead><tbody><tr><td>EVA fair</td><td>APPROVE</td><td>deterministic</td></tr><tr><td>EVA biased</td><td>BLOCK</td><td>fail-closed</td></tr><tr><td>demo/ready</td><td>ready:true</td><td>auto-heal</td></tr><tr><td>Division metrics</td><td>may be zero</td><td>zeros OK</td></tr></tbody></table><p class="dd-mut">Assessor: Gateway → Core health → demo/ready → Sentinel Fair/Biased → division path → UDOC Admin Layers.</p>';
    root.appendChild(help);

    const cred=el("div",{className:"dd-panel"});
    cred.innerHTML='<h3>Staff credentials · Capstone</h3><div class="dd-row"><span class="dd-chip">admin@gods.local / admin123</span><span class="dd-chip">seths@ / madiba@ / ts@ · staff123</span><span class="dd-chip">client@udoc.demo / client123</span></div><p class="dd-mut">No new registration on Neon free · staff + client demo seed only</p>';
    root.appendChild(cred);

    const termPanel = Array.from(host.querySelectorAll(".panel,div")).find(function(p){return /Ops terminal|Terminal/i.test(p.textContent||"") && p.querySelector(".term,#term");});
    if(termPanel && termPanel.parentNode) termPanel.parentNode.insertBefore(root, termPanel);
    else host.appendChild(root);

    setTimeout(function(){ probeReady().catch(function(){}); probeDivMetrics().catch(function(){}); }, 500);

    if(typeof window.evaSmoke==="function"){
      const orig=window.evaSmoke;
      window.evaSmoke=async function(){ try{ await orig.apply(this,arguments);}catch(_){} return evaSmoke(); };
    } else window.evaSmoke=evaSmoke;
  }

  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",mount);
  else mount();
})();
