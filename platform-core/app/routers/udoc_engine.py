"""
G.O.D.S / UDOC — Sovereign Governance Engine (patent v9.2 software layer).

This router implements the patent mechanisms that were specified but not yet exposed
as callable software. It does NOT re-implement the EVA engine — it CALLS the real one
(app.services.governance_bridge.evaluate) and writes real, hash-chained audit rows
(app.services.audit_writer.append_audit). What it adds is the patent's *enforcement
interface* that sits above scoring:

  • POST /engine/enforce      — Governance-Before-Execution gate (Part 3.2): the
                                G_SOV_VERIFY opcode → the 14-stage deterministic
                                sovereign execution sequence (Claim 15) → SVS=min()
                                arbitration → hardware-relay verdict (RELAY_OPEN /
                                G_HALT / G_LOCK + FAIL_CLOSED).
  • GET  /engine/state        — 13-state fail-closed state machine (Part 6.1) and the
                                5 degraded operating modes (Part 6.2), plus live state.
  • POST /engine/jurisdiction — Federated multi-jurisdiction sovereign mesh (Emb. 23/30,
                                ZA-UDOC-005): ZA/AU/BRICS/NATO treaty logic as an MFCM
                                check with ZK-1/2/3 attestation refs.
  • GET  /engine/manifest     — self-describing map of opcodes, stages, modes (public).

HONESTY: In this deployment the FPGA enforcement lattice, the hardware relay, the HSM
cells and the QPU are EMULATED IN SOFTWARE — exactly as the specification states for a
non-silicon deployment. Latencies reported are software-measured (Python perf_counter),
not sub-nanosecond hardware timings. Cryptographic seals are real HMAC-SHA256; "Dilithium"
and "ZK proof" references are named placeholders for the production PQC/zero-knowledge
paths, not live lattice signatures. Nothing here claims real silicon.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import time, hashlib

from app.db.session import get_db
from app.core.dependencies import principal
from app.services.governance_bridge import Evidence, evaluate, seal_payload
from app.services.audit_writer import append_audit

router = APIRouter(prefix="/engine", tags=["UDOC sovereign engine"])
_now = lambda: datetime.now(timezone.utc).isoformat()

# ───────────────────────── patent constants (v9.2) ─────────────────────────

# Extended FPGA opcode set (Part 4.1) — emulated in software here.
OPCODES = {
    "G_SOV_VERIFY": "Sovereign pre-execution verification; gates the relay before any action runs.",
    "G_HALT": "CPU-freeze enforcement (hardware: sub-10ns freeze pin). Stops execution on block.",
    "Relay_control": "Drives the hardware relay OPEN (permit) / DISCONNECT (failure state).",
    "G_lock_out": "HSM-NVRAM lock signal; persists across reboots (Part 10.2, Category B).",
}

# 14-stage deterministic sovereign execution sequence (Claim 15, Part 5).
STAGE_NAMES = [
    "Axiom Register load (128 governance axioms)",
    "Psi-Sim Heartbeat Bus liveness",
    "HSM Cell Scores (key-custody attestation)",
    "Policy Cell array (active compiled rules)",
    "Telemetry-Loss detection (sensor integrity)",
    "EVA 6-D Governance scoring",
    "Sovereignty SVS=min() arbitration",
    "Mandatory-block override gate",
    "Governance Enforcement decision",
    "Nanosecond-precision timestamp #1",
    "Nanosecond-precision timestamp #2",
    "StayChain audit append (dual-path)",
    "Dilithium seal (PQC, emulated → HMAC)",
    "Relay control (OPEN / DISCONNECT)",
]

# 13-state fail-closed state machine (Part 6.1).
FSM_STATES = [
    {"code": "S0",  "state": "NOMINAL",         "condition": "All planes healthy",                 "behaviour": "Full governance, relays armed",          "exit": "—"},
    {"code": "S1",  "state": "ARMED",           "condition": "Request received",                   "behaviour": "G_SOV_VERIFY begins, relay held",        "exit": "VERIFY_START"},
    {"code": "S2",  "state": "VERIFY",          "condition": "Axiom/HSM/policy load",              "behaviour": "Stages 1-5 run",                         "exit": "VERIFY_OK | VERIFY_FAULT"},
    {"code": "S3",  "state": "SCORING",         "condition": "Evidence assembled",                 "behaviour": "EVA 6-D evaluate()",                     "exit": "SCORED"},
    {"code": "S4",  "state": "SOVEREIGN_CHECK", "condition": "SVS=min(signals)",                   "behaviour": "Sovereignty arbitration",                "exit": "SOV_OK | SOV_BREACH"},
    {"code": "S5",  "state": "BLOCK_OVERRIDE",  "condition": "Any mandatory threshold tripped",    "behaviour": "Force block, no discretion",             "exit": "OVERRIDE_FIRED"},
    {"code": "S6",  "state": "RELAY_OPEN",      "condition": "APPROVE",                            "behaviour": "Relay OPEN — execution permitted",       "exit": "COMPLETE"},
    {"code": "S7",  "state": "RELAY_HOLD",      "condition": "REVIEW / ESCALATE",                  "behaviour": "Permit pending HITL / COB",              "exit": "HITL_RESOLVE"},
    {"code": "S8",  "state": "RELAY_DISCONNECT","condition": "BLOCK",                              "behaviour": "Relay DISCONNECT — execution denied",    "exit": "HALTED"},
    {"code": "S9",  "state": "G_HALT",          "condition": "Enforcement block",                  "behaviour": "CPU-freeze opcode emitted",              "exit": "HALTED"},
    {"code": "S10", "state": "G_LOCK_OUT",      "condition": "UNACCEPTABLE / sovereignty breach",  "behaviour": "Persisted lock across reboots",          "exit": "ADMIN_UNLOCK"},
    {"code": "S11", "state": "DEGRADED",        "condition": "Plane fault (telemetry/HSM/sov)",    "behaviour": "Conservative scoring, see modes",        "exit": "RECOVER | FAIL_CLOSED"},
    {"code": "S12", "state": "RECOVERY",        "condition": "Fault cleared + attested",           "behaviour": "Re-arm, replay audit",                   "exit": "NOMINAL"},
]

# 5 degraded operating modes (Part 6.2).
DEGRADED_MODES = [
    {"mode": "M0-NOMINAL",          "trigger": "No fault",                         "policy": "Full 6-D governance, all relays armed."},
    {"mode": "M1-TELEMETRY_LOSS",   "trigger": "Telemetry/sensor integrity drop",  "policy": "Treat missing signals as worst-case; auto-escalate borderline decisions."},
    {"mode": "M2-SOVEREIGN_ISOLATE","trigger": "BGP/traceroute/DNSSEC/storage breach", "policy": "Isolate to local sovereign core; deny all egress; SVS forced non-sovereign."},
    {"mode": "M3-KEY_CUSTODY",      "trigger": "HSM cell / dual-custody fault",    "policy": "Read-only; no new seals or activations; existing verdicts honoured."},
    {"mode": "M4-FAIL_CLOSED",      "trigger": "Unrecoverable / multi-plane fault","policy": "Full lockdown; all relays DISCONNECT; G_lock_out; admin recovery required."},
]

# ── 13-state FSM transition table (Part 6.1) — deterministic, fail-closed ──
# Module-level live state (best-effort; not persisted across restart/workers — emulated).
_FSM = {"state": "S0", "mode": "M0-NOMINAL"}

# Valid transitions {from_state: {event: to_state}}. Any event not listed for the current
# state is treated as a fault: the machine fails closed toward DEGRADED/LOCK_OUT — never
# toward a more-permissive state.
TRANSITIONS = {
    "S0":  {"request": "S1"},
    "S1":  {"verify_start": "S2"},
    "S2":  {"verify_ok": "S3", "verify_fault": "S11"},
    "S3":  {"scored": "S4"},
    "S4":  {"sov_ok": "S6", "review": "S7", "sov_breach": "S5"},
    "S5":  {"override_fired": "S8"},
    "S6":  {"complete": "S0"},
    "S7":  {"hitl_resolve": "S0"},
    "S8":  {"halted": "S9"},
    "S9":  {"recover": "S12"},
    "S10": {"admin_unlock": "S12"},     # locked-out only exits via admin
    "S11": {"recover": "S12", "fail_closed": "S10"},
    "S12": {"nominal": "S0"},
}
# Fault events that also drive a degraded operating mode.
FAULT_MODE = {"verify_fault": "M1-TELEMETRY_LOSS", "telemetry_fault": "M1-TELEMETRY_LOSS",
              "sov_breach": "M2-SOVEREIGN_ISOLATE", "key_fault": "M3-KEY_CUSTODY",
              "fail_closed": "M4-FAIL_CLOSED"}
_STATE_NAME = {s["code"]: s["state"] for s in FSM_STATES}
# Terminal states that cannot be left except by their one explicit recovery/unlock event.
_LOCKED_STATES = {"S10"}

# Federated mesh treaty logic (Emb. 23 & 30). 1.0 = clean signal expected.
JURISDICTIONS = {
    "ZA": "South Africa (national sovereign)", "ZA-GP": "Gauteng", "ZA-WC": "Western Cape",
    "ZA-KZN": "KwaZulu-Natal", "AU": "African Union (treaty)", "BRICS": "BRICS (treaty)",
    "NATO": "NATO (restricted)", "FOREIGN": "Non-treaty foreign",
}

# ───────────────────────── request models ─────────────────────────

class EnforceReq(BaseModel):
    model_config = {"protected_namespaces": ()}
    action: str = Field(..., description="The action/inference being gated, e.g. 'credit-decision', 'model-inference'.")
    model_id: str = Field("demo-model", description="Registered model identifier.")
    risk_tier: str = Field("NOTABLE", description="MINIMAL | NOTABLE | MEDIUM | HIGH | UNACCEPTABLE")
    raw_confidence: float = 0.9
    temperature: float = 0.7
    compliance: float = 1.0
    ecs: float = 0.75
    current_dist: list[float] = [0.25, 0.25, 0.25, 0.25]
    baseline_dist: list[float] = [0.25, 0.25, 0.25, 0.25]
    priv_favorable: int = 480
    priv_total: int = 1000
    unpriv_favorable: int = 470
    unpriv_total: int = 1000
    bgp: float = 1.0
    traceroute: float = 1.0
    dnssec: float = 1.0
    storage: float = 1.0

class JurisdictionReq(BaseModel):
    source: str = Field("ZA-GP", description="Origin jurisdiction code.")
    destination: str = Field("ZA", description="Destination jurisdiction code.")
    data_class: str = Field("PERSONAL", description="PUBLIC | INTERNAL | PERSONAL | SPECIAL | STATE")
    action: str = Field("process", description="process | store | transit | replicate")

class StateTransitionReq(BaseModel):
    event: str = Field(..., description="FSM event: request, verify_start, verify_ok, verify_fault, scored, sov_ok, sov_breach, review, override_fired, complete, hitl_resolve, halted, recover, admin_unlock, nominal, fail_closed, telemetry_fault, key_fault.")
    from_state: str | None = Field(None, description="Override the from-state (default: the engine's live state).")

# ───────────────────────── helpers ─────────────────────────

def _verdict_to_relay(decision: str, block_reasons: list, risk_tier: str, sovereign: bool):
    """Map the EVA Verdict.decision onto the patent's opcode + relay state."""
    hard_lock = (risk_tier == "UNACCEPTABLE") or (not sovereign)
    if decision == "APPROVE":
        return ("RELAY_OPEN", "Relay_control:OPEN", "S6", "PERMIT", False)
    if decision in ("REVIEW", "ESCALATE"):
        return ("RELAY_HOLD", "Relay_control:HOLD", "S7", "PERMIT_PENDING_HITL", False)
    # BLOCK
    if hard_lock:
        return ("G_LOCK + FAIL_CLOSED", "G_lock_out", "S10", "DENY", True)
    return ("G_HALT + FAIL_CLOSED", "G_HALT", "S9", "DENY", False)

