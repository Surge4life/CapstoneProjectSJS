"""
Governance bridge — multi-sector 6-D EVA + deterministic controllers.

Canonical scoring for platform-core decisions. Sector profiles re-weight dimensions and
thresholds so PUBLIC / PRIVATE / HEALTH / FINANCE / EDUCATION / JUSTICE / WELFARE /
GENERAL are inclusive of different duty-of-care postures without LLM controllers.

Pipeline (deterministic, ordered):
  1) Metric derivation (validity, confidence, risk, fairness, stability, impact, …)
  2) Sector weight profile + threshold profile
  3) Hard controllers (risk, DI, SPD, compliance, drift, ECS, sovereignty, sector duty)
  4) Soft escalate/review bands
  5) HMAC seal
"""
from __future__ import annotations

import hashlib
import hmac
import math
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

_SOV_KEY = os.environ.get("GODS_SOV_KEY", "emulated-sovereign-key").encode()

RISK_TIER_R = {
    "MINIMAL": 0.0,
    "NOTABLE": 0.2,
    "MEDIUM": 0.5,
    "HIGH": 0.8,
    "UNACCEPTABLE": 1.0,
}

W_DEFAULT = {
    "validity": 0.15,
    "confidence": 0.15,
    "risk": 0.25,
    "compliance": 0.20,
    "stability": 0.10,
    "societal": 0.15,
}

THRESH_DEFAULT = {
    "risk_block": 0.80,
    "compliance_block": 0.70,
    "di_block": 0.80,
    "jsd_block": 0.40,
    "ecs_block": 0.65,
    "spd_block": 0.05,
    "explainability_block": 0.35,
    "audit_block": 0.40,
    "inclusion_block": 0.45,
    "sov_min": 1.0,
}

SECTOR_PROFILES: Dict[str, Dict[str, Any]] = {
    "GENERAL": {
        "weights": dict(W_DEFAULT),
        "thresh": dict(THRESH_DEFAULT),
        "duty": "Baseline duty of care",
    },
    "PUBLIC": {
        "weights": {
            "validity": 0.12, "confidence": 0.12, "risk": 0.22,
            "compliance": 0.24, "stability": 0.10, "societal": 0.20,
        },
        "thresh": {**THRESH_DEFAULT, "compliance_block": 0.75, "di_block": 0.85, "spd_block": 0.04},
        "duty": "Constitutional public-duty · citizen impact elevated",
    },
    "PRIVATE": {
        "weights": {
            "validity": 0.14, "confidence": 0.16, "risk": 0.28,
            "compliance": 0.18, "stability": 0.12, "societal": 0.12,
        },
        "thresh": {**THRESH_DEFAULT, "risk_block": 0.78, "ecs_block": 0.60},
        "duty": "Commercial conduct · consumer fairness",
    },
    "HEALTH": {
        "weights": {
            "validity": 0.18, "confidence": 0.14, "risk": 0.28,
            "compliance": 0.18, "stability": 0.10, "societal": 0.12,
        },
        "thresh": {**THRESH_DEFAULT, "risk_block": 0.70, "compliance_block": 0.80, "di_block": 0.85},
        "duty": "Clinical / health-data duty · elevated risk floor",
    },
    "FINANCE": {
        "weights": {
            "validity": 0.14, "confidence": 0.16, "risk": 0.26,
            "compliance": 0.22, "stability": 0.12, "societal": 0.10,
        },
        "thresh": {**THRESH_DEFAULT, "di_block": 0.85, "spd_block": 0.04, "compliance_block": 0.78},
        "duty": "Conduct / lending fairness · disparate-impact strict",
    },
    "EDUCATION": {
        "weights": {
            "validity": 0.16, "confidence": 0.12, "risk": 0.20,
            "compliance": 0.18, "stability": 0.12, "societal": 0.22,
        },
        "thresh": {**THRESH_DEFAULT, "di_block": 0.85, "inclusion_block": 0.55},
        "duty": "Learner equity · inclusion floor elevated",
    },
    "JUSTICE": {
        "weights": {
            "validity": 0.18, "confidence": 0.12, "risk": 0.24,
            "compliance": 0.22, "stability": 0.10, "societal": 0.14,
        },
        "thresh": {**THRESH_DEFAULT, "risk_block": 0.70, "explainability_block": 0.50, "audit_block": 0.55},
        "duty": "Due process · explainability & audit floors elevated",
    },
    "WELFARE": {
        "weights": {
            "validity": 0.14, "confidence": 0.12, "risk": 0.22,
            "compliance": 0.20, "stability": 0.10, "societal": 0.22,
        },
        "thresh": {**THRESH_DEFAULT, "di_block": 0.85, "inclusion_block": 0.55, "spd_block": 0.04},
        "duty": "Benefit access equity · inclusion & fairness elevated",
    },
}

