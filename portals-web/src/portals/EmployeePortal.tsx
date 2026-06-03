import { useEffect, useState } from "react";
import { api } from "../api";

export function EmployeePortal({ onBack }: { onBack: () => void }) {
  const [ref, setRef] = useState(localStorage.getItem("emp_ref") || "");
  const [refInput, setRefInput] = useState("");
  const [profile, setProfile] = useState<any>(null);
  const [payslip, setPayslip] = useState<any>(null);
  const [hours, setHours] = useState(160);
  const [msg, setMsg] = useState("");

  async function ensureToken() { try { await api.login("admin@gods.za", "admin123"); } catch {} }
  async function load() {
    if (!ref) return;
    try {
      setProfile(await api.get(`/portal/employee/${ref}`));
      setPayslip(await api.get(`/portal/employee/${ref}/payslip`));
    } catch (e: any) { setMsg(e.message); }
  }
  useEffect(() => { load(); }, [ref]);

  function connect() { localStorage.setItem("emp_ref", refInput); setRef(refInput); }
  async function submitTimesheet() {
    await ensureToken();
    await api.post(`/portal/employee/${ref}/timesheet`, { hours }); setMsg("Timesheet submitted"); load();
  }

  return (
    <div className="wrap">
      <div className="hdr"><div><span className="gods">G.O.D.S · TS Industries</span><h2>Employee Portal</h2></div>
        <span className="back" onClick={onBack}>← portals</span></div>

      {!ref ? (
        <div className="card"><h3>Access your employee record</h3>
          <p style={{ fontSize: ".78rem", marginBottom: 8 }}>Enter the EMP- reference issued when you were placed.</p>
          <input placeholder="EMP-xxxxxxxx" value={refInput} onChange={e => setRefInput(e.target.value)} />
          <button className="btn" onClick={connect}>Open my portal</button>
        </div>
      ) : (
        <>
          <div className="card"><h3>My Employment</h3>
            {profile && <>
              <div className="metric">{profile.full_name}</div>
              <p style={{ fontSize: ".82rem" }}>{profile.role || "Worker"} · {profile.division} ·
                status <span className={`tag ${profile.status}`}>{profile.status}</span></p>
              <p style={{ fontSize: ".82rem", marginTop: 6 }}>Salary: R{profile.monthly_salary?.toLocaleString()}/mo</p>
            </>}
          </div>
          <div className="card"><h3>Submit Timesheet</h3>
            <input type="number" value={hours} onChange={e => setHours(Number(e.target.value))} />
            <button className="btn" onClick={submitTimesheet}>Submit hours</button>
          </div>
          {payslip && <div className="card"><h3>Payslip · {payslip.period}</h3>
            <table><tbody>
              <tr><td>Gross</td><td>R{payslip.gross.toLocaleString()}</td></tr>
              <tr><td>UIF (1%)</td><td>-R{payslip.uif.toLocaleString()}</td></tr>
              <tr><td>PAYE</td><td>-R{payslip.paye.toLocaleString()}</td></tr>
              <tr><td style={{ color: "var(--ok)" }}><b>Net pay</b></td><td style={{ color: "var(--ok)" }}><b>R{payslip.net.toLocaleString()}</b></td></tr>
            </tbody></table></div>}
        </>
      )}
      {msg && <div className="ok">{msg}</div>}
      <div className="foot">TS INDUSTRIES WORKFORCE · DATA GOVERNED BY UDOC</div>
    </div>
  );
}
