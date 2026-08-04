/* UDOC Admin — EIF density (M.A.D.I.B.A. Diamond · UDOC assurance)
 * Injected by SW after admin-v7-enhance.js. Staff-only nomination audit.
 */
(function () {
  function esc(s) {
    var d = document.createElement("div");
    d.textContent = String(s == null ? "" : s);
    return d.innerHTML;
  }
  function coreBase() {
    try {
      if (typeof apiBase === "function") return apiBase();
    } catch (e) {}
    return (
      localStorage.getItem("udoc_admin_api") ||
      "https://gods-platform-core.onrender.com"
    );
  }

  window.showEifPanel = async function () {
    var main = document.getElementById("main");
    if (!main) return;
    main.innerHTML =
      '<div class="pgh"><h2>EIF · Diamond</h2><span class="desc">M.A.D.I.B.A. Exceptional Individual Fund · UDOC assurance · no capital on free tier</span></div>' +
      '<div class="panel muted">Loading framework…</div>';
    try {
      var fw = await api("/eif/framework");
      var h = fw.honesty || {};
      var domains = (fw.domains || [])
        .map(function (d) {
          return (
            "<tr><td><b>" +
            esc(d.label) +
            '</b></td><td class="mono">' +
            esc(d.id) +
            '</td><td class="small muted">' +
            esc(d.examples) +
            "</td></tr>"
          );
        })
        .join("");
      var tiers = (fw.passport_tiers || [])
        .map(function (t) {
          return (
            "<tr><td><b>" +
            esc(t.tier) +
            "</b></td><td>" +
            esc(t.recognises) +
            "</td></tr>"
          );
        })
        .join("");
      var safeguards = (fw.safeguards || [])
        .map(function (s) {
          return (
            "<tr><td>" +
            esc(s.safeguard) +
            '</td><td class="mono small">' +
            esc(s.pillar) +
            "</td></tr>"
          );
        })
        .join("");
      main.innerHTML =
        '<div class="pgh"><h2>EIF · Diamond</h2><span class="desc">Staff assurance surface · audit-only nomination</span></div>' +
        '<div class="panel" style="border-left:3px solid #E8C97A"><h3>' +
        esc(fw.instrument || "EIF") +
        "</h3>" +
        '<div class="small muted">' +
        esc((fw.philosophy || {}).funds || "") +
        "</div>" +
        '<pre class="mono" style="margin-top:10px;font-size:11px;white-space:pre-wrap;background:#050a12;padding:10px;border-radius:8px">proven: ' +
        esc(h.proven || "") +
        "\ndesigned: " +
        esc(h.designed || "") +
        "\naspirational: " +
        esc(h.aspirational || "") +
        "</pre>" +
        '<div style="margin-top:10px"><a class="btn cyan sm" href="' +
        coreBase() +
        '/eif-ui" target="_blank">Open /eif-ui</a> ' +
        '<a class="btn sm" href="' +
        coreBase() +
        '/Sentinel" target="_blank">Sentinel</a></div></div>' +
        '<div class="panel"><h3>Six Domains</h3><table><thead><tr><th>Domain</th><th>Id</th><th>Examples</th></tr></thead><tbody>' +
        domains +
        "</tbody></table></div>" +
        '<div class="panel"><h3>Passport tiers · Diamond ceiling</h3><table><thead><tr><th>Tier</th><th>Recognises</th></tr></thead><tbody>' +
        tiers +
        "</tbody></table></div>" +
        '<div class="panel"><h3>Safeguards → UDOC pillars</h3><table><thead><tr><th>Safeguard</th><th>Pillar</th></tr></thead><tbody>' +
        safeguards +
        "</tbody></table></div>" +
        '<div class="panel"><h3>Nominate (audit log only · no funding)</h3>' +
        '<div class="row"><div class="f"><label>Nominee label</label><input id="eif-name" placeholder="Name or handle"/></div>' +
        '<div class="f"><label>Domain</label><select id="eif-dom">' +
        (fw.domains || [])
          .map(function (d) {
            return (
              '<option value="' + esc(d.id) + '">' + esc(d.label) + "</option>"
            );
          })
          .join("") +
        "</select></div>" +
        '<div class="f"><label>Pathway</label><select id="eif-path"><option value="open">Open / external</option><option value="seths_platinum">S.E.T.H.S. Platinum</option></select></div></div>' +
        "<label>Contribution summary</label><textarea id=\"eif-sum\" rows=\"3\" style=\"width:100%;background:#091022;border:1px solid var(--bd,#1A2D4A);color:inherit;border-radius:8px;padding:10px;font:inherit\"></textarea>" +
        '<label>Evidence note</label><input id="eif-ev" placeholder="Independent evidence pointer"/>' +
        '<div style="margin-top:10px"><button class="btn cyan" type="button" onclick="eifNominateAdmin()">Log nomination to UDOC audit</button> <span id="eif-msg" class="small muted"></span></div>' +
        '<div class="small muted" style="margin-top:8px">Pillar VI Transparency · LOGGED_PENDING_REVIEW · capital not deployed on Capstone host</div></div>';
    } catch (e) {
      main.innerHTML =
        '<div class="pgh"><h2>EIF · Diamond</h2></div><div class="panel t-bad">' +
        esc(e.message || e) +
        " · ensure Core /eif is live and you are signed in as staff</div>";
    }
  };

  window.eifNominateAdmin = async function () {
    var msg = document.getElementById("eif-msg");
    if (msg) msg.textContent = "…";
    try {
      var body = {
        nominee_label: (
          (document.getElementById("eif-name") &&
            document.getElementById("eif-name").value) ||
          ""
        ).trim(),
        domain:
          (document.getElementById("eif-dom") &&
            document.getElementById("eif-dom").value) ||
          "intellectual",
        contribution_summary: (
          (document.getElementById("eif-sum") &&
            document.getElementById("eif-sum").value) ||
          ""
        ).trim(),
        evidence_note: (
          (document.getElementById("eif-ev") &&
            document.getElementById("eif-ev").value) ||
          ""
        ).trim(),
        pathway:
          (document.getElementById("eif-path") &&
            document.getElementById("eif-path").value) ||
          "open",
      };
      if (!body.nominee_label || body.contribution_summary.length < 10) {
        if (msg) msg.textContent = "Nominee + contribution (≥10 chars) required";
        return;
      }
      var d = await api("/eif/nominate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (msg)
        msg.innerHTML =
          '<span class="t-ok">' +
          esc(d.status || "LOGGED") +
          "</span> · " +
          esc(d.udoc || "");
    } catch (e) {
      if (msg)
        msg.innerHTML =
          '<span class="t-bad">' + esc(e.message || e) + "</span>";
    }
  };

  function injectEifNav() {
    var nav = document.getElementById("nav");
    if (!nav || document.getElementById("v7-eif-nav")) return;
    var div = document.createElement("div");
    div.id = "v7-eif-nav";
    div.innerHTML =
      '<div class="sech">MADIBA · EIF</div>' +
      '<div class="navitem" data-view="_eif"><span class="ico">◆</span> EIF · Diamond</div>';
    nav.appendChild(div);
    div.querySelectorAll(".navitem").forEach(function (n) {
      n.addEventListener("click", function () {
        document
          .querySelectorAll("#nav .navitem")
          .forEach(function (x) {
            x.classList.remove("active");
          });
        n.classList.add("active");
        showEifPanel();
      });
    });
  }

  function run() {
    injectEifNav();
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", run);
  else run();
  setTimeout(run, 800);
  setTimeout(run, 2000);
})();
