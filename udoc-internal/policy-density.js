/* UDOC Admin — Policy-to-Code + EVA runtime matrix density */
(function () {
  function esc(s) {
    var d = document.createElement("div");
    d.textContent = String(s == null ? "" : s);
    return d.innerHTML;
  }

  window.showPolicyPanel = async function () {
    var main = document.getElementById("main");
    if (!main) return;
    main.innerHTML =
      '<div class="pgh"><h2>Policy-to-Code · Runtime</h2><span class="desc">Upload → compile → activate → EVA matrix</span></div>' +
      '<div class="panel muted">Loading active rules…</div>';
    try {
      var active = await api("/policy/active");
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
      main.innerHTML =
        '<div class="pgh"><h2>Policy-to-Code · Runtime</h2><span class="desc">Active packs drive EVA apply() at decision time</span></div>' +
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
        "</div>" +
        '<div id="pol-matrix-out" style="margin-top:12px"></div></div>' +
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
        '<div class="panel"><h3>Pipeline</h3><div class="small muted">Upload legislation → extract_rules → review → activate → ' +
        "GET /policy/active · POST /policy/runtime-matrix · POST /decisions/batch (persist)</div></div>";
    } catch (e) {
      main.innerHTML =
        '<div class="pgh"><h2>Policy-to-Code</h2></div><div class="panel t-bad">' +
        esc(e.message || e) +
        "</div>";
    }
  };

  window.runPolicyMatrix = async function () {
    var out = document.getElementById("pol-matrix-out");
    if (out) out.innerHTML = '<div class="muted small">POST /policy/runtime-matrix …</div>';
    try {
      var m = await api("/policy/runtime-matrix", {
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
      await api("/policy/hot-reload", {
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
