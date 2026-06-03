import { useEffect, useState } from "react";
import { api } from "../lib/api";

export function UDOCConsole() {
  const [models, setModels] = useState<any[]>([]);
  const [result, setResult] = useState<any>(null);
  const [scenario, setScenario] = useState("healthy");
  const refresh = () => api.get("/registry/models").then(setModels).catch(() => {});
  useEffect(() => { refresh(); }, []);

  async function decide() {
    const base: any = { model_id: "model-001" };
    if (scenario === "biased") Object.assign(base, { risk_tier: "HIGH", priv_favorable: 600, unpriv_favorable: 300, ecs: 0.3 });
    if (scenario === "breach") Object.assign(base, { traceroute: 0.4 });
    try { setResult(await api.post("/decisions", base)); } catch (e: any) { setResult({ error: e.message }); }
  }
  return (
    <>
      <div className="topbar"><h2>UDOC Governance Console (public)</h2><span className="pill">EVA 6-D · fail-closed</span></div>
      <div className="card">
        <h3>Live Decision Path</h3>
        <div style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 14 }}>
          <select value={scenario} onChange={e => setScenario(e.target.value)}>
            <option value="healthy">Healthy model</option>
            <option value="biased">Biased + high-risk</option>
            <option value="breach">Sovereignty breach</option>
          </select>
          <button className="btn" onClick={decide}>Run governance decision</button>
        </div>
        {result && !result.error && (
          <div>
            <p>Decision: <span className={`tag ${result.decision}`}>{result.decision}</span>
              &nbsp; SVS <b>{result.svs}</b> · risk <b>{result.risk}</b> · sovereign <b>{String(result.sovereign)}</b></p>
            <p style={{ fontSize: ".78rem", marginTop: 6 }}>latency {result.latency_ms}ms (budget {result.budget_ms}ms ·
              within budget {String(result.within_budget)}) · seal {result.seal?.slice(0, 24)}…</p>
            {result.block_reasons?.length > 0 && <ul style={{ marginTop: 8, fontSize: ".78rem", color: "var(--bad)" }}>
              {result.block_reasons.map((r: string, i: number) => <li key={i}>• {r}</li>)}</ul>}
          </div>
        )}
        {result?.error && <p className="err">{result.error}</p>}
      </div>
      <div className="card">
        <h3>Model Registry</h3>
        <table><thead><tr><th>Model</th><th>Risk Tier</th><th>Jurisdiction</th><th>Status</th></tr></thead>
          <tbody>{models.map(m => <tr key={m.model_id}>
            <td>{m.model_id}</td><td>{m.risk_tier}</td><td>{m.jurisdiction}</td>
            <td><span className={`tag ${m.status}`}>{m.status}</span></td></tr>)}
          </tbody></table>
      </div>
    </>
  );
}
