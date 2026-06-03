"""
Governance bridge — the 6-D EVA scoring + UDOC decision logic, in Python.
Mirrors the hardened TypeScript engines (capstone-source) so platform-core can make
sovereign governance decisions synchronously within the sub-50ms budget. The canonical
TS engines remain the reference; this is the in-process service implementation.
"""
import hashlib
import hmac
import os
import time
from dataclasses import dataclass, field
from typing import Optional

# Sovereign signing key. Production: injected from HSM (never in code/env). Emulated here.
_SOV_KEY = os.environ.get("GODS_SOV_KEY", "emulated-sovereign-key").encode()

RISK_TIER_R = {"MINIMAL": 0.0, "NOTABLE": 0.2, "MEDIUM": 0.5, "HIGH": 0.8, "UNACCEPTABLE": 1.0}

# SA default 6-D weights (sum = 1.0)
W = {"validity": 0.15, "confidence": 0.15, "risk": 0.25,
     "compliance": 0.20, "stability": 0.10, "societal": 0.15}

THRESH = {"risk_block": 0.80, "compliance_block": 0.70, "di_block": 0.80,
          "jsd_block": 0.40, "ecs_block": 0.65, "spd_block": 0.05}


@dataclass
class Evidence:
    model_id: str
    risk_tier: str = "NOTABLE"
    validity_correct: int = 950
    validity_total: int = 1000
    raw_confidence: float = 0.9
    temperature: float = 0.7
    compliance: float = 1.0
    current_dist: list = field(default_factory=lambda: [0.25, 0.25, 0.25, 0.25])
    baseline_dist: list = field(default_factory=lambda: [0.25, 0.25, 0.25, 0.25])
    priv_favorable: int = 480
    priv_total: int = 1000
    unpriv_favorable: int = 470
    unpriv_total: int = 1000
    ecs: float = 0.75            # CMAG ethical cooperation (C*A*I*F), precomputed upstream
    # Sovereignty signals (1.0 = clean)
    bgp: float = 1.0
    traceroute: float = 1.0
    dnssec: float = 1.0
    storage: float = 1.0


@dataclass
class Verdict:
    model_id: str
    decision: str
    svs: float
    risk: float
    compliance: float
    stability: float
    societal: float
    disparate_impact: float
    spd: float
    ecs: float
    sovereign: bool
    sovereign_svs: float
    seal: str
    latency_ms: float
    block_reasons: list


def _jsd(p, q):
    import math
    def kl(a, b):
        return sum(0.0 if ai == 0 else ai * math.log2(ai / (b[i] if b[i] else 1e-10))
                   for i, ai in enumerate(a))
    m = [(p[i] + q[i]) / 2 for i in range(len(p))]
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def _pos_rate(fav, tot):
    return fav / tot if tot else 0.0


def evaluate(ev: Evidence) -> Verdict:
    """Full 6-D EVA score + sovereignty (SVS=min) + decision, sealed with HMAC."""
    t0 = time.perf_counter()

    validity = max(0.0, min(1.0, ev.validity_correct / ev.validity_total)) if ev.validity_total else 0.0
    import math
    confidence = ev.raw_confidence / (1 + math.log(ev.temperature + 1)) if ev.temperature > 0 else ev.raw_confidence
    risk = RISK_TIER_R.get(ev.risk_tier, 0.5)
    compliance = ev.compliance
    jsd = _jsd(ev.current_dist, ev.baseline_dist)
    stability = max(0.0, 1 - jsd)

    pr_p = _pos_rate(ev.priv_favorable, ev.priv_total)
    pr_u = _pos_rate(ev.unpriv_favorable, ev.unpriv_total)
    di = (min(pr_p, pr_u) / max(pr_p, pr_u)) if max(pr_p, pr_u) > 0 else 1.0
    spd = pr_u - pr_p
    # Societal impact proxy (full H-OS-56 lives in the TS engine; here a calibrated proxy)
    societal = 0.7

    block = []
    if risk >= THRESH["risk_block"]:
        block.append(f"R={risk:.3f} ≥ 0.80 (risk)")
    if compliance < THRESH["compliance_block"]:
        block.append(f"Co={compliance:.3f} < 0.70 (compliance)")
    if di < THRESH["di_block"]:
        block.append(f"DI={di:.3f} < 0.80 (disparate impact)")
    if jsd > THRESH["jsd_block"]:
        block.append(f"JSD={jsd:.3f} > 0.40 (drift)")
    if ev.ecs < THRESH["ecs_block"]:
        block.append(f"ECS={ev.ecs:.3f} < 0.65 (cooperation)")
    if abs(spd) > THRESH["spd_block"]:
        block.append(f"|SPD|={abs(spd):.3f} > 0.05 (parity)")
    if ev.risk_tier == "UNACCEPTABLE":
        block.append("UNACCEPTABLE tier — permanent block")

    eva_svs = min(max(
        W["validity"] * validity + W["confidence"] * confidence + W["risk"] * (1 - risk) +
        W["compliance"] * compliance + W["stability"] * stability + W["societal"] * societal, 0.0), 1.0)

    # Sovereignty: SVS = min of signals; any breach forces non-sovereign + isolate.
    sov_svs = min(ev.bgp, ev.traceroute, ev.dnssec, ev.storage)
    sovereign = sov_svs >= 1.0
    if not sovereign:
        block.append(f"Sovereignty breach (SVS={sov_svs:.2f})")

    if block:
        decision = "BLOCK"
    elif risk >= 0.6 or compliance < 0.80:
        decision = "REVIEW"
    elif risk >= 0.5:
        decision = "RESTRICT"
    else:
        decision = "APPROVE"

    svs_r = round(eva_svs, 4)
    payload = f"{ev.model_id}:{decision}:{svs_r:.6f}:{risk:.6f}"
    seal = hmac.new(_SOV_KEY, payload.encode(), hashlib.sha256).hexdigest()
    latency = (time.perf_counter() - t0) * 1000

    return Verdict(ev.model_id, decision, round(eva_svs, 4), risk, compliance, round(stability, 4),
                   societal, round(di, 4), round(spd, 4), ev.ecs, sovereign, round(sov_svs, 3),
                   seal, round(latency, 3), block)


def verify_seal(model_id: str, decision: str, svs: float, risk: float, seal: str) -> bool:
    payload = f"{model_id}:{decision}:{svs:.6f}:{risk:.6f}"
    expected = hmac.new(_SOV_KEY, payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, seal)
