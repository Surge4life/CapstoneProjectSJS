/* UDOC Admin P3 — v7-platform Command Centre parity
 * Fixes esc, relabels nav, Command Centre boot, infra links, denser EVA + HITL.
 */
(function () {
  "use strict";

  window.esc = function (s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&")
      .replace(/</g, "<")
      .replace(/>/g, ">")
      .replace(/"/g, """);
  };

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
      '<div class="sech">INFRASTRUCTURE</div>' +
      '<div class="navitem" data-view="_sentinel"><span class="ico">◎</span> Sentinel runtime</div>' +
      '<div class="navitem" data-view="_apihealth"><span class="ico">⚡</span> API Health</div>' +
      '<div class="navitem" data-view="_jobs"><span class="ico">⏱</span> Scheduled Jobs</div>' +
      '<div class="navitem" data-view="_portals"><span class="ico">▤</span> 24 Portals</div>';
    nav.appendChild(div);
    div.querySelectorAll(".navitem").forEach(function (n) {
      n.addEventListener("click", function () {
        var v = n.dataset.view;
        var base =
          typeof apiBase === "function"
            ? apiBase()
            : "https://gods-platform-core.onrender.com";
        if (v === "_sentinel") window.open(base + "/Sentinel", "_blank");
        else if (v === "_apihealth") window.location.href = "/api-health.html";
        else if (v === "_jobs") window.location.href = "/jobs.html";
        else if (v === "_portals") window.open(base + "/portals", "_blank");
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
        var banner = document.createElement("div");
        banner.className = "panel";
        banner.style.borderLeft = "3px solid #C9A84C";
        banner.innerHTML =
          "<h3>Command Centre · boot posture</h3><div class=\"small\">" +
          (ready.ready
            ? '<span class="tag2 t-ok">DEMO READY</span> · active rules ' +
              esc(String(ready.active_rules)) +
              ' · prefer <span class="mono">model-001</span>'
            : '<span class="tag2 t-bad">SEED PENDING</span> · ' +
              esc((ready.missing || []).join("; ") || "check Core")) +
          '</div><div class="small muted" style="margin-top:8px">v7-platform parity · live Core · Neon ≤500MB</div>';
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
          "Full platform overview · live registry · SA NAIFP / POPIA · fail-closed";
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
          "<h3>EVA scenario chips (v7 parity)</h3>" +
          '<div class="row" style="gap:8px;flex-wrap:wrap">' +
          '<button class="btn cyan sm" onclick="v7Eva(\'fair\')">Fair</button>' +
          '<button class="btn sm" onclick="v7Eva(\'biased\')">Biased → BLOCK</button>' +
          '<button class="btn sm" onclick="v7Eva(\'high\')">High-risk</button>' +
          '<button class="btn sm" onclick="v7Eva(\'sov\')">Sovereignty</button>' +
          "</div><div id="v7-eva-out" class="small muted" style="margin-top:10px"></div>";
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

  window.v7Eva = async function (kind) {
    var out = document.getElementById("v7-eva-out");
    if (out) out.textContent = "Evaluating " + kind + "…";
    var midEl = document.getElementById("ev-mid");
    var mid = midEl ? midEl.value.trim() : "model-001";
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
      if (document.getElementById("ev-fair") && kind === "biased") {
        document.getElementById("ev-fair").value = "biased";
      }
      if (typeof runEvaluate === "function" && kind === "biased") {
        /* leave panel for full dim view */
      }
    } catch (e) {
      if (out) out.innerHTML = '<span class="t-bad">' + esc(e.message) + "</span>";
    }
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
          "Human-in-the-loop · escalated & blocked decisions · COB resolution";
    };
    window.vOversight._v7 = true;
  }

  function run() {
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