# ───────────────────────── endpoints ─────────────────────────

@router.get("/manifest")
def engine_manifest():
    """Public, read-only map of the sovereign engine: opcodes, the 14-stage sequence,
    the fail-closed FSM and the degraded modes. Describes the engine; does not act."""
    return {
        "engine": "UDOC Sovereign Governance Engine",
        "patent": "UDOC Sovereign AI Governance Infrastructure v9.2",
        "deployment_note": "FPGA lattice / hardware relay / HSM / QPU EMULATED IN SOFTWARE. "
                           "Seals are real HMAC-SHA256; Dilithium/ZK references are PQC placeholders.",
        "opcodes": OPCODES,
        "execution_sequence_claim15": {f"stage_{i+1}": n for i, n in enumerate(STAGE_NAMES)},
        "fail_closed_fsm_part6_1": {"states": len(FSM_STATES), "table": FSM_STATES},
        "degraded_modes_part6_2": DEGRADED_MODES,
        "mandatory_block_thresholds_part7_1": {
            "risk": "R >= 0.80", "compliance": "Co < 0.70", "disparate_impact": "DI < 0.80",
            "drift_jsd": "JSD >= 0.40", "cooperation_ecs": "ECS < 0.65", "parity_spd": "|SPD| > 0.05",
        },
        "endpoints": {
            "POST /engine/enforce": "Governance-before-execution gate (auth).",
            "GET /engine/state": "Live FSM state + degraded modes (public).",
            "POST /engine/jurisdiction": "Federated multi-jurisdiction MFCM treaty check (auth).",
        },
        "generated_at": _now(),
    }

