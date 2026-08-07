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
  const [filterCat, setFilterCat] = useState("");
  const [log, setLog] = useState<string[]>(["G.O.D.S Intelligence · internal archive only · Pillar VIII"]);

  function push(line: string) {
    setLog((prev) => [`${new Date().toLocaleTimeString()}  ${line}`, ...prev].slice(0, 24));
  }

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
      push(`archive docs=${state?.corpus_docs ?? "?"} chars=${state?.corpus_chars ?? "?"}`);
    } catch (e: any) {
      push(`ERROR ${e.message}`);
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
    try {
      const r = await api.post("/intel/ask", { query: queryText });
      setAns(r);
      push(`ASK ${queryText.slice(0, 48)}… blocked=${!!r.blocked}`);
    } catch (e: any) {
      push(`FAIL ask ${e.message}`);
    }
    setBusy(false);
  }

  async function addDoc() {
    if (!form.title || !form.text) {
      push("FAIL title and text required");
      return;
    }
    try {
      await api.post("/intel/ingest-text", form);
      push(`INGEST “${form.title}” [${form.category}]`);
      setForm({ title: "", category: form.category, text: "", division: form.division });
      load();
    } catch (e: any) {
      push(`FAIL ingest ${e.message}`);
    }
  }

  async function rm(id: number) {
    try {
      await api.del(`/intel/docs/${id}`);
      push(`REMOVE doc ${id}`);
      load();
    } catch (e: any) {
      push(`FAIL remove ${e.message}`);
    }
  }

  const stageColor = (s: string) => (s === "ACTIVE" ? "var(--ok)" : "var(--warn)");
  const byCat = st?.by_category || {};
  const visible = filterCat ? docs.filter((d) => d.category === filterCat) : docs;

  return (
    <div>
      <div className="top">
        <h2>G.O.D.S Intelligence</h2>
        <span className="badge">🔒 INTERNAL ONLY · {st?.pillar || "Pillar VIII"}</span>
      </div>

      <div className="banner warn">
        GODS archive only — not client Company Knowledge. Neon-capped text extracts. Human primacy non-overridable.
      </div>

      <div className="guide">
        <h3>Intelligence command path</h3>
        <div className="row" style={{ marginBottom: 8, flexWrap: "wrap" }}>
          {QUICK_ASK.map((chip) => (
            <button key={chip} className="btn sm" disabled={busy} onClick={() => ask(chip)}>
              {chip.slice(0, 36)}
              {chip.length > 36 ? "…" : ""}
            </button>
          ))}
          <button className="btn ghost" disabled={busy} onClick={load}>
            ↻ Refresh
          </button>
        </div>
      </div>

      <div className="grid">
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
        <div className="row">
          <input
            style={{ flex: 1, minWidth: 200 }}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && ask()}
            placeholder="Ask about G.O.D.S, UDOC, EVA, GBS, EIF…"
          />
          <button className="btn" onClick={() => ask()} disabled={busy}>
            {busy ? "Thinking…" : "Ask"}
          </button>
        </div>
        {ans && (
          <div style={{ marginTop: 12 }}>
            {ans.blocked && <div className="err">⛔ {ans.pillar || "Pillar VIII"} — refused (non-overridable)</div>}
            <div className="term">{ans.answer}</div>
            {ans.citations?.length > 0 && (
              <div className="row" style={{ marginTop: 8 }}>
                {ans.citations.map((c: any) => (
                  <span key={c.id || c.title} className="tag">
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
          <div className="term">{JSON.stringify(gaps, null, 2).slice(0, 900)}</div>
        </div>
      )}

      <div className="panel">
        <h3>Maturity ladder</h3>
        {(st?.maturity || []).map((m: any) => (
          <div key={m.stage} style={{ display: "flex", gap: 10, padding: "7px 0", borderBottom: "1px solid var(--rule)" }}>
            <span style={{ fontFamily: "monospace", color: stageColor(m.status), minWidth: 70 }}>{m.status}</span>
            <div>
              <b style={{ fontSize: ".85rem" }}>
                Stage {m.stage} · {m.name}
              </b>
              <div style={{ fontSize: ".76rem" }}>{m.summary}</div>
              <div style={{ fontSize: ".7rem", color: "var(--warn)" }}>Gate: {m.gate}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="panel">
        <h3>Knowledge archive — staff text ingest</h3>
        <div className="row">
          <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="title" style={{ flex: 1 }} />
          <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
            {CATEGORIES.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
          <input value={form.division} onChange={(e) => setForm({ ...form, division: e.target.value })} placeholder="division" style={{ width: 100 }} />
        </div>
        <textarea
          value={form.text}
          onChange={(e) => setForm({ ...form, text: e.target.value })}
          placeholder="paste extract…"
          rows={3}
          style={{ width: "100%", marginBottom: 8 }}
        />
        <button className="btn" onClick={addDoc} disabled={!form.title || !form.text}>
          Add to archive
        </button>
        <div className="row" style={{ marginTop: 10 }}>
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
                <td>
                  <span className="tag">{d.category}</span>
                </td>
                <td>{d.char_len}</td>
                <td>{d.active ? "✓" : "—"}</td>
                <td>
                  <button className="btn sm danger" onClick={() => rm(d.id)}>
                    remove
                  </button>
                </td>
              </tr>
            ))}
            {!visible.length && (
              <tr>
                <td colSpan={5}>Archive empty for filter</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="panel">
        <h3>Ops terminal</h3>
        <div className="term">{log.join("\n")}</div>
      </div>

      <p style={{ fontSize: ".68rem", color: "var(--rule)", marginTop: 14 }}>
        PRE-REGISTRATION · INTERNAL · corpus-grounded · not client-exposed
      </p>
    </div>
  );
}
