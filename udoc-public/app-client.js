const PROD_API="https://gods-platform-core.onrender.com";
let SCENARIO="fair",SECTOR=null;
function apiBase(){return localStorage.getItem("udoc_client_api")||PROD_API;}
function setApiBase(v){localStorage.setItem("udoc_client_api",v.replace(/\/+$/,""));}
function token(){return localStorage.getItem("udoc_client_tok")||"";}
function esc(s){return String(s==null?"":s).replace(/&/g,"&").replace(/</g,"<").replace(/>/g,">").replace(/\"/g,""");}
async function api(path,opts={}){const h=Object.assign({},opts.headers||{});if(token())h.Authorization="Bearer "+token();
const r=await fetch(apiBase()+path,Object.assign({},opts,{headers:h}));
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
localStorage.setItem("udoc_client_who",JSON.stringify({email:document.getElementById("li-email").value.trim().toLowerCase(),role:d.role,tenant_id:d.tenant_id}));enterApp();
}catch(err){e.textContent=err.message;}finally{btn.disabled=false;btn.textContent="Sign in";}}
function logout(){localStorage.removeItem("udoc_client_tok");document.getElementById("app").style.display="none";document.getElementById("login").style.display="flex";}
async function enterApp(){const w=JSON.parse(localStorage.getItem("udoc_client_who")||"{}");
document.getElementById("login").style.display="none";document.getElementById("app").style.display="grid";
document.getElementById("who-email").textContent=w.email||"—";document.getElementById("who-tenant").textContent=w.tenant_id||"";
heartbeat();try{SECTOR=await api("/sector/profile");}catch(e){}nav("dash");}
async function heartbeat(){const el=document.getElementById("hb");try{await fetch(apiBase()+"/health");el.textContent="· online";el.className="pill up";}catch{el.textContent="· offline";el.className="pill down";}}
function nav(v){if(v==="sentinel"){window.open(apiBase()+"/Sentinel","_blank");return;}
document.querySelectorAll("#nav .navitem").forEach(n=>n.classList.toggle("active",n.dataset.view===v));
const m=document.getElementById("main");m.innerHTML='<div class="loading">Loading…</div>';
({dash:vDash,systems:vSystems,compliance:vCompliance,audit:vAudit,bias:vBias,sovereignty:vSov,govern:vGovern,decisions:vDecisions,knowledge:vKnowledge,settings:vSettings}[v]||vDash)(m);}
document.querySelectorAll("#nav .navitem").forEach(n=>n.addEventListener("click",()=>nav(n.dataset.view)));
function asArray(d){if(Array.isArray(d))return d;if(d&&typeof d==="object"){for(const k of["items","models","results","data","keys"])if(Array.isArray(d[k]))return d[k];}return [];}
function riskTag(v){v=String(v||"").toUpperCase();const c=/HIGH|CRIT|UNACCEPTABLE/.test(v)?"t-bad":(/MEDIUM|NOTABLE/.test(v)?"t-warn":"t-ok");return '<span class="tag2 '+c+'">'+esc(v||"—")+'</span>';}
function statusTag(v){const u=String(v||"").toUpperCase();const c=/ACTIVE|APPROVE|VALID|VERIFIED/.test(u)?"t-ok":(/PEND|REVIEW/.test(u)?"t-warn":(/BLOCK|DENIED|INVALID/.test(u)?"t-bad":"t-info"));return '<span class="tag2 '+c+'">'+esc(v||"—")+'</span>';}
function tableFrom(rows,cols){if(!rows.length)return'<div class="muted">No records.</div>';let h='<table><thead><tr>'+cols.map(c=>'<th>'+esc(c.h)+'</th>').join('')+'</tr></thead><tbody>';
rows.forEach(r=>{h+='<tr>'+cols.map(c=>'<td>'+(c.r?c.r(r):esc(r[c.k]))+'</td>').join('')+'</tr>';});return h+'</tbody></table>';}
async function safe(host,fn){try{return await fn();}catch(e){host.innerHTML='<div class="panel t-bad">'+esc(e.message)+'</div>';}}
function dimsHtml(dims){if(!dims||typeof dims!=="object")return"";const order=["Validity","Confidence","Risk","Compliance","Stability","Impact"];
const keys=order.filter(k=>dims[k]!=null).concat(Object.keys(dims).filter(k=>!order.includes(k)));
return'<div class="dims">'+keys.map(k=>{const v=Number(dims[k]);const pct=isNaN(v)?0:Math.min(100,Math.max(0,(v<=1?v*100:v*10)));
return'<div class="dim"><div class="dk">'+esc(k)+'</div><div class="dv">'+(isNaN(v)?"—":(v<=1?v.toFixed(2):v))+'</div><div class="bar"><i style="width:'+pct+'%"></i></div></div>';}).join('')+'</div>';}
function honesty(){return'<div class="note">Pre-registration · GG54477 withdrawn · POPIA s71 + Constitution · Neon ≤500MB · Netlify mvp-1/mvp-2 acceptance path.</div>';}

