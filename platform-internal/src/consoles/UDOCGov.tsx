import { useEffect, useState } from "react";
import { api } from "../api";
export function UDOCGov(){
  const [models,setModels]=useState<any[]>([]); const [cases,setCases]=useState<any[]>([]);
  const [chain,setChain]=useState<any>(null); const [sov,setSov]=useState<any>(null);
  const [result,setResult]=useState<any>(null); const [scenario,setScenario]=useState("healthy"); const [msg,setMsg]=useState("");
  async function load(){ try{
    setModels(await api.get("/registry/models"));
    setCases(await api.get("/oversight/cases").catch(()=>[]));
    setChain(await api.get("/audit/chain/verify").catch(()=>null));
    setSov(await api.get("/sovereignty/posture").catch(()=>null));
  }catch(e:any){ setMsg(e.message); } }
  useEffect(()=>{ load(); },[]);
  async function decide(){
    const b:any={model_id: models[0]?.model_id || "model-001"};
    if(scenario==="biased") Object.assign(b,{risk_tier:"HIGH",priv_favorable:600,unpriv_favorable:300,ecs:0.3});
    if(scenario==="breach") Object.assign(b,{traceroute:0.4});
    try{ setResult(await api.post("/decisions",b)); load(); }catch(e:any){ setResult({error:e.message}); }
  }
  async function openCase(){ const mid=models[0]?.model_id||"model-001";
    await api.post("/oversight/cases",{model_id:mid,reason:"manual staff review"}); setMsg("Oversight case opened"); load(); }
  async function resolve(ref:string){ await api.post(`/oversight/cases/${ref}/resolve?resolution=reviewed&override=false`); load(); }
  return (<><div className="top"><h2><span className="acc-udoc">UDOC</span> Governance</h2><span className="badge">🔒 INTERNAL ONLY</span></div>
    <div className="grid">
      <div className="card"><h3>Models</h3><div className="metric">{models.length}</div></div>
      <div className="card"><h3>Audit Records</h3><div className="metric">{chain?.records??"—"}</div></div>
      <div className="card"><h3>Chain Intact</h3><div className="metric" style={{color:chain?.intact?"var(--ok)":"var(--bad)"}}>{chain?String(chain.intact):"—"}</div></div>
      <div className="card"><h3>Sovereign Rate</h3><div className="metric">{sov?((sov.sovereign_rate*100).toFixed(0)+"%"):"—"}</div></div>
    </div>
    <div className="panel"><h3>Run Governance Decision</h3>
      <div className="row">
        <select value={scenario} onChange={e=>setScenario(e.target.value)}>
          <option value="healthy">Healthy model</option><option value="biased">Biased + high-risk</option><option value="breach">Sovereignty breach</option></select>
        <button className="btn" onClick={decide}>Evaluate</button></div>
      {result&&!result.error&&<p style={{fontSize:".82rem"}}>Decision <span className={`tag ${result.decision}`}>{result.decision}</span>
        · SVS {result.svs} · latency {result.latency_ms}ms (budget {result.budget_ms}ms) · sealed {result.seal?.slice(0,16)}…
        {result.block_reasons?.length>0 && <span style={{color:"var(--bad)"}}> · {result.block_reasons.length} block reasons</span>}</p>}
      {result?.error&&<div className="err">{result.error}</div>}
    </div>
    <div className="panel"><h3>Human Oversight Cases (Pillar VIII)</h3>
      <div className="row"><button className="btn sm" onClick={openCase}>Open review case</button></div>
      <table><thead><tr><th>Ref</th><th>Model</th><th>Reason</th><th>State</th><th></th></tr></thead>
        <tbody>{cases.map((c:any)=><tr key={c.case_ref}>
          <td>{c.case_ref}</td><td>{c.model_id}</td><td>{c.reason}</td><td><span className={`tag ${c.state}`}>{c.state}</span></td>
          <td>{c.state==="OPEN"&&<button className="btn sm" onClick={()=>resolve(c.case_ref)}>Resolve</button>}</td></tr>)}
          {!cases.length&&<tr><td colSpan={5} style={{color:"var(--rule)"}}>No open cases</td></tr>}
        </tbody></table></div>
    <div className="panel"><h3>Registered Models</h3>
      <table><thead><tr><th>Model</th><th>Operator</th><th>Risk</th><th>Status</th></tr></thead>
        <tbody>{models.map(m=><tr key={m.model_id}>
          <td>{m.model_id}</td><td>{m.operator_id||"—"}</td><td>{m.risk_tier}</td><td><span className={`tag ${m.status}`}>{m.status}</span></td></tr>)}
        </tbody></table></div>
    {msg&&<div className="ok">{msg}</div>}</>);
}
