import { useEffect, useState } from "react";
import { api } from "../api";

type Scenario = "fair" | "biased" | "high" | "sov";

export function UDOCGov() {
  const [models, setModels] = useState<any[]>([]);
  const [cases, setCases] = useState<any[]>([]);
  const [chain, setChain] = useState<any>(null);
  const [sov, setSov] = useState<any>(null);
  const [demo, setDemo] = useState<any>(null);
  const [policy, setPolicy] = useState<any>(null);
  const [eif, setEif] = useState<any>(null);
  const [gbs, setGbs] = useState<any>(null);
  const [batch, setBatch] = useState<any>(null);
  const [result, setResult] = useState<any>(null);
  const [scenario, setScenario] = useState<Scenario>("fair");
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const [certId, setCertId] = useState("");

  async function load() {
    setErr("");
    try {
      const [mods, cs, ch, sv, dm, pol, eh, arch] = await Promise.all([
        api.get("/registry/models").catch(() => []),
        api.get("/oversight/cases").catch(() => []),
        api.get("/audit/chain/verify").catch(() => null),
        api.get("/sovereignty/posture").catch(() => null),
        api.get("/udoc/demo/ready").catch(() => null),
        api.get("/policy/active").catch(() => null),
        api.get("/eif/health").catch(() => null),
        api.get("/gis/gbs/architecture").catch(() => null),
      ]);
      setModels(Array.isArray(mods) ? mods : mods?.models || []);
      setCases(Array.isArray(cs) ? cs : cs?.cases || []);
      setChain(ch);
      setSov(sv);
      setDemo(dm);
      setPolicy(pol);
      setEif(eh);
      setGbs(arch);
    } catch (e: any) {
      setErr(e.message || String(e));
    }
  }

  useEffect(() => {
    load();
  }, []);

  function scenarioBody(s: Scenario) {
    const model_id = models.find((m) => m.status === "ACTIVE")?.model_id || models[0]?.model_id || "model-001";
    const b: any = { model_id };
    if (s === "fair") Object.assign(b, { risk_tier: "LOW" });
    if (s === "biased") Object.assign(b, { risk_tier: "HIGH", priv_favorable: 600, unpriv_favorable: 300, ecs: 0.3 });
    if (s === "high") Object.assign(b, { risk_tier: "HIGH" });
    if (s === "sov") Object.assign(b, { traceroute: 0.4, risk_tier: "MEDIUM" });
    return b;
  }

  async function decide() {
    setBusy(true);
    setErr("");
    setMsg("");
    try {
      const r = await api.post("/decisions", scenarioBody(scenario));
      setResult(r);
      setMsg(`Decision ${r.decision}`);
      await load();
    } catch (e: any) {
      setResult({ error: e.message });
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function runBatch() {
    setBusy(true);
    setErr("");
    setMsg("");
    try {
      const r = await api.post("/decisions/batch", {
        options: ["fair", "biased", "high", "sov"],
        model_id: models.find((m) => m.status === "ACTIVE")?.model_id || "model-001",
      });
      setBatch(r);
      setMsg("Batch EVA complete");
      await load();
    } catch (e: any) {
      setErr(e.message || String(e));
    } finally {
      setBusy(false);
    }
  }

  async function openCase() {
    setBusy(true);
    try {
      const mid = models[0]?.model_id || "model-001";
      await api.post("/oversight/cases", { model_id: mid, reason: "manual staff review" });
      setMsg("Oversight case opened");
      await load();
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function resolve(ref: string) {
    setBusy(true);
    try {
      await api.post(`/oversight/cases/${encodeURIComponent(ref)}/resolve?resolution=reviewed&override=false`);
      setMsg(`Resolved ${ref}`);
      await load();
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function verifyCert() {
    if (!certId.trim()) return;
    setBusy(true);
    setErr("");
    try {
      const r = await api.get(`/certificates/${encodeURIComponent(certId.trim())}`).catch(async () => {
        return api.post("/certificates/verify", { certificate_id: certId.trim() });
      });
      setMsg(`Cert: ${JSON.stringify(r).slice(0, 160)}`);
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  }

  const outcomes = batch?.outcomes || batch?.results || null;
  const gate = batch?.gate || null;
  const rulesCount = Array.isArray(policy?.rules) ? policy.rules.length : policy?.active_rules ?? "—";

  return (
    <>
      <div className="top">
        <h2>
          <span className="acc-udoc">UDOC</span> Governance
        </h2>
        <span className="badge">🔒 INTERNAL ONLY</span>
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
          <div className="metric">{models.length}</div>
        </div>
        <div className="card">
          <h3>Chain intact</h3>
          <div className="metric" style={{ color: chain?.intact ? "var(--ok)" : "var(--bad)" }}>
            {chain ? String(chain.intact) : "—"}
          </div>
        </div>
        <div className="card">
          <h3>Active policy rules</h3>
          <div className="metric">{rulesCount}</div>
        </div>
        <div className="card">
          <h3>Sovereignty</h3>
          <div className="metric">{sov ? `${(sov.sovereign_rate * 100).toFixed(0)}%` : "—"}</div>
        </div>
        <div className="card">
          <h3>EIF</h3>
          <div className="metric">{eif?.status || eif?.ok || "—"}</div>
        </div>
      </div>

      <div className="panel">
        <h3>EVA · scenario evaluate</h3>
        <p style={{ fontSize: ".76rem", marginBottom: 8 }}>
          Capstone gate: <b>fair ≠ BLOCK</b> · <b>biased = BLOCK</b>. Uses live Core <code>/decisions</code> and{" "}
          <code>/decisions/batch</code>.
        </p>
        <div className="row" style={{ flexWrap: "wrap", gap: 8 }}>
          {(["fair", "biased", "high", "sov"] as Scenario[]).map((s) => (
            <button
              key={s}
              className="btn"
              disabled={busy}
              onClick={() => setScenario(s)}
              style={{ opacity: scenario === s ? 1 : 0.75, borderColor: scenario === s ? "var(--udoc)" : undefined }}
            >
              {s}
            </button>
          ))}
          <button className="btn" disabled={busy} onClick={decide}>
            Evaluate {scenario}
          </button>
          <button className="btn" disabled={busy} onClick={runBatch}>
            Run Full EVA batch
          </button>
          <button className="btn" disabled={busy} onClick={load}>
            ↻ Refresh
          </button>
        </div>
        {result && !result.error && (
          <p style={{ fontSize: ".82rem", marginTop: 10 }}>
            Decision <span className={`tag ${result.decision}`}>{result.decision}</span>
            {result.svs != null && <> · SVS {result.svs}</>}
            {result.latency_ms != null && (
              <>
                {" "}
                · latency {result.latency_ms}ms (budget {result.budget_ms}ms)
              </>
            )}
            {result.seal && <> · sealed {String(result.seal).slice(0, 16)}…</>}
            {result.block_reasons?.length > 0 && (
              <span style={{ color: "var(--bad)" }}> · {result.block_reasons.length} block reasons</span>
            )}
          </p>
        )}
        {result?.error && <div className="err">{result.error}</div>}
        {outcomes && (
          <div style={{ marginTop: 12, fontSize: ".78rem" }}>
            <b>Batch outcomes</b>
            <pre style={{ whiteSpace: "pre-wrap", fontSize: ".72rem", maxHeight: 160, overflow: "auto" }}>
              {JSON.stringify(outcomes, null, 2).slice(0, 1200)}
            </pre>
            {gate && (
              <p>
                Gate: fair_neq_block={String(gate.fair_neq_block)} · biased_eq_block={String(gate.biased_eq_block)}
              </p>
            )}
          </div>
        )}
      </div>

      <div className="panel">
        <h3>Human oversight (Pillar VIII)</h3>
        <div className="row" style={{ marginBottom: 8 }}>
          <button className="btn sm" disabled={busy} onClick={openCase}>
            Open review case
          </button>
        </div>
        <table>
          <thead>
            <tr>
              <th>Ref</th>
              <th>Model</th>
              <th>Reason</th>
              <th>State</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {cases.map((c: any) => (
              <tr key={c.case_ref || c.ref}>
                <td>{c.case_ref || c.ref}</td>
                <td>{c.model_id}</td>
                <td>{c.reason}</td>
                <td>
                  <span className={`tag ${c.state}`}>{c.state}</span>
                </td>
                <td>
                  {c.state === "OPEN" && (
                    <button className="btn sm" disabled={busy} onClick={() => resolve(c.case_ref || c.ref)}>
                      Resolve
                    </button>
                  )}
                </td>
              </tr>
            ))}
            {!cases.length && (
              <tr>
                <td colSpan={5} style={{ color: "var(--rule)" }}>
                  No open cases
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="panel">
        <h3>Registered models</h3>
        <table>
          <thead>
            <tr>
              <th>Model</th>
              <th>Operator</th>
              <th>Risk</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {models.map((m) => (
              <tr key={m.model_id}>
                <td>{m.model_id}</td>
                <td>{m.operator_id || "—"}</td>
                <td>{m.risk_tier}</td>
                <td>
                  <span className={`tag ${m.status}`}>{m.status}</span>
                </td>
              </tr>
            ))}
            {!models.length && (
              <tr>
                <td colSpan={4} style={{ color: "var(--rule)" }}>
                  No models in registry
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="panel">
        <h3>Cert verify · GBS / EIF context</h3>
        <div className="row" style={{ gap: 8, flexWrap: "wrap" }}>
          <input value={certId} onChange={(e) => setCertId(e.target.value)} placeholder="certificate id" style={{ minWidth: 180 }} />
          <button className="btn" disabled={busy} onClick={verifyCert}>
            Verify cert
          </button>
          <a className="btn" href="https://gods-platform-core.onrender.com/Sentinel" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            Open Sentinel
          </a>
          <a className="btn" href="https://gods-platform-core.onrender.com/gbs" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            Open /gbs freeze
          </a>
          <a className="btn" href="https://gods-platform-core.onrender.com/eif-ui" target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
            Open EIF
          </a>
        </div>
        {gbs?.divisions && (
          <p style={{ fontSize: ".76rem", marginTop: 10 }}>
            GBS four-division: {gbs.divisions.map((d: any) => d.division).join(" · ")}
          </p>
        )}
      </div>

      {msg && <div className="ok">{msg}</div>}
      {err && <div className="err">{err}</div>}
    </>
  );
}
