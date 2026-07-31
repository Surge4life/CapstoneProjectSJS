/* UDOC Admin — Internal package density
 * Staff-only identity · nav relabel · Command Centre · EVA batch · HITL · infra links
 */
(function () {
  "use strict";

  window.esc = function (s) {
    var d = document.createElement("div");
    d.textContent = String(s == null ? "" : s);
    return d.innerHTML;
  };

  function stampInternalPackage() {
    document.documentElement.setAttribute("data-udoc-package", "internal");
    if (document.title && !/Internal/i.test(document.title)) {
      document.title = "UDOC Internal · GODS Staff";
    }
    var tag = document.getElementById("org-tag");
    if (tag) tag.textContent = "INTERNAL · STAFF";
    if (document.getElementById("udoc-internal-ribbon")) return;
    var rib = document.createElement("div");
    rib.id = "udoc-internal-ribbon";
    rib.setAttribute(
      "style",
      "background:#060E1C;color:#C9A84C;font:10px/1.4 'IBM Plex Mono',Consolas,monospace;" +
        "letter-spacing:.08em;text-align:center;padding:6px 10px;border-bottom:1px solid #1A2D4A;"
    );
    rib.textContent =
      "UDOC INTERNAL PACKAGE · STAFF ONLY · NOT CLIENT SAAS · KILL-SWITCH · HITL · JOBS · CORE API";
    var body = document.body;
    if (body && body.firstChild) body.insertBefore(rib, body.firstChild);
    else if (body) body.appendChild(rib);
  }

  function relabelNav() {
    var map = {
      overview: "Command Centre",
      systems: "AI Registry",
      control: "Kill-switch",
      decisions: "EVA Command",
      lifecycle: "AI Lifecycle",
      evidence: "Evidence · Replay",
      policy: "Policy Engine",
      oversight: "HITL Queue",
      audit: "Audit Trail",
      governance: "Constitution",
      compliance: "Compliance",
      sovereignty: "Sovereignty",
      incidents: "Incident Command",
      intelligence: "Intelligence",
      tenants: "Clients / Tenants",
      divisions: "Division Ops",
      sectors: "Sectors",
      access: "User Management",
      roles: "Roles & Profiles",
    };
    document.querySelectorAll("#nav .navitem").forEach(function (n) {
      var v = n.dataset.view;
      if (!map[v]) return;
      var ico = n.querySelector(".ico");
      var iconHtml = ico ? ico.outerHTML : '<span class="ico">·</span>';
      n.innerHTML = iconHtml + " " + map[v];
    });
    var sech = document.querySelectorAll("#nav .sech");
    if (sech[0]) sech[0].textContent = "PLATFORM";
    if (sech[1]) sech[1].textContent = "UDOC GOVERNANCE";
    if (sech[2]) sech[2].textContent = "INTELLIGENCE";
    if (sech[3]) sech[3].textContent = "ECOSYSTEM";
    if (sech[4]) sech[4].textContent = "ACCESS";
  }

  function injectInfraLinks() {
    var nav = document.getElementById("nav");
    if (!nav || document.getElementById("v7-infra")) return;
    var div = document.createElement("div");
    div.id = "v7-infra";
    div.innerHTML =
      '<div class="sech">INFRASTRUCTURE · INTERNAL</div>' +
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
        var v = n.dataset.view;
        var base =
          typeof apiBase === "function"
            ? apiBase()
            : "https://gods-platform-core.onrender.com";
        if (v === "_sentinel") window.open(base + "/Sentinel", "_blank");
        else if (v === "_coreadmin") window.open(base + "/admin", "_blank");
        else if (v === "_apihealth") window.location.href = "/api-health.html";
        else if (v === "_jobs") window.location.href = "/jobs.html";
        else if (v === "_portals") window.open(base + "/portals", "_blank");
        else if (v === "_citizen") {
          window.open("https://gods-udoc-client.onrender.com/citizen.html", "_blank");
        } else if (v === "_client") {
          window.open("https://gods-udoc-client.onrender.com/", "_blank");
        }
      });
    });
  }

  function wrapOverview() {
    if (typeof vOverview !== "function" || vOverview._v7) return;
    var _orig = vOverview;
    window.vOverview = async function (m) {
      await _orig(m);
      try {
        var ready = await api("/udoc/demo/ready");
        var sum = {};
        try {
          sum = await api("/udoc/regulator/summary");
        } catch (e2) {}
        var oc = (sum.decisions && sum.decisions.by_outcome) || {};
        var banner = document.createElement("div");
        banner.className = "panel";
        banner.style.borderLeft = "3px solid #C9A84C";
        banner.innerHTML =
          "<h3>Command Centre · Internal boot posture</h3><div class=\"small\">" +
          (ready.ready
            ? '<span class="tag2 t-ok">DEMO READY</span> · active rules ' +
              esc(String(ready.active_rules)) +
              ' · prefer <span class="mono">model-001</span>'
            : '<span class="tag2 t-bad">SEED PENDING</span> · ' +
              esc((ready.missing || []).join("; ") || "check Core")) +
          '</div><div class="small" style="margin-top:10px">' +
          "APPROVE <b>" +
          esc(oc.APPROVE || 0) +
          "</b> · BLOCK <b>" +
          esc(oc.BLOCK || 0) +
          "</b> · ESCALATE <b>" +
          esc(oc.ESCALATE || 0) +
          "</b> · HITL open <b>" +
          esc(sum.oversight && sum.oversight.open != null ? sum.oversight.open : "—") +
          "</b></div>" +
          '<div class="small muted" style="margin-top:8px">Internal package · live Core · Neon ≤500MB · ' +
          '<a href="#" onclick="if(typeof showPage===\'function\')showPage(\'decisions\');return false">EVA Command</a></div>';
        var main = document.getElementById("main");
        if (main) {
          var pgh = main.querySelector(".pgh");
          if (pgh && pgh.nextSibling) main.insertBefore(banner, pgh.nextSibling);
          else main.appendChild(banner);
        }
      } catch (e) {}
      var h2 = document.querySelector("#main .pgh h2");
      if (h2) h2.textContent = "Command Centre";
      var desc = document.querySelector("#main .pgh .desc");
      if (desc)
        desc.textContent =
          "Staff control plane · registry · kill-switch · HITL · fail-closed governance";
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
          "</b> → <span class=\"tag2\">" +
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
          ["Validity", "Confidence", "Risk", "Compliance", "Stability", "Impact"].forEach(function (k) {
            if (d.dimensions[k] != null)
              lines.push("  " + k + " = " + Number(d.dimensions[k]).toFixed(3));
          });
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
    if (out) out.textContent = "Running Full EVA batch…";
    if (term) {
      term.style.display = "block";
      term.textContent = "matrix · fair · biased · high · sov";
    }
    var midEl = document.getElementById("ev-mid");
    var mid = midEl ? midEl.value.trim() : "model-001";
    var kinds = ["fair", "biased", "high", "sov"];
    var results = [];
    for (var i = 0; i < kinds.length; i++) {
      var k = kinds[i];
      try {
        var d = await api("/decisions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(scenarioBody(k, mid)),
        });
        results.push({
          kind: k,
          ok: true,
          decision: d.decision,
          eva: d.composite_eva,
          policy: d.policy_enforced,
          reasons: d.block_reasons || [],
        });
      } catch (e) {
        results.push({ kind: k, ok: false, decision: e.message });
      }
    }
    var counts = { APPROVE: 0, BLOCK: 0, ESCALATE: 0, OTHER: 0 };
    results.forEach(function (r) {
      var d = String(r.decision || "").toUpperCase();
      if (d === "APPROVE") counts.APPROVE++;
      else if (d === "BLOCK") counts.BLOCK++;
      else if (d === "ESCALATE") counts.ESCALATE++;
      else if (r.ok) counts.OTHER++;
    });
    if (kpis) {
      kpis.innerHTML =
        '<div class="small">Batch <b>' +
        results.filter(function (r) {
          return r.ok;
        }).length +
        "/4</b> · APPROVE <b>" +
        counts.APPROVE +
        "</b> · BLOCK <b>" +
        counts.BLOCK +
        "</b> · ESCALATE <b>" +
        counts.ESCALATE +
        "</b></div>";
    }
    var lines = ["FULL EVA BATCH · " + (mid || "model-001")];
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
    if (out)
      out.innerHTML =
        "Matrix complete · biased should be <span class=\"tag2 t-bad\">BLOCK</span>";
  };

  function wrapOversight() {
    if (typeof vOversight !== "function" || vOversight._v7) return;
    var _orig = vOversight;
    window.vOversight = async function (m) {
      await _orig(m);
      var h2 = document.querySelector("#main .pgh h2");
      if (h2) h2.textContent = "HITL Queue";
      var desc = document.querySelector("#main .pgh .desc");
      if (desc)
        desc.textContent =
          "Human-in-the-loop · escalated & blocked · COB · portal dual-path (Internal)";
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
      setTimeout(run, 80);
    };
  }
})();
