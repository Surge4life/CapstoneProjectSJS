"""Local fallback EVA for the edge node (mirrors core thresholds; used when offline)."""
RISK = {"MINIMAL":0.0,"NOTABLE":0.2,"MEDIUM":0.5,"HIGH":0.8,"UNACCEPTABLE":1.0}
def local_decide(model_id, sig):
    risk = RISK.get(sig.get("risk_tier","NOTABLE"),0.5)
    sov = min(sig.get("bgp",1.0),sig.get("traceroute",1.0),sig.get("dnssec",1.0),sig.get("storage",1.0))
    reasons=[]
    if risk>=0.8: reasons.append("local: risk≥0.8")
    if sov<1.0: reasons.append(f"local: sovereignty breach {sov}")
    decision = "BLOCK" if reasons else ("REVIEW" if risk>=0.5 else "APPROVE")
    return {"model_id":model_id,"decision":decision,"sovereign":sov>=1.0,
            "block_reasons":reasons,"_local":True}
