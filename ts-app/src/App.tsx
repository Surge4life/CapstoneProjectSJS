import { useEffect, useState } from "react";
import { api, getBase, setBase, ping, getToken, setToken } from "./api";

export function App() {
  const [base,setBaseState]=useState(getBase());
  const [connected,setConnected]=useState<boolean|null>(null);
  const [authed,setAuthed]=useState(!!getToken());
  const [tab,setTab]=useState<"submit"|"partner">("submit");
  const [projects,setProjects]=useState<any[]>([]);
  const [title,setTitle]=useState(""); const [sector,setSector]=useState("ENERGY");
  const [stype,setStype]=useState("PRIVATE"); const [capex,setCapex]=useState(50000000); const [submitter,setSubmitter]=useState("");
  const [porg,setPorg]=useState(""); const [pcap,setPcap]=useState("");
  const [msg,setMsg]=useState("");
  async function checkConn(){ setConnected(await ping()); } useEffect(()=>{checkConn();},[]);
  function saveBase(){ setBase(base); setBaseState(getBase()); checkConn(); }
  async function login(){ try{ await api.login("admin@gods.local","admin123"); setAuthed(true);}catch(e:any){setMsg(e.message);} }
  async function load(){ try{ setProjects(await api.get("/ts/submit/projects")); }catch(e:any){ setMsg(e.message); } }
  useEffect(()=>{ if(authed) load(); }, [authed]);
  async function submitProject(){ const r=await api.post("/ts/submit/project",{submitter_name:submitter,submitter_type:stype,sector,title,capex_estimate:capex}); setMsg(`Submitted ${r.submission_ref}`); setTitle(""); load(); }
  async function advance(ref:string){ await api.post(`/ts/submit/project/${ref}/advance`); load(); }
  async function applyPartner(){ const r=await api.post("/ts/submit/partner",{org_name:porg,capability:pcap,sector}); setMsg(`Partner application ${r.app_ref} submitted`); setPorg(""); setPcap(""); }

  if(connected!==true) return (<div className="connect"><span className="gods">G.O.D.S · TS</span><h1>Connect</h1>
    <input value={base} onChange={e=>setBaseState(e.target.value)} placeholder="backend URL"/>
    <button className="btn" onClick={saveBase}>Connect</button>
    <div className={`status ${connected?"ok":"bad"}`}>{connected===null?"checking…":`✗ ${getBase()} unreachable`}</div></div>);
  if(!authed) return (<div className="connect"><span className="gods">G.O.D.S · TS</span><h1>Sign in</h1>
    <div className="status ok">✓ {getBase()}</div><button className="btn" onClick={login}>Sign in</button>{msg&&<div className="err">{msg}</div>}</div>);

  return (<div className="wrap">
    <div className="hdr"><div><span className="gods">G.O.D.S · TS Industries</span><h2>Projects & Partners</h2></div>
      <span className="back" onClick={()=>{setToken(null);location.reload();}}>sign out</span></div>
    <div style={{display:"flex",gap:8,marginBottom:16}}>
      <button className={`btn sm ${tab==="submit"?"":"danger"}`} style={{background:tab==="submit"?"var(--accent)":"transparent",color:tab==="submit"?"var(--navy)":"var(--text)",border:"1px solid var(--rule)"}} onClick={()=>setTab("submit")}>Submit / Track</button>
      <button className="btn sm" style={{background:tab==="partner"?"var(--accent)":"transparent",color:tab==="partner"?"var(--navy)":"var(--text)",border:"1px solid var(--rule)"}} onClick={()=>setTab("partner")}>Become a Partner</button>
    </div>
    {tab==="submit" ? (<>
      <div className="card"><h3>Submit a project (SPV / government / private)</h3>
        <input placeholder="Submitter / organisation" value={submitter} onChange={e=>setSubmitter(e.target.value)}/>
        <select value={stype} onChange={e=>setStype(e.target.value)}><option>GOV</option><option>PRIVATE</option><option>SPV</option></select>
        <input placeholder="Project title" value={title} onChange={e=>setTitle(e.target.value)}/>
        <select value={sector} onChange={e=>setSector(e.target.value)}><option>ENERGY</option><option>HOUSING</option><option>AGRITECH</option><option>WATER</option><option>LOGISTICS</option></select>
        <input type="number" value={capex} onChange={e=>setCapex(Number(e.target.value))}/>
        <button className="btn" onClick={submitProject}>Submit project</button></div>
      <div className="card"><h3>Project tracking</h3>
        <table><thead><tr><th>Ref</th><th>Title</th><th>Type</th><th>Stage</th><th></th></tr></thead>
          <tbody>{projects.map(p=><tr key={p.ref}>
            <td>{p.ref}</td><td>{p.title}</td><td>{p.type}</td><td><span className={`tag ${p.stage}`}>{p.stage}</span></td>
            <td>{["SUBMITTED","SCREENING","APPROVED"].includes(p.stage)&&<button className="btn sm" onClick={()=>advance(p.ref)}>Advance</button>}</td></tr>)}
            {projects.length===0&&<tr><td colSpan={5} style={{color:"var(--rule)"}}>No projects yet</td></tr>}
          </tbody></table></div>
    </>):(
      <div className="card"><h3>Apply to become a partnered build assistant</h3>
        <input placeholder="Organisation" value={porg} onChange={e=>setPorg(e.target.value)}/>
        <input placeholder="Capability (e.g. EPC, civils, solar)" value={pcap} onChange={e=>setPcap(e.target.value)}/>
        <select value={sector} onChange={e=>setSector(e.target.value)}><option>ENERGY</option><option>HOUSING</option><option>AGRITECH</option><option>WATER</option><option>LOGISTICS</option></select>
        <button className="btn" onClick={applyPartner}>Submit partner application</button></div>
    )}
    {msg&&<div className="ok">{msg}</div>}
    <div className="foot">TS INDUSTRIES · PROJECT DELIVERY & PARTNER NETWORK</div>
  </div>);
}
