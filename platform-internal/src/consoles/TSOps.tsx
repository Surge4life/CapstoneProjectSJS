import { useEffect, useState } from "react";
import { api } from "../api";

export function TSOps() {
  const [projects, setProjects] = useState<any[]>([]);
  const [spvs, setSpvs] = useState<any[]>([]);
  const [placed, setPlaced] = useState<any[]>([]);
  const [k, setK] = useState<any>(null);
  const [tm, setTm] = useState<any>(null);
  const [name, setName] = useState("Internal Demo SPV");
  const [equity, setEquity] = useState(0.3);
  const [sector, setSector] = useState("ENERGY");
  const [spvId, setSpvId] = useState("");
  const [learner, setLearner] = useState("");
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  async function load() {
    setErr("");
    try {
      const [subs, metrics, kpis, list, learners] = await Promise.all([
        api.get("/ts/submit/projects").catch(() => []),
        api.get("/ts/metrics").catch(() => null),
        api.get("/analytics/TS/kpis").catch(() => null),
        api.get("/ts/projects").catch(() => []),
        api.get("/seths/learners?status=PLACED&limit=30").catch(() => ({ learners: [] })),
      ]);
      setProjects(Array.isArray(subs) ? subs : subs?.projects || []);
      setTm(metrics);
      setK(kpis);
      setSpvs(Array.isArray(list) ? list : list?.projects || []);
      setPlaced(learners?.learners || (Array.isArray(learners) ? learners : []));
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
        sector,
        subsidiary: sector,
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
      setMsg(`Workers on SPV: ${r.workers_deployed ?? r.workers ?? "?"}`);
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

      <div className="panel" style={{ borderLeft: "3px solid var(--ts, #3dd68c)" }}>
        <p style={{ fontSize: ".76rem", margin: 0 }}>
          Trusted Systems absorb <b>PLACED</b> SETHS learners into SPVs. Equity gate 0.20–0.60. Honest zeros OK when no
          live projects.
        </p>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Projects</h3>
          <div className="metric">{tm?.projects ?? k?.projects ?? spvs.length ?? "—"}</div>
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
          <h3>PLACED pool</h3>
          <div className="metric">{placed.length}</div>
        </div>
      </div>

      <div className="panel">
        <h3>Deploy SPV</h3>
        <div className="row" style={{ flexWrap: "wrap", gap: 8 }}>
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="SPV name" />
          <select value={sector} onChange={(e) => setSector(e.target.value)}>
            {["ENERGY", "WATER", "AGRI", "HOUSING", "DIGITAL"].map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
          <input
            type="number"
            step="0.05"
            value={equity}
            onChange={(e) => setEquity(parseFloat(e.target.value || "0.3"))}
            style={{ width: 80 }}
            title="Equity 0.20–0.60"
          />
          <button className="btn" disabled={busy} onClick={deploy}>
            Deploy SPV
          </button>
          <button className="btn" disabled={busy} onClick={load}>
            ↻ Refresh
          </button>
        </div>
      </div>

      <div className="panel">
        <h3>Assign PLACED learner</h3>
        <div className="row" style={{ flexWrap: "wrap", gap: 8 }}>
          <input value={spvId} onChange={(e) => setSpvId(e.target.value)} placeholder="SPV-…" style={{ minWidth: 140 }} />
          <input value={learner} onChange={(e) => setLearner(e.target.value)} placeholder="SETHS-… (PLACED)" style={{ minWidth: 160 }} />
          <button className="btn" disabled={busy} onClick={assign}>
            Assign worker
          </button>
        </div>
        {placed.length > 0 && (
          <div style={{ marginTop: 10 }}>
            <p style={{ fontSize: ".72rem", color: "var(--text)" }}>PLACED learners — click to fill assign field:</p>
            <div style={{ maxHeight: 140, overflow: "auto" }}>
              {placed.map((l: any) => (
                <div
                  key={l.ref}
                  onClick={() => setLearner(l.ref)}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    padding: "6px 4px",
                    cursor: "pointer",
                    borderBottom: "1px solid var(--rule)",
                    background: learner === l.ref ? "rgba(61,214,140,.08)" : "transparent",
                    fontSize: ".75rem",
                  }}
                >
                  <span style={{ fontFamily: "ui-monospace,monospace" }}>{l.ref}</span>
                  <span>
                    {l.stream || l.qualification || ""} · R{Number(l.monthly_value || 0).toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
        {spvs.length > 0 && (
          <div style={{ marginTop: 12, maxHeight: 180, overflow: "auto" }}>
            <p style={{ fontSize: ".72rem" }}>SPVs — click to select:</p>
            {spvs.slice(0, 15).map((p: any) => (
              <div
                key={p.spv_id}
                onClick={() => setSpvId(p.spv_id)}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  padding: "6px 0",
                  cursor: "pointer",
                  borderBottom: "1px solid var(--rule)",
                  background: spvId === p.spv_id ? "rgba(61,214,140,.08)" : "transparent",
                }}
              >
                <span style={{ fontFamily: "ui-monospace,monospace", fontSize: ".75rem" }}>{p.spv_id}</span>
                <span style={{ fontSize: ".75rem" }}>
                  {p.name} · w:{p.workers ?? p.workers_deployed ?? 0} · eq:{(p.equity_pct ?? p.equity) ?? "—"}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="panel">
        <h3>Partner submissions</h3>
        {projects.length === 0 ? (
          <p style={{ fontSize: ".82rem" }}>No open submissions (honest empty OK).</p>
        ) : (
          projects.slice(0, 8).map((p: any, i: number) => (
            <div key={p.ref || i} style={{ fontSize: ".76rem", padding: "4px 0", borderBottom: "1px solid var(--rule)" }}>
              {p.ref || p.name || JSON.stringify(p).slice(0, 80)}
            </div>
          ))
        )}
      </div>

      {msg && <div className="ok">{msg}</div>}
      {err && <div className="err">{err}</div>}
    </>
  );
}
