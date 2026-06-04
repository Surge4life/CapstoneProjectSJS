import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, NavLink, Navigate, useNavigate } from "react-router-dom";
import { api, getToken, setToken } from "./api";
import { Overview } from "./consoles/Overview";
import { SethsOps } from "./consoles/SethsOps";
import { MadibaOps } from "./consoles/MadibaOps";
import { TSOps } from "./consoles/TSOps";
import { UDOCGov } from "./consoles/UDOCGov";

interface Sys { key: string; title: string; path: string; }
interface Profile { email: string; role: string; division: string; systems: Sys[]; is_admin: boolean; }

function Login({ onAuth }: { onAuth: () => void }) {
  const [email, setEmail] = useState("admin@gods.local");
  const [pw, setPw] = useState("admin123");
  const [err, setErr] = useState("");
  async function go(){ try{ await api.login(email,pw); onAuth(); }catch(e:any){ setErr(e.message); } }
  return (<div className="login"><h1>G.O.D.S Internal</h1>
    <span className="lock">🔒 Network-locked · role-based access</span>
    <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="staff email"/>
    <input type="password" value={pw} onChange={e=>setPw(e.target.value)} placeholder="password"/>
    <button className="btn" onClick={go}>Sign in</button>{err&&<div className="err">{err}</div>}
    <p style={{fontSize:".68rem",color:"var(--rule)",marginTop:14}}>Try: seths.op@gods.local · ts.op@gods.local · auditor@gods.local · viewer@gods.local (pw staff123)</p>
  </div>);
}

// The G.O.D.S core launcher — shows ONLY the systems this user may open.
function Launcher({ profile }: { profile: Profile }) {
  const nav = useNavigate();
  const accent: Record<string,string> = { "seths-ops":"var(--seths)","madiba-ops":"var(--madiba)","ts-ops":"var(--ts)","udoc-gov":"var(--udoc)","holdings-overview":"var(--gold)" };
  return (<div style={{maxWidth:760,margin:"0 auto",padding:"40px 20px"}}>
    <div style={{textAlign:"center",marginBottom:30}}>
      <h1 style={{color:"var(--gold)",letterSpacing:".1em"}}>G.O.D.S</h1>
      <p style={{fontSize:".7rem",letterSpacing:".2em",textTransform:"uppercase",color:"var(--text)"}}>Internal Operating Core</p>
      <p style={{fontSize:".82rem",marginTop:10}}>Signed in as <b>{profile.email}</b> · {profile.role} / {profile.division}</p>
      <p style={{fontSize:".7rem",color:"var(--warn)"}}>🔒 Systems shown are scoped to your access rights</p>
    </div>
    <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(200px,1fr))",gap:14}}>
      {profile.systems.map(s=>(
        <div key={s.key} onClick={()=>nav(s.path)} className="card" style={{cursor:"pointer",borderTop:`3px solid ${accent[s.key]||"var(--gold)"}`,textAlign:"center",padding:"24px 16px"}}>
          <h3 style={{color:accent[s.key]||"var(--gold)",fontSize:".95rem",marginBottom:6,textTransform:"none",letterSpacing:0}}>{s.title}</h3>
          <p style={{fontSize:".72rem"}}>Open →</p>
        </div>
      ))}
    </div>
    <div style={{textAlign:"center",marginTop:30}}>
      <a onClick={()=>{setToken(null);location.reload();}} style={{color:"var(--bad)",fontSize:".8rem",cursor:"pointer"}}>Sign out</a></div>
  </div>);
}

function Shell({ profile, children }: { profile: Profile; children: React.ReactNode }) {
  return (<div className="app">
    <aside className="side">
      <div className="brand"><h1>G.O.D.S</h1><span>Internal Operating Core</span>
        <span className="lock">🔒 {profile.role}/{profile.division}</span></div>
      <nav className="nav">
        <NavLink to="/launcher" className={({isActive})=>isActive?"active":""}>⌂ Launcher</NavLink>
        {profile.systems.some(s=>s.key==="holdings-overview") && <NavLink to="/overview" className={({isActive})=>isActive?"active":""}>Holdings Overview</NavLink>}
        {(profile.systems.some(s=>["seths-ops","madiba-ops","ts-ops"].includes(s.key))) && <div className="sec">Division Operations</div>}
        {profile.systems.some(s=>s.key==="seths-ops") && <NavLink to="/seths" className={({isActive})=>isActive?"active":""}>SETHS Ops</NavLink>}
        {profile.systems.some(s=>s.key==="madiba-ops") && <NavLink to="/madiba" className={({isActive})=>isActive?"active":""}>MADIBA Ops</NavLink>}
        {profile.systems.some(s=>s.key==="ts-ops") && <NavLink to="/ts" className={({isActive})=>isActive?"active":""}>TS Industries Ops</NavLink>}
        {profile.systems.some(s=>s.key==="udoc-gov") && <><div className="sec">Governance</div>
          <NavLink to="/udoc" className={({isActive})=>isActive?"active":""}>UDOC Governance</NavLink></>}
        <a onClick={()=>{setToken(null);location.reload();}} style={{color:"var(--bad)",marginTop:16}}>Sign out</a>
      </nav>
    </aside>
    <main className="main">{children}</main>
  </div>);
}

// Guard wrapper: a console only renders if the system is in the user's profile.
function Guarded({ profile, sysKey, children }: { profile: Profile; sysKey: string; children: React.ReactNode }) {
  const allowed = profile.systems.some(s=>s.key===sysKey);
  if(!allowed) return <div className="main"><div className="top"><h2>Access denied</h2><span className="badge">🔒 403</span></div>
    <div className="panel"><p style={{fontSize:".85rem"}}>Your role ({profile.role}/{profile.division}) may not open this system. The backend enforces this too.</p></div></div>;
  return <>{children}</>;
}

export function App(){
  const [authed,setAuthed]=useState(!!getToken());
  const [profile,setProfile]=useState<Profile|null>(null);
  const [err,setErr]=useState("");
  useEffect(()=>{ if(authed){ api.get("/access/profile").then(setProfile).catch(e=>setErr(e.message)); } },[authed]);
  if(!authed) return <Login onAuth={()=>setAuthed(true)}/>;
  if(err) return <div className="login"><h1>G.O.D.S</h1><div className="err">{err}</div>
    <button className="btn" onClick={()=>{setToken(null);location.reload();}}>Back to sign in</button></div>;
  if(!profile) return <div className="login"><h1>G.O.D.S</h1><p>Opening your systems…</p></div>;
  return (<BrowserRouter><Shell profile={profile}><Routes>
    <Route path="/launcher" element={<Launcher profile={profile}/>}/>
    <Route path="/overview" element={<Guarded profile={profile} sysKey="holdings-overview"><Overview/></Guarded>}/>
    <Route path="/seths" element={<Guarded profile={profile} sysKey="seths-ops"><SethsOps/></Guarded>}/>
    <Route path="/madiba" element={<Guarded profile={profile} sysKey="madiba-ops"><MadibaOps/></Guarded>}/>
    <Route path="/ts" element={<Guarded profile={profile} sysKey="ts-ops"><TSOps/></Guarded>}/>
    <Route path="/udoc" element={<Guarded profile={profile} sysKey="udoc-gov"><UDOCGov/></Guarded>}/>
    <Route path="*" element={<Navigate to="/launcher"/>}/>
  </Routes></Shell></BrowserRouter>);
}
