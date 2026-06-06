const BASE = import.meta.env.VITE_API_BASE || "/api";
let token: string | null = localStorage.getItem("gods_int_token");
export function setToken(t:string|null){ token=t; t?localStorage.setItem("gods_int_token",t):localStorage.removeItem("gods_int_token"); }
export function getToken(){ return token; }
async function req(p:string,o:RequestInit={}){
  const h:Record<string,string>={"Content-Type":"application/json",...(o.headers as any)};
  if(token) h["Authorization"]=`Bearer ${token}`;
  const r=await fetch(`${BASE}${p}`,{...o,headers:h});
  if(!r.ok) throw new Error((await r.json().catch(()=>({}))).detail||`HTTP ${r.status}`);
  return r.json();
}
export const api={
  get:(p:string)=>req(p), post:(p:string,b?:any)=>req(p,{method:"POST",body:b?JSON.stringify(b):undefined}),
  del:(p:string)=>req(p,{method:"DELETE"}),
  login: async(email:string,password:string)=>{
    const f=new URLSearchParams({username:email,password});
    const r=await fetch(`${BASE}/auth/login`,{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:f});
    if(!r.ok) throw new Error("bad credentials"); const d=await r.json(); setToken(d.access_token); return d;
  },
};
