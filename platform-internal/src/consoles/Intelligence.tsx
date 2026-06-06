import { useEffect, useState } from "react";
import { api } from "../api";

// G.O.D.S Intelligence — internal admin console. Corpus-grounded knowledge + governance brain,
// hard-wired to Pillar VIII (Human Primacy). INTERNAL ONLY (the backend enforces role gating).
export function Intelligence() {
  const [st, setSt] = useState<any>(null);
  const [docs, setDocs] = useState<any[]>([]);
  const [q, setQ] = useState("What outcomes and dimensions does EVA use?");
  const [ans, setAns] = useState<any>(null);
  const [busy, setBusy] = useState(false);
  const [form, setForm] = useState({ title: "", category: "GENERAL", text: "" });
  const [msg, setMsg] = useState(""); const [err, setErr] = useState("");

  async function load() {
    try { setSt(await api.get("/intel/state")); setDocs(await api.get("/intel/docs")); }
    catch (e: any) { setErr(e.message); }
  }
  useEffect(() => { load(); }, []);

  async function ask() {
    setBusy(true); setAns(null); setErr("");
    try { setAns(await api.post("/intel/ask", { query: q })); } catch (e: any) { setErr(e.message); }
    setBusy(false);
  }
  async function addDoc() {
    if (!form.title || !form.text) { setErr("title and text required"); return; }
    setMsg(""); setErr("");
    try { await api.post("/intel/ingest-text", form); setMsg(`Added “${form.title}” to the archive — knowledge updated.`);
      setForm({ title: "", category: "GENERAL", text: "" }); load(); } catch (e: any) { setErr(e.message); }
  }
  async function rm(id: number) { try { await api.del(`/intel/docs/${id}`); load(); } catch (e: any) { setErr(e.message); } }

  const stageColor = (s: string) => s === "ACTIVE" ? "var(--ok)" : "var(--warn)";

  return (<div>
    <div className="top"><h2>G.O.D.S Intelligence</h2>
      <span className="badge" style={{ background: "rgba(124,92,191,.15)", color: "var(--udoc, #7C5CBF)" }}>
        🔒 INTERNAL ONLY · {st?.pillar || "Pillar VIII"}</span></div>

    <div className="panel" style={{ borderLeft: "3px solid #7C5CBF" }}>
      <p style={{ fontSize: ".82rem" }}>Self-contained, corpus-grounded institutional intelligence — reasons only over the G.O.D.S archive,
        hard-wired to human primacy, and never exposed to SaaS clients. “Training” = curating the archive below.</p>
    </div>

    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))", gap: 12, marginBottom: 14 }}>
      <div className="card"><h3>Maturity Stage</h3><div style={{ fontSize: "1.1rem", color: "#7C5CBF" }}>{st ? `${st.stage} · ${st.stage_name}` : "—"}</div></div>
      <div className="card"><h3>Archive Documents</h3><div style={{ fontSize: "1.6rem" }}>{st?.corpus_docs ?? "—"}</div></div>
      <div className="card"><h3>Knowledge (chars)</h3><div style={{ fontSize: "1.6rem" }}>{st?.corpus_chars?.toLocaleString?.() ?? "—"}</div></div>
    </div>

    <div className="panel"><h3>Ask G.O.D.S Intelligence</h3>
      <div style={{ display: "flex", gap: 8 }}>
        <input style={{ flex: 1 }} value={q} onChange={e => setQ(e.target.value)} placeholder="Ask about G.O.D.S, UDOC, EVA, the mandate…" />
        <button className="btn" onClick={ask} disabled={busy}>{busy ? "Thinking…" : "Ask"}</button></div>
      {ans && <div style={{ marginTop: 12 }}>
        {ans.blocked && <div className="err" style={{ marginBottom: 8 }}>⛔ {ans.pillar} — refused (non-overridable)</div>}
        <pre style={{ whiteSpace: "pre-wrap", fontSize: ".82rem", background: "var(--panel,#0c1422)", padding: 12, borderRadius: 8, margin: 0 }}>{ans.answer}</pre>
        {ans.citations?.length > 0 && <div style={{ marginTop: 8 }}>{ans.citations.map((c: any) => <span key={c.id} className="badge" style={{ marginRight: 6 }}>{c.title}</span>)}</div>}
      </div>}
    </div>

    <div className="panel"><h3>Maturity Ladder · AI → AGI → Singularity</h3>
      {(st?.maturity || []).map((m: any) => <div key={m.stage} style={{ display: "flex", gap: 10, padding: "7px 0", borderBottom: "1px solid var(--rule,#1c2738)" }}>
        <span style={{ fontFamily: "monospace", color: stageColor(m.status), minWidth: 70 }}>{m.status}</span>
        <div><b style={{ fontSize: ".85rem" }}>Stage {m.stage} · {m.name}</b>
          <div style={{ fontSize: ".76rem", color: "var(--text)" }}>{m.summary}</div>
          <div style={{ fontSize: ".7rem", color: "var(--warn)" }}>Gate: {m.gate}</div></div></div>)}
      <p style={{ fontSize: ".7rem", color: "var(--warn)", marginTop: 8 }}>Stages 2–5 are gated roadmap — not present capability. AGI is governable by UDOC; Singularity governance is treaty-level.</p>
    </div>

    <div className="panel"><h3>250-Year Mandate</h3>
      {(st?.mandate || []).map((p: any, i: number) => <div key={i} style={{ display: "flex", gap: 10, padding: "5px 0" }}>
        <span className="badge" style={{ minWidth: 70 }}>{p.status}</span>
        <div><b style={{ fontSize: ".82rem" }}>{p.phase}</b> <span style={{ fontSize: ".72rem", color: "var(--text)" }}>· {p.horizon}</span>
          <div style={{ fontSize: ".76rem", color: "var(--text)" }}>{p.focus}</div></div></div>)}
    </div>

    <div className="panel"><h3>Constitutional Guardrails — non-overridable</h3>
      <ul style={{ margin: 0, paddingLeft: 18, fontSize: ".8rem" }}>{(st?.guardrails || []).map((g: string, i: number) => <li key={i} style={{ marginBottom: 4 }}>{g}</li>)}</ul>
    </div>

    <div className="panel"><h3>Knowledge Archive — add / remove training data</h3>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 140px", gap: 8, marginBottom: 8 }}>
        <input value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} placeholder="document title" />
        <select value={form.category} onChange={e => setForm({ ...form, category: e.target.value })}>
          <option>GENERAL</option><option>PATENT</option><option>SPEC</option><option>BRAND</option><option>MANDATE</option><option>FINANCIAL</option><option>LEGAL</option><option>MEMOIR</option></select></div>
      <textarea value={form.text} onChange={e => setForm({ ...form, text: e.target.value })} placeholder="paste document text…" rows={3} style={{ width: "100%", marginBottom: 8 }} />
      <button className="btn" onClick={addDoc} disabled={!form.title || !form.text}>Add to archive</button>
      {msg && <div style={{ color: "var(--ok)", fontSize: ".78rem", marginTop: 6 }}>{msg}</div>}
      <table style={{ marginTop: 12 }}><thead><tr><th>Title</th><th>Category</th><th>Chars</th><th>On</th><th></th></tr></thead>
        <tbody>{docs.map(d => <tr key={d.id}><td>{d.title}</td><td>{d.category}</td><td>{d.char_len}</td><td>{d.active ? "✓" : "—"}</td>
          <td><a style={{ color: "var(--bad)", cursor: "pointer", fontSize: ".75rem" }} onClick={() => rm(d.id)}>remove</a></td></tr>)}
          {!docs.length && <tr><td colSpan={5} style={{ color: "var(--rule)" }}>Archive empty — add documents above (or ingest from the data room).</td></tr>}</tbody></table>
    </div>

    {err && <div className="err">{err}</div>}
    <p style={{ fontSize: ".68rem", color: "var(--rule)", marginTop: 14 }}>PRE-REGISTRATION · INTERNAL · © 2026 Sashin J. Singh — corpus-grounded; not client-exposed.</p>
  </div>);
}
