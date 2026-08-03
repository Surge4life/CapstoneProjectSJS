/* Bootstrap: restore after placeholder corruption. Loads last-good client then batch overlay. */
(async function () {
  var GOOD =
    "https://raw.githubusercontent.com/Surge4life/CapstoneProjectSJS/cdfb7e1d/udoc-public/app-client.js";
  var OVERLAY =
    "https://raw.githubusercontent.com/Surge4life/CapstoneProjectSJS/main/udoc-public/client-batch-overlay.js";
  function loadScriptText(txt) {
    var s = document.createElement("script");
    s.textContent = txt;
    document.head.appendChild(s);
  }
  try {
    var r = await fetch(GOOD + "?t=" + Date.now());
    if (!r.ok) throw new Error("restore fetch " + r.status);
    loadScriptText(await r.text());
    try {
      var o = await fetch(OVERLAY + "?t=" + Date.now());
      if (o.ok) loadScriptText(await o.text());
    } catch (e2) {}
  } catch (e) {
    console.error("[udoc] app-client bootstrap failed", e);
    document.body &&
      (document.body.innerHTML =
        '<pre style="padding:20px;color:#f66">Client JS restore failed: ' +
        String(e.message || e) +
        "\nOpen Core /health and hard-refresh.</pre>");
  }
})();
