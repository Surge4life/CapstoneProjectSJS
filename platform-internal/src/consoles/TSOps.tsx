import { useEffect, useState } from "react";
import { api } from "../api";
export function TSOps(){
  const [projects,setProjects]=useState<any[]>([]); const [k,setK]=useState<any>(null); const [msg,setMsg]=useState("");
  async function load(){ try{ setProjects(await api.get("/ts/submit/projects")); setK(await api.get("/analytics/TS/kpis")); }catch(e:any){ setMsg(e.message); } }
  useEffect(()=>{ load(); },[]);
  async function advance(ref:string){ await api.post(`/ts/submit/project/${ref}/advance`); setMsg(`Advanced ${ref}`); load(); }
  async function deploy(){ await api.post("/ts/projects",{sector:"ENERGY",name:"Internal SPV",workers_deployed:5,monthly_revenue:2000000,operating_margin:0.31}); setMsg("SPV deployed"); load(); }
  return (<><div className="top"><h2><span className="acc-ts">TS Industries</span> Operations</h2><span className="badge">🔒 STAFF</span></div>
    <div className="grid">
      <div className="card"><h3>Revenue</h3><div className="metric">R{((k?.total_revenue??0)/1e6).toFixed(1)}M</div></div>
      <div className="card"><h3>Profit</h3><div className="metric">R{((k?.total_profit??0)/1e6).toFixed(1)}M</div></div>
      <div className="card"><h3>Workers</h3><div className="metric">{k?.workers_absorbed??"—"}</div></div>
      <div className="card"><h3>Avg Margin</h3><div className="metric">{k?((k.avg_margin*100).toFixed(0)+"%"):"—"}</div></div>
    </div>
    <div className="panel"><h3>Project Submissions (staff screening)</h3>
      <table><thead><tr><th>Ref</th><th>Title</th><th>Type</th><th>Capex</th><th>Stage</th><th></th></tr></thead>
        <tbody>{projects.map(p=><tr key={p.ref}>
          <td>{p.ref}</td><td>{p.title}</td><td>{p.type}</td><td>R{(p.capex/1e6).toFixed(0)}M</td>
          <td><span className={`tag ${p.stage}`}>{p.stage}</span></td>
          <td>{["SUBMITTED","SCREENING","APPROVED"].includes(p.stage)&&<button className="btn sm" onClick={()=>advance(p.ref)}>Advance</button>}</td></tr>)}
          {!projects.length&&<tr><td colSpan={6} style={{color:"var(--rule)"}}>No submissions (added via TS app)</td></tr>}
        </tbody></table></div>
    <div className="panel"><h3>SPV Deployment</h3>
      <div className="row"><button className="btn" onClick={deploy}>Deploy internal SPV</button></div></div>
    {msg&&<div className="ok">{msg}</div>}</>);
}
