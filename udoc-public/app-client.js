/* Permanent densified client — inflate from same-origin or GitHub raw payloads */
(async function(){
  var bases=[
    location.origin+"/",
    "https://raw.githubusercontent.com/Surge4life/CapstoneProjectSJS/main/udoc-public/"
  ];
  function loadScript(txt){var s=document.createElement("script");s.textContent=txt;document.head.appendChild(s);}
  async function tryBase(base){
    var chunks=[];
    for(var i=0;i<5;i++){
      var r=await fetch(base+"app_client_payload_"+i+".b64?v=20260807c",{cache:"no-store"});
      if(!r.ok) throw new Error("part "+i+" "+r.status);
      chunks.push((await r.text()).trim());
    }
    var b64=chunks.join("");
    var bin=Uint8Array.from(atob(b64),function(c){return c.charCodeAt(0);});
    var stream=new Blob([bin]).stream().pipeThrough(new DecompressionStream("gzip"));
    var txt=await new Response(stream).text();
    if(txt.length<1000) throw new Error("short");
    loadScript(txt);
  }
  var last=null;
  for(var b=0;b<bases.length;b++){
    try{await tryBase(bases[b]);return;}catch(e){last=e;}
  }
  console.error("[app-client] density load failed", last);
  document.body&&(document.body.insertAdjacentHTML("afterbegin",
    '<div style="background:#3b1d1d;color:#fecaca;padding:8px 12px;font:13px system-ui">Client density payload missing — '+String(last&&last.message||last)+'</div>'));
})();
