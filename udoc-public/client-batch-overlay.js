/* Client Full EVA batch → POST /decisions/batch — load after app-client.js */
(function () {
  window.gBatch = async function () {
    var out = document.getElementById("g-out");
    var kpis = document.getElementById("g-batch-kpis");
    if (out) out.innerHTML = '<div class="panel muted">POST /decisions/batch …</div>';
    var mid =
      (document.getElementById("g-mid") && document.getElementById("g-mid").value.trim()) ||
      "model-001";
    try {
      var pack = await api("/decisions/batch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_id: mid, options: ["fair", "biased", "high", "sov"] }),
      });
      var results = pack.results || [];
      var oc = pack.outcomes || {};
      var g = pack.gate || {};
      if (kpis)
        kpis.innerHTML =
          '<div class="grid kpis" style="margin-top:12px">' +
          '<div class="kpi"><div class="k">Batch</div><div class="v cyan">' +
          (pack.count || results.length) +
          "</div></div>" +
          '<div class="kpi"><div class="k">APPROVE</div><div class="v green">' +
          (oc.APPROVE || 0) +
          "</div></div>" +
          '<div class="kpi"><div class="k">BLOCK</div><div class="v red">' +
          (oc.BLOCK || 0) +
          "</div></div>" +
          '<div class="kpi"><div class="k">Gate</div><div class="v">' +
          (g.biased_eq_block && g.fair_neq_block ? "PASS" : "CHECK") +
          "</div></div></div>";
      var term = "FULL EVA BATCH · " + mid + " · /decisions/batch\n";
      results.forEach(function (r) {
        term +=
          "\n[" +
          (r.option || "?") +
          "] → " +
          (r.decision || r.error || "?") +
          (r.composite_eva != null ? " · EVA " + r.composite_eva : "") +
          "\n";
        (r.block_reasons || []).slice(0, 3).forEach(function (x) {
          term += "  • " + x + "\n";
        });
        if (r.certificate_id) window.LAST_CERT = r.certificate_id;
        if (r.id) window.LAST_DID = r.id;
      });
      if (out)
        out.innerHTML =
          '<div class="panel"><h3>Batch terminal</h3><div class="term">' +
          term.replace(/</g, "&lt;") +
          "</div></div>";
    } catch (e) {
      if (out) out.innerHTML = '<div class="panel t-bad">' + (e.message || e) + "</div>";
    }
  };
})();
