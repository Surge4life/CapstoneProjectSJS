import { useEffect, useState } from "react";
import { api } from "../lib/api";
export function MADIBAConsole() {
  const [m, setM] = useState<any>(null);
  const refresh = () => api.get("/madiba/metrics").then(setM).catch(() => {});
  useEffect(() => { refresh(); }, []);
  async function cycle() {
    const month = (m?.cycles ?? 0) + 1;
    await api.post("/madiba/allocate", { month, total_inflow: 1894000 }); refresh();
  }
  return (<>
    <div className="topbar"><h2>MADIBA — Capital Recycling</h2><span className="pill">Pillar 2 · &gt;50% recycle</span></div>
    <div className="grid">
      <div className="card"><h3>Cycles Run</h3><div className="metric">{m?.cycles ?? "—"}</div></div>
      <div className="card"><h3>Cumulative Recycled</h3><div className="metric">R{m?.cumulative_recycled?.toLocaleString() ?? "—"}</div></div>
    </div>
    <div className="card"><h3>Allocation Series</h3>
      <table><thead><tr><th>Month</th><th>Inflow</th><th>Recycled to SETHS</th></tr></thead>
      <tbody>{m?.series?.map((c: any) => <tr key={c.month}><td>{c.month}</td>
        <td>R{c.inflow.toLocaleString()}</td><td>R{c.recycled.toLocaleString()}</td></tr>)}</tbody></table>
    </div>
    <button className="btn" onClick={cycle}>Run next capital cycle</button>
  </>);
}
