import { useEffect, useState } from "react";
import { api } from "../api";
export function Overview(){
  const [s,setS]=useState<any>(null); const [loop,setLoop]=useState<any>(null);
  const [chain,setChain]=useState<any>(null); const [sov,setSov]=useState<any>(null);
  const [bias,setBias]=useState<any>(null); const [audit,setAudit]=useState<any[]>([]);
  async function load(){
    api.get("/admin/status").then(setS).catch(()=>{});
    api.get("/intelligence/loop-snapshot").then(setLoop).catch(()=>{});
    api.get("/audit/chain/verify").then(setChain).catch(()=>{});
    api.get("/sovereignty/posture").then(setSov).catch(()=>{});
    api.get("/bias/scan").then(setBias).catch(()=>{});
    api.get("/audit/records").then(setAudit).catch(()=>{});
  }
  useEffect(()=>{ load(); const t=setInterval(load,8000); return ()=>clearInterval(t); },[]);
  const sovPct = sov ? (sov.sovereign_rate*100).toFixed(0)+"%" : "—";
  return (<><div className="top"><h2>Holdings Overview</h2><span className="badge">🔒 INTERNAL · LIVE</span></div>
    <div className="grid">
      <div className="card"><h3>Models Governed</h3><div className="metric">{s?.models??"—"}</div></div>
      <div className="card"><h3>Decisions</h3><div className="metric">{s?.decisions??"—"}</div></div>
      <div className="card"><h3>Open Oversight</h3><div className="metric">{s?.open_oversight??"—"}</div></div>
      <div className="card"><h3>Sovereignty</h3><div className="metric">{sovPct}</div></div>
      <div className="card"><h3>Bias Flags</h3><div className="metric">{bias?.fairness_flagged??"—"}<small>of {bias?.decisions_scanned??0} scanned</small></div></div>
      <div className="card"><h3>Audit Chain</h3><div className="metric" style={{color:chain?.intact?"var(--ok)":"var(--bad)"}}>{chain?(chain.intact?"INTACT":"BROKEN"):"—"}<small>{chain?.records??0} records</small></div></div>
      <div className="card"><h3>SETHS Learners</h3><div className="metric">{s?.learners??"—"}</div></div>
      <div className="card"><h3>TS Projects</h3><div className="metric">{s?.ts_projects??"—"}</div></div>
    </div>
    <div className="panel"><h3>Closed-Loop Economic Snapshot</h3>
      {loop?<p style={{color:"var(--white)",fontSize:".85rem"}}>{loop.loop} — SETHS placed <b>{loop.seths_placed}</b> ·
        TS monthly profit <b>R{(loop.ts_monthly_profit||0).toLocaleString()}</b> ·
        MADIBA recycled <b>R{(loop.madiba_cumulative_recycled||0).toLocaleString()}</b> ·
        UDOC decisions <b>{loop.udoc_decisions}</b></p>:<p>Loading…</p>}
    </div>
    <div className="panel"><h3>Live Audit Stream</h3>
      <div style={{maxHeight:300,overflow:"auto"}}>
        {audit.length? audit.slice(0,14).map((r:any,i:number)=>(
          <div key={i} style={{display:"flex",gap:10,padding:"6px 2px",borderBottom:"1px solid rgba(29,48,80,.5)",fontSize:".76rem"}}>
            <span style={{color:"var(--rule)",fontFamily:"monospace",minWidth:62}}>{String(r.created_at||"").slice(11,19)}</span>
            <span style={{color:"var(--gold)",minWidth:128,fontFamily:"monospace"}}>{r.event_type||r.event||"EVENT"}</span>
            <span style={{flex:1,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{typeof r.detail==="string"?r.detail:JSON.stringify(r.detail||r.classification||"")}</span>
          </div>)) : <p style={{color:"var(--rule)",fontSize:".8rem"}}>No audit events yet — run a governance decision in UDOC.</p>}
      </div>
    </div></>);
}
