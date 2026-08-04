/* UDOC Admin — Policy-to-Code uploader + runtime matrix */
(function () {
  function esc(s) {
    var d = document.createElement("div");
    d.textContent = String(s == null ? "" : s);
    return d.innerHTML;
  }
  function token() {
    try {
      return localStorage.getItem("udoc_tok") || localStorage.getItem("token") || "";
    } catch (e) {
      return "";
    }
  }
  function apiBase() {
    if (typeof window.apiBase === "function") return window.apiBase();
    return localStorage.getItem("udoc_api") || "https://gods-platform-core.onrender.com";
  }
  async function polApi(path, opts) {
    if (typeof window.api === "function") return window.api(path, opts || {});
    var h = Object.assign({}, (opts && opts.headers) || {});
    var t = token();
    if (t) h["Authorization"] = "Bearer " + t;
    var r = await fetch(apiBase() + path, Object.assign({}, opts || {}, { headers: h }));
    var ct = r.headers.get("content-type") || "";
    var body = ct.includes("json") ? await r.json().catch(function () { return null; }) : await r.text();
    if (!r.ok) throw new Error((body && body.detail) || (typeof body === "string" ? body : "HTTP " + r.status));
    return body;
  }

  window.showPolicyPanel = async function () {
    var main = document.getElementById("main");
    if (!main) return;
    main.innerHTML =
      '<div class="pgh"><h2>Policy-to-Code · Runtime</h2><span class="desc">Upload → compile → activate → EVA matrix</span></div>' +
      '<div class="panel muted">Loading…</div>';
    try {
      var active = await polApi("/policy/active");
      var allPacks = await polApi("/policy/packs").catch(function () { return []; });
      if (!Array.isArray(allPacks)) allPacks = allPacks.items || allPacks.packs || [];
      var packs = active.active_packs || [];
      var rules = active.rules || [];
      var kinds = active.by_kind || {};
      var kindRows = Object.keys(kinds)
        .map(function (k) {
          return "<tr><td class=\"mono\">" + esc(k) + "</td><td><b>" + esc(kinds[k]) + "</b></td></tr>";
        })
        .join("");
      var ruleRows = rules
        .map(function (r) {
          return (
            "<tr><td class=\"mono\">" +
            esc(r.code) +
            "</td><td>" +
            esc(r.kind) +
            "</td><td>" +
            esc(r.severity) +
            "</td><td class=\"small\">" +
            esc(r.description) +
            "</td></tr>"
          );
        })
        .join("");
      var packRows = packs
        .map(function (p) {
          return (
            "<tr><td><b>" +
            esc(p.name) +
            "</b></td><td class=\"mono\">" +
            esc(p.status) +
            "</td><td>" +
            esc(p.rule_count) +
            "</td><td class=\"small muted\">" +
            esc(p.summary || "") +
            "</td></tr>"
          );
        })
        .join("");
      var draftRows = allPacks
        .filter(function (p) {
          return String(p.status || "").toUpperCase() !== "ACTIVE";
        })
        .map(function (p) {
          var st = String(p.status || "").toUpperCase();
          var act =
            st === "DRAFT" || st === "PROPOSED"
              ? '<button class="btn sm cyan" type="button" onclick="activatePack(' +
                esc(p.id) +
                ')">Activate</button> '
              : "";
          act +=
            '<button class="btn sm" type="button" onclick="viewPack(' +
            esc(p.id) +
            ')">View rules</button>';
          return (
            "<tr><td><b>" +
            esc(p.name) +
            '</b><div class="small muted">' +
            esc(p.source_filename || "") +
            "</div></td><td class=\"mono\">" +
            esc(p.status) +
            "</td><td>" +
            esc(p.rule_count) +
            '</td><td class="small">' +
            act +
            "</td></tr>"
          );
        })
        .join("");

      main.innerHTML =
        '<div class="pgh"><h2>Policy-to-Code · Runtime</h2><span class="desc">Uploader + active enforcement + EVA matrix</span></div>' +
        '<div class="panel" style="border-left:3px solid #C9A84C">' +
        "<h3>Upload legislation / policy</h3>" +
        '<div class="small muted">PDF · DOCX · TXT · max 5MB · compiles candidate rules (human review before activate)</div>' +
        '<div class="row" style="margin-top:10px;flex-wrap:wrap;gap:10px">' +
        '<div class="f" style="min-width:160px"><label>Pack name</label>' +
        '<input id="pol-name" value="Client policy pack" placeholder="e.g. POPIA fairness pack"/></div>' +
        '<div class="f" style="min-width:100px"><label>Jurisdiction</label>' +
        '<input id="pol-jur" value="ZA"/></div>' +
        '<div class="f" style="min-width:100px"><label>Sector</label>' +
        '<input id="pol-sec" value="GENERAL"/></div>' +
        "</div>" +
        '<div style="margin-top:10px"><label>File</label>' +
        '<input id="pol-file" type="file" accept=".txt,.pdf,.docx,.doc,text/plain,application/pdf"/></div>' +
        '<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">' +
        '<button class="btn gold" type="button" id="pol-upload-btn" onclick="uploadPolicyFile()">Compile rules from file</button>' +
        "</div>" +
        '<div id="pol-upload-out" style="margin-top:12px"></div></div>' +
        '<div class="panel" style="border-left:3px solid #00C2D4"><h3>Active posture</h3>' +
        '<div class="small">Enforced rules <b>' +
        esc(active.enforced_rules) +
        "</b> · epoch " +
        esc((active.hot_reload && active.hot_reload.epoch) || 0) +
        '</div><div class="small muted" style="margin-top:6px">' +
        esc(active.note || "") +
        "</div>" +
        '<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">' +
        '<button class="btn cyan" type="button" onclick="runPolicyMatrix()">Run EVA × policy matrix</button>' +
        '<button class="btn sm" type="button" onclick="policyHotReload()">Hot-reload rules</button>' +
        '<button class="btn sm" type="button" onclick="showPolicyPanel()">Refresh</button>' +
        "</div>" +
        '<div id="pol-matrix-out" style="margin-top:12px"></div></div>' +
        '<div class="panel"><h3>Draft / other packs</h3>' +
        "<table><thead><tr><th>Name</th><th>Status</th><th>Rules</th><th>Actions</th></tr></thead><tbody>" +
        (draftRows || "<tr><td colspan=4 class=muted>No draft packs — upload above</td></tr>") +
        "</tbody></table></div>" +
        '<div class="panel"><h3>Active packs · ' +
        packs.length +
        "</h3><table><thead><tr><th>Name</th><th>Status</th><th>Rules</th><th>Summary</th></tr></thead><tbody>" +
        (packRows || "<tr><td colspan=4 class=muted>None</td></tr>") +
        "</tbody></table></div>" +
        '<div class="panel"><h3>By kind</h3><table><thead><tr><th>Kind</th><th>Count</th></tr></thead><tbody>' +
        (kindRows || "<tr><td colspan=2 class=muted>—</td></tr>") +
        "</tbody></table></div>" +
        '<div class="panel"><h3>Enforced rules · ' +
        rules.length +
        "</h3><table><thead><tr><th>Code</th><th>Kind</th><th>Severity</th><th>Description</th></tr></thead><tbody>" +
        (ruleRows || "<tr><td colspan=4 class=muted>—</td></tr>") +
        "</tbody></table></div>" +
        '<div class="panel"><h3>Pipeline</h3><div class="small muted">' +
        "Upload → extract_rules → draft → Activate → GET /policy/active · POST /policy/runtime-matrix · POST /decisions/batch" +
        "</div></div>";
    } catch (e) {
      main.innerHTML =
        '<div class="pgh"><h2>Policy-to-Code</h2></div><div class="panel t-bad">' +
        esc(e.message || e) +
        "</div>";
    }
  };

  window.uploadPolicyFile = async function () {
    var out = document.getElementById("pol-upload-out");
    var btn = document.getElementById("pol-upload-btn");
    var fileEl = document.getElementById("pol-file");
    var name = ((document.getElementById("pol-name") || {}).value || "").trim() || "Policy pack";
    var jur = ((document.getElementById("pol-jur") || {}).value || "ZA").trim();
    var sec = ((document.getElementById("pol-sec") || {}).value || "GENERAL").trim();
    if (!fileEl || !fileEl.files || !fileEl.files[0]) {
      if (out) out.innerHTML = '<span class="t-bad">Choose a file first (.txt / .pdf / .docx)</span>';
      return;
    }
    var file = fileEl.files[0];
    if (file.size > 5 * 1024 * 1024) {
      if (out) out.innerHTML = '<span class="t-bad">File over 5MB (free-tier cap)</span>';
      return;
    }
    if (btn) {
      btn.disabled = true;
      btn.textContent = "Compiling…";
    }
    if (out) out.innerHTML = '<div class="muted small">POST /policy/upload — extracting &amp; compiling rules…</div>';
    try {
      var fd = new FormData();
      fd.append("name", name);
      fd.append("jurisdiction", jur);
      fd.append("sector", sec);
      fd.append("file", file, file.name);
      var t = token();
      var r = await fetch(apiBase() + "/policy/upload", {
        method: "POST",
        headers: t ? { Authorization: "Bearer " + t } : {},
        body: fd,
      });
      var body = await r.json().catch(function () {
        return {};
      });
      if (!r.ok) throw new Error(body.detail || body.message || "Upload failed " + r.status);
      var pack = body.pack || {};
      var compiled = body.rules || [];
      var rows = compiled
        .slice(0, 40)
        .map(function (ru) {
          return (
            "<tr><td class=\"mono\">" +
            esc(ru.code) +
            "</td><td>" +
            esc(ru.kind) +
            "</td><td>" +
            esc(ru.severity) +
            '</td><td class="small">' +
            esc((ru.description || "").slice(0, 120)) +
            '</td><td class="small muted">' +
            esc((ru.source_excerpt || "").slice(0, 80)) +
            "</td></tr>"
          );
        })
        .join("");
      if (out)
        out.innerHTML =
          '<div class="t-ok small"><b>Draft pack #' +
          esc(pack.id) +
          "</b> · " +
          esc(pack.rule_count) +
          " candidate rules · status " +
          esc(pack.status) +
          "</div>" +
          '<div class="small muted" style="margin-top:4px">' +
          esc(pack.summary || body.note || "") +
          "</div>" +
          (rows
            ? '<table style="margin-top:10px"><thead><tr><th>Code</th><th>Kind</th><th>Sev</th><th>Description</th><th>Source</th></tr></thead><tbody>' +
              rows +
              "</tbody></table>"
            : '<div class="muted small" style="margin-top:8px">No rule patterns matched — try text with fairness / human oversight / sovereignty language.</div>') +
          '<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">' +
          '<button class="btn cyan" type="button" onclick="activatePack(' +
          esc(pack.id) +
          ')">Activate pack #' +
          esc(pack.id) +
          "</button>" +
          '<button class="btn sm" type="button" onclick="showPolicyPanel()">Refresh list</button></div>';
    } catch (e) {
      if (out) out.innerHTML = '<span class="t-bad">' + esc(e.message || e) + "</span>";
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.textContent = "Compile rules from file";
      }
    }
  };

  window.activatePack = async function (id) {
    if (!id) return;
    if (!confirm("Activate pack #" + id + "?\nRules will enforce on next EVA decision (hot-reload).")) return;
    try {
      var d = await polApi("/policy/packs/" + id + "/activate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: "{}",
      });
      alert("Activated · active_rules=" + (d.active_rules != null ? d.active_rules : "?") + "\n" + (d.note || ""));
      showPolicyPanel();
    } catch (e) {
      alert("Activate failed: " + (e.message || e) + "\n(COB packs may need submit → approve)");
    }
  };

  window.viewPack = async function (id) {
    try {
      var d = await polApi("/policy/packs/" + id);
      var rules = d.rules || [];
      var lines = rules
        .map(function (r) {
          return r.code + " · " + r.kind + " · " + r.severity + " — " + (r.description || "");
        })
        .join("\n");
      alert("Pack #" + id + " · " + rules.length + " rules\n\n" + (lines || "(none)").slice(0, 1500));
    } catch (e) {
      alert(e.message || e);
    }
  };

  window.runPolicyMatrix = async function () {
    var out = document.getElementById("pol-matrix-out");
    if (out) out.innerHTML = '<div class="muted small">POST /policy/runtime-matrix …</div>';
    try {
      var m = await polApi("/policy/runtime-matrix", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_id: "model-001" }),
      });
      var g = m.gate || {};
      var rows = (m.results || [])
        .map(function (r) {
          return (
            "<tr><td>" +
            esc(r.option) +
            "</td><td><b>" +
            esc(r.decision) +
            "</b></td><td>" +
            esc(r.fired_count) +
            '</td><td class="small">' +
            esc((r.block_reasons || []).slice(0, 2).join(" · ")) +
            "</td></tr>"
          );
        })
        .join("");
      if (out)
        out.innerHTML =
          '<div class="small">Gate fair≠BLOCK <b>' +
          (g.fair_neq_block ? "PASS" : "FAIL") +
          "</b> · biased=BLOCK <b>" +
          (g.biased_eq_block ? "PASS" : "FAIL") +
          "</b> · rules " +
          esc(m.active_rule_count) +
          '</div><table style="margin-top:8px"><thead><tr><th>Scenario</th><th>Decision</th><th>Fired</th><th>Reasons</th></tr></thead><tbody>' +
          rows +
          "</tbody></table>" +
          '<div class="small muted" style="margin-top:8px">' +
          esc(m.note || "") +
          "</div>";
    } catch (e) {
      if (out) out.innerHTML = '<span class="t-bad">' + esc(e.message || e) + "</span>";
    }
  };

  window.policyHotReload = async function () {
    try {
      await polApi("/policy/hot-reload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: "{}",
      });
      showPolicyPanel();
    } catch (e) {
      alert(e.message || e);
    }
  };

  function injectNav() {
    var nav = document.getElementById("nav");
    if (!nav || document.getElementById("v7-policy-nav")) return;
    var div = document.createElement("div");
    div.id = "v7-policy-nav";
    div.innerHTML =
      '<div class="sech">POLICY · CODE</div>' +
      '<div class="navitem" data-view="_policy"><span class="ico">§</span> Policy-to-Code</div>';
    nav.appendChild(div);
    div.querySelectorAll(".navitem").forEach(function (n) {
      n.addEventListener("click", function () {
        document.querySelectorAll("#nav .navitem").forEach(function (x) {
          x.classList.remove("active");
        });
        n.classList.add("active");
        showPolicyPanel();
      });
    });
  }

  function run() {
    injectNav();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
  setTimeout(run, 800);
  setTimeout(run, 2000);
})();
