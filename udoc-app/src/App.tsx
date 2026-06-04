import { useEffect, useState } from "react";
import { api, getBase, setBase, ping, getToken, setToken } from "./api";

export function App() {
  const [base, setBaseState] = useState(getBase());
  const [connected, setConnected] = useState<boolean | null>(null);
  const [authed, setAuthed] = useState(!!getToken());
  const [clientRef, setClientRef] = useState(localStorage.getItem("cli_ref") || "");
  const [org, setOrg] = useState(""); const [cemail, setCemail] = useState("");
  const [dash, setDash] = useState<any>(null);
  const [models, setModels] = useState<any[]>([]);
  const [msg, setMsg] = useState("");

  async function checkConn(){ setConnected(await ping()); }
  useEffect(()=>{ checkConn(); }, []);
  function saveBase(){ setBase(base); setBaseState(getBase()); checkConn(); }

  async function login(){ try{ await api.login("admin@gods.local","admin123"); setAuthed(true); }catch(e:any){ setMsg(e.message); } }
  async function load(){
    if(!clientRef) return;
    try{ setDash(await api.get(`/saas/${clientRef}/dashboard`)); setModels(await api.get(`/saas/${clientRef}/models`)); }
    catch(e:any){ setMsg(e.message); }
  }
  useEffect(()=>{ if(authed && clientRef) load(); }, [authed, clientRef]);

  async function register(){
    try{ const r=await api.post("/saas/register",{org_name:org,contact_email:cemail,tier:"SOVEREIGN"});
      localStorage.setItem("cli_ref",r.client_ref); setClientRef(r.client_ref); setMsg(`Registered ${r.client_ref} · API key ${r.api_key.slice(0,12)}…`);
    }catch(e:any){ setMsg(e.message); }
  }
  async function toggle(model_id:string, status:string){
    const action = status==="ACTIVE" ? "suspend" : "resume";
    await api.post(`/saas/${clientRef}/${action}/${model_id}`); load();
  }

  if(connected===false || connected===null) return (
    <div className="connect"><span className="gods">G.O.D.S · UDOC</span><h1>Connect to UDOC</h1>
      <p style={{fontSize:".8rem",margin:"8px 0"}}>Point this app at your UDOC deployment.</p>
      <input value={base} onChange={e=>setBaseState(e.target.value)} placeholder="http://your-ip:8000 or tunnel URL"/>
      <button className="btn" onClick={saveBase}>Connect</button>
      <div className={`status ${connected?"ok":"bad"}`}>{connected===null?"checking…":`✗ not reachable at ${getBase()}`}</div>
      <div className="foot">SaaS AI GOVERNANCE CONTROL</div></div>
  );
  if(!authed) return (
    <div className="connect"><span className="gods">G.O.D.S · UDOC</span><h1>Sign in</h1>
      <div className="status ok">✓ connected to {getBase()}</div>
      <button className="btn" onClick={login}>Sign in</button>{msg&&<div className="err">{msg}</div>}</div>
  );

  return (
    <div className="wrap">
      <div className="hdr"><div><span className="gods">G.O.D.S · UDOC</span><h2>AI Control Console</h2></div>
        <span className="back" onClick={()=>{setToken(null);location.reload();}}>sign out</span></div>
      {!clientRef ? (
        <div className="card"><h3>Register your organisation</h3>
          <input placeholder="Organisation" value={org} onChange={e=>setOrg(e.target.value)}/>
          <input placeholder="Contact email" value={cemail} onChange={e=>setCemail(e.target.value)}/>
          <button className="btn" onClick={register}>Register as UDOC client</button></div>
      ):(<>
        <div className="grid">
          <div className="card"><h3>My AIs</h3><div className="metric">{dash?.models ?? "—"}</div></div>
          <div className="card"><h3>Active</h3><div className="metric">{dash?.active ?? "—"}</div></div>
          <div className="card"><h3>Suspended</h3><div className="metric">{dash?.suspended ?? "—"}</div></div>
          <div className="card"><h3>Recent Blocks</h3><div className="metric">{dash?.recent_blocks ?? "—"}</div></div>
        </div>
        <div className="card"><h3>Deployed AIs — you are always in control</h3>
          <table><thead><tr><th>Model</th><th>Risk</th><th>Status</th><th>Control</th></tr></thead>
            <tbody>{models.map(m=><tr key={m.model_id}>
              <td>{m.model_id}</td><td>{m.risk_tier}</td><td><span className={`tag ${m.status}`}>{m.status}</span></td>
              <td><button className={`btn sm ${m.status==="ACTIVE"?"danger":""}`} onClick={()=>toggle(m.model_id,m.status)}>
                {m.status==="ACTIVE"?"Suspend (kill-switch)":"Resume"}</button></td></tr>)}
              {models.length===0&&<tr><td colSpan={4} style={{color:"var(--rule)"}}>No AIs registered yet</td></tr>}
            </tbody></table>
        </div>
      </>)}
      {msg&&<div className="ok">{msg}</div>}
      <div className="foot">UDOC SOVEREIGN GOVERNANCE · CLIENT CONTROL PLANE</div>
    </div>
  );
}
