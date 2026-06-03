import { useEffect, useState } from "react";
import { api } from "../api";
export function Overview(){
  const [s,setS]=useState<any>(null); const [loop,setLoop]=useState<any>(null);
  useEffect(()=>{ api.get("/admin/status").then(setS).catch(()=>{});
    api.get("/intelligence/loop-snapshot").then(setLoop).catch(()=>{}); },[]);
  return (<><div className="top"><h2>Holdings Overview</h2><span className="badge">🔒 INTERNAL</span></div>
    <div className="grid">
      <div className="card"><h3>Models Governed</h3><div className="metric">{s?.models??"—"}</div></div>
      <div className="card"><h3>Decisions</h3><div className="metric">{s?.decisions??"—"}</div></div>
      <div className="card"><h3>SETHS Learners</h3><div className="metric">{s?.learners??"—"}</div></div>
      <div className="card"><h3>TS Projects</h3><div className="metric">{s?.ts_projects??"—"}</div></div>
      <div className="card"><h3>Open Oversight</h3><div className="metric">{s?.open_oversight??"—"}</div></div>
      <div className="card"><h3>Staff Users</h3><div className="metric">{s?.users??"—"}</div></div>
    </div>
    <div className="panel"><h3>Closed-Loop Economic Snapshot</h3>
      {loop?<p style={{color:"var(--white)",fontSize:".85rem"}}>{loop.loop} — SETHS placed <b>{loop.seths_placed}</b> ·
        TS monthly profit <b>R{loop.ts_monthly_profit?.toLocaleString()}</b> ·
        MADIBA recycled <b>R{loop.madiba_cumulative_recycled?.toLocaleString()}</b> ·
        UDOC decisions <b>{loop.udoc_decisions}</b></p>:<p>Loading…</p>}
    </div></>);
}
