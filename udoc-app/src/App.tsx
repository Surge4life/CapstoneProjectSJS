import { useEffect, useState } from "react";
import { api, getBase, setBase, ping, getToken, setToken } from "./api";
declare const __BUILD_ID__: string;

const Emblem = () => (
  <svg className="em" viewBox="0 0 60 70" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M30 3 L55 12 V34 C55 50 44 62 30 67 C16 62 5 50 5 34 V12 Z" fill="#0C1A2E" stroke="#C9A84C" strokeWidth="2"/>
    <circle cx="30" cy="33" r="15" stroke="#C9A84C" strokeWidth="1.4" opacity=".6"/>
    <path d="M30 18 L33 30 L45 33 L33 36 L30 48 L27 36 L15 33 L27 30 Z" fill="#C9A84C"/>
    <circle cx="30" cy="33" r="4" fill="#0C1A2E" stroke="#E8C97A" strokeWidth="1.5"/>
  </svg>
);
const UpdateBanner = ({ on }: { on: boolean }) => on ? (
  <div className="update-banner" onClick={() => location.reload()}>↻ New version deployed to the eco-system — tap to update</div>
) : null;
const clamp = (v: number) => Math.max(0, Math.min(1, Number(v) || 0));
function Meter({ label, value, raw, invert }: { label: string; value: number; raw?: any; invert?: boolean }) {
  const pct = clamp(value) * 100;
  const good = invert ? pct < 50 : pct >= 60;
  return (<div className="meter"><h4>{label}</h4><div className="mv">{raw !== undefined ? raw : value.toFixed(2)}</div>
    <div className={`bar ${good ? "ok" : "bad"}`}><i style={{ width: pct + "%" }} /></div></div>);
}

type Plane = "select" | "software" | "hardware";
type SwTab = "dash" | "registry" | "eva" | "policy" | "intel" | "tenancy" | "audit" | "compliance";
type HwTab = "hqos" | "edge" | "sovereignty" | "killswitch";