async function vDash(m){let sys=[],dec=[],ready=null,ex={},certs=[];
try{sys=asArray(await api("/registry/models"));}catch(e){}
try{dec=asArray(await api("/decisions"));}catch(e){}
try{ready=await api("/udoc/demo/ready");}catch(e){}
try{ex=await api("/udoc/exchange");}catch(e){}
try{certs=asArray(await api("/decisions/certificates"));}catch(e){}
const ap=dec.filter(d=>/APPROVE/i.test(String(d.decision||""))).length;
const bl=dec.filter(d=>/BLOCK|ESCALATE/i.test(String(d.decision||""))).length;
const card=(k,v,c)=>'<div class="kpi"><div class="k">'+esc(k)+'</div><div class="v '+(c||'')+'">'+esc(v)+'</div></div>';
m.innerHTML='<div class="pgh"><h2>Command Dashboard</h2><span class="desc">mvp-1 International Standards · live</span></div>'+
'<div class="panel"><h3>Boot</h3><div>'+(ready&&ready.ready?'<span class="t-ok">READY</span> · rules '+esc(ready.active_rules):'<span class="t-bad">SEED PENDING</span>')+' · <span class="mono">model-001</span></div></div>'+
'<div class="grid kpis">'+card("AI systems",sys.length,"cyan")+card("Decisions",dec.length)+card("APPROVE",ap,"green")+card("BLOCK / ESC",bl,"amber")+card("Certs",certs.length,"cyan")+'</div>'+
'<div class="grid" style="grid-template-columns:1fr 1fr;gap:12px">'+
'<div class="panel" style="margin:0"><h3>Sovereignty</h3><div class="sov-ok">ZA · '+esc(ex.jurisdiction||"ZA")+'</div><div class="sov-ok">Localisation rules · '+esc(ex.rules_active!=null?ex.rules_active:"—")+'</div><div class="sov-ok">Fail-closed path</div></div>'+
'<div class="panel" style="margin:0"><h3>Quick</h3><button class="btn cyan sm" onclick="nav(\'govern\')">Govern · EVA</button> <button class="btn sm" onclick="nav(\'compliance\')">Compliance</button></div></div>'+honesty();}

async function vSystems(m){await safe(m,async()=>{const rows=asArray(await api("/registry/models"));
m.innerHTML='<div class="pgh"><h2>AI Registry</h2><span class="desc">mvp-1</span></div><div class="panel"><h3>Registered · '+rows.length+'</h3>'+tableFrom(rows,[
{h:"System",r:x=>'<b>'+esc(x.name||x.model_id)+'</b><br><span class="mono muted" style="font-size:11px">'+esc(x.model_id)+'</span>'},
{h:"Risk",r:x=>riskTag(x.risk_tier)},{h:"Status",r:x=>statusTag(x.status)}])+'</div>'+honesty();});}

