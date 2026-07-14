import { useEffect, useState } from "react";
import { api } from "../lib/api";

export function AdminDash() {
  const [s, setS] = useState<any>(null);
  const [loop, setLoop] = useState<any>(null);
  useEffect(() => {
    api.get("/admin/status").then(setS).catch(() => {});
    api.get("/intelligence/loop-snapshot").then(setLoop).catch(() => {});
  }, []);
  return (
    <>
      <div className="topbar"><h2>GODS Admin Mainframe</h2><span className="pill">LIVE</span></div>
      <div className="grid">
        <div className="card"><h3>Registered Models</h3><div className="metric">{s?.models ?? "—"}</div></div>
        <div className="card"><h3>Governance Decisions</h3><div className="metric">{s?.decisions ?? "—"}</div></div>
        <div className="card"><h3>SETHS Learners</h3><div className="metric">{s?.learners ?? "—"}</div></div>
        <div className="card"><h3>TS Projects</h3><div className="metric">{s?.ts_projects ?? "—"}</div></div>
        <div className="card"><h3>Open Oversight</h3><div className="metric">{s?.open_oversight ?? "—"}</div></div>
        <div className="card"><h3>Users</h3><div className="metric">{s?.users ?? "—"}</div></div>
      </div>
      <div className="card">
        <h3>Closed-Loop Snapshot</h3>
        {loop ? <p style={{ color: "var(--white)" }}>
          {loop.loop} — SETHS placed <b>{loop.seths_placed}</b> · TS profit <b>R{loop.ts_monthly_profit?.toLocaleString()}</b> ·
          MADIBA recycled <b>R{loop.madiba_cumulative_recycled?.toLocaleString()}</b> · UDOC decisions <b>{loop.udoc_decisions}</b>
        </p> : <p>Loading…</p>}
      </div>
    </>
  );
}
