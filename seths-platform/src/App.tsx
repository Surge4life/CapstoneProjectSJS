import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { api, getToken, setToken } from "./api";
import { Login } from "./Login";

export function App() {
  const [authed, setAuthed] = useState(!!getToken());
  const [kpis, setKpis] = useState<any>(null);
  const [series, setSeries] = useState<any[]>([]);
  const [records, setRecords] = useState<any[]>([]);
  const [busy, setBusy] = useState(false);

  async function load() {
    try {
      setKpis(await api.kpis());
      setSeries((await api.timeseries("monthly_value")).series);
      setRecords((await api.records(40)).records);
    } catch { /* not logged in yet */ }
  }
  useEffect(() => { if (authed) load(); }, [authed]);

  async function enrolCohort() {
    setBusy(true);
    try {
      const r = await api.post("/seths/enrol", { count: 10 });
      // advance 4 to placed so analytics shows movement
      for (const ref of r.refs.slice(0, 4)) {
        await api.post(`/seths/${ref}/advance`, {}); // ENROLLED→COMPLETED
        await api.post(`/seths/${ref}/advance`, {}); // COMPLETED→PLACED
      }
      await load();
    } finally { setBusy(false); }
  }

  if (!authed) return <Login onAuth={() => setAuthed(true)} />;
  return (
    <div className="shell">
      <div className="hdr">
        <div className="brand"><span className="gods">G.O.D.S Holdings</span>
          <h1>SETHS</h1><div className="sub">Workforce Reintegration · NQF 5 · 118707</div></div>
        <div>
          <span className="pill">UDOC-recorded</span>
          <button className="btn" style={{ marginLeft: 12 }} onClick={() => { setToken(null); location.reload(); }}>Sign out</button>
        </div>
      </div>

      <div className="grid">
        <div className="card"><h3>Enrolled</h3><div className="metric">{kpis?.enrolled ?? "—"}</div></div>
        <div className="card"><h3>Placed</h3><div className="metric">{kpis?.placed ?? "—"}</div></div>
        <div className="card"><h3>Placement Rate</h3><div className="metric">{kpis ? (kpis.placement_rate * 100).toFixed(0) + "%" : "—"}</div></div>
        <div className="card"><h3>Monthly Output</h3><div className="metric">R{(kpis?.monthly_output ?? 0).toLocaleString()}</div></div>
      </div>

      <div className="panel">
        <h2>Economic Output Over Time (UDOC analytics)</h2>
        <ResponsiveContainer width="100%" height={240}>
          <LineChart data={series}>
            <CartesianGrid stroke="#1d3050" strokeDasharray="3 3" />
            <XAxis dataKey="period" stroke="#D0C8B0" fontSize={12} />
            <YAxis stroke="#D0C8B0" fontSize={12} />
            <Tooltip contentStyle={{ background: "#0C1A2E", border: "1px solid #1d3050", color: "#F5F0E8" }} />
            <Line type="monotone" dataKey="value" stroke="#3FA7D6" strokeWidth={2} dot={{ r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
        <button className="btn" disabled={busy} onClick={enrolCohort}>{busy ? "Processing…" : "Enrol cohort of 10 (place 4)"}</button>
      </div>

      <div className="panel">
        <h2>UDOC Event Records</h2>
        <table><thead><tr><th>Event</th><th>Entity</th><th>Metric</th><th>Value</th><th>Period</th></tr></thead>
          <tbody>{records.map(r => <tr key={r.id}>
            <td>{r.event_type}</td><td>{r.entity_ref || "—"}</td><td>{r.metric_name}</td>
            <td>{r.metric_value}</td><td>{r.period}</td></tr>)}
          </tbody></table>
      </div>
      <div className="foot">G.O.D.S HOLDINGS · SETHS PLATFORM · DATA RECORDED & GOVERNED BY UDOC</div>
    </div>
  );
}
