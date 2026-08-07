import { useEffect, useState } from "react";
import { api } from "../api";

const STAGES = ["INTRODUCED", "DD", "TERM_SHEET", "COMMITTED", "FUNDED"];

export function MadibaOps() {
  const [pipe, setPipe] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [sa, setSa] = useState<any>(null);
  const [records, setRecords] = useState<any[]>([]);
  const [inflow, setInflow] = useState(100000);
  const [month, setMonth] = useState(8);
  const [investor, setInvestor] = useState("Capstone Demo LP");
  const [amount, setAmount] = useState(250000);
  const [active, setActive] = useState("");
  const [log, setLog] = useState<string[]>(["MADIBA ready · demo ledger ≠ AUM · capital not_deployed"]);
  const [busy, setBusy] = useState(false);

  function push(line: string) {
    setLog((prev) => [`${new Date().toLocaleTimeString()}  ${line}`, ...prev].slice(0, 24));
  }

  async function load() {
    try {
      const [p, m, series, rec] = await Promise.all([
        api.get("/madiba/engage/pipeline").catch(() => null),
        api.get("/madiba/metrics").catch(() => null),
        api.get("/madiba/series-a-status").catch(() => null),
        api.get("/analytics/MADIBA/records").catch(() => []),
      ]);
      setPipe(p);
      setMetrics(m);
      setSa(series);
      setRecords(Array.isArray(rec) ? rec : rec?.records || []);
    } catch (e: any) {
      push(`ERROR ${e.message}`);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function createEngage() {
    setBusy(true);
    try {
      const r = await api.post("/madiba/engage", {
        investor_name: investor,
        investor_type: "INSTITUTIONAL",
        instrument: "blended",
        indicated_amount: amount,
      });
      setActive(r.engagement_ref || "");
      push(`ENGAGE ${r.engagement_ref} stage=${r.stage} amount=${amount}`);
      await load();
    } catch (e: any) {
      push(`FAIL engage ${e.message}`);
    } finally {
      setBusy(false);
    }
  }

  async function advance() {
    const ref = active.trim();
    if (!ref) {
      push("FAIL select engagement ref");
      return;
    }
    setBusy(true);
    try {
      const r = await api.post(`/madiba/engage/${encodeURIComponent(ref)}/advance`);
      push(`ADVANCE ${ref} → ${r.stage}`);
      await load();
    } catch (e: any) {
      push(`FAIL advance ${e.message}`);
    } finally {
      setBusy(false);
    }
  }

  async function allocate() {
    setBusy(true);
    try {
      const r = await api.post("/madiba/allocate", { month, total_inflow: inflow });
      push(`ALLOCATE month=${month} inflow=${inflow} recycled=${r.recycled_to_seths ?? "?"}`);
      await load();
    } catch (e: any) {
      push(`FAIL allocate ${e.message}`);
    } finally {
      setBusy(false);
    }
  }

  const list = pipe?.list || [];
  const by = pipe?.by_stage || {};
  const triggers = sa?.triggers || {};
  const series = metrics?.series || [];

  return (
    <>
      <div className="top">
        <h2>
          <span className="acc-madiba">MADIBA</span> Operations
        </h2>
        <span className="badge">🔒 STAFF · LIVE</span>
      </div>

      <div className="banner warn">
        Demo ledger only — not institutional AUM. Capital not_deployed. EIF Diamond = audit nomination only on Capstone free tier.
        {metrics?.honesty ? ` · ${metrics.honesty}` : ""}
        {metrics?.note ? ` · ${metrics.note}` : ""}
      </div>

      <div className="guide">
        <h3>MADIBA command path</h3>
        <div className="row" style={{ marginBottom: 0 }}>
          <button className="btn" disabled={busy} onClick={createEngage}>
            Create engagement
          </button>
          <button className="btn" disabled={busy} onClick={advance}>
            Advance stage
          </button>
          <button className="btn" disabled={busy} onClick={allocate}>
            Allocate recycle
          </button>
          <a className="btn ghost" href="https://gods-platform-core.onrender.com/eif-ui" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            EIF Diamond
          </a>
          <button className="btn ghost" disabled={busy} onClick={load}>
            ↻ Refresh
          </button>
        </div>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Cycles</h3>
          <div className="metric">{metrics?.cycles ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Total inflow</h3>
          <div className="metric">R{Number(metrics?.total_inflow ?? 0).toLocaleString()}</div>
        </div>
        <div className="card">
          <h3>Recycled → SETHS</h3>
          <div className="metric">R{Number(metrics?.cumulative_recycled ?? 0).toLocaleString()}</div>
        </div>
        <div className="card">
          <h3>Recycle ratio</h3>
          <div className="metric">{metrics?.recycle_ratio != null ? `${(metrics.recycle_ratio * 100).toFixed(0)}%` : "—"}</div>
        </div>
        <div className="card">
          <h3>Engagements</h3>
          <div className="metric">{pipe?.engagements ?? list.length}</div>
        </div>
        <div className="card">
          <h3>Committed</h3>
          <div className="metric">R{Number(pipe?.committed_total ?? 0).toLocaleString()}</div>
        </div>
        <div className="card">
          <h3>Indicated</h3>
          <div className="metric">R{Number(pipe?.indicated_total ?? 0).toLocaleString()}</div>
        </div>
        <div className="card">
          <h3>Series-A</h3>
          <div className="metric">{sa?.all_conditions_met ? "met" : "not met"}</div>
        </div>
      </div>

      <div className="panel">
        <h3>Pipeline stages</h3>
        <div className="row">
          {STAGES.map((s) => (
            <span key={s} className={`tag ${s}`}>
              {s}: {by[s] ?? 0}
            </span>
          ))}
        </div>
      </div>

      <div className="panel">
        <h3>New engagement</h3>
        <div className="row">
          <input value={investor} onChange={(e) => setInvestor(e.target.value)} placeholder="Investor" style={{ minWidth: 160 }} />
          <input type="number" value={amount} onChange={(e) => setAmount(parseFloat(e.target.value || "0"))} style={{ width: 140 }} />
          <button className="btn" disabled={busy} onClick={createEngage}>
            Create
          </button>
          <input value={active} onChange={(e) => setActive(e.target.value)} placeholder="ENG-…" style={{ minWidth: 140 }} />
          <button className="btn" disabled={busy} onClick={advance}>
            Advance
          </button>
        </div>
      </div>

      <div className="panel">
        <h3>Engage pipeline</h3>
        {list.length === 0 ? (
          <p style={{ fontSize: ".82rem" }}>No engagements — create above</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Ref</th>
                <th>Investor</th>
                <th>Stage</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {list.slice(0, 25).map((e: any) => (
                <tr key={e.ref} onClick={() => setActive(e.ref)} style={{ cursor: "pointer", background: active === e.ref ? "rgba(155,109,214,.12)" : undefined }}>
                  <td style={{ fontFamily: "ui-monospace,monospace" }}>{e.ref}</td>
                  <td>{e.investor}</td>
                  <td>
                    <span className={`tag ${e.stage}`}>{e.stage}</span>
                  </td>
                  <td>R{Number(e.amount || 0).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="panel">
        <h3>Allocate (demo ledger)</h3>
        <div className="row">
          <label style={{ fontSize: ".72rem" }}>
            Month <input type="number" value={month} onChange={(e) => setMonth(parseInt(e.target.value || "1", 10))} style={{ width: 64 }} />
          </label>
          <label style={{ fontSize: ".72rem" }}>
            Inflow R <input type="number" value={inflow} onChange={(e) => setInflow(parseFloat(e.target.value || "0"))} style={{ width: 120 }} />
          </label>
          <button className="btn" disabled={busy} onClick={allocate}>
            Allocate
          </button>
        </div>
        {series.length > 0 && (
          <div className="term" style={{ marginTop: 10 }}>
            {JSON.stringify(series.slice(-6), null, 2).slice(0, 700)}
          </div>
        )}
      </div>

      <div className="panel">
        <h3>Series-A triggers (honest)</h3>
        <table>
          <thead>
            <tr>
              <th>Trigger</th>
              <th>Actual</th>
              <th>Target</th>
              <th>Met</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(triggers).map(([key, v]: any) => (
              <tr key={key}>
                <td>{key}</td>
                <td>{v?.actual ?? "—"}</td>
                <td>{v?.target ?? "—"}</td>
                <td>
                  <span className={`tag ${v?.met ? "ACTIVE" : "OPEN"}`}>{v?.met ? "met" : "not met"}</span>
                </td>
              </tr>
            ))}
            {!Object.keys(triggers).length && (
              <tr>
                <td colSpan={4}>—</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="panel">
        <h3>Ops terminal</h3>
        <div className="term">{log.join("\n")}</div>
      </div>

      <div className="panel">
        <h3>Analytics records</h3>
        <div className="term">{records.length ? JSON.stringify(records.slice(0, 5), null, 2).slice(0, 800) : "—"}</div>
      </div>
    </>
  );
}
