import { useEffect, useState } from "react";
import { api, setToken } from "../api";

export function StudentPortal({ onBack }: { onBack: () => void }) {
  const [ref, setRef] = useState(localStorage.getItem("stu_ref") || "");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [profile, setProfile] = useState<any>(null);
  const [opps, setOpps] = useState<any[]>([]);
  const [msg, setMsg] = useState("");

  async function ensureToken() {
    if (!api.get) return;
    try { await api.login("admin@gods.za", "admin123"); } catch { /* demo auth */ }
  }
  async function load() {
    if (!ref) return;
    try {
      setProfile(await api.get(`/portal/student/${ref}`));
      setOpps(await api.get(`/portal/student/opportunities/open`));
    } catch (e: any) { setMsg(e.message); }
  }
  useEffect(() => { ensureToken().then(load); }, [ref]);

  async function register() {
    setMsg("");
    try {
      const r = await api.post("/portal/student/register", { full_name: name, email });
      localStorage.setItem("stu_ref", r.student_ref); setRef(r.student_ref);
      setMsg(`Registered as ${r.student_ref}`);
    } catch (e: any) { setMsg(e.message); }
  }
  async function setProgress(pct: number) {
    await ensureToken();
    await api.post(`/portal/student/${ref}/progress?pct=${pct}`); load();
  }
  async function apply(oid: number) {
    await ensureToken();
    try { await api.post(`/portal/student/${ref}/apply/${oid}`); setMsg("Application submitted"); load(); }
    catch (e: any) { setMsg(e.message); }
  }

  return (
    <div className="wrap">
      <div className="hdr"><div><span className="gods">G.O.D.S · SETHS</span><h2>Student Portal</h2></div>
        <span className="back" onClick={onBack}>← portals</span></div>

      {!ref ? (
        <div className="card"><h3>Register as a learner</h3>
          <input placeholder="Full name" value={name} onChange={e => setName(e.target.value)} />
          <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
          <button className="btn" onClick={register}>Enrol in SETHS</button>
        </div>
      ) : (
        <>
          <div className="card"><h3>My Programme</h3>
            {profile && <>
              <div className="metric">{profile.full_name}</div>
              <p style={{ fontSize: ".82rem" }}>{profile.qualification} · NQF {profile.nqf_level} ·
                status <span className={`tag ${profile.status}`}>{profile.status}</span></p>
              <p style={{ margin: "10px 0", fontSize: ".82rem" }}>Progress: {profile.progress_pct}%</p>
              <div style={{ display: "flex", gap: 8 }}>
                <button className="btn sm" onClick={() => setProgress(50)}>Mark 50%</button>
                <button className="btn sm" onClick={() => setProgress(100)}>Mark complete</button>
              </div>
            </>}
          </div>
          <div className="card"><h3>Open Opportunities</h3>
            <table><thead><tr><th>Role</th><th>Employer</th><th>Stipend</th><th></th></tr></thead>
              <tbody>{opps.map(o => <tr key={o.id}>
                <td>{o.title}</td><td>{o.employer}</td><td>R{o.monthly_stipend.toLocaleString()}</td>
                <td><button className="btn sm" onClick={() => apply(o.id)}>Apply</button></td></tr>)}
                {opps.length === 0 && <tr><td colSpan={4} style={{ color: "var(--rule)" }}>No open roles yet</td></tr>}
              </tbody></table>
          </div>
        </>
      )}
      {msg && <div className="ok">{msg}</div>}
      <div className="foot">DATA RECORDED & GOVERNED BY UDOC</div>
    </div>
  );
}
