import { useEffect, useState } from "react";
import { api } from "../api";

export function TSOps() {
  const [projects, setProjects] = useState<any[]>([]);
  const [spvs, setSpvs] = useState<any[]>([]);
  const [k, setK] = useState<any>(null);
  const [tm, setTm] = useState<any>(null);
  const [name, setName] = useState("Internal Demo SPV");
  const [equity, setEquity] = useState(0.3);
  const [spvId, setSpvId] = useState("");
  const [learner, setLearner] = useState("");
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  async function load() {
    setErr("");
    try {
      const [subs, metrics, kpis, list] = await Promise.all([
        api.get("/ts/submit/projects").catch(() => []),
        api.get("/ts/metrics").catch(() => null),
        api.get("/analytics/TS/kpis").catch(() => null),
        api.get("/ts/projects").catch(() => []),
      ]);
      setProjects(Array.isArray(subs) ? subs : subs?.projects || []);
      setTm(metrics);
      setK(kpis);
      setSpvs(Array.isArray(list) ? list : list?.projects || []);
    } catch (e: any) {
      setErr(e.message || String(e));
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function deploy() {
    setBusy(true);
    setMsg("");
    setErr("");
    try {
      if (!(equity >= 0.2 && equity <= 0.6)) throw new Error("Equity must be 0.20–0.60");
      const r = await api.post("/ts/projects", {
        name,
        sector: "ENERGY",
        subsidiary: "ENERGY",
        equity_pct: equity,
        workers_deployed: 0,
        monthly_revenue: 0,
        operating_margin: 0.3,
      });
      setSpvId(r.spv_id || "");
      setMsg(`Deployed ${r.spv_id}`);
      await load();
    } catch (e: any) {
      setErr(e.message || String(e));
    } finally {
      setBusy(false);
    }
  }

  async function assign() {
    setBusy(true);
    setMsg("");
    setErr("");
    try {
      if (!spvId || !learner) throw new Error("SPV id + PLACED learner ref required");
      const r = await api.post(`/ts/projects/${encodeURIComponent(spvId)}/assign-worker`, {
        learner_ref: learner,
        role: "technician",
        monthly_wage: 0,
      });
      setMsg(`Workers on SPV: ${r.workers_deployed ?? "?"}`);
      await load();
    } catch (e: any) {
      setErr(e.message || String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <div className="top">
        <h2>
          <span className="acc-ts">TS</span> Industries Operations
        </h2>
        <span className="badge">🔒 STAFF</span>
      </div>
      <div className="grid">
        <div className="card">
          <h3>Projects</h3>
          <div className="metric">{tm?.projects ?? k?.projects ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Workers</h3>
          <div className="metric">{tm?.workers_absorbed ?? k?.workers_absorbed ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Op. Profit</h3>
          <div className="metric">R{Number(tm?.monthly_operating_profit ?? k?.total_profit ?? 0).toLocaleString()}</div>
        </div>
        <div className="card">
          <h3>Submissions</h3>
          <div className="metric">{projects.length}</div>
        </div>
      </div>
      <div className="panel">
        <h3>Deploy SPV</h3>
        <p style={{ fontSize: ".76rem", marginBottom: 8 }}>Equity gate 0.20–0.60. Only PLACED SETHS learners are assignable.</p>
        <div className="row" style={{ flexWrap: "wrap", gap: 8 }}>
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="SPV name" />
          <input
            type="number"
            step="0.05"
            value={equity}
            onChange={(e) => setEquity(parseFloat(e.target.value || "0.3"))}
            style={{ width: 80 }}
          />
          <button className="btn" disabled={busy} onClick={deploy}>
            Deploy
          </button>
          <button className="btn" disabled={busy} onClick={load}>
            ↻ Refresh
          </button>
        </div>
      </div>
      <div className="panel">
        <h3>Assign PLACED learner</h3>
        <div className="row" style={{ flexWrap: "wrap", gap: 8 }}>
          <input value={spvId} onChange={(e) => setSpvId(e.target.value)} placeholder="SPV-…" />
          <input value={learner} onChange={(e) => setLearner(e.target.value)} placeholder="SETHS-… (PLACED)" />
          <button className="btn" disabled={busy} onClick={assign}>
            Assign worker
          </button>
        </div>
        {spvs.length > 0 && (
          <div style={{ marginTop: 10, maxHeight: 180, overflow: "auto" }}>
            {spvs.slice(0, 12).map((p: any) => (
              <div
                key={p.spv_id}
                onClick={() => setSpvId(p.spv_id)}
                style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", cursor: "pointer", borderBottom: "1px solid var(--rule)" }}
              >
                <span style={{ fontFamily: "ui-monospace,monospace", fontSize: ".75rem" }}>{p.spv_id}</span>
                <span style={{ fontSize: ".75rem" }}>
                  {p.name} · w:{p.workers ?? 0}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
      {msg && <div className="ok">{msg}</div>}
      {err && <div className="err">{err}</div>}
    </>
  );
}
