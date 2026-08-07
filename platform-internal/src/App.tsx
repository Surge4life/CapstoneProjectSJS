import { useEffect, useState, type ReactNode } from "react";
import { BrowserRouter, Routes, Route, NavLink, Navigate, useNavigate } from "react-router-dom";
import { api, getToken, setToken } from "./api";
import { Overview } from "./consoles/Overview";
import { SethsOps } from "./consoles/SethsOps";
import { MadibaOps } from "./consoles/MadibaOps";
import { TSOps } from "./consoles/TSOps";
import { UDOCGov } from "./consoles/UDOCGov";
import { Intelligence } from "./consoles/Intelligence";

interface Sys { key: string; title: string; path: string; }
interface Profile { email: string; role: string; division: string; systems: Sys[]; is_admin: boolean; }
const isInternal = (p: Profile) => p.is_admin || ["admin", "operator", "gov"].includes(p.role);

function Login({ onAuth }: { onAuth: () => void }) {
  const [email, setEmail] = useState("admin@gods.local");
  const [pw, setPw] = useState("admin123");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const staff = [
    { email: "admin@gods.local", pw: "admin123", label: "Admin" },
    { email: "seths@gods.local", pw: "staff123", label: "SETHS" },
    { email: "madiba@gods.local", pw: "staff123", label: "MADIBA" },
    { email: "ts@gods.local", pw: "staff123", label: "TS" },
  ];
  async function go(e?: string, p?: string) {
    setBusy(true); setErr("");
    try {
      await api.login(e ?? email, p ?? pw);
      onAuth();
    } catch (ex: any) {
      setErr(ex.message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="login">
      <h1>G.O.D.S Internal</h1>
      <span className="lock">🔒 Network-locked · role-based access</span>
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="staff email" />
      <input type="password" value={pw} onChange={(e) => setPw(e.target.value)} placeholder="password" />
      <button className="btn" disabled={busy} onClick={() => go()}>
        Sign in
      </button>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 12, justifyContent: "center" }}>
        {staff.map((s) => (
          <button
            key={s.email}
            className="btn"
            disabled={busy}
            style={{ fontSize: ".72rem", opacity: 0.9 }}
            onClick={() => {
              setEmail(s.email);
              setPw(s.pw);
              go(s.email, s.pw);
            }}
          >
            {s.label}
          </button>
        ))}
      </div>
      {err && <div className="err">{err}</div>}
      <p style={{ fontSize: ".68rem", color: "var(--rule)", marginTop: 14 }}>
        Division staff · staff123 · admin · admin123
      </p>
    </div>
  );
}

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
      {isInternal(profile) && <div onClick={()=>nav("/intelligence")} className="card" style={{cursor:"pointer",borderTop:"3px solid #7C5CBF",textAlign:"center",padding:"24px 16px"}}>
        <h3 style={{color:"#7C5CBF",fontSize:".95rem",marginBottom:6,textTransform:"none",letterSpacing:0}}>G.O.D.S Intelligence</h3>
        <p style={{fontSize:".72rem"}}>Internal · Open →</p></div>}
    </div>
  </div>);
}

function Guarded({ profile, sysKey, children }: { profile: Profile; sysKey: string; children: ReactNode }) {
  if (!profile.systems.some(s => s.key === sysKey) && !profile.is_admin) {
    return <div className="main"><div className="top"><h2>Access denied</h2><span className="badge">🔒 403</span></div></div>;
  }
  return <>{children}</>;
}

function Shell({ profile, children }: { profile: Profile; children: ReactNode }) {
  const nav = useNavigate();
  return (
    <div className="shell">
      <aside className="side">
        <div className="logo">G.O.D.S</div>
        <div className="sub">INTERNAL OPERATING CORE</div>
        <div className="who">{profile.email}<br/>{profile.role}/{profile.division}</div>
        <NavLink to="/launcher" className={({isActive})=>isActive?"active":""}>Launcher</NavLink>
        {profile.systems.some(s=>s.key==="holdings-overview") && <NavLink to="/overview" className={({isActive})=>isActive?"active":""}>Holdings Overview</NavLink>}
        {(profile.systems.some(s=>["seths-ops","madiba-ops","ts-ops"].includes(s.key))) && <div className="sec">Division Operations</div>}
        {profile.systems.some(s=>s.key==="seths-ops") && <NavLink to="/seths" className={({isActive})=>isActive?"active":""}>SETHS Ops</NavLink>}
        {profile.systems.some(s=>s.key==="madiba-ops") && <NavLink to="/madiba" className={({isActive})=>isActive?"active":""}>MADIBA Ops</NavLink>}
        {profile.systems.some(s=>s.key==="ts-ops") && <NavLink to="/ts" className={({isActive})=>isActive?"active":""}>TS Industries Ops</NavLink>}
        {profile.systems.some(s=>s.key==="udoc-gov") && <><div className="sec">Governance</div><NavLink to="/udoc" className={({isActive})=>isActive?"active":""}>UDOC Governance</NavLink></>}
        {isInternal(profile) && <><div className="sec">Intelligence</div><NavLink to="/intelligence" className={({isActive})=>isActive?"active":""}>G.O.D.S Intelligence</NavLink></>}
        <button className="btn" style={{marginTop:24}} onClick={()=>{ setToken(null); nav("/"); window.location.reload(); }}>Sign out</button>
      </aside>
      <div className="main">{children}</div>
    </div>
  );
}

export default function App() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [booting, setBooting] = useState(true);
  async function boot() {
    if (!getToken()) { setBooting(false); return; }
    try {
      const me = await api.get("/auth/me");
      setProfile(me);
    } catch {
      setToken(null);
    }
    setBooting(false);
  }
  useEffect(() => { boot(); }, []);
  if (booting) return <div className="login"><p>Loading…</p></div>;
  if (!profile) return <Login onAuth={() => boot()} />;
  return (<BrowserRouter><Shell profile={profile}><Routes>
    <Route path="/launcher" element={<Launcher profile={profile}/>}/>
    <Route path="/overview" element={<Guarded profile={profile} sysKey="holdings-overview"><Overview/></Guarded>}/>
    <Route path="/seths" element={<Guarded profile={profile} sysKey="seths-ops"><SethsOps/></Guarded>}/>
    <Route path="/madiba" element={<Guarded profile={profile} sysKey="madiba-ops"><MadibaOps/></Guarded>}/>
    <Route path="/ts" element={<Guarded profile={profile} sysKey="ts-ops"><TSOps/></Guarded>}/>
    <Route path="/udoc" element={<Guarded profile={profile} sysKey="udoc-gov"><UDOCGov/></Guarded>}/>
    <Route path="/intelligence" element={isInternal(profile)?<Intelligence/>:<div className="main"><div className="top"><h2>Access denied</h2><span className="badge">🔒 403</span></div></div>}/>
    <Route path="*" element={<Navigate to="/launcher"/>}/>
  </Routes></Shell></BrowserRouter>);
}
