const BASE = import.meta.env.VITE_API_BASE || "/api";
const DIVISION = "TS";
let token: string | null = localStorage.getItem("gods_token");
export function setToken(t: string | null){ token=t; t?localStorage.setItem("gods_token",t):localStorage.removeItem("gods_token"); }
export function getToken(){ return token; }
async function req(path:string, opts:RequestInit={}){
  const headers:Record<string,string>={"Content-Type":"application/json",...(opts.headers as any)};
  if(token) headers["Authorization"]=`Bearer ${token}`;
  const res=await fetch(`${BASE}${path}`,{...opts,headers});
  if(!res.ok) throw new Error((await res.json().catch(()=>({}))).detail||`HTTP ${res.status}`);
  return res.json();
}
export const api={
  division: DIVISION,
  get:(p:string)=>req(p),
  post:(p:string,b?:any)=>req(p,{method:"POST",body:b?JSON.stringify(b):undefined}),
  login: async (email:string,password:string)=>{
    const form=new URLSearchParams({username:email,password});
    const res=await fetch(`${BASE}/auth/login`,{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:form});
    if(!res.ok) throw new Error("bad credentials");
    const d=await res.json(); setToken(d.access_token); return d;
  },
  kpis:()=>req(`/analytics/${DIVISION}/kpis`),
  totals:()=>req(`/analytics/${DIVISION}/totals`),
  timeseries:(metric:string)=>req(`/analytics/${DIVISION}/timeseries?metric=${metric}`),
  records:(limit=50)=>req(`/analytics/${DIVISION}/records?limit=${limit}`),
};
