const KEY_BASE = "gods_api_base";
const KEY_TOKEN = "gods_token";
export function getBase(){ return localStorage.getItem(KEY_BASE) || "http://localhost:8000"; }
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
  login: async(email:string,password:string)=>{
    const form=new URLSearchParams({username:email,password});
    const res=await fetch(`${getBase()}/auth/login`,{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:form});
    if(!res.ok) throw new Error("bad credentials"); const d=await res.json(); setToken(d.access_token); return d;
  },
  // multipart upload (documents)
  upload: async(division:string,owner:string,category:string,file:File)=>{
    const fd=new FormData(); fd.append("division",division); fd.append("owner_ref",owner);
    fd.append("category",category); fd.append("file",file);
    const tok=getToken();
    const res=await fetch(`${getBase()}/documents/upload`,{method:"POST",headers:tok?{"Authorization":`Bearer ${tok}`}:{},body:fd});
    if(!res.ok) throw new Error("upload failed"); return res.json();
  },
  downloadUrl:(docRef:string)=>`${getBase()}/documents/${docRef}/download`,
};
