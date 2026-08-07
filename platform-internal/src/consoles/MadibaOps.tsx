import { useEffect, useState } from "react";
import { api } from "../api";

export function MadibaOps() {
  const [pipe, setPipe] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [sa, setSa] = useState<any>(null);
  const [inflow, setInflow] = useState(100000);
  const [month, setMonth] = useState(8);
  const [investor, setInvestor] = useState("Capstone Demo LP");
  const [amount, setAmount] = useState(250000);
  const [active, setActive] = useState("");
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  async function load() {
    setErr("");
    try {
      const [p, m, series] = await Promise.all([
        api.get("/madiba/engage/pipeline").catch(() => null),
        api.get("/madiba/metrics").catch(() => null),
        api.get("/madiba/series-a-status").catch(() => null),
      ]);
      setPipe(p);
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

  async function createEngage() {
    setBusy(true);
    setMsg("");
    setErr("");
    try {
      const r = await api.post("/madiba/engage", {
        investor_name: investor,
        investor_type: "INSTITUTIONAL",
        instrument: "blended",
        indicated_amount: amount,
      });
      setActive(r.engagement_ref || "");
      setMsg(`Engagement ${r.engagement_ref} · ${r.stage}`);
      await load();
    } catch (e: any) {
      setErr(e.message || String(e));
    } finally {
      setBusy(false);
    }
  }

  async function advance() {
    const ref = active.trim();
    if (!ref) {
      setErr("Select or enter engagement ref");
      return;
    }
    setBusy(true);
    setMsg("");
    setErr("");
    try {
      const r = await api.post(`/madiba/engage/${encodeURIComponent(ref)}/advance`);
      setMsg(`${ref} → ${r.stage}`);
      await load();
    } catch (e: any) {
      setErr(e.message || String(e));
    } finally {
      setBusy(false);
    }
  }

  const list = pipe?.list || [];
  const by = pipe?.by_stage || {};
  const triggers = sa?.triggers || {};

  return (
    <>
      <div className="top">
        <h2>
          <span className="acc-madiba">MADIBA</span> Operations
        </h2>
        <span className="badge">🔒 STAFF</span>
      </div>

      <div className="panel" style={{ borderLeft: "3px solid var(--warn)" }}>
        <p style={{ fontSize: ".76rem", margin: 0, color: "var(--warn)" }}>
          Demo ledger only — not institutional AUM. Capital not_deployed. EIF Diamond nominations are audit-only on Capstone.
        </p>
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
          <h3>Committed</h3>
          <div className="metric">R{Number(pipe?.committed_total ?? 0).toLocaleString()}</div>
        </div>
        <div className="card">
          <h3>Series-A</h3>
          <div className="metric">{sa?.all_conditions_met ? "met" : "not met"}</div>
        </div>
        <div className="card">
          <h3>Indicated total</h3>
          <div className="metric">R{Number(pipe?.indicated_total ?? 0).toLocaleString()}</div>
        </div>
      </div>

      <div className="panel">
        <h3>Pipeline stages</h3>
        <div className="row" style={{ flexWrap: "wrap", gap: 8 }}>
          {["INTRODUCED", "DD", "TERM_SHEET", "COMMITTED", "FUNDED"].map((s) => (
            <span key={s} className="badge" style={{ fontSize: ".72rem" }}>
              {s}: {by[s] ?? 0}
            </span>
          ))}
        </div>
      </div>

      <div className="panel">
        <h3>New engagement</h3>
        <div className="row" style={{ flexWrap: "wrap", gap: 8 }}>
          <input value={investor} onChange={(e) => setInvestor(e.target.value)} placeholder="Investor name" style={{ minWidth: 160 }} />
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(parseFloat(e.target.value || "0"))}
            placeholder="Indicated amount"
            style={{ width: 140 }}
          />
          <button className="btn" disabled={busy} onClick={createEngage}>
            Create engagement
          </button>
        </div>
        <div className="row" style={{ marginTop: 10, gap: 8, flexWrap: "wrap" }}>
          <input value={active} onChange={(e) => setActive(e.target.value)} placeholder="ENG-…" style={{ minWidth: 160 }} />
          <button className="btn" disabled={busy} onClick={advance}>
            Advance stage
          </button>
          <button className="btn" disabled={busy} onClick={load}>
            ↻ Refresh
          </button>
          <a className="btn" href="https://gods-platform-core.onrender.com/eif-ui" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            Open EIF Diamond
          </a>
        </div>
      </div>

      <div className="panel">
        <h3>Engage pipeline</h3>
        {list.length === 0 ? (
          <p style={{ fontSize: ".82rem" }}>No engagements — create one above (honest empty OK).</p>
        ) : (
          <div style={{ maxHeight: 220, overflow: "auto" }}>
            {list.slice(0, 20).map((e: any) => (
              <div
                key={e.ref}
                onClick={() => setActive(e.ref)}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  gap: 8,
                  padding: "8px 6px",
                  borderBottom: "1px solid var(--rule)",
                  cursor: "pointer",
                  background: active === e.ref ? "rgba(245,165,36,.08)" : "transparent",
                }}
              >
                <span style={{ fontFamily: "ui-monospace,monospace", fontSize: ".75rem" }}>{e.ref}</span>
                <span style={{ fontSize: ".75rem" }}>
                  {e.investor} · {e.stage} · R{Number(e.amount || 0).toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="panel">
        <h3>Allocate (demo ledger)</h3>
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
        </div>
      </div>

      <div className="panel">
        <h3>Series-A triggers (honest)</h3>
        {Object.keys(triggers).length === 0 ? (
          <p style={{ fontSize: ".82rem" }}>—</p>
        ) : (
          Object.entries(triggers).map(([k, v]: any) => (
            <div key={k} style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", borderBottom: "1px solid var(--rule)", fontSize: ".78rem" }}>
              <span>{k}</span>
              <span>
                {v?.actual ?? "—"} / {v?.target ?? "—"} · {v?.met ? "met" : "not met"}
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
