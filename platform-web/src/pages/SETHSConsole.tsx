import { useEffect, useState } from "react";
import { api } from "../lib/api";
export function SETHSConsole() {
  const [m, setM] = useState<any>(null);
  const refresh = () => api.get("/seths/metrics").then(setM).catch(() => {});
  useEffect(() => { refresh(); }, []);
  async function enrol() { await api.post("/seths/enrol", { count: 10 }); refresh(); }
  return (<>
    <div className="topbar"><h2>SETHS — Workforce Reintegration</h2><span className="pill">NQF 5 · 118707</span></div>
    <div className="grid">
      <div className="card"><h3>Total Learners</h3><div className="metric">{m?.total ?? "—"}</div></div>
      <div className="card"><h3>Completed</h3><div className="metric">{m?.completed ?? "—"}</div></div>
      <div className="card"><h3>Placed</h3><div className="metric">{m?.placed ?? "—"}</div></div>
      <div className="card"><h3>Placement Rate</h3><div className="metric">{m ? (m.placement_rate*100).toFixed(0)+"%" : "—"}</div></div>
      <div className="card"><h3>Monthly Output</h3><div className="metric">R{m?.monthly_economic_output?.toLocaleString() ?? "—"}</div></div>
    </div>
    <button className="btn" onClick={enrol}>Enrol cohort (10)</button>
  </>);
}