# Backward-compat module-level aliases used by policy_engine
W = W_DEFAULT
THRESH = THRESH_DEFAULT


def _norm_weights(w: Dict[str, float]) -> Dict[str, float]:
    s = sum(w.values()) or 1.0
    return {k: v / s for k, v in w.items()}


def resolve_sector(sector: Optional[str]) -> str:
    key = (sector or "GENERAL").strip().upper()
    aliases = {
        "GOV": "PUBLIC", "GOVERNMENT": "PUBLIC", "CITIZEN": "PUBLIC",
        "COMMERCIAL": "PRIVATE", "CORP": "PRIVATE",
        "BANKING": "FINANCE", "FS": "FINANCE",
        "MEDICAL": "HEALTH", "CLINICAL": "HEALTH",
        "SCHOOL": "EDUCATION",
        "COURT": "JUSTICE", "LEGAL": "JUSTICE",
        "SOCIAL": "WELFARE", "SASSA": "WELFARE",
    }
    key = aliases.get(key, key)
    return key if key in SECTOR_PROFILES else "GENERAL"


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
    ecs: float = 0.75
    bgp: float = 1.0
    traceroute: float = 1.0
    dnssec: float = 1.0
    storage: float = 1.0
    sector: str = "GENERAL"
    explainability: float = 0.85
    audit_trail: float = 0.90
    inclusion_access: float = 0.85
    human_oversight_present: bool = True


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
    validity: float = 0.0
    reliability: float = 0.0
    impact: float = 0.0
    composite_eva: float = 0.0
    dimensions: dict = field(default_factory=dict)
    sector: str = "GENERAL"
    scales: dict = field(default_factory=dict)
    controllers: list = field(default_factory=list)
    weights_used: dict = field(default_factory=dict)
    thresholds_used: dict = field(default_factory=dict)
    duty: str = ""


def _jsd(p, q):
    def kl(a, b):
        return sum(
            0.0 if ai == 0 else ai * math.log2(ai / (b[i] if b[i] else 1e-10))
            for i, ai in enumerate(a)
        )
    n = min(len(p), len(q))
    if n == 0:
        return 0.0
    p, q = p[:n], q[:n]
    m = [(p[i] + q[i]) / 2 for i in range(n)]
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def _pos_rate(fav, tot):
    return (fav / tot) if tot else 0.0


def _controller(name: str, fired: bool, severity: str, message: str) -> Dict[str, Any]:
    return {"controller": name, "fired": fired, "severity": severity, "message": message}


