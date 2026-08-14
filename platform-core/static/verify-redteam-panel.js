/*! verify-redteam-panel.js — Capstone Red-Team / Verify gate (UDOC Admin)
 * Authority: GODS_INTELLIGENCE_OPERATING_METHOD + VERIFY_REDTEAM_CHECKLIST
 * Does not call LLMs. Probes live Core only. Staff operator aid.
 */
(function () {
  if (window.__VERIFY_REDTEAM_PANEL__) return;
  window.__VERIFY_REDTEAM_PANEL__ = 1;
  const API = location.origin;

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
    const t = document.getElementById("vrt-term");
    if (!t) return;
    t.textContent = new Date().toLocaleTimeString() + "  " + msg + "\n" + t.textContent.slice(0, 1800);
  }

  function setK(id, v) {
    const n = document.getElementById(id);
    if (n) n.textContent = v;
  }

  async function probeLive() {
    try {
      const h = await (await fetch(API + "/health")).json();
      setK("vrt-h", h.status || "ok");
      log("HEALTH " + JSON.stringify(h).slice(0, 120));
    } catch (e) {
      setK("vrt-h", "FAIL");
      log("HEALTH FAIL " + e.message);
    }
    try {
      const r = await (await fetch(API + "/udoc/demo/ready")).json();
      setK("vrt-r", r.ready ? "READY" : "NO");
      log("READY " + JSON.stringify({ ready: r.ready }));
    } catch (e) {
      setK("vrt-r", "FAIL");
      log("READY FAIL " + e.message);
    }
    try {
      const j = await (await fetch(API + "/decisions/batch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenarios: ["fair", "biased"] })
      })).json();
      const o = j.outcomes || {};
      const gate = Number(o.BLOCK || 0) >= 1 ? "PASS" : "CHECK";
      setK("vrt-e", gate + " · B" + (o.BLOCK || 0) + "/A" + (o.APPROVE || 0));
      log("EVA " + gate + " " + JSON.stringify(o));
    } catch (e) {
      setK("vrt-e", "FAIL");
      log("EVA FAIL " + e.message);
    }
  }

  function toggleAttack(btn) {
    const s = btn.getAttribute("data-state") || "open";
    const next = s === "open" ? "hit" : s === "hit" ? "pass" : "open";
    btn.setAttribute("data-state", next);
    btn.textContent = btn.getAttribute("data-label") + " · " + next.toUpperCase();
    btn.style.borderColor = next === "pass" ? "#2D9B5A" : next === "hit" ? "#E85D5D" : "#1c2a45";
  }

  function mount() {
    if (document.getElementById("verify-redteam-panel")) return;
    const host = document.querySelector("main") || document.querySelector(".wrap") || document.body;
    const panel = el("div", { id: "verify-redteam-panel" });
    panel.style.cssText = "max-width:1100px;margin:16px auto;padding:0 16px 32px;font:13px/1.45 system-ui,sans-serif;color:#e8edf6";
    panel.innerHTML = [
      '<div style="background:#0c1830;border:1px solid #1c2a45;border-radius:12px;padding:14px">',
      '<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px">',
      '<b style="color:#C9A84C">Verify · Red-Team gate</b>',
      '<span style="font-size:11px;color:#8fa0bd">UDOC primacy · not LLM-as-controller · Capstone checklist</span>',
      '<span style="flex:1"></span>',
      '<button type="button" id="vrt-run" style="background:#00C2D4;color:#041018;border:none;border-radius:8px;padding:6px 12px;font-weight:600;cursor:pointer;font-size:12px">Run live probes</button>',
      '</div>',
      '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;margin-bottom:12px">',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">Health</div><div id="vrt-h" style="font-weight:700">—</div></div>',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">Ready</div><div id="vrt-r" style="font-weight:700">—</div></div>',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">EVA gate</div><div id="vrt-e" style="font-weight:700">—</div></div>',
      '<div style="background:#091022;border:1px solid #1c2a45;border-radius:8px;padding:10px"><div style="font-size:10px;color:#C9A84C;text-transform:uppercase">Honesty</div><div style="font-weight:700;font-size:12px">not_deployed</div></div>',
      '</div>',
      '<div style="margin-bottom:8px;font-size:11px;color:#C9A84C;text-transform:uppercase;letter-spacing:.06em">Red-Team attacks (click cycle: open → hit → pass)</div>',
      '<div id="vrt-attacks" style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px"></div>',
      '<div style="margin-bottom:8px;font-size:11px;color:#C9A84C;text-transform:uppercase;letter-spacing:.06em">Honesty bounds</div>',
      '<ul style="margin:0 0 12px;padding-left:18px;color:#8fa0bd;font-size:12px">',
      '<li>Capital <b style="color:#E8A13A">not_deployed</b></li>',
      '<li>MADIBA <b style="color:#E8A13A">≠ AUM</b> · Sovereign-Verified <b style="color:#E8A13A">designed_not_built</b> where stated</li>',
      '<li>UDOC is controller · LLM assist is not</li>',
      '<li>Zeros on metrics OK · free-tier Neon/Render bounds visible</li>',
      '</ul>',
      '<div style="font-family:ui-monospace,monospace;font-size:11px;background:#050b16;border:1px solid #1c2a45;border-radius:8px;padding:10px;white-space:pre-wrap;max-height:160px;overflow:auto" id="vrt-term">Verify · Red-Team · probes Core only</div>',
      '<p style="margin:10px 0 0;font-size:11px;color:#64748B">Full checklist: VERIFY_REDTEAM_CHECKLIST.md · Method: GODS_INTELLIGENCE_OPERATING_METHOD.md</p>',
      '</div>'
    ].join("");
    host.appendChild(panel);

    const attacks = [
      "Unsupported market size / ROI",
      "Implied funded national programme",
      "LLM-as-controller language",
      "Live feature that is only scaffolded",
      "Legal/POPIA certainty without counsel",
      "Cross-doc terminology drift",
      "Demo seed as production fleet"
    ];
    const box = document.getElementById("vrt-attacks");
    attacks.forEach(function (label) {
      const b = el("button", {
        type: "button",
        "data-label": label,
        "data-state": "open",
        style: "border:1px solid #1c2a45;border-radius:16px;padding:4px 10px;font-size:11px;cursor:pointer;background:#091022;color:#e8edf6"
      }, label + " · OPEN");
      b.onclick = function () { toggleAttack(b); };
      box.appendChild(b);
    });

    document.getElementById("vrt-run").onclick = function () { probeLive(); };
    setTimeout(function () { probeLive(); }, 500);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
