(async function(){
  var bases=[location.origin+"/", "https://raw.githubusercontent.com/Surge4life/CapstoneProjectSJS/main/udoc-public/"];
  async function fetchText(name){
    for(var i=0;i<bases.length;i++){
      try{
        var r=await fetch(bases[i]+name+"?v=20260807e",{cache:"no-store"});
        if(!r.ok) continue;
        var t=await r.text();
        if(t.length<20) continue;
        return t;
      }catch(e){}
    }
    return null;
  }
  function run(t){var s=document.createElement("script");s.textContent=t;document.head.appendChild(s);}
  var a1=await fetchText("app-client-a1.js");
  var a2=await fetchText("app-client-a2.js");
  var bb=await fetchText("app-client-b.js");
  if(!a1||!a2||!bb){
    console.error("[app-client] missing parts",!!a1,!!a2,!!bb);
    document.body&&document.body.insertAdjacentHTML("afterbegin",
      '<div style="background:#3b1d1d;color:#fecaca;padding:8px 12px;font:13px system-ui">Client densify parts missing</div>');
    return;
  }
  run(a1+a2);
  run(bb);
})();
