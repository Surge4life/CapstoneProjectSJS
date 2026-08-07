import { useEffect, useState } from "react";
import { api } from "../api";

export function TSOps() {
  const [projects, setProjects] = useState<any[]>([]);
  const [spvs, setSpvs] = useState<any[]>([]);
  const [placed, setPlaced] = useState<any[]>([]);
  const [workers, setWorkers] = useState<any[]>([]);
  const [k, setK] = useState<any>(null);
  const [tm, setTm] = useState<any>(null);
  const [name, setName] = useState("Internal Demo SPV");
  const [equity, setEquity] = useState(0.3);
  const [sector, setSector] = useState("ENERGY");
  const [spvId, setSpvId] = useState("");
  const [learner, setLearner] = useState("");
  const [log, setLog] = useState<string[]>(["TS Industries ready · equity gate 0.20–0.60"]);
  const [busy, setBusy] = useState(false);

  function push(line: string) {
    setLog((prev) => [`${new Date().toLocaleTimeString()}  ${line}`, ...prev].slice(0, 24));
  }

  async function load() {
    try {
      const [subList, metrics, kpis, list, learners] = await Promise.all([
        api.get("/ts/submit/projects").catch(() => []),
        api.get("/ts/metrics").catch(() => null),
        api.get("/analytics/TS/kpis").catch(() => null),
        api.get("/ts/projects").catch(() => []),
        api.get("/seths/learners?status=PLACED&limit=40").catch(() => ({ learners: [] })),
      ]);
      setProjects(Array.isArray(subList) ? subList : subList?.projects || []);
      setTm(metrics);
      setK(kpis);
      setSpvs(Array.isArray(list) ? list : list?.projects || []);
      setPlaced(learners?.learners || (Array.isArray(learners) ? learners : []));
      if (spvId) {
        const w = await api.get(`/ts/projects/${encodeURIComponent(spvId)}/workers`).catch(() => []);
        setWorkers(Array.isArray(w) ? w : w?.workers || []);
      }
    } catch (e: any) {
      push(`ERROR ${e.message}`);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function deploy() {
    setBusy(true);
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
      push(`DEPLOY ${r.spv_id} equity=${equity} sector=${sector}`);
      await load();
    } catch (e: any) {
      push(`FAIL deploy ${e.message}`);
    } finally {
      setBusy(false);
    }
  }

  async function assign() {
    setBusy(true);
    try {
      if (!spvId || !learner) throw new Error("SPV id + PLACED learner required");
      const r = await api.post(`/ts/projects/${encodeURIComponent(spvId)}/assign-worker`, {
        learner_ref: learner,
        role: "technician",
        monthly_wage: 0,
      });
      push(`ASSIGN ${learner} → ${spvId} workers=${r.workers_deployed ?? r.workers ?? "?"}`);
      const w = await api.get(`/ts/projects/${encodeURIComponent(spvId)}/workers`).catch(() => []);
      setWorkers(Array.isArray(w) ? w : w?.workers || []);
      await load();
    } catch (e: any) {
      push(`FAIL assign ${e.message}`);
    } finally {
      setBusy(false);
    }
  }

  async function selectSpv(id: string) {
    setSpvId(id);
    const w = await api.get(`/ts/projects/${encodeURIComponent(id)}/workers`).catch(() => []);
    setWorkers(Array.isArray(w) ? w : w?.workers || []);
    push(`SELECT ${id}`);
  }

  const bySub = tm?.by_subsidiary || {};

  return (
    <>
      <div className="top">
        <h2>
          <span className="acc-ts">TS</span> Industries Operations
        </h2>
        <span className="badge">🔒 STAFF · LIVE</span>
      </div>

      <div className="guide">
        <h3>TS command path</h3>
        <div className="row" style={{ marginBottom: 0 }}>
          <button className="btn" disabled={busy} onClick={deploy}>
            Deploy SPV
          </button>
          <button className="btn" disabled={busy} onClick={assign}>
            Assign PLACED
          </button>
          <button className="btn ghost" disabled={busy} onClick={load}>
            ↻ Refresh
          </button>
        </div>
        <p style={{ fontSize: ".72rem", marginTop: 8 }}>
          Prerequisite: SETHS learners in <b>PLACED</b>. Equity gate enforced server-side.
        </p>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Projects</h3>
          <div className="metric">{tm?.projects ?? k?.projects ?? spvs.length}</div>
        </div>
        <div className="card">
          <h3>Workers</h3>
          <div className="metric">{tm?.workers_absorbed ?? k?.workers_absorbed ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Op. profit</h3>
          <div className="metric">R{Number(tm?.monthly_operating_profit ?? k?.total_profit ?? 0).toLocaleString()}</div>
        </div>
        <div className="card">
          <h3>PLACED pool</h3>
          <div className="metric">{placed.length}</div>
        </div>
        <div className="card">
          <h3>SPV rows</h3>
          <div className="metric">{spvs.length}</div>
        </div>
        <div className="card">
          <h3>Submissions</h3>
          <div className="metric">{projects.length}</div>
        </div>
      </div>

      {Object.keys(bySub).length > 0 && (
        <div className="panel">
          <h3>By subsidiary</h3>
          <div className="row">
            {Object.entries(bySub).map(([key, v]) => (
              <span key={key} className="tag">
                {key}: {String(v)}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="panel">
        <h3>Deploy SPV</h3>
        <div className="row">
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="SPV name" />
          <select value={sector} onChange={(e) => setSector(e.target.value)}>
            {["ENERGY", "WATER", "AGRI", "HOUSING", "DIGITAL"].map((s) => (
              <option key={s}>{s}</option>
            ))}
          </select>
          <input
            type="number"
            step="0.05"
            min={0.2}
            max={0.6}
            value={equity}
            onChange={(e) => setEquity(parseFloat(e.target.value || "0.3"))}
            style={{ width: 80 }}
          />
          <button className="btn" disabled={busy} onClick={deploy}>
            Deploy
          </button>
        </div>
      </div>

      <div className="panel">
        <h3>Assign workspace</h3>
        <div className="row">
          <input value={spvId} onChange={(e) => setSpvId(e.target.value)} placeholder="SPV-…" style={{ minWidth: 140 }} />
          <input value={learner} onChange={(e) => setLearner(e.target.value)} placeholder="SETHS-… PLACED" style={{ minWidth: 160 }} />
          <button className="btn" disabled={busy} onClick={assign}>
            Assign worker
          </button>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 12 }}>
          <div>
            <p style={{ fontSize: ".72rem", marginBottom: 6 }}>PLACED learners</p>
            <div style={{ maxHeight: 180, overflow: "auto" }}>
              {placed.length === 0 ? (
                <p style={{ fontSize: ".78rem" }}>None — run SETHS → PLACED first</p>
              ) : (
                <table>
                  <thead>
                    <tr>
                      <th>Ref</th>
                      <th>Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    {placed.map((l: any) => (
                      <tr key={l.ref} onClick={() => setLearner(l.ref)} style={{ cursor: "pointer", background: learner === l.ref ? "rgba(76,175,125,.12)" : undefined }}>
                        <td style={{ fontFamily: "ui-monospace,monospace" }}>{l.ref}</td>
                        <td>R{Number(l.monthly_value || 0).toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
          <div>
            <p style={{ fontSize: ".72rem", marginBottom: 6 }}>SPVs</p>
            <div style={{ maxHeight: 180, overflow: "auto" }}>
              {spvs.length === 0 ? (
                <p style={{ fontSize: ".78rem" }}>No SPVs — deploy above</p>
              ) : (
                <table>
                  <thead>
                    <tr>
                      <th>SPV</th>
                      <th>Workers</th>
                      <th>Eq</th>
                    </tr>
                  </thead>
                  <tbody>
                    {spvs.slice(0, 20).map((p: any) => (
                      <tr key={p.spv_id} onClick={() => selectSpv(p.spv_id)} style={{ cursor: "pointer", background: spvId === p.spv_id ? "rgba(76,175,125,.12)" : undefined }}>
                        <td style={{ fontFamily: "ui-monospace,monospace" }}>{p.spv_id}</td>
                        <td>{p.workers ?? p.workers_deployed ?? 0}</td>
                        <td>{p.equity_pct ?? p.equity ?? "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
        {workers.length > 0 && (
          <div style={{ marginTop: 12 }}>
            <p style={{ fontSize: ".72rem" }}>Workers on selected SPV</p>
            <div className="term">{JSON.stringify(workers.slice(0, 8), null, 2).slice(0, 600)}</div>
          </div>
        )}
      </div>

      <div className="panel">
        <h3>Ops terminal</h3>
        <div className="term">{log.join("\n")}</div>
      </div>

      <div className="panel">
        <h3>Partner submissions</h3>
        {projects.length === 0 ? (
          <p style={{ fontSize: ".82rem" }}>No submissions (honest empty OK)</p>
        ) : (
          <div className="term">{JSON.stringify(projects.slice(0, 5), null, 2).slice(0, 700)}</div>
        )}
      </div>
    </>
  );
}
