import { useState } from "react";
import { api } from "../lib/api";

export function Login({ onAuth }: { onAuth: () => void }) {
  const [email, setEmail] = useState("admin@gods.za");
  const [pw, setPw] = useState("admin123");
  const [err, setErr] = useState("");
  async function submit() {
    try { await api.login(email, pw); onAuth(); }
    catch (e: any) { setErr(e.message || "login failed"); }
  }
  return (
    <div className="login">
      <h1>G.O.D.S</h1>
      <p>Sovereign AI Governance Platform · sign in</p>
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="email" />
      <input type="password" value={pw} onChange={e => setPw(e.target.value)} placeholder="password" />
      <button className="btn" onClick={submit}>Sign In</button>
      {err && <div className="err">{err}</div>}
    </div>
  );
}
