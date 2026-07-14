import { useState } from "react";
import { api } from "./api";
export function Login({ onAuth }: { onAuth: () => void }) {
  const [email, setEmail] = useState("admin@gods.local");
  const [pw, setPw] = useState("admin123");
  const [err, setErr] = useState("");
  async function submit(){ try{ await api.login(email,pw); onAuth(); }catch(e:any){ setErr(e.message||"login failed"); } }
  return (<div className="login">
    <span className="gods">G.O.D.S Holdings</span>
    <h1>{api.division}</h1>
    <p style={{fontSize:".8rem",margin:"6px 0 18px"}}>Sign in to the division platform</p>
    <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="email"/>
    <input type="password" value={pw} onChange={e=>setPw(e.target.value)} placeholder="password"/>
    <button className="btn" onClick={submit}>Sign In</button>
    {err && <div className="err">{err}</div>}
  </div>);
}
