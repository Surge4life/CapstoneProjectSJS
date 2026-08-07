(async function(){
  var bases=[location.origin+"/", "https://raw.githubusercontent.com/Surge4life/CapstoneProjectSJS/main/udoc-public/"];
  async function load(name){
    for(var i=0;i<bases.length;i++){
      try{
        var r=await fetch(bases[i]+name+"?v=20260807d",{cache:"no-store"});
        if(!r.ok) continue;
        var t=await r.text();
        if(t.length<50) continue;
        var s=document.createElement("script"); s.textContent=t; document.head.appendChild(s);
        return true;
      }catch(e){}
    }
    return false;
  }
  var okA=await load("app-client-a.js");
  var okB=await load("app-client-b.js");
  if(!okA||!okB){
    console.error("[app-client] densify parts missing", okA, okB);
    document.body&&document.body.insertAdjacentHTML("afterbegin",
      '<div style="background:#3b1d1d;color:#fecaca;padding:8px 12px;font:13px system-ui">Client densify parts missing — hard-refresh or check app-client-a/b.js</div>');
  }
})();
