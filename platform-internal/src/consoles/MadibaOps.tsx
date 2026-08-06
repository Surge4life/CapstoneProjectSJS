import { useEffect, useState } from "react";
import { api } from "../api";

export function MadibaOps() {
  const [pipe, setPipe] = useState<any>(null);
  const [k, setK] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [sa, setSa] = useState<any>(null);
  const [inflow, setInflow] = useState(100000);
  const [month, setMonth] = useState(8);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  async function load() {
    setErr("");
    try {
      const [p, ak, m, series] = await Promise.all([
        api.get("/madiba/engage/pipeline").catch(() => null),
        api.get("/analytics/MADIBA/kpis").catch(() => null),
        api.get("/madiba/metrics").catch(() => null),
        api.get("/madiba/series-a-status").catch(() => null),
      ]);
      setPipe(p);
      setK(ak);
      setMetrics(m);
      setSa(series);
    } catch (e: any) {
      setErr(e.message || String(e));
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function allocate() {
    setBusy(true);
    setMsg("");
    setErr("");
    try {
      const r = await api.post("/madiba/allocate", { month, total_inflow: inflow });
      setMsg(`Recycled to SETHS: R${Number(r.recycled_to_seths || 0).toLocaleString()}`);
      await load();
    } catch (e: any) {
      setErr(e.message || String(e));
    } finally {
      setBusy(false);
    }
  }

  const list = pipe?.list || pipe?.engagements_list || [];

  return (
    <>
      <div className="top">
        <h2>
          <span className="acc-madiba">MADIBA</span> Operations
        </h2>
        <span className="badge">🔒 STAFF</span>
      </div>
      <div className="grid">
        <div className="card">
          <h3>Cycles</h3>
          <div className="metric">{metrics?.cycles ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Recycled → SETHS</h3>
          <div className="metric">R{Number(metrics?.cumulative_recycled ?? 0).toLocaleString()}</div>
        </div>
        <div className="card">
          <h3>Engagements</h3>
          <div className="metric">{pipe?.engagements ?? list.length ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Series-A</h3>
          <div className="metric">{sa?.all_conditions_met ? "met" : "not met"}</div>
        </div>
      </div>
      <div className="panel">
        <h3>Allocate (demo ledger)</h3>
        <p style={{ fontSize: ".76rem", marginBottom: 8, color: "var(--warn)" }}>
          Demo ledger only — not institutional AUM. Capital not_deployed on free tier.
        </p>
        <div className="row" style={{ gap: 8, flexWrap: "wrap" }}>
          <label style={{ fontSize: ".72rem" }}>
            Month{" "}
            <input type="number" value={month} onChange={(e) => setMonth(parseInt(e.target.value || "1", 10))} style={{ width: 64 }} />
          </label>
          <label style={{ fontSize: ".72rem" }}>
            Inflow R{" "}
            <input type="number" value={inflow} onChange={(e) => setInflow(parseFloat(e.target.value || "0"))} style={{ width: 120 }} />
          </label>
          <button className="btn" disabled={busy} onClick={allocate}>
            Allocate
          </button>
          <button className="btn" disabled={busy} onClick={load}>
            ↻ Refresh
          </button>
        </div>
      </div>
      <div className="panel">
        <h3>Engage pipeline</h3>
        {list.length === 0 ? (
          <p style={{ fontSize: ".82rem" }}>No open engagements (honest empty OK).</p>
        ) : (
          list.slice(0, 10).map((e: any) => (
            <div key={e.ref} style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", borderBottom: "1px solid var(--rule)" }}>
              <span style={{ fontFamily: "ui-monospace,monospace", fontSize: ".75rem" }}>{e.ref}</span>
              <span style={{ fontSize: ".75rem" }}>
                {e.investor || e.investor_name} · {e.stage}
              </span>
            </div>
          ))
        )}
      </div>
      {msg && <div className="ok">{msg}</div>}
      {err && <div className="err">{err}</div>}
    </>
  );
}