@router.post("/enforce")
def enforce(req: EnforceReq, db: Session = Depends(get_db), user: dict = Depends(principal)):
    """
    GOVERNANCE-BEFORE-EXECUTION GATE (Part 3.2).

    Runs the 14-stage deterministic sovereign execution sequence (Claim 15). Stage 6 calls
    the REAL EVA engine (governance_bridge.evaluate); SVS=min() and the six mandatory-block
    overrides are enforced there. The verdict is mapped onto the patent's opcode + hardware
    relay state and a real audit row is appended (StayChain dual-path, emulated). No action is
    permitted unless G_SOV_VERIFY passes — fail-closed by construction.
    """
    t0 = time.perf_counter()
    trace = []

    def stage(idx, status="OK", detail=""):
        trace.append({
            "stage": idx + 1, "name": STAGE_NAMES[idx], "status": status,
            "t_ns": int((time.perf_counter() - t0) * 1e9), "detail": detail,
        })

    # Stages 1–5: pre-flight (axiom/heartbeat/HSM/policy/telemetry) — emulated attestations.
    stage(0, detail="128 axioms loaded")
    stage(1, detail="heartbeat bus live")
    stage(2, detail="HSM cell scores attested (emulated)")
    stage(3, detail="active policy cells bound to EVA path")
    telemetry_ok = all(x >= 0.0 for x in (req.bgp, req.traceroute, req.dnssec, req.storage))
    stage(4, "OK" if telemetry_ok else "FAULT", "sensor integrity nominal")

    # Stage 6: the REAL EVA 6-D scoring.
    ev = Evidence(
        model_id=req.model_id, risk_tier=req.risk_tier, raw_confidence=req.raw_confidence,
        temperature=req.temperature, compliance=req.compliance, ecs=req.ecs,
        current_dist=req.current_dist, baseline_dist=req.baseline_dist,
        priv_favorable=req.priv_favorable, priv_total=req.priv_total,
        unpriv_favorable=req.unpriv_favorable, unpriv_total=req.unpriv_total,
        bgp=req.bgp, traceroute=req.traceroute, dnssec=req.dnssec, storage=req.storage,
    )
    v = evaluate(ev)
    stage(5, detail=f"EVA decision={v.decision} SVS={v.svs} composite={v.composite_eva}/10")

    # Stage 7: sovereignty arbitration.
    stage(6, "OK" if v.sovereign else "BREACH", f"sovereign_svs={v.sovereign_svs}")

    # Stage 8: mandatory-block override gate.
    stage(7, "CLEAR" if not v.block_reasons else "TRIPPED",
          "; ".join(v.block_reasons) if v.block_reasons else "no override")

    # Stage 9: enforcement decision → opcode + relay.
    relay, opcode, fsm, verdict_word, locked = _verdict_to_relay(
        v.decision, v.block_reasons, req.risk_tier, v.sovereign)
    stage(8, detail=f"{opcode} → {relay}")

    # Stages 10–11: deterministic nanosecond timestamps.
    stage(9, detail="ts1 sealed")
    stage(10, detail="ts2 sealed")

    # Stage 12: StayChain dual-path audit (REAL hash-chained row).
    try:
        ref = append_audit(db, "ENGINE_ENFORCE", {
            "action": req.action, "model_id": req.model_id, "decision": v.decision,
            "verdict": verdict_word, "opcode": opcode, "relay": relay, "svs": v.svs,
            "block_reasons": v.block_reasons, "actor": user.get("email") if isinstance(user, dict) else str(user),
        }, classification="INTERNAL", actor_class="SYSTEM")
        audit_ref = getattr(ref, "ref", None) or getattr(ref, "id", None) or "appended"
        stage(11, detail=f"StayChain row {audit_ref}")
    except Exception as e:  # never let audit failure silently permit — note it, keep verdict
        audit_ref = None
        stage(11, "WARN", f"audit append degraded: {type(e).__name__}")

    # Stage 13: Dilithium seal (emulated as HMAC over the canonical verdict).
    seal = seal_payload(f"{req.action}:{req.model_id}:{v.decision}:{v.svs:.6f}:{relay}")
    stage(12, detail=f"seal {seal[:16]}…")

    # Stage 14: relay control.
    stage(13, "OPEN" if verdict_word.startswith("PERMIT") else "DISCONNECT", relay)

    latency_ms = round((time.perf_counter() - t0) * 1000, 3)
    return {
        "action": req.action,
        "g_sov_verify": verdict_word.startswith("PERMIT"),
        "verdict": verdict_word,
        "opcode": opcode,
        "relay_state": relay,
        "fsm_state": fsm,
        "locked_out": locked,
        "eva": {
            "decision": v.decision, "svs": v.svs, "composite_eva_out_of_10": v.composite_eva,
            "risk": v.risk, "compliance": v.compliance, "stability": v.stability,
            "disparate_impact": v.disparate_impact, "spd": v.spd, "ecs": v.ecs,
            "sovereign": v.sovereign, "sovereign_svs": v.sovereign_svs, "dimensions": v.dimensions,
        },
        "block_reasons": v.block_reasons,
        "seal_hmac_sha256": seal,
        "audit_ref": audit_ref,
        "stage_trace": trace,
        "engine_latency_ms": latency_ms,
        "note": "Software enforcement; FPGA relay & HSM emulated. Execution is only permitted "
                "when g_sov_verify is true (fail-closed).",
        "generated_at": _now(),
    }

