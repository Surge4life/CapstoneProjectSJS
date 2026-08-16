/* GODS Admin live density — divisions + SETHS→TS→MADIBA loop + ENTRY strip */
(function(){
  if(window.__GODS_ADMIN_DENSITY__) return;
  window.__GODS_ADMIN_DENSITY__=1;
  const API=location.origin;
  function tok(){try{return localStorage.getItem('gods_token')||localStorage.getItem('access_token')||'';}catch(e){return '';}}
  function authH(){const t=tok();return t?{Authorization:'Bearer '+t}:{};}
  function el(tag,attrs,html){const n=document.createElement(tag);if(attrs)Object.keys(attrs).forEach(k=>{if(k==='style'&&typeof attrs[k]==='object')Object.assign(n.style,attrs[k]);else if(k==='onclick')n.onclick=attrs[k];else n.setAttribute(k,attrs[k]);});if(html!=null)n.innerHTML=html;return n;}
  function log(id,m){const t=document.getElementById(id);if(t)t.textContent=new Date().toLocaleTimeString()+'  '+m+'\n'+t.textContent.slice(0,900);}

  async function j(path,opts){
    const h=Object.assign({},authH(),(opts&&opts.headers)||{});
    const r=await fetch(API+path,Object.assign({},opts||{},{headers:h}));
    const ct=r.headers.get('content-type')||'';
    const body=ct.includes('json')?await r.json().catch(()=>null):await r.text();
    if(!r.ok) throw new Error((body&&body.detail)||('HTTP '+r.status));
    return body;
  }

  function densify(){
    /* existing loop panels if present — additive only */
    if(document.getElementById('gods-live-loop')) return;
    const page=document.getElementById('page-cmd')||document.getElementById('page-seths')||document.querySelector('main');
    if(!page) return;
    const box=el('div',{id:'gods-live-loop'});
    box.style.cssText='margin:12px 0;padding:12px;background:#0c1830;border:1px solid #1c2a45;border-radius:12px;font:13px/1.45 system-ui,sans-serif;color:#e8edf6';
    box.innerHTML=[
      '<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px">',
      '<b style="color:#C9A84C">Division loop · SETHS → TS → MADIBA</b>',
      '<span style="font-size:11px;color:#8fa0bd">live Core metrics · capital not_deployed</span>',
      '<span style="flex:1"></span>',
      '<a href="/seths" style="color:#00C2D4;font-size:12px">SETHS operator</a>',
      '<a href="/ts" style="color:#00C2D4;font-size:12px">TS operator</a>',
      '<a href="/madiba" style="color:#00C2D4;font-size:12px">MADIBA operator</a>',
      '<a href="/portals" style="color:#00C2D4;font-size:12px">Portals</a>',
      '</div>',
      '<div id="gods-live-term" style="font-family:ui-monospace,monospace;font-size:11px;background:#050b16;border:1px solid #1c2a45;border-radius:8px;padding:8px;max-height:100px;overflow:auto">GODS Admin · division loop</div>'
    ].join('');
    page.insertBefore(box, page.firstChild);
  }

  function arm(){ densify(); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',function(){setTimeout(arm,300);});
  else setTimeout(arm,300);
  setInterval(function(){ densify(); }, 20000);
})();

/* GODS entry strip — Command / Portals / Divisions first; Intelligence is one page not the product */
(function godsEntryStrip(){
  if (window.__GODS_ENTRY_STRIP__) return;
  window.__GODS_ENTRY_STRIP__ = 1;

  function chip(href, label, primary) {
    var st = primary
      ? 'background:#00C2D4;color:#041018;border:none;font-weight:700;'
      : 'background:#091022;color:#e8edf6;border:1px solid #1c2a45;';
    return '<a href="'+href+'" style="'+st+'border-radius:16px;padding:6px 12px;font-size:12px;text-decoration:none;display:inline-block">'+label+'</a>';
  }

  function goPage(id) {
    var el = document.getElementById(id);
    if (el) {
      document.querySelectorAll('[id^="page-"]').forEach(function(p){ p.style.display = 'none'; });
      el.style.display = 'block';
      try { el.scrollIntoView({behavior:'smooth', block:'start'}); } catch(e) {}
      return true;
    }
    return false;
  }

  function mount() {
    if (document.getElementById('gods-entry-strip')) return;
    var host = document.querySelector('main') || document.querySelector('.app') || document.body;
    var root = document.createElement('div');
    root.id = 'gods-entry-strip';
    root.style.cssText = 'max-width:1200px;margin:10px auto;padding:0 16px 8px;font:13px/1.45 system-ui,sans-serif;color:#e8edf6;position:relative;z-index:50';
    root.innerHTML = [
      '<div style="background:#0c1830;border:1px solid #C9A84C;border-radius:12px;padding:12px 14px">',
      '<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px">',
      '<b style="color:#C9A84C">G.O.D.S internal · entry</b>',
      '<span style="font-size:11px;color:#8fa0bd">Command · Portals · Divisions first · Intelligence is one page</span>',
      '</div>',
      '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px">',
      chip('/admin','Command / Admin', true),
      chip('/portals','Portals · 24', true),
      chip('/divisions','Divisions', true),
      chip('/seths','SETHS', false),
      chip('/ts','TS', false),
      chip('/madiba','MADIBA', false),
      chip('/gbs','GBS', false),
      chip('/Sentinel','Sentinel · EVA', false),
      chip('/eif-ui','EIF', false),
      chip('/udoc-admin','UDOC Admin', false),
      '</div>',
      '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:6px">',
      '<button type="button" id="gods-go-cmd" style="border:1px solid #1c2a45;border-radius:16px;padding:5px 12px;font-size:12px;background:#091022;color:#e8edf6;cursor:pointer">Open Command page</button>',
      '<button type="button" id="gods-go-seths" style="border:1px solid #1c2a45;border-radius:16px;padding:5px 12px;font-size:12px;background:#091022;color:#e8edf6;cursor:pointer">Open SETHS page</button>',
      '<a href="/portals" style="border:1px solid #00C2D4;border-radius:16px;padding:5px 12px;font-size:12px;color:#00C2D4;text-decoration:none">Open Portals workspace</a>',
      '</div>',
      '<p style="margin:0;font-size:11px;color:#8fa0bd">Intelligence / corpus ask = grounded Capstone path (citeable). Richer agent intelligence = method layer under UDOC — not disabled, not the only product surface.</p>',
      '</div>'
    ].join('');
    if (host.firstChild) host.insertBefore(root, host.firstChild);
    else host.appendChild(root);

    var b1 = document.getElementById('gods-go-cmd');
    if (b1) b1.onclick = function(){ if(!goPage('page-cmd')) location.href='/admin'; };
    var b2 = document.getElementById('gods-go-seths');
    if (b2) b2.onclick = function(){ if(!goPage('page-seths')) location.href='/seths'; };
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function(){ setTimeout(mount, 200); });
  else setTimeout(mount, 200);
})();