def evaluate(ev: Evidence) -> Verdict:
    """Sector-aware 6-D EVA + deterministic controller chain + sovereignty seal."""
    t0 = time.perf_counter()
    sector = resolve_sector(getattr(ev, "sector", None) or "GENERAL")
    profile = SECTOR_PROFILES[sector]
    Ww = _norm_weights(profile["weights"])
    THRESH = dict(profile["thresh"])
    duty = profile.get("duty", "")

    validity = max(0.0, min(1.0, ev.validity_correct / ev.validity_total)) if ev.validity_total else 0.0
    confidence = (
        ev.raw_confidence / (1 + math.log(ev.temperature + 1)) if ev.temperature > 0 else ev.raw_confidence
    )
    confidence = max(0.0, min(1.0, confidence))
    risk = RISK_TIER_R.get(ev.risk_tier, 0.5)
    compliance = max(0.0, min(1.0, float(ev.compliance)))
    jsd = _jsd(ev.current_dist, ev.baseline_dist)
    stability = max(0.0, 1 - jsd)

    pr_p = _pos_rate(ev.priv_favorable, ev.priv_total)
    pr_u = _pos_rate(ev.unpriv_favorable, ev.unpriv_total)
    di = (min(pr_p, pr_u) / max(pr_p, pr_u)) if max(pr_p, pr_u) > 0 else 1.0
    spd = pr_u - pr_p
    impact_sev = max(
        0.0,
        min(1.0, 0.4 * (1 - di) + 0.3 * min(1.0, abs(spd) / 0.2) + 0.3 * risk),
    )
    societal = 1 - impact_sev

    explainability = max(0.0, min(1.0, float(getattr(ev, "explainability", 0.85))))
    audit_trail = max(0.0, min(1.0, float(getattr(ev, "audit_trail", 0.90))))
    inclusion = max(0.0, min(1.0, float(getattr(ev, "inclusion_access", 0.85))))

    controllers: List[Dict[str, Any]] = []
    block: List[str] = []

    def hard(name: str, cond: bool, msg: str):
        controllers.append(_controller(name, cond, "BLOCK" if cond else "PASS", msg if cond else f"{name} clear"))
        if cond:
            block.append(msg)

    hard("RISK_CAP", risk >= THRESH["risk_block"], f"R={risk:.3f} ≥ {THRESH['risk_block']:.2f} (risk)")
    hard("COMPLIANCE_FLOOR", compliance < THRESH["compliance_block"],
         f"Co={compliance:.3f} < {THRESH['compliance_block']:.2f} (compliance)")
    hard("DISPARATE_IMPACT", di < THRESH["di_block"], f"DI={di:.3f} < {THRESH['di_block']:.2f} (disparate impact)")
    hard("STATISTICAL_PARITY", abs(spd) > THRESH["spd_block"], f"|SPD|={abs(spd):.3f} > {THRESH['spd_block']:.2f} (parity)")
    hard("DISTRIBUTION_DRIFT", jsd > THRESH["jsd_block"], f"JSD={jsd:.3f} > {THRESH['jsd_block']:.2f} (drift)")
    hard("ETHICAL_COOPERATION", ev.ecs < THRESH["ecs_block"], f"ECS={ev.ecs:.3f} < {THRESH['ecs_block']:.2f} (cooperation)")
    hard("UNACCEPTABLE_TIER", ev.risk_tier == "UNACCEPTABLE", "UNACCEPTABLE tier — permanent block")
    hard("EXPLAINABILITY", explainability < THRESH["explainability_block"],
         f"Explainability={explainability:.3f} < {THRESH['explainability_block']:.2f}")
    hard("AUDIT_TRAIL", audit_trail < THRESH["audit_block"],
         f"AuditTrail={audit_trail:.3f} < {THRESH['audit_block']:.2f}")
    hard("INCLUSION_ACCESS", inclusion < THRESH["inclusion_block"],
         f"Inclusion={inclusion:.3f} < {THRESH['inclusion_block']:.2f}")
    hitl_fail = (ev.risk_tier in ("HIGH", "UNACCEPTABLE")) and not bool(
        getattr(ev, "human_oversight_present", True)
    )
    hard("HITL_REQUIRED", hitl_fail, "High-risk system without human oversight present")

    eva_svs = min(
        max(
            Ww["validity"] * validity
            + Ww["confidence"] * confidence
            + Ww["risk"] * (1 - risk)
            + Ww["compliance"] * compliance
            + Ww["stability"] * stability
            + Ww["societal"] * societal,
            0.0,
        ),
        1.0,
    )
    composite_eva = round(eva_svs * 10, 2)

    dims = {
        "Validity": round(validity * 10, 1),
        "Confidence": round(confidence * 10, 1),
        "Risk": round(risk * 10, 1),
        "Compliance": round(compliance * 10, 1),
        "Stability": round(stability * 10, 1),
        "Impact": round(impact_sev * 10, 1),
    }
    scales = {
        "normalized_0_1": {
            "validity": round(validity, 4),
            "confidence": round(confidence, 4),
            "risk": round(risk, 4),
            "compliance": round(compliance, 4),
            "stability": round(stability, 4),
            "impact_severity": round(impact_sev, 4),
            "societal_quality": round(societal, 4),
            "disparate_impact": round(di, 4),
            "spd": round(spd, 4),
            "ecs": round(ev.ecs, 4),
            "explainability": round(explainability, 4),
            "audit_trail": round(audit_trail, 4),
            "inclusion_access": round(inclusion, 4),
            "composite": round(eva_svs, 4),
        },
        "scale_0_10": dict(dims),
        "scale_0_100": {k: round(v * 10, 1) for k, v in dims.items()},
        "composite_0_10": composite_eva,
        "composite_0_100": round(eva_svs * 100, 1),
    }

    sov_svs = min(ev.bgp, ev.traceroute, ev.dnssec, ev.storage)
    sovereign = sov_svs >= THRESH.get("sov_min", 1.0)
    if not sovereign:
        msg = f"Sovereignty breach (SVS={sov_svs:.2f})"
        block.append(msg)
        controllers.append(_controller("SOVEREIGNTY", True, "BLOCK", msg))
    else:
        controllers.append(_controller("SOVEREIGNTY", False, "PASS", "in-jurisdiction signals clean"))

    controllers.append(_controller("SECTOR_DUTY", False, "INFO", f"{sector}: {duty}"))

    if block:
        decision = "BLOCK"
    elif risk >= 0.6 or compliance < 0.80 or impact_sev >= 0.55 or eva_svs < 0.60:
        decision = "ESCALATE"
        controllers.append(_controller("BAND_ESCALATE", True, "ESCALATE", "soft band: elevated residual risk"))
    elif risk >= 0.5 or eva_svs < 0.75:
        decision = "REVIEW"
        controllers.append(_controller("BAND_REVIEW", True, "REVIEW", "soft band: review recommended"))
    else:
        decision = "APPROVE"
        controllers.append(_controller("BAND_APPROVE", True, "APPROVE", "all hard controllers clear"))

    svs_r = round(eva_svs, 4)
    payload = f"{ev.model_id}:{decision}:{svs_r:.6f}:{risk:.6f}:{sector}"
    seal = hmac.new(_SOV_KEY, payload.encode(), hashlib.sha256).hexdigest()
    latency = (time.perf_counter() - t0) * 1000

    return Verdict(
        model_id=ev.model_id, decision=decision, svs=round(eva_svs, 4), risk=risk,
        compliance=compliance, stability=round(stability, 4), societal=round(societal, 4),
        disparate_impact=round(di, 4), spd=round(spd, 4), ecs=ev.ecs, sovereign=sovereign,
        sovereign_svs=round(sov_svs, 3), seal=seal, latency_ms=round(latency, 3),
        block_reasons=block, validity=round(validity, 4), reliability=round(confidence, 4),
        impact=round(impact_sev, 4), composite_eva=composite_eva, dimensions=dims,
        sector=sector, scales=scales, controllers=controllers,
        weights_used={k: round(v, 4) for k, v in Ww.items()},
        thresholds_used={k: (round(v, 4) if isinstance(v, float) else v) for k, v in THRESH.items()},
        duty=duty,
    )


def seal_payload(payload: str) -> str:
    from app.services.crypto_provider import sign
    return sign(payload)


def verify_payload(payload: str, signature: str) -> bool:
    from app.services.crypto_provider import verify
    return verify(payload, signature)


def verify_seal(model_id: str, decision: str, svs: float, risk: float, seal: str) -> bool:
    for payload in (
        f"{model_id}:{decision}:{svs:.6f}:{risk:.6f}",
        f"{model_id}:{decision}:{svs:.6f}:{risk:.6f}:GENERAL",
    ):
        expected = hmac.new(_SOV_KEY, payload.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected, seal):
            return True
    return False


def list_sectors() -> List[Dict[str, Any]]:
    return [
        {"key": k, "duty": v.get("duty", ""), "weights": _norm_weights(v["weights"])}
        for k, v in SECTOR_PROFILES.items()
    ]
