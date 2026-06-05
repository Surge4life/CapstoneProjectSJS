import { useEffect, useState } from "react";
import { api, getBase, setBase, ping, getToken, setToken } from "./api";

const Emblem = () => (
  <svg className="em" viewBox="0 0 60 70" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M30 3 L55 12 V34 C55 50 44 62 30 67 C16 62 5 50 5 34 V12 Z" fill="#0C1A2E" stroke="#C9A84C" strokeWidth="2"/>
    <circle cx="30" cy="33" r="15" stroke="#C9A84C" strokeWidth="1.4" opacity=".6"/>
    <path d="M30 18 L33 30 L45 33 L33 36 L30 48 L27 36 L15 33 L27 30 Z" fill="#C9A84C"/>
    <circle cx="30" cy="33" r="4" fill="#0C1A2E" stroke="#E8C97A" strokeWidth="1.5"/>
  </svg>
);

type Tab = "dash" | "registry" | "decisions" | "audit" | "compliance";

export function App() {
  const [base, setBaseState] = useState(getBase());
  const [connected, setConnected] = useState<boolean | null>(null);
  const [authed, setAuthed] = useState(!!getToken());
  const [email, setEmail] = useState("admin@gods.local");
  const [pw, setPw] = useState("admin123");
  const [tab, setTab] = useState<Tab>("dash");
  const [me, setMe] = useState<any>(null);
  const [msg, setMsg] = useState(""); const [err, setErr] = useState("");

  const [models, setModels] = useState<any[]>([]);
  const [decisions, setDecisions] = useState<any[]>([]);
  const [audit, setAudit] = useState<any[]>([]);
  const [chain, setChain] = useState<any>(null);
  const [merkle, setMerkle] = useState<string>("");
  const [sov, setSov] = useState<any>(null);
  const [bias, setBias] = useState<any>(null);
  const [frameworks, setFrameworks] = useState<string[]>([]);
  const [sweep, setSweep] = useState<any>(null);

  // register form + decision scenario
  const [f, setF] = useState({ model_id: "", name: "", operator_id: "", risk_tier: "NOTABLE", use_case: "", jurisdiction: "ZA" });
  const [scenario, setScenario] = useState("healthy");
  const [verdict, setVerdict] = useState<any>(null);

  async function checkConn() { setConnected(await ping()); }
  useEffect(() => { checkConn(); }, []);
  function saveBase() { setBase(base); setBaseState(getBase()); checkConn(); }

  async function login() {
    setErr("");
    try { await api.login(email, pw); setAuthed(true); }
    catch (e: any) { setErr(e.message || "login failed"); }
  }

  async function refresh() {
    try {
      const [m, d, a, ch, mr, sv, bs, fw, sw, prof] = await Promise.all([
        api.get("/registry/models").catch(() => []),
        api.get("/decisions").catch(() => []),
        api.get("/audit/records").catch(() => []),
        api.get("/audit/chain/verify").catch(() => null),
        api.get("/audit/chain/merkle-root").catch(() => ({})),
        api.get("/sovereignty/posture").catch(() => null),
        api.get("/bias/scan").catch(() => null),
        api.get("/compliance/frameworks").catch(() => ({ frameworks: [] })),
        api.get("/compliance/sweep").catch(() => null),
        api.get("/access/profile").catch(() => null),
      ]);
      setModels(m); setDecisions(d); setAudit(a); setChain(ch);
      setMerkle((mr && mr.merkle_root) || ""); setSov(sv); setBias(bs);
      setFrameworks((fw && fw.frameworks) || []); setSweep(sw); setMe(prof);
    } catch (e: any) { setErr(e.message); }
  }
  useEffect(() => { if (authed) { refresh(); const t = setInterval(refresh, 8000); return () => clearInterval(t); } }, [authed]);

  async function registerModel() {
    setMsg(""); setErr("");
    try {
      const r = await api.post("/registry/models", f);
      setMsg(`Registered ${r.model_id} · ${r.status}`);
      setF({ model_id: "", name: "", operator_id: "", risk_tier: "NOTABLE", use_case: "", jurisdiction: "ZA" });
      refresh();
    } catch (e: any) { setErr(e.message); }
  }
  async function toggle(model_id: string, status: string) {
    const ns = status === "ACTIVE" ? "SUSPENDED" : "ACTIVE";
    try { await api.post(`/registry/models/${model_id}/status?new_status=${ns}`); setMsg(`${model_id} → ${ns}`); refresh(); }
    catch (e: any) { setErr(e.message); }
  }
  async function decide() {
    setErr(""); setVerdict(null);
    const b: any = { model_id: models[0]?.model_id || "model-001" };
    if (scenario === "biased") Object.assign(b, { risk_tier: "HIGH", priv_favorable: 620, unpriv_favorable: 300, ecs: 0.3 });
    if (scenario === "breach") Object.assign(b, { traceroute: 0.4, dnssec: 0.5 });
    try { setVerdict(await api.post("/decisions", b)); refresh(); }
    catch (e: any) { setVerdict({ error: e.message }); }
  }

  // ---------- gate screens ----------
  if (connected === false || connected === null) return (
    <div className="connect">
      <Emblem /><span className="gods">G.O.D.S · UDOC</span>
      <h1>Connect to UDOC</h1>
      <p>Point this client at your UDOC / platform-core deployment.</p>
      <input value={base} onChange={e => setBaseState(e.target.value)} placeholder="http://127.0.0.1:8077 or deployment URL" />
      <button className="btn" style={{ width: "100%" }} onClick={saveBase}>Connect</button>
      <div className={`status ${connected ? "ok" : "bad"}`}>{connected === null ? "checking…" : `✗ not reachable at ${getBase()}`}</div>
      <div className="foot">UDOC · Sovereign AI Governance — Client Control Plane</div>
      <div className="prereg">PRE-REGISTRATION FORECAST · G.O.D.S HOLDINGS (PTY) LTD (PROPOSED)</div>
    </div>
  );
  if (!authed) return (
    <div className="login">
      <Emblem /><span className="gods">G.O.D.S · UDOC</span>
      <h1>Sign in</h1>
      <div className="status ok">✓ connected to {getBase()}</div>
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="email" />
      <input type="password" value={pw} onChange={e => setPw(e.target.value)} placeholder="password" />
      <button className="btn" style={{ width: "100%" }} onClick={login}>Sign in</button>
      {err && <div className="err">{err}</div>}
      <div className="prereg">admin@gods.local / admin123 · staff roles use staff123</div>
    </div>
  );

  const sovPct = sov ? Math.round((sov.sovereign_rate ?? 1) * 100) : "—";
  const TABS: [Tab, string][] = [["dash", "Dashboard"], ["registry", "AI Registry"], ["decisions", "Decisions"], ["audit", "Audit Trail"], ["compliance", "Compliance"]];

  return (
    <div className="wrap">
      <div className="topbar">
        <div className="lg"><Emblem /><h2>UDOC Control<small>Sovereign AI Governance · Client Plane</small></h2></div>
        <span className="sp" />
        <span className="conn"><span className="dot live" />LIVE · {me?.role || "user"} · {getBase().replace(/^https?:\/\//, "")}</span>
        <span className="signout" onClick={() => { setToken(null); location.reload(); }}>sign out</span>
      </div>
      <div className="ribbon">PRE-REGISTRATION FORECAST · NO COMPANY / TRUST / TRADEMARK / DOMAIN YET REGISTERED · IP-PREPARATION WORK</div>
      <div className="tabs">{TABS.map(([k, t]) => <button key={k} className={tab === k ? "active" : ""} onClick={() => setTab(k)}>{t}</button>)}</div>

      <div className="main">
        {tab === "dash" && <>
          <div className="pg-h"><div><h2>Governance Dashboard</h2><p>Live posture across registered AI systems, governed decisions, sovereignty and the tamper-evident audit chain.</p></div></div>
          <div className="grid">
            <div className="card udoc"><h3>Systems Governed</h3><div className="metric">{models.length}</div></div>
            <div className="card udoc"><h3>Decisions</h3><div className="metric">{decisions.length}<small>EVA-governed</small></div></div>
            <div className="card udoc"><h3>Sovereignty</h3><div className="metric">{sovPct}%<small>ZA jurisdiction</small></div></div>
            <div className="card udoc"><h3>Bias Flags</h3><div className="metric">{bias?.fairness_flagged ?? "—"}<small>of {bias?.decisions_scanned ?? 0} scanned</small></div></div>
            <div className="card udoc"><h3>Audit Chain</h3><div className="metric" style={{ color: chain?.intact ? "var(--ok)" : "var(--bad)" }}>{chain ? (chain.intact ? "INTACT" : "BROKEN") : "—"}<small>{chain?.records ?? 0} records</small></div></div>
          </div>
          <div className="panel"><h3>Live Audit Stream <span className="tag PASS">● LIVE</span></h3>
            <div className="stream">{audit.length ? audit.slice(0, 14).map((r, i) =>
              <div className="ev" key={i}><span className="t">{String(r.created_at || "").slice(11, 19)}</span><span className="e">{r.event_type || r.event || "EVENT"}</span><span className="d">{typeof r.detail === "string" ? r.detail : JSON.stringify(r.detail || r.classification || "")}</span></div>
            ) : <p className="muted">No audit events yet — run a decision to populate the Merkle chain.</p>}</div>
          </div>
        </>}

        {tab === "registry" && <>
          <div className="pg-h"><div><h2>AI System Registry</h2><p>Every AI system must register before any consequential decision (Constitutional Pillar VIII). Kill-switch available per system.</p></div></div>
          <div className="panel"><h3>Register a system</h3>
            <div className="row">
              <input placeholder="model id" value={f.model_id} onChange={e => setF({ ...f, model_id: e.target.value })} />
              <input placeholder="name" value={f.name} onChange={e => setF({ ...f, name: e.target.value })} />
              <input placeholder="operator id" value={f.operator_id} onChange={e => setF({ ...f, operator_id: e.target.value })} />
              <select value={f.risk_tier} onChange={e => setF({ ...f, risk_tier: e.target.value })}>
                <option>MINIMAL</option><option>NOTABLE</option><option>HIGH</option><option>UNACCEPTABLE</option></select>
              <input placeholder="use case" value={f.use_case} onChange={e => setF({ ...f, use_case: e.target.value })} />
              <button className="btn" onClick={registerModel} disabled={!f.model_id || !f.name}>Register</button>
            </div>
          </div>
          <div className="panel"><h3>Registered systems — {models.length}</h3>
            <table><thead><tr><th>System ID</th><th>Name</th><th>Operator</th><th>Risk Tier</th><th>Status</th><th>Control</th></tr></thead>
              <tbody>{models.map(m => <tr key={m.model_id}>
                <td className="mono">{m.model_id}</td><td>{m.name}</td><td>{m.operator_id || "—"}</td><td><span className={`tag ${m.risk_tier}`}>{m.risk_tier}</span></td>
                <td><span className={`tag ${m.status}`}>{m.status}</span></td>
                <td><button className={`btn sm ${m.status === "ACTIVE" ? "danger" : ""}`} onClick={() => toggle(m.model_id, m.status)}>{m.status === "ACTIVE" ? "Suspend (kill-switch)" : "Resume"}</button></td>
              </tr>)}{!models.length && <tr><td colSpan={6} className="muted">No systems registered.</td></tr>}</tbody></table>
          </div>
        </>}

        {tab === "decisions" && <>
          <div className="pg-h"><div><h2>Governed Decisions</h2><p>The non-bypassable governance path: EVA 6-D scoring + sovereignty, sealed verdict, immutable audit.</p></div></div>
          <div className="panel"><h3>Run a governance decision</h3>
            <div className="row">
              <select value={scenario} onChange={e => setScenario(e.target.value)}>
                <option value="healthy">Healthy model</option><option value="biased">Biased + high-risk</option><option value="breach">Sovereignty breach</option></select>
              <button className="btn" onClick={decide}>Evaluate (model {models[0]?.model_id || "model-001"})</button>
            </div>
            {verdict && !verdict.error && <div className="verdict">
              Decision <span className={`tag ${verdict.decision}`}>{verdict.decision}</span> · SVS {verdict.svs} · risk {verdict.risk} · compliance {verdict.compliance}<br />
              sovereign {String(verdict.sovereign)} · latency {verdict.latency_ms}ms (budget {verdict.budget_ms}ms) · within budget {String(verdict.within_budget)}<br />
              sealed {String(verdict.seal || "").slice(0, 24)}…{verdict.block_reasons?.length ? <span style={{ color: "var(--bad)" }}><br />blocked: {verdict.block_reasons.join(" | ")}</span> : null}
            </div>}
            {verdict?.error && <div className="err">{verdict.error}</div>}
          </div>
          <div className="panel"><h3>Recent decisions — {decisions.length}</h3>
            <table><thead><tr><th>ID</th><th>Decision</th><th>SVS</th><th>Sovereign</th><th>Latency</th><th>Time</th></tr></thead>
              <tbody>{decisions.slice(0, 20).map(d => <tr key={d.id}>
                <td className="mono">{d.id}</td><td><span className={`tag ${d.decision}`}>{d.decision}</span></td><td>{d.svs}</td><td>{String(d.sovereign)}</td><td>{d.latency_ms}ms</td><td className="mono">{String(d.created_at || "").slice(11, 19)}</td>
              </tr>)}{!decisions.length && <tr><td colSpan={6} className="muted">No decisions yet.</td></tr>}</tbody></table>
          </div>
        </>}

        {tab === "audit" && <>
          <div className="pg-h"><div><h2>Audit Trail</h2><p>Tamper-evident, HMAC-chained, Merkle-linked. Every governed action is recorded and verifiable.</p></div></div>
          <div className="grid">
            <div className="card udoc"><h3>Records</h3><div className="metric">{chain?.records ?? audit.length}</div></div>
            <div className="card udoc"><h3>Chain Integrity</h3><div className="metric" style={{ color: chain?.intact ? "var(--ok)" : "var(--bad)" }}>{chain ? (chain.intact ? "INTACT" : "BROKEN") : "—"}</div></div>
            <div className="card udoc"><h3>Merkle Root</h3><div className="metric" style={{ fontSize: ".8rem", wordBreak: "break-all" }}>{merkle ? merkle.slice(0, 24) + "…" : "—"}</div></div>
          </div>
          <div className="panel"><h3>Audit records</h3>
            <div className="stream">{audit.length ? audit.map((r, i) =>
              <div className="ev" key={i}><span className="t">{String(r.created_at || "").slice(11, 19)}</span><span className="e">{r.event_type || r.event || "EVENT"}</span><span className="d">{typeof r.detail === "string" ? r.detail : JSON.stringify(r.detail || r.classification || "")}</span></div>
            ) : <p className="muted">No records yet.</p>}</div>
          </div>
        </>}

        {tab === "compliance" && <>
          <div className="pg-h"><div><h2>Compliance</h2><p>Regulatory frameworks tracked by UDOC; per-model compliance sweep.</p></div></div>
          <div className="panel"><h3>Frameworks</h3>
            <div className="row">{frameworks.map(fw => <span className="tag" key={fw} style={{ fontSize: ".7rem", padding: "5px 10px" }}>{fw}</span>)}{!frameworks.length && <span className="muted">—</span>}</div>
          </div>
          <div className="panel"><h3>Compliance sweep — {sweep?.checked ?? 0} checked</h3>
            <table><thead><tr><th>Model</th><th>Risk Tier</th><th>Status</th><th>Last Compliance</th><th>Compliant</th></tr></thead>
              <tbody>{(sweep?.results || []).map((r: any, i: number) => <tr key={i}>
                <td className="mono">{r.model_id}</td><td>{r.risk_tier}</td><td><span className={`tag ${r.status}`}>{r.status}</span></td><td>{r.last_compliance || "—"}</td>
                <td><span className={`tag ${r.compliant === false ? "FAIL" : r.compliant ? "PASS" : "REVIEW"}`}>{r.compliant === null || r.compliant === undefined ? "PENDING" : String(r.compliant)}</span></td>
              </tr>)}{!(sweep?.results || []).length && <tr><td colSpan={5} className="muted">No models to sweep.</td></tr>}</tbody></table>
          </div>
        </>}

        {msg && <div className="ok">{msg}</div>}{err && <div className="err">{err}</div>}
        <div className="foot center">UDOC SOVEREIGN GOVERNANCE · CLIENT CONTROL PLANE · © 2026 SASHIN J. SINGH · PRE-REGISTRATION</div>
      </div>
    </div>
  );
}
