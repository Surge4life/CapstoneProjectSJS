import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { api, getToken, setToken } from "./api";
import { Login } from "./Login";

export function App() {
  const [authed, setAuthed] = useState(!!getToken());
  const [kpis, setKpis] = useState<any>(null);
  const [chart, setChart] = useState<any[]>([]);
  const [records, setRecords] = useState<any[]>([]);
  const [busy, setBusy] = useState(false);

  async function load() {
    try {
      setKpis(await api.kpis());
      const inflow = (await api.timeseries("inflow")).series;
      const recycled = (await api.timeseries("recycled")).series;
      const merged = inflow.map((i: any) => ({
        period: i.period, inflow: i.value,
        recycled: recycled.find((r: any) => r.period === i.period)?.value ?? 0,
      }));
      setChart(merged);
      setRecords((await api.records(40)).records);
    } catch { /* unauth */ }
  }
  useEffect(() => { if (authed) load(); }, [authed]);

  async function runCycle() {
    setBusy(true);
    try {
      const month = chart.length + 1;
      await api.post("/madiba/allocate", { month, total_inflow: 1894000 + month * 120000 });
      await load();
    } finally { setBusy(false); }
  }

  if (!authed) return <Login onAuth={() => setAuthed(true)} />;
  return (
    <div className="shell">
      <div className="hdr">
        <div className="brand"><span className="gods">G.O.D.S Holdings</span>
          <h1>MADIBA Capital</h1><div className="sub">Capital Recycling · Pillar 2 (&gt;50% recycle)</div></div>
        <div><span className="pill">UDOC-recorded</span>
          <button className="btn" style={{ marginLeft: 12 }} onClick={() => { setToken(null); location.reload(); }}>Sign out</button></div>
      </div>

      <div className="grid">
        <div className="card"><h3>Total Inflow</h3><div className="metric">R{(kpis?.total_inflow ?? 0).toLocaleString()}</div></div>
        <div className="card"><h3>Total Recycled</h3><div className="metric">R{(kpis?.total_recycled ?? 0).toLocaleString()}</div></div>
        <div className="card"><h3>Recycle Ratio</h3><div className="metric">{kpis ? (kpis.recycle_ratio * 100).toFixed(0) + "%" : "—"}<small>Pillar 2 needs &gt;50%</small></div></div>
      </div>

      <div className="panel">
        <h2>Inflow vs Recycled-to-SETHS (UDOC analytics)</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chart}>
            <CartesianGrid stroke="#1d3050" strokeDasharray="3 3" />
            <XAxis dataKey="period" stroke="#D0C8B0" fontSize={12} />
            <YAxis stroke="#D0C8B0" fontSize={12} />
            <Tooltip contentStyle={{ background: "#0C1A2E", border: "1px solid #1d3050", color: "#F5F0E8" }} />
            <Legend />
            <Bar dataKey="inflow" fill="#1d3050" name="Inflow" />
            <Bar dataKey="recycled" fill="#C9A84C" name="Recycled → SETHS" />
          </BarChart>
        </ResponsiveContainer>
        <button className="btn" disabled={busy} onClick={runCycle}>{busy ? "Processing…" : "Run next capital cycle"}</button>
      </div>

      <div className="panel">
        <h2>UDOC Event Records</h2>
        <table><thead><tr><th>Event</th><th>Metric</th><th>Value</th><th>Period</th></tr></thead>
          <tbody>{records.map(r => <tr key={r.id}>
            <td>{r.event_type}</td><td>{r.metric_name}</td><td>R{r.metric_value.toLocaleString()}</td><td>{r.period}</td></tr>)}
          </tbody></table>
      </div>
      <div className="foot">G.O.D.S HOLDINGS · MADIBA CAPITAL · DATA RECORDED & GOVERNED BY UDOC</div>
    </div>
  );
}
