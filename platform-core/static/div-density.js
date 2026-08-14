/*! div-density.js — multi-environment density for operator surfaces
 * Inject only. Links Core + Gateway + Client + Sector + Operator.
 * Capstone density package Priority 1 — 2026-08-14
 */
(function () {
  if (window.__DIV_DENSITY__) return;
  window.__DIV_DENSITY__ = 1;
  const API = location.origin;
  const CORE = "https://gods-platform-core.onrender.com";
  const ENV = {
    gateway: "https://gods-udoc-gateway.onrender.com/",
    client: "https://gods-udoc-client.onrender.com/",
    sector: "https://gods-udoc-sector.onrender.com/",
    operator: "https://gods-udoc-operator.onrender.com/",
    portals: "https://gods-udoc-portals.onrender.com/",
    adminHost: "https://gods-udoc-admin.onrender.com/",
    web: "https://gods-udoc-web.onrender.com/"
  };

  function el(tag, attrs, html) {
    const n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === "style" && typeof attrs[k] === "object") Object.assign(n.style, attrs[k]);
      else if (k === "onclick") n.onclick = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    if (html != null) n.innerHTML = html;
    return n;
  }

  function log(msg) {
    const t = document.getElementById("dd-term");
    if (!t) return;
    t.textContent = new Date().toLocaleTimeString() + "  " + msg + "\n" + t.textContent.slice(0, 1200);
  }

  function setK(id, v) {
    const n = document.getElementById(id);
    if (n) n.textContent = v;
  }

  async function evaSmoke() {
    try {
      const j = await (await fetch(API + "/decisions/batch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenarios: ["fair", "biased"] })
      })).json();
      const o = j.outcomes || {};
      const gate = Number(o.BLOCK || 0) >= 1 ? "PASS" : "CHECK";
      setK("dd-eva", gate + " · B" + (o.BLOCK || 0) + "/A" + (o.APPROVE || 0));
      log("EVA " + gate + " " + JSON.stringify(o));
      return gate;
    } catch (e) {
      setK("dd-eva", "FAIL");
      log("EVA FAIL " + e.message);
    }
  }

  async function probeReady() {
    try {
      const j = await (await fetch(API + "/udoc/demo/ready")).json();
      setK("dd-ready", j.ready ? "READY" : "NO");
      log("READY " + JSON.stringify({ ready: j.ready }));
    } catch (e) {
      setK("dd-ready", "FAIL");
      log("READY FAIL " + e.message);
    }
  }

  async function probeHealth() {
    try {
      const j = await (await fetch(API + "/health")).json();
      setK("dd-health", j.status || "ok");
      log("HEALTH " + (j.status || "ok"));
    } catch (e) {
      setK("dd-health", "FAIL");
      log("HEALTH FAIL " + e.message);
    }
  }

  function mount() {
    if (document.getElementById("div-density-root")) return;
    const host = document.querySelector(".wrap") || document.querySelector("main") || document.body;
    const root = el("div", { id: "div-density-root" });
    root.style.cssText = "max-width:1100px;margin:12px auto;padding:0 16px 28px;font:13px/1.45 system-ui,sans-serif;color:#e8edf6";
    root.innerHTML = [
      '<div style="background:#0c1830;border:1px solid #1c2a45;border-radius:12px;padding:14px;margin-bottom:10px">',
      '<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px">',
      '<b style="color:#C9A84C">Assessor · density strip</b>',
      '<span style="font-size:11px;color:#8fa0bd">Core probes · multi-env · capital not_deployed</span>',
      '<span style="flex:1"></span>',
      '<button type="button" id="dd-run" style="background:#00C2D4;color:#041018;border:none;border-radius:8px;padding:6px 12px;font-weight:600;cursor:pointer;font-size:12px">Run probes</button>',
      '</div>',
      '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin-bottom:10px">',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">Health</div><div id="dd-health" style="font-weight:700">—</div></div>',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">Ready</div><div id="dd-ready" style="font-weight:700">—</div></div>',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">EVA</div><div id="dd-eva" style="font-weight:700">—</div></div>',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">Honesty</div><div style="font-weight:700;font-size:12px">not_deployed</div></div>',
      '</div>',
      '<div style="font-family:ui-monospace,monospace;font-size:11px;background:#050b16;border:1px solid #1c2a45;border-radius:8px;padding:10px;white-space:pre-wrap;max-height:120px;overflow:auto" id="dd-term">Density · Core probes</div>',
      '</div>',
      '<div style="background:#0c1830;border:1px solid #1c2a45;border-radius:12px;padding:14px">',
      '<div style="color:#C9A84C;font-weight:600;margin-bottom:8px;font-size:12px">Environments · full stack</div>',
      '<div style="display:flex;flex-wrap:wrap;gap:6px">',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#e8edf6;text-decoration:none" href="/seths">SETHS</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#e8edf6;text-decoration:none" href="/ts">TS</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#e8edf6;text-decoration:none" href="/madiba">MADIBA</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#e8edf6;text-decoration:none" href="/divisions">Divisions</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#e8edf6;text-decoration:none" href="/gbs">GBS</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#e8edf6;text-decoration:none" href="/eif-ui">EIF</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#e8edf6;text-decoration:none" href="/Sentinel">Sentinel</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#e8edf6;text-decoration:none" href="/portals">Portals</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#e8edf6;text-decoration:none" href="/udoc-admin">UDOC Admin</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#00C2D4;text-decoration:none" href="' + ENV.gateway + '" target="_blank" rel="noopener">Gateway</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#00C2D4;text-decoration:none" href="' + ENV.client + '" target="_blank" rel="noopener">Client</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#00C2D4;text-decoration:none" href="' + ENV.sector + '" target="_blank" rel="noopener">Sector</a>',
      '<a style="border:1px solid #1c2a45;border-radius:16px;padding:3px 10px;font-size:11px;color:#00C2D4;text-decoration:none" href="' + ENV.operator + '" target="_blank" rel="noopener">Operator</a>',
      '</div>',
      '<p style="margin:10px 0 0;font-size:11px;color:#8fa0bd">Honesty: capital not_deployed · MADIBA ≠ AUM · Sovereign-Verified designed_not_built · UDOC controller · density Priority 1</p>',
      '</div>'
    ].join("");
    host.appendChild(root);
    document.getElementById("dd-run").onclick = function () {
      probeHealth(); probeReady(); evaSmoke();
    };
    setTimeout(function () { probeHealth(); probeReady(); evaSmoke(); }, 400);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();

/* density package v2 — path-aware metrics */
(function densifyV2(){
  if (window.__DIV_DENSITY_V2__) return;
  window.__DIV_DENSITY_V2__ = 1;
  const API = location.origin;
  const path = (location.pathname || "/").replace(/\/$/, "") || "/";

  function setK(id, v) {
    const n = document.getElementById(id);
    if (n) n.textContent = v;
  }

  function card(title, id) {
    return '<div style="background:#091022;border:1px solid #1c2a45;border-radius:10px;padding:10px">' +
      '<div style="font-size:10px;color:#C9A84C;text-transform:uppercase">' + title + '</div>' +
      '<div id="' + id + '" style="font-weight:700;font-size:1.05rem;margin-top:4px">—</div></div>';
  }

  async function loadMetrics() {
    try {
      const h = await (await fetch(API + "/health")).json();
      setK("dv2-health", h.status || "ok");
    } catch (e) { setK("dv2-health", "FAIL"); }
    try {
      const r = await (await fetch(API + "/udoc/demo/ready")).json();
      setK("dv2-ready", r.ready ? "READY" : "NO");
    } catch (e) { setK("dv2-ready", "FAIL"); }
    try {
      const batch = await (await fetch(API + "/decisions/batch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenarios: ["fair", "biased"] })
      })).json();
      const o = batch.outcomes || {};
      const gate = Number(o.BLOCK || 0) >= 1 ? "PASS" : "CHECK";
      setK("dv2-eva", gate + " · B" + (o.BLOCK || 0) + "/A" + (o.APPROVE || 0));
    } catch (e) { setK("dv2-eva", "FAIL"); }

    try {
      if (path.indexOf("seths") >= 0) {
        const m = await (await fetch(API + "/seths/metrics")).json();
        setK("dv2-m1", m.total != null ? m.total : "—");
        setK("dv2-m2", m.placed != null ? m.placed : "—");
        setK("dv2-m3", m.placement_rate != null ? (Math.round(m.placement_rate * 100) + "%") : "—");
      } else if (path.indexOf("/ts") >= 0 || path.endsWith("ts")) {
        const m = await (await fetch(API + "/ts/metrics")).json();
        setK("dv2-m1", m.projects != null ? m.projects : (m.total != null ? m.total : "—"));
        setK("dv2-m2", m.workers_absorbed != null ? m.workers_absorbed : (m.workers != null ? m.workers : "—"));
        setK("dv2-m3", "TS deploy");
      } else if (path.indexOf("madiba") >= 0) {
        const m = await (await fetch(API + "/madiba/metrics")).json();
        setK("dv2-m1", m.cycles != null ? m.cycles : (m.total != null ? m.total : "—"));
        setK("dv2-m2", m.cumulative_recycled != null ? m.cumulative_recycled : (m.recycled != null ? m.recycled : "—"));
        setK("dv2-m3", "≠ AUM");
      } else if (path.indexOf("gbs") >= 0 || path.indexOf("holdings") >= 0) {
        setK("dv2-m1", "GBS");
        setK("dv2-m2", "designed_not_built");
        setK("dv2-m3", "four-division");
      } else {
        setK("dv2-m1", path.split("/").pop() || "core");
        setK("dv2-m2", "operator");
        setK("dv2-m3", "Capstone");
      }
    } catch (e) {
      setK("dv2-m1", "—"); setK("dv2-m2", "—"); setK("dv2-m3", "—");
    }
  }

  function mountV2() {
    if (document.getElementById("div-density-v2")) return;
    const host = document.querySelector(".wrap") || document.querySelector("main") || document.body;
    const box = document.createElement("div");
    box.id = "div-density-v2";
    box.style.cssText = "max-width:1100px;margin:12px auto;padding:0 16px 24px;font:13px/1.45 system-ui,sans-serif;color:#e8edf6";
    box.innerHTML = [
      '<div style="background:#0c1830;border:1px solid #1c2a45;border-radius:12px;padding:14px">',
      '<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px">',
      '<b style="color:#C9A84C">Density package · live metrics</b>',
      '<span style="font-size:11px;color:#8fa0bd">path-aware · Core API</span>',
      '<span style="flex:1"></span>',
      '<button type="button" id="dv2-refresh" style="background:#00C2D4;color:#041018;border:none;border-radius:8px;padding:6px 12px;font-weight:600;cursor:pointer;font-size:12px">Refresh metrics</button>',
      '</div>',
      '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px">',
      card("Health", "dv2-health"),
      card("Ready", "dv2-ready"),
      card("EVA gate", "dv2-eva"),
      card("Metric A", "dv2-m1"),
      card("Metric B", "dv2-m2"),
      card("Metric C", "dv2-m3"),
      '</div></div>'
    ].join("");
    host.appendChild(box);
    const btn = document.getElementById("dv2-refresh");
    if (btn) btn.onclick = loadMetrics;
    loadMetrics();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mountV2);
  else mountV2();
})();
