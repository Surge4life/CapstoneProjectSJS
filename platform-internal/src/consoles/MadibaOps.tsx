import { useEffect, useState } from "react";
import { api } from "../api";
export function MadibaOps(){
  const [pipe,setPipe]=useState<any>(null); const [k,setK]=useState<any>(null); const [msg,setMsg]=useState("");
  async function load(){ try{ setPipe(await api.get("/madiba/engage/pipeline")); setK(await api.get("/analytics/MADIBA/kpis")); }catch(e:any){ setMsg(e.message); } }
  useEffect(()=>{ load(); },[]);
  async function cycle(){ const month=(k?.cycles||0)+1; await api.post("/madiba/allocate",{month,total_inflow:1894000}); setMsg("Capital cycle allocated"); load(); }
  async function advance(ref:string){ await api.post(`/madiba/engage/${ref}/advance`); load(); }
  return (<><div className="top"><h2><span className="acc-madiba">MADIBA</span> Operations</h2><span className="badge">🔒 STAFF</span></div>
    <div className="grid">
      <div className="card"><h3>Engagements</h3><div className="metric">{pipe?.engagements??"—"}</div></div>
      <div className="card"><h3>Indicated</h3><div className="metric">R{((pipe?.indicated_total??0)/1e6).toFixed(0)}M</div></div>
      <div className="card"><h3>Committed</h3><div className="metric">R{((pipe?.committed_total??0)/1e6).toFixed(0)}M</div></div>
      <div className="card"><h3>Recycle Ratio</h3><div className="metric">{k?((k.recycle_ratio*100).toFixed(0)+"%"):"—"}<small>Pillar 2 &gt;50%</small></div></div>
    </div>
    <div className="panel"><h3>Capital Operations</h3>
      <div className="row"><button className="btn" onClick={cycle}>Run capital allocation cycle</button></div></div>
    <div className="panel"><h3>Investor Pipeline (staff review)</h3>
      <table><thead><tr><th>Investor</th><th>Type</th><th>Amount</th><th>Stage</th><th></th></tr></thead>
        <tbody>{pipe?.list?.map((e:any)=><tr key={e.ref}>
          <td>{e.investor}</td><td>{e.type}</td><td>R{(e.amount/1e6).toFixed(0)}M</td>
          <td><span className={`tag ${e.stage}`}>{e.stage}</span></td>
          <td>{e.stage!=="FUNDED"&&<button className="btn sm" onClick={()=>advance(e.ref)}>Advance stage</button>}</td></tr>)}
          {(!pipe?.list||!pipe.list.length)&&<tr><td colSpan={5} style={{color:"var(--rule)"}}>No engagements (added via MADIBA app)</td></tr>}
        </tbody></table></div>
    {msg&&<div className="ok">{msg}</div>}</>);
}
