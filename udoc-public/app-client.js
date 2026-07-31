const PROD_API="https://gods-platform-core.onrender.com";
let SCENARIO="fair",SECTOR=null,LAST_CERT="",LAST_DID=null;
function apiBase(){return localStorage.getItem("udoc_client_api")||PROD_API;}
function setApiBase(v){localStorage.setItem("udoc_client_api",v.replace(/\/+$/,""));}
function token(){return localStorage.getItem("udoc_client_tok")||"";}
function esc(s){const d=document.createElement("div");d.textContent=String(s==null?"":s);return d.innerHTML;}
function netErr(e){const m=String(e&&e.message||e||"");if(/Failed to fetch|NetworkError|Load failed|network/i.test(m))return "Core unreachable (Render cold start or offline). Open "+apiBase()+"/health · wait 30–90s · retry.";return m;}
async function api(path,opts={}){const h=Object.assign({},opts.headers||{});if(token())h.Authorization="Bearer "+token();
let r;
try{r=await fetch(apiBase()+path,Object.assign({},opts,{headers:h}));}catch(e){throw new Error(netErr(e));}
if(r.status===401){if(token())logout();throw new Error("Session expired");}
const ct=r.headers.get("content-type")||"";const body=ct.includes("json")?await r.json().catch(()=>null):await r.text();
if(!r.ok)throw new Error((body&&body.detail)||(typeof body==="string"?body:("HTTP "+r.status)));return body;}
document.getElementById("li-api").value=apiBase();
async function doLogin(){const e=document.getElementById("li-err");e.textContent="";const a=document.getElementById("li-api").value.trim();if(a)setApiBase(a);
const btn=document.getElementById("li-btn");btn.disabled=true;btn.textContent="Signing in…";
try{const f=new URLSearchParams({username:document.getElementById("li-email").value.trim().toLowerCase(),password:document.getElementById("li-pass").value});
const r=await fetch(apiBase()+"/auth/login",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:f});
if(!r.ok)throw new Error(r.status===401?"Invalid credentials":"Login failed");
const d=await r.json();localStorage.setItem("udoc_client_tok",d.access_token);
localStorage.setItem("udoc_client_who",JSON.stringify({email:document.getElementById("li-email").value.trim().toLowerCase(),role:d.role,tenant_id:d.tenant_id,tenant_pk:d.tenant_pk}));enterApp();
}catch(err){e.textContent=netErr(err);}finally{btn.disabled=false;btn.textContent="Sign in";}}
function logout(){localStorage.removeItem("udoc_client_tok");document.getElementById("app").style.display="none";document.getElementById("login").style.display="flex";}
async function enterApp(){const w=JSON.parse(localStorage.getItem("udoc_client_who")||"{}");
document.getElementById("login").style.display="none";document.getElementById("app").style.display="grid";
document.getElementById("who-email").textContent=w.email||"—";document.getElementById("who-tenant").textContent=w.tenant_id||(w.role?("role:"+w.role):"");
heartbeat();try{SECTOR=await api("/sector/profile");}catch(e){}nav("dash");}
async function heartbeat(){const el=document.getElementById("hb");try{await fetch(apiBase()+"/health");el.textContent="· online";el.className="pill up";}catch{el.textContent="· offline";el.className="pill down";}}
function nav(v){
if(v==="citizen"){window.location.href="/citizen.html";return;}
if(v==="sentinel"){window.open(apiBase()+"/Sentinel","_blank");return;}
document.querySelectorAll("#nav .navitem").forEach(n=>n.classList.toggle("active",n.dataset.view===v));
const m=document.getElementById("main");m.innerHTML='<div class="loading">Loading…</div>';
({dash:vDash,systems:vSystems,compliance:vCompliance,audit:vAudit,bias:vBias,sovereignty:vSov,govern:vGovern,decisions:vDecisions,knowledge:vKnowledge,settings:vSettings}[v]||vDash)(m);}
document.querySelectorAll("#nav .navitem").forEach(n=>n.addEventListener("click",()=>nav(n.dataset.view)));
function asArray(d){if(Array.isArray(d))return d;if(d&&typeof d==="object"){for(const k of["items","models","results","data","keys","incidents","certificates"])if(Array.isArray(d[k]))return d[k];}return [];}
function riskTag(v){v=String(v||"").toUpperCase();const c=/HIGH|CRIT|UNACCEPTABLE/.test(v)?"t-bad":(/MEDIUM|NOTABLE/.test(v)?"t-warn":"t-ok");return '<span class="tag2 '+c+'">'+esc(v||"—")+'</span>';}
function statusTag(v){const u=String(v||"").toUpperCase();const c=/ACTIVE|APPROVE|VALID|VERIFIED/.test(u)?"t-ok":(/PEND|REVIEW/.test(u)?"t-warn":(/BLOCK|DENIED|INVALID|ESCALATE/.test(u)?"t-bad":"t-info"));return '<span class="tag2 '+c+'">'+esc(v||"—")+'</span>';}
function tableFrom(rows,cols){if(!rows.length)return'<div class="muted">No records.</div>';let h='<table><thead><tr>'+cols.map(c=>'<th>'+esc(c.h)+'</th>').join('')+'</tr></thead><tbody>';
rows.forEach(r=>{h+='<tr>'+cols.map(c=>'<td>'+(c.r?c.r(r):esc(r[c.k]))+'</td>').join('')+'</tr>';});return h+'</tbody></table>';}
async function safe(host,fn){try{return await fn();}catch(e){host.innerHTML='<div class="panel t-bad">'+esc(netErr(e))+'</div>';}}
function dimsHtml(dims){if(!dims||typeof dims!=="object")return"";const order=["Validity","Confidence","Risk","Compliance","Stability","Impact"];
const keys=order.filter(k=>dims[k]!=null).concat(Object.keys(dims).filter(k=>!order.includes(k)));
return'<div class="dims">'+keys.map(k=>{const v=Number(dims[k]);const pct=isNaN(v)?0:Math.min(100,Math.max(0,(v<=1?v*100:v*10)));
return'<div class="dim"><div class="dk">'+esc(k)+'</div><div class="dv">'+(isNaN(v)?"—":(v<=1?v.toFixed(2):v))+'</div><div class="bar"><i style="width:'+pct+'%"></i></div></div>';}).join('')+'</div>';}
function honesty(){return'<div class="note">Pre-registration · GG54477 withdrawn · POPIA s71 + Constitution · Neon ≤500MB · Netlify mvp-1/mvp-2 acceptance path.</div>';}

