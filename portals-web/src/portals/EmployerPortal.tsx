import { useEffect, useState } from "react";
import { api } from "../api";

export function EmployerPortal({ onBack }: { onBack: () => void }) {
  const [eid, setEid] = useState(localStorage.getItem("emp_id") || "");
  const [org, setOrg] = useState(""); const [cemail, setCemail] = useState("");
  const [opps, setOpps] = useState<any[]>([]);
  const [title, setTitle] = useState(""); const [stipend, setStipend] = useState(15000);
  const [applicants, setApplicants] = useState<any[]>([]);
  const [activeOpp, setActiveOpp] = useState<number | null>(null);
  const [msg, setMsg] = useState("");

  async function ensureToken() { try { await api.login("admin@gods.za", "admin123"); } catch {} }
  async function load() {
    if (!eid) return;
    await ensureToken();
    try { setOpps(await api.get(`/portal/employer/${eid}/opportunities`)); } catch (e: any) { setMsg(e.message); }
  }
  useEffect(() => { load(); }, [eid]);

  async function register() {
    try {
      const r = await api.post("/portal/employer/register", { org_name: org, contact_email: cemail });
      localStorage.setItem("emp_id", String(r.employer_id)); setEid(String(r.employer_id));
      setMsg(`Registered as employer #${r.employer_id}`);
    } catch (e: any) { setMsg(e.message); }
  }
  async function postOpp() {
    await ensureToken();
    await api.post("/portal/employer/opportunities", { employer_id: Number(eid), title, sector: "GENERAL", positions: 2, monthly_stipend: stipend });
    setTitle(""); load();
  }
  async function viewApplicants(oid: number) {
    await ensureToken(); setActiveOpp(oid);
    setApplicants(await api.get(`/portal/employer/opportunities/${oid}/applicants`));
  }
  async function offer(appId: number) {
    await ensureToken();
    const r = await api.post(`/portal/employer/applications/${appId}/offer`);
    setMsg(`Offer made → ${r.employee_ref} created as TS employee`);
    if (activeOpp) viewApplicants(activeOpp);
  }

  return (
    <div className="wrap">
      <div className="hdr"><div><span className="gods">G.O.D.S · Employer</span><h2>Employer Portal</h2></div>
        <span className="back" onClick={onBack}>← portals</span></div>

      {!eid ? (
        <div className="card"><h3>Register your organisation</h3>
          <input placeholder="Organisation name" value={org} onChange={e => setOrg(e.target.value)} />
          <input placeholder="Contact email" value={cemail} onChange={e => setCemail(e.target.value)} />
          <button className="btn" onClick={register}>Register</button>
        </div>
      ) : (
        <>
          <div className="card"><h3>Post an opportunity</h3>
            <input placeholder="Role title" value={title} onChange={e => setTitle(e.target.value)} />
            <input type="number" placeholder="Monthly stipend" value={stipend} onChange={e => setStipend(Number(e.target.value))} />
            <button className="btn" onClick={postOpp}>Post (2 positions)</button>
          </div>
          <div className="card"><h3>My Opportunities</h3>
            <table><thead><tr><th>Role</th><th>Positions</th><th>Status</th><th></th></tr></thead>
              <tbody>{opps.map(o => <tr key={o.id}>
                <td>{o.title}</td><td>{o.positions}</td><td><span className={`tag ${o.status}`}>{o.status}</span></td>
                <td><button className="btn sm" onClick={() => viewApplicants(o.id)}>Applicants</button></td></tr>)}
              </tbody></table>
          </div>
          {activeOpp && <div className="card"><h3>Applicants for opportunity #{activeOpp}</h3>
            <table><thead><tr><th>Candidate</th><th>Progress</th><th>State</th><th></th></tr></thead>
              <tbody>{applicants.map(a => <tr key={a.application_id}>
                <td>{a.full_name} ({a.student_ref})</td><td>{a.progress_pct}%</td>
                <td><span className={`tag ${a.state}`}>{a.state}</span></td>
                <td>{a.state !== "PLACED" && <button className="btn sm" onClick={() => offer(a.application_id)}>Offer</button>}</td></tr>)}
                {applicants.length === 0 && <tr><td colSpan={4} style={{ color: "var(--rule)" }}>No applicants yet</td></tr>}
              </tbody></table>
          </div>}
        </>
      )}
      {msg && <div className="ok">{msg}</div>}
      <div className="foot">PLACEMENTS FLOW SETHS → TS INDUSTRIES · GOVERNED BY UDOC</div>
    </div>
  );
}
