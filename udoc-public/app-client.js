/* UDOC client densify — gzip payloads from GitHub (platform-core/static) */
(async function(){
  var bases=[
    "https://raw.githubusercontent.com/Surge4life/CapstoneProjectSJS/main/platform-core/static/",
    location.origin+"/"
  ];
  function run(t){var s=document.createElement("script");s.textContent=t;document.head.appendChild(s);}
  async function tryBase(base){
    var chunks=[];
    for(var i=0;i<5;i++){
      var r=await fetch(base+"client_app_payload_"+i+".b64?v=20260811",{cache:"no-store"});
      if(!r.ok) throw new Error("part "+i+" "+r.status);
      chunks.push((await r.text()).trim());
    }
    var b64=chunks.join("");
    while(b64.length%4) b64+="=";
    var bin=Uint8Array.from(atob(b64),function(c){return c.charCodeAt(0);});
    var stream=new Blob([bin]).stream().pipeThrough(new DecompressionStream("gzip"));
    var txt=await new Response(stream).text();
    if(txt.length<1000) throw new Error("short");
    run(txt);
  }
  var last=null;
  for(var i=0;i<bases.length;i++){
    try{await tryBase(bases[i]);return;}catch(e){last=e;}
  }
  console.error("[app-client] densify failed", last);
  document.body&&document.body.insertAdjacentHTML("afterbegin",
    '<div style="background:#3b1d1d;color:#fecaca;padding:8px 12px;font:13px system-ui">Client densify missing — '+String(last&&last.message||last)+'</div>');
})();
