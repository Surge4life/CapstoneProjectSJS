import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { api, getToken, setToken } from "./api";
import { Login } from "./Login";

const SECTORS = ["ENERGY", "HOUSING", "AGRITECH", "WATER", "LOGISTICS"];

export function App() {
  const [authed, setAuthed] = useState(!!getToken());
  const [kpis, setKpis] = useState<any>(null);
  const [projects, setProjects] = useState<any[]>([]);
  const [sector, setSector] = useState("ENERGY");
  const [busy, setBusy] = useState(false);

  async function load() {
    try {
      setKpis(await api.kpis());
      setProjects(await api.get("/ts/projects"));
    } catch { /* unauth */ }
  }
  useEffect(() => { if (authed) load(); }, [authed]);

  async function deploy() {
    setBusy(true);
    try {
      await api.post("/ts/projects", { sector, name: `${sector} SPV ${projects.length + 1}`,
        workers_deployed: 4 + Math.floor(Math.random() * 6),
        monthly_revenue: 1500000 + Math.floor(Math.random() * 2000000), operating_margin: 0.3 });
      await load();
    } finally { setBusy(false); }
  }

  const chart = projects.map(p => ({ name: p.spv_id.slice(0, 12), revenue: p.monthly_revenue }));
  if (!authed) return <Login onAuth={() => setAuthed(true)} />;
  return (
    <div className="shell">
      <div className="hdr">
        <div className="brand"><span className="gods">G.O.D.S Holdings</span>
          <h1>TS Industries</h1><div className="sub">Production SPVs · absorbs SETHS-placed workers</div></div>
        <div><span className="pill">UDOC-recorded</span>
          <button className="btn" style={{ marginLeft: 12 }} onClick={() => { setToken(null); location.reload(); }}>Sign out</button></div>
      </div>

      <div className="grid">
        <div className="card"><h3>Total Revenue</h3><div className="metric">R{(kpis?.total_revenue ?? 0).toLocaleString()}</div></div>
        <div className="card"><h3>Total Profit</h3><div className="metric">R{(kpis?.total_profit ?? 0).toLocaleString()}</div></div>
        <div className="card"><h3>Workers Absorbed</h3><div className="metric">{kpis?.workers_absorbed ?? "—"}</div></div>
        <div className="card"><h3>Avg Margin</h3><div className="metric">{kpis ? (kpis.avg_margin * 100).toFixed(0) + "%" : "—"}</div></div>
      </div>

      <div className="panel">
        <h2>SPV Revenue (UDOC analytics)</h2>
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={chart}>
            <CartesianGrid stroke="#1d3050" strokeDasharray="3 3" />
            <XAxis dataKey="name" stroke="#D0C8B0" fontSize={11} />
            <YAxis stroke="#D0C8B0" fontSize={12} />
            <Tooltip contentStyle={{ background: "#0C1A2E", border: "1px solid #1d3050", color: "#F5F0E8" }} />
            <Bar dataKey="revenue" fill="#4CAF7D" name="Monthly Revenue" />
          </BarChart>
        </ResponsiveContainer>
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          <select value={sector} onChange={e => setSector(e.target.value)}
            style={{ background: "#060E1C", color: "#F5F0E8", border: "1px solid #1d3050", padding: 9, borderRadius: 6 }}>
            {SECTORS.map(s => <option key={s}>{s}</option>)}
          </select>
          <button className="btn" disabled={busy} onClick={deploy}>{busy ? "Deploying…" : "Deploy SPV"}</button>
        </div>
      </div>

      <div className="panel">
        <h2>SPV Portfolio</h2>
        <table><thead><tr><th>SPV</th><th>Sector</th><th>Workers</th><th>Revenue</th></tr></thead>
          <tbody>{projects.map(p => <tr key={p.spv_id}>
            <td>{p.spv_id}</td><td>{p.sector}</td><td>{p.workers}</td>
            <td>R{p.monthly_revenue.toLocaleString()}</td></tr>)}
          </tbody></table>
      </div>
      <div className="foot">G.O.D.S HOLDINGS · TS INDUSTRIES · DATA RECORDED & GOVERNED BY UDOC</div>
    </div>
  );
}
