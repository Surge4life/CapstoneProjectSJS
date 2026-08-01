/* Intelligence density overlay — GODS archive ingest/ask/remove */
(function () {
  "use strict";

  window.askIntel = async function () {
    var a = document.getElementById("ians");
    if (!a) return;
    var q = (document.getElementById("iq") && document.getElementById("iq").value) || "";
    q = q.trim();
    if (!q) {
      a.textContent = "Enter a question.";
      return;
    }
    a.textContent = "…";
    try {
      var d = await api("/intel/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q }),
      });
      var t = (d.answer || d.response || "").toString();
      if (d.blocked) t = "[BLOCKED · Human Primacy] " + t;
      if (d.coverage != null) t += "\n\ncoverage=" + d.coverage;
      if (d.citations && d.citations.length)
        t +=
          "\n\nCitations:\n" +
          d.citations
            .map(function (c) {
              return "· " + (c.title || c.doc || JSON.stringify(c));
            })
            .join("\n");
      a.textContent = t || JSON.stringify(d);
    } catch (e) {
      a.textContent = e.message || String(e);
    }
  };

  window.intelIngest = async function () {
    var mg = document.getElementById("ix-msg");
    var body = {
      title:
        ((document.getElementById("ix-t") && document.getElementById("ix-t").value) || "").trim() ||
        "Untitled",
      text: (document.getElementById("ix-text") && document.getElementById("ix-text").value) || "",
      category: (document.getElementById("ix-cat") && document.getElementById("ix-cat").value) || "GENERAL",
      division: (document.getElementById("ix-div") && document.getElementById("ix-div").value) || "GODS",
      tags: (document.getElementById("ix-tags") && document.getElementById("ix-tags").value) || "",
      source: "inline-admin",
    };
    if (!body.text.trim()) {
      if (mg) mg.textContent = "Paste text first.";
      return;
    }
    if (mg) mg.textContent = "saving…";
    try {
      await api("/intel/ingest-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (mg) mg.textContent = "saved";
      nav("intelligence");
    } catch (e) {
      if (mg) mg.textContent = e.message || String(e);
    }
  };

  window.intelUpload = async function (inp) {
    var mg = document.getElementById("ix-msg");
    if (!inp || !inp.files || !inp.files[0]) return;
    if (mg) mg.textContent = "uploading…";
    try {
      var fd = new FormData();
      fd.append("file", inp.files[0]);
      fd.append(
        "title",
        (document.getElementById("ix-t") && document.getElementById("ix-t").value) || inp.files[0].name
      );
      fd.append(
        "category",
        (document.getElementById("ix-cat") && document.getElementById("ix-cat").value) || "GENERAL"
      );
      fd.append(
        "division",
        (document.getElementById("ix-div") && document.getElementById("ix-div").value) || "GODS"
      );
      fd.append("tags", (document.getElementById("ix-tags") && document.getElementById("ix-tags").value) || "");
      var h = {};
      if (typeof token === "function" && token()) h["Authorization"] = "Bearer " + token();
      var r = await fetch(apiBase() + "/intel/ingest", { method: "POST", headers: h, body: fd });
      if (!r.ok) throw new Error(await r.text());
      if (mg) mg.textContent = "uploaded";
      nav("intelligence");
    } catch (e) {
      if (mg) mg.textContent = e.message || String(e);
    }
  };

  window.intelDelete = async function (id) {
    if (!confirm("Remove document #" + id + " from GODS archive?")) return;
    try {
      await api("/intel/docs/" + id, { method: "DELETE" });
      nav("intelligence");
    } catch (e) {
      alert(e.message || String(e));
    }
  };

  window.vIntelligence = async function (m) {
    await safe(m, async function () {
      var st = {},
        docs = [],
        gaps = null,
        errMsg = "";
      try {
        st = await api("/intel/state");
      } catch (e) {
        errMsg = String(e.message || e);
      }
      try {
        if (!errMsg) docs = asArray(await api("/intel/docs"));
      } catch (e) {
        if (!errMsg) errMsg = String(e.message || e);
      }
      try {
        gaps = await api("/intel/gaps");
      } catch (e) {}
      var stageName = st.stage_name || (st.stage != null ? "Stage " + st.stage : "—");
      var pillar = st.pillar || "Pillar VIII · Human Primacy";
      var gapsPanel = "";
      if (gaps && gaps.categories) {
        gapsPanel =
          '<div class="panel"><h3>Knowledge-gap coverage · ' +
          (gaps.maturity_pct != null ? gaps.maturity_pct + "%" : "—") +
          " covered (" +
          (gaps.covered || 0) +
          "/" +
          (gaps.total || 0) +
          ")</h3>" +
          tableFrom(gaps.categories, [
            {
              h: "Category",
              r: function (x) {
                return (
                  "<b>" +
                  esc(x.category) +
                  '</b> <span class="muted small">' +
                  esc(x.label || "") +
                  "</span>"
                );
              },
            },
            {
              h: "Docs",
              r: function (x) {
                return esc(x.docs);
              },
            },
            {
              h: "Status",
              r: function (x) {
                return (
                  '<span class="tag2 ' +
                  (x.status === "COVERED" ? "t-ok" : x.status === "THIN" ? "t-warn" : "t-bad") +
                  '">' +
                  esc(x.status) +
                  "</span>"
                );
              },
            },
          ]) +
          "</div>";
      }
      var guard = (st.guardrails || [])
        .slice(0, 3)
        .map(function (g) {
          return '<li class="small muted">' + esc(g) + "</li>";
        })
        .join("");
      m.innerHTML =
        '<div class="pgh"><h2>G.O.D.S Intelligence</h2><span class="desc">INTERNAL archive · staff only · retrieval-grounded · not client-exposed · Neon text extracts</span></div>' +
        (errMsg
          ? '<div class="panel" style="border-color:var(--bad)"><b>Load error</b><div class="small">' +
            esc(errMsg) +
            "</div></div>"
          : "") +
        '<div class="grid kpis">' +
        '<div class="kpi"><div class="k">Documents</div><div class="v cyan">' +
        (st.corpus_docs != null ? st.corpus_docs : docs.length) +
        "</div></div>" +
        '<div class="kpi"><div class="k">Corpus chars</div><div class="v">' +
        (st.corpus_chars != null ? Number(st.corpus_chars).toLocaleString() : "—") +
        "</div></div>" +
        '<div class="kpi"><div class="k">Stage</div><div class="v amber" style="font-size:15px">' +
        esc(stageName) +
        "</div></div>" +
        '<div class="kpi"><div class="k">Client exposed</div><div class="v" style="font-size:15px">' +
        (st.client_exposed ? "YES" : "NO") +
        "</div></div></div>" +
        '<div class="panel"><h3>Archive posture</h3><div class="small muted">' +
        esc(pillar) +
        "</div>" +
        (guard ? '<ul style="margin:8px 0 0 18px">' + guard + "</ul>" : "") +
        '<div class="muted small" style="margin-top:8px">Client Company Knowledge is a separate tenant-private table. Internal paste does not appear on client SaaS.</div></div>' +
        gapsPanel +
        '<div class="panel"><h3>Ingest text · GODS archive</h3>' +
        '<div class="row" style="gap:8px;flex-wrap:wrap">' +
        '<div class="f" style="min-width:160px"><label class="small muted">Title</label><input id="ix-t" placeholder="Document title"></div>' +
        '<div class="f" style="min-width:120px"><label class="small muted">Category</label><select id="ix-cat"><option>GENERAL</option><option>GBS</option><option>CANON</option><option>POLICY</option><option>SOP</option><option>CONSTITUTION</option><option>EIF</option></select></div>' +
        '<div class="f" style="min-width:120px"><label class="small muted">Division</label><select id="ix-div"><option>GODS</option><option>SETHS</option><option>MADIBA</option><option>TS</option><option>UDOC</option><option>GBS</option></select></div>' +
        '<div class="f" style="min-width:120px"><label class="small muted">Tags</label><input id="ix-tags" placeholder="optional tags"></div></div>' +
        '<label class="small muted">Text (extract only — not full Drive portfolio)</label>' +
        '<textarea id="ix-text" rows="5" style="width:100%;background:#091022;border:1px solid var(--bd);color:var(--txt);border-radius:8px;padding:10px;font:inherit;margin-top:4px" placeholder="Paste short institutional extract…"></textarea>' +
        '<div style="margin-top:8px"><button class="btn cyan" onclick="intelIngest()" ' +
        (errMsg ? "disabled" : "") +
        '>Add to GODS archive</button> <label class="btn" style="display:inline-block;cursor:pointer">Upload file<input type="file" id="ix-file" style="display:none" onchange="intelUpload(this)"></label> <span id="ix-msg" class="muted small"></span></div></div>' +
        '<div class="panel"><h3>Ask the knowledge base</h3>' +
        '<div class="row"><div class="f"><input id="iq" placeholder="Ask grounded in the GODS archive…"></div>' +
        '<button class="btn cyan" onclick="askIntel()">Ask</button></div>' +
        '<div id="ians" class="small" style="margin-top:10px;white-space:pre-wrap;color:var(--txt2)"></div></div>' +
        '<div class="panel"><h3>Archive documents · ' +
        docs.length +
        "</h3>" +
        tableFrom(docs.slice(0, 80), [
          {
            h: "Document",
            r: function (x) {
              return (
                "<b>" +
                esc(x.title || "—") +
                '</b><div class="muted small mono">' +
                esc(x.source || "") +
                "</div>"
              );
            },
          },
          {
            h: "Category",
            r: function (x) {
              return esc(x.category || "—");
            },
          },
          {
            h: "Division",
            r: function (x) {
              return esc(x.division || "—");
            },
          },
          {
            h: "Chars",
            r: function (x) {
              return esc(x.char_len != null ? x.char_len : "—");
            },
          },
          {
            h: "",
            r: function (x) {
              return (
                '<button class="btn sm" onclick="intelDelete(' + Number(x.id) + ')">Remove</button>'
              );
            },
          },
        ]) +
        "</div>" +
        (typeof honesty === "function" ? honesty() : "");
    });
  };
})();
