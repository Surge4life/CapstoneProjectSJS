/*! client-env-density.js — Capstone env links for Client package (Gateway + Core honesty) */
(function(){
  if(window.__CLIENT_ENV_DENSITY__) return; window.__CLIENT_ENV_DENSITY__=1;
  const CORE="https://gods-platform-core.onrender.com";
  function mount(){
    if(document.getElementById("client-env-density")) return;
    const host=document.querySelector("header")||document.body;
    const bar=document.createElement("div");
    bar.id="client-env-density";
    bar.style.cssText="display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:6px 12px;border-bottom:1px solid #1A2D4A;background:#0A1628;font-size:11px";
    bar.innerHTML='<span style="color:#C9A84C;font-weight:600">Env</span>'+
      '<a style="color:#00C2D4;text-decoration:none" href="https://gods-udoc-gateway.onrender.com/" target="_blank">Gateway</a>'+
      '<a style="color:#94A3B8;text-decoration:none" href="'+CORE+'/Sentinel" target="_blank">Sentinel</a>'+
      '<a style="color:#94A3B8;text-decoration:none" href="'+CORE+'/portals" target="_blank">Core Portals</a>'+
      '<a style="color:#94A3B8;text-decoration:none" href="/citizen.html">Citizen</a>'+
      '<span style="color:#64748B;margin-left:auto">Client package · Core API · capital not_deployed</span>';
    if(host.tagName==="HEADER") host.parentNode.insertBefore(bar, host.nextSibling);
    else document.body.insertBefore(bar, document.body.firstChild);
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",mount);
  else mount();
})();
