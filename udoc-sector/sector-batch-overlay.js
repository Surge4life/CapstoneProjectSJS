/* Sector Full EVA → POST /decisions/batch — include after main sector <script> */
(function () {
  window.runEvalBatch = async function () {
    var o = document.getElementById("ev-out");
    var kpis = document.getElementById("ev-batch-kpis");
    if (o) o.innerHTML = '<div class="muted small">POST /decisions/batch …</div>';
    var mid =
      (document.getElementById("ev-mid") && document.getElementById("ev-mid").value.trim()) ||
      "model-001";
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
          '<div class="small">Gate fair≠BLOCK <b>' +
          (g.fair_neq_block ? "PASS" : "FAIL") +
          "</b> · biased=BLOCK <b>" +
          (g.biased_eq_block ? "PASS" : "FAIL") +
          "</b></div>";
    } catch (e) {
      if (o) o.innerHTML = '<div class="t-bad">' + (e.message || e) + "</div>";
      return;
    }
    var counts = { APPROVE: 0, BLOCK: 0, ESCALATE: 0, OTHER: 0 };
    results.forEach(function (r) {
      var d = String(r.decision || "").toUpperCase();
      if (d === "APPROVE") counts.APPROVE++;
      else if (d === "BLOCK") counts.BLOCK++;
      else if (d === "ESCALATE") counts.ESCALATE++;
      else counts.OTHER++;
    });
    var term = "SECTOR FULL EVA BATCH · " + mid + "\n";
    results.forEach(function (r) {
      term +=
        "\n[" +
        r.kind +
        "] → " +
        (r.decision || "?") +
        (r.eva != null ? " · EVA " + r.eva : "") +
        "\n";
    });
    if (o)
      o.innerHTML =
        '<div class="panel"><h3>Batch · ' +
        results.length +
        " · APPROVE " +
        counts.APPROVE +
        " · BLOCK " +
        counts.BLOCK +
        '</h3><pre class="mono" style="font-size:11px;white-space:pre-wrap">' +
        term.replace(/</g, "&lt;") +
        "</pre></div>";
  };
})();
