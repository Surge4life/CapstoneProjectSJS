import { useEffect, useState } from "react";
import { api } from "../lib/api";
export function TSConsole() {
  const [p, setP] = useState<any[]>([]);
  const [m, setM] = useState<any>(null);
  const refresh = () => { api.get("/ts/projects").then(setP); api.get("/ts/metrics").then(setM).catch(()=>{}); };
  useEffect(refresh, []);
  async function deploy() {
    await api.post("/ts/projects", { sector: "ENERGY", name: "Solar SPV", workers_deployed: 4,
      monthly_revenue: 2200000, operating_margin: 0.32 }); refresh();
  }
  return (<>
    <div className="topbar"><h2>TS Industries — Production SPVs</h2><span className="pill">Real economic output</span></div>
    <div className="grid">
      <div className="card"><h3>Projects</h3><div className="metric">{m?.projects ?? "—"}</div></div>
      <div className="card"><h3>Workers Absorbed</h3><div className="metric">{m?.workers_absorbed ?? "—"}</div></div>
      <div className="card"><h3>Monthly Profit</h3><div className="metric">R{m?.monthly_operating_profit?.toLocaleString() ?? "—"}</div></div>
    </div>
    <div className="card"><h3>SPV Portfolio</h3>
      <table><thead><tr><th>SPV</th><th>Sector</th><th>Workers</th><th>Revenue</th></tr></thead>
      <tbody>{p.map(x => <tr key={x.spv_id}><td>{x.spv_id}</td><td>{x.sector}</td>
        <td>{x.workers}</td><td>R{x.monthly_revenue.toLocaleString()}</td></tr>)}</tbody></table>
    </div>
    <button className="btn" onClick={deploy}>Deploy energy SPV</button>
  </>);
}