async function vCompliance(m){await safe(m,async()=>{let sfw={frameworks:[]},active={},ready=null;
try{sfw=await api("/sector/frameworks");}catch(e){}try{active=await api("/policy/active");}catch(e){}try{ready=await api("/udoc/demo/ready");}catch(e){}
const defaults=[{name:"POPIA s71",basis:"POPIA",focus:"Automated decisions"},{name:"Constitution ss 9/14/33",basis:"Bill of Rights",focus:"Equality · privacy · PAJA"},
{name:"National AI Policy Framework 2024",basis:"Standing SA instrument",focus:"GG54477 withdrawn"},
{name:"EU AI Act risk tiers",basis:"Intl",focus:"Risk classification"},{name:"NIST AI RMF",basis:"Govern-Map-Measure-Manage",focus:"Lifecycle"},
{name:"ISO/IEC 42001:2023",basis:"AIMS",focus:"Organisation controls"}];
const fws=(sfw.frameworks&&sfw.frameworks.length)?sfw.frameworks:defaults;
const cards=fws.map((f,i)=>{const pct=55+(i*9)%40;return'<div class="panel" style="margin:0;border-left:3px solid var(--gold)"><h3 style="text-transform:none;letter-spacing:0;color:var(--txt);font-size:13px">'+esc(f.name)+'</h3><div class="mono" style="font-size:10px;color:var(--cyan)">'+esc(f.basis||"")+'</div><div class="muted" style="font-size:12px;margin-top:6px">'+esc(f.focus||"")+'</div><div class="covbar"><i style="width:'+pct+'%"></i></div></div>';}).join('');
m.innerHTML='<div class="pgh"><h2>Multi-Framework Compliance</h2><span class="desc">mvp-2</span></div>'+
'<div class="grid kpis"><div class="kpi"><div class="k">Frameworks</div><div class="v cyan">'+fws.length+'</div></div><div class="kpi"><div class="k">Policy rules</div><div class="v">'+(active.enforced_rules!=null?active.enforced_rules:"—")+'</div></div><div class="kpi"><div class="k">Seed</div><div class="v" style="font-size:16px">'+(ready&&ready.ready?"READY":"WAIT")+'</div></div></div>'+
'<div class="panel"><button class="btn cyan" onclick="runSweep(this)">Run compliance sweep</button> <span id="sweep-res" class="muted" style="font-size:12px"></span></div>'+
'<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px">'+cards+'</div>'+honesty();});}
async function runSweep(btn){btn.disabled=true;const r=document.getElementById("sweep-res");if(r)r.textContent="running…";
try{const d=await api("/compliance/sweep",{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"});if(r)r.textContent="done · "+esc(JSON.stringify(d).slice(0,120));}
catch(e){if(r)r.textContent=e.message;}finally{btn.disabled=false;}}

async function vAudit(m){await safe(m,async()=>{const rows=asArray(await api("/decisions"));
m.innerHTML='<div class="pgh"><h2>Audit Trail</h2><span class="desc">mvp-1</span></div><div class="panel"><h3>Recent · '+rows.length+'</h3>'+tableFrom(rows.slice(0,50),[
{h:"ID",r:x=>'<span class="mono">'+esc(x.id)+'</span>'},{h:"System",r:x=>esc(x.model_id)},{h:"Verdict",r:x=>statusTag(x.decision)},
{h:"EVA",r:x=>'<b style="color:var(--gold-l)">'+esc(x.composite_eva!=null?x.composite_eva:"—")+'</b>'},{h:"ms",r:x=>esc(x.latency_ms)}])+'</div>'+honesty();});}

async function vBias(m){await safe(m,async()=>{let sum={},inc={};try{sum=await api("/udoc/regulator/summary");}catch(e){}try{inc=await api("/udoc/incidents");}catch(e){}
const oc=(sum.decisions&&sum.decisions.by_outcome)||{};const incidents=inc.incidents||[];
m.innerHTML='<div class="pgh"><h2>Bias Monitor</h2><span class="desc">mvp-1</span></div>'+
'<div class="grid kpis"><div class="kpi"><div class="k">BLOCK</div><div class="v red">'+(oc.BLOCK||0)+'</div></div><div class="kpi"><div class="k">ESCALATE</div><div class="v amber">'+(oc.ESCALATE||0)+'</div></div><div class="kpi"><div class="k">Incidents</div><div class="v">'+incidents.length+'</div></div></div>'+
'<div class="panel"><h3>Feed</h3>'+(incidents.length?tableFrom(incidents.slice(0,15),[{h:"Decision",r:x=>esc(x.decision_id)},{h:"Model",r:x=>esc(x.model_id)},{h:"Severity",r:x=>statusTag(x.severity)},{h:"Reasons",r:x=>esc(x.reasons)}]):'<div class="muted">None yet — run Biased on Govern.</div>')+'</div>'+
'<div class="panel"><button class="btn cyan sm" onclick="nav(\'govern\')">Govern · Biased test</button></div>'+honesty();});}

async function vSov(m){await safe(m,async()=>{let ex={},ready={};try{ex=await api("/udoc/exchange");}catch(e){}try{ready=await api("/udoc/demo/ready");}catch(e){}
m.innerHTML='<div class="pgh"><h2>Sovereignty</h2><span class="desc">mvp-1/2</span></div>'+
'<div class="grid kpis"><div class="kpi"><div class="k">Jurisdiction</div><div class="v cyan">'+esc(ex.jurisdiction||"ZA")+'</div></div><div class="kpi"><div class="k">Rules</div><div class="v">'+(ex.rules_active!=null?ex.rules_active:"—")+'</div></div><div class="kpi"><div class="k">Seed</div><div class="v" style="font-size:16px">'+(ready.ready?"OK":"WAIT")+'</div></div></div>'+
'<div class="panel"><h3>Guarantees</h3><div class="sov-ok">South African jurisdiction</div><div class="sov-ok">Fail-closed when model/policy missing</div><div class="sov-ok">Policy-to-code on decisions</div><div class="term">'+esc(ex.basis||"")+' · '+esc(ex.cross_border_transfer||"")+'</div></div>'+honesty();});}

async function vGovern(m){await safe(m,async()=>{let models=asArray(await api("/registry/models").catch(()=>[]));let ready=null;try{ready=await api("/udoc/demo/ready");}catch(e){}
const mid0=(models.find(x=>x.model_id==="model-001")||models[0]||{}).model_id||"model-001";
m.innerHTML='<div class="pgh"><h2>Govern · EVA</h2><span class="desc">'+(ready&&ready.ready?'<span class="t-ok">demo ready</span>':'<span class="t-bad">seed pending</span>')+'</span></div>'+
'<div class="panel"><h3>Scenario</h3><div class="scenarios">'+
'<span class="chip active" onclick="gScenario(this,\'fair\')">Fair</span><span class="chip" onclick="gScenario(this,\'biased\')">Biased → BLOCK</span>'+
'<span class="chip" onclick="gScenario(this,\'high\')">High-risk</span><span class="chip" onclick="gScenario(this,\'sov\')">Sovereignty</span></div>'+
'<div class="row"><div class="f"><label>Model</label><input id="g-mid" value="'+esc(mid0)+'"/></div>'+
'<div class="f"><label>Confidence</label><input id="g-conf" value="0.92"/></div>'+
'<div class="f"><label>Compliance</label><input id="g-comp" value="1.0"/></div></div>'+
'<div style="margin-top:12px"><button class="btn" onclick="gEvaluate()">Evaluate · EVA</button></div></div><div id="g-out"></div>'+honesty();});}
function gScenario(el,kind){SCENARIO=kind;document.querySelectorAll('.scenarios .chip').forEach(c=>c.classList.remove('active'));if(el)el.classList.add('active');gEvaluate();}
async function gEvaluate(){const out=document.getElementById("g-out");out.innerHTML='<div class="panel muted">Evaluating…</div>';
const body={model_id:document.getElementById("g-mid").value.trim(),raw_confidence:parseFloat(document.getElementById("g-conf").value)||0.9,compliance:parseFloat(document.getElementById("g-comp").value)||1.0};
if(SCENARIO==="biased"){body.priv_favorable=900;body.priv_total=1000;body.unpriv_favorable=120;body.unpriv_total=1000;}
if(SCENARIO==="high")body.risk_tier="HIGH";
if(SCENARIO==="sov"){body.bgp=0.4;body.traceroute=0.5;body.dnssec=0.6;body.storage=0.7;}
try{const d=await api("/decisions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
const decision=d.decision||"—";const reasons=Array.isArray(d.block_reasons)?d.block_reasons:[];
let term="SCENARIO: "+SCENARIO+" · "+body.model_id+"\n";
if(d.dimensions){["Validity","Confidence","Risk","Compliance","Stability","Impact"].forEach(k=>{if(d.dimensions[k]!=null)term+="  "+k+" = "+Number(d.dimensions[k]).toFixed(3)+"\n";});}
term+="  Composite = "+(d.composite_eva!=null?d.composite_eva:"—")+"\n  Policy = "+(d.policy_enforced?"ENFORCED":"off")+"\n  → "+decision+"\n";
reasons.forEach(x=>{term+="  • "+x+"\n";});
out.innerHTML='<div class="panel"><h3>EVA Verdict</h3><div class="verdict-big">'+statusTag(decision)+'</div>'+dimsHtml(d.dimensions)+
'<div class="term">'+esc(term)+'</div>'+(d.certificate_id?'<div style="margin-top:8px" class="mono">'+esc(d.certificate_id)+'</div>':'')+'</div>';
}catch(e){out.innerHTML='<div class="panel t-bad">'+esc(e.message)+'</div>';}}

async function vDecisions(m){await safe(m,async()=>{let rows=[],certs=[];try{rows=asArray(await api("/decisions"));}catch(e){}try{certs=asArray(await api("/decisions/certificates"));}catch(e){}
m.innerHTML='<div class="pgh"><h2>Decisions · EVA</h2></div><div class="panel"><h3>Decisions · '+rows.length+'</h3>'+tableFrom(rows.slice(0,50),[
{h:"ID",r:x=>'<span class="mono">'+esc(x.id)+'</span>'},{h:"System",r:x=>esc(x.model_id)},{h:"EVA",r:x=>esc(x.composite_eva)},{h:"Verdict",r:x=>statusTag(x.decision)}])+'</div>'+
'<div class="panel"><h3>Certificates · '+certs.length+'</h3>'+tableFrom(certs.slice(0,25),[
{h:"Cert",r:x=>'<span class="mono">'+esc(x.certificate_id||x.id)+'</span>'},{h:"Verdict",r:x=>statusTag(x.decision)}])+'</div>'+honesty();});}

async function vKnowledge(m){await safe(m,async()=>{let st={},docs=[];try{st=await api("/client/knowledge/state");}catch(e){}try{docs=asArray(await api("/client/knowledge/docs"));}catch(e){}
m.innerHTML='<div class="pgh"><h2>Company Knowledge</h2><span class="desc">Text only · Neon-light</span></div>'+
'<div class="grid kpis"><div class="kpi"><div class="k">Docs</div><div class="v cyan">'+(st.docs!=null?st.docs:docs.length)+'</div></div></div>'+
'<div class="panel"><h3>Ask</h3><div class="row"><div class="f"><input id="kb-q" placeholder="query"/></div><button class="btn cyan" onclick="kbAsk()">Ask</button></div><div id="kb-ans" style="margin-top:8px"></div></div>'+
'<div class="panel"><h3>Add text</h3><label>Title</label><input id="kb-t"/><label>Text</label><textarea id="kb-text" rows="3" style="width:100%;background:#091022;border:1px solid var(--bd);color:var(--txt);border-radius:8px;padding:10px;font:inherit"></textarea>'+
'<div style="margin-top:8px"><button class="btn" onclick="kbIngest()">Add</button> <span id="kb-msg" class="muted"></span></div></div>'+
'<div class="panel"><h3>Documents</h3>'+tableFrom(docs.slice(0,20),[{h:"Title",r:x=>esc(x.title)},{h:"Chars",r:x=>esc(x.char_len)},{h:"",r:x=>'<button class="btn sm" onclick="kbDelete('+x.id+')">remove</button>'}])+'</div>'+honesty();});}
async function kbAsk(){const a=document.getElementById("kb-ans");const q=document.getElementById("kb-q").value.trim();if(!q)return;a.textContent="…";
try{const r=await api("/client/knowledge/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({query:q})});a.innerHTML='<div class="note">'+esc(r.answer||"")+'</div>';}catch(e){a.textContent=e.message;}}
async function kbIngest(){const mg=document.getElementById("kb-msg");const body={title:document.getElementById("kb-t").value.trim(),text:document.getElementById("kb-text").value,category:"GENERAL"};
if(!body.title||!body.text){mg.textContent="Required";return;}mg.textContent="…";
try{await api("/client/knowledge/ingest-text",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});nav("knowledge");}catch(e){mg.textContent=e.message;}}
async function kbDelete(id){try{await api("/client/knowledge/docs/"+id,{method:"DELETE"});nav("knowledge");}catch(e){alert(e.message);}}

async function vSettings(m){await safe(m,async()=>{let plan={},keys=[];try{plan=await api("/tenants/me");}catch(e){}try{keys=asArray(await api("/tenants/me/apikeys"));}catch(e){}
const rows=Object.entries(plan||{}).filter(([k,v])=>typeof v!=="object").map(([k,v])=>'<tr><td class="muted">'+esc(k)+'</td><td class="mono">'+esc(v)+'</td></tr>');
m.innerHTML='<div class="pgh"><h2>Plan & API Keys</h2></div><div class="panel"><h3>Subscription</h3>'+(rows.length?'<table><tbody>'+rows.join('')+'</tbody></table>':'<div class="muted">No plan data</div>')+'</div>'+
'<div class="panel"><h3>Keys · '+keys.length+'</h3>'+tableFrom(keys,[{h:"Key",r:x=>esc(x.label||x.prefix||x.id)},{h:"Status",r:x=>statusTag(x.status||"active")}])+'</div>'+honesty();});}

if(token()){try{enterApp();}catch(e){logout();}}
