import { useEffect, useState } from "react";
import { api } from "../api";
export function SethsOps(){
  const [m,setM]=useState<any>(null); const [subs,setSubs]=useState<any[]>([]); const [msg,setMsg]=useState("");
  async function load(){ try{
    setM(await api.get("/analytics/SETHS/kpis"));
    setSubs(await api.get("/ts/submit/projects").catch(()=>[]));
  }catch(e:any){ setMsg(e.message); } }
  useEffect(()=>{ load(); },[]);
  async function enrol(){ await api.post("/seths/enrol",{count:10}); setMsg("Cohort of 10 enrolled"); load(); }
  return (<><div className="top"><h2><span className="acc-seths">SETHS</span> Operations</h2><span className="badge">🔒 STAFF</span></div>
    <div className="grid">
      <div className="card"><h3>Enrolled</h3><div className="metric">{m?.enrolled??"—"}</div></div>
      <div className="card"><h3>Placed</h3><div className="metric">{m?.placed??"—"}</div></div>
      <div className="card"><h3>Placement Rate</h3><div className="metric">{m?((m.placement_rate*100).toFixed(0)+"%"):"—"}</div></div>
      <div className="card"><h3>Monthly Output</h3><div className="metric">R{(m?.monthly_output??0).toLocaleString()}</div></div>
    </div>
    <div className="panel"><h3>Cohort Management</h3>
      <div className="row"><button className="btn" onClick={enrol}>Enrol new cohort (10)</button>
        <span style={{fontSize:".76rem",color:"var(--text)"}}>Learners flow through ENROLLED → COMPLETED → PLACED; placements create TS employees.</span></div>
    </div>
    <div className="panel"><h3>Programme Note</h3>
      <p style={{fontSize:".82rem"}}>Software Developer (SAQA 118707, NQF 5). Student applications and document
      verification are handled in the external SETHS app; staff approve placements via the Employer flow.</p></div>
    {msg&&<div className="ok">{msg}</div>}</>);
}