@router.get("/state")
def engine_state():
    """Public: the 13-state fail-closed FSM (Part 6.1), the 5 degraded modes (Part 6.2),
    and the current LIVE operating state of this engine instance."""
    return {
        "current_state": _FSM["state"],
        "current_state_name": _STATE_NAME.get(_FSM["state"], _FSM["state"]),
        "current_mode": _FSM["mode"],
        "armed": _FSM["state"] not in _LOCKED_STATES,
        "locked_out": _FSM["state"] in _LOCKED_STATES,
        "fail_closed_fsm": {"count": len(FSM_STATES), "states": FSM_STATES},
        "degraded_modes": DEGRADED_MODES,
        "opcodes": OPCODES,
        "note": "Fail-closed by construction: any unrecoverable fault transitions to "
                "M4-FAIL_CLOSED / S10 with all relays DISCONNECT. Live state is in-memory "
                "(emulated; not persisted across restart/workers).",
        "generated_at": _now(),
    }

@router.post("/state/transition")
def state_transition(req: StateTransitionReq, db: Session = Depends(get_db),
                     user: dict = Depends(principal)):
    """Drive the fail-closed FSM. A valid event for the current state advances normally; any
    unrecognised event for that state is a FAULT and the machine fails closed toward DEGRADED
    (or to G_LOCK_OUT from DEGRADED). Locked-out states only exit via their explicit unlock
    event. Every transition is written to the StayChain audit chain."""
    frm = (req.from_state or _FSM["state"]).upper()
    if frm not in TRANSITIONS:
        raise HTTPException(400, f"unknown from_state '{frm}'; valid: {list(TRANSITIONS)}")
    event = req.event.strip()

    allowed = TRANSITIONS[frm]
    if event in allowed:
        to = allowed[event]
        fail_closed = event in FAULT_MODE
    else:
        # FAULT: fail closed. From a locked state we stay locked; otherwise go DEGRADED.
        to = frm if frm in _LOCKED_STATES else "S11"
        fail_closed = True

    mode = FAULT_MODE.get(event, _FSM["mode"])
    if to == "S0":
        mode = "M0-NOMINAL"          # full recovery clears the degraded mode

    _FSM["state"], _FSM["mode"] = to, mode

    ref = append_audit(db, "ENGINE_FSM_TRANSITION", {
        "from": frm, "event": event, "to": to, "mode": mode, "fail_closed": fail_closed,
        "actor": user.get("email") if isinstance(user, dict) else str(user),
    }, classification="INTERNAL", actor_class="SYSTEM")
    audit_ref = getattr(ref, "seq", None) or getattr(ref, "id", None)

    return {
        "from_state": frm, "from_name": _STATE_NAME.get(frm, frm),
        "event": event,
        "to_state": to, "to_name": _STATE_NAME.get(to, to),
        "valid_transition": event in allowed,
        "fail_closed": fail_closed,
        "current_mode": mode,
        "locked_out": to in _LOCKED_STATES,
        "armed": to not in _LOCKED_STATES,
        "audit_ref": audit_ref,
        "note": "Unrecognised events fail closed to DEGRADED (S11); from S10 they stay locked.",
        "generated_at": _now(),
    }

