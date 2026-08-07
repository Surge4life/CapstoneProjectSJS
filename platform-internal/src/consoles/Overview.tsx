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
  const [pipe, setPipe] = useState<any>(null);
  const [demo, setDemo] = useState<any>(null);
  const [gbs, setGbs] = useState<any>(null);
  const [eif, setEif] = useState<any>(null);
  const [log, setLog] = useState<string[]>(["Holdings overview · polling live Core"]);
  const [busy, setBusy] = useState(false);

  function push(line: string) {
    setLog((prev) => [`${new Date().toLocaleTimeString()}  ${line}`, ...prev].slice(0, 20));
  }

  async function load() {
    setBusy(true);
    try {
      const results = await Promise.allSettled([
        api.get("/admin/status"),
        api.get("/intelligence/loop-snapshot"),
        api.get("/audit/chain/verify"),
        api.get("/sovereignty/posture"),
        api.get("/bias/scan"),
        api.get("/audit/records"),
        api.get("/analytics/SETHS/kpis"),
        api.get("/ts/metrics"),
        api.get("/madiba/metrics"),
        api.get("/madiba/engage/pipeline"),
        api.get("/udoc/demo/ready"),
        api.get("/gis/gbs/architecture"),
        api.get("/eif/health"),
      ]);
      const val = (i: number) => (results[i].status === "fulfilled" ? (results[i] as any).value : null);
      setS(val(0));
      setLoop(val(1));
      setChain(val(2));
      setSov(val(3));
      setBias(val(4));
      setAudit(Array.isArray(val(5)) ? val(5) : val(5)?.records || []);
      setSeths(val(6));
      setTs(val(7));
      setMadiba(val(8));
      setPipe(val(9));
      setDemo(val(10));
      setGbs(val(11));
      setEif(val(12));
      push("refresh OK");
    } catch (e: any) {
      push(`ERROR ${e.message}`);
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    load();
    const t = setInterval(load, 12000);
    return () => clearInterval(t);
  }, []);

  const sovPct = sov ? `${(sov.sovereign_rate * 100).toFixed(0)}%` : "—";

  return (
    <>
      <div className="top">
        <h2>Holdings Overview</h2>
        <span className="badge">🔒 INTERNAL · LIVE</span>
      </div>

      <div className="guide">
        <h3>Holdings command path</h3>
        <div className="row" style={{ marginBottom: 0, flexWrap: "wrap" }}>
          <button className="btn" disabled={busy} onClick={load}>
            ↻ Refresh all
          </button>
          <a className="btn ghost" href="https://gods-platform-core.onrender.com/eif-ui" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            EIF Diamond
          </a>
          <a className="btn ghost" href="https://gods-platform-core.onrender.com/gbs" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            GBS freeze
          </a>
          <a className="btn ghost" href="https://gods-platform-core.onrender.com/Sentinel" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            Sentinel EVA
          </a>
          <a className="btn ghost" href="https://gods-platform-core.onrender.com/divisions" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            Core /divisions
          </a>
        </div>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Demo ready</h3>
          <div className="metric" style={{ color: demo?.ready ? "var(--ok)" : "var(--warn)" }}>
            {demo ? String(demo.ready) : "—"}
          </div>
        </div>
        <div className="card">
          <h3>Models</h3>
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
        <div className="card">
          <h3>Engagements</h3>
          <div className="metric">{pipe?.engagements ?? "—"}</div>
        </div>
        <div className="card">
          <h3>EIF</h3>
          <div className="metric">{eif?.status || eif?.ok || "—"}</div>
        </div>
      </div>

      <div className="panel">
        <h3>GBS four-division</h3>
        {gbs?.divisions ? (
          <div className="row">
            {gbs.divisions.map((d: any, i: number) => (
              <span key={i} className="tag">
                {d.division || d.name || JSON.stringify(d).slice(0, 40)}
              </span>
            ))}
          </div>
        ) : (
          <p style={{ fontSize: ".82rem" }}>—</p>
        )}
        <p style={{ fontSize: ".72rem", color: "var(--warn)", marginTop: 8 }}>
          Pre-registration forecast · honest empties valid · MADIBA ledger ≠ AUM · capital not_deployed
        </p>
      </div>

      <div className="panel">
        <h3>Live posture</h3>
        <div className="term">
          bias: {bias ? JSON.stringify(bias).slice(0, 200) : "—"}
          {"\n"}
          intelligence: {loop ? JSON.stringify(loop).slice(0, 200) : "—"}
          {"\n"}
          eif: {eif ? JSON.stringify(eif).slice(0, 160) : "—"}
        </div>
      </div>

      <div className="panel">
        <h3>Ops terminal</h3>
        <div className="term">{log.join("\n")}</div>
      </div>

      <div className="panel">
        <h3>Recent audit</h3>
        <div className="term">{Array.isArray(audit) && audit.length ? JSON.stringify(audit.slice(0, 8), null, 2).slice(0, 1200) : "—"}</div>
      </div>
    </>
  );
}
