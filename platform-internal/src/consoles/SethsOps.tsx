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
  const [records, setRecords] = useState<any[]>([]);
  const [active, setActive] = useState("");
  const [count, setCount] = useState(3);
  const [filter, setFilter] = useState("");
  const [log, setLog] = useState<string[]>(["SETHS ops ready · live Core APIs"]);
  const [busy, setBusy] = useState(false);

  function push(line: string) {
    setLog((prev) => [`${new Date().toLocaleTimeString()}  ${line}`, ...prev].slice(0, 24));
  }

  async function load(statusFilter?: string) {
    try {
      const [kpis, metrics, roster, rec] = await Promise.all([
        api.get("/analytics/SETHS/kpis").catch(() => null),
        api.get("/seths/metrics").catch(() => null),
        api.get("/seths/learners?limit=40" + (statusFilter ? `&status=${statusFilter}` : "")).catch(() => ({ learners: [] })),
        api.get("/analytics/SETHS/records").catch(() => []),
      ]);
      setM(kpis);
      setSm(metrics);
      setLearners(roster?.learners || []);
      setRecords(Array.isArray(rec) ? rec : rec?.records || []);
    } catch (e: any) {
      push(`ERROR ${e.message}`);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function run(label: string, fn: () => Promise<void>) {
    setBusy(true);
    try {
      await fn();
      push(label);
      await load(filter || undefined);
    } catch (e: any) {
      push(`FAIL ${e.message}`);
    } finally {
      setBusy(false);
    }
  }

  async function enrol(n = count) {
    await run(`ENROL cohort ×${n}`, async () => {
      const r = await api.post("/seths/enrol", {
        count: Math.max(1, Math.min(n, 20)),
        qualification: "Digital Operations & AI Literacy",
        nqf_level: 5,
      });
      if (r?.refs?.[0]) setActive(r.refs[0]);
      push(`refs ${JSON.stringify(r?.refs || r).slice(0, 120)}`);
    });
  }

  async function advance(toPlaced = false) {
    const ref = active.trim();
    if (!ref) throw new Error("Select a learner ref first");
    await run(`ADVANCE ${ref}${toPlaced ? " → PLACED" : ""}`, async () => {
      let last = await api.post(`/seths/${encodeURIComponent(ref)}/advance`, {});
      if (toPlaced && last?.status !== "PLACED") {
        last = await api.post(`/seths/${encodeURIComponent(ref)}/advance`, {});
      }
      push(`${ref} status=${last?.status}`);
    });
  }

  const enrolled = m?.enrolled ?? sm?.total ?? "—";
  const placed = m?.placed ?? sm?.placed ?? "—";
  const completed = sm?.completed ?? "—";
  const rate =
    m?.placement_rate != null
      ? `${(m.placement_rate * 100).toFixed(0)}%`
      : sm?.placement_rate != null
        ? `${(sm.placement_rate * 100).toFixed(0)}%`
        : "—";
  const output = m?.monthly_output ?? sm?.monthly_economic_output ?? 0;
  const byStatus = learners.reduce((a: any, l) => {
    a[l.status] = (a[l.status] || 0) + 1;
    return a;
  }, {} as Record<string, number>);

  return (
    <>
      <div className="top">
        <h2>
          <span className="acc-seths">SETHS</span> Operations
        </h2>
        <span className="badge">🔒 STAFF · LIVE</span>
      </div>

      <div className="guide">
        <h3>SETHS command path</h3>
        <div className="row" style={{ marginBottom: 0 }}>
          <button className="btn" disabled={busy} onClick={() => enrol(3)}>
            Demo: Enrol ×3
          </button>
          <button className="btn" disabled={busy} onClick={() => advance(false)}>
            Advance selected
          </button>
          <button className="btn" disabled={busy} onClick={() => advance(true)}>
            Force → PLACED
          </button>
          <button className="btn ghost" disabled={busy} onClick={() => load(filter || undefined)}>
            ↻ Refresh
          </button>
        </div>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Enrolled</h3>
          <div className="metric">{enrolled}</div>
        </div>
        <div className="card">
          <h3>Completed</h3>
          <div className="metric">{completed}</div>
        </div>
        <div className="card">
          <h3>Placed</h3>
          <div className="metric">{placed}</div>
        </div>
        <div className="card">
          <h3>Placement rate</h3>
          <div className="metric">{rate}</div>
        </div>
        <div className="card">
          <h3>Monthly output</h3>
          <div className="metric">R{Number(output).toLocaleString()}</div>
        </div>
        <div className="card">
          <h3>Roster rows</h3>
          <div className="metric">{learners.length}</div>
        </div>
      </div>

      <div className="panel">
        <h3>Status distribution (loaded roster)</h3>
        <div className="row">
          {["ENROLLED", "COMPLETED", "PLACED"].map((s) => (
            <span key={s} className={`tag ${s}`}>
              {s}: {byStatus[s] || 0}
            </span>
          ))}
        </div>
      </div>

      <div className="panel">
        <h3>Cohort controls</h3>
        <p style={{ fontSize: ".76rem", marginBottom: 10 }}>
          Flow <b>ENROLLED → COMPLETED → PLACED</b>. Placements feed TS assign-worker.
        </p>
        <div className="row">
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
          <button className="btn" disabled={busy} onClick={() => enrol(count)}>
            Enrol cohort
          </button>
          <input
            value={active}
            onChange={(e) => setActive(e.target.value)}
            placeholder="Active SETHS-…"
            style={{ minWidth: 180 }}
          />
        </div>
      </div>

      <div className="panel">
        <h3>Learner roster</h3>
        <div className="row">
          {["", "ENROLLED", "COMPLETED", "PLACED"].map((f) => (
            <button
              key={f || "all"}
              className="btn sm"
              disabled={busy}
              onClick={() => {
                setFilter(f);
                load(f || undefined);
              }}
            >
              {f || "All"}
            </button>
          ))}
        </div>
        {learners.length === 0 ? (
          <p style={{ fontSize: ".82rem" }}>No learners in filter — enrol to seed roster.</p>
        ) : (
          <div style={{ maxHeight: 300, overflow: "auto" }}>
            <table>
              <thead>
                <tr>
                  <th>Ref</th>
                  <th>Status</th>
                  <th>Stream</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                {learners.map((l) => (
                  <tr
                    key={l.ref}
                    onClick={() => setActive(l.ref)}
                    style={{ cursor: "pointer", background: active === l.ref ? "rgba(63,167,214,.1)" : undefined }}
                  >
                    <td style={{ fontFamily: "ui-monospace,monospace", color: "var(--seths)" }}>{l.ref}</td>
                    <td>
                      <span className={`tag ${l.status}`}>{l.status}</span>
                    </td>
                    <td>{l.stream || l.qualification || "—"}</td>
                    <td>R{Number(l.monthly_value || 0).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="panel">
        <h3>Ops terminal</h3>
        <div className="term">{log.join("\n")}</div>
      </div>

      <div className="panel">
        <h3>Analytics records</h3>
        <div className="term">
          {records.length
            ? JSON.stringify(records.slice(0, 6), null, 2).slice(0, 900)
            : "No analytics records yet"}
        </div>
      </div>
    </>
  );
}
