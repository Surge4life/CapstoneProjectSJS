import { useEffect, useState } from "react";
import { api } from "../api";

type Learner = {
  ref: string;
  status: string;
  qualification?: string;
  nqf_level?: number;
  monthly_value?: number;
  cohort?: string;
  stream?: string;
};

export function SethsOps() {
  const [m, setM] = useState<any>(null);
  const [sm, setSm] = useState<any>(null);
  const [learners, setLearners] = useState<Learner[]>([]);
  const [active, setActive] = useState("");
  const [count, setCount] = useState(1);
  const [filter, setFilter] = useState("");
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  async function load(statusFilter?: string) {
    setErr("");
    try {
      const [kpis, metrics, roster] = await Promise.all([
        api.get("/analytics/SETHS/kpis").catch(() => null),
        api.get("/seths/metrics").catch(() => null),
        api.get("/seths/learners?limit=30" + (statusFilter ? `&status=${statusFilter}` : "")).catch(() => ({ learners: [] })),
      ]);
      setM(kpis);
      setSm(metrics);
      setLearners(roster?.learners || []);
    } catch (e: any) {
      setErr(e.message || String(e));
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function run(label: string, fn: () => Promise<void>) {
    setBusy(true);
    setMsg("");
    setErr("");
    try {
      await fn();
      setMsg(label);
      await load(filter || undefined);
    } catch (e: any) {
      setErr(e.message || String(e));
    } finally {
      setBusy(false);
    }
  }

  async function enrol() {
    await run(`Enrolled cohort of ${count}`, async () => {
      const r = await api.post("/seths/enrol", {
        count: Math.max(1, Math.min(count, 20)),
        qualification: "Digital Operations & AI Literacy",
        nqf_level: 5,
      });
      if (r?.refs?.[0]) setActive(r.refs[0]);
    });
  }

  async function advance(toPlaced = false) {
    const ref = active.trim();
    if (!ref) throw new Error("Select a learner ref first");
    await run(`Advanced ${ref}`, async () => {
      let last = await api.post(`/seths/${encodeURIComponent(ref)}/advance`, {});
      if (toPlaced && last?.status !== "PLACED") {
        last = await api.post(`/seths/${encodeURIComponent(ref)}/advance`, {});
      }
      setMsg(`${ref} → ${last?.status || "?"}`);
    });
  }

  const enrolled = m?.enrolled ?? sm?.total ?? "—";
  const placed = m?.placed ?? sm?.placed ?? "—";
  const rate =
    m?.placement_rate != null
      ? `${(m.placement_rate * 100).toFixed(0)}%`
      : sm?.placement_rate != null
        ? `${(sm.placement_rate * 100).toFixed(0)}%`
        : "—";
  const output = m?.monthly_output ?? sm?.monthly_economic_output ?? 0;

  return (
    <>
      <div className="top">
        <h2>
          <span className="acc-seths">SETHS</span> Operations
        </h2>
        <span className="badge">🔒 STAFF</span>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Enrolled</h3>
          <div className="metric">{enrolled}</div>
        </div>
        <div className="card">
          <h3>Placed</h3>
          <div className="metric">{placed}</div>
        </div>
        <div className="card">
          <h3>Placement Rate</h3>
          <div className="metric">{rate}</div>
        </div>
        <div className="card">
          <h3>Monthly Output</h3>
          <div className="metric">R{Number(output).toLocaleString()}</div>
        </div>
      </div>

      <div className="panel">
        <h3>Cohort Management</h3>
        <p style={{ fontSize: ".76rem", color: "var(--text)", marginBottom: 10 }}>
          Learner flow: <b>ENROLLED → COMPLETED → PLACED</b>. Placements feed TS worker assignment.
        </p>
        <div className="row" style={{ flexWrap: "wrap", gap: 8, alignItems: "center" }}>
          <label style={{ fontSize: ".72rem" }}>
            Count{" "}
            <input
              type="number"
              min={1}
              max={20}
              value={count}
              onChange={(e) => setCount(parseInt(e.target.value || "1", 10))}
              style={{ width: 64, marginLeft: 6 }}
            />
          </label>
          <button className="btn" disabled={busy} onClick={enrol}>
            Enrol cohort
          </button>
          <button className="btn" disabled={busy} onClick={() => advance(false)} style={{ opacity: 0.9 }}>
            Advance selected
          </button>
          <button className="btn" disabled={busy} onClick={() => advance(true)}>
            → PLACED
          </button>
          <button className="btn" disabled={busy} onClick={() => load(filter || undefined)} style={{ opacity: 0.85 }}>
            ↻ Refresh
          </button>
        </div>
        <div className="row" style={{ marginTop: 10, gap: 8, alignItems: "center" }}>
          <label style={{ fontSize: ".72rem", flex: 1 }}>
            Active ref
            <input
              value={active}
              onChange={(e) => setActive(e.target.value)}
              placeholder="SETHS-…"
              style={{ width: "100%", marginTop: 4 }}
            />
          </label>
        </div>
      </div>

      <div className="panel">
        <h3>Learner roster</h3>
        <div className="row" style={{ gap: 8, marginBottom: 10 }}>
          <button className="btn" disabled={busy} onClick={() => { setFilter(""); load(); }}>
            All
          </button>
          <button className="btn" disabled={busy} onClick={() => { setFilter("PLACED"); load("PLACED"); }}>
            PLACED
          </button>
          <button className="btn" disabled={busy} onClick={() => { setFilter("COMPLETED"); load("COMPLETED"); }}>
            COMPLETED
          </button>
          <button className="btn" disabled={busy} onClick={() => { setFilter("ENROLLED"); load("ENROLLED"); }}>
            ENROLLED
          </button>
        </div>
        {learners.length === 0 ? (
          <p style={{ fontSize: ".82rem", color: "var(--text)" }}>
            No learners in this filter — enrol a cohort to seed the roster.
          </p>
        ) : (
          <div style={{ maxHeight: 280, overflow: "auto" }}>
            {learners.map((l) => (
              <div
                key={l.ref}
                onClick={() => setActive(l.ref)}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  gap: 8,
                  padding: "8px 10px",
                  borderBottom: "1px solid var(--rule)",
                  cursor: "pointer",
                  background: active === l.ref ? "rgba(0,194,212,.08)" : "transparent",
                }}
              >
                <span style={{ fontFamily: "ui-monospace,monospace", fontSize: ".78rem", color: "var(--seths, #00C2D4)" }}>
                  {l.ref}
                </span>
                <span style={{ fontSize: ".76rem" }}>
                  {l.status}
                  {l.monthly_value ? ` · R${Number(l.monthly_value).toLocaleString()}` : ""}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="panel">
        <h3>Programme Note</h3>
        <p style={{ fontSize: ".82rem" }}>
          Software Developer (SAQA 118707, NQF 5). Student applications and document verification are handled in the
          external SETHS app; staff approve placements via the Employer flow. This Internal console operates the live
          Core APIs on Neon (enrol / advance / roster) for Capstone staff demos.
        </p>
      </div>

      {msg && <div className="ok">{msg}</div>}
      {err && <div className="err">{err}</div>}
    </>
  );
}
