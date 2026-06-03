import { useEffect, useState } from "react";
import { api, getBase, setBase, ping, getToken, setToken } from "./api";

export function App() {
  const [base, setBaseState] = useState(getBase());
  const [connected, setConnected] = useState<boolean|null>(null);
  const [authed, setAuthed] = useState(!!getToken());
  const [sref, setSref] = useState(localStorage.getItem("stu_ref") || "");
  const [name, setName] = useState(""); const [email, setEmail] = useState("");
  const [profile, setProfile] = useState<any>(null);
  const [opps, setOpps] = useState<any[]>([]);
  const [docs, setDocs] = useState<any[]>([]);
  const [msg, setMsg] = useState("");

  async function checkConn(){ setConnected(await ping()); } useEffect(()=>{checkConn();},[]);
  function saveBase(){ setBase(base); setBaseState(getBase()); checkConn(); }
  async function login(){ try{ await api.login("admin@gods.za","admin123"); setAuthed(true);}catch(e:any){setMsg(e.message);} }
  async function load(){
    if(!sref) return;
    try{ setProfile(await api.get(`/portal/student/${sref}`));
      setOpps(await api.get(`/portal/student/opportunities/open`));
      setDocs(await api.get(`/documents/owner/${sref}`)); }catch(e:any){ setMsg(e.message); }
  }
  useEffect(()=>{ if(authed&&sref) load(); }, [authed, sref]);

  async function register(){ try{ const r=await api.post("/portal/student/register",{full_name:name,email});
    localStorage.setItem("stu_ref",r.student_ref); setSref(r.student_ref);}catch(e:any){setMsg(e.message);} }
  async function progress(p:number){ await api.post(`/portal/student/${sref}/progress?pct=${p}`); load(); }
  async function apply(oid:number){ try{ await api.post(`/portal/student/${sref}/apply/${oid}`); setMsg("Applied"); load(); }catch(e:any){ setMsg(e.message); } }
  async function uploadDoc(e:any){
    const f=e.target.files?.[0]; if(!f) return;
    try{ const r=await api.upload("SETHS",sref,"CV",f); setMsg(`Uploaded ${r.doc_ref}`); load(); }catch(err:any){ setMsg(err.message); }
  }

  if(connected!==true) return (
    <div className="connect"><span className="gods">G.O.D.S · SETHS</span><h1>Connect</h1>
      <input value={base} onChange={e=>setBaseState(e.target.value)} placeholder="backend URL"/>
      <button className="btn" onClick={saveBase}>Connect</button>
      <div className={`status ${connected?"ok":"bad"}`}>{connected===null?"checking…":`✗ ${getBase()} unreachable`}</div></div>
  );
  if(!authed) return (<div className="connect"><span className="gods">G.O.D.S · SETHS</span><h1>Sign in</h1>
    <div className="status ok">✓ {getBase()}</div><button className="btn" onClick={login}>Sign in</button>{msg&&<div className="err">{msg}</div>}</div>);

  return (
    <div className="wrap">
      <div className="hdr"><div><span className="gods">G.O.D.S · SETHS</span><h2>Student Portal</h2></div>
        <span className="back" onClick={()=>{setToken(null);location.reload();}}>sign out</span></div>
      {!sref ? (
        <div className="card"><h3>Enrol</h3>
          <input placeholder="Full name" value={name} onChange={e=>setName(e.target.value)}/>
          <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)}/>
          <button className="btn" onClick={register}>Enrol in SETHS</button></div>
      ):(<>
        <div className="card"><h3>My Programme</h3>
          {profile&&<><div className="metric">{profile.full_name}</div>
            <p style={{fontSize:".82rem"}}>{profile.qualification} · status <span className={`tag ${profile.status}`}>{profile.status}</span> · {profile.progress_pct}%</p>
            <div style={{display:"flex",gap:8,marginTop:8}}>
              <button className="btn sm" onClick={()=>progress(50)}>50%</button>
              <button className="btn sm" onClick={()=>progress(100)}>Complete</button></div></>}
        </div>
        <div className="card"><h3>My Documents (stored via UDOC records)</h3>
          <input type="file" onChange={uploadDoc}/>
          <table><thead><tr><th>File</th><th>Category</th><th>Size</th><th></th></tr></thead>
            <tbody>{docs.map(d=><tr key={d.doc_ref}>
              <td>{d.filename}</td><td>{d.category}</td><td>{d.size_bytes}B</td>
              <td><a className="btn sm" href={api.downloadUrl(d.doc_ref)} target="_blank">Download</a></td></tr>)}
              {docs.length===0&&<tr><td colSpan={4} style={{color:"var(--rule)"}}>No documents yet — upload your CV/qualifications</td></tr>}
            </tbody></table>
        </div>
        <div className="card"><h3>Open Opportunities</h3>
          <table><thead><tr><th>Role</th><th>Employer</th><th>Stipend</th><th></th></tr></thead>
            <tbody>{opps.map(o=><tr key={o.id}>
              <td>{o.title}</td><td>{o.employer}</td><td>R{o.monthly_stipend.toLocaleString()}</td>
              <td><button className="btn sm" onClick={()=>apply(o.id)}>Apply</button></td></tr>)}
              {opps.length===0&&<tr><td colSpan={4} style={{color:"var(--rule)"}}>No open roles yet</td></tr>}
            </tbody></table>
        </div>
      </>)}
      {msg&&<div className="ok">{msg}</div>}
      <div className="foot">SETHS · DOCUMENTS GOVERNED & RECORDED BY UDOC</div>
    </div>
  );
}
