import { useEffect, useState } from "react";
import { api } from "../api";

export function Overview() {
  const [s, setS] = useState<any>(null);
  const [loop, setLoop] = useState<any>(null);
  const [chain, setChain] = useState<any>(null);
  const [sov, setSov] = useState<any>(null);
  const [bias, setBias] = useState<any>(null);
  const [audit, setAudit] = useState<any[]>([]);
  const [seths, setSeths] = useState<any>(null);
  const [ts, setTs] = useState<any>(null);
  const [madiba, setMadiba] = useState<any>(null);
  const [demo, setDemo] = useState<any>(null);
  const [gbs, setGbs] = useState<any>(null);

  async function load() {
    api.get("/admin/status").then(setS).catch(() => {});
    api.get("/intelligence/loop-snapshot").then(setLoop).catch(() => {});
    api.get("/audit/chain/verify").then(setChain).catch(() => {});
    api.get("/sovereignty/posture").then(setSov).catch(() => {});
    api.get("/bias/scan").then(setBias).catch(() => {});
    api.get("/audit/records").then(setAudit).catch(() => {});
    api.get("/analytics/SETHS/kpis").then(setSeths).catch(() => {});
    api.get("/ts/metrics").then(setTs).catch(() => {});
    api.get("/madiba/metrics").then(setMadiba).catch(() => {});
    api.get("/udoc/demo/ready").then(setDemo).catch(() => {});
    api.get("/gis/gbs/architecture").then(setGbs).catch(() => {});
  }

  useEffect(() => {
    load();
    const t = setInterval(load, 10000);
    return () => clearInterval(t);
  }, []);

  const sovPct = sov ? (sov.sovereign_rate * 100).toFixed(0) + "%" : "—";

  return (
    <>
      <div className="top">
        <h2>Holdings Overview</h2>
        <span className="badge">🔒 INTERNAL · LIVE</span>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Models governed</h3>
          <div className="metric">{s?.models ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Decisions</h3>
          <div className="metric">{s?.decisions ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Open oversight</h3>
          <div className="metric">{s?.open_oversight ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Sovereignty</h3>
          <div className="metric">{sovPct}</div>
        </div>
        <div className="card">
          <h3>Demo ready</h3>
          <div className="metric" style={{ color: demo?.ready ? "var(--ok)" : "var(--warn)" }}>
            {demo ? String(demo.ready) : "—"}
          </div>
        </div>
        <div className="card">
          <h3>Chain intact</h3>
          <div className="metric" style={{ color: chain?.intact ? "var(--ok)" : "var(--bad)" }}>
            {chain ? String(chain.intact) : "—"}
          </div>
        </div>
        <div className="card">
          <h3>SETHS enrolled</h3>
          <div className="metric">{seths?.enrolled ?? "—"}</div>
        </div>
        <div className="card">
          <h3>SETHS placed</h3>
          <div className="metric">{seths?.placed ?? "—"}</div>
        </div>
        <div className="card">
          <h3>TS projects</h3>
          <div className="metric">{ts?.projects ?? "—"}</div>
        </div>
        <div className="card">
          <h3>TS workers</h3>
          <div className="metric">{ts?.workers_absorbed ?? "—"}</div>
        </div>
        <div className="card">
          <h3>MADIBA cycles</h3>
          <div className="metric">{madiba?.cycles ?? "—"}</div>
        </div>
        <div className="card">
          <h3>MADIBA recycled</h3>
          <div className="metric">R{Number(madiba?.cumulative_recycled ?? 0).toLocaleString()}</div>
        </div>
      </div>

      <div className="panel">
        <h3>Quick links · Core surfaces</h3>
        <div className="row" style={{ flexWrap: "wrap", gap: 8 }}>
          <a className="btn" href="https://gods-platform-core.onrender.com/eif-ui" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            EIF Diamond
          </a>
          <a className="btn" href="https://gods-platform-core.onrender.com/gbs" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            GBS freeze
          </a>
          <a className="btn" href="https://gods-platform-core.onrender.com/Sentinel" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            Sentinel EVA
          </a>
          <a className="btn" href="https://gods-platform-core.onrender.com/divisions" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            Core /divisions
          </a>
          <button className="btn" onClick={load}>
            ↻ Refresh
          </button>
        </div>
        {gbs?.divisions && (
          <p style={{ fontSize: ".76rem", marginTop: 10 }}>
            Four-division GBS: {gbs.divisions.map((d: any) => d.division || d.name || d).join(" · ")}
          </p>
        )}
      </div>

      <div className="panel">
        <h3>Live posture</h3>
        <p style={{ fontSize: ".82rem" }}>Bias scan: {bias ? JSON.stringify(bias).slice(0, 160) : "—"}</p>
        <p style={{ fontSize: ".82rem" }}>Intelligence loop: {loop ? JSON.stringify(loop).slice(0, 160) : "—"}</p>
        <p style={{ fontSize: ".76rem", color: "var(--warn)" }}>
          Pre-registration forecast · honest empties valid · MADIBA ledger ≠ AUM · capital not_deployed
        </p>
      </div>

      <div className="panel">
        <h3>Recent audit</h3>
        <pre style={{ fontSize: ".7rem", maxHeight: 160, overflow: "auto" }}>
          {Array.isArray(audit) ? JSON.stringify(audit.slice(0, 8), null, 2) : "—"}
        </pre>
      </div>
    </>
  );
}
