/* UDOC Admin — Internal package density
 * Staff-only identity · nav relabel · Command Centre · EVA batch · HITL · infra links
 * Intelligence density loaded from /intel-density.js (SW inject)
 * EIF density loaded from /eif-density.js (SW inject)
 */
(function () {
  window.esc = function (s) {
    var d = document.createElement("div");
    d.textContent = String(s == null ? "" : s);
    return d.innerHTML;
  };

  function stampInternalPackage() {
    try {
      var bar = document.getElementById("v7-staff-ribbon");
      if (bar) return;
      bar = document.createElement("div");
      bar.id = "v7-staff-ribbon";
      bar.style.cssText =
        "background:#1a1305;color:#E8C97A;font-size:11px;padding:6px 12px;border-bottom:1px solid #3d2e0a;letter-spacing:.04em";
      bar.textContent =
        "UDOC INTERNAL PACKAGE · STAFF ONLY · NOT CLIENT SAAS · KILL-SWITCH · HITL · JOBS · CORE API";
      var app = document.getElementById("app") || document.body;
      app.insertBefore(bar, app.firstChild);
    } catch (e) {}
  }

  function relabelNav() {
    var map = {
      overview: "Command Centre",
      decisions: "EVA Command",
      oversight: "HITL Queue",
      incidents: "Incident Command",
      intelligence: "Intelligence",
    };
    document.querySelectorAll("#nav .navitem").forEach(function (n) {
      var v = n.getAttribute("data-view");
      if (map[v] && n.childNodes.length) {
        var t = n.querySelector(".txt") || n;
        /* keep icon; set text node if present */
      }
    });
  }

  function injectInfraLinks() {
    var nav = document.getElementById("nav");
    if (!nav || document.getElementById("v7-infra")) return;
    var div = document.createElement("div");
    div.id = "v7-infra";
    var base =
      typeof apiBase === "function"
        ? apiBase()
        : "https://gods-platform-core.onrender.com";
    div.innerHTML =
      '<div class="sech">INFRA · CORE</div>' +
      '<div class="navitem" data-view="_sentinel"><span class="ico">◎</span> Sentinel runtime</div>' +
      '<div class="navitem" data-view="_coreadmin"><span class="ico">⚖</span> Core /admin constitutional</div>' +
      '<div class="navitem" data-view="_apihealth"><span class="ico">⚡</span> API Health</div>' +
      '<div class="navitem" data-view="_jobs"><span class="ico">⏱</span> Scheduled Jobs</div>' +
      '<div class="navitem" data-view="_portals"><span class="ico">▤</span> 24 Portals dual-path</div>' +
      '<div class="navitem" data-view="_citizen"><span class="ico">✋</span> Citizen (public view)</div>' +
      '<div class="navitem" data-view="_client"><span class="ico">◇</span> Client SaaS host</div>';
    nav.appendChild(div);
    div.querySelectorAll(".navitem").forEach(function (n) {
      n.addEventListener("click", function () {
        var v = n.getAttribute("data-view");
        if (v === "_sentinel") window.open(base + "/Sentinel", "_blank");
        else if (v === "_coreadmin") window.open(base + "/admin", "_blank");
        else if (v === "_apihealth") window.location.href = "/api-health.html";
        else if (v === "_jobs") window.location.href = "/jobs.html";
        else if (v === "_portals") window.open(base + "/portals", "_blank");
        else if (v === "_citizen")
          window.open(
            "https://gods-udoc-client.onrender.com/citizen.html",
            "_blank"
          );
        else if (v === "_client")
          window.open("https://gods-udoc-client.onrender.com/", "_blank");
      });
    });
  }

  function wrapOverview() {
    if (typeof vOverview !== "function" || vOverview._v7) return;
    var _orig = vOverview;
    window.vOverview = async function (m) {
      await _orig(m);
      try {
        var ready = null;
        try {
          ready = await api("/udoc/demo/ready");
        } catch (e) {}
        var bar = document.createElement("div");
        bar.className = "panel";
        bar.style.borderLeft = "3px solid #C9A84C";
        bar.innerHTML =
          "<h3>Command Centre · Internal boot posture</h3><div class=\"small\">" +
          (ready && ready.ready
            ? '<span class="t-ok">DEMO READY</span>'
            : '<span class="t-bad">SEED PENDING</span>') +
          " · model-001 · policy pack · fail-closed</div>";
        var main = document.getElementById("main");
        if (main) {
          var first = main.querySelector(".panel");
          if (first) main.insertBefore(bar, first);
          else main.appendChild(bar);
        }
      } catch (e) {}
      var h2 = document.querySelector("#main .pgh h2");
      if (h2) h2.textContent = "Command Centre";
    };
    window.vOverview._v7 = true;
  }

  function wrapDecisions() {
    if (typeof vDecisions !== "function" || vDecisions._v7) return;
    var _orig = vDecisions;
    window.vDecisions = async function (m) {
      await _orig(m);
      try {
        var panel = document.createElement("div");
        panel.className = "panel";
        panel.style.borderLeft = "3px solid #00C2D4";
        panel.innerHTML =
          "<h3>EVA scenario chips + Full matrix (Internal density)</h3>" +
          '<div class="row" style="gap:8px;flex-wrap:wrap">' +
          '<button class="btn cyan sm" type="button" onclick="v7Eva(\'fair\')">Fair</button>' +
          '<button class="btn sm" type="button" onclick="v7Eva(\'biased\')">Biased → BLOCK</button>' +
          '<button class="btn sm" type="button" onclick="v7Eva(\'high\')">High-risk</button>' +
          '<button class="btn sm" type="button" onclick="v7Eva(\'sov\')">Sovereignty</button>' +
          '<button class="btn cyan sm" type="button" onclick="v7EvaBatch()">Run Full EVA batch</button>' +
          '</div><div id="v7-eva-kpis" style="margin-top:10px"></div>' +
          '<div id="v7-eva-out" class="small muted" style="margin-top:10px"></div>' +
          '<pre id="v7-eva-term" class="mono" style="margin-top:8px;font-size:11px;white-space:pre-wrap;background:#050a12;padding:10px;border-radius:8px;display:none"></pre>';
        var main = document.getElementById("main");
        if (main) {
          var first = main.querySelector(".panel");
          if (first) main.insertBefore(panel, first);
          else main.appendChild(panel);
        }
      } catch (e) {}
      var h2 = document.querySelector("#main .pgh h2");
      if (h2) h2.textContent = "EVA Command";
    };
    window.vDecisions._v7 = true;
  }

  function scenarioBody(kind, mid) {
    var body = {
      model_id: mid || "model-001",
      raw_confidence: 0.92,
      compliance: 1.0,
    };
    if (kind === "fair") {
      body.raw_confidence = 0.94;
      body.compliance = 1.0;
    }
    if (kind === "biased") {
      body.raw_confidence = 0.88;
      body.compliance = 0.95;
      body.priv_favorable = 900;
      body.priv_total = 1000;
      body.unpriv_favorable = 120;
      body.unpriv_total = 1000;
    }
    if (kind === "high") {
      body.raw_confidence = 0.7;
      body.compliance = 0.85;
      body.risk_tier = "HIGH";
    }
    if (kind === "sov") {
      body.bgp = 0.4;
      body.traceroute = 0.5;
      body.dnssec = 0.6;
      body.storage = 0.7;
    }
    return body;
  }

  window.v7Eva = async function (kind) {
    var out = document.getElementById("v7-eva-out");
    var term = document.getElementById("v7-eva-term");
    if (out) out.textContent = "Evaluating " + kind + "…";
    if (term) {
      term.style.display = "block";
      term.textContent = "POST /decisions …";
    }
    var midEl = document.getElementById("ev-mid");
    var mid = midEl ? midEl.value.trim() : "model-001";
    var body = scenarioBody(kind, mid);
    try {
      var d = await api("/decisions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      var decision = d.decision || d.verdict || "—";
      var reasons = Array.isArray(d.block_reasons)
        ? d.block_reasons.join(" · ")
        : d.block_reasons || "";
      if (out) {
        out.innerHTML =
          "<b>" +
          esc(kind) +
          '</b> → <span class="tag2">' +
          esc(decision) +
          "</span> · EVA " +
          esc(d.composite_eva != null ? d.composite_eva : "—") +
          " · policy " +
          (d.policy_enforced ? "ENFORCED" : "off") +
          (reasons ? " · " + esc(reasons) : "");
      }
      if (term) {
        var lines = ["SCENARIO: " + kind + " · " + body.model_id];
        if (d.dimensions) {
          ["Validity", "Confidence", "Risk", "Compliance", "Stability", "Impact"].forEach(
            function (k) {
              if (d.dimensions[k] != null)
                lines.push("  " + k + " = " + Number(d.dimensions[k]).toFixed(3));
            }
          );
        }
        lines.push("  Composite = " + (d.composite_eva != null ? d.composite_eva : "—"));
        lines.push("  Policy = " + (d.policy_enforced ? "ENFORCED" : "off"));
        lines.push("  → " + decision);
        if (reasons) lines.push("  · " + reasons);
        if (d.certificate_id) lines.push("  cert " + d.certificate_id);
        term.textContent = lines.join("\n");
      }
    } catch (e) {
      if (out) out.innerHTML = '<span class="t-bad">' + esc(e.message) + "</span>";
      if (term) term.textContent = "FAIL " + e.message;
    }
  };

  window.v7EvaBatch = async function () {
    var out = document.getElementById("v7-eva-out");
    var term = document.getElementById("v7-eva-term");
    var kpis = document.getElementById("v7-eva-kpis");
    if (out) out.textContent = "POST /decisions/batch …";
    if (term) {
      term.style.display = "block";
      term.textContent = "batch…";
    }
    var midEl = document.getElementById("ev-mid");
    var mid = midEl ? midEl.value.trim() : "model-001";
    var results = [];
    try {
      var pack = await api("/decisions/batch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model_id: mid,
          options: ["fair", "biased", "high", "sov"],
        }),
      });
      (pack.results || []).forEach(function (r) {
        results.push({
          kind: r.option,
          ok: !!r.ok,
          decision: r.decision || r.error,
          eva: r.composite_eva,
          policy: r.policy_enforced,
          reasons: r.block_reasons || [],
        });
      });
      var g = pack.gate || {};
      if (kpis)
        kpis.innerHTML =
          '<div class="small">Gate fair≠BLOCK: <b>' +
          (g.fair_neq_block ? "PASS" : "FAIL") +
          "</b> · biased=BLOCK: <b>" +
          (g.biased_eq_block ? "PASS" : "FAIL") +
          "</b></div>";
    } catch (e) {
      if (out) out.innerHTML = '<span class="t-bad">' + esc(e.message) + "</span>";
    }
    var counts = { APPROVE: 0, BLOCK: 0, ESCALATE: 0, OTHER: 0 };
    results.forEach(function (r) {
      var d = String(r.decision || "").toUpperCase();
      if (d === "APPROVE") counts.APPROVE++;
      else if (d === "BLOCK") counts.BLOCK++;
      else if (d === "ESCALATE") counts.ESCALATE++;
      else counts.OTHER++;
    });
    if (out)
      out.innerHTML =
        "Batch <b>" +
        results.filter(function (r) {
          return r.ok;
        }).length +
        "/" +
        results.length +
        "</b> · APPROVE <b>" +
        counts.APPROVE +
        "</b> · BLOCK <b>" +
        counts.BLOCK +
        "</b> · ESCALATE <b>" +
        counts.ESCALATE +
        "</b>";
    var lines = ["FULL EVA BATCH · " + (mid || "model-001") + " · /decisions/batch"];
    results.forEach(function (r) {
      lines.push(
        "[" +
          r.kind +
          "] → " +
          (r.decision || "?") +
          (r.eva != null ? " · EVA " + r.eva : "") +
          (r.policy ? " · policy ENFORCED" : "")
      );
      (r.reasons || []).slice(0, 2).forEach(function (x) {
        lines.push("  · " + x);
      });
    });
    if (term) term.textContent = lines.join("\n");
  };

  function wrapOversight() {
    if (typeof vOversight !== "function" || vOversight._v7) return;
    var _orig = vOversight;
    window.vOversight = async function (m) {
      await _orig(m);
      var h2 = document.querySelector("#main .pgh h2");
      if (h2) h2.textContent = "HITL Queue";
      try {
        var base =
          typeof apiBase === "function"
            ? apiBase()
            : "https://gods-platform-core.onrender.com";
        var bar = document.createElement("div");
        bar.className = "panel";
        bar.style.borderLeft = "3px solid #10B981";
        bar.innerHTML =
          "<h3>Portal dual-path</h3><div class=\"small muted\">HITL / Regulator controls open or resolve OversightCase on Neon.</div>" +
          '<div style="margin-top:8px"><button class="btn cyan sm" type="button" onclick="window.open(\'' +
          base +
          "/portals','_blank')">Open 24 Portals · HITL workspace</button></div>";
        var main = document.getElementById("main");
        if (main) {
          var first = main.querySelector(".panel");
          if (first) main.insertBefore(bar, first);
          else main.appendChild(bar);
        }
      } catch (e) {}
    };
    window.vOversight._v7 = true;
  }

  function run() {
    stampInternalPackage();
    relabelNav();
    injectInfraLinks();
    wrapOverview();
    wrapDecisions();
    wrapOversight();
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", run);
  else run();

  var _enter = window.enterApp;
  if (typeof _enter === "function") {
    window.enterApp = async function () {
      await _enter.apply(this, arguments);
      run();
    };
  }
})();
