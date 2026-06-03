import { useEffect, useState } from "react";
import { api, getBase, setBase, ping, getToken, setToken } from "./api";

export function App() {
  const [base,setBaseState]=useState(getBase());
  const [connected,setConnected]=useState<boolean|null>(null);
  const [authed,setAuthed]=useState(!!getToken());
  const [pipe,setPipe]=useState<any>(null);
  const [inv,setInv]=useState(""); const [amt,setAmt]=useState(100000000); const [itype,setItype]=useState("SOVEREIGN");
  const [msg,setMsg]=useState("");
  async function checkConn(){ setConnected(await ping()); } useEffect(()=>{checkConn();},[]);
  function saveBase(){ setBase(base); setBaseState(getBase()); checkConn(); }
  async function login(){ try{ await api.login("admin@gods.za","admin123"); setAuthed(true);}catch(e:any){setMsg(e.message);} }
  async function load(){ try{ setPipe(await api.get("/madiba/engage/pipeline")); }catch(e:any){ setMsg(e.message); } }
  useEffect(()=>{ if(authed) load(); }, [authed]);
  async function create(){ await api.post("/madiba/engage",{investor_name:inv,investor_type:itype,instrument:"blended",indicated_amount:amt}); setInv(""); load(); }
  async function advance(ref:string){ await api.post(`/madiba/engage/${ref}/advance`); load(); }

  if(connected!==true) return (<div className="connect"><span className="gods">G.O.D.S · MADIBA</span><h1>Connect</h1>
    <input value={base} onChange={e=>setBaseState(e.target.value)} placeholder="backend URL"/>
    <button className="btn" onClick={saveBase}>Connect</button>
    <div className={`status ${connected?"ok":"bad"}`}>{connected===null?"checking…":`✗ ${getBase()} unreachable`}</div></div>);
  if(!authed) return (<div className="connect"><span className="gods">G.O.D.S · MADIBA</span><h1>Sign in</h1>
    <div className="status ok">✓ {getBase()}</div><button className="btn" onClick={login}>Sign in</button>{msg&&<div className="err">{msg}</div>}</div>);

  return (<div className="wrap">
    <div className="hdr"><div><span className="gods">G.O.D.S · MADIBA</span><h2>Investor Engagement</h2></div>
      <span className="back" onClick={()=>{setToken(null);location.reload();}}>sign out</span></div>
    <div className="grid">
      <div className="card"><h3>Engagements</h3><div className="metric">{pipe?.engagements ?? "—"}</div></div>
      <div className="card"><h3>Indicated</h3><div className="metric">R{((pipe?.indicated_total??0)/1e6).toFixed(0)}M</div></div>
      <div className="card"><h3>Committed</h3><div className="metric">R{((pipe?.committed_total??0)/1e6).toFixed(0)}M</div></div>
    </div>
    <div className="card"><h3>Log a sovereign / institutional engagement</h3>
      <input placeholder="Investor name" value={inv} onChange={e=>setInv(e.target.value)}/>
      <select value={itype} onChange={e=>setItype(e.target.value)}>
        <option>SOVEREIGN</option><option>DFI</option><option>INSTITUTIONAL</option><option>PRIVATE</option></select>
      <input type="number" value={amt} onChange={e=>setAmt(Number(e.target.value))}/>
      <button className="btn" onClick={create}>Add engagement</button></div>
    <div className="card"><h3>Pipeline (project updates)</h3>
      <table><thead><tr><th>Investor</th><th>Type</th><th>Amount</th><th>Stage</th><th></th></tr></thead>
        <tbody>{pipe?.list?.map((e:any)=><tr key={e.ref}>
          <td>{e.investor}</td><td>{e.type}</td><td>R{(e.amount/1e6).toFixed(0)}M</td>
          <td><span className={`tag ${e.stage}`}>{e.stage}</span></td>
          <td>{e.stage!=="FUNDED"&&<button className="btn sm" onClick={()=>advance(e.ref)}>Advance</button>}</td></tr>)}
          {(!pipe?.list||pipe.list.length===0)&&<tr><td colSpan={5} style={{color:"var(--rule)"}}>No engagements yet</td></tr>}
        </tbody></table></div>
    {msg&&<div className="ok">{msg}</div>}
    <div className="foot">MADIBA CAPITAL · SOVEREIGN INFRASTRUCTURE INVESTMENT</div>
  </div>);
}