function scenarioBody(kind, mid, conf, comp){
  const body={model_id:mid||"model-001",raw_confidence:conf!=null?conf:0.92,compliance:comp!=null?comp:1.0};
  if(kind==="biased"){body.priv_favorable=900;body.priv_total=1000;body.unpriv_favorable=120;body.unpriv_total=1000;}
  if(kind==="high")body.risk_tier="HIGH";
  if(kind==="sov"){body.bgp=0.4;body.traceroute=0.5;body.dnssec=0.6;body.storage=0.7;}
  return body;
}

async function clientSmoke(){
  const host=document.getElementById("client-smoke-out"); if(!host) return;
  host.innerHTML="Running 4 live checks…";
  const steps=[]; const t0=Date.now();
  async function step(name,fn){try{const d=await fn();steps.push({name,ok:true,d});}catch(e){steps.push({name,ok:false,d:String(e.message||e)});}}
  await step("/health",async()=>{const r=await fetch(apiBase()+"/health");if(!r.ok)throw new Error("HTTP "+r.status);return await r.json().catch(()=>({}));});
  await step("/udoc/demo/ready",async()=>{const d=await api("/udoc/demo/ready");if(!d.ready)throw new Error((d.missing||[]).join("; ")||"not ready");return d;});
  await step("EVA fair",async()=>{const d=await api("/decisions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(scenarioBody("fair"))});if(d.decision==="BLOCK")throw new Error("fair BLOCK");return {decision:d.decision};});
  await step("EVA biased BLOCK",async()=>{const d=await api("/decisions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(scenarioBody("biased"))});if(d.decision!=="BLOCK")throw new Error("got "+d.decision);return {decision:d.decision};});
  const ok=steps.filter(s=>s.ok).length;
  host.innerHTML='<div class="grid kpis" style="margin-top:8px"><div class="kpi"><div class="k">Passed</div><div class="v '+(ok===4?'green':'red')+'">'+ok+'/4</div></div><div class="kpi"><div class="k">ms</div><div class="v">'+(Date.now()-t0)+'</div></div></div>'+
    '<table style="margin-top:8px"><thead><tr><th>Check</th><th>Result</th><th>Detail</th></tr></thead><tbody>'+
    steps.map(s=>'<tr><td>'+esc(s.name)+'</td><td class="'+(s.ok?'t-ok':'t-bad')+'">'+(s.ok?'PASS':'FAIL')+'</td><td class="mono" style="font-size:11px">'+esc(typeof s.d==='object'?JSON.stringify(s.d).slice(0,80):String(s.d).slice(0,80))+'</td></tr>').join('')+
    '</tbody></table>';
}

async function vDash(m){let sys=[],dec=[],ready=null,ex={},certs=[],sum={};
try{sys=asArray(await api("/registry/models"));}catch(e){}
try{dec=asArray(await api("/decisions"));}catch(e){}
try{ready=await api("/udoc/demo/ready");}catch(e){}
try{ex=await api("/udoc/exchange");}catch(e){}
try{certs=asArray(await api("/decisions/certificates"));}catch(e){}
try{sum=await api("/udoc/regulator/summary");}catch(e){}
const oc=(sum.decisions&&sum.decisions.by_outcome)||{};
const ap=oc.APPROVE!=null?oc.APPROVE:dec.filter(d=>/APPROVE/i.test(String(d.decision||""))).length;
const bl=oc.BLOCK!=null?oc.BLOCK:dec.filter(d=>/BLOCK/i.test(String(d.decision||""))).length;
const es=oc.ESCALATE!=null?oc.ESCALATE:dec.filter(d=>/ESCALATE/i.test(String(d.decision||""))).length;
const card=(k,v,c)=>'<div class="kpi"><div class="k">'+esc(k)+'</div><div class="v '+(c||'')+'">'+esc(v)+'</div></div>';
const recent=dec.slice(0,8);
m.innerHTML='<div class="pgh"><h2>Command Dashboard</h2><span class="desc">mvp-1 International Standards · live Core · demo density</span></div>'+
'<div class="panel"><h3>Boot posture</h3><div>'+(ready&&ready.ready?'<span class="t-ok">DEMO READY</span> · active rules '+esc(ready.active_rules):'<span class="t-bad">SEED PENDING</span>')+' · prefer <span class="mono">model-001</span> · policy-to-code</div></div>'+
'<div class="grid kpis">'+card("AI systems",sys.length,"cyan")+card("Decisions",dec.length)+card("APPROVE",ap,"green")+card("BLOCK",bl,"red")+card("ESCALATE",es,"amber")+card("Certs",certs.length,"cyan")+'</div>'+
'<div class="grid" style="grid-template-columns:1fr 1fr;gap:12px">'+
'<div class="panel" style="margin:0"><h3>Sovereignty strip</h3><div class="sov-ok">ZA · '+esc(ex.jurisdiction||"ZA")+'</div><div class="sov-ok">Localisation rules · '+esc(ex.rules_active!=null?ex.rules_active:"—")+'</div><div class="sov-ok">Fail-closed path · policy-to-code</div></div>'+
'<div class="panel" style="margin:0"><h3>Quick actions</h3>'+
'<button class="btn cyan sm" onclick="nav(\'govern\')">Govern · EVA</button> '+
'<button class="btn sm" onclick="nav(\'knowledge\')">Company Knowledge</button> '+
'<button class="btn sm" onclick="nav(\'bias\')">Bias Monitor</button> '+
'<button class="btn sm" onclick="nav(\'compliance\')">Compliance</button> '+
'<button class="btn sm" onclick="nav(\'citizen\')">Citizen Portal</button> '+
'<button class="btn sm" onclick="nav(\'sentinel\')">Sentinel</button></div></div>'+
'<div class="panel"><h3>Recent decisions · live</h3>'+(recent.length?tableFrom(recent,[
{h:"ID",r:x=>'<span class="mono">'+esc(x.id||x.decision_id)+'</span>'},
{h:"Model",r:x=>esc(x.model_id)},
{h:"EVA",r:x=>'<b style="color:var(--gold-l)">'+esc(x.composite_eva!=null?x.composite_eva:"—")+'</b>'},
{h:"Verdict",r:x=>statusTag(x.decision)}
]):'<div class="muted">None yet — run Govern scenario chips or Full EVA batch.</div>')+
'<div style="margin-top:10px"><button class="btn cyan sm" onclick="nav(\'govern\')">Open Govern · run scenarios</button></div></div>'+
'<div class="panel"><h3>Client smoke · 4 live checks</h3>'+
'<button class="btn cyan" onclick="clientSmoke()">Run client smoke</button>'+
'<div id="client-smoke-out" class="muted" style="margin-top:10px;font-size:12px">health · demo/ready · fair ≠ BLOCK · biased = BLOCK</div></div>'+
honesty();}

async function vSystems(m){await safe(m,async()=>{const rows=asArray(await api("/registry/models"));
m.innerHTML='<div class="pgh"><h2>AI Registry</h2><span class="desc">mvp-1 · registered systems</span></div><div class="panel"><h3>Registered · '+rows.length+'</h3>'+tableFrom(rows,[
{h:"System",r:x=>'<b>'+esc(x.name||x.model_id)+'</b><br><span class="mono muted" style="font-size:11px">'+esc(x.model_id)+'</span>'},
{h:"Risk",r:x=>riskTag(x.risk_tier)},{h:"Status",r:x=>statusTag(x.status)}])+'</div>'+
'<div class="panel"><button class="btn cyan sm" onclick="nav(\'govern\')">Evaluate on Govern</button></div>'+honesty();});}

async function vCompliance(m){await safe(m,async()=>{let sfw={frameworks:[]},active={},ready=null;
try{sfw=await api("/sector/frameworks");}catch(e){}try{active=await api("/policy/active");}catch(e){}try{ready=await api("/udoc/demo/ready");}catch(e){}
const defaults=[{name:"POPIA s71",basis:"POPIA",focus:"Automated decisions"},{name:"Constitution ss 9/14/33",basis:"Bill of Rights",focus:"Equality · privacy · PAJA"},
{name:"National AI Policy Framework 2024",basis:"Standing SA instrument",focus:"GG54477 withdrawn"},
{name:"EU AI Act risk tiers",basis:"Intl",focus:"Risk classification"},{name:"NIST AI RMF",basis:"Govern-Map-Measure-Manage",focus:"Lifecycle"},
{name:"ISO/IEC 42001:2023",basis:"AIMS",focus:"Organisation controls"}];
const fws=(sfw.frameworks&&sfw.frameworks.length)?sfw.frameworks:defaults;
const cards=fws.map((f,i)=>{const pct=55+(i*9)%40;return'<div class="panel" style="margin:0;border-left:3px solid var(--gold)"><h3 style="text-transform:none;letter-spacing:0;color:var(--txt);font-size:13px">'+esc(f.name)+'</h3><div class="mono" style="font-size:10px;color:var(--cyan)">'+esc(f.basis||"")+'</div><div class="muted" style="font-size:12px;margin-top:6px">'+esc(f.focus||"")+'</div><div class="covbar"><i style="width:'+pct+'%"></i></div></div>';}).join('');
m.innerHTML='<div class="pgh"><h2>Multi-Framework Compliance</h2><span class="desc">mvp-2 · coverage bars</span></div>'+
'<div class="grid kpis"><div class="kpi"><div class="k">Frameworks</div><div class="v cyan">'+fws.length+'</div></div><div class="kpi"><div class="k">Policy rules</div><div class="v">'+(active.enforced_rules!=null?active.enforced_rules:(active.active_rules!=null?active.active_rules:"—"))+'</div></div><div class="kpi"><div class="k">Seed</div><div class="v" style="font-size:16px">'+(ready&&ready.ready?"READY":"WAIT")+'</div></div></div>'+
'<div class="panel"><button class="btn cyan" onclick="runSweep(this)">Run compliance sweep</button> <button class="btn sm" onclick="nav(\'govern\')">Govern EVA</button> <span id="sweep-res" class="muted" style="font-size:12px"></span></div>'+
'<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px">'+cards+'</div>'+honesty();});}
async function runSweep(btn){btn.disabled=true;const r=document.getElementById("sweep-res");if(r)r.textContent="running…";
try{const d=await api("/compliance/sweep",{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"});if(r)r.textContent="done · "+esc(JSON.stringify(d).slice(0,120));}
catch(e){if(r)r.textContent=netErr(e);}finally{btn.disabled=false;}}

async function vAudit(m){await safe(m,async()=>{const rows=asArray(await api("/decisions"));
m.innerHTML='<div class="pgh"><h2>Audit Trail</h2><span class="desc">mvp-1 · sealed decisions</span></div><div class="panel"><h3>Recent · '+rows.length+'</h3>'+tableFrom(rows.slice(0,50),[
{h:"ID",r:x=>'<span class="mono">'+esc(x.id||x.decision_id)+'</span>'},{h:"System",r:x=>esc(x.model_id)},{h:"Verdict",r:x=>statusTag(x.decision)},
{h:"EVA",r:x=>'<b style="color:var(--gold-l)">'+esc(x.composite_eva!=null?x.composite_eva:"—")+'</b>'},{h:"ms",r:x=>esc(x.latency_ms)}])+'</div>'+honesty();});}

async function vBias(m){await safe(m,async()=>{let sum={},inc={};
try{sum=await api("/udoc/regulator/summary");}catch(e){}try{inc=await api("/udoc/incidents");}catch(e){}
const oc=(sum.decisions&&sum.decisions.by_outcome)||{};const incidents=inc.incidents||asArray(inc);
m.innerHTML='<div class="pgh"><h2>Bias Monitor</h2><span class="desc">mvp-1 · live scan + Biased EVA path</span></div>'+
'<div class="grid kpis"><div class="kpi"><div class="k">BLOCK</div><div class="v red">'+(oc.BLOCK||0)+'</div></div><div class="kpi"><div class="k">ESCALATE</div><div class="v amber">'+(oc.ESCALATE||0)+'</div></div><div class="kpi"><div class="k">Incidents</div><div class="v">'+incidents.length+'</div></div></div>'+
'<div class="panel"><h3>Live bias scan</h3><button class="btn cyan" onclick="runBiasScan(this)">Run bias scan</button> <button class="btn sm" onclick="SCENARIO=\'biased\';nav(\'govern\')">Govern · Biased → BLOCK</button> <span id="bias-scan-res" class="muted" style="font-size:12px"></span></div>'+
'<div class="panel"><h3>Incident feed</h3>'+(incidents.length?tableFrom(incidents.slice(0,15),[{h:"Decision",r:x=>esc(x.decision_id)},{h:"Model",r:x=>esc(x.model_id)},{h:"Severity",r:x=>statusTag(x.severity)},{h:"Reasons",r:x=>esc(x.reasons)}]):'<div class="muted">None yet — run Biased on Govern or bias scan.</div>')+'</div>'+honesty();});}
async function runBiasScan(btn){btn.disabled=true;const r=document.getElementById("bias-scan-res");if(r)r.textContent="scanning…";
try{const d=await api("/bias/scan");if(r)r.textContent="scanned "+(d.decisions_scanned!=null?d.decisions_scanned:"?")+" · flagged "+(d.fairness_flagged!=null?d.fairness_flagged:"?")+" · rate "+(d.flag_rate!=null?(d.flag_rate*100).toFixed(1)+"%":"—");}
catch(e){if(r)r.textContent=netErr(e);}finally{btn.disabled=false;}}

async function vSov(m){await safe(m,async()=>{let ex={},ready={};try{ex=await api("/udoc/exchange");}catch(e){}try{ready=await api("/udoc/demo/ready");}catch(e){}
m.innerHTML='<div class="pgh"><h2>Sovereignty</h2><span class="desc">mvp-1/2 · ZA localisation</span></div>'+
'<div class="grid kpis"><div class="kpi"><div class="k">Jurisdiction</div><div class="v cyan">'+esc(ex.jurisdiction||"ZA")+'</div></div><div class="kpi"><div class="k">Rules</div><div class="v">'+(ex.rules_active!=null?ex.rules_active:"—")+'</div></div><div class="kpi"><div class="k">Seed</div><div class="v" style="font-size:16px">'+(ready.ready?"OK":"WAIT")+'</div></div></div>'+
'<div class="panel"><h3>Guarantees</h3><div class="sov-ok">South African jurisdiction</div><div class="sov-ok">Fail-closed when model/policy missing</div><div class="sov-ok">Policy-to-code on decisions</div><div class="term">'+esc(ex.basis||"")+' · '+esc(ex.cross_border_transfer||"")+'</div></div>'+
'<div class="panel"><button class="btn cyan sm" onclick="SCENARIO=\'sov\';nav(\'govern\')">Govern · Sovereignty scenario</button></div>'+honesty();});}

async function vGovern(m){await safe(m,async()=>{let models=asArray(await api("/registry/models").catch(()=>[]));let ready=null;try{ready=await api("/udoc/demo/ready");}catch(e){}
const mid0=(models.find(x=>x.model_id==="model-001")||models[0]||{}).model_id||"model-001";
m.innerHTML='<div class="pgh"><h2>Govern · EVA</h2><span class="desc">'+(ready&&ready.ready?'<span class="t-ok">demo ready</span>':'<span class="t-bad">seed pending</span>')+' · Fair / Biased / High-risk / Sovereignty</span></div>'+
'<div class="panel"><h3>Scenario chips · auto-run</h3><div class="scenarios">'+
'<span class="chip active" onclick="gScenario(this,\'fair\')">Fair</span>'+
'<span class="chip" onclick="gScenario(this,\'biased\')">Biased → BLOCK</span>'+
'<span class="chip" onclick="gScenario(this,\'high\')">High-risk</span>'+
'<span class="chip" onclick="gScenario(this,\'sov\')">Sovereignty</span></div>'+
'<div class="row"><div class="f"><label>Model</label><input id="g-mid" value="'+esc(mid0)+'"/></div>'+
'<div class="f"><label>Confidence</label><input id="g-conf" value="0.92"/></div>'+
'<div class="f"><label>Compliance</label><input id="g-comp" value="1.0"/></div></div>'+
'<div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">'+
'<button class="btn" onclick="gEvaluate()">Evaluate · EVA</button>'+
'<button class="btn cyan" onclick="gBatch()">Run Full EVA batch</button></div></div>'+
'<div id="g-batch-kpis"></div>'+
'<div id="g-out"></div>'+honesty();});}
function gScenario(el,kind){SCENARIO=kind;document.querySelectorAll('.scenarios .chip').forEach(c=>c.classList.remove('active'));if(el)el.classList.add('active');gEvaluate();}
async function gEvaluate(){const out=document.getElementById("g-out");if(!out)return;out.innerHTML='<div class="panel muted">Evaluating…</div>';
const mid=document.getElementById("g-mid").value.trim();
const conf=parseFloat(document.getElementById("g-conf").value)||0.9;
const comp=parseFloat(document.getElementById("g-comp").value)||1.0;
const body=scenarioBody(SCENARIO,mid,conf,comp);
try{const d=await api("/decisions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
const decision=d.decision||"—";const reasons=Array.isArray(d.block_reasons)?d.block_reasons:[];
if(d.id) LAST_DID=d.id; if(d.certificate_id) LAST_CERT=d.certificate_id;
let term="SCENARIO: "+SCENARIO+" · "+body.model_id+"\n";
if(d.dimensions){["Validity","Confidence","Risk","Compliance","Stability","Impact"].forEach(k=>{if(d.dimensions[k]!=null)term+="  "+k+" = "+Number(d.dimensions[k]).toFixed(3)+"\n";});}
term+="  Composite = "+(d.composite_eva!=null?d.composite_eva:"—")+"\n  Policy = "+(d.policy_enforced?"ENFORCED":"off")+"\n  → "+decision+"\n";
reasons.forEach(x=>{term+="  • "+x+"\n";});
const certBlock=d.certificate_id
  ?('<div style="margin-top:10px" class="row"><div class="f"><label>Certificate</label><input id="g-cert" class="mono" value="'+esc(d.certificate_id)+'"/></div>'+
    '<button class="btn cyan sm" type="button" onclick="gVerifyCert()">Verify cert</button>'+
    (d.id?'<button class="btn sm" type="button" onclick="gEvidence('+d.id+')">Evidence</button>':'')+
    '</div><div id="g-cert-out" class="muted" style="margin-top:8px;font-size:12px"></div>')
  :(d.id?'<div style="margin-top:10px"><button class="btn sm" type="button" onclick="gEvidence('+d.id+')">Evidence</button> <span id="g-cert-out" class="muted" style="font-size:12px"></span></div>':'');
out.innerHTML='<div class="panel"><h3>EVA Verdict · '+esc(SCENARIO)+'</h3><div class="verdict-big">'+statusTag(decision)+'</div>'+dimsHtml(d.dimensions)+
'<div class="term">'+esc(term)+'</div>'+certBlock+'</div>';
}catch(e){out.innerHTML='<div class="panel t-bad">'+esc(netErr(e))+'</div>';}}
async function gBatch(){
  const out=document.getElementById("g-out");
  const kpis=document.getElementById("g-batch-kpis");
  if(out)out.innerHTML='<div class="panel muted">Running Full EVA batch (fair · biased · high · sov)…</div>';
  const mid=(document.getElementById("g-mid")&&document.getElementById("g-mid").value.trim())||"model-001";
  const kinds=["fair","biased","high","sov"];
  const results=[];
  for(const k of kinds){
    try{
      const d=await api("/decisions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(scenarioBody(k,mid))});
      results.push({kind:k,ok:true,decision:d.decision,eva:d.composite_eva,policy:d.policy_enforced,id:d.id,cert:d.certificate_id,dims:d.dimensions,reasons:d.block_reasons ||[]});
      if(d.certificate_id) LAST_CERT=d.certificate_id;
      if(d.id) LAST_DID=d.id;
    }catch(e){results.push({kind:k,ok:false,decision:netErr(e)});}
  }
  const counts={APPROVE:0,BLOCK:0,ESCALATE:0,OTHER:0};
  results.forEach(r=>{const d=String(r.decision||"").toUpperCase();if(d==="APPROVE")counts.APPROVE++;else if(d==="BLOCK")counts.BLOCK++;else if(d==="ESCALATE")counts.ESCALATE++;else counts.OTHER++;});
  if(kpis)kpis.innerHTML='<div class="grid kpis" style="margin-top:12px">'+
    '<div class="kpi"><div class="k">Batch</div><div class="v cyan">'+results.filter(r=>r.ok).length+'/4</div></div>'+
    '<div class="kpi"><div class="k">APPROVE</div><div class="v green">'+counts.APPROVE+'</div></div>'+
    '<div class="kpi"><div class="k">BLOCK</div><div class="v red">'+counts.BLOCK+'</div></div>'+
    '<div class="kpi"><div class="k">ESCALATE</div><div class="v amber">'+counts.ESCALATE+'</div></div></div>';
  let term="FULL EVA BATCH · "+mid+"\n";
  results.forEach(r=>{
    term+="\n["+r.kind+"] → "+(r.decision||"?")+(r.eva!=null?" · EVA "+r.eva:"")+(r.policy?" · policy ENFORCED":"")+"\n";
    (r.reasons||[]).slice(0,3).forEach(x=>{term+="  • "+x+"\n";});
  });
  const last=results.filter(r=>r.ok).slice(-1)[0];
  if(out)out.innerHTML='<div class="panel"><h3>Batch terminal</h3><div class="term">'+esc(term)+'</div>'+
    (last&&last.dims?dimsHtml(last.dims):"")+
    (LAST_CERT?'<div style="margin-top:10px" class="row"><div class="f"><label>Last certificate</label><input id="g-cert" class="mono" value="'+esc(LAST_CERT)+'"/></div>'+
      '<button class="btn cyan sm" type="button" onclick="gVerifyCert()">Verify cert</button></div><div id="g-cert-out" class="muted" style="margin-top:8px;font-size:12px"></div>':"")+
    '</div>';
}
async function gVerifyCert(){
  const id=(document.getElementById("g-cert")&&document.getElementById("g-cert").value.trim())||LAST_CERT;
  const o=document.getElementById("g-cert-out"); if(!id){if(o)o.textContent="No certificate id";return;}
  if(o)o.textContent="Verifying…";
  try{const v=await api("/decisions/certificates/"+encodeURIComponent(id)+"/verify");
    if(o)o.innerHTML='<span class="'+(v.valid?'t-ok':'t-bad')+'">'+(v.valid?'VALID':'INVALID')+'</span> · '+esc(v.decision||"");
  }catch(e){if(o)o.innerHTML='<span class="t-bad">'+esc(netErr(e))+'</span>';}
}
async function gEvidence(id){
  const o=document.getElementById("g-cert-out"); if(o)o.textContent="Loading evidence…";
  try{const d=await api("/udoc/decisions/"+id+"/evidence");
    if(o)o.innerHTML='<div class="term" style="margin-top:6px">'+esc(JSON.stringify(d,null,2).slice(0,1200))+'</div>';
  }catch(e){if(o)o.innerHTML='<span class="t-bad">'+esc(netErr(e))+'</span>';}
}

async function vDecisions(m){await safe(m,async()=>{let rows=[],certs=[];try{rows=asArray(await api("/decisions"));}catch(e){}try{certs=asArray(await api("/decisions/certificates"));}catch(e){}
m.innerHTML='<div class="pgh"><h2>Decisions · EVA</h2><span class="desc">live ledger</span></div>'+
'<div class="panel"><button class="btn cyan sm" onclick="nav(\'govern\')">Run Govern batch</button></div>'+
'<div class="panel"><h3>Decisions · '+rows.length+'</h3>'+tableFrom(rows.slice(0,50),[
{h:"ID",r:x=>'<span class="mono">'+esc(x.id||x.decision_id)+'</span>'},{h:"System",r:x=>esc(x.model_id)},{h:"EVA",r:x=>esc(x.composite_eva)},{h:"Verdict",r:x=>statusTag(x.decision)}])+'</div>'+
'<div class="panel"><h3>Certificates · '+certs.length+'</h3>'+tableFrom(certs.slice(0,25),[
{h:"Cert",r:x=>'<span class="mono">'+esc(x.certificate_id||x.id)+'</span>'},{h:"Verdict",r:x=>statusTag(x.decision)},
{h:"",r:x=>{const cid=x.certificate_id||x.id;return cid?'<button class="btn sm" type="button" onclick="LAST_CERT=\''+esc(cid)+'\';nav(\'govern\');setTimeout(function(){var el=document.getElementById(\'g-cert\');if(el){el.value=\''+esc(cid)+'\';}gVerifyCert();},400)">Verify</button>':'';}}])+'</div>'+honesty();});}

async function vKnowledge(m){
  const who=JSON.parse(localStorage.getItem("udoc_client_who")||"{}");
  let st=null,docs=[],errMsg="";
  try{st=await api("/client/knowledge/state");}catch(e){errMsg=netErr(e);}
  try{if(!errMsg)docs=asArray(await api("/client/knowledge/docs"));}catch(e){if(!errMsg)errMsg=netErr(e);}
  const locked=/tenant-private|No tenant|403|Internal staff/i.test(errMsg);
  m.innerHTML='<div class="pgh"><h2>Company Knowledge</h2><span class="desc">Private tenant corpus · grounded ask · Neon-light text substrate</span></div>'+
    (errMsg?'<div class="panel t-bad"><b>'+(locked?'Tenant-private surface':'Error')+'</b><br>'+esc(errMsg)+
      (locked?'<br><span class="muted">Sign in as role <b>client</b> with a tenant_pk. Platform admin uses Core <code>/intel</code> — not this Client KB.</span>':'')+
      '</div>':'')+
    '<div class="grid kpis">'+
      '<div class="kpi"><div class="k">Your docs</div><div class="v cyan">'+(st&&st.docs!=null?st.docs:docs.length)+'</div></div>'+
      '<div class="kpi"><div class="k">Characters</div><div class="v">'+(st&&st.chars!=null?st.chars:"—")+'</div></div>'+
      '<div class="kpi"><div class="k">Scope</div><div class="v" style="font-size:14px">'+(st&&st.tenant_scoped?'TENANT':'—')+'</div></div>'+
      '<div class="kpi"><div class="k">Account</div><div class="v" style="font-size:12px">'+esc(who.role||"?")+'</div></div></div>'+
    '<div class="panel"><h3>Private intelligence · how it works</h3>'+
      '<div class="sov-ok">Each client tenant only sees rows with their tenant_pk</div>'+
      '<div class="sov-ok">Ask answers cite only your active documents</div>'+
      '<div class="sov-ok">Shared UDOC host · private KB rows · not a second Neon per client</div>'+
      '<div class="muted" style="font-size:12px;margin-top:8px">'+esc(st&&st.note?st.note:"Upload SOPs, policies, and company text. Grounded retrieval — not open-web chat.")+'</div></div>'+
    '<div class="panel"><h3>Ask your corpus</h3>'+
      '<div class="row"><div class="f"><input id="kb-q" placeholder="Question using terms from your documents"/></div>'+
      '<button class="btn cyan" onclick="kbAsk()" '+(errMsg?'disabled':'')+'>Ask</button></div>'+
      '<div id="kb-ans" style="margin-top:10px"></div></div>'+
    '<div class="panel"><h3>Add text (preferred · Neon-light)</h3>'+
      '<label>Title</label><input id="kb-t" placeholder="e.g. Leave policy 2026"/>'+
      '<label>Category</label><select id="kb-cat"><option>GENERAL</option><option>POLICY</option><option>SOP</option><option>LEGAL</option><option>HR</option><option>PRODUCT</option></select>'+
      '<label>Text</label><textarea id="kb-text" rows="4" style="width:100%;background:#091022;border:1px solid var(--bd);color:var(--txt);border-radius:8px;padding:10px;font:inherit" placeholder="Paste company material…"></textarea>'+
      '<div style="margin-top:8px"><button class="btn" onclick="kbIngest()" '+(errMsg?'disabled':'')+'>Add to private KB</button> <span id="kb-msg" class="muted"></span></div></div>'+
    '<div class="panel"><h3>Upload file (PDF · DOCX · TXT · max 25MB)</h3>'+
      '<input type="file" id="kb-file" accept=".pdf,.docx,.txt,.md"/>'+
      '<div style="margin-top:8px"><button class="btn cyan" onclick="kbUpload()" '+(errMsg?'disabled':'')+'>Upload into private KB</button> <span id="kb-up-msg" class="muted"></span></div>'+
      '<div class="muted" style="font-size:11px;margin-top:8px">Large archives stay off free Neon — prefer short policy extracts.</div></div>'+
    '<div class="panel"><h3>Documents in your tenant · '+docs.length+'</h3>'+
      (docs.length?tableFrom(docs.slice(0,40),[{
        h:"Title",r:x=>'<b>'+esc(x.title)+'</b><br><span class="mono muted" style="font-size:10px">'+esc(x.category||"")+' · '+esc(x.source||"")+'</span>'},
        {h:"Chars",r:x=>esc(x.char_len)},
        {h:"Active",r:x=>statusTag(x.active?"ACTIVE":"OFF")},
        {h:"",r:x=>'<button class="btn sm" onclick="kbDelete('+x.id+')">remove</button>'}]):
        '<div class="muted">Empty — add text or upload a small document to start your private substrate.</div>')+
    '</div>'+honesty();
}
async function kbAsk(){const a=document.getElementById("kb-ans");const q=document.getElementById("kb-q").value.trim();if(!q)return;a.innerHTML='<span class="muted">…</span>';
try{const r=await api("/client/knowledge/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({query:q})});
  let html='<div class="note">'+esc(r.answer||"")+'</div>';
  if(r.coverage!=null)html+='<div class="muted" style="font-size:11px;margin-top:6px">coverage '+esc(r.coverage)+(r.blocked?' · blocked':'')+'</div>';
  if(r.citations&&r.citations.length){
    html+='<table style="margin-top:8px"><thead><tr><th>Source</th><th>Snippet</th></tr></thead><tbody>'+
      r.citations.map(c=>'<tr><td>'+esc(c.title)+'<br><span class="mono muted" style="font-size:10px">#'+esc(c.doc_id)+' · '+esc(c.category||"")+'</span></td><td style="font-size:12px">'+esc(c.snippet||"")+'</td></tr>').join('')+
      '</tbody></table>';
  }
  a.innerHTML=html;
}catch(e){a.innerHTML='<span class="t-bad">'+esc(netErr(e))+'</span>';}}
async function kbIngest(){const mg=document.getElementById("kb-msg");const body={title:document.getElementById("kb-t").value.trim(),text:document.getElementById("kb-text").value,category:(document.getElementById("kb-cat")&&document.getElementById("kb-cat").value)||"GENERAL"};
if(!body.title||!body.text){mg.textContent="Title and text required";return;}mg.textContent="Saving…";
try{await api("/client/knowledge/ingest-text",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});nav("knowledge");}catch(e){mg.textContent=netErr(e);}}
async function kbUpload(){const mg=document.getElementById("kb-up-msg");const f=document.getElementById("kb-file");const file=f&&f.files&&f.files[0];if(!file){mg.textContent="Choose a file";return;}
mg.textContent="Uploading…";
try{const fd=new FormData();fd.append("file",file);fd.append("title",file.name);fd.append("category","GENERAL");
  const h={};if(token())h.Authorization="Bearer "+token();
  const r=await fetch(apiBase()+"/client/knowledge/ingest",{method:"POST",headers:h,body:fd});
  const ct=r.headers.get("content-type")||"";const body=ct.includes("json")?await r.json().catch(()=>null):await r.text();
  if(!r.ok)throw new Error((body&&body.detail)||("HTTP "+r.status));
  nav("knowledge");
}catch(e){mg.textContent=netErr(e);}}
async function kbDelete(id){try{await api("/client/knowledge/docs/"+id,{method:"DELETE"});nav("knowledge");}catch(e){alert(netErr(e));}}

async function vSettings(m){await safe(m,async()=>{let plan={},keys=[];try{plan=await api("/tenants/me");}catch(e){}try{keys=asArray(await api("/tenants/me/apikeys"));}catch(e){}
const rows=Object.entries(plan||{}).filter(([k,v])=>typeof v!=="object").map(([k,v])=>'<tr><td class="muted">'+esc(k)+'</td><td class="mono">'+esc(v)+'</td></tr>');
m.innerHTML='<div class="pgh"><h2>Plan & API Keys</h2></div><div class="panel"><h3>Subscription</h3>'+(rows.length?'<table><tbody>'+rows.join('')+'</tbody></table>':'<div class="muted">No plan data</div>')+'</div>'+
'<div class="panel"><h3>Keys · '+keys.length+'</h3>'+tableFrom(keys,[{h:"Key",r:x=>esc(x.label||x.prefix||x.id)},{h:"Status",r:x=>statusTag(x.status||"active")}])+'</div>'+honesty();});}

if(token()){try{enterApp();}catch(e){logout();}}