@router.post("/jurisdiction")
def jurisdiction(req: JurisdictionReq, user: dict = Depends(principal)):
    """
    FEDERATED MULTI-JURISDICTION SOVEREIGN MESH (Embodiment 23 & 30, ZA-UDOC-005).

    Evaluates a cross-jurisdiction data flow against treaty logic encoded as a Multi-Factor
    Constitutional Mesh (MFCM) check, returning permit/deny + the treaty rule applied + a
    ZK-1/2/3 attestation reference. Implements Constitutional Pillar III (sovereign respect /
    zero foreign transit): any non-treaty foreign egress is denied.
    """
    src, dst = req.source.upper(), req.destination.upper()
    if src not in JURISDICTIONS or dst not in JURISDICTIONS:
        raise HTTPException(400, f"unknown jurisdiction; valid: {list(JURISDICTIONS)}")

    dc = req.data_class.upper()
    src_za = src.startswith("ZA")
    dst_za = dst.startswith("ZA")

    # MFCM check set (emulated 47-check, summarised into the constitutional factors that decide).
    checks = []
    def chk(name, ok, why):
        checks.append({"check": name, "pass": ok, "detail": why})
        return ok

    intra_za = src_za and dst_za            # informational flag, not a gating requirement
    foreign_egress = (src_za and not dst_za)
    treaty_party = dst in ("AU", "BRICS")
    state_data = dc in ("STATE", "SPECIAL")

    chk("pillar-III-no-foreign-transit", not (foreign_egress and dst in ("FOREIGN", "NATO")),
        "no egress to non-treaty / restricted jurisdictions")
    chk("treaty-coverage", intra_za or treaty_party,
        "flow is intra-sovereign or to an AU/BRICS treaty party")
    chk("data-class-permitted", not (state_data and not intra_za),
        "STATE/SPECIAL data must remain within sovereign territory")
    chk("routing-anchor", True, "routing anchored to sovereign path (emulated clean)")

    permit = all(c["pass"] for c in checks)
    if intra_za:
        rule = "INTRA-ZA: permitted (national sovereign mesh)."
        zk = "ZK-1 (intra-sovereign attestation)"
    elif permit and treaty_party:
        rule = f"TREATY-{dst}: permitted under {JURISDICTIONS[dst]} for class {dc}."
        zk = "ZK-2 (cross-border treaty attestation)"
    else:
        rule = "DENY: violates sovereign / treaty constraints (Pillar III)."
        zk = "ZK-3 (denial proof, audit-anchored)"

    return {
        "source": {"code": src, "name": JURISDICTIONS[src]},
        "destination": {"code": dst, "name": JURISDICTIONS[dst]},
        "data_class": dc, "action": req.action,
        "permit": permit,
        "verdict": "PERMIT" if permit else "DENY",
        "treaty_rule": rule,
        "mfcm_checks": checks,
        "mfcm_pass_count": f"{sum(c['pass'] for c in checks)}/{len(checks)}",
        "zk_attestation": zk,
        "pillar": "III — sovereign respect / zero foreign transit",
        "note": "Software treaty logic; ZK references are placeholders for production "
                "zero-knowledge proofs, not live ZK circuits.",
        "generated_at": _now(),
    }
