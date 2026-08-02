/* Client Company Knowledge density — empty-state + demo proof chips */
(function(){
"use strict";
async function vKnowledge(m){
  const who=JSON.parse(localStorage.getItem("udoc_client_who")||"{}");
  let st=null,docs=[],errMsg="";
  try{st=await api("/client/knowledge/state");}catch(e){errMsg=netErr(e);}
  try{if(!errMsg)docs=asArray(await api("/client/knowledge/docs"));}catch(e){if(!errMsg)errMsg=netErr(e);}
  const locked=/tenant-private|No tenant|403|Internal staff/i.test(errMsg);
  const nDocs=st&&st.docs!=null?st.docs:docs.length;
  const empty=!errMsg && nDocs===0;
  m.innerHTML='<div class="pgh"><h2>Company Knowledge</h2><span class="desc">Private tenant corpus · grounded ask · Neon-light text substrate · not GODS /intel</span></div>'+
    (errMsg?'<div class="panel t-bad"><b>'+(locked?'Tenant-private surface':'Error')+'</b><br>'+esc(errMsg)+
      (locked?'<br><span class="muted">Sign in as role <b>client</b> with a tenant_pk. Platform admin uses Core <code>/intel</code> — not this Client KB.</span>':'')+
      '</div>':'')+
    '<div class="grid kpis">'+
      '<div class="kpi"><div class="k">Your docs</div><div class="v cyan">'+nDocs+'</div></div>'+
      '<div class="kpi"><div class="k">Characters</div><div class="v">'+(st&&st.chars!=null?st.chars:"—")+'</div></div>'+
      '<div class="kpi"><div class="k">Scope</div><div class="v" style="font-size:14px">'+(st&&st.tenant_scoped?'TENANT':'—')+'</div></div>'+
      '<div class="kpi"><div class="k">Account</div><div class="v" style="font-size:12px">'+esc(who.role||"?")+(who.tenant_id?(' · '+esc(who.tenant_id)):'')+'</div></div></div>'+
    (empty?'<div class="panel" style="border-left:3px solid var(--amber,#F59E0B)"><h3>Empty corpus · expected until you ingest</h3>'+
      '<div class="muted small">Grounded ask returns “not in knowledge base” when you have zero documents. '+
      'Paste a short SOP below (or use Capstone seed after Core redeploy). Full Google Drive portfolios stay offline — Neon holds extracts only.</div>'+
      '<div class="small" style="margin-top:8px">Demo login: <span class="mono">client@udoc.demo</span> · seed Leave SOP + POPIA note when Core bootstrap has run.</div></div>':'')+
    (!errMsg&&nDocs>0?'<div class="panel" style="border-left:3px solid #10B981"><h3>Demo proof · seed live</h3>'+
      '<div class="small">Try: <button class="btn sm cyan" type="button" onclick="kbQuickAsk(\'leave advance notice working days\')">Leave notice?</button> '+
      '<button class="btn sm" type="button" onclick="kbQuickAsk(\'POPIA automated decision human intervention\')">POPIA safeguards?</button></div>'+
      '<div class="muted small" style="margin-top:6px">Expected: grounded citations from your tenant docs only — not Internal GODS archive.</div></div>':'')+
    '<div class="panel"><h3>Private intelligence · how it works</h3>'+
      '<div class="sov-ok">Each client tenant only sees rows with their tenant_pk</div>'+
      '<div class="sov-ok">Ask answers cite only your active documents</div>'+
      '<div class="sov-ok">Shared UDOC host · private KB rows · not a second Neon per client</div>'+
      '<div class="sov-ok">Internal GODS Intelligence (/intel) is a different table — staff only</div>'+
      '<div class="muted" style="font-size:12px;margin-top:8px">'+esc(st&&st.note?st.note:"Upload SOPs, policies, and company text. Grounded retrieval — not open-web chat.")+'</div></div>'+
    '<div class="panel"><h3>Ask your corpus</h3>'+
      '<div class="row"><div class="f"><input id="kb-q" placeholder="Question using terms from your documents"/></div>'+
      '<button class="btn cyan" onclick="kbAsk()" '+(errMsg?'disabled':'')+'>Ask</button></div>'+
      '<div id="kb-ans" style="margin-top:10px"></div></div>'+
    '<div class="panel"><h3>Add text (preferred · Neon-light)</h3>'+
      '<label>Title</label><input id="kb-t" placeholder="e.g. Leave policy 2026"/>'+
      '<label>Category</label><select id="kb-cat"><option>SOP</option><option>POLICY</option><option>GENERAL</option><option>HR</option><option>COMPLIANCE</option></select>'+
      '<label>Text</label><textarea id="kb-text" rows="4" style="width:100%;background:#091022;border:1px solid var(--bd);color:var(--txt);border-radius:8px;padding:10px;font:inherit" placeholder="Paste company material (short extract)…"></textarea>'+
      '<div style="margin-top:8px"><button class="btn" onclick="kbIngest()" '+(errMsg?'disabled':'')+'>Add to private KB</button> <span id="kb-msg" class="muted"></span></div></div>'+
    '<div class="panel"><h3>Upload file (PDF/DOCX/TXT · 25MB cap · text extracted)</h3>'+
      '<input type="file" id="kb-file" accept=".pdf,.docx,.txt,.md"/> '+
      '<button class="btn sm" onclick="kbUpload()" '+(errMsg?'disabled':'')+'>Upload</button> <span id="kb-up-msg" class="muted"></span></div>'+
    '<div class="panel"><h3>Your documents · '+docs.length+'</h3>'+
      (docs.length?tableFrom(docs.slice(0,80),[
        {h:"Title",r:x=>'<b>'+esc(x.title||"—")+'</b>'},
        {h:"Category",r:x=>esc(x.category||"—")},
        {h:"Chars",r:x=>esc(x.char_len!=null?x.char_len:"—")},
        {h:"",r:x=>'<button class="btn sm" onclick="kbDelete('+Number(x.id)+')">Remove</button>'},
      ]):'<div class="muted small">No documents yet. Add text above.</div>')+'</div>'+honesty();
}
function kbQuickAsk(q){
  const el=document.getElementById("kb-q"); if(el) el.value=q;
  kbAsk();
}
async function kbAsk(){
  const a=document.getElementById("kb-ans"); if(!a) return;
  const q=(document.getElementById("kb-q")&&document.getElementById("kb-q").value||"").trim();
  if(!q){a.innerHTML='<span class="muted">Enter a question that uses words from your documents.</span>';return;}
  a.innerHTML='<span class="muted">…</span>';
  try{
    const d=await api("/client/knowledge/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({query:q})});
    let html='<div style="white-space:pre-wrap;font-size:13px">'+esc(d.answer||d.response||JSON.stringify(d))+'</div>';
    if(d.blocked) html='<span class="t-bad">[BLOCKED]</span> '+html;
    if(d.citations&&d.citations.length){
      html+='<table style="margin-top:10px"><thead><tr><th>Citation</th><th>Snippet</th></tr></thead><tbody>'+
        d.citations.map(c=>'<tr><td><b>'+esc(c.title||"")+'</b><br><span class="mono muted" style="font-size:10px">#'+esc(c.doc_id||c.id||"")+' · '+esc(c.category||"")+'</span></td><td style="font-size:12px">'+esc(c.snippet||"")+'</td></tr>').join('')+
        '</tbody></table>';
    }
    if(d.coverage===0||/(not in|unable to find|empty|no document)/i.test(String(d.answer||""))){
      html+='<div class="muted small" style="margin-top:8px">Empty or no match: add a short extract that contains the words you are asking about. Internal GODS archive is not searched from this Client surface.</div>';
    }
    a.innerHTML=html;
  }catch(e){a.innerHTML='<span class="t-bad">'+esc(netErr(e))+'</span>';}
}
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
})();
