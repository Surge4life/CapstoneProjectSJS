/* UDOC Admin P3 — v7-platform Command Centre parity helpers
 * Loaded after main inline script. Fixes esc, densifies Overview as Command Centre,
 * adds demo boot posture + links to Sentinel / API Health / Jobs.
 */
(function () {
  "use strict";

  // Correct HTML escape (inline esc was entity-stripped in some builds)
  window.esc = function (s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&")
      .replace(/</g, "<")
      .replace(/>/g, ">")
      .replace(/"/g, """);
  };

  function relabelNav() {
    var map = {
      overview: "◈ Command Centre",
      systems: "◉ AI Registry",
      control: "⏻ Kill-switch",
      decisions: "🧠 EVA Command",
      lifecycle: "↻ AI Lifecycle",
      evidence: "◫ Evidence · Replay",
      policy: "📐 Policy Engine",
      oversight: "👁 HITL Queue",
      audit: "🔐 Audit Trail",
      governance: "⚖ Constitution",
      compliance: "✓ Compliance",
      sovereignty: "🛡 Sovereignty",
      incidents: "🚨 Incident Command",
      intelligence: "◈ Intelligence",
      tenants: "⌂ Clients / Tenants",
      divisions: "◎ Division Ops",
      sectors: "◫ Sectors",
      access: "👥 User Management",
      roles: "⚇ Roles & Profiles",
    };
    document.querySelectorAll("#nav .navitem").forEach(function (n) {
      var v = n.dataset.view;
      if (map[v]) {
        var ico = n.querySelector(".ico");
        var icon = ico ? ico.outerHTML : "";
        n.innerHTML = icon + " " + map[v].replace(/^[^\s]+\s/, "");
        // keep icon + full label
        n.innerHTML = "<span class=\"ico\"></span> " + map[v];
      }
    });
    // Section headers closer to demo
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
        var base = (typeof apiBase === "function" ? apiBase() : "https://gods-platform-core.onrender.com");
        if (v === "_sentinel") window.open(base + "/Sentinel", "_blank");
        else if (v === "_apihealth") window.location.href = "/api-health.html";
        else if (v === "_jobs") window.location.href = "/jobs.html";
        else if (v === "_portals") window.open(base + "/portals", "_blank");
      });
    });
  }

  var _origOverview = null;
  function wrapOverview() {
    if (typeof vOverview !== "function") return;
    if (vOverview._v7) return;
    _origOverview = vOverview;
    window.vOverview = async function (m) {
      await _origOverview(m);
      try {
        var ready = await api("/udoc/demo/ready");
        var banner = document.createElement("div");
        banner.className = "panel";
        banner.style.borderLeft = "3px solid #C9A84C";
        banner.innerHTML =
          "<h3>Command Centre · boot posture</h3><div class=\"small\">" +
          (ready.ready
            ? '<span class="tag2 t-ok">DEMO READY</span> · active rules ' +
              esc(ready.active_rules) +
              " · prefer <span class=\"mono\">model-001</span>"
            : '<span class="tag2 t-bad">SEED PENDING</span> · ' +
              esc((ready.missing || []).join("; ") || "check Core")) +
          "</div><div class=\"small muted\" style=\"margin-top:8px\">v7-platform parity path · live Core only · Neon ≤500MB</div>";
        var main = document.getElementById("main");
        if (main && main.firstChild) main.insertBefore(banner, main.children[1] || null);
        else if (main) main.appendChild(banner);
      } catch (e) {}
      // Title rename
      var h2 = document.querySelector("#main .pgh h2");
      if (h2) h2.textContent = "Command Centre";
      var desc = document.querySelector("#main .pgh .desc");
      if (desc) desc.textContent = "Full platform overview · live registry · SA NAIFP / POPIA · fail-closed";
    };
    window.vOverview._v7 = true;
  }

  function run() {
    relabelNav();
    injectInfraLinks();
    wrapOverview();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
  // Re-wrap after login enters app (nav rebuilt visibility)
  var _enter = window.enterApp;
  if (typeof _enter === "function") {
    window.enterApp = async function () {
      await _enter.apply(this, arguments);
      setTimeout(run, 50);
    };
  }
})();