export function App() {
  const [base, setBaseState] = useState(getBase());
  const [connected, setConnected] = useState<boolean | null>(null);
  const [authed, setAuthed] = useState(!!getToken());
  const [email, setEmail] = useState("admin@gods.local");
  const [pw, setPw] = useState("admin123");
  const [plane, setPlane] = useState<Plane>("select");
  const [swTab, setSwTab] = useState<SwTab>("dash");
  const [hwTab, setHwTab] = useState<HwTab>("hqos");
  const [me, setMe] = useState<any>(null);
  const [msg, setMsg] = useState(""); const [err, setErr] = useState("");

  const [models, setModels] = useState<any[]>([]);
  const [decisions, setDecisions] = useState<any[]>([]);
  const [audit, setAudit] = useState<any[]>([]);
  const [chain, setChain] = useState<any>(null);
  const [merkle, setMerkle] = useState(""); const [sov, setSov] = useState<any>(null);
  const [bias, setBias] = useState<any>(null);
  const [frameworks, setFrameworks] = useState<string[]>([]); const [sweep, setSweep] = useState<any>(null);

  const [f, setF] = useState({ model_id: "", name: "", operator_id: "", risk_tier: "NOTABLE", use_case: "", jurisdiction: "ZA" });
  const [scenario, setScenario] = useState("healthy");
  const [verdict, setVerdict] = useState<any>(null);
  const [certs, setCerts] = useState<any[]>([]);
  const [packs, setPacks] = useState<any[]>([]);
  const [activePol, setActivePol] = useState<any>(null);
  const [packDetail, setPackDetail] = useState<any>(null);
  const [pform, setPform] = useState({ name: "", jurisdiction: "ZA", sector: localStorage.getItem("udoc_sector") || "PUBLIC" });
  const [pfile, setPfile] = useState<File | null>(null);
  const [updateReady, setUpdateReady] = useState(false);
  const [sector, setSectorState] = useState<string>(localStorage.getItem("udoc_sector") || "PUBLIC");
  function setSector(x: string) { localStorage.setItem("udoc_sector", x); setSectorState(x); }

  const [intelSt, setIntelSt] = useState<any>(null);
  const [intelDocs, setIntelDocs] = useState<any[]>([]);
  const [askQ, setAskQ] = useState(""); const [askA, setAskA] = useState<any>(null);
  const [iText, setIText] = useState({ title: "", text: "", category: "GENERAL" });
  const [iFile, setIFile] = useState<File | null>(null);
  const [plan, setPlan] = useState<any>(null); const [myKeys, setMyKeys] = useState<any[]>([]);
  const [versions, setVersions] = useState<any[]>([]); const [hot, setHot] = useState<any>(null);

  async function doAsk() { setErr(""); setAskA(null); try { setAskA(await api.intelAsk(askQ)); } catch (e: any) { setErr(e.message); } }
  async function doIntelText() { setErr(""); try { await api.intelText(iText.title, iText.text, iText.category); setMsg("Added to corpus."); setIText({ title: "", text: "", category: "GENERAL" }); api.intelState().then(setIntelSt).catch(()=>{}); api.intelDocs().then(setIntelDocs).catch(()=>{}); } catch (e: any) { setErr(e.message); } }
  async function doIntelFile() { if (!iFile) return; setErr(""); try { await api.intelIngest(iFile, iFile.name, "GENERAL"); setMsg("Document ingested into the corpus."); setIFile(null); api.intelState().then(setIntelSt).catch(()=>{}); api.intelDocs().then(setIntelDocs).catch(()=>{}); } catch (e: any) { setErr(e.message); } }
  async function doIssueKey() { setErr(""); try { const r = await api.issueMyKey("mobile"); setMsg("API key (copy now — shown once): " + r.api_key); api.myKeys().then(setMyKeys).catch(()=>{}); } catch (e: any) { setErr(e.message); } }
  async function doSubmitPack(id: number) { setErr(""); try { const r = await api.submitPack(id); setMsg(`Submitted v${r.version.version} for COB review.`); api.packVersions(id).then(setVersions).catch(()=>{}); refresh(); } catch (e: any) { setErr(e.message); } }
  async function doApproveVer(vid: number, pid: number) { setErr(""); try { await api.approveVersion(vid); setMsg("COB approved · hot-reloaded into the live path."); api.packVersions(pid).then(setVersions).catch(()=>{}); api.hotreload().then(setHot).catch(()=>{}); refresh(); } catch (e: any) { setErr(e.message); } }

  async function checkConn() { setConnected(await ping()); }
  useEffect(() => { checkConn(); }, []);
  function saveBase() { setBase(base); setBaseState(getBase()); checkConn(); }
  async function login() { setErr(""); try { await api.login(email, pw); setAuthed(true); } catch (e: any) { setErr(e.message || "login failed"); } }

  async function refresh() {
    try {
      const [m, d, a, ch, mr, sv, bs, fw, sw, prof] = await Promise.all([
        api.get("/registry/models").catch(() => []), api.get("/decisions").catch(() => []),
        api.get("/audit/records").catch(() => []), api.get("/audit/chain/verify").catch(() => null),
        api.get("/audit/chain/merkle-root").catch(() => ({})), api.get("/sovereignty/posture").catch(() => null),
        api.get("/bias/scan").catch(() => null), api.get("/compliance/frameworks").catch(() => ({ frameworks: [] })),
        api.get("/compliance/sweep").catch(() => null), api.get("/access/profile").catch(() => null),
      ]);
      setModels(m); setDecisions(d); setAudit(a); setChain(ch); setMerkle((mr && mr.merkle_root) || "");
      setSov(sv); setBias(bs); setFrameworks((fw && fw.frameworks) || []); setSweep(sw); setMe(prof);
      api.get("/policy/packs").then(setPacks).catch(() => {});
      api.get("/policy/active").then(setActivePol).catch(() => {});
      api.get("/decisions/certificates").then(setCerts).catch(() => {});
      api.intelState().then(setIntelSt).catch(() => {}); api.intelDocs().then(setIntelDocs).catch(() => {});
      api.myTenant().then(setPlan).catch(() => {}); api.myKeys().then(setMyKeys).catch(() => {});
      api.hotreload().then(setHot).catch(() => {});
    } catch (e: any) { setErr(e.message); }
  }
  useEffect(() => { if (authed) { refresh(); const t = setInterval(refresh, 8000); return () => clearInterval(t); } }, [authed]);
  useEffect(() => {
    if (connected !== true) return;
    let first: string | null = null;
    const check = async () => {
      try { const v = await (await fetch(`${getBase()}/version`)).json();
        const c = `${v.commit}:${v.deployed_at}`;
        if (first === null) first = c; else if (c !== first) setUpdateReady(true);
      } catch { /* offline */ }
    };
    check(); const t = setInterval(check, 60000); return () => clearInterval(t);
  }, [connected]);

  async function registerModel() {
    setMsg(""); setErr("");
    try { const r = await api.post("/registry/models", f); setMsg(`Registered ${r.model_id} · ${r.status}`);
      setF({ model_id: "", name: "", operator_id: "", risk_tier: "NOTABLE", use_case: "", jurisdiction: "ZA" }); refresh();
    } catch (e: any) { setErr(e.message); }
  }
  async function toggle(model_id: string, status: string) {
    const ns = status === "ACTIVE" ? "SUSPENDED" : "ACTIVE";
    try { await api.post(`/registry/models/${model_id}/status?new_status=${ns}`); setMsg(`${model_id} → ${ns}`); refresh(); } catch (e: any) { setErr(e.message); }
  }
  async function decide() {
    setErr(""); setVerdict(null);
    const b: any = { model_id: models[0]?.model_id || "model-001" };
    if (scenario === "biased") Object.assign(b, { risk_tier: "HIGH", priv_favorable: 620, unpriv_favorable: 300, ecs: 0.3 });
    if (scenario === "breach") Object.assign(b, { traceroute: 0.4, dnssec: 0.5 });
    try { setVerdict(await api.post("/decisions", b)); refresh(); } catch (e: any) { setVerdict({ error: e.message }); }
  }

  async function doUploadPolicy() {
    if (!pfile || !pform.name) { setErr("choose a file and name"); return; }
    setMsg(""); setErr("");
    try {
      const r = await api.uploadPolicy(pform.name, pform.jurisdiction, pform.sector, pfile);
      setMsg(`Compiled ${r.pack.rule_count} rules from ${r.pack.source_filename} — review & activate.`);
      setPackDetail(r); setPform({ name: "", jurisdiction: "ZA", sector: "PUBLIC" }); setPfile(null); refresh();
    } catch (e: any) { setErr(e.message); }
  }
  async function loadPack(id: number) { try { setPackDetail(await api.get(`/policy/packs/${id}`)); api.packVersions(id).then(setVersions).catch(() => {}); } catch (e: any) { setErr(e.message); } }
  async function activatePack(id: number) { try { const r = await api.post(`/policy/packs/${id}/activate`); setMsg(`Pack ${id} ACTIVE — ${r.active_rules} rules enforced.`); refresh(); loadPack(id); } catch (e: any) { setErr(e.message); } }
  async function toggleRule(rid: number, enabled: boolean) { try { await api.patch(`/policy/rules/${rid}`, { enabled }); if (packDetail) loadPack(packDetail.pack.id); } catch (e: any) { setErr(e.message); } }

  // ---------- gates ----------
  if (connected === false || connected === null) return (
    <div className="connect"><Emblem /><span className="gods">G.O.D.S · UDOC</span><h1>Connect to UDOC</h1>
      <p>Point this client at your UDOC / platform-core deployment.</p>
      <input value={base} onChange={e => setBaseState(e.target.value)} placeholder="http://127.0.0.1:8077 or deployment URL" />
      <button className="btn" style={{ width: "100%" }} onClick={saveBase}>Connect</button>
      <div className={`status ${connected ? "ok" : "bad"}`}>{connected === null ? "checking…" : `✗ not reachable at ${getBase()}`}</div>
      <div className="foot">UDOC · Sovereign AI Governance — Software + Hardware Control Plane</div>
      <div className="prereg">PRE-REGISTRATION FORECAST · G.O.D.S HOLDINGS (PTY) LTD (PROPOSED)</div></div>
  );
  if (!authed) return (
    <div className="login"><Emblem /><span className="gods">G.O.D.S · UDOC</span><h1>Sign in</h1>
      <div className="status ok">✓ connected to {getBase()}</div>
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="email" />
      <input type="password" value={pw} onChange={e => setPw(e.target.value)} placeholder="password" />
      <button className="btn" style={{ width: "100%" }} onClick={login}>Sign in</button>
      {err && <div className="err">{err}</div>}
      <div className="prereg">admin@gods.local / admin123 · staff roles use staff123</div></div>
  );

  // ---------- split selection ----------
  if (plane === "select") return (
    <div className="wrap">
      <UpdateBanner on={updateReady} />
      <div className="ribbon">PRE-REGISTRATION FORECAST · NO COMPANY / TRUST / TRADEMARK / DOMAIN YET REGISTERED · IP-PREPARATION WORK</div>
      <div className="select-h"><Emblem /><h1>UDOC Control</h1><p>Sovereign AI Governance. Choose the plane you want to operate.</p>
        <p style={{ fontSize: ".7rem", marginTop: 6 }} className="conn"><span className="dot live" />LIVE · {me?.role || "user"} · {getBase().replace(/^https?:\/\//, "")} · <span className="signout" onClick={() => { setToken(null); location.reload(); }}>sign out</span></p></div>
      <div className="sector-pick"><span>Operating sector</span>
        <button className={sector === "PUBLIC" ? "on" : ""} onClick={() => setSector("PUBLIC")}>Public Sector</button>
        <button className={sector === "PRIVATE" ? "on" : ""} onClick={() => setSector("PRIVATE")}>Private Sector</button></div>
      <div className="planes">
        <div className="plane sw" onClick={() => { setPlane("software"); setSwTab("dash"); }}>
          <div className="pi">🛡</div><h3>UDOC Software</h3>
          <p>AI System Registry · EVA decision engine · tamper-evident audit · compliance &amp; bias governance.</p>
          <div className="go">ENTER GOVERNANCE →</div></div>
        <div className="plane hw" onClick={() => { setPlane("hardware"); setHwTab("hqos"); }}>
          <div className="pi">🔌</div><h3>UDOC Hardware</h3>
          <p>HQ-OS hybrid classical+quantum · sovereign edge nodes · sovereignty posture · hardware kill-switch.</p>
          <div className="go">ENTER HARDWARE →</div></div>
      </div>
      <div className="foot center">EVA ENGINE · 6-D GOVERNANCE · © 2026 SASHIN J. SINGH · PRE-REGISTRATION</div>
    </div>
  );

  const sovPct = sov ? Math.round((sov.sovereign_rate ?? 1) * 100) : "—";
  const isSw = plane === "software";
  const SW_ALL: [SwTab, string][] = [["dash", "Dashboard"], ["registry", "AI Registry"], ["eva", "EVA Engine"], ["policy", "Policy-to-Code"], ["intel", "Intelligence"], ["tenancy", "Tenancy"], ["audit", "Audit Trail"], ["compliance", "Compliance"]];
  const HW_ALL: [HwTab, string][] = [["hqos", "HQ-OS"], ["edge", "Sovereign Edge"], ["sovereignty", "Sovereignty"], ["killswitch", "Kill-Switch"]];
  // Role-scoped capabilities — the UI shows only what the role may operate; the backend enforces it independently.
  const role: string = me?.role || "viewer";
  const isAdmin: boolean = !!me?.is_admin;
  const CAPS: Record<string, { sw: string[]; hw: string[]; reg: boolean; kill: boolean; appr: boolean; ro: boolean }> = {
    admin:    { sw: ["dash", "registry", "eva", "policy", "intel", "tenancy", "audit", "compliance"], hw: ["hqos", "edge", "sovereignty", "killswitch"], reg: true,  kill: true,  appr: true,  ro: false },
    operator: { sw: ["dash", "registry", "eva", "audit", "compliance"],                               hw: ["hqos", "edge", "sovereignty"],               reg: true,  kill: false, appr: false, ro: false },
    gov:      { sw: ["dash", "eva", "policy", "intel", "audit", "compliance"],                         hw: ["hqos", "edge", "sovereignty"],               reg: false, kill: false, appr: true,  ro: false },
    auditor:  { sw: ["dash", "eva", "audit", "compliance"],                                            hw: ["hqos", "edge", "sovereignty"],               reg: false, kill: false, appr: false, ro: true  },
    viewer:   { sw: ["dash", "eva", "audit", "compliance"],                                            hw: ["hqos", "edge", "sovereignty"],               reg: false, kill: false, appr: false, ro: true  },
    client:   { sw: ["dash", "registry", "eva", "policy", "intel", "tenancy"],                         hw: [],                                            reg: true,  kill: false, appr: false, ro: false },
  };
  const cap = isAdmin ? CAPS.admin : (CAPS[role] || CAPS.viewer);
  const SW = SW_ALL.filter(([k]) => cap.sw.includes(k));
  const HW = HW_ALL.filter(([k]) => cap.hw.includes(k));

  return (
    <div className="wrap">
      <UpdateBanner on={updateReady} />
      <div className="topbar">
        <div className="lg"><Emblem /><h2>UDOC {isSw ? "Software" : "Hardware"}<small>{isSw ? "Sovereign AI Governance" : "HQ-OS · Sovereign Edge"}</small></h2></div>
        <span className="sp" />
        <span className="switch" onClick={() => setPlane("select")}>⇄ Switch plane</span>
        <span className="sector-chip">{sector === "PUBLIC" ? "Public Sector" : "Private Sector"}</span><span className="conn"><span className="dot live" />LIVE · {me?.role || "user"}</span>
        <span className="signout" onClick={() => { setToken(null); location.reload(); }} style={{ marginLeft: 10 }}>sign out</span>
      </div>
      <div className="ribbon">PRE-REGISTRATION FORECAST · NO COMPANY / TRUST / TRADEMARK / DOMAIN YET REGISTERED · IP-PREPARATION WORK</div>
      <div style={{ fontSize: ".72rem", color: "#9fb3d6", padding: "2px 0 6px" }}>Role <b style={{ color: "#C9A84C" }}>{role}{me?.division && me.division !== "GODS" ? " · " + me.division : ""}</b> — scoped to {cap.sw.length} software area{cap.sw.length === 1 ? "" : "s"}{cap.ro ? " · read-only" : ""}{cap.kill ? " · kill-switch" : ""}{cap.appr ? " · policy approval" : ""}</div>
      <div className="tabs">{(isSw ? SW : HW).map(([k, t]) => <button key={k} className={(isSw ? swTab : hwTab) === k ? "active" : ""} onClick={() => isSw ? setSwTab(k as SwTab) : setHwTab(k as HwTab)}>{t}</button>)}</div>

      <div className="main">
        {/* ===================== SOFTWARE ===================== */}
        {isSw && swTab === "dash" && <>
          <div className="pg-h"><div><h2>Governance Dashboard</h2><p>Live posture across registered AI systems, EVA-governed decisions, sovereignty and the tamper-evident audit chain.</p></div></div>
          <div className="grid">
            <div className="card udoc"><h3>Systems Governed</h3><div className="metric">{models.length}</div></div>
            <div className="card udoc"><h3>Decisions</h3><div className="metric">{decisions.length}<small>EVA-governed</small></div></div>
            <div className="card udoc"><h3>Sovereignty</h3><div className="metric">{sovPct}%<small>ZA jurisdiction</small></div></div>
            <div className="card udoc"><h3>Bias Flags</h3><div className="metric">{bias?.fairness_flagged ?? "—"}<small>of {bias?.decisions_scanned ?? 0} scanned</small></div></div>
            <div className="card udoc"><h3>Audit Chain</h3><div className="metric" style={{ color: chain?.intact ? "var(--ok)" : "var(--bad)" }}>{chain ? (chain.intact ? "INTACT" : "BROKEN") : "—"}<small>{chain?.records ?? 0} records</small></div></div>
          </div>
          <div className="panel"><h3>Live Audit Stream <span className="tag PASS">● LIVE</span></h3>
            <div className="stream">{audit.length ? audit.slice(0, 14).map((r, i) => <div className="ev" key={i}><span className="t">{String(r.created_at || "").slice(11, 19)}</span><span className="e">{r.event_type || r.event || "EVENT"}</span><span className="d">{typeof r.detail === "string" ? r.detail : JSON.stringify(r.detail || r.classification || "")}</span></div>) : <p className="muted">No audit events yet — run an EVA decision.</p>}</div></div>
        </>}

        {isSw && swTab === "registry" && <>
          <div className="pg-h"><div><h2>AI System Registry</h2><p>Every AI system must register before any consequential decision (Pillar VIII). Kill-switch per system.</p></div></div>
          <div className="panel"><h3>Register a system</h3>
            <div className="row">
              <input placeholder="model id" value={f.model_id} onChange={e => setF({ ...f, model_id: e.target.value })} />
              <input placeholder="name" value={f.name} onChange={e => setF({ ...f, name: e.target.value })} />
              <input placeholder="operator id" value={f.operator_id} onChange={e => setF({ ...f, operator_id: e.target.value })} />
              <select value={f.risk_tier} onChange={e => setF({ ...f, risk_tier: e.target.value })}><option>MINIMAL</option><option>NOTABLE</option><option>HIGH</option><option>UNACCEPTABLE</option></select>
              <button className="btn" onClick={registerModel} disabled={!f.model_id || !f.name}>Register</button></div></div>
          <div className="panel"><h3>Registered systems — {models.length}</h3>
            <table><thead><tr><th>System ID</th><th>Name</th><th>Operator</th><th>Risk</th><th>Status</th><th>Control</th></tr></thead>
              <tbody>{models.map(m => <tr key={m.model_id}><td className="mono">{m.model_id}</td><td>{m.name}</td><td>{m.operator_id || "—"}</td><td><span className={`tag ${m.risk_tier}`}>{m.risk_tier}</span></td><td><span className={`tag ${m.status}`}>{m.status}</span></td><td>{cap.kill ? <button className={`btn sm ${m.status === "ACTIVE" ? "danger" : ""}`} onClick={() => toggle(m.model_id, m.status)}>{m.status === "ACTIVE" ? "Suspend" : "Resume"}</button> : <span className="muted">—</span>}</td></tr>)}{!models.length && <tr><td colSpan={6} className="muted">No systems registered.</td></tr>}</tbody></table></div>
        </>}

        {isSw && swTab === "eva" && <>
          <div className="pg-h"><div><h2>EVA Engine</h2><p>The non-bypassable governance path — 6-dimensional scoring (validity, risk, compliance, stability, fairness, sovereignty), sealed verdict, immutable audit. Fail-closed for critical classes.</p></div></div>
          <div className="panel"><h3>Run a governed decision</h3>
            <div className="row"><select value={scenario} onChange={e => setScenario(e.target.value)}><option value="healthy">Healthy model</option><option value="biased">Biased + high-risk</option><option value="breach">Sovereignty breach</option></select>
              <button className="btn" onClick={decide}>Evaluate · model {models[0]?.model_id || "model-001"}</button></div>
            {verdict && !verdict.error && <>
              <div className="eva-verdict">
                <span className={`eva-big ${verdict.decision}`}>{verdict.decision}</span>
                <div className="composite"><div className="cscore">{verdict.composite_eva ?? "—"}<small>/10</small></div><div className="lat">Composite EVA Score</div></div>
                <div><div className="lat">sealed {String(verdict.seal || "").slice(0, 20)}…</div>
                  <div className="lat">latency {verdict.latency_ms}ms / budget {verdict.budget_ms}ms · within budget {String(verdict.within_budget)}</div>
                  {verdict.certificate_id && <div className="lat" style={{ color: "var(--ok)" }}>✓ EVA Certificate {verdict.certificate_id} · verifiable</div>}
                  <div className="bar" style={{ width: 200, marginTop: 5 }}><i style={{ width: Math.min(100, (verdict.latency_ms / (verdict.budget_ms || 1)) * 100) + "%" }} /></div></div></div>
              <div className="meters">
                {verdict.dimensions && Object.entries(verdict.dimensions).map(([k, val]: any) => (
                  <Meter key={k} label={k} value={(Number(val) || 0) / 10} raw={val} invert={k === "Risk" || k === "Impact"} />
                ))}
                <Meter label="Sovereignty (ECS)" value={verdict.ecs} />
              </div>
              {verdict.block_reasons?.length > 0 && <div className="err" style={{ marginTop: 10 }}>{verdict.decision} — {verdict.block_reasons.join(" | ")}</div>}
            </>}
            {verdict?.error && <div className="err">{verdict.error}</div>}
          </div>
          <div className="panel"><h3>Recent EVA decisions — {decisions.length}</h3>
            <table><thead><tr><th>ID</th><th>Decision</th><th>SVS</th><th>Sovereign</th><th>Latency</th><th>Time</th></tr></thead>
              <tbody>{decisions.slice(0, 20).map(d => <tr key={d.id}><td className="mono">{d.id}</td><td><span className={`tag ${d.decision}`}>{d.decision}</span></td><td>{d.svs}</td><td>{String(d.sovereign)}</td><td>{d.latency_ms}ms</td><td className="mono">{String(d.created_at || "").slice(11, 19)}</td></tr>)}{!decisions.length && <tr><td colSpan={6} className="muted">No decisions yet.</td></tr>}</tbody></table></div>
          <div className="panel"><h3>EVA Certificates — {certs.length} <span className="tag PASS">signed · verifiable</span></h3>
            <table><thead><tr><th>Certificate ID</th><th>Model</th><th>Composite</th><th>Issued</th></tr></thead>
              <tbody>{certs.slice(0, 10).map((ct: any) => <tr key={ct.certificate_id}><td className="mono">{ct.certificate_id}</td><td>{ct.model_id}</td><td>{ct.composite_eva}/10</td><td className="mono">{String(ct.issued_at || "").slice(0, 19)}</td></tr>)}{!certs.length && <tr><td colSpan={4} className="muted">No certificates yet — an APPROVE outcome issues one.</td></tr>}</tbody></table></div>
        </>}

        {isSw && swTab === "policy" && <>
          <div className="pg-h"><div><h2>Policy-to-Code Enforcement</h2><p>Upload passed / applicable legislation (PDF · DOCX · TXT). UDOC compiles transparent, editable rules; once you activate a pack, the rules are enforced inside the EVA decision path.</p></div></div>
          <div className="panel"><h3>Upload legislation</h3>
            <div className="row">
              <input placeholder="policy name (e.g. National AI Act)" value={pform.name} onChange={e => setPform({ ...pform, name: e.target.value })} style={{ minWidth: 220 }} />
              <input placeholder="jurisdiction" value={pform.jurisdiction} onChange={e => setPform({ ...pform, jurisdiction: e.target.value })} style={{ width: 110 }} />
              <select value={pform.sector} onChange={e => setPform({ ...pform, sector: e.target.value })}><option>PUBLIC</option><option>PRIVATE</option><option>GENERAL</option></select>
              <input type="file" accept=".pdf,.docx,.txt" onChange={e => setPfile(e.target.files?.[0] || null)} />
              <button className="btn" onClick={doUploadPolicy} disabled={!pfile || !pform.name}>Compile rules</button>
            </div>
            <p className="note-hw">Extraction is assistive — review and edit the compiled rules before activation. Nothing is enforced until a pack is ACTIVE.</p></div>
          {activePol && <div className="grid">
            <div className="card udoc"><h3>Active Packs</h3><div className="metric">{activePol.active_packs?.length || 0}</div></div>
            <div className="card udoc"><h3>Enforced Rules</h3><div className="metric">{activePol.enforced_rules || 0}</div></div></div>}
          <div className="panel"><h3>Policy packs — {packs.length}</h3>
            <table><thead><tr><th>Name</th><th>Sector</th><th>Jurisdiction</th><th>Rules</th><th>Status</th><th>Action</th></tr></thead>
              <tbody>{packs.map(p => <tr key={p.id}><td>{p.name}</td><td>{p.sector}</td><td>{p.jurisdiction}</td><td>{p.rule_count}</td><td><span className={`tag ${p.status === "ACTIVE" ? "ACTIVE" : "REVIEW"}`}>{p.status}</span></td><td><button className="btn sm ghost" onClick={() => loadPack(p.id)}>Review</button>{p.status !== "ACTIVE" && <button className="btn sm" style={{ marginLeft: 6 }} onClick={() => activatePack(p.id)}>Activate</button>}{(p.status === "DRAFT" || p.status === "PENDING_APPROVAL") && <button className="btn sm ghost" style={{ marginLeft: 6 }} onClick={() => doSubmitPack(p.id)}>Submit→COB</button>}</td></tr>)}{!packs.length && <tr><td colSpan={6} className="muted">No policy packs yet — upload legislation above.</td></tr>}</tbody></table></div>
          {versions.length > 0 && <div className="panel"><h3>Policy versions <span className="tag PASS">hot-reload {hot?.last_reload_ms ?? "—"}ms</span></h3>
            <table><thead><tr><th>v</th><th>State</th><th>Rules</th><th>Proposed by</th><th>COB</th></tr></thead>
              <tbody>{versions.map((v: any) => <tr key={v.id}><td>{v.version}</td><td><span className={`tag ${v.state === "ACTIVE" ? "ACTIVE" : (v.state === "VETOED" ? "FAIL" : "REVIEW")}`}>{v.state}</span></td><td>{v.rule_count}</td><td className="mono" style={{ fontSize: ".7rem" }}>{v.proposed_by}</td><td>{v.state === "PROPOSED" && cap.appr && <button className="btn sm" onClick={() => doApproveVer(v.id, v.pack_id)}>Approve</button>}</td></tr>)}</tbody></table>
            <p className="note-hw">COB approval (gov/admin) freezes a signed version and hot-reloads it into the live EVA path. Veto is available in the admin console.</p></div>}
          {packDetail && <div className="panel"><h3>{packDetail.pack.name} — {packDetail.rules.length} rules <span className={`tag ${packDetail.pack.status === "ACTIVE" ? "ACTIVE" : "REVIEW"}`}>{packDetail.pack.status}</span></h3>
            <p className="muted" style={{ fontSize: ".74rem", marginBottom: 10 }}>{packDetail.pack.summary}</p>
            <table><thead><tr><th>Code</th><th>Kind</th><th>Severity</th><th>Source clause</th><th>On</th></tr></thead>
              <tbody>{packDetail.rules.map((r: any) => <tr key={r.id}><td className="mono">{r.code}</td><td><span className="tag">{r.kind}</span></td><td><span className={`tag ${r.severity}`}>{r.severity}</span></td><td style={{ fontSize: ".72rem" }}>{r.source_excerpt}</td><td><button className={`btn sm ${r.enabled ? "" : "ghost"}`} onClick={() => toggleRule(r.id, !r.enabled)}>{r.enabled ? "ON" : "off"}</button></td></tr>)}</tbody></table></div>}
        </>}

        {isSw && swTab === "intel" && <>
          <div className="pg-h"><div><h2>G.O.D.S Intelligence</h2><p>Retrieval-grounded intelligence over your curated corpus (internal — operator / gov / admin). Answers cite ingested documents and never invent sources. Human primacy is non-overridable.</p></div></div>
          <div className="grid">
            <div className="card udoc"><h3>Corpus</h3><div className="metric">{intelSt?.corpus_docs ?? "—"}<small>documents</small></div></div>
            <div className="card udoc"><h3>Characters</h3><div className="metric">{intelSt?.corpus_chars ?? 0}</div></div>
            <div className="card udoc"><h3>Maturity</h3><div className="metric" style={{ fontSize: ".85rem" }}>{intelSt?.stage_name || "Automated · Assistive"}</div></div>
          </div>
          <div className="panel"><h3>Ask the corpus</h3>
            <div className="row"><input placeholder="ask a question grounded in the corpus" value={askQ} onChange={e => setAskQ(e.target.value)} style={{ minWidth: 260 }} /><button className="btn" onClick={doAsk} disabled={!askQ}>Ask</button></div>
            {askA && <div className="panel" style={{ marginTop: 10 }}><p style={{ whiteSpace: "pre-wrap" }}>{askA.answer}</p>{askA.citations?.length > 0 && <p className="muted" style={{ fontSize: ".72rem" }}>Sources: {askA.citations.map((c: any) => c.title).join(" · ")}</p>}</div>}</div>
          <div className="panel"><h3>Add to corpus</h3>
            <div className="row"><input placeholder="title" value={iText.title} onChange={e => setIText({ ...iText, title: e.target.value })} /><select value={iText.category} onChange={e => setIText({ ...iText, category: e.target.value })}><option>GENERAL</option><option>SPEC</option><option>PATENT</option><option>LEGAL</option><option>FINANCIAL</option></select></div>
            <textarea placeholder="paste text to ingest" value={iText.text} onChange={e => setIText({ ...iText, text: e.target.value })} style={{ width: "100%", minHeight: 80, marginTop: 8, background: "#0b1830", color: "#e8edf6", border: "1px solid #1c2a45", borderRadius: 8, padding: 8 }} />
            <div className="row" style={{ marginTop: 8 }}><button className="btn" onClick={doIntelText} disabled={!iText.title || !iText.text}>Add text</button>
              <input type="file" accept=".pdf,.docx,.txt,.md,.html" onChange={e => setIFile(e.target.files?.[0] || null)} />
              <button className="btn" onClick={doIntelFile} disabled={!iFile}>Upload document</button></div>
            <p className="note-hw">Large Google-Drive corpora load server-side via tools/ingest_corpus.py; single documents upload here.</p></div>
          <div className="panel"><h3>Corpus documents — {intelDocs.length}</h3>
            <table><thead><tr><th>Title</th><th>Category</th><th>Active</th></tr></thead>
              <tbody>{intelDocs.slice(0, 30).map((d: any) => <tr key={d.id}><td>{d.title}</td><td><span className="tag">{d.category}</span></td><td>{String(d.active)}</td></tr>)}{!intelDocs.length && <tr><td colSpan={3} className="muted">Corpus empty — add text or upload a document (or load your Drive zip server-side).</td></tr>}</tbody></table></div>
        </>}

        {isSw && swTab === "tenancy" && <>
          <div className="pg-h"><div><h2>Tenancy &amp; Plan</h2><p>Your organisation's commercial plan, decision usage and API keys on the G.O.D.S platform.</p></div></div>
          {plan && plan.tenant_id ? <>
            <div className="grid">
              <div className="card udoc"><h3>Plan</h3><div className="metric" style={{ fontSize: "1rem" }}>{plan.tier_name}<small>{plan.status}</small></div></div>
              <div className="card udoc"><h3>Decisions used</h3><div className="metric">{plan.usage_decisions}<small>{plan.decision_quota < 0 ? "of unlimited" : ("of " + plan.decision_quota)}</small></div></div>
              <div className="card udoc"><h3>Max models</h3><div className="metric">{plan.entitlements?.max_models < 0 ? "∞" : plan.entitlements?.max_models}</div></div>
              <div className="card udoc"><h3>COB sign-off</h3><div className="metric" style={{ fontSize: "1rem" }}>{plan.entitlements?.cob ? "required" : "not required"}</div></div>
            </div>
            <div className="panel"><h3>API keys — {myKeys.length} <button className="btn sm" style={{ float: "right" }} onClick={doIssueKey}>+ Issue key</button></h3>
              <table><thead><tr><th>Prefix</th><th>Name</th><th>Active</th><th>Last used</th></tr></thead>
                <tbody>{myKeys.map((k: any) => <tr key={k.id}><td className="mono">{k.prefix}…</td><td>{k.name}</td><td>{String(k.active)}</td><td className="mono">{String(k.last_used_at || "—").slice(0, 19)}</td></tr>)}{!myKeys.length && <tr><td colSpan={4} className="muted">No keys yet — issue one to call the API as a service (X-API-Key).</td></tr>}</tbody></table></div>
          </> : <div className="panel"><p className="muted">Signed in as platform staff (not tenant-scoped) — tenant plans are managed in the admin console.</p></div>}
        </>}

        {isSw && swTab === "audit" && <>
          <div className="pg-h"><div><h2>Audit Trail</h2><p>Tamper-evident, HMAC-chained, Merkle-linked. Every governed action recorded and verifiable.</p></div></div>
          <div className="grid">
            <div className="card udoc"><h3>Records</h3><div className="metric">{chain?.records ?? audit.length}</div></div>
            <div className="card udoc"><h3>Chain Integrity</h3><div className="metric" style={{ color: chain?.intact ? "var(--ok)" : "var(--bad)" }}>{chain ? (chain.intact ? "INTACT" : "BROKEN") : "—"}</div></div>
            <div className="card udoc"><h3>Merkle Root</h3><div className="metric" style={{ fontSize: ".78rem", wordBreak: "break-all" }}>{merkle ? merkle.slice(0, 22) + "…" : "—"}</div></div></div>
          <div className="panel"><h3>Audit records</h3><div className="stream">{audit.length ? audit.map((r, i) => <div className="ev" key={i}><span className="t">{String(r.created_at || "").slice(11, 19)}</span><span className="e">{r.event_type || r.event || "EVENT"}</span><span className="d">{typeof r.detail === "string" ? r.detail : JSON.stringify(r.detail || r.classification || "")}</span></div>) : <p className="muted">No records yet.</p>}</div></div>
        </>}

        {isSw && swTab === "compliance" && <>
          <div className="pg-h"><div><h2>Compliance</h2><p>Regulatory frameworks tracked by UDOC; per-model compliance sweep.</p></div></div>
          <div className="panel"><h3>Regulatory landscape — live status</h3>
            <table><thead><tr><th>Instrument</th><th>Juris.</th><th>Status</th><th>Relevance to AI governance</th></tr></thead><tbody>
              <tr><td>EU AI Act · Reg 2024/1689</td><td>EU</td><td><span className="tag PASS">IN FORCE · phased</span></td><td>Prohibited practices &amp; GPAI in force; high-risk obligations from 2 Aug 2026.</td></tr>
              <tr><td>POPIA · Act 4 of 2013</td><td>ZA</td><td><span className="tag PASS">IN FORCE</span></td><td>Automated decision-making &amp; personal information (s71).</td></tr>
              <tr><td>Constitution of RSA · 1996</td><td>ZA</td><td><span className="tag PASS">IN FORCE</span></td><td>Equality (s9), expression (s16), just administrative action (s33).</td></tr>
              <tr><td>Draft National AI Policy · GG 54477</td><td>ZA</td><td><span className="tag FAIL">WITHDRAWN 26 Apr 2026</span></td><td>Draft withdrawn after citation errors — no enacted AI-specific law in ZA yet.</td></tr>
            </tbody></table>
            <p className="note-hw">UDOC governs to whatever legislation applies to you — activate the relevant instrument in Policy-to-Code and EVA enforces it.{activePol ? ` Currently enforcing ${activePol.enforced_rules || 0} rules from ${activePol.active_packs?.length || 0} pack(s).` : ""}</p></div>
          <div className="panel"><h3>Frameworks</h3><div className="row">{frameworks.map(fw => <span className="tag" key={fw} style={{ fontSize: ".7rem", padding: "5px 10px" }}>{fw}</span>)}{!frameworks.length && <span className="muted">—</span>}</div></div>
          <div className="panel"><h3>Compliance sweep — {sweep?.checked ?? 0} checked</h3>
            <table><thead><tr><th>Model</th><th>Risk</th><th>Status</th><th>Compliant</th></tr></thead>
              <tbody>{(sweep?.results || []).map((r: any, i: number) => <tr key={i}><td className="mono">{r.model_id}</td><td>{r.risk_tier}</td><td><span className={`tag ${r.status}`}>{r.status}</span></td><td><span className={`tag ${r.compliant === false ? "FAIL" : r.compliant ? "PASS" : "REVIEW"}`}>{r.compliant == null ? "PENDING" : String(r.compliant)}</span></td></tr>)}{!(sweep?.results || []).length && <tr><td colSpan={4} className="muted">No models to sweep.</td></tr>}</tbody></table></div>
        </>}

        {/* ===================== HARDWARE ===================== */}
        {!isSw && hwTab === "hqos" && <>
          <div className="pg-h"><div><h2>HQ-OS · Hybrid Classical + Quantum</h2><p>The sovereign operating substrate. Post-quantum cryptography is active today; quantum phases are on the forward roadmap.</p></div></div>
          <div className="grid" style={{ gridTemplateColumns: "repeat(auto-fit,minmax(190px,1fr))" }}>
            <div className="phase on"><h4>Phase 1 · PQC Baseline</h4><small>ACTIVE — CRYSTALS-Kyber-1024 + Dilithium</small></div>
            <div className="phase next"><h4>Phase 2 · Cloud QPU</h4><small>NEXT — quantum acceleration via cloud</small></div>
            <div className="phase future"><h4>Phase 3 · On-Prem QPU</h4><small>FORECAST — sovereign on-prem quantum</small></div>
            <div className="phase future"><h4>Phase 4 · AQGN</h4><small>FORECAST — quantum network services</small></div>
            <div className="phase future"><h4>Phase 5 · Global</h4><small>FORECAST — global sovereign mesh</small></div>
          </div>
          <div className="panel"><h3>Active Cryptographic Posture</h3>
            <div className="row">{(frameworks.filter(x => /PQC|FIPS|NIST/i.test(x)).length ? frameworks.filter(x => /PQC|FIPS|NIST/i.test(x)) : ["NIST PQC", "FIPS 140-3"]).map(x => <span className="tag PASS" key={x} style={{ fontSize: ".7rem", padding: "5px 10px" }}>{x}</span>)}
              <span className="tag PASS" style={{ fontSize: ".7rem", padding: "5px 10px" }}>CRYSTALS-Kyber-1024</span><span className="tag PASS" style={{ fontSize: ".7rem", padding: "5px 10px" }}>CRYSTALS-Dilithium</span></div>
            <p className="note-hw">⚠ Phases 2–5 and QPU/AQGN are forecast capabilities — shown for roadmap transparency, not live quantum hardware.</p></div>
        </>}

        {!isSw && hwTab === "edge" && <>
          <div className="pg-h"><div><h2>Sovereign Edge Components</h2><p>UDOC governance runs to the edge: each component enforces the same fail-closed governance close to where decisions happen.</p></div></div>
          {[["🧩", "UDOC Edge Node", "Runs local EVA governance at the edge; fail-closed when disconnected from core."],
            ["🚪", "UDOC Gateway", "Sovereign ingress — routes and governs traffic into the platform."],
            ["🤖", "UDOC Agent", "On-host enforcement agent for governed workloads."],
            ["🔗", "UDOC Sidecar", "Per-service governance sidecar for fine-grained control."],
            ["💽", "HW Bring-up", "Bootable self-test + live banner; sovereign OS image for hardware."]].map(([i, n, d]) =>
            <div className="comp" key={n}><span className="ci">{i}</span><div><h4>{n}</h4><p>{d}</p></div><span className="cs">DEFINED · IN REPO</span></div>)}
          <p className="note-hw">⚠ Components are implemented in the repository; live per-node telemetry is not yet wired, so status reflects definition, not runtime health.</p>
        </>}

        {!isSw && hwTab === "sovereignty" && <>
          <div className="pg-h"><div><h2>Sovereignty Posture</h2><p>UDOC verifies that decisions execute under ZA jurisdiction across the network and storage path. Live posture below.</p></div></div>
          <div className="grid">
            <div className="card" style={{ borderTop: "3px solid var(--cyan)" }}><h3>Sovereign Rate</h3><div className="metric">{sovPct}%</div></div>
            <div className="card" style={{ borderTop: "3px solid var(--cyan)" }}><h3>Decisions</h3><div className="metric">{sov?.decisions ?? "—"}</div></div>
            <div className="card" style={{ borderTop: "3px solid var(--cyan)" }}><h3>Breaches</h3><div className="metric" style={{ color: (sov?.sovereignty_breaches ?? 0) > 0 ? "var(--bad)" : "var(--ok)" }}>{sov?.sovereignty_breaches ?? "—"}</div></div></div>
          <div className="panel"><h3>Sovereign network checks (evaluated each decision)</h3>
            <table><thead><tr><th>Signal</th><th>What UDOC verifies</th><th>Last evaluation</th></tr></thead><tbody>
              {[["BGP", "Routing announced from ZA ASNs", verdict?.sovereign != null ? "from last EVA run" : "run a decision"],
                ["Traceroute", "Path stays within sovereign borders", "—"], ["DNSSEC", "Signed, sovereign DNS resolution", "—"],
                ["Storage", "Data at rest in ZA region", "—"], ["ECS", "Egress / compute sovereignty score", verdict ? String(verdict.ecs) : "—"]].map((r: any, i) =>
                <tr key={i}><td className="mono">{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>)}
            </tbody></table>
            <p className="note-hw">Live sovereign rate is computed by the backend over all governed decisions; per-signal telemetry is illustrative until edge nodes report in.</p></div>
        </>}

        {!isSw && hwTab === "killswitch" && <>
          <div className="pg-h"><div><h2>Hardware Kill-Switch</h2><p>Sovereign authority to halt any registered AI system. Suspension is enforced fail-closed — a suspended system cannot transact.</p></div></div>
          <div className="panel"><h3>Registered systems — {models.length}</h3>
            <table><thead><tr><th>System ID</th><th>Name</th><th>Risk</th><th>Status</th><th>Kill-switch</th></tr></thead>
              <tbody>{models.map(m => <tr key={m.model_id}><td className="mono">{m.model_id}</td><td>{m.name}</td><td><span className={`tag ${m.risk_tier}`}>{m.risk_tier}</span></td><td><span className={`tag ${m.status}`}>{m.status}</span></td><td><button className={`btn sm ${m.status === "ACTIVE" ? "danger" : ""}`} onClick={() => toggle(m.model_id, m.status)}>{m.status === "ACTIVE" ? "HALT (suspend)" : "Restore"}</button></td></tr>)}{!models.length && <tr><td colSpan={5} className="muted">No systems registered.</td></tr>}</tbody></table></div>
        </>}

        {msg && <div className="ok">{msg}</div>}{err && <div className="err">{err}</div>}
        <div className="foot center">UDOC SOVEREIGN GOVERNANCE · EVA ENGINE · © 2026 SASHIN J. SINGH · PRE-REGISTRATION</div>
      </div>
    </div>
  );
}
