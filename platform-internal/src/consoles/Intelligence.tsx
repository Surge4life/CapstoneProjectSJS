import { useEffect, useState } from "react";
import { api } from "../api";

const CATEGORIES = [
  "GENERAL", "GBS", "CANON", "EIF", "POLICY", "UDOC", "PATENT", "SPEC", "BRAND", "MANDATE", "FINANCIAL", "LEGAL", "MEMOIR",
];

const QUICK_ASK = [
  "What is EVA and what dimensions does it use?",
  "What is the four-division GBS architecture?",
  "What does Sovereign-Verified mean?",
  "What is human primacy under Pillar VIII?",
  "Summarise EIF Diamond vs systems certification",
];

export function Intelligence() {
  const [st, setSt] = useState<any>(null);
  const [docs, setDocs] = useState<any[]>([]);
  const [gaps, setGaps] = useState<any>(null);
  const [q, setQ] = useState(QUICK_ASK[0]);
  const [ans, setAns] = useState<any>(null);
  const [busy, setBusy] = useState(false);
  const [form, setForm] = useState({ title: "", category: "GBS", text: "", division: "GODS" });
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const [filterCat, setFilterCat] = useState("");

  async function load() {
    try {
      const [state, list, g] = await Promise.all([
        api.get("/intel/state"),
        api.get("/intel/docs"),
        api.get("/intel/gaps").catch(() => null),
      ]);
      setSt(state);
      setDocs(Array.isArray(list) ? list : list?.docs || []);
      setGaps(g);
      setErr("");
    } catch (e: any) {
      setErr(e.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function ask(query?: string) {
    const queryText = (query ?? q).trim();
    if (!queryText) return;
    setQ(queryText);
    setBusy(true);
    setAns(null);
    setErr("");
    try {
      setAns(await api.post("/intel/ask", { query: queryText }));
    } catch (e: any) {
      setErr(e.message);
    }
    setBusy(false);
  }

  async function addDoc() {
    if (!form.title || !form.text) {
      setErr("title and text required");
      return;
    }
    setMsg("");
    setErr("");
    try {
      await api.post("/intel/ingest-text", form);
      setMsg(`Added “${form.title}” to the GODS archive.`);
      setForm({ title: "", category: form.category, text: "", division: form.division });
      load();
    } catch (e: any) {
      setErr(e.message);
    }
  }

  async function rm(id: number) {
    try {
      await api.del(`/intel/docs/${id}`);
      load();
    } catch (e: any) {
      setErr(e.message);
    }
  }

  const stageColor = (s: string) => (s === "ACTIVE" ? "var(--ok)" : "var(--warn)");
  const byCat = st?.by_category || {};
  const visible = filterCat ? docs.filter((d) => d.category === filterCat) : docs;

  return (
    <div>
      <div className="top">
        <h2>G.O.D.S Intelligence</h2>
        <span className="badge" style={{ background: "rgba(124,92,191,.15)", color: "var(--udoc, #7C5CBF)" }}>
          🔒 INTERNAL ONLY · {st?.pillar || "Pillar VIII"}
        </span>
      </div>

      <div className="panel" style={{ borderLeft: "3px solid #7C5CBF" }}>
        <p style={{ fontSize: ".82rem", margin: 0 }}>
          Corpus-grounded institutional intelligence over the GODS archive only — not client Company Knowledge.
          Client KB is tenant-isolated on the SaaS path; this console is staff GODS archive (text ingest, Neon-capped).
          Human primacy is non-overridable.
        </p>
      </div>

      <div className="grid" style={{ marginTop: 12 }}>
        <div className="card">
          <h3>Maturity stage</h3>
          <div className="metric" style={{ fontSize: "1rem", color: "#7C5CBF" }}>
            {st ? `${st.stage} · ${st.stage_name}` : "—"}
          </div>
        </div>
        <div className="card">
          <h3>Archive docs</h3>
          <div className="metric">{st?.corpus_docs ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Knowledge (chars)</h3>
          <div className="metric">{st?.corpus_chars?.toLocaleString?.() ?? "—"}</div>
        </div>
        <div className="card">
          <h3>Categories</h3>
          <div className="metric" style={{ fontSize: ".85rem" }}>
            {Object.keys(byCat).length ? Object.keys(byCat).join(" · ") : "—"}
          </div>
        </div>
      </div>

      <div className="panel">
        <h3>Ask G.O.D.S Intelligence</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 10 }}>
          {QUICK_ASK.map((chip) => (
            <button key={chip} className="btn sm" disabled={busy} onClick={() => ask(chip)} style={{ fontSize: ".72rem" }}>
              {chip.slice(0, 42)}
              {chip.length > 42 ? "…" : ""}
            </button>
          ))}
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <input
            style={{ flex: 1 }}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && ask()}
            placeholder="Ask about G.O.D.S, UDOC, EVA, GBS, EIF…"
          />
          <button className="btn" onClick={() => ask()} disabled={busy}>
            {busy ? "Thinking…" : "Ask"}
          </button>
          <button className="btn" onClick={load} disabled={busy}>
            ↻
          </button>
        </div>
        {ans && (
          <div style={{ marginTop: 12 }}>
            {ans.blocked && (
              <div className="err" style={{ marginBottom: 8 }}>
                ⛔ {ans.pillar || "Pillar VIII"} — refused (non-overridable)
              </div>
            )}
            <pre
              style={{
                whiteSpace: "pre-wrap",
                fontSize: ".82rem",
                background: "var(--panel,#0c1422)",
                padding: 12,
                borderRadius: 8,
                margin: 0,
              }}
            >
              {ans.answer}
            </pre>
            {ans.citations?.length > 0 && (
              <div style={{ marginTop: 8 }}>
                {ans.citations.map((c: any) => (
                  <span key={c.id || c.title} className="badge" style={{ marginRight: 6 }}>
                    {c.title}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {gaps && (
        <div className="panel">
          <h3>Corpus gaps</h3>
          <pre style={{ fontSize: ".72rem", maxHeight: 120, overflow: "auto" }}>{JSON.stringify(gaps, null, 2).slice(0, 800)}</pre>
        </div>
      )}

      <div className="panel">
        <h3>Maturity ladder · AI → AGI → Singularity</h3>
        {(st?.maturity || []).map((m: any) => (
          <div key={m.stage} style={{ display: "flex", gap: 10, padding: "7px 0", borderBottom: "1px solid var(--rule,#1c2738)" }}>
            <span style={{ fontFamily: "monospace", color: stageColor(m.status), minWidth: 70 }}>{m.status}</span>
            <div>
              <b style={{ fontSize: ".85rem" }}>
                Stage {m.stage} · {m.name}
              </b>
              <div style={{ fontSize: ".76rem", color: "var(--text)" }}>{m.summary}</div>
              <div style={{ fontSize: ".7rem", color: "var(--warn)" }}>Gate: {m.gate}</div>
            </div>
          </div>
        ))}
        <p style={{ fontSize: ".7rem", color: "var(--warn)", marginTop: 8 }}>
          Stages 2–5 are gated roadmap — not present capability. Capstone proves Stage 1 assistive governance intelligence
          with an auditable track record.
        </p>
      </div>

      <div className="panel">
        <h3>250-Year Mandate</h3>
        {(st?.mandate || []).map((p: any, i: number) => (
          <div key={i} style={{ display: "flex", gap: 10, padding: "5px 0" }}>
            <span className="badge" style={{ minWidth: 70 }}>
              {p.status}
            </span>
            <div>
              <b style={{ fontSize: ".82rem" }}>{p.phase}</b>{" "}
              <span style={{ fontSize: ".72rem", color: "var(--text)" }}>· {p.horizon}</span>
              <div style={{ fontSize: ".76rem", color: "var(--text)" }}>{p.focus}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="panel">
        <h3>Constitutional guardrails — non-overridable</h3>
        <ul style={{ margin: 0, paddingLeft: 18, fontSize: ".8rem" }}>
          {(st?.guardrails || []).map((g: string, i: number) => (
            <li key={i} style={{ marginBottom: 4 }}>
              {g}
            </li>
          ))}
        </ul>
      </div>

      <div className="panel">
        <h3>Knowledge archive — staff text ingest</h3>
        <p style={{ fontSize: ".72rem", color: "var(--warn)", marginBottom: 8 }}>
          Neon ≤500MB — prefer short extracts. 11GB Drive stays external. Client Company Knowledge is a separate
          tenant-isolated path.
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 140px 120px", gap: 8, marginBottom: 8 }}>
          <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="document title" />
          <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
            {CATEGORIES.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
          <input value={form.division} onChange={(e) => setForm({ ...form, division: e.target.value })} placeholder="division" />
        </div>
        <textarea
          value={form.text}
          onChange={(e) => setForm({ ...form, text: e.target.value })}
          placeholder="paste document text…"
          rows={3}
          style={{ width: "100%", marginBottom: 8 }}
        />
        <button className="btn" onClick={addDoc} disabled={!form.title || !form.text}>
          Add to archive
        </button>
        {msg && (
          <div style={{ color: "var(--ok)", fontSize: ".78rem", marginTop: 6 }}>{msg}</div>
        )}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 12 }}>
          <button className="btn sm" onClick={() => setFilterCat("")}>
            All
          </button>
          {Object.keys(byCat).map((c) => (
            <button key={c} className="btn sm" onClick={() => setFilterCat(c)}>
              {c} ({byCat[c]})
            </button>
          ))}
        </div>
        <table style={{ marginTop: 12 }}>
          <thead>
            <tr>
              <th>Title</th>
              <th>Category</th>
              <th>Chars</th>
              <th>On</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {visible.map((d) => (
              <tr key={d.id}>
                <td>{d.title}</td>
                <td>{d.category}</td>
                <td>{d.char_len}</td>
                <td>{d.active ? "✓" : "—"}</td>
                <td>
                  <a style={{ color: "var(--bad)", cursor: "pointer", fontSize: ".75rem" }} onClick={() => rm(d.id)}>
                    remove
                  </a>
                </td>
              </tr>
            ))}
            {!visible.length && (
              <tr>
                <td colSpan={5} style={{ color: "var(--rule)" }}>
                  Archive empty for this filter — add extracts above.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {err && <div className="err">{err}</div>}
      <p style={{ fontSize: ".68rem", color: "var(--rule)", marginTop: 14 }}>
        PRE-REGISTRATION · INTERNAL · © 2026 Sashin J. Singh — corpus-grounded; not client-exposed.
      </p>
    </div>
  );
}
