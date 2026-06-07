const KEY_BASE = "gods_api_base";
const KEY_TOKEN = "gods_token";
export function getBase(){ return localStorage.getItem(KEY_BASE) || "https://gods-platform-core.onrender.com"; }
export function setBase(b:string){ localStorage.setItem(KEY_BASE, b.replace(/\/$/, "")); }
export function getToken(){ return localStorage.getItem(KEY_TOKEN); }
export function setToken(t:string|null){ t?localStorage.setItem(KEY_TOKEN,t):localStorage.removeItem(KEY_TOKEN); }
async function req(path:string, opts:RequestInit={}){
  const headers:Record<string,string>={"Content-Type":"application/json",...(opts.headers as any)};
  const tok=getToken(); if(tok) headers["Authorization"]=`Bearer ${tok}`;
  const res=await fetch(`${getBase()}${path}`,{...opts,headers});
  if(!res.ok) throw new Error((await res.json().catch(()=>({}))).detail||`HTTP ${res.status}`);
  return res.json();
}
export async function ping(){ try{ return (await fetch(`${getBase()}/health`)).ok; }catch{ return false; } }
export const api={
  get:(p:string)=>req(p),
  post:(p:string,b?:any)=>req(p,{method:"POST",body:b?JSON.stringify(b):undefined}),
  patch:(p:string,b?:any)=>req(p,{method:"PATCH",body:b?JSON.stringify(b):undefined}),
  login: async(email:string,password:string)=>{
    const body=`username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`;
    const hit=()=>fetch(`${getBase()}/auth/login`,{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body});
    let res:Response|undefined;
    try{ res=await hit(); }
    catch{ // network error => free-tier core likely asleep; wake it and retry
      for(let i=0;i<4 && !res;i++){ try{ await fetch(`${getBase()}/health`); }catch{} await new Promise(r=>setTimeout(r,2500)); try{ res=await hit(); }catch{} }
      if(!res) throw new Error("server is waking up — tap Sign in again in a few seconds");
    }
    if(!res.ok) throw new Error(res.status===401?"bad credentials":`sign-in failed (HTTP ${res.status})`);
    const d=await res.json(); setToken(d.access_token); return d;
  },
  // ── G.O.D.S Intelligence (internal: operator/gov/admin) ──
  intelState:()=>req("/intel/state"),
  intelDocs:()=>req("/intel/docs"),
  intelAsk:(query:string)=>req("/intel/ask",{method:"POST",body:JSON.stringify({query})}),
  intelText:(title:string,text:string,category:string)=>req("/intel/ingest-text",{method:"POST",body:JSON.stringify({title,text,category})}),
  intelIngest: async(file:File,title:string,category:string)=>{
    const fd=new FormData(); fd.append("file",file); fd.append("title",title||file.name); fd.append("category",category);
    const tok=getToken();
    const res=await fetch(`${getBase()}/intel/ingest`,{method:"POST",headers:tok?{"Authorization":`Bearer ${tok}`}:{},body:fd});
    if(!res.ok) throw new Error((await res.json().catch(()=>({}))).detail||"ingest failed"); return res.json();
  },
  // ── tenancy / commercial ──
  myTenant:()=>req("/tenants/me"),
  myKeys:()=>req("/tenants/me/apikeys"),
  issueMyKey:(name:string)=>req("/tenants/me/apikeys",{method:"POST",body:JSON.stringify({name})}),
  // ── policy versioning + COB ──
  submitPack:(id:number)=>req(`/policy/packs/${id}/submit`,{method:"POST"}),
  packVersions:(id:number)=>req(`/policy/versions?pack_id=${id}`),
  approveVersion:(vid:number)=>req(`/policy/versions/${vid}/approve`,{method:"POST"}),
  hotreload:()=>req("/policy/hotreload"),
  // multipart upload (documents)
  upload: async(division:string,owner:string,category:string,file:File)=>{
    const fd=new FormData(); fd.append("division",division); fd.append("owner_ref",owner);
    fd.append("category",category); fd.append("file",file);
    const tok=getToken();
    const res=await fetch(`${getBase()}/documents/upload`,{method:"POST",headers:tok?{"Authorization":`Bearer ${tok}`}:{},body:fd});
    if(!res.ok) throw new Error("upload failed"); return res.json();
  },
  uploadPolicy: async(name:string,jurisdiction:string,sector:string,file:File)=>{
    const fd=new FormData(); fd.append("name",name); fd.append("jurisdiction",jurisdiction);
    fd.append("sector",sector); fd.append("file",file);
    const tok=getToken();
    const res=await fetch(`${getBase()}/policy/upload`,{method:"POST",headers:tok?{"Authorization":`Bearer ${tok}`}:{},body:fd});
    if(!res.ok) throw new Error((await res.json().catch(()=>({}))).detail||"policy upload failed"); return res.json();
  },
  downloadUrl:(docRef:string)=>`${getBase()}/documents/${docRef}/download`,
};
